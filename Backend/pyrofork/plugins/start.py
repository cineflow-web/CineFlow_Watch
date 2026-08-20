from datetime import datetime

from pyrogram import Client, enums, filters
from pyrogram.types import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Message

from Backend import db
from Backend.config import Telegram
from Backend.helper.settings_manager import SettingsManager
from Backend.logger import LOGGER

def _currency_symbol(code):
    return {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "AUD": "A$", "CAD": "C$", "SGD": "S$", "AED": "د.إ", "BRL": "R$"}.get((code or "INR").upper(), f"{(code or 'INR')} ")



#----- /start: hand out the Stremio addon link, gated by subscription state
@Client.on_message(filters.command('start') & filters.private, group=10)
async def send_start_message(client: Client, message: Message):
    try:
        user_id = (message.from_user.id if message.from_user else None) or (message.sender_chat.id if message.sender_chat else None) or message.chat.id
        base_url = SettingsManager.current().base_url
        addon_url = f"{base_url}/stremio/manifest.json"

        #----- No subscription mode: owner-only, single personal token
        if not SettingsManager.current().subscription:
            if user_id != Telegram.OWNER_ID:
                return
            user_name = (message.from_user.first_name or message.from_user.username or f"User {user_id}") if message.from_user else f"Chat {user_id}"
            try:
                token_doc = await db.add_api_token(name=user_name, user_id=user_id)
                addon_url = f"{base_url}/stremio/{token_doc.get('token')}/manifest.json"
            except Exception as e:
                LOGGER.error(f"Error ensuring token for free user: {e}")

            await message.reply_text(
                '🎉 <b>Welcome to the CineFlow Media Server!</b>\n\n'
                'Here is your personal Stremio Addon link:\n\n'
                '🎬 <b>Stremio Addon — Install Link:</b>\n'
                f'<code>{addon_url}</code>\n\n'
                'Tap the link above → <b>Install</b> in Stremio to start watching!',
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )
            return

        #----- Subscription mode: verify active subscription, else offer plans
        user = await db.get_user(user_id)
        now = datetime.utcnow()

        #----- If a payment is already pending (e.g. plan picked on the web configure page),
        #----- show those package details right away instead of the generic welcome text —
        #----- this is what "Send Screenshot on Telegram" from the web page lands on.
        pending = user.get("pending_payment") if user else None
        if pending:
            settings = SettingsManager.current()
            duration = pending.get("duration", "?")
            price = pending.get("price", 0)
            currency = pending.get("currency", "INR")
            sym = _currency_symbol(currency)

            payment_instructions = settings.payment_instructions
            payment_qr_url = settings.payment_qr_url

            text = (
                f"<b>📦 Pending Payment</b>\n\n"
                f"<b>Plan:</b> {duration} Days\n"
                f"<b>Price:</b> {sym}{price}\n\n"
                f"<b>📋 How to Pay:</b>\n"
            )
            text += f"{payment_instructions}\n\n" if payment_instructions else f"Pay {sym}{price} to the admin.\n\n"
            text += (
                "<b>After paying:</b> send your payment screenshot directly here "
                "(in this chat). The admin will review and activate your subscription."
            )

            if payment_qr_url:
                try:
                    await client.send_photo(chat_id=user_id, photo=payment_qr_url, caption=f"📷 Scan to pay {sym}{price}")
                except Exception as e:
                    LOGGER.warning(f"Could not send payment QR to {user_id}: {e}")

            return await message.reply_text(
                text,
                reply_markup=ForceReply(selective=True),
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )

        #----- Owner / admin / never-expiring (subscription_exempt) tokens don't buy
        #----- plans — they never see plan-selection or renew buttons, no matter
        #----- what their subscription record looks like.
        token_doc = await db.get_api_token_by_user(user_id)
        is_no_expiry = (
            user_id == Telegram.OWNER_ID
            or bool(token_doc and (token_doc.get("is_admin") or token_doc.get("subscription_exempt")))
        )

        if is_no_expiry:
            user_name = (user.get("first_name") or user.get("username")) if user else None
            if not token_doc:
                token_doc = await db.ensure_api_token_for_user(user_id, user_name)
            if token_doc and token_doc.get("token"):
                addon_url = f"{base_url}/stremio/{token_doc['token']}/manifest.json"

            return await message.reply_text(
                '🎉 <b>Welcome back to the CineFlow Subscription Manager!</b>\n\n'
                '🎬 <b>Stremio Addon — Install Link:</b>\n'
                f'<code>{addon_url}</code>\n\n'
                'Tap the link above → <b>Install</b> in Stremio to start watching!',
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )

        is_active = db.is_subscription_active(user, now)
        if not is_active and user and user.get("subscription_status") == "active":
            await db.mark_user_expired(user_id)

        #----- Honour a manual token grant (a future fixed token expiry, e.g. set
        #----- via update_token_expiry) — subscription_exempt is already handled above.
        if not is_active:
            if token_doc and token_doc.get("expires_at") and token_doc["expires_at"] > now:
                is_active = True

        if not is_active:
            plans = await db.get_subscription_plans()
            if not plans:
                return await message.reply_text(
                    '<b>Welcome to the CineFlow Private Group!</b>\n\n'
                    'Currently, no subscription plans are set up. Please contact the administrator.',
                    quote=True,
                    parse_mode=enums.ParseMode.HTML
                )

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"{plan['days']} Days - {_currency_symbol(plan.get('currency'))}{plan['price']}", callback_data=f"plan_{plan['_id']}")]
                for plan in plans
            ])
            return await message.reply_text(
                '<b>Welcome to the CineFlow Private Group!</b>\n\n'
                'Access to this bot and the Stremio Addon requires an active subscription.\n'
                'Please select a subscription plan below to continue:',
                reply_markup=keyboard,
                quote=True,
                parse_mode=enums.ParseMode.HTML
            )

        #----- Active subscriber: return their token link, creating one if missing
        user_name = (user.get("first_name") or user.get("username")) if user else None
        token_doc = await db.ensure_api_token_for_user(user_id, user_name)
        if token_doc and token_doc.get("token"):
            addon_url = f"{base_url}/stremio/{token_doc['token']}/manifest.json"

        #----- Show which plan they're on and when it expires, not just the addon link
        expiry = user.get("subscription_expiry") if user else None
        current_plan = user.get("current_plan") if user else None
        status_lines = []
        if current_plan:
            status_lines.append(
                f"📦 <b>Current Plan:</b> {current_plan.get('duration', '?')} days "
                f"({_currency_symbol(current_plan.get('currency'))}{current_plan.get('price', '?')})"
            )
        if expiry:
            status_lines.append(f"📅 <b>Expires:</b> {expiry.strftime('%Y-%m-%d')} UTC")
        status_block = ("\n".join(status_lines) + "\n\n") if status_lines else ""

        text = (
            '🎉 <b>Welcome back to the CineFlow Subscription Manager!</b>\n\n'
            f'{status_block}'
            '🎬 <b>Stremio Addon — Install Link:</b>\n'
            f'<code>{addon_url}</code>\n\n'
            'Tap the link above → <b>Install</b> in Stremio to start watching!'
        )

        #----- Offer a Renew option even though the subscription is still active
        keyboard = None
        plans = await db.get_subscription_plans()
        if plans:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(f"🔄 Renew — {plan['days']} Days ({_currency_symbol(plan.get('currency'))}{plan['price']})", callback_data=f"plan_{plan['_id']}")]
                for plan in plans
            ])

        await message.reply_text(
            text,
            reply_markup=keyboard,
            quote=True,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")
        LOGGER.error(f"Error in /start handler: {e}")

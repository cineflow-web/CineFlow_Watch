DEFAULT_THEME = "dracula"

# Official Dracula palette — https://draculatheme.com/contribute
THEMES = {
    "dracula": {
        "name": "Dracula",
        "is_dark": True,
        "colors": {
            "primary": "#BD93F9",        # Purple
            "secondary": "#FF79C6",      # Pink
            "accent": "#8BE9FD",         # Cyan
            "background": "#282A36",     # Background
            "card": "#21222C",           # Darker panel
            "border": "#44475A",         # Current Line / Selection
            "text": "#F8F8F2",           # Foreground
            "text_secondary": "#6272A4"  # Comment
        },
        "css_classes": "theme-dracula"
    },
    "nord": {
        "name": "Nord",
        "is_dark": True,
        "colors": {
            "primary": "#88C0D0",        # Frost — cyan
            "secondary": "#B48EAD",      # Aurora — purple
            "accent": "#8FBCBB",         # Frost — teal
            "background": "#2E3440",     # Polar Night — nord0
            "card": "#3B4252",           # Polar Night — nord1
            "border": "#4C566A",         # Polar Night — nord3
            "text": "#ECEFF4",           # Snow Storm — nord6
            "text_secondary": "#81A1C1"  # Frost — blue
        },
        "css_classes": "theme-nord"
    }
}


#----- Resolve a theme by name, falling back to the default (always Dracula)
def get_theme(theme_name: str = DEFAULT_THEME):
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


#----- Return the full theme registry
def get_all_themes():
    return THEMES

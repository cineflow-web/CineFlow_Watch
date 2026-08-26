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
    },
    "tokyo_night": {
        "name": "Tokyo Night",
        "is_dark": True,
        "colors": {
            "primary": "#7AA2F7",        # Blue
            "secondary": "#BB9AF7",      # Purple
            "accent": "#7DCFFF",         # Cyan
            "background": "#1A1B26",     # Night background
            "card": "#16161E",           # Darker panel
            "border": "#292E42",         # Storm border
            "text": "#C0CAF5",           # Foreground
            "text_secondary": "#565F89"  # Comment
        },
        "css_classes": "theme-tokyo-night"
    },
    "catppuccin_mocha": {
        "name": "Catppuccin Mocha",
        "is_dark": True,
        "colors": {
            "primary": "#CBA6F7",        # Mauve
            "secondary": "#F5C2E7",      # Pink
            "accent": "#89DCEB",         # Sky
            "background": "#1E1E2E",     # Base
            "card": "#181825",           # Mantle
            "border": "#313244",         # Surface0
            "text": "#CDD6F4",           # Text
            "text_secondary": "#6C7086"  # Overlay0
        },
        "css_classes": "theme-catppuccin-mocha"
    },
    "solarized_dark": {
        "name": "Solarized Dark",
        "is_dark": True,
        "colors": {
            "primary": "#268BD2",        # Blue
            "secondary": "#D33682",      # Magenta
            "accent": "#2AA198",         # Cyan
            "background": "#002B36",     # base03
            "card": "#073642",           # base02
            "border": "#586E75",         # base01
            "text": "#EEE8D5",           # base2
            "text_secondary": "#657B83"  # base00
        },
        "css_classes": "theme-solarized-dark"
    },
    "gruvbox_dark": {
        "name": "Gruvbox Dark",
        "is_dark": True,
        "colors": {
            "primary": "#FE8019",        # Orange
            "secondary": "#FABD2F",      # Yellow
            "accent": "#83A598",         # Aqua
            "background": "#282828",     # bg0
            "card": "#1D2021",           # bg0_h
            "border": "#504945",         # bg2
            "text": "#EBDBB2",           # fg
            "text_secondary": "#928374"  # gray
        },
        "css_classes": "theme-gruvbox-dark"
    },
    "material_gray": {
        "name": "Material Gray & White",
        "is_dark": False,
        "colors": {
            "primary": "#1976D2",        # Material blue 700
            "secondary": "#757575",      # Gray 600
            "accent": "#00BCD4",         # Cyan 500
            "background": "#FAFAFA",     # Gray 50
            "card": "#FFFFFF",           # White
            "border": "#E0E0E0",         # Gray 300
            "text": "#212121",           # Gray 900
            "text_secondary": "#757575"  # Gray 600
        },
        "css_classes": "theme-material-gray"
    },
    "slate_gray": {
        "name": "Slate Gray",
        "is_dark": True,
        "colors": {
            "primary": "#90A4AE",        # Blue gray 300
            "secondary": "#78909C",      # Blue gray 400
            "accent": "#B0BEC5",         # Blue gray 200
            "background": "#121212",     # Material dark base
            "card": "#1E1E1E",           # Elevated panel
            "border": "#2E2E2E",         # Hairline
            "text": "#E8E8E8",           # Near-white
            "text_secondary": "#9E9E9E"  # Gray 500
        },
        "css_classes": "theme-slate-gray"
    },
    "aurora": {
        "name": "Aurora",
        "is_dark": True,
        "colors": {
            "primary": "#FF6B6B",        # Coral
            "secondary": "#4ECDC4",      # Teal
            "accent": "#FFE66D",         # Yellow
            "background": "#1A1A2E",     # Deep navy
            "card": "#16213E",           # Panel navy
            "border": "#0F3460",         # Border blue
            "text": "#EAEAEA",           # Off-white
            "text_secondary": "#A0A0C0"  # Muted lavender-gray
        },
        "css_classes": "theme-aurora"
    }
}


#----- Resolve a theme by name, falling back to the default (always Dracula)
def get_theme(theme_name: str = DEFAULT_THEME):
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


#----- Return the full theme registry
def get_all_themes():
    return THEMES

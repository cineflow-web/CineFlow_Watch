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
    }
}


#----- Resolve a theme by name, falling back to the default (always Dracula)
def get_theme(theme_name: str = DEFAULT_THEME):
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


#----- Return the full theme registry
def get_all_themes():
    return THEMES

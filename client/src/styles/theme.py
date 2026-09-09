# Define modern palette
COLORS = {
    "bg_window": "#0B0F17",
    "bg_card": "#151C28",
    "border": "#263346",
    "text_primary": "#F8FAFC",
    "text_muted": "#94A3B8",
    "accent": "#2563EB",
    "accent_hover": "#3B82F6",
    "accent_pressed": "#1D4ED8",
    "input_bg": "#0F172A",
    "input_focus": "#38BDF8",
    "error_bg": "#7F1D1D",
    "error_text": "#F87171"
}

DARK_THEME_QSS = f"""
    QWidget {{
        color: {COLORS['text_primary']};
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }}
    QMainWindow {{
        background-color: {COLORS['bg_window']};
    }}
    QLineEdit {{
        background-color: {COLORS['input_bg']};
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 14px;
        color: {COLORS['text_primary']};
    }}
    QLineEdit:focus {{
        border: 2px solid {COLORS['input_focus']};
    }}
    QPushButton {{
        background-color: {COLORS['accent']};
        color: white;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px;
        font-size: 14px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['accent_hover']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['accent_pressed']};
    }}
"""

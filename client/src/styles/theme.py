# Premium Dark Theme Palette for Anexa Academy
COLORS = {
    # Background Colors
    "bg_window": "#0F1017",              # Deep dark background
    "bg_window_secondary": "#161822",    # Secondary background
    "bg_card": "#1F2232",                # Card/Panel background
    "bg_card_hover": "#26293D",          # Card hover state
    "bg_input": "#0A0B12",               # Input field background
    "bg_sidebar": "#08090E",             # Sidebar background
    
    # Border Colors
    "border": "#2E324A",                # Default border
    "border_light": "#3A3F5A",          # Light border
    "border_focus": "#6C5CE7",          # Focus border (accent)
    
    # Text Colors
    "text_primary": "#FFFFFF",           # Primary text
    "text_secondary": "#A0A5C0",        # Secondary text
    "text_muted": "#6B7285",            # Muted text
    "text_disabled": "#4B5563",         # Disabled text
    
    # Accent Colors - Electric Violet & Cyan
    "accent": "#6C5CE7",                # Primary accent (Electric Violet)
    "accent_hover": "#8C7AE6",          # Accent hover
    "accent_pressed": "#5B4CC5",        # Accent pressed
    "accent_secondary": "#00CEC9",      # Secondary accent (Cyan)
    "accent_secondary_hover": "#00E5DE", # Secondary accent hover
    
    # Status Colors
    "success": "#00CEC9",               # Cyan for success
    "success_bg": "#0A3A3A",            # Success background
    "error": "#FF6B6B",                # Red for error
    "error_text": "#FFB8B8",           # Light red for error text
    "error_bg": "#3A1515",              # Error background
    "warning": "#FDCB6E",               # Orange for warning
    "warning_bg": "#3A2A15",            # Warning background
    "info": "#74B9FF",                 # Blue for info
    "info_bg": "#15203A",               # Info background
    
    # Input Colors
    "input_focus": "#6C5CE7",           # Input focus glow
    "input_placeholder": "#6B7285",    # Input placeholder text
}

# Modern Dark Theme QSS Stylesheet
DARK_THEME_QSS = f"""
/* ============================================
   GLOBAL STYLES
   ============================================ */
QWidget {{
    color: {COLORS['text_primary']};
    font-family: 'Inter', 'Segoe UI', 'SF Pro Display', sans-serif;
    font-size: 14px;
    background-color: transparent;
}}

QMainWindow {{
    background-color: {COLORS['bg_window']};
}}

/* ============================================
   SCROLLBARS
   ============================================ */
QScrollBar:vertical {{
    background: {COLORS['bg_window_secondary']};
    width: 8px;
    border-radius: 4px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['border_light']};
    min-height: 20px;
    border-radius: 4px;
    margin: 2px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['text_muted']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS['bg_window_secondary']};
    height: 8px;
    border-radius: 4px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['border_light']};
    min-width: 20px;
    border-radius: 4px;
    margin: 2px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS['text_muted']};
}}

QScrollArea {{
    border: none;
    background-color: transparent;
}}

/* ============================================
   BUTTONS
   ============================================ */
QPushButton {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 14px;
    min-height: 16px;
}}

QPushButton:hover {{
    background-color: {COLORS['accent_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['accent_pressed']};
}}

QPushButton:disabled {{
    background-color: {COLORS['border']};
    color: {COLORS['text_disabled']};
}}

QPushButton.flat {{
    background-color: transparent;
    border: 1px solid {COLORS['border']};
    color: {COLORS['text_secondary']};
}}

QPushButton.flat:hover {{
    background-color: {COLORS['bg_card']};
    border-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QPushButton.danger {{
    background-color: {COLORS['error']};
}}

QPushButton.danger:hover {{
    background-color: #DC2626;
}}

QPushButton.success {{
    background-color: {COLORS['success']};
}}

QPushButton.success:hover {{
    background-color: #059669;
}}

/* ============================================
   INPUT FIELDS
   ============================================ */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 14px;
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent']};
    selection-color: {COLORS['text_primary']};
}}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 2px solid {COLORS['input_focus']};
    background-color: {COLORS['bg_window_secondary']};
}}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{
    border-color: {COLORS['border_light']};
}}

/* ============================================
   COMBO BOXES
   ============================================ */
QComboBox {{
    background-color: {COLORS['bg_input']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 12px;
    font-size: 14px;
    color: {COLORS['text_primary']};
    min-height: 20px;
}}

QComboBox:hover {{
    border-color: {COLORS['border_light']};
}}

QComboBox:focus {{
    border: 2px solid {COLORS['input_focus']};
}}

QComboBox::drop-down {{
    border: none;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    selection-background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

/* ============================================
   TABLES
   ============================================ */
QTableWidget {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['accent']};
    selection-color: {COLORS['text_primary']};
}}

QTableWidget::item {{
    padding: 12px;
    border-bottom: 1px solid {COLORS['border']};
}}

QTableWidget::item:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QTableWidget::item:hover {{
    background-color: {COLORS['bg_card_hover']};
}}

QHeaderView::section {{
    background-color: {COLORS['bg_window_secondary']};
    color: {COLORS['text_secondary']};
    padding: 12px;
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    border-right: 1px solid {COLORS['border']};
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* ============================================
   TABS
   ============================================ */
QTabWidget::pane {{
    border: none;
    background-color: {COLORS['bg_window']};
}}

QTabBar::tab {{
    background-color: {COLORS['bg_card']};
    color: {COLORS['text_muted']};
    padding: 12px 24px;
    border: 1px solid {COLORS['border']};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 4px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS['bg_card_hover']};
}}

/* ============================================
   PROGRESS BAR
   ============================================ */
QProgressBar {{
    background-color: {COLORS['bg_window_secondary']};
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
        stop:0 {COLORS['accent']}, stop:1 {COLORS['accent_secondary']});
    border-radius: 4px;
}}

/* ============================================
   SLIDER
   ============================================ */
QSlider::groove:horizontal {{
    height: 6px;
    background: {COLORS['bg_window_secondary']};
    border-radius: 3px;
}}

QSlider::handle:horizontal {{
    background: {COLORS['accent']};
    width: 18px;
    height: 18px;
    margin: -6px 0;
    border-radius: 9px;
}}

QSlider::handle:horizontal:hover {{
    background: {COLORS['accent_hover']};
}}

/* ============================================
   MENU
   ============================================ */
QMenu {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['accent']};
    color: {COLORS['text_primary']};
}}

QMenu::separator {{
    height: 1px;
    background: {COLORS['border']};
    margin: 4px 8px;
}}

/* ============================================
   STATUS BAR
   ============================================ */
QStatusBar {{
    background-color: {COLORS['bg_window_secondary']};
    border-top: 1px solid {COLORS['border']};
    color: {COLORS['text_muted']};
}}

/* ============================================
   TOOL BUTTON
   ============================================ */
QToolButton {{
    background-color: transparent;
    border: none;
    border-radius: 6px;
    padding: 6px;
}}

QToolButton:hover {{
    background-color: {COLORS['bg_card']};
}}

QToolButton:pressed {{
    background-color: {COLORS['bg_card_hover']};
}}

/* ============================================
   FRAME
   ============================================ */
QFrame {{
    background-color: transparent;
    border: none;
}}

QFrame[frameShape="4"], QFrame[frameShape="5"] {{
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
}}

/* ============================================
   GROUP BOX
   ============================================ */
QGroupBox {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    margin-top: 12px;
    padding: 16px;
    font-weight: 600;
    color: {COLORS['text_primary']};
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 16px;
    padding: 0 8px;
}}
"""

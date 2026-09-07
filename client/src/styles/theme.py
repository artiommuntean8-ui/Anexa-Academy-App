"""
Master modern SaaS Dark/Obsidian QSS stylesheet for ArkiTech Student Dashboard.
Inspired by Linear, Raycast, Discord, and modern developer tools.
"""

DARK_THEME_QSS = """
/* ==========================================================================
   GLOBAL BASE & TYPOGRAPHY
   ========================================================================== */
QWidget {
    background-color: #080b11;
    color: #f1f5f9;
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, 'Roboto', sans-serif;
    font-size: 13px;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

QMainWindow, QDialog {
    background-color: #080b11;
}

/* ==========================================================================
   SCROLL AREAS & SCROLLBARS (Ultra-Modern 6px)
   ========================================================================== */
QScrollArea {
    background-color: transparent;
    border: none;
}

QScrollBar:vertical {
    background-color: transparent;
    width: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background-color: #1e293b;
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background-color: #334155;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
    height: 0px;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 6px;
    margin: 0px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal {
    background-color: #1e293b;
    min-width: 24px;
    border-radius: 3px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #334155;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
    width: 0px;
}

/* ==========================================================================
   BUTTONS
   ========================================================================== */
QPushButton {
    background-color: #161f36;
    color: #e2e8f0;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #1e2a4a;
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.15);
}

QPushButton:pressed {
    background-color: #131b2e;
}

QPushButton:disabled {
    background-color: #0d121f;
    color: #475569;
    border-color: rgba(255, 255, 255, 0.03);
}

/* Primary Button Variant */
QPushButton#PrimaryButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.2);
    font-weight: 700;
}

QPushButton#PrimaryButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4338ca, stop:1 #6d28d9);
    border-color: rgba(255, 255, 255, 0.35);
}

/* ==========================================================================
   INPUTS & TEXT FIELDS
   ========================================================================== */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #0e1424;
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 9px;
    padding: 10px 14px;
    font-size: 13px;
}

QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {
    border-color: rgba(255, 255, 255, 0.18);
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #6366f1;
    background-color: #11182c;
}

/* ==========================================================================
   TABLES & DATA GRIDS (Modern Card Rows)
   ========================================================================== */
QTableWidget {
    background-color: #0e1424;
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 14px;
    gridline-color: rgba(255, 255, 255, 0.04);
    color: #f1f5f9;
}

QTableWidget::item {
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

QTableWidget::item:selected {
    background-color: rgba(99, 102, 241, 0.15);
    color: #ffffff;
}

QHeaderView::section {
    background-color: #0a0e1a;
    color: #64748b;
    padding: 12px 14px;
    font-size: 11px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

/* ==========================================================================
   PROGRESS BARS
   ========================================================================== */
QProgressBar {
    background-color: #161f36;
    border: none;
    border-radius: 5px;
    height: 10px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:0.5 #06b6d4, stop:1 #10b981);
    border-radius: 5px;
}

/* ==========================================================================
   TOOLTIPS & MENUS
   ========================================================================== */
QToolTip {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 12px;
}
"""

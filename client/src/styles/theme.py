"""
Enterprise SaaS Theme and Design System for ArkiTech Student Dashboard.
Crafted with modern Slate/Dark palette, refined typography, and consistent spacing.
"""

DARK_THEME_QSS = """
/* ==========================================================================
   GLOBAL RESET & BASE TYPOGRAPHY
   ========================================================================== */
* {
    outline: none;
}

QMainWindow, QWidget#MainContainer {
    background-color: #090d16;
    color: #f8fafc;
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
}

/* ==========================================================================
   SIDEBAR NAVIGATION
   ========================================================================== */
QWidget#Sidebar {
    background-color: #0d1322;
    border-right: 1px solid rgba(255, 255, 255, 0.07);
}

QLabel#LogoTitle {
    color: #ffffff;
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.8px;
}

QLabel#LogoSubtitle {
    color: #818cf8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

QPushButton.NavBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 10px;
    padding: 12px 16px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
}

QPushButton.NavBtn:hover {
    background-color: rgba(255, 255, 255, 0.05);
    color: #ffffff;
}

QPushButton.NavBtn:checked {
    background-color: #1e1b4b;
    color: #a5b4fc;
    font-weight: 700;
    border-left: 4px solid #6366f1;
}

/* ==========================================================================
   HEADER BAR
   ========================================================================== */
QWidget#Header {
    background-color: #0d1322;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    padding: 12px 28px;
}

QLabel#HeaderTitle {
    color: #ffffff;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
}

QLabel#HeaderSubtitle {
    color: #64748b;
    font-size: 12px;
    font-weight: 500;
}

/* ==========================================================================
   SURFACES & CARDS
   ========================================================================== */
QFrame.Card, QWidget.Card {
    background-color: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
}

QFrame.Card:hover {
    border-color: rgba(99, 102, 241, 0.4);
}

QFrame.ElevatedCard {
    background-color: #141e33;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
}

/* ==========================================================================
   BUTTONS (SaaS Modern)
   ========================================================================== */
QPushButton.PrimaryBtn {
    background-color: #4f46e5;
    color: #ffffff;
    border: 1px solid #6366f1;
    border-radius: 9px;
    padding: 10px 18px;
    font-weight: 700;
    font-size: 13px;
}

QPushButton.PrimaryBtn:hover {
    background-color: #4338ca;
    border-color: #818cf8;
}

QPushButton.PrimaryBtn:pressed {
    background-color: #3730a3;
}

QPushButton.SecondaryBtn {
    background-color: #1e293b;
    color: #f1f5f9;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 9px;
    padding: 9px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton.SecondaryBtn:hover {
    background-color: #334155;
    color: #ffffff;
    border-color: rgba(255, 255, 255, 0.2);
}

QPushButton.DangerBtn {
    background-color: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 9px;
    padding: 8px 14px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton.DangerBtn:hover {
    background-color: #ef4444;
    color: #ffffff;
    border-color: #ef4444;
}

QPushButton.SuccessBtn {
    background-color: #059669;
    color: #ffffff;
    border: 1px solid #10b981;
    border-radius: 9px;
    padding: 9px 16px;
    font-weight: 700;
    font-size: 13px;
}

QPushButton.SuccessBtn:hover {
    background-color: #047857;
}

/* ==========================================================================
   INPUTS & FORM CONTROLS
   ========================================================================== */
QLineEdit, QTextEdit, QComboBox {
    background-color: #131c2e;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 9px;
    padding: 10px 14px;
    color: #ffffff;
    font-size: 13px;
    selection-background-color: #6366f1;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1.5px solid #6366f1;
    background-color: #162035;
}

QLineEdit:disabled, QTextEdit:disabled {
    background-color: #0d1322;
    color: #64748b;
    border-color: rgba(255, 255, 255, 0.05);
}

/* ==========================================================================
   TABLES & LISTS
   ========================================================================== */
QTableWidget {
    background-color: #111827;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    gridline-color: rgba(255, 255, 255, 0.05);
    color: #f1f5f9;
    selection-background-color: #1e1b4b;
    selection-color: #a5b4fc;
}

QHeaderView::section {
    background-color: #0d1322;
    color: #94a3b8;
    padding: 12px 10px;
    border: none;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    font-weight: 700;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QTableWidget::item {
    padding: 12px 10px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

QTableWidget::item:hover {
    background-color: rgba(255, 255, 255, 0.03);
}

/* ==========================================================================
   PROGRESS BAR
   ========================================================================== */
QProgressBar {
    background-color: #1e293b;
    border: none;
    border-radius: 6px;
    height: 10px;
    text-align: right;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #06b6d4);
    border-radius: 6px;
}

/* ==========================================================================
   CUSTOM SCROLLBAR
   ========================================================================== */
QScrollBar:vertical {
    border: none;
    background: #090d16;
    width: 6px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 24px;
    border-radius: 3px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    border: none;
    background: #090d16;
    height: 6px;
    margin: 0px;
}

QScrollBar::handle:horizontal {
    background: #334155;
    min-width: 24px;
    border-radius: 3px;
}

/* ==========================================================================
   TOOLTIPS
   ========================================================================== */
QToolTip {
    background-color: #1e293b;
    color: #f8fafc;
    border: 1px solid #475569;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 11px;
}
"""

"""
Theme and styling definitions for ArkiTech Student Dashboard Desktop.
"""

DARK_THEME_QSS = """
/* Global Window Styles */
QMainWindow, QWidget#MainContainer {
    background-color: #0b0f19;
    color: #f8fafc;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
}

/* Sidebar Styles */
QWidget#Sidebar {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}

QLabel#LogoTitle {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QLabel#LogoSubtitle {
    color: #38bdf8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}

QPushButton.NavBtn {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton.NavBtn:hover {
    background-color: #1e293b;
    color: #ffffff;
}

QPushButton.NavBtn:checked, QPushButton.NavBtnActive {
    background-color: #1e3a8a;
    color: #60a5fa;
    font-weight: 600;
    border-left: 3px solid #3b82f6;
}

/* Header Styles */
QWidget#Header {
    background-color: #0f172a;
    border-bottom: 1px solid #1e293b;
    padding: 8px 20px;
}

QLabel#HeaderTitle {
    color: #f8fafc;
    font-size: 18px;
    font-weight: 700;
}

QLabel#HeaderSubtitle {
    color: #64748b;
    font-size: 12px;
}

/* Card Containers */
QFrame.Card {
    background-color: #131d33;
    border: 1px solid #1e293b;
    border-radius: 12px;
}

QFrame.Card:hover {
    border-color: #334155;
}

/* Stat Cards */
QLabel.StatValue {
    font-size: 26px;
    font-weight: 800;
    color: #f8fafc;
}

QLabel.StatLabel {
    font-size: 12px;
    font-weight: 600;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QLabel.SectionHeader {
    font-size: 16px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 8px;
}

/* Inputs & Form Controls */
QLineEdit {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px 14px;
    color: #ffffff;
    font-size: 13px;
    selection-background-color: #3b82f6;
}

QLineEdit:focus {
    border: 1px solid #3b82f6;
    background-color: #1e293b;
}

QLineEdit:disabled {
    background-color: #0f172a;
    color: #64748b;
}

/* Buttons */
QPushButton.PrimaryBtn {
    background-color: #2563eb;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton.PrimaryBtn:hover {
    background-color: #1d4ed8;
}

QPushButton.PrimaryBtn:pressed {
    background-color: #1e40af;
}

QPushButton.SecondaryBtn {
    background-color: #1e293b;
    color: #e2e8f0;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 500;
    font-size: 13px;
}

QPushButton.SecondaryBtn:hover {
    background-color: #334155;
    color: #ffffff;
}

QPushButton.DangerBtn {
    background-color: #dc2626;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton.DangerBtn:hover {
    background-color: #b91c1c;
}

/* Tables */
QTableWidget {
    background-color: #131d33;
    border: 1px solid #1e293b;
    border-radius: 8px;
    gridline-color: #1e293b;
    color: #e2e8f0;
    selection-background-color: #1e3a8a;
    selection-color: #ffffff;
}

QHeaderView::section {
    background-color: #0f172a;
    color: #94a3b8;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #1e293b;
    font-weight: 600;
    font-size: 12px;
}

QTableWidget::item {
    padding: 10px;
    border-bottom: 1px solid #1e293b;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #0f172a;
    width: 8px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #334155;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #475569;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Badges & Tags */
QLabel.Badge {
    padding: 3px 8px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
}

QLabel.BadgeSuccess {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34d399;
}

QLabel.BadgeInfo {
    background-color: rgba(14, 165, 233, 0.15);
    color: #38bdf8;
}

QLabel.BadgeWarning {
    background-color: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
}
"""

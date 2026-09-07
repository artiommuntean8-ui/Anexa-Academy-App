from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt


class AchievementCard(QFrame):
    """Visual card displaying an achievement with unlocked/locked states."""

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        unlocked = data.get("unlocked", False)

        if unlocked:
            self.setStyleSheet("""
                QFrame {
                    background-color: #111827;
                    border: 1px solid rgba(245, 158, 11, 0.4);
                    border-radius: 14px;
                    padding: 14px 16px;
                }
                QFrame:hover {
                    border: 1px solid #f59e0b;
                    background-color: #141f33;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: rgba(17, 24, 39, 0.5);
                    border: 1px dashed rgba(255, 255, 255, 0.08);
                    border-radius: 14px;
                    padding: 14px 16px;
                }
            """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        # Icon box
        icon_box = QFrame()
        icon_box.setFixedSize(48, 48)
        if unlocked:
            icon_box.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(245, 158, 11, 0.2), stop:1 rgba(217, 119, 6, 0.2));
                    border: 1px solid rgba(245, 158, 11, 0.4);
                    border-radius: 12px;
                }
            """)
            icon_lbl = QLabel(data.get("icon", "🏆"))
        else:
            icon_box.setStyleSheet("""
                QFrame {
                    background-color: #1e293b;
                    border: 1px solid rgba(255, 255, 255, 0.05);
                    border-radius: 12px;
                }
            """)
            icon_lbl = QLabel("🔒")

        ib_layout = QVBoxLayout(icon_box)
        ib_layout.setContentsMargins(0, 0, 0, 0)
        ib_layout.setAlignment(Qt.AlignCenter)
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 22px;")
        ib_layout.addWidget(icon_lbl)
        layout.addWidget(icon_box)

        # Text info
        text_layout = QVBoxLayout()
        text_layout.setSpacing(3)

        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        title_lbl = QLabel(data.get("title", "Insignă"))
        if unlocked:
            title_lbl.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: 800;")
        else:
            title_lbl.setStyleSheet("color: #64748b; font-size: 14px; font-weight: 700;")
        title_row.addWidget(title_lbl)

        xp_pill = QLabel(f"+{data.get('xp_reward', 50)} XP")
        if unlocked:
            xp_pill.setStyleSheet("""
                background-color: rgba(245, 158, 11, 0.15);
                color: #fbbf24;
                font-size: 10px;
                font-weight: 800;
                padding: 2px 7px;
                border-radius: 5px;
            """)
        else:
            xp_pill.setStyleSheet("""
                background-color: rgba(255, 255, 255, 0.05);
                color: #475569;
                font-size: 10px;
                font-weight: 700;
                padding: 2px 7px;
                border-radius: 5px;
            """)
        title_row.addWidget(xp_pill)
        title_row.addStretch()
        text_layout.addLayout(title_row)

        desc_lbl = QLabel(data.get("description", ""))
        desc_lbl.setWordWrap(True)
        if unlocked:
            desc_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        else:
            desc_lbl.setStyleSheet("color: #475569; font-size: 12px;")
        text_layout.addWidget(desc_lbl)

        layout.addLayout(text_layout)

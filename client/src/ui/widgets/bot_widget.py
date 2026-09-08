from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QLineEdit, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QSize
from client.src.services.api_client import api

class AnexaBotWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.addStretch()
        self.scroll.setWidget(self.chat_container)
        layout.addWidget(self.scroll)
        
        self.hint_btn = QPushButton("💡 Cere Indiciu")
        self.hint_btn.setStyleSheet("""
            QPushButton { background-color: #38BDF8; color: #0F172A; font-weight: bold; padding: 10px; border-radius: 8px; }
            QPushButton:hover { background-color: #7DD3FC; }
        """)
        self.hint_btn.clicked.connect(self.request_hint)
        layout.addWidget(self.hint_btn)

    def add_message(self, text, is_ai=True):
        bubble = QFrame()
        color = "#1E293B" if is_ai else "#2563EB"
        bubble.setStyleSheet(f"background-color: {color}; border-radius: 12px; padding: 10px;")
        layout = QVBoxLayout(bubble)
        layout.addWidget(QLabel(text))
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble)

    def request_hint(self):
        # Placeholder pentru apelul API
        self.add_message("Mă gândesc...", is_ai=True)
        # Aici se va apela api.post("/api/ai/hint", ...)

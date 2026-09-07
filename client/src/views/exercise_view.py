from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)
from PySide6.QtCore import Qt
from client.src.components.code_editor import CodeEditor
from client.src.services.api_client import api
from client.src.components.toast import ToastNotification


class ExerciseView(QWidget):
    """Interactive Python exercise view with syntax-highlighted code editor and instant feedback."""

    def __init__(self, exercise_data=None, parent=None):
        super().__init__(parent)
        self.exercise = exercise_data or {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 28)
        layout.setSpacing(16)

        # Header bar with title and back button
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("← Înapoi la Teme")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                font-weight: 600;
                padding: 8px 14px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #334155; color: white; }
        """)
        self.back_btn.clicked.connect(self.go_back)
        top_bar.addWidget(self.back_btn)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Instructions Card
        instr_card = QFrame()
        instr_card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 16px 20px;
            }
        """)
        ic_layout = QVBoxLayout(instr_card)
        ic_layout.setSpacing(6)

        self.title_lbl = QLabel(self.exercise.get("title", "Exercițiu Python"))
        self.title_lbl.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800;")
        ic_layout.addWidget(self.title_lbl)

        self.desc_lbl = QLabel(self.exercise.get("description", "Scrie codul tău în editorul de mai jos:"))
        self.desc_lbl.setStyleSheet("color: #94a3b8; font-size: 13px;")
        self.desc_lbl.setWordWrap(True)
        ic_layout.addWidget(self.desc_lbl)

        layout.addWidget(instr_card)

        # Code Editor
        self.editor = CodeEditor()
        self.editor.setPlainText(self.exercise.get("starter_code", "# Scrie codul tău aici\nprint('Salut, ArkiTech!')\n"))
        layout.addWidget(self.editor, stretch=1)

        # Output / Results Card
        self.output_card = QFrame()
        self.output_card.setStyleSheet("""
            QFrame {
                background-color: #0b1120;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 10px;
                padding: 12px 16px;
            }
        """)
        oc_layout = QVBoxLayout(self.output_card)
        oc_layout.setSpacing(4)
        oc_header = QLabel("REZULTAT CONSOLĂ:")
        oc_header.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px;")
        oc_layout.addWidget(oc_header)

        self.output_lbl = QLabel("Apasă 'Rulează & Validează Soluția' pentru a verifica codul.")
        self.output_lbl.setStyleSheet("color: #cbd5e1; font-family: 'Consolas', monospace; font-size: 12px;")
        self.output_lbl.setWordWrap(True)
        oc_layout.addWidget(self.output_lbl)
        layout.addWidget(self.output_card)

        # Action Button Row
        btn_row = QHBoxLayout()
        self.submit_btn = QPushButton("▶ Rulează & Validează Soluția")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                font-weight: 700;
                font-size: 13px;
                padding: 12px 24px;
                border-radius: 8px;
                border: 1px solid #10b981;
            }
            QPushButton:hover { background-color: #047857; }
        """)
        self.submit_btn.clicked.connect(self.submit_code)
        btn_row.addWidget(self.submit_btn)
        btn_row.addStretch()

        layout.addLayout(btn_row)

    def go_back(self):
        main_win = self.window()
        if hasattr(main_win, "views_stack"):
            main_win.views_stack.setCurrentIndex(2)
            if hasattr(main_win, "header"):
                main_win.header.set_title("Teme & Proiecte", "Monitorizarea temelor de laborator și termenelor", "Teme")

    def submit_code(self):
        code = self.editor.toPlainText()
        self.submit_btn.setEnabled(False)
        self.submit_btn.setText("Se execută...")

        try:
            result = api.post("/exercises/validate", json_data={
                "code": code,
                "exercise_id": self.exercise.get("id")
            })

            msg = result.get("message", "")
            self.output_lbl.setText(msg)

            if result.get("status") == "success":
                self.output_card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(16, 185, 129, 0.1);
                        border: 1px solid rgba(16, 185, 129, 0.3);
                        border-radius: 10px;
                        padding: 12px 16px;
                    }
                """)
                self.output_lbl.setStyleSheet("color: #34d399; font-family: 'Consolas', monospace; font-size: 12px;")
                toast = ToastNotification("✓ Soluția ta a fost validată și notată cu 100p!", self)
                toast.show_toast(self.width() // 2 - 140, self.height() - 80)
            else:
                self.output_card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(239, 68, 68, 0.1);
                        border: 1px solid rgba(239, 68, 68, 0.3);
                        border-radius: 10px;
                        padding: 12px 16px;
                    }
                """)
                self.output_lbl.setStyleSheet("color: #fca5a5; font-family: 'Consolas', monospace; font-size: 12px;")

        except Exception as e:
            self.output_lbl.setText(f"Eroare: {str(e)}")
        finally:
            self.submit_btn.setEnabled(True)
            self.submit_btn.setText("▶ Rulează & Validează Soluția")

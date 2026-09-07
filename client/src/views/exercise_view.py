from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QScrollArea, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.code_editor import CodeEditor
from client.src.components.toast import ToastNotification
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class ExerciseView(QWidget):
    """Interactive Python exercise view with Auto-Grader unit testing and gamification feedback."""

    def __init__(self, exercise_data=None, parent=None):
        super().__init__(parent)
        self.exercise = exercise_data or {}

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #090d16; }")

        container = QWidget()
        container.setStyleSheet("background-color: #090d16;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(16)

        # 1. Top bar with back button & Auto-Grader Badge
        top_bar = QHBoxLayout()
        self.back_btn = QPushButton("← Înapoi la Teme")
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
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

        autograder_tag = QLabel("⚡ Auto-Grader AI Activ")
        autograder_tag.setStyleSheet("""
            background-color: rgba(99, 102, 241, 0.15);
            color: #a5b4fc;
            font-size: 11px;
            font-weight: 800;
            padding: 5px 12px;
            border-radius: 6px;
            border: 1px solid rgba(99, 102, 241, 0.3);
        """)
        top_bar.addWidget(autograder_tag)
        self.layout.addLayout(top_bar)

        # 2. Instructions Card
        instr_card = QFrame()
        instr_card.setStyleSheet("""
            QFrame {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 18px 22px;
            }
        """)
        ic_layout = QVBoxLayout(instr_card)
        ic_layout.setSpacing(6)

        self.title_lbl = QLabel(self.exercise.get("title", "Exercițiu Python"))
        self.title_lbl.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 800;")
        ic_layout.addWidget(self.title_lbl)

        self.desc_lbl = QLabel(self.exercise.get("description", "Scrie codul tău în editorul de mai jos:"))
        self.desc_lbl.setStyleSheet("color: #94a3b8; font-size: 13px; line-height: 1.4;")
        self.desc_lbl.setWordWrap(True)
        ic_layout.addWidget(self.desc_lbl)

        self.layout.addWidget(instr_card)

        # 3. Code Editor
        self.editor = CodeEditor()
        self.editor.setPlainText(self.exercise.get("starter_code", "# Scrie codul tău aici\n"))
        self.editor.setMinimumHeight(220)
        self.layout.addWidget(self.editor)

        # 4. Action Button Row
        btn_row = QHBoxLayout()
        self.submit_btn = QPushButton("▶ Rulează & Validează Soluția")
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                font-weight: 800;
                font-size: 13px;
                padding: 12px 24px;
                border-radius: 9px;
                border: 1px solid #10b981;
            }
            QPushButton:hover { background-color: #047857; }
        """)
        self.submit_btn.clicked.connect(self.submit_code)
        btn_row.addWidget(self.submit_btn)
        btn_row.addStretch()
        self.layout.addLayout(btn_row)

        # 5. Auto-Grader Results Container
        self.results_card = QFrame()
        self.results_card.setStyleSheet("""
            QFrame {
                background-color: #0d1322;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                padding: 18px 20px;
            }
        """)
        self.results_layout = QVBoxLayout(self.results_card)
        self.results_layout.setSpacing(12)

        # Results header
        r_head = QHBoxLayout()
        self.r_title = QLabel("REZULTATE TESTE AUTOMATE")
        self.r_title.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 800; letter-spacing: 1px;")
        r_head.addWidget(self.r_title)
        r_head.addStretch()

        self.score_badge = QLabel("Scor: -")
        self.score_badge.setStyleSheet("""
            background-color: #1e293b;
            color: #ffffff;
            font-size: 11px;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 6px;
        """)
        r_head.addWidget(self.score_badge)
        self.results_layout.addLayout(r_head)

        # Test cases dynamic list
        self.tests_container = QVBoxLayout()
        self.tests_container.setSpacing(8)
        self.results_layout.addLayout(self.tests_container)

        # Pedagogical Hint Banner (Hidden by default)
        self.hint_banner = QFrame()
        self.hint_banner.setStyleSheet("""
            QFrame {
                background-color: rgba(245, 158, 11, 0.12);
                border: 1px solid rgba(245, 158, 11, 0.35);
                border-radius: 10px;
                padding: 12px 16px;
            }
        """)
        hb_layout = QVBoxLayout(self.hint_banner)
        hb_layout.setContentsMargins(0, 0, 0, 0)
        self.hint_lbl = QLabel("")
        self.hint_lbl.setStyleSheet("color: #fcd34d; font-size: 12px; font-weight: 600;")
        self.hint_lbl.setWordWrap(True)
        hb_layout.addWidget(self.hint_lbl)
        self.hint_banner.hide()
        self.results_layout.addWidget(self.hint_banner)

        # Console Output
        oc_header = QLabel("IEȘIRE CONSOLĂ (STDOUT):")
        oc_header.setStyleSheet("color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 0.8px;")
        self.results_layout.addWidget(oc_header)

        self.console_output = QLabel("(Apasă 'Rulează & Validează Soluția' pentru a verifica codul)")
        self.console_output.setStyleSheet("color: #94a3b8; font-family: 'Consolas', monospace; font-size: 12px; background-color: #080d1a; padding: 10px; border-radius: 8px;")
        self.console_output.setWordWrap(True)
        self.results_layout.addWidget(self.console_output)

        self.layout.addWidget(self.results_card)
        self.layout.addStretch()

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def set_exercise_data(self, data: dict):
        self.exercise = data
        self.title_lbl.setText(data.get("title", "Exercițiu Python"))
        self.desc_lbl.setText(data.get("description", "Scrie codul tău mai jos:"))
        self.editor.setPlainText(data.get("starter_code", "# Scrie codul tău aici\n"))
        self._clear_results()

    def _clear_results(self):
        while self.tests_container.count():
            item = self.tests_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.hint_banner.hide()
        self.score_badge.setText("Scor: -")
        self.score_badge.setStyleSheet("background-color: #1e293b; color: #ffffff; padding: 3px 10px; border-radius: 6px; font-weight: 800;")
        self.console_output.setText("(Apasă 'Rulează & Validează Soluția' pentru a verifica codul)")

    def go_back(self):
        main_win = self.window()
        if hasattr(main_win, "views_stack"):
            main_win.views_stack.setCurrentIndex(2)
            if hasattr(main_win, "header"):
                main_win.header.set_title("Teme & Proiecte", "Monitorizarea temelor de laborator și termenelor", "Teme")

    def submit_code(self):
        code = self.editor.toPlainText()
        self.submit_btn.setEnabled(False)
        self.submit_btn.setText("Se evaluează testele...")

        try:
            result = api.post("/exercises/validate", json_data={
                "code": code,
                "exercise_id": self.exercise.get("id")
            })

            self._render_validation_results(result)

        except Exception as e:
            self.console_output.setText(f"Eroare de comunicare cu serverul: {str(e)}")
        finally:
            self.submit_btn.setEnabled(True)
            self.submit_btn.setText("▶ Rulează & Validează Soluția")

    def _render_validation_results(self, result: dict):
        # 1. Clear previous test cards
        while self.tests_container.count():
            item = self.tests_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        score = result.get("score", 0.0)
        is_passed = result.get("passed", False)
        tests = result.get("test_results", [])
        stdout = result.get("stdout", "")
        hint = result.get("hint")
        unlocked = result.get("unlocked_achievements", [])

        # 2. Update Score Badge
        if is_passed:
            self.score_badge.setText(f"✓ Scor: {score:.0f}% (Promovat)")
            self.score_badge.setStyleSheet("background-color: #065f46; color: #34d399; font-weight: 800; padding: 4px 12px; border-radius: 6px;")
        else:
            self.score_badge.setText(f"✗ Scor: {score:.0f}% (Eșuat)")
            self.score_badge.setStyleSheet("background-color: #7f1d1d; color: #fca5a5; font-weight: 800; padding: 4px 12px; border-radius: 6px;")

        # 3. Render individual test case cards
        for t in tests:
            t_card = QFrame()
            p = t.get("passed", False)
            if p:
                t_card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(16, 185, 129, 0.08);
                        border: 1px solid rgba(16, 185, 129, 0.25);
                        border-radius: 8px;
                        padding: 8px 12px;
                    }
                """)
            else:
                t_card.setStyleSheet("""
                    QFrame {
                        background-color: rgba(239, 68, 68, 0.08);
                        border: 1px solid rgba(239, 68, 68, 0.25);
                        border-radius: 8px;
                        padding: 8px 12px;
                    }
                """)

            t_layout = QVBoxLayout(t_card)
            t_layout.setContentsMargins(0, 0, 0, 0)
            t_layout.setSpacing(4)

            t_row = QHBoxLayout()
            icon = QLabel("✓" if p else "✗")
            icon.setStyleSheet(f"color: {'#10b981' if p else '#ef4444'}; font-weight: 900; font-size: 14px;")
            t_row.addWidget(icon)

            name = QLabel(t.get("name", "Test"))
            name.setStyleSheet("color: #ffffff; font-weight: 700; font-size: 13px;")
            t_row.addWidget(name)
            t_row.addStretch()

            status_text = QLabel("TRECUT" if p else "EȘUAT")
            status_text.setStyleSheet(f"color: {'#34d399' if p else '#fca5a5'}; font-weight: 800; font-size: 11px;")
            t_row.addWidget(status_text)
            t_layout.addLayout(t_row)

            # Details
            if not p:
                details = QLabel(f"Așteptat: {t.get('expected')}  |  Obținut: {t.get('actual')}")
                details.setStyleSheet("color: #cbd5e1; font-size: 11px; font-family: 'Consolas', monospace;")
                t_layout.addWidget(details)

            self.tests_container.addWidget(t_card)

        # 4. Hint banner
        if hint:
            self.hint_lbl.setText(hint)
            self.hint_banner.show()
        else:
            self.hint_banner.hide()

        # 5. Console stdout
        self.console_output.setText(stdout if stdout.strip() else "(Fără mesaje afișate în consolă)")

        # 6. Toast & Celebration for unlocked achievements!
        if unlocked:
            for ach in unlocked:
                msg = f"🎉 Insignă Deblocată: {ach.get('title')} (+{ach.get('xp_reward')} XP)!"
                toast = ToastNotification(msg, self)
                toast.show_toast(self.width() // 2 - 160, self.height() - 90)
        elif is_passed:
            toast = ToastNotification("✓ Soluția a trecut toate testele!", self)
            toast.show_toast(self.width() // 2 - 120, self.height() - 80)

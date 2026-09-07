import csv
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from client.src.components.badge import StatusBadge
from client.src.components.stat_card import StatCard
from client.src.components.empty_state import EmptyState
from client.src.services.api_client import api
from client.src.services.auth_service import auth


class GradesView(QWidget):
    """Academic grades, performance overview, instructor feedback ledger, and CSV export."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GradesView")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #090d16; }")

        container = QWidget()
        container.setStyleSheet("background-color: #090d16;")
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(28, 24, 28, 28)
        self.layout.setSpacing(20)

        # 1. Performance Overview Top Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_gpa = StatCard("Medie Ponderată", "0.0", "⭐", "#10b981", "rgba(16, 185, 129, 0.12)", "Toate evaluările")
        self.card_total_evals = StatCard("Evaluări Finalizate", "0", "📋", "#6366f1", "rgba(99, 102, 241, 0.12)", "Teme notate")
        self.card_status = StatCard("Status Academic", "Excelent", "🏆", "#06b6d4", "rgba(6, 182, 212, 0.12)", "Semestrul curent")

        stats_layout.addWidget(self.card_gpa)
        stats_layout.addWidget(self.card_total_evals)
        stats_layout.addWidget(self.card_status)
        self.layout.addLayout(stats_layout)

        # 2. Table Header with Export Action
        h_box = QHBoxLayout()
        t_label = QLabel("Registrul Notelor & Feedback-ul Instructorilor")
        t_label.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: 700; letter-spacing: -0.2px;")
        h_box.addWidget(t_label)
        h_box.addStretch()

        export_btn = QPushButton("📥 Exportă CSV")
        export_btn.setCursor(QCursor(Qt.PointingHandCursor))
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #1e293b;
                color: #cbd5e1;
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                padding: 7px 14px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #334155;
                color: #ffffff;
            }
        """)
        export_btn.clicked.connect(self.export_grades)
        h_box.addWidget(export_btn)

        self.layout.addLayout(h_box)

        # 3. Grades Ledger Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Temă", "Notă Acordată", "Feedback & Observații", "Data Înregistrării"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #111827;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                color: #f1f5f9;
                gridline-color: rgba(255, 255, 255, 0.05);
            }
            QHeaderView::section {
                background-color: #0d1322;
                color: #94a3b8;
                padding: 14px 12px;
                border: none;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                font-weight: 700;
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            QTableWidget::item {
                padding: 14px 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            }
        """)

        self.layout.addWidget(self.table)
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

    def export_grades(self):
        if self.table.rowCount() == 0:
            QMessageBox.information(self, "Export", "Nu există note de exportat.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Exportă Note CSV", "note_arkitech.csv", "CSV Files (*.csv)")
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID Temă", "Notă Acordată", "Feedback & Observații", "Data Înregistrării"])
                    for row in range(self.table.rowCount()):
                        tema_id = self.table.item(row, 0).text().strip() if self.table.item(row, 0) else ""
                        feedback = self.table.item(row, 2).text().strip() if self.table.item(row, 2) else ""
                        data = self.table.item(row, 3).text().strip() if self.table.item(row, 3) else ""
                        # Score from cell widget
                        widget = self.table.cellWidget(row, 1)
                        score_text = widget.findChild(QLabel).text().replace("★", "").replace("puncte", "").strip() if widget else ""
                        writer.writerow([tema_id, score_text, feedback, data])
                QMessageBox.information(self, "Succes", "Fișierul CSV a fost exportat cu succes!")
            except Exception as e:
                QMessageBox.critical(self, "Eroare", f"Nu s-a putut exporta fișierul: {str(e)}")

    def refresh_data(self):
        """Fetch student grades from backend."""
        user = auth.current_user
        if not user:
            return

        student_id = user.get("id")
        try:
            grades = api.get("/grades/", params={"student_id": student_id})
            self._render_data(grades)
        except Exception as e:
            print(f"Error loading grades: {e}")

    def _render_data(self, grades: List[dict]):
        self.table.setRowCount(len(grades))

        total_score = 0.0
        for row, g in enumerate(grades):
            score = g.get("score", 0.0)
            total_score += score

            # 1. Assignment ID
            a_item = QTableWidgetItem(f"  Temă #{g.get('assignment_id')}  ")
            a_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, a_item)

            # 2. Score Badge
            score_widget = QWidget()
            s_layout = QHBoxLayout(score_widget)
            s_layout.setContentsMargins(6, 6, 6, 6)
            s_layout.setAlignment(Qt.AlignCenter)
            badge = StatusBadge("graded", f"★ {score:.1f} puncte")
            s_layout.addWidget(badge)
            self.table.setCellWidget(row, 1, score_widget)

            # 3. Feedback
            fb = g.get("feedback") or "Evaluare completată cu succes."
            f_item = QTableWidgetItem(f"\"{fb}\"")
            f_item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            self.table.setItem(row, 2, f_item)

            # 4. Date
            d = g.get("graded_at", "")
            d_str = d[:10] if d else "-"
            d_item = QTableWidgetItem(f" 📅 {d_str} ")
            d_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, d_item)

            self.table.setRowHeight(row, 50)

        # Update Top KPI Cards
        eval_count = len(grades)
        self.card_total_evals.set_value(str(eval_count))

        if eval_count > 0:
            avg = total_score / eval_count
            self.card_gpa.set_value(f"{avg:.1f}")
            if avg >= 90:
                self.card_status.set_value("Excelent 🏆")
            elif avg >= 70:
                self.card_status.set_value("Bun ✓")
            else:
                self.card_status.set_value("Satisfăcător ⚠️")
        else:
            self.card_gpa.set_value("-")
            self.card_status.set_value("Fără note")

from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QGridLayout
from PySide6.QtCore import Qt

class TestCaseCard(QFrame):
    def __init__(self, test_id, passed, is_hidden, expected, got, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {'#064E3B' if passed else '#7F1D1D'};
                border: 2px solid {'#4ADE80' if passed else '#F87171'};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        layout = QVBoxLayout(self)
        status = "PASSED ✓" if passed else "FAILED ✗"
        layout.addWidget(QLabel(f"Test {test_id}: {status}"))
        
        if not is_hidden:
            layout.addWidget(QLabel(f"Așteptat: {expected} | Primit: {got}"))
        else:
            layout.addWidget(QLabel("Test Ascuns"))

class TestCasesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("🧪 Rezultate Teste"))
        
    def update_results(self, results):
        # Ștergem widget-urile vechi
        for i in reversed(range(self.layout.count())): 
            if i > 0: # Nu ștergem titlul
                self.layout.itemAt(i).widget().setParent(None)
                
        for res in results:
            card = TestCaseCard(
                res["test_id"], 
                res["status"] == "PASSED", 
                res["is_hidden"],
                res["expected"],
                res["got"]
            )
            self.layout.addWidget(card)

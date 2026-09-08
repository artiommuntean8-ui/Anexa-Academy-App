from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLabel

class VariableInspectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Variabilă", "Tip", "Valoare"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(QLabel("🔍 Inspector Variabile"))
        layout.addWidget(self.table)
        
    def update_data(self, trace_data):
        self.table.setRowCount(0)
        # trace_data vine sub formă de listă de pași, luăm ultima stare
        if not trace_data:
            return
        
        last_state = trace_data[-1].get("vars", {})
        self.table.setRowCount(len(last_state))
        for i, (var, val) in enumerate(last_state.items()):
            self.table.setItem(i, 0, QTableWidgetItem(var))
            self.table.setItem(i, 1, QTableWidgetItem("N/A"))
            self.table.setItem(i, 2, QTableWidgetItem(val))

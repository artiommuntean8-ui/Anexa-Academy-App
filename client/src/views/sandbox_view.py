from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel
from PySide6.QtCore import Qt
from client.src.components.code_editor import CodeEditor
from client.src.ui.widgets.bot_widget import AnexaBotWidget
from client.src.ui.widgets.variable_inspector import VariableInspectorWidget
from client.src.ui.widgets.test_cases_widget import TestCasesWidget
from client.src.styles.theme import COLORS

class SandboxView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Splitter principal: Stânga (Cod+Teste) vs Dreapta (AI+Inspectare)
        splitter = QSplitter(Qt.Horizontal)
        
        # Stânga: Cod și Teste
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        self.editor = CodeEditor()
        self.test_widget = TestCasesWidget()
        left_layout.addWidget(QLabel("Cod Python"))
        left_layout.addWidget(self.editor)
        left_layout.addWidget(self.test_widget)
        
        # Dreapta: Inspector + Bot
        right_splitter = QSplitter(Qt.Vertical)
        self.bot = AnexaBotWidget()
        self.inspector = VariableInspectorWidget()
        right_splitter.addWidget(self.bot)
        right_splitter.addWidget(self.inspector)
        
        splitter.addWidget(left_container)
        splitter.addWidget(right_splitter)
        
        layout.addWidget(splitter)
        
        # Stilizare pentru Splitter
        splitter.setStyleSheet(f"QSplitter::handle {{ background-color: {COLORS['border']}; }}")

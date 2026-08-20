from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from client.src.components.code_editor import CodeEditor
import sys

class TestEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Editor")
        self.resize(600, 400)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        
        self.editor = CodeEditor()
        self.editor.setPlainText("def hello():\n    print('Hello World') # Comment")
        
        layout.addWidget(self.editor)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestEditorWindow()
    window.show()
    sys.exit(app.exec())

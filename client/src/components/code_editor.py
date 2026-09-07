from PySide6.QtCore import Qt, QRegularExpression, Signal, QTimer
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtWidgets import QPlainTextEdit

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Keyword format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#c678dd"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = ["def", "class", "if", "else", "elif", "while", "for", "in", "return", "import", "from", "print"]
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#98c379"))
        self.highlighting_rules.append((QRegularExpression('".*"|\'.*\''), string_format))

        # Comment format
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#5c6370"))
        self.highlighting_rules.append((QRegularExpression("#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CodeEditor(QPlainTextEdit):
    text_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e2127;
                color: #abb2bf;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 14px;
                border: 1px solid #3e4451;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.highlighter = PythonHighlighter(self.document())
        
        # Debounce timer for live updates
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.setInterval(500)
        self.update_timer.timeout.connect(self._emit_text_changed)
        
        self.document().contentsChanged.connect(self.update_timer.start)

    def _emit_text_changed(self):
        self.text_changed.emit(self.toPlainText())

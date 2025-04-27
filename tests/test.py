from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QPlainTextEdit, QSizePolicy
)
from QHubMarkdown.QHubMarkdown import QHubMarkdown
import sys

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Editor")
        self.resize(1000, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        layout = QHBoxLayout(centralWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Markdown here...")
        self.editor.textChanged.connect(self.updatePreview)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.preview = QHubMarkdown(theme="dark")

        layout.addWidget(self.editor, 1)
        layout.addWidget(self.preview, 2)

        # Cargar contenido inicial
        initialText = "# Hello 👋\n"
        self.editor.setPlainText(initialText)
        self.preview.insertMarkdown(initialText)

    def updatePreview(self):
        text = self.editor.toPlainText()
        self.preview.insertMarkdown(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec_())
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPlainTextEdit, QSizePolicy, QPushButton, QTextEdit, QLabel
)
from QHubMarkdown import QHubMarkdown
import sys

class MarkdownEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Markdown Editor with WebChannel")
        self.resize(1200, 700)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        # Main horizontal layout
        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Left panel for editor and controls
        leftPanel = QWidget()
        leftLayout = QVBoxLayout(leftPanel)
        leftLayout.setContentsMargins(10, 10, 10, 10)
        leftLayout.setSpacing(10)

        # Editor
        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText("Markdown here...")
        self.editor.textChanged.connect(self.updatePreview)
        self.editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Control buttons
        buttonLayout = QHBoxLayout()
        
        self.getTextButton = QPushButton("Get Markdown Text (Sync)")
        self.getTextButton.clicked.connect(self.getMarkdownTextSync)
        
        self.getTextAsyncButton = QPushButton("Get Markdown Text (Async)")
        self.getTextAsyncButton.clicked.connect(self.getMarkdownTextAsync)
        
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearContent)
        
        buttonLayout.addWidget(self.getTextButton)
        buttonLayout.addWidget(self.getTextAsyncButton)
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addStretch()

        # Text display area for showing retrieved markdown
        self.textDisplay = QTextEdit()
        self.textDisplay.setMaximumHeight(100)
        self.textDisplay.setPlaceholderText("Retrieved markdown text will appear here...")
        self.textDisplay.setReadOnly(True)

        # Status label
        self.statusLabel = QLabel("Ready")
        self.statusLabel.setStyleSheet("color: #666; font-style: italic;")

        leftLayout.addWidget(self.editor, 1)
        leftLayout.addLayout(buttonLayout)
        leftLayout.addWidget(self.textDisplay)
        leftLayout.addWidget(self.statusLabel)

        # Right panel for preview
        self.preview = QHubMarkdown(theme="dark")

        mainLayout.addWidget(leftPanel, 1)
        mainLayout.addWidget(self.preview, 2)

        # Cargar contenido inicial
        initialText = "# Hello 👋\n\nThis is a **markdown editor** with WebChannel support.\n\n## Features:\n- *Real-time preview*\n- `Code highlighting`\n- **Bidirectional communication**\n- **No delay text retrieval**\n\n```python\nprint('Hello from WebChannel!')\n```"
        self.editor.setPlainText(initialText)

    def updatePreview(self):
        text = self.editor.toPlainText()
        self.preview.writeMarkdown(text)

    def getMarkdownTextSync(self):
        """Get the current markdown text synchronously (no delay)."""
        markdownText = self.preview.getMarkdownText()
        self.textDisplay.setPlainText(markdownText)
        self.statusLabel.setText(f"Sync: Retrieved {len(markdownText)} characters")
        print(f"Sync - Retrieved markdown text: {repr(markdownText)}")

    def getMarkdownTextAsync(self):
        """Get the current markdown text asynchronously."""
        def callback(text):
            self.textDisplay.setPlainText(text)
            self.statusLabel.setText(f"Async: Retrieved {len(text)} characters")
            print(f"Async - Retrieved markdown text: {repr(text)}")
        
        self.preview.getMarkdownTextAsync(callback)
        self.statusLabel.setText("Async: Requesting text...")

    def clearContent(self):
        """Clear both editor and preview."""
        self.editor.clear()
        self.preview.clear()
        self.textDisplay.clear()
        self.statusLabel.setText("Content cleared")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MarkdownEditor()
    window.show()
    sys.exit(app.exec_())
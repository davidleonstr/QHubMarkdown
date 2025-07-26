import sys
from qtpy.QtWidgets import QApplication, QMainWindow
from QHubMarkdown import QHubMarkdown

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.markdown = QHubMarkdown(theme='dark')
        
        try:
            initialText = open('examples/markdown/markdown_example.md', encoding='utf-8').read()
        except:
            initialText = "# Hello 👋\nThis is a simple markdown renderer in Qt."
        
        self.markdown.insertMarkdown(initialText)
        self.setCentralWidget(self.markdown)
        self.setWindowTitle('Markdown Display')
        self.resize(800, 600)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

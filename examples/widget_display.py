from PyQt5.QtWidgets import QApplication, QMainWindow
from QHubMarkdown import QHubMarkdown

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Create an instance of QHubMarkdown with a dark theme (default theme)
        self.markdown = QHubMarkdown(theme="dark")
        
        # Initial markdown content to display
        try:
            initialText = open('examples/markdown/markdown_example.md', encoding='utf-8').read()
        except:
            initialText = "# Hello 👋\nThis is a simple markdown renderer in PyQt5."
        
        # Insert the markdown content into the widget
        self.markdown.insertMarkdown(initialText)
        
        # Set the widget as the central widget of the main window
        self.setCentralWidget(self.markdown)
        
        self.setWindowTitle("Markdown Display")
        self.resize(800, 600)
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    app.exec_()
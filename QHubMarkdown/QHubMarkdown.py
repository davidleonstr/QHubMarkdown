"""
This module contains the 'QHubMarkdown' component.
"""

from qtpy.QtWidgets import QWidget, QVBoxLayout
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtCore import QTimer, QObject, Signal, Slot
from qtpy.QtWebChannel import QWebChannel

# Importing style properties and dependencies
from .properties import *

class MarkdownBridge(QObject):
    """
    Bridge class for communication between Python and JavaScript via WebChannel.
    """
    
    # Signal emitted when markdown text is requested from JavaScript
    markdownTextRequested = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._markdown_text = ""
    
    @Slot(str)
    def setMarkdownText(self, text):
        """
        Slot to receive markdown text from JavaScript.
        
        Args:
            text (str): The markdown text from the web page.
        """
        self._markdown_text = text
    
    @Slot()
    def requestMarkdownText(self):
        """
        Slot to request markdown text from JavaScript.
        """
        self.markdownTextRequested.emit()
    
    def getMarkdownText(self):
        """
        Get the current markdown text.
        
        Returns:
            str: The current markdown text.
        """
        return self._markdown_text

class QHubMarkdown(QWidget):
    """
    A custom QWidget for rendering and displaying Markdown content with GitHub-like styling.
    
    Provides an easy way to integrate styled Markdown, including code highlighting, 
    directly into PyQt/PySide applications using the power of PyQtWebEngine.
    """

    def __init__(self, parent = None, theme: str = 'dark'):
        """
        Initializes a QHubMarkdown object.

        Args:
            parent (Any, optional): Father of the widget. Default is None.
            theme (str, optional): Default GitHub theme ('dark', 'light'). Default is 'dark'.
        """
        super().__init__(parent)

        self.view = QWebEngineView()
        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.view)

        # Complete HTML with embedded JS and CSS code
        self.html = QHubMarkdownHTML(theme=theme)

        # Setup WebChannel for communication
        self.channel = QWebChannel()
        self.bridge = MarkdownBridge()
        self.channel.registerObject('markdownBridge', self.bridge)
        self.view.page().setWebChannel(self.channel)
        
        # Connect signal to request markdown text
        self.bridge.markdownTextRequested.connect(self._requestMarkdownTextFromJS)

        self.view.setHtml(self.html)

        # Indicates the moment when the browser is completely ready
        self.isReady = False

        # If there is markdown to insert
        self.pendingMarkdown = []

        # If the redirection status is pending
        self.pendingRedirectStatus = None

        # If there is a pending text box cleanup
        self.pendingClean = None

        # If there is a pending theme change
        self.pendingTheme = None
        
        self.checkReadyTimer = QTimer()
        self.checkReadyTimer.timeout.connect(self._checkRendererReady)
        self.checkReadyTimer.start(16)

    def _checkRendererReady(self) -> None:
        self.view.page().runJavaScript(
            'window.markdownRendererReady',
            self._handleRendererReady
        )

    def _handleRendererReady(self, isReady: bool) -> None:
        """
        Due to the asynchronous nature of the embedded browser, some functions may leave things pending.
        """
        if isReady and not self.isReady:
            self.isReady = True
            self.checkReadyTimer.stop()
            if self.pendingTheme:
                self.setTheme(self.pendingTheme)
            if self.pendingClean:
                self.clear()
            if self.pendingRedirectStatus:
                self.setNativeRedirection(self.pendingRedirectStatus)
                self.pendingRedirectStatus = None
            if len(self.pendingMarkdown) > 0:
                for item in self.pendingMarkdown:
                    self.insertMarkdown(item)

                self.pendingMarkdown.clear()

    def _requestMarkdownTextFromJS(self):
        """
        Request markdown text from JavaScript.
        """
        if not self.isReady:
            return
            
        js = 'window.getMarkdownText();'
        self.view.page().runJavaScript(js)

    def insertMarkdown(self, text: str) -> None:
        """
        Insert markdown text.

        Args:
            text (str): The text to insert.
        """
        if not self.isReady:
            self.pendingMarkdown.append(text)
            return
            
        js = f'window.insertMarkdown({repr(text)});'
        self.view.page().runJavaScript(js)
    
    def writeMarkdown(self, text: str) -> None:
        """
        Write the markdown text by deleting all existing content.

        Args:
            text (str): The text to insert.
        """
        if not self.isReady:
            self.pendingMarkdown.append(text)
            self.pendingClean = True
            return
        
        js = f'window.writeMarkdown({repr(text)});'
        self.view.page().runJavaScript(js)

    def clear(self) -> None:
        """
        Delete all markdown content
        """
        if not self.isReady:
            self.pendingClean = True
            return
        
        self.view.page().runJavaScript('window.clearMarkdown();')
    
    def getMarkdownText(self) -> str:
        """
        Get the current markdown text from the web page.
        
        Returns:
            str: The current markdown text.
        """
        if not self.isReady:
            return ''
        
        # Return the text stored in the bridge (no delay)
        return self.bridge.getMarkdownText()
    
    def getMarkdownTextAsync(self, callback=None) -> None:
        """
        Get the current markdown text asynchronously from the web page.
        
        Args:
            callback (callable, optional): Function to call with the result.
        """
        if not self.isReady:
            if callback:
                callback('')
            return
        
        # Request the text from JavaScript
        self.bridge.requestMarkdownText()
        
        # If callback provided, set up a timer to check for the result
        if callback:
            def check_result():
                result = self.bridge.getMarkdownText()
                callback(result)
            
            # Use a short timer to allow JavaScript to respond
            QTimer.singleShot(50, check_result)
        
    def setNativeRedirection(self, state: bool) -> None:
        """
        Sets a state for using redirection with the embedded browser.

        Args:
            state (bool): Status of the redirection possibility.
        """
        if not self.isReady:
            self.pendingRedirectStatus = state
            return
        
        js = f'window.setNativeRedirection({repr(state).lower()});'
        # '.lower' because booleans in JS are lowercase

        self.view.page().runJavaScript(js)
    
    def setTheme(self, theme: str) -> None:
        """
        Sets a new theme by injecting CSS into the document head.

        Args:
            theme (str): Default GitHub theme ('dark', 'light').
        """
        if not self.isReady:
            self.pendingTheme = theme
            return

        css = readFileContent(
            os.path.join(
                currentDir, 
                resources['folder'], 
                THEMES['custom'][theme]
            )
        )

        if not css:
            return Exception(f"Theme '{theme}' does not exist")

        js = r"""
        (() => {{
            const style = document.createElement("style");
            style.textContent = [css];
            document.head.appendChild(style);
        }})()
        """
        js = js.replace('[css]', repr(css))

        self.view.page().runJavaScript(js)
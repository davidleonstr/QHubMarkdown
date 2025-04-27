"""
This module contains the 'QHubMarkdown' component.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QTimer

# Importing style properties and dependencies
from .properties import *

class QHubMarkdown(QWidget):
    """
    A custom QWidget for rendering and displaying Markdown content with GitHub-like styling.
    
    Provides an easy way to integrate styled Markdown, including code highlighting, 
    directly into PyQt5 applications using the power of PyQtWebEngine.
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
        html = QHubMarkdownHTML(theme=theme)

        self.view.setHtml(html)

        # Indicates the moment when the browser is completely ready
        self.isReady = False

        # If there is markdown to insert
        self.pendingMarkdown = None

        #If the redirection status is pending
        self.pendingRedirectStatus = None

        #If there is a pending text box cleanup
        self.pendingClean = None
        
        self.checkReadyTimer = QTimer()
        self.checkReadyTimer.timeout.connect(self._checkRendererReady)
        self.checkReadyTimer.start(16)

    def _checkRendererReady(self) -> None:
        self.view.page().runJavaScript(
            "window.markdownRendererReady",
            self._handleRendererReady
        )

    def _handleRendererReady(self, isReady: bool) -> None:
        """
        Due to the asynchronous nature of the embedded browser, some functions may leave things pending.
        """
        if isReady and not self.isReady:
            self.isReady = True
            self.checkReadyTimer.stop()
            if self.pendingClean:
                self.clear()
            if self.pendingRedirectStatus:
                self.setNativeRedirection(self.pendingRedirectStatus)
                self.pendingRedirectStatus = None
            if self.pendingMarkdown:
                self.insertMarkdown(self.pendingMarkdown)
                self.pendingMarkdown = None

    def insertMarkdown(self, text: str) -> None:
        """
        Insert markdown text.

        Args:
            text (str): The text to insert.
        """
        if not self.isReady:
            self.pendingMarkdown = text
            return
            
        js = f"window.insertMarkdown({repr(text)});"
        self.view.page().runJavaScript(js)
    
    def writeMarkdown(self, text: str) -> None:
        """
        Write the markdown text by deleting all existing content.

        Args:
            text (str): The text to insert.
        """
        if not self.isReady:
            self.pendingMarkdown = text
            self.pendingClean = True
            return
        
        self.clear()
        self.insertMarkdown(text)

    def clear(self) -> None:
        """
        Delete all markdown content
        """
        if self.isReady:
            self.view.page().runJavaScript("window.clearMarkdown();")
        
    def setNativeRedirection(self, state: bool) -> None:
        """
        Sets a state for using redirection with the embedded browser.

        Args:
            state (bool): Status of the redirection possibility.
        """
        if not self.isReady:
            self.pendingRedirectStatus = state
            return
        
        js = f"window.setNativeRedirection({repr(state).lower()});" 
        # '.lower' because booleans in JS are lowercase

        self.view.page().runJavaScript(js)
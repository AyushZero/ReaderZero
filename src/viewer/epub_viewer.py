from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import tempfile
import os
from pathlib import Path

class CustomWebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundColor(Qt.white)
    
    def javaScriptConsoleMessage(self, level, message, line, source):
        """Suppress JavaScript console messages."""
        pass

class EpubViewer(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.current_page = 0
        self.book = None
        self.spine_items = []
        self.temp_dir = None
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Create web view
        self.web_view = QWebEngineView()
        self.web_view.setPage(CustomWebPage(self.web_view))
        self.web_view.setContextMenuPolicy(Qt.NoContextMenu)
        self.layout.addWidget(self.web_view)
        
        # Load document
        self.load_document(file_path)
    
    def load_document(self, file_path: str):
        """Load and parse ePub document."""
        self.book = epub.read_epub(file_path)
        self.spine_items = list(self.book.spine)
        
        # Create temporary directory for extracted files
        self.temp_dir = tempfile.mkdtemp()
        
        # Extract and process first page
        self.show_page(0)
    
    def show_page(self, page_num: int):
        """Display the specified page."""
        if not self.book or page_num < 0 or page_num >= len(self.spine_items):
            return
        
        self.current_page = page_num
        item = self.spine_items[page_num]
        
        # Get content
        content = item.get_content()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Add basic styling
        style = soup.new_tag('style')
        style.string = """
            body {
                margin: 0;
                padding: 20px;
                font-family: system-ui, -apple-system, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
            }
            img { max-width: 100%; height: auto; }
        """
        soup.head.append(style)
        
        # Convert to file URL
        temp_file = os.path.join(self.temp_dir, f'page_{page_num}.html')
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        # Load in web view
        self.web_view.setUrl(QUrl.fromLocalFile(temp_file))
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < len(self.spine_items) - 1:
            self.show_page(self.current_page + 1)
    
    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.show_page(self.current_page - 1)
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir)
    
    def closeEvent(self, event):
        """Handle window close."""
        self.cleanup()
        super().closeEvent(event)
    
    def sizeHint(self):
        """Return preferred size."""
        return QSize(800, 600)  # Default size 
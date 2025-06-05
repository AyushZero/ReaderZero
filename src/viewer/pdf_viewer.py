from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage, QPixmap, QPainter
import fitz  # PyMuPDF
from pathlib import Path

class PDFViewer(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.current_page = 0
        self.document = None
        self.page_image = None
        
        # Load document
        self.load_document(file_path)
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Initial render
        self.render_current_page()
    
    def load_document(self, file_path: str):
        """Load PDF document using PyMuPDF."""
        self.document = fitz.open(file_path)
        if not self.document:
            raise RuntimeError(f"Failed to load PDF: {file_path}")
    
    def render_current_page(self):
        """Render the current page to fit the window."""
        if not self.document:
            return
        
        # Get current page
        page = self.document[self.current_page]
        if not page:
            return
        
        # Calculate scale to fit window
        page_rect = page.rect
        window_size = self.size()
        scale_x = window_size.width() / page_rect.width
        scale_y = window_size.height() / page_rect.height
        scale = min(scale_x, scale_y)
        
        # Render page
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.page_image = img
        self.update()
    
    def paintEvent(self, event):
        """Paint the current page."""
        if not self.page_image:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Center the image
        x = (self.width() - self.page_image.width()) // 2
        y = (self.height() - self.page_image.height()) // 2
        painter.drawImage(x, y, self.page_image)
    
    def resizeEvent(self, event):
        """Handle window resize."""
        super().resizeEvent(event)
        self.render_current_page()
    
    def next_page(self):
        """Go to next page."""
        if self.current_page < len(self.document) - 1:
            self.current_page += 1
            self.render_current_page()
    
    def previous_page(self):
        """Go to previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.render_current_page()
    
    def sizeHint(self):
        """Return preferred size."""
        if self.document and self.current_page < len(self.document):
            page = self.document[self.current_page]
            if page:
                return QSize(page.rect.width, page.rect.height)
        return QSize(800, 600)  # Default size 
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
        self.zoom_factor = 1.0
        self.base_dpi = 150  # Base DPI for rendering
        
        # Load document
        self.load_document(file_path)
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Set initial size based on first page
        if self.document and len(self.document) > 0:
            page = self.document[0]
            if page:
                # Convert PDF points to pixels (72 points per inch)
                width = int(page.rect.width * self.base_dpi / 72)
                height = int(page.rect.height * self.base_dpi / 72)
                self.resize(width, height)
        
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
        
        # Calculate scale to fit window while maintaining aspect ratio
        page_rect = page.rect
        window_size = self.size()
        
        # Convert PDF points to pixels (72 points per inch)
        page_width = page_rect.width * self.base_dpi / 72
        page_height = page_rect.height * self.base_dpi / 72
        
        # Calculate scale to fit window
        scale_x = window_size.width() / page_width
        scale_y = window_size.height() / page_height
        scale = min(scale_x, scale_y) * self.zoom_factor
        
        # Render page with calculated scale
        matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.page_image = img
        self.update()
    
    def paintEvent(self, event):
        """Paint the current page."""
        if not self.page_image:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Calculate position to center the image
        x = (self.width() - self.page_image.width()) // 2
        y = (self.height() - self.page_image.height()) // 2
        
        # Draw the image
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
    
    def zoom_in(self):
        """Increase zoom level."""
        self.zoom_factor *= 1.2
        self.render_current_page()
    
    def zoom_out(self):
        """Decrease zoom level."""
        self.zoom_factor /= 1.2
        self.render_current_page()
    
    def reset_zoom(self):
        """Reset zoom to fit window."""
        self.zoom_factor = 1.0
        self.render_current_page() 
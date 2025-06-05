from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage, QPixmap, QPainter
import fitz  # PyMuPDF
from pathlib import Path

class PDFViewer(QWidget):
    def __init__(self, file_path: str):
        super().__init__()
        self.current_page = 0
        self.document = None
        self.a4_height = 1080
        self.a4_width = int(self.a4_height / 1.414)
        
        # Load document
        self.load_document(file_path)
        
        # Set up layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        # Set up scroll area and label
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)

        # Set initial window size to A4 at 1080px height
        self.resize(self.a4_width, self.a4_height)

        # Initial render
        self.render_current_page()

    def load_document(self, file_path: str):
        """Load PDF document using PyMuPDF."""
        self.document = fitz.open(file_path)
        if not self.document:
            raise RuntimeError(f"Failed to load PDF: {file_path}")
    
    def render_current_page(self):
        if not self.document:
            return
        page = self.document[self.current_page]
        if not page:
            return
        # Render so that height is always 1080px, width is A4 aspect
        scale = self.a4_height / page.rect.height
        matrix = fitz.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(img))
        self.image_label.resize(img.width(), img.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # No need to re-render on resize

    def paintEvent(self, event):
        pass  # No custom painting needed

    def sizeHint(self):
        return QSize(self.a4_width, self.a4_height)

    def minimumSizeHint(self):
        return QSize(400, 300)
    
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
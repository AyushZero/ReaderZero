#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QKeyEvent

from viewer.pdf_viewer import PDFViewer
from viewer.epub_viewer import EpubViewer

class ReaderWindow(QMainWindow):
    def __init__(self, file_path: str):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.showFullScreen()
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize viewer based on file type
        self.viewer = self._create_viewer(file_path)
        if self.viewer:
            self.setCentralWidget(self.viewer)
    
    def _create_viewer(self, file_path: str):
        ext = Path(file_path).suffix.lower()
        if ext == '.pdf':
            return PDFViewer(file_path)
        elif ext == '.epub':
            return EpubViewer(file_path)
        return None
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.viewer.next_page()
        elif event.key() == Qt.Key_Backspace:
            self.viewer.previous_page()
        super().keyPressEvent(event)

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_document>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = ReaderWindow(file_path)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QKeyEvent

from viewer.pdf_viewer import PDFViewer
from viewer.epub_viewer import EpubViewer

class ReaderWindow(QMainWindow):
    def __init__(self, file_path: str):
        super().__init__()
        # Remove forced full-screen and frameless window
        self.setWindowTitle("Reader")
        
        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Initialize viewer based on file type
        self.viewer = self._create_viewer(file_path)
        if self.viewer:
            self.setCentralWidget(self.viewer)
        else:
            QMessageBox.critical(self, "Unsupported File", f"Cannot open file: {file_path}")
            self.close()
    
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
        elif event.key() == Qt.Key_Space or event.key() == Qt.Key_Right:
            if self.viewer:
                self.viewer.next_page()
        elif event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Left:
            if self.viewer:
                self.viewer.previous_page()
        elif event.key() == Qt.Key_Plus or event.key() == Qt.Key_Equal:
            if isinstance(self.viewer, PDFViewer):
                self.viewer.zoom_in()
        elif event.key() == Qt.Key_Minus:
            if isinstance(self.viewer, PDFViewer):
                self.viewer.zoom_out()
        elif event.key() == Qt.Key_0:
            if isinstance(self.viewer, PDFViewer):
                self.viewer.reset_zoom()
        super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    file_path = None

    # If a file is provided as an argument, use it
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        if not os.path.exists(file_path):
            QMessageBox.critical(None, "File Not Found", f"File not found: {file_path}")
            sys.exit(1)
    else:
        # Show file open dialog
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Open PDF or ePub File")
        file_dialog.setNameFilters(["PDF Files (*.pdf)", "ePub Files (*.epub)", "All Files (*.*)"])
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
        if not file_path:
            # User cancelled
            sys.exit(0)

    window = ReaderWindow(file_path)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 
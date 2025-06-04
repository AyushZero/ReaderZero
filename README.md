# Reader

A minimalist, full-screen document reader for PDF and ePub files. Designed for distraction-free reading with minimal resource usage.

## Features

- Full-screen reading experience with no UI elements
- Native PDF rendering via Poppler
- Efficient ePub rendering
- Minimal resource usage
- Cross-platform support (Windows/Linux)
- Fast startup time
- Escape key to exit

## Requirements

- Python 3.8+
- Qt 6.5+
- Poppler (for PDF rendering)

## Installation

1. Install system dependencies:
   - Windows: Install Poppler via [poppler-windows](https://github.com/oschwartz10612/poppler-windows)
   - Linux: `sudo apt-get install poppler-qt5`

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python src/main.py path/to/document.pdf
# or
python src/main.py path/to/document.epub
```

## Controls

- `Esc` - Exit application
- `Space` - Next page
- `Backspace` - Previous page

## Development

The project is structured for easy extension:

- `src/` - Main application code
  - `main.py` - Application entry point
  - `viewer/` - Document viewer implementations
  - `utils/` - Utility functions
  - `config/` - Configuration management 
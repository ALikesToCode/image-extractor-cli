# Image Extractor CLI

A command-line utility for extracting images from PDF, DOCX, and PPTX files.

## Features

- Extract images from multiple document formats:
  - PDF files using `pypdf`
  - DOCX files using `python-docx`
  - PPTX files using `python-pptx`
- Automatically generate unique filenames for extracted images
- Handle various image formats (JPG, PNG, GIF, BMP, TIFF, etc.)
- Convert JP2 images to PNG format
- Parallel processing for faster extraction
- Modular architecture for easy extension to additional formats
- Pure Python implementation (no subprocess dependencies)

## Installation

### From PyPI (recommended)

```bash
pip install image-extractor
```

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/image-extractor-cli.git
cd image-extractor-cli

# Install in development mode
pip install -e .
```

## Usage

### Command Line

```bash
# Basic usage
image-extractor document.pdf

# Specify output directory
image-extractor presentation.pptx -o ./extracted_images

# Enable verbose logging
image-extractor document.docx -v
```

### As a Python Library

```python
from image_extractor import ImageExtractor

# Extract images from a document
extracted_files = ImageExtractor.extract("document.pdf", "output_directory")

# Print the paths of extracted images
for image_path in extracted_files:
    print(f"Extracted: {image_path}")
```

## Command-line Arguments

- `file_path`: Path to the document file (required)
- `-o, --output-dir`: Directory to save extracted images (default: 'extracted_images' in same directory as input file)
- `-v, --verbose`: Enable verbose logging

## Requirements

- Python 3.7+
- Pillow (for image processing)
- pypdf (for PDF extraction)
- python-docx (for DOCX extraction)
- python-pptx (for PPTX extraction)

## Extending

The project is designed to be easily extensible with new document formats:

1. Create a new handler class in `image_extractor/handlers/`
2. Extend `ExtractorHandler` base class
3. Implement the `extract` method
4. Register the handler with `@ExtractorRegistry.register(['.ext'])`

Example:

```python
from ..handlers.base import ExtractorHandler, ExtractorRegistry
from ..utils.image_processing import save_image

@ExtractorRegistry.register(['.odt'])
class OdtExtractor(ExtractorHandler):
    """Handler for extracting images from ODT files."""
    
    def extract(self, source_path: Path, output_path: Path) -> List[Path]:
        # Implementation here
        pass
```

## License

MIT

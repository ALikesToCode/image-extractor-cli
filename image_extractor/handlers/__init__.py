"""
Image extractor handlers package.

This package contains handlers for different document formats.
"""

# Import all handlers so they register themselves
from .pdf_handler import PdfExtractor
from .docx_handler import DocxExtractor
from .pptx_handler import PptxExtractor 
"""
Image Extractor - A utility for extracting images from document files.

This package provides a simple API for extracting images from various document formats.
"""

from pathlib import Path
from typing import List, Optional, Union
import logging

from .handlers.base import ExtractorRegistry

__version__ = "0.1.0"

logger = logging.getLogger(__name__)


class ImageExtractor:
    """Main API class for extracting images from documents."""
    
    @staticmethod
    def extract(source_path: Union[str, Path], 
                output_path: Optional[Union[str, Path]] = None) -> List[Path]:
        """Extract images from the specified document.
        
        Args:
            source_path: Path to the document file
            output_path: Directory to save extracted images
                        (default: 'extracted_images' subdirectory)
        
        Returns:
            List of paths to the extracted images
            
        Raises:
            ValueError: If the file type is not supported
            FileNotFoundError: If the input file doesn't exist
        """
        # Convert to Path objects
        source = Path(source_path)
        
        # Check if file exists
        if not source.exists():
            raise FileNotFoundError(f"Input file not found: {source}")
        
        # Set default output path if not provided
        if output_path is None:
            output = source.parent / "extracted_images"
        else:
            output = Path(output_path)
        
        # Get appropriate handler for file type
        file_extension = source.suffix.lower()
        handler_class = ExtractorRegistry.get_handler(file_extension)
        handler = handler_class()
        
        # Extract images
        return handler.extract(source, output) 
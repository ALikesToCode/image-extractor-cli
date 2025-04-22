"""
Handler for extracting images from PDF files using pypdf.
"""

import logging
from pathlib import Path
from typing import List, Set

from pypdf import PdfReader

from ..handlers.base import ExtractorHandler, ExtractorRegistry
from ..utils.image_processing import save_image, handle_jp2_image, standardize_extension

logger = logging.getLogger(__name__)


@ExtractorRegistry.register(['.pdf'])
class PdfExtractor(ExtractorHandler):
    """Handler for extracting images from PDF files."""
    
    def extract(self, source_path: Path, output_path: Path) -> List[Path]:
        """Extract images from a PDF file.
        
        Args:
            source_path: Path to the PDF file
            output_path: Directory to save extracted images
            
        Returns:
            List of paths to extracted image files
            
        Raises:
            Exception: If extraction fails
        """
        try:
            reader = PdfReader(source_path)
            seen_images: Set[int] = set()
            extracted_files = []

            logger.info(f"Extracting images from PDF: {source_path}")
            logger.info(f"Found {len(reader.pages)} pages")

            # Process each page in the PDF
            for i, page in enumerate(reader.pages):
                logger.debug(f"Processing page {i+1}/{len(reader.pages)}")
                
                # Extract images from the current page
                for image in page.images:
                    image_data = image.data
                    image_hash = hash(image_data)

                    # Skip duplicate images
                    if image_hash in seen_images:
                        continue

                    seen_images.add(image_hash)

                    # Process the image
                    ext = Path(image.name).suffix.lower()
                    ext = standardize_extension(ext)
                    
                    # Handle JP2 images specially
                    if ext == ".jp2":
                        try:
                            image_data, ext = handle_jp2_image(image_data)
                        except ValueError as e:
                            logger.error(str(e))
                            continue

                    # Save the image
                    file_path = save_image(image_data, output_path, ext)
                    extracted_files.append(file_path)
                    
            logger.info(f"Extracted {len(extracted_files)} unique images from PDF")
            return extracted_files
            
        except Exception as e:
            logger.error(f"Failed to extract images from {source_path}: {e}", exc_info=True)
            raise 
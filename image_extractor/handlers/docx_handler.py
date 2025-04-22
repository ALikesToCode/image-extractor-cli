"""
Handler for extracting images from DOCX files using python-docx.
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import here to catch import errors early
try:
    from docx import Document
except ImportError:
    raise ImportError(
        "python-docx is required for DOCX extraction. "
        "Install it with 'pip install python-docx'."
    )

from ..handlers.base import ExtractorHandler, ExtractorRegistry
from ..utils.image_processing import save_image, standardize_extension

logger = logging.getLogger(__name__)


@ExtractorRegistry.register(['.docx'])
class DocxExtractor(ExtractorHandler):
    """Handler for extracting images from DOCX files."""
    
    # Map of content types to file extensions
    CONTENT_TYPE_MAP: Dict[str, str] = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/gif": ".gif",
        "image/bmp": ".bmp",
        "image/tiff": ".tiff",
        "image/x-tiff": ".tiff",
        "image/jp2": ".jp2",
        "image/webp": ".webp",
    }
    
    def extract(self, source_path: Path, output_path: Path) -> List[Path]:
        """Extract images from a DOCX file using python-docx.
        
        Args:
            source_path: Path to the DOCX file
            output_path: Directory to save extracted images
            
        Returns:
            List of paths to extracted image files
            
        Raises:
            Exception: If extraction fails
        """
        try:
            logger.info(f"Extracting images from DOCX: {source_path}")
            document = Document(source_path)
            extracted_files = []
            
            # Access the relationships in the document to find images
            rels = document.part.rels
            image_parts = []
            
            # Find all image relationships
            for rel in rels.values():
                if "image" in rel.reltype:
                    try:
                        image_parts.append(rel.target_part)
                    except Exception as e:
                        logger.error(f"Failed to access image part: {e}")
            
            logger.info(f"Found {len(image_parts)} potential images in DOCX")
            
            # Process images in parallel
            with ThreadPoolExecutor() as executor:
                futures = []
                
                for image_part in image_parts:
                    try:
                        future = executor.submit(
                            self._process_image_part,
                            image_part,
                            output_path
                        )
                        futures.append(future)
                    except Exception as e:
                        logger.error(f"Failed to process image part: {e}")
                
                # Collect results
                for future in futures:
                    try:
                        result = future.result()
                        if result:
                            extracted_files.append(result)
                    except Exception as e:
                        logger.error(f"Error processing image: {e}")
            
            logger.info(f"Extracted {len(extracted_files)} images from DOCX")
            return extracted_files
            
        except Exception as e:
            logger.error(f"Failed to extract images from {source_path}: {e}", exc_info=True)
            raise
    
    def _get_extension_from_content_type(self, content_type: str) -> str:
        """Convert content type to file extension.
        
        Args:
            content_type: MIME type of the image
            
        Returns:
            File extension including the dot (e.g., '.jpg')
        """
        return self.CONTENT_TYPE_MAP.get(content_type.lower(), ".jpg")
    
    def _process_image_part(self, image_part, output_path: Path) -> Optional[Path]:
        """Process an image part from a DOCX file.
        
        Args:
            image_part: The image part from the document
            output_path: Directory to save the image
            
        Returns:
            Path to the saved image file or None if processing failed
        """
        try:
            # Get image data
            image_data = image_part.blob
            
            # Determine file extension from content type
            content_type = image_part.content_type
            ext = self._get_extension_from_content_type(content_type)
            ext = standardize_extension(ext)
            
            # Save the image
            return save_image(image_data, output_path, ext)
        except Exception as e:
            logger.error(f"Failed to process image part: {e}")
            return None 
"""
Handler for extracting images from PPTX files using python-pptx.
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Import here to catch import errors early
try:
    from pptx import Presentation
except ImportError:
    raise ImportError(
        "python-pptx is required for PPTX extraction. "
        "Install it with 'pip install python-pptx'."
    )

from ..handlers.base import ExtractorHandler, ExtractorRegistry
from ..utils.image_processing import save_image, standardize_extension

logger = logging.getLogger(__name__)


@ExtractorRegistry.register(['.pptx'])
class PptxExtractor(ExtractorHandler):
    """Handler for extracting images from PPTX files."""
    
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
        """Extract images from a PPTX file using python-pptx.
        
        Args:
            source_path: Path to the PPTX file
            output_path: Directory to save extracted images
            
        Returns:
            List of paths to extracted image files
            
        Raises:
            Exception: If extraction fails
        """
        try:
            logger.info(f"Extracting images from PPTX: {source_path}")
            presentation = Presentation(source_path)
            extracted_files = []
            
            # Get all parts related to the presentation
            related_parts = presentation.part.related_parts
            image_parts = []
            
            # Find all image parts
            for part in related_parts.values():
                if part.partname and '/media/' in part.partname:
                    image_parts.append(part)
            
            logger.info(f"Found {len(image_parts)} potential images in PPTX")
            
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
            
            logger.info(f"Extracted {len(extracted_files)} images from PPTX")
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
        """Process an image part from a PPTX file.
        
        Args:
            image_part: The image part from the presentation
            output_path: Directory to save the image
            
        Returns:
            Path to the saved image file or None if processing failed
        """
        try:
            # Get image data
            image_data = image_part.blob
            
            # Try to determine the content type from the part name
            part_name = str(image_part.partname).lower()
            
            # Get extension from part name
            ext = Path(part_name).suffix
            
            # If no extension or unrecognized, try content type
            if not ext or ext not in self.CONTENT_TYPE_MAP.values():
                content_type = getattr(image_part, 'content_type', None)
                if content_type:
                    ext = self._get_extension_from_content_type(content_type)
                else:
                    # Default to jpg if we can't determine
                    ext = ".jpg"
            
            ext = standardize_extension(ext)
            
            # Save the image
            return save_image(image_data, output_path, ext)
        except Exception as e:
            logger.error(f"Failed to process image part: {e}")
            return None 
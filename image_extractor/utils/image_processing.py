"""
Utility functions for image processing and file operations.
"""

import io
import logging
from pathlib import Path
from typing import Set, Tuple
from uuid import uuid4

from PIL import Image

# Constants
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".jp2", ".gif", ".bmp", ".tiff", ".webp"}

logger = logging.getLogger(__name__)


def generate_uuid_filename(extension: str) -> str:
    """Generate a unique filename with the specified extension.
    
    Args:
        extension: File extension (e.g., '.jpg', '.png')
        
    Returns:
        A string containing a UUID with the provided extension
    """
    if not extension.startswith('.'):
        extension = f".{extension}"
    return f"{uuid4()}{extension.lower()}"


def handle_jp2_image(image_data: bytes) -> Tuple[bytes, str]:
    """Convert JP2 image to PNG format.
    
    Args:
        image_data: Raw JP2 image data
        
    Returns:
        Tuple of (converted image data, new extension)
        
    Raises:
        ValueError: If conversion fails
    """
    try:
        with Image.open(io.BytesIO(image_data)) as img:
            if img.mode == "RGBA":
                img = img.convert("RGB")
            
            output = io.BytesIO()
            img.save(output, format="PNG")
            return output.getvalue(), ".png"
    except Exception as e:
        raise ValueError(f"Failed to convert JP2 to PNG: {e}")


def save_image(image_data: bytes, output_path: Path, extension: str) -> Path:
    """Save image data to a file with a unique filename.
    
    Args:
        image_data: Raw image data
        output_path: Directory to save the image
        extension: File extension for the image
        
    Returns:
        Path to the saved image file
    """
    # Ensure the output directory exists
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate a unique filename
    image_filename = generate_uuid_filename(extension)
    file_path = output_path / image_filename
    
    # Write the image data
    with open(file_path, "wb") as fp:
        fp.write(image_data)
    
    logger.debug(f"Saved image to {file_path}")
    return file_path


def standardize_extension(ext: str) -> str:
    """Standardize file extensions.
    
    Args:
        ext: File extension (e.g., '.jpeg', '.jp2')
    
    Returns:
        Standardized extension (e.g., '.jpg', '.png')
    """
    ext = ext.lower()
    if ext == ".jpeg":
        return ".jpg"
    return ext


def is_valid_image_extension(ext: str) -> bool:
    """Check if a file extension is a valid image extension.
    
    Args:
        ext: File extension to check
        
    Returns:
        True if valid, False otherwise
    """
    return ext.lower() in VALID_EXTENSIONS 
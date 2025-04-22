"""
Command-line interface for the image extractor.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional

from . import ImageExtractor

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application.
    
    Args:
        verbose: If True, set log level to DEBUG, otherwise INFO
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract images from PDF, DOCX, and PPTX files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m image_extractor document.pdf
  python -m image_extractor presentation.pptx -o ./images
  python -m image_extractor document.docx -v
        """
    )
    parser.add_argument(
        "file_path", 
        help="Path to the document file"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        help="Directory to save extracted images (default: 'extracted_images' in same directory as input file)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    return parser.parse_args()


def main() -> int:
    """Main entry point for the command line tool.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    args = parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    try:
        # Extract images using the API
        extracted_files = ImageExtractor.extract(args.file_path, args.output_dir)
        
        # Report results
        if extracted_files:
            output_dir = Path(extracted_files[0]).parent
            print(f"Successfully extracted {len(extracted_files)} images to: {output_dir}")
        else:
            print("No images were extracted from the document.")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Please install the required dependencies.", file=sys.stderr)
        return 1
    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"Error: An unexpected error occurred. See log for details.", file=sys.stderr)
        return 1 
"""
Main entry point for the image extractor package.

This allows the package to be run as a module:
python -m image_extractor [arguments]
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main()) 
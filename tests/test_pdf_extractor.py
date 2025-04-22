"""
Tests for the PDF extractor handler.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from image_extractor import ImageExtractor
from image_extractor.handlers.pdf_handler import PdfExtractor


class TestPdfExtractor(unittest.TestCase):
    """Test case for the PDF extractor handler."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for output
        self.temp_dir = tempfile.mkdtemp()
        
        # Path to test PDF file
        self.samples_dir = Path(__file__).parent / "samples"
        self.pdf_file = self.samples_dir / "sample.pdf"
        
        # Skip if sample file doesn't exist
        if not self.pdf_file.exists():
            self.skipTest(f"Sample PDF file '{self.pdf_file}' not found")
    
    def tearDown(self):
        """Clean up after the test."""
        # Remove the temporary directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_pdf_extraction(self):
        """Test PDF image extraction."""
        # Skip if the pdf file doesn't exist
        if not self.pdf_file.exists():
            self.skipTest(f"Sample PDF file '{self.pdf_file}' not found")
            
        handler = PdfExtractor()
        output_path = Path(self.temp_dir)
        
        # Extract images using the handler directly
        extracted_files = handler.extract(self.pdf_file, output_path)
        
        # Verify extraction results
        self.assertIsInstance(extracted_files, list)
        
        # If the sample PDF contains images, verify they were extracted
        if extracted_files:
            for file_path in extracted_files:
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(os.path.getsize(file_path) > 0)
    
    def test_api_extraction(self):
        """Test extraction using the main API."""
        # Skip if the pdf file doesn't exist
        if not self.pdf_file.exists():
            self.skipTest(f"Sample PDF file '{self.pdf_file}' not found")
            
        output_path = Path(self.temp_dir)
        
        # Extract images using the API
        extracted_files = ImageExtractor.extract(self.pdf_file, output_path)
        
        # Verify extraction results
        self.assertIsInstance(extracted_files, list)
        
        # If the sample PDF contains images, verify they were extracted
        if extracted_files:
            for file_path in extracted_files:
                self.assertTrue(os.path.exists(file_path))
                self.assertTrue(os.path.getsize(file_path) > 0)


if __name__ == "__main__":
    unittest.main() 
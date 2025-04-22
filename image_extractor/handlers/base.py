"""
Base classes for document image extractors.

This module defines the ExtractorHandler base class and ExtractorRegistry for
registering handlers for different document types.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Type, ClassVar


class ExtractorHandler(ABC):
    """Base class for document image extractors."""
    
    @abstractmethod
    def extract(self, source_path: Path, output_path: Path) -> List[Path]:
        """Extract images from document to the output path.
        
        Args:
            source_path: Path to the source document
            output_path: Directory to save extracted images
            
        Returns:
            List of paths to extracted image files
        """
        pass


class ExtractorRegistry:
    """Registry for file handlers."""
    
    _handlers: ClassVar[Dict[str, Type[ExtractorHandler]]] = {}
    
    @classmethod
    def register(cls, extensions: List[str]):
        """Decorator to register a handler for specific extensions.
        
        Args:
            extensions: List of file extensions this handler supports (e.g., ['.pdf'])
            
        Returns:
            Decorator function that registers the handler class
        """
        def decorator(handler_class: Type[ExtractorHandler]) -> Type[ExtractorHandler]:
            for ext in extensions:
                if not ext.startswith('.'):
                    ext = f'.{ext}'
                cls._handlers[ext.lower()] = handler_class
            return handler_class
        return decorator
    
    @classmethod
    def get_handler(cls, file_extension: str) -> Type[ExtractorHandler]:
        """Get the appropriate handler for a file extension.
        
        Args:
            file_extension: The file extension (e.g., '.pdf')
            
        Returns:
            The handler class for the extension
            
        Raises:
            ValueError: If no handler is registered for the extension
        """
        if not file_extension.startswith('.'):
            file_extension = f'.{file_extension}'
            
        ext = file_extension.lower()
        if ext not in cls._handlers:
            supported = ", ".join(sorted(cls._handlers.keys()))
            raise ValueError(f"Unsupported file type: {ext}. Supported types: {supported}")
        return cls._handlers[ext] 
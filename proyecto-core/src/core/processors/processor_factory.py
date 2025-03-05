from typing import Dict, Type
from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .word_processor import WordProcessor
from .excel_processor import ExcelProcessor
from .text_processor import TextProcessor
from .code_processor import CodeProcessor
from .uasset_processor import UAssetProcessor
from .pptx_processor import PowerPointProcessor

class ProcessorFactory:
    """Factory para crear el procesador adecuado según el tipo de archivo"""
    
    def __init__(self):
        self.processors: Dict[str, Type[BaseProcessor]] = {
            # Documentos
            "application/pdf": PDFProcessor,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": WordProcessor,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ExcelProcessor,
            "application/vnd.openxmlformats-officedocument.presentationml.presentation": PowerPointProcessor,
            
            # Texto y código
            "text/plain": TextProcessor,
            "text/x-python": CodeProcessor,
            "text/x-c++": CodeProcessor,
            
            # Especializados
            "application/x-uasset": UAssetProcessor,
        }

        # Extensiones de archivo a MIME types
        self.extensions = {
            ".pdf": "application/pdf",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            ".txt": "text/plain",
            ".csv": "text/plain",
            ".py": "text/x-python",
            ".cpp": "text/x-c++",
            ".uasset": "application/x-uasset",
        }

    def get_processor(self, file_path: str) -> BaseProcessor:
        """Obtiene el procesador adecuado según la extensión del archivo"""
        from pathlib import Path
        extension = Path(file_path).suffix.lower()
        
        mime_type = self.extensions.get(extension)
        if not mime_type:
            raise ValueError(f"No hay procesador disponible para la extensión: {extension}")
            
        processor_class = self.processors.get(mime_type)
        if not processor_class:
            raise ValueError(f"No hay procesador disponible para el tipo MIME: {mime_type}")
            
        return processor_class()

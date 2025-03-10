import os
from pathlib import Path
from typing import Optional, Dict

from .base_processor import BaseProcessor
from .pdf_processor import PDFProcessor
from .excel_processor import ExcelProcessor
from .word_processor import WordProcessor
from .text_processor import TextProcessor
from .file_type_detector import FileTypeDetector

class ProcessorFactory:
    """
    Factory para crear instancias de procesadores según el tipo de archivo.
    Utiliza el FileTypeDetector para determinar el tipo de archivo.
    """
    
    def __init__(self):
        self.type_detector = FileTypeDetector()
        self._processors = {}
        self._register_default_processors()
    
    def _register_default_processors(self):
        """Registra los procesadores predeterminados"""
        self.register_processor("application/pdf", PDFProcessor())
        self.register_processor("application/vnd.openxmlformats-officedocument.wordprocessingml.document", WordProcessor())
        self.register_processor("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ExcelProcessor())
        self.register_processor("application/vnd.ms-excel", ExcelProcessor())
        self.register_processor("text/plain", TextProcessor())
    
    def register_processor(self, mime_type: str, processor: BaseProcessor):
        """
        Registra un nuevo procesador para un tipo MIME específico
        
        Args:
            mime_type: Tipo MIME del archivo
            processor: Instancia del procesador
        """
        self._processors[mime_type] = processor
    
    def get_processor(self, file_path: str) -> Optional[BaseProcessor]:
        """
        Devuelve el procesador adecuado para un archivo
        
        Args:
            file_path: Ruta al archivo
        
        Returns:
            BaseProcessor: Instancia del procesador o None si no hay procesador disponible
        """
        if not os.path.exists(file_path):
            return None
        
        # Determinar el tipo MIME del archivo
        mime_type = self.type_detector.detect_file_type(file_path)
        
        # Buscar por tipo MIME exacto
        if mime_type in self._processors:
            return self._processors[mime_type]
        
        # Buscar por categoría general (text/*, application/*, etc.)
        general_type = mime_type.split('/')[0] + '/*'
        if general_type in self._processors:
            return self._processors[general_type]
            
        return None
    
    def get_supported_types(self) -> Dict[str, str]:
        """
        Devuelve un diccionario con los tipos MIME soportados y sus descripciones
        
        Returns:
            Dict[str, str]: Diccionario con tipos MIME como claves y descripciones como valores
        """
        return {
            "application/pdf": "PDF Document",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "Microsoft Word Document",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "Microsoft Excel Spreadsheet",
            "application/vnd.ms-excel": "Microsoft Excel Spreadsheet (Legacy)",
            "text/plain": "Plain Text Document"
        }

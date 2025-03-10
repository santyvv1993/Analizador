from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProcessedContent:
    """Clase que representa el contenido procesado de un archivo"""
    content: str
    metadata: Dict
    summary: str
    keywords: List[str]
    created_date: Optional[datetime] = None
    modified_date: Optional[datetime] = None
    author: Optional[str] = None
    title: Optional[str] = None
    num_pages: int = 1
    language: str = "en"
    entities: List[Dict] = None
    confidence_score: float = 0.5

    def __post_init__(self):
        if self.entities is None:
            self.entities = []

class BaseProcessor(ABC):
    """Clase base para todos los procesadores de archivos"""

    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """
        Valida si el archivo puede ser procesado por este procesador
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            bool: True si el archivo es válido, False en caso contrario
        """
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Devuelve el tipo MIME del archivo
        
        Returns:
            str: Tipo MIME del archivo
        """
        pass

    @abstractmethod
    def process(self, file_path: str) -> ProcessedContent:
        """
        Procesa el archivo y devuelve su contenido procesado
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            ProcessedContent: Contenido procesado del archivo
        """
        pass

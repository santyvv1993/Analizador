from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ProcessedContent:
    """Estructura de datos para el contenido procesado"""
    content: str
    metadata: Dict
    summary: str
    keywords: List[str]
    created_date: Optional[datetime]
    modified_date: Optional[datetime]
    author: Optional[str]
    title: Optional[str]
    num_pages: Optional[int]
    language: Optional[str]
    entities: List[Dict]
    confidence_score: float

class BaseProcessor(ABC):
    """Clase base para todos los procesadores de archivos"""
    
    @abstractmethod
    def process(self, file_path: str) -> ProcessedContent:
        """Procesa el archivo y retorna el contenido estructurado"""
        pass

    @abstractmethod
    def validate(self, file_path: str) -> bool:
        """Valida si el archivo puede ser procesado por este procesador"""
        pass

    @abstractmethod
    def get_mime_type(self) -> str:
        """Retorna el tipo MIME que este procesador puede manejar"""
        pass

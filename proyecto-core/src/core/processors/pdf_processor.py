from pypdf import PdfReader
from pathlib import Path
from typing import List, Dict, Optional
import langdetect
from datetime import datetime

from .base_processor import BaseProcessor, ProcessedContent
from ..ai.ai_analyzer import AIAnalyzer

class PDFProcessor(BaseProcessor):
    """Procesador específico para archivos PDF"""

    def __init__(self):
        self.ai_analyzer = AIAnalyzer()

    def validate(self, file_path: str) -> bool:
        """Valida si el archivo es un PDF válido"""
        if not Path(file_path).exists():
            return False
        
        try:
            with open(file_path, 'rb') as file:
                PdfReader(file)
            return True
        except Exception:
            return False

    def get_mime_type(self) -> str:
        return "application/pdf"

    def process(self, file_path: str) -> ProcessedContent:
        """Procesa un archivo PDF y extrae su contenido y metadatos"""
        if not self.validate(file_path):
            raise ValueError(f"Archivo inválido o no existe: {file_path}")

        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            
            content = ""
            for page in pdf.pages:
                content += page.extract_text() + "\n"

            metadata = dict(pdf.metadata) if pdf.metadata else {}
            ai_analysis = self.ai_analyzer.analyze_content(content, metadata)
            analysis_result = ai_analysis.get("analysis_result", {})

            return ProcessedContent(
                content=content,
                metadata={
                    **metadata,
                    "ai_analysis": ai_analysis
                },
                summary=analysis_result.get("summary", content[:500]),
                keywords=analysis_result.get("keywords", self._extract_keywords(content)),
                created_date=self._parse_date(metadata.get('/CreationDate')),
                modified_date=self._parse_date(metadata.get('/ModDate')),
                author=metadata.get('/Author'),
                title=metadata.get('/Title'),
                num_pages=len(pdf.pages),
                language=langdetect.detect(content),
                entities=analysis_result.get("entities", []),
                confidence_score=ai_analysis.get("confidence_score", 0.5)
            )

    def _extract_keywords(self, content: str) -> List[str]:
        """Extrae palabras clave del contenido (implementación básica)"""
        # TODO: Mejorar con procesamiento NLP
        words = content.lower().split()
        # Eliminar palabras comunes y cortas
        keywords = [word for word in words if len(word) > 4]
        # Retornar las 10 palabras más frecuentes
        from collections import Counter
        return [word for word, _ in Counter(keywords).most_common(10)]

    def _extract_entities(self, content: str) -> List[Dict]:
        """Extrae entidades del contenido (implementación básica)"""
        # TODO: Implementar extracción de entidades con spaCy o similar
        return []

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Convierte fechas de PDF a formato datetime"""
        if not date_str:
            return None
        try:
            # Formato típico PDF: "D:20240221123456+01'00'"
            date_str = date_str.replace("D:", "").split('+')[0]
            return datetime.strptime(date_str, "%Y%m%d%H%M%S")
        except:
            return None

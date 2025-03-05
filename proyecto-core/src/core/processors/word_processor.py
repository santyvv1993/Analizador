from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import docx
import langdetect
from .base_processor import BaseProcessor, ProcessedContent
from ..ai.ai_analyzer import AIAnalyzer

class WordProcessor(BaseProcessor):
    """Procesador específico para archivos Word (DOCX)"""

    def __init__(self):
        self.ai_analyzer = AIAnalyzer()

    def validate(self, file_path: str) -> bool:
        if not Path(file_path).exists():
            return False
        try:
            docx.Document(file_path)
            return True
        except Exception:
            return False

    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    def process(self, file_path: str) -> ProcessedContent:
        if not self.validate(file_path):
            raise ValueError(f"Archivo inválido o no existe: {file_path}")

        doc = docx.Document(file_path)
        
        # Extraer contenido
        content = []
        for paragraph in doc.paragraphs:
            content.append(paragraph.text)

        # Extraer tablas
        for table in doc.tables:
            table_content = []
            for row in table.rows:
                row_content = []
                for cell in row.cells:
                    row_content.append(cell.text)
                table_content.append(" | ".join(row_content))
            content.append("\n".join(table_content))

        full_content = "\n".join(content)

        # Extraer metadatos
        core_properties = doc.core_properties
        metadata = {
            "author": core_properties.author,
            "created": core_properties.created,
            "modified": core_properties.modified,
            "title": core_properties.title,
            "subject": core_properties.subject,
            "keywords": core_properties.keywords,
            "language": core_properties.language,
            "category": core_properties.category,
            "comments": core_properties.comments,
            "document_statistics": {
                "paragraphs": len(doc.paragraphs),
                "tables": len(doc.tables)
            }
        }

        # Realizar análisis con IA
        ai_analysis = self.ai_analyzer.analyze_content(full_content, metadata)
        analysis_result = ai_analysis.get("analysis_result", {})

        return ProcessedContent(
            content=full_content,
            metadata={
                **metadata,
                "ai_analysis": ai_analysis
            },
            summary=analysis_result.get("summary", full_content[:500]),
            keywords=analysis_result.get("keywords", self._extract_keywords(full_content)),
            created_date=core_properties.created,
            modified_date=core_properties.modified,
            author=core_properties.author,
            title=core_properties.title,
            num_pages=self._count_pages(doc),
            language=core_properties.language or langdetect.detect(full_content),
            entities=analysis_result.get("entities", []),
            confidence_score=ai_analysis.get("confidence_score", 0.5)
        )

    def _count_pages(self, doc) -> int:
        # Aproximación basada en secciones
        return len(doc.sections)

    def _extract_keywords(self, content: str) -> List[str]:
        words = content.lower().split()
        keywords = [word for word in words if len(word) > 4]
        from collections import Counter
        return [word for word, _ in Counter(keywords).most_common(10)]

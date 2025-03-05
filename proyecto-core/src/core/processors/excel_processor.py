from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime
import langdetect
from .base_processor import BaseProcessor, ProcessedContent
from ..ai.ai_analyzer import AIAnalyzer

class ExcelProcessor(BaseProcessor):
    """Procesador específico para archivos Excel"""

    def __init__(self):
        self.ai_analyzer = AIAnalyzer()

    def validate(self, file_path: str) -> bool:
        """Valida si el archivo es un Excel válido"""
        if not Path(file_path).exists():
            return False
        
        try:
            pd.ExcelFile(file_path)
            return True
        except Exception:
            return False

    def get_mime_type(self) -> str:
        return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def process(self, file_path: str) -> ProcessedContent:
        """Procesa un archivo Excel y extrae su contenido y metadatos"""
        if not self.validate(file_path):
            raise ValueError(f"Archivo inválido o no existe: {file_path}")

        excel = pd.ExcelFile(file_path)
        
        # Extraer contenido de todas las hojas
        content = []
        metadata = {
            "sheets": [],
            "total_rows": 0,
            "total_columns": 0
        }

        for sheet_name in excel.sheet_names:
            df = pd.read_excel(excel, sheet_name)
            sheet_content = df.to_string(index=False)
            content.append(f"Sheet: {sheet_name}\n{sheet_content}")
            
            metadata["sheets"].append({
                "name": sheet_name,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist()
            })
            metadata["total_rows"] += len(df)
            metadata["total_columns"] = max(metadata["total_columns"], len(df.columns))

        # Unir todo el contenido
        full_content = "\n\n".join(content)

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
            created_date=self._get_file_date(file_path),
            modified_date=self._get_file_date(file_path, "modified"),
            author=None,  # Excel no proporciona autor directamente
            title=Path(file_path).stem,
            num_pages=len(excel.sheet_names),
            language=langdetect.detect(full_content),
            entities=analysis_result.get("entities", []),
            confidence_score=ai_analysis.get("confidence_score", 0.5)
        )

    def _extract_keywords(self, content: str) -> List[str]:
        """Extrae palabras clave del contenido"""
        words = content.lower().split()
        keywords = [word for word in words if len(word) > 4]
        from collections import Counter
        return [word for word, _ in Counter(keywords).most_common(10)]

    def _get_file_date(self, file_path: str, date_type: str = "created") -> Optional[datetime]:
        """Obtiene la fecha de creación o modificación del archivo"""
        path = Path(file_path)
        try:
            if date_type == "modified":
                return datetime.fromtimestamp(path.stat().st_mtime)
            return datetime.fromtimestamp(path.stat().st_ctime)
        except:
            return None

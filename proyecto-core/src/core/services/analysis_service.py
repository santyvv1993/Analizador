from datetime import datetime
import hashlib
import time
from typing import Dict, Optional
from sqlalchemy.orm import Session
from ..repositories.analysis_repository import AnalysisRepository
from ..repositories.file_repository import FileRepository
from ..models.models import AnalysisResult, File
from ..processors.base_processor import ProcessedContent

class AnalysisService:
    def __init__(self, db: Session):
        self.db = db
        self.analysis_repository = AnalysisRepository(db)
        self.file_repository = FileRepository(db)

    def save_analysis(self, file_id: int, processed_content: ProcessedContent) -> AnalysisResult:
        """Guarda el resultado del análisis en la base de datos"""
        # Verificar que el archivo existe
        file = self.file_repository.get_by_id(file_id)
        if not file:
            raise ValueError(f"No se encontró el archivo con ID {file_id}")

        start_time = time.time()
        
        # Calcular hash del contenido
        content_hash = hashlib.sha256(
            processed_content.content.encode()
        ).hexdigest()

        # Preparar datos para la base de datos
        analysis_data = {
            "file_id": file_id,
            "analysis_type": self._determine_analysis_type(file),
            "confidence": processed_content.confidence_score,
            "result_data": processed_content.metadata.get("ai_analysis", {}).get("analysis_result", {}),
            "language": processed_content.language,
            "summary": processed_content.summary,
            "keywords": processed_content.keywords,
            "extracted_metadata": processed_content.metadata,
            "content_hash": content_hash,
            "processing_metadata": {
                "processor_version": "1.0",
                "processing_timestamp": datetime.now().isoformat(),
                "file_size": file.file_size,
                "original_filename": file.filename
            },
            "model_used": processed_content.metadata.get("ai_analysis", {}).get("model", "deepseek-chat"),
            "tokens_used": len(processed_content.content.split()),
            "processing_time": time.time() - start_time
        }

        # Guardar en la base de datos
        analysis_result = self.analysis_repository.create_analysis(analysis_data)

        # Actualizar estado del archivo
        file.is_processed = True
        self.file_repository.update(file)

        return analysis_result

    def get_latest_analysis(self, file_id: int) -> Optional[AnalysisResult]:
        """Obtiene el análisis más reciente de un archivo"""
        return self.analysis_repository.get_latest_by_file_id(file_id)

    def _determine_analysis_type(self, file: File) -> str:
        """Determina el tipo de análisis basado en el tipo de archivo"""
        mime_type_mapping = {
            "application/pdf": "pdf_analysis",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx_analysis",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx_analysis",
            "text/plain": "text_analysis"
        }
        return mime_type_mapping.get(file.mime_type, "generic_analysis")

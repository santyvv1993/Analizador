from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models.models import AnalysisResult
from .base_repository import BaseRepository

class AnalysisRepository(BaseRepository[AnalysisResult]):
    def __init__(self, db: Session):
        super().__init__(AnalysisResult, db)

    def create_analysis(self, analysis_data: dict) -> AnalysisResult:
        """Crea un nuevo registro de análisis"""
        analysis = AnalysisResult(**analysis_data)
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_by_file_id(self, file_id: int) -> List[AnalysisResult]:
        """Obtiene todos los análisis para un archivo específico"""
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.file_id == file_id)\
            .order_by(desc(AnalysisResult.created_at), desc(AnalysisResult.id))\
            .all()

    def get_latest_by_file_id(self, file_id: int) -> Optional[AnalysisResult]:
        """Obtiene el análisis más reciente para un archivo"""
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.file_id == file_id)\
            .order_by(desc(AnalysisResult.created_at), desc(AnalysisResult.id))\
            .first()

    def get_by_analysis_type(self, analysis_type: str) -> List[AnalysisResult]:
        """Obtiene análisis por tipo"""
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.analysis_type == analysis_type)\
            .all()

    def get_recent_analyses(self, limit: int = 10) -> List[AnalysisResult]:
        return self.db.query(AnalysisResult)\
            .order_by(desc(AnalysisResult.created_at), desc(AnalysisResult.id))\
            .limit(limit)\
            .all()

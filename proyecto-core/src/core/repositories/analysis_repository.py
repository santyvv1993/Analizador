from typing import List
from sqlalchemy.orm import Session
from ..models.models import AnalysisResult
from .base_repository import BaseRepository

class AnalysisRepository(BaseRepository[AnalysisResult]):
    def __init__(self, db: Session):
        super().__init__(AnalysisResult, db)

    def get_by_file_id(self, file_id: int) -> List[AnalysisResult]:
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.file_id == file_id)\
            .all()

    def get_by_analysis_type(self, analysis_type: str) -> List[AnalysisResult]:
        return self.db.query(AnalysisResult)\
            .filter(AnalysisResult.analysis_type == analysis_type)\
            .all()

    def get_recent_analyses(self, limit: int = 10) -> List[AnalysisResult]:
        return self.db.query(AnalysisResult)\
            .order_by(AnalysisResult.created_at.desc())\
            .limit(limit)\
            .all()

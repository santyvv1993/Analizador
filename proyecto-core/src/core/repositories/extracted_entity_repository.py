from typing import List
from sqlalchemy.orm import Session
from ..models.models import ExtractedEntity
from .base_repository import BaseRepository

class ExtractedEntityRepository(BaseRepository[ExtractedEntity]):
    def __init__(self, db: Session):
        super().__init__(ExtractedEntity, db)

    def get_by_file_id(self, file_id: int) -> List[ExtractedEntity]:
        return self.db.query(ExtractedEntity)\
            .filter(ExtractedEntity.file_id == file_id)\
            .all()

    def get_by_entity_type(self, entity_type: str) -> List[ExtractedEntity]:
        return self.db.query(ExtractedEntity)\
            .filter(ExtractedEntity.entity_type == entity_type)\
            .all()

    def get_by_confidence_threshold(self, threshold: float) -> List[ExtractedEntity]:
        return self.db.query(ExtractedEntity)\
            .filter(ExtractedEntity.confidence >= threshold)\
            .all()

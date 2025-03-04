from typing import List
from sqlalchemy.orm import Session
from ..models.models import ProcessingHistory
from .base_repository import BaseRepository

class ProcessingHistoryRepository(BaseRepository[ProcessingHistory]):
    def __init__(self, db: Session):
        super().__init__(ProcessingHistory, db)

    def get_by_file_id(self, file_id: int) -> List[ProcessingHistory]:
        return self.db.query(ProcessingHistory)\
            .filter(ProcessingHistory.file_id == file_id)\
            .all()

    def get_by_plugin_id(self, plugin_id: int) -> List[ProcessingHistory]:
        return self.db.query(ProcessingHistory)\
            .filter(ProcessingHistory.plugin_id == plugin_id)\
            .all()

    def get_failures(self) -> List[ProcessingHistory]:
        return self.db.query(ProcessingHistory)\
            .filter(ProcessingHistory.status == 'failure')\
            .all()

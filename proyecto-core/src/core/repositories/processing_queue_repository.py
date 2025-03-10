from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import ProcessingQueue
from .base_repository import BaseRepository

class ProcessingQueueRepository(BaseRepository[ProcessingQueue]):
    def __init__(self, db: Session):
        super().__init__(ProcessingQueue, db)

    def get_pending_tasks(self) -> List[ProcessingQueue]:
        return self.db.query(ProcessingQueue)\
            .filter(ProcessingQueue.status == 'pending')\
            .order_by(ProcessingQueue.priority.desc())\
            .all()

    def get_tasks_by_status(self, status: str) -> List[ProcessingQueue]:
        return self.db.query(ProcessingQueue)\
            .filter(ProcessingQueue.status == status)\
            .all()

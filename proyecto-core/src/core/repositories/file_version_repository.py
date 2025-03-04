from typing import List
from sqlalchemy.orm import Session
from ..models.models import FileVersion
from .base_repository import BaseRepository

class FileVersionRepository(BaseRepository[FileVersion]):
    def __init__(self, db: Session):
        super().__init__(FileVersion, db)

    def get_by_file_id(self, file_id: int) -> List[FileVersion]:
        return self.db.query(FileVersion).filter(FileVersion.file_id == file_id).all()

    def get_latest_version(self, file_id: int) -> FileVersion:
        return self.db.query(FileVersion)\
            .filter(FileVersion.file_id == file_id)\
            .order_by(FileVersion.version_number.desc())\
            .first()

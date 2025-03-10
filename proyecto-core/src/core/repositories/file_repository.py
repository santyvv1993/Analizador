from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import File
from .base_repository import BaseRepository

class FileRepository(BaseRepository[File]):
    def __init__(self, db: Session):
        super().__init__(File, db)

    def get_by_user_id(self, user_id: int) -> List[File]:
        return self.db.query(File).filter(File.user_id == user_id).all()

    def get_by_type(self, file_type: str) -> List[File]:
        return self.db.query(File).filter(File.file_type == file_type).all()

    def get_unprocessed_files(self) -> List[File]:
        return self.db.query(File).filter(File.is_processed == False).all()

    def get_by_id(self, file_id: int) -> Optional[File]:
        return self.db.query(File).filter(File.id == file_id).first()
    
    def update(self, file: File) -> File:
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

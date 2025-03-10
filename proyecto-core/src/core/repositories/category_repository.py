from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import Category
from .base_repository import BaseRepository

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(Category, db)

    def get_root_categories(self) -> List[Category]:
        return self.db.query(Category).filter(Category.parent_id == None).all()

    def get_subcategories(self, parent_id: int) -> List[Category]:
        return self.db.query(Category).filter(Category.parent_id == parent_id).all()

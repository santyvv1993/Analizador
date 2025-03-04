from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session, declarative_base, declared_attr

Base = declarative_base()

class BaseModel:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: int

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model_class: Type[ModelType], db: Session):
        self.model_class = model_class
        self.db = db

    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def get_all(self) -> List[ModelType]:
        return self.db.query(self.model_class).all()

    def create(self, obj_in: ModelType) -> ModelType:
        self.db.add(obj_in)
        self.db.commit()
        self.db.refresh(obj_in)
        return obj_in

    def update(self, obj_data: ModelType) -> ModelType:
        self.db.merge(obj_data)
        self.db.commit()
        return obj_data

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

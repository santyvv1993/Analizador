from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.models import Plugin
from .base_repository import BaseRepository

class PluginRepository(BaseRepository[Plugin]):
    def __init__(self, db: Session):
        super().__init__(Plugin, db)

    def get_enabled_plugins(self) -> List[Plugin]:
        return self.db.query(Plugin).filter(Plugin.enabled == True).all()

    def get_by_name(self, name: str) -> Optional[Plugin]:
        return self.db.query(Plugin).filter(Plugin.name == name).first()

    def get_by_version(self, name: str, version: str) -> Optional[Plugin]:
        return self.db.query(Plugin).filter(
            Plugin.name == name,
            Plugin.version == version
        ).first()

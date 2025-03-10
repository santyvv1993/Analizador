from typing import Optional
from sqlalchemy.orm import Session
from ..models.models import UserSettings
from .base_repository import BaseRepository

class UserSettingsRepository(BaseRepository[UserSettings]):
    def __init__(self, db: Session):
        super().__init__(UserSettings, db)

    def get_by_user_id(self, user_id: int) -> Optional[UserSettings]:
        return self.db.query(UserSettings)\
            .filter(UserSettings.user_id == user_id)\
            .first()

    def update_preferences(self, user_id: int, preferences: dict) -> Optional[UserSettings]:
        settings = self.get_by_user_id(user_id)
        if settings:
            settings.preferences = preferences
            self.db.commit()
            self.db.refresh(settings)
        return settings

    def update_api_keys(self, user_id: int, api_keys: dict) -> Optional[UserSettings]:
        settings = self.get_by_user_id(user_id)
        if settings:
            settings.api_keys = api_keys
            self.db.commit()
            self.db.refresh(settings)
        return settings

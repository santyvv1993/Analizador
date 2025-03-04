from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, JSON, Enum, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..config.database import Base

# Primero definimos FileRelationship para que esté disponible para File
class FileRelationship(Base):
    __tablename__ = "file_relationships"

    source_file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    related_file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    relationship_type = Column(String(50))
    confidence = Column(Float)
    relationship_metadata = Column(JSON)  # Cambiado de metadata a relationship_metadata
    created_at = Column(DateTime, default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum('admin', 'user', 'api'), nullable=False, default='user')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    last_login = Column(DateTime)

    # Relaciones
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    files = relationship("File", back_populates="user")

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    preferences = Column(JSON)
    api_keys = Column(JSON)
    notification_settings = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)

    # Relaciones
    user = relationship("User", back_populates="settings")

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String(255), nullable=False)
    file_path = Column(String(1024), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    hash_value = Column(String(64))
    mime_type = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    last_modified = Column(DateTime)
    is_processed = Column(Boolean, default=False)
    file_metadata = Column(JSON)  # Cambiado de metadata a file_metadata

    # Relaciones
    user = relationship("User", back_populates="files")
    versions = relationship("FileVersion", back_populates="file")
    categories = relationship("Category", secondary="file_categories", back_populates="files")
    analysis_results = relationship("AnalysisResult", back_populates="file")
    entities = relationship("ExtractedEntity", back_populates="file")
    source_relationships = relationship(
        "FileRelationship",
        foreign_keys=[FileRelationship.source_file_id],
        backref="source_file"
    )
    related_relationships = relationship(
        "FileRelationship",
        foreign_keys=[FileRelationship.related_file_id],
        backref="related_file"
    )

class FileVersion(Base):
    __tablename__ = "file_versions"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    version_number = Column(Integer)
    file_path = Column(String(1024))
    hash_value = Column(String(64))
    created_at = Column(DateTime, default=func.now())
    version_metadata = Column(JSON)  # Cambiado de metadata a version_metadata

    # Relaciones
    file = relationship("File", back_populates="versions")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(1000))  # Añadida longitud
    parent_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    files = relationship("File", secondary="file_categories", back_populates="categories")
    subcategories = relationship("Category")

class FileCategory(Base):
    __tablename__ = "file_categories"

    file_id = Column(Integer, ForeignKey('files.id'), primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'), primary_key=True)
    confidence = Column(Float)
    created_at = Column(DateTime, default=func.now())

class ProcessingQueue(Base):
    __tablename__ = "processing_queue"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    status = Column(Enum('pending', 'processing', 'completed', 'failed'), default='pending')
    priority = Column(Integer, default=0)
    attempts = Column(Integer, default=0)
    error_message = Column(String(1000))  # Añadida longitud
    created_at = Column(DateTime, default=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    parent_task_id = Column(Integer, ForeignKey('processing_queue.id'))
    task_type = Column(String(50), default='file_processing')
    timeout_seconds = Column(Integer, default=3600)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    analysis_type = Column(String(50), nullable=False)
    confidence = Column(Float)
    result_data = Column(JSON)
    model_used = Column(String(100))
    tokens_used = Column(Integer)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    file = relationship("File", back_populates="analysis_results")

class ExtractedEntity(Base):
    __tablename__ = "extracted_entities"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    entity_type = Column(String(50))
    entity_value = Column(String(1000))  # Añadida longitud
    confidence = Column(Float)
    context = Column(String(2000))  # Añadida longitud
    entity_metadata = Column(JSON)  # Cambiado de metadata a entity_metadata
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    file = relationship("File", back_populates="entities")

class Plugin(Base):
    __tablename__ = "plugins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    version = Column(String(20), nullable=False)
    enabled = Column(Boolean, default=True)
    settings = Column(JSON)
    created_at = Column(DateTime, default=func.now())
    last_updated = Column(DateTime)

    # Relaciones
    processing_history = relationship("ProcessingHistory", back_populates="plugin")

class ProcessingHistory(Base):
    __tablename__ = "processing_history"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    plugin_id = Column(Integer, ForeignKey('plugins.id'))
    status = Column(Enum('success', 'failure'), nullable=False)
    processing_time = Column(Float)
    error_message = Column(String(1000))  # Añadida longitud
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    plugin = relationship("Plugin", back_populates="processing_history")

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)
    component = Column(String(50))
    message = Column(String(2000))
    stack_trace = Column(String(4000))
    created_at = Column(DateTime, default=func.now())

class PerformanceMetric(Base):
    __tablename__ = "performance_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    component = Column(String(50))
    created_at = Column(DateTime, default=func.now())

class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(50))
    schedule_type = Column(Enum('one-time', 'recurring'))
    cron_expression = Column(String(100))
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    settings = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class ApiUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    endpoint = Column(String(255))
    method = Column(String(10))
    response_time = Column(Float)
    status_code = Column(Integer)
    request_size = Column(Integer)
    response_size = Column(Integer)
    created_at = Column(DateTime, default=func.now())

    # Relaciones
    user = relationship("User")

import os
import sys
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.models.models import Base, User

# Configurar base de datos de prueba usando la variable de entorno DB_NAME_TEST
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME_TEST = os.getenv("DB_NAME_TEST", "core_system_test")

# Determinar qué tipo de base de datos usar para pruebas (en memoria o MySQL)
USE_IN_MEMORY_DB = os.getenv("USE_IN_MEMORY_DB", "False").lower() == "true"

if USE_IN_MEMORY_DB:
    TEST_DATABASE_URL = "sqlite:///:memory:"
else:
    TEST_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}"

@pytest.fixture(scope="session")
def test_engine():
    """Crear motor de base de datos para pruebas"""
    if not USE_IN_MEMORY_DB:
        # Verificar si la base de datos de prueba existe, crearla si no
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}")
        with engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME_TEST}"))
            connection.execute(text(f"USE {DB_NAME_TEST}"))
        engine.dispose()
    
    # Conectar a la base de datos de prueba
    engine = create_engine(TEST_DATABASE_URL)
    
    # Crear todas las tablas en la base de datos de prueba
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Limpiar después de todas las pruebas
    if USE_IN_MEMORY_DB:
        Base.metadata.drop_all(bind=engine)
    else:
        # Para MySQL, truncamos las tablas en lugar de eliminarlas
        with engine.connect() as connection:
            connection.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            for table in reversed(Base.metadata.sorted_tables):
                connection.execute(text(f"TRUNCATE TABLE {table.name}"))
            connection.execute(text("SET FOREIGN_KEY_CHECKS=1"))

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Proporcionar una sesión de base de datos para pruebas"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()  # Revertir cambios pendientes
        session.close()  # Cerrar la sesión

@pytest.fixture(scope="session", autouse=True)
def setup_test_data(test_engine):
    """
    Inicializa datos básicos necesarios para las pruebas.
    Utiliza autouse=True para asegurar que se ejecuta automáticamente.
    """
    # Crear una sesión de prueba
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    
    try:
        # Verificar si ya existe un usuario admin
        admin_user = session.query(User).filter(User.username == "admin").first()
        
        # Si no existe, creamos el usuario admin
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password="admin_password",  # En producción debería estar hash
                role="admin",
                is_active=True,
                created_at=datetime.now()
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)
        
        # Aquí podemos inicializar otros datos básicos para todas las pruebas
        
        yield
    finally:
        session.close()

def pytest_configure(config):
    # Configurar marcadores para pruebas
    config.addinivalue_line(
        "markers", "analysis_service: mark test that requires database setup"
    )
    config.addinivalue_line(
        "markers", "db: mark test that uses the database"
    )

def pytest_collection_modifyitems(config, items):
    # Ya no es necesario marcar automáticamente las pruebas de análisis para omitirlas
    # Ya que ahora tenemos una base de datos de prueba real
    pass

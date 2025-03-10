import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Importar desde sqlalchemy.orm
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "core_system")

# URL de conexión para SQLAlchemy
def get_db_url(db_name=None):
    """
    Devuelve la URL de conexión para SQLAlchemy
    
    Args:
        db_name: Nombre de la base de datos (opcional, por defecto usa DB_NAME del .env)
        
    Returns:
        str: URL de conexión para SQLAlchemy
    """
    name = db_name or DB_NAME
    return f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{name}"

DATABASE_URL = get_db_url()

# Crear motor de base de datos
engine = create_engine(DATABASE_URL)

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos declarativos usando la nueva ubicación
Base = declarative_base()  # Este es el cambio principal

def get_db():
    """
    Proporciona una sesión de base de datos para usar en una aplicación
    
    Yields:
        Session: Sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
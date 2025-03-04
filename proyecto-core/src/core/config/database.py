from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # Cambiado a import directo
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Construir URL de conexión usando variables de entorno
DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
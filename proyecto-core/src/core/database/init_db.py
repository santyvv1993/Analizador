from sqlalchemy import text
from ..config.database import engine, SessionLocal, Base
from ..models.models import *

def init_database():
    """Inicializa la base de datos creando todas las tablas"""
    db = SessionLocal()
    try:
        # Desactivar foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # Eliminar todas las tablas existentes
        Base.metadata.drop_all(bind=engine)
        
        # Crear todas las tablas nuevas
        Base.metadata.create_all(bind=engine)
        
        # Reactivar foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        db.commit()
        print("Base de datos inicializada correctamente")
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()

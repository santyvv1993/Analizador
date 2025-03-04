from ..config.database import SessionLocal

def get_db():
    """Proporciona una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

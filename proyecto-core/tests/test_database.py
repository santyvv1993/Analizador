import os
import sys
import pytest
from sqlalchemy import text, inspect

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.core.config.database import SessionLocal, engine
from src.core.models.models import User, Base
from src.core.repositories.user_repository import UserRepository

@pytest.fixture(scope="module")
def db():
    """Fixture que proporciona una sesión de base de datos para las pruebas"""
    # Crear todas las tablas para las pruebas
    Base.metadata.create_all(bind=engine)
    
    # Crear una sesión de prueba
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Crear una nueva conexión para la limpieza
        cleanup_db = SessionLocal()
        try:
            # Desactivar foreign key checks
            cleanup_db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            cleanup_db.commit()
            
            # Obtener todas las tablas y eliminarlas
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                cleanup_db.execute(text(f"DROP TABLE IF EXISTS {table}"))
            
            cleanup_db.commit()
            
            # Reactivar foreign key checks
            cleanup_db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            cleanup_db.commit()
        finally:
            cleanup_db.close()

@pytest.fixture
def user_repository(db):
    """Fixture que proporciona un repositorio de usuarios"""
    return UserRepository(db)

def test_database_connection(db):
    """Prueba la conexión a la base de datos"""
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1, "La conexión a la base de datos falló"
    except Exception as e:
        pytest.fail(f"Error de conexión: {e}")

def test_user_crud(user_repository):
    """Prueba las operaciones CRUD del repositorio de usuarios"""
    # Crear usuario de prueba
    test_user = User(
        username="test_user",
        email="test@example.com",
        password="test_password",
        role="user"
    )
    
    # Probar creación
    created_user = user_repository.create(test_user)
    assert created_user.id is not None
    assert created_user.username == "test_user"
    
    # Probar lectura
    retrieved_user = user_repository.get_by_id(created_user.id)
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"
    
    # Probar actualización
    retrieved_user.username = "updated_user"
    updated_user = user_repository.update(retrieved_user)
    assert updated_user.username == "updated_user"
    
    # Probar eliminación
    assert user_repository.delete(created_user.id) is True
    assert user_repository.get_by_id(created_user.id) is None

def test_user_query_methods(user_repository):
    """Prueba métodos específicos del repositorio de usuarios"""
    # Crear usuario de prueba
    test_user = User(
        username="test_query",
        email="test_query@example.com",
        password="test_password",
        role="user"
    )
    created_user = user_repository.create(test_user)
    
    # Probar búsqueda por email
    found_user = user_repository.get_by_email("test_query@example.com")
    assert found_user is not None
    assert found_user.username == "test_query"
    
    # Probar búsqueda por username
    found_user = user_repository.get_by_username("test_query")
    assert found_user is not None
    assert found_user.email == "test_query@example.com"
    
    # Limpiar
    user_repository.delete(created_user.id)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

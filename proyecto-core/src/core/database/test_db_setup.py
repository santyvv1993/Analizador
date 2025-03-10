"""
Script para configurar o restablecer la base de datos de pruebas.
Se puede ejecutar directamente para configurar la base de datos antes de las pruebas.
"""
import os
import sys
import argparse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Agregar directorio raíz al PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.core.models.models import Base

def setup_test_db(force=False, use_sql=False):
    """
    Configura la base de datos de prueba
    
    Args:
        force: Si es True, elimina la base de datos si existe
        use_sql: Si es True, usa el archivo schema.sql en lugar de SQLAlchemy
    """
    # Cargar variables de entorno
    load_dotenv()
    
    # Configuración de base de datos
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME_TEST = os.getenv("DB_NAME_TEST", "core_system_test")
    
    # Crear motor para conexión al servidor
    server_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}"
    engine = create_engine(server_url)
    
    with engine.connect() as connection:
        # Eliminar base de datos si existe y se especifica force
        if force:
            try:
                connection.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME_TEST}"))
                print(f"Base de datos {DB_NAME_TEST} eliminada")
            except Exception as e:
                print(f"Error al eliminar la base de datos: {e}")
        
        # Crear base de datos
        try:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME_TEST}"))
            print(f"Base de datos {DB_NAME_TEST} creada o ya existe")
        except Exception as e:
            print(f"Error al crear la base de datos: {e}")
            return
    
    # Cerrar conexión al servidor
    engine.dispose()
    
    # Crear motor para conexión a la base de datos
    db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME_TEST}"
    engine = create_engine(db_url)
    
    if use_sql:
        # Usar archivo SQL para crear tablas
        script_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(script_dir, "schema.sql")
        
        if not os.path.exists(schema_path):
            print(f"Archivo schema.sql no encontrado en {schema_path}")
            return
        
        with open(schema_path, 'r') as f:
            sql = f.read()
        
        with engine.connect() as connection:
            connection.execute(text(sql))
            print("Tablas creadas con schema.sql")
    else:
        # Usar SQLAlchemy para crear tablas
        Base.metadata.create_all(engine)
        
        # Inicializar datos básicos
        from src.core.models.models import User
        from datetime import datetime
        from sqlalchemy.orm import sessionmaker
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
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
            
            # También agregar un usuario normal para pruebas
            test_user = User(
                username="test_user",
                email="test@example.com",
                password="test_password",  # En producción debería estar hash
                role="user",
                is_active=True,
                created_at=datetime.now()
            )
            session.add(test_user)
            
            session.commit()
            print("Usuarios de prueba creados")
        
        session.close()
        
        print("Tablas creadas con SQLAlchemy")
    
    print(f"Base de datos de prueba {DB_NAME_TEST} configurada correctamente")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Configurar base de datos de prueba')
    parser.add_argument('--force', action='store_true', help='Eliminar base de datos si existe')
    parser.add_argument('--use-sql', action='store_true', help='Usar archivo schema.sql en lugar de SQLAlchemy')
    args = parser.parse_args()
    
    setup_test_db(args.force, args.use_sql)

from sqlalchemy import text, inspect
from ..config.database import engine, SessionLocal, Base
from ..models.models import *
import os

def get_all_tables(db):
    """Obtiene todas las tablas existentes en la base de datos"""
    inspector = inspect(engine)
    return inspector.get_table_names()

def drop_all_tables(db):
    """Elimina todas las tablas existentes de la base de datos"""
    try:
        # Desactivar foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        db.commit()

        # Obtener todas las tablas
        tables = get_all_tables(db)
        
        print(f"Tablas encontradas: {tables}")
        
        # Eliminar cada tabla
        for table in tables:
            print(f"Eliminando tabla: {table}")
            db.execute(text(f"DROP TABLE IF EXISTS {table}"))
            db.commit()

        # Reactivar foreign key checks
        db.execute(text("SET FOREIGN_KEY_CHECKS=1"))
        db.commit()
        print("Todas las tablas han sido eliminadas")
        
    except Exception as e:
        print(f"Error al eliminar tablas: {e}")
        raise

def execute_sql_file(db, file_path):
    """Ejecuta un archivo SQL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql = file.read()
            # Dividir el archivo en statements individuales
            statements = sql.split(';')
            for statement in statements:
                if statement.strip():
                    try:
                        db.execute(text(statement))
                        db.commit()
                    except Exception as e:
                        print(f"Error ejecutando statement: {statement[:100]}...")
                        print(f"Error: {e}")
                        raise
    except FileNotFoundError:
        print(f"No se encontró el archivo SQL en: {file_path}")
        raise

def setup_database(use_sql_file=False, force_recreate=False):
    """
    Configura la base de datos usando schema.sql o SQLAlchemy
    
    Args:
        use_sql_file (bool): Si True, usa schema.sql, si False usa SQLAlchemy
        force_recreate (bool): Si True, elimina todas las tablas existentes antes de crear nuevas
    """
    db = SessionLocal()
    try:
        print("Iniciando configuración de base de datos...")
        
        # Verificar si existen tablas
        existing_tables = get_all_tables(db)
        if existing_tables:
            if force_recreate:
                print("Se encontraron tablas existentes. Eliminando...")
                drop_all_tables(db)
            else:
                print("La base de datos ya contiene tablas. Use --force para recrear.")
                return

        if use_sql_file:
            # Usar schema.sql
            schema_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                '..',
                '..',
                '..',
                'ScriptDB',
                'schema.sql'
            )
            print(f"Ejecutando schema.sql desde: {schema_path}")
            execute_sql_file(db, schema_path)
        else:
            # Usar SQLAlchemy
            print("Creando tablas usando SQLAlchemy...")
            Base.metadata.create_all(bind=engine)

        print("Base de datos configurada correctamente")
        
    except Exception as e:
        print(f"Error durante la configuración: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Configuración de la base de datos')
    parser.add_argument('--use-sql', action='store_true', 
                       help='Usar schema.sql en lugar de SQLAlchemy')
    parser.add_argument('--force', action='store_true',
                       help='Forzar la recreación de todas las tablas')
    args = parser.parse_args()
    
    setup_database(use_sql_file=args.use_sql, force_recreate=args.force)

# Core System

## Estructura
```
core/
├── __init__.py
├── models/                  # Modelos de datos
│   ├── __init__.py
│   └── models.py
├── repositories/            # Repositorios
│   ├── __init__.py
│   ├── base_repository.py
│   ├── user_repository.py
│   ├── file_repository.py
│   ├── category_repository.py
│   ├── plugin_repository.py
│   ├── analysis_repository.py
│   └── processing_repository.py
├── services/               # Servicios de negocio
│   ├── __init__.py
│   ├── document_service.py
│   ├── analysis_service.py
│   └── file_processor_service.py
├── processors/             # Procesadores de archivos
│   ├── __init__.py
│   ├── pdf_processor.py
│   ├── excel_processor.py
│   ├── word_processor.py
│   ├── uasset_processor.py
│   └── processor_factory.py
├── config/                 # Configuración
│   ├── __init__.py
│   ├── database.py
│   └── settings.py
├── database/               # Conexión a base de datos
|   ├── db_session.py
|   └── init_db.py
└── api/                    # API RESTful
    ├── __init__.py
    ├── main.py
    ├── endpoints/
    └── schemas/
```

## Componentes Principales
- [Modelos](models.md)
- [Repositorios](repositories.md)
- [Servicios](services.md)
- [Procesadores](processors.md)
- [API](api.md)

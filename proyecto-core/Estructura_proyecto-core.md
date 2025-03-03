### Estructura de la Aplicación

```
proyecto-core/
└── src/
    ├── desktop_app/
    │   ├── __init__.py
    │   ├── main.py                  # Punto de entrada
    │   ├── resources/               # Recursos (iconos, estilos)
    │   ├── views/                   # Interfaces
    │   │   ├── main_window.py
    │   │   ├── document_view.py
    │   │   ├── analysis_view.py
    │   │   └── settings_view.py
    │   ├── controllers/             # Lógica de la interfaz
    │   │   ├── document_controller.py
    │   │   ├── analysis_controller.py
    │   │   └── settings_controller.py
    │   ├── models/                  # Modelos específicos para la UI
    │   │   └── table_models.py
    │   └── utils/                   # Utilidades para la UI
    │       ├── qt_helpers.py
    │       └── config_manager.py
    ├── core/
    │   ├── __init__.py
    │   ├── services/                # Servicios de negocio
    │   │   ├── document_service.py
    │   │   ├── analysis_service.py
    │   │   └── file_processor_service.py
    │   ├── repositories/            # Repositorios de datos
    │   │   ├── document_repository.py
    │   │   ├── category_repository.py
    │   │   └── entity_repository.py
    │   ├── processors/              # Procesadores de archivos
    │   │   ├── __init__.py
    │   │   ├── pdf_processor.py
    │   │   ├── excel_processor.py
    │   │   ├── word_processor.py
    │   │   ├── uasset_processor.py  # Procesador para archivos UASSET
    │   │   └── processor_factory.py
    │   ├── config/                  # Configuración centralizada
    │   │   └── settings.py
    │   └── api/                     # API RESTful
    │       ├── __init__.py
    │       ├── main.py              # Punto de entrada de la API
    │       ├── endpoints/           # Endpoints de la API
    │       │   ├── document_endpoints.py
    │       │   ├── analysis_endpoints.py
    │       │   └── file_endpoints.py
    │       └── schemas/             # Esquemas de datos para la API
    │           ├── document_schema.py
    │           ├── analysis_schema.py
    │           └── file_schema.py
    └── tests/                       # Pruebas unitarias y de integración
        ├── __init__.py
        ├── test_services.py
        ├── test_repositories.py
        ├── test_processors.py
        └── test_api.py
```
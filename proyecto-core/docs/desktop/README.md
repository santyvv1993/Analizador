# Desktop Application

## Estructura
```
desktop_app/
├── __init__.py
├── main.py                # Punto de entrada
├── resources/             # Recursos
├── views/                 # Interfaces
│   ├── main_window.py
│   ├── document_view.py
│   ├── analysis_view.py
│   └── settings_view.py
├── controllers/           # Controladores
│   ├── document_controller.py
│   ├── analysis_controller.py
│   └── settings_controller.py
├── models/               # Modelos UI
│   └── table_models.py
└── utils/               # Utilidades
    ├── qt_helpers.py
    └── config_manager.py
```

## Componentes
- [Vistas](views.md)
- [Controladores](controllers.md)
- [Modelos UI](ui-models.md)

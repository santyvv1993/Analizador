# Sistema Analizador de Información Local

## Descripción General
Sistema centralizado para análisis, clasificación y consulta de información en archivos locales, con procesamiento inteligente mediante IA y capacidad de expansión a través de plugins.

## Funcionalidades Principales
- 📁 Procesamiento inteligente de archivos (PDF, Excel, Word, UASSET)
- 🤖 Análisis automatizado mediante IA (OpenAI/DeepSeek)
- 🔍 Sistema de búsqueda y consulta avanzada
- 🧩 Arquitectura extensible mediante plugins
- 🖥️ Interfaz de administración desktop
- 🌐 API REST para integraciones

## Estructura del Proyecto

```
proyecto-core/
├── src/
│   ├── desktop_app/     # Aplicación de escritorio
│   ├── core/            # Núcleo del sistema
│   └── tests/           # Pruebas
├── docs/                # Documentación detallada
├── requirements.txt     # Dependencias del proyecto
└── .env.example         # Plantilla de variables de entorno
```

## Primeros Pasos

### Requisitos
- Python 3.10+
- MySQL 8.0+
- Dependencias adicionales en requirements.txt

### Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/username/proyecto-core.git
cd proyecto-core
```

2. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Inicializar base de datos
```bash
python -m src.core.database.db_setup --force
```

### Ejecutar la aplicación
```bash
# Iniciar API
python -m src.core.api.main

# Iniciar aplicación desktop
python -m src.desktop_app.main
```

## Documentación

- [Guía de Desarrollo](docs/development-guide.md) - Guías para desarrolladores
- [Definición Funcional](docs/functional-definition.md) - Especificación detallada del sistema
- [Roadmap](docs/roadmap.md) - Plan de desarrollo detallado
- [Documentación Técnica](docs/technical/) - Detalles técnicos y arquitectura
- [Documentación de API](docs/api/) - Referencia de la API REST

## Licencia

[MIT](LICENSE)

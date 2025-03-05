# Sistema Analizador de Información Local

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://semver.org)
[![License](https://img.shields.io-badge/license-MIT-green.svg)](LICENSE)

## Descripción General
Sistema de análisis e indexación que examina archivos en sus ubicaciones originales, proporcionando análisis inteligente mediante IA y capacidades de búsqueda avanzada. No requiere mover o copiar archivos, trabajando directamente con los documentos en su ubicación original.

## Funcionalidades Principales
- 📁 Análisis in-situ de archivos (PDF, Excel, Word)
- 🤖 Análisis mediante IA (OpenAI/DeepSeek)
- 🔍 Indexación y búsqueda avanzada
- 📊 Extracción inteligente de información
- 🧩 Sistema extensible de procesadores
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

## Configuración de Proveedores de IA

El sistema soporta múltiples proveedores de IA. Configura las credenciales en tu archivo .env:

## Ejemplos de Uso

### Análisis de Archivos
```python
from analizador.core import DocumentProcessor

processor = DocumentProcessor()
result = processor.process("documento.pdf")
print(f"Contenido extraído: {result.content}")
```

### Análisis con IA
```python
from analizador.core import AIAnalyzer

analyzer = AIAnalyzer()
analysis = analyzer.analyze_document("documento.pdf")
print(f"Categoría: {analysis.category}")
print(f"Entidades detectadas: {analysis.entities}")
```

### Uso de la API
```bash
# Subir un documento
curl -X POST http://localhost:8000/api/documents \
  -H "Content-Type: multipart/form-data" \
  -F "file=@documento.pdf"

# Consultar análisis
curl http://localhost:8000/api/documents/1/analysis
```

## Documentación
- [Guía de Desarrollo](docs/development-guide.md) - Guías para desarrolladores
- [Definición Funcional](docs/functional-definition.md) - Especificación detallada
- [Roadmap](docs/roadmap.md) - Plan de desarrollo detallado
- [Documentación Técnica](docs/technical/) - Detalles técnicos
- [Documentación de API](docs/api/) - Referencia de la API REST

## Contribuir
¡Las contribuciones son bienvenidas! Por favor, lee nuestra [guía de contribución](CONTRIBUTING.md) antes de empezar.

## Comunidad y Soporte
- [Reportar un Bug](https://github.com/yourusername/analizador/issues)
- [Solicitar una Feature](https://github.com/yourusername/analizador/issues)
- [Discord](https://discord.gg/tuenlace)
- Email: soporte@tudominio.com

## Licencia
[MIT](LICENSE)

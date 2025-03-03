# Roadmap Actualizado: Sistema Core con Python y MySQL

## Comandos Útiles

1. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   # Activar en Windows
   venv\Scripts\activate
   # Activar en macOS/Linux
   source venv/bin/activate
   ```
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```   
3. **Iniciar servidor de desarrollo**:
   ```bash
   uvicorn src.core.api.main:app --reload
   ```

## Introducción

## Resumen de Fases
1. **Fase 1**: Preparación y Configuración (Semanas 1-2)
2. **Fase 2**: Módulo de Procesamiento de Archivos (Semanas 3-4)
3. **Fase 3**: Integración con IA (Semanas 5-6)
4. **Fase 4**: Sistema de Almacenamiento y Consulta (Semanas 7-8)
5. **Fase 5**: Interfaz de Administración Desktop (Semanas 9-10)
6. **Fase 6**: API y Servicios Web (Semanas 11-12)
7. **Fase 7**: Operaciones Asíncronas y Optimización (Semanas 13-14)
8. **Fase 8**: Extensibilidad y Plugins (Semanas 15-16)

## Fase 1: Preparación y Configuración (Semanas 1-2)

### Semana 1: Configuración del Entorno
1. **Día 1-2: Preparación del entorno de desarrollo**
   - Instalar Python 3.10+ y pip
   - Instalar MySQL Server y MySQL Workbench
   - Configurar un entorno virtual con `venv`
   ```bash
   python -m venv venv
   # Activar en Windows
   venv\Scripts\activate
   # Activar en macOS/Linux
   source venv/bin/activate
   ```
   - Instalar Git y configurar repositorio

2. **Día 3-4: Estructura inicial del proyecto**
   - Crear la estructura de carpetas según el diseño propuesto
   - Inicializar archivo `requirements.txt` con dependencias básicas:
   ```
   fastapi==0.103.1
   uvicorn==0.23.2
   sqlalchemy==2.0.20
   mysql-connector-python==8.1.0
   python-dotenv==1.0.0
   pydantic==2.3.0
   pytest==7.4.2
   PyPDF2==3.0.1
   pandas==2.1.0
   openpyxl==3.1.2
   openai==0.28.0
   python-multipart==0.0.6
   PyQt5==5.15.9  # Para interfaz de administración
   ```

3. **Día 5: Configuración de variables de entorno**
   - Crear archivo `.env.example` y `.env` para variables de entorno
   - Configurar datos de conexión a MySQL y claves API en `.env`
   ```
   # Base de datos
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=core_system
   
   # OpenAI
   OPENAI_API_KEY=your_api_key
   
   # Sistema
   FILE_STORAGE_PATH=./storage/documents
   ```

### Semana 2: Diseño y Configuración de Base de Datos

1. **Día 1-2: Diseño del esquema de base de datos**
   - Crear script SQL para definir tablas y relaciones
   - Implementar modelado en workbench
   - Crear scripts de inicialización y migración

2. **Día 3-4: Configuración ORM**
   - Configurar SQLAlchemy
   - Implementar modelos de entidades según el esquema
   - Crear capa de repositorio para acceso a datos

3. **Día 5: Pruebas de conexión**
   - Implementar pruebas de conectividad
   - Validar operaciones CRUD básicas
   - Configurar script de migración automática

## Fase 2: Módulo de Procesamiento de Archivos (Semanas 3-4)

### Semana 3: Procesamiento Básico

1. **Día 1-2: Procesamiento de PDFs**
   - Implementar clase PDFProcessor
   - Funciones para extraer texto
   - Manejo de excepciones y errores

2. **Día 3-4: Procesamiento de Excel**
   - Implementar clase ExcelProcessor
   - Funciones para leer hojas y datos
   - Conversión a formatos manejables

3. **Día 5: Sistema de almacenamiento**
   - Implementar sistema para guardar archivos en disco
   - Crear estructura de directorios para organizar archivos
   - Funciones de carga y descarga de archivos

### Semana 4: Procesamiento Avanzado

1. **Día 1-2: Detección de tipos de documento**
   - Implementar análisis básico de contenido
   - Sistema de reglas para clasificación preliminar
   - Manejo de metadatos de archivos

2. **Día 3-4: Preprocesamiento para IA**
   - Normalizar texto extraído
   - Chunking para documentos grandes
   - Extracción de información básica (fechas, números, etc.)

3. **Día 5: Pruebas y refinamiento**
   - Pruebas unitarias del módulo de procesamiento
   - Optimización de rendimiento
   - Documentación de componentes

## Fase 3: Integración con IA (Semanas 5-6)

### Semana 5: Configuración del Cliente IA

1. **Día 1-2: Implementación de cliente OpenAI**
   - Configurar conexión a API
   - Implementar función de análisis básico
   - Gestión de tokens y costos

2. **Día 3-4: Diseño de prompts**
   - Crear templates para diferentes tipos de análisis
   - Optimizar prompts para mejores resultados
   - Implementar system prompts específicos

3. **Día 5: Manejo de respuestas**
   - Parsear respuestas JSON
   - Manejar errores de API
   - Implementar reintentos y fallbacks

### Semana 6: Procesamiento Avanzado con IA

1. **Día 1-2: Clasificación de documentos**
   - Implementar análisis de tipo de documento
   - Extracción de metadatos avanzados
   - Sistema de confianza para clasificaciones

2. **Día 3-4: Extracción de entidades**
   - Identificar fechas, montos, personas, etc.
   - Normalizar entidades extraídas
   - Relacionar entidades con categorías

3. **Día 5: Generación de resúmenes**
   - Implementar generación de resúmenes
   - Extracción de puntos clave
   - Formateo de salida para almacenamiento

## Fase 4: Sistema de Almacenamiento y Consulta (Semanas 7-8)

### Semana 7: Almacenamiento Estructurado

1. **Día 1-2: Implementación de repositorios**
   - Implementar DocumentRepository
   - Implementar CategoryRepository
   - Implementar EntityRepository

2. **Día 3-4: Servicios de almacenamiento**
   - Crear servicios para guardar resultados de IA
   - Implementar transacciones para operaciones múltiples
   - Gestión de relaciones entre entidades

3. **Día 5: Validación y normalización**
   - Implementar validadores de datos
   - Normalizar información antes de almacenar
   - Manejo de conflictos y duplicados

### Semana 8: Sistema de Consultas

1. **Día 1-2: Consultas básicas**
   - Implementar búsqueda por tipo de documento
   - Filtrado por fechas y otros metadatos
   - Paginación de resultados

2. **Día 3-4: Consultas avanzadas**
   - Búsqueda por contenido
   - Filtrado multifacético
   - Ordenamiento y agrupación

3. **Día 5: Optimización**
   - Indexación para consultas frecuentes
   - Caché de resultados
   - Monitoreo de rendimiento

## Fase 5: Interfaz de Administración Desktop (Semanas 9-10) - NUEVA

### Semana 9: Diseño e Implementación Básica

1. **Día 1-2: Configuración de PyQt5**
   - Instalar PyQt5 y Qt Designer
   - Diseñar estructura básica de la interfaz
   - Configurar sistema de navegación entre pantallas

2. **Día 3-4: Interfaz de gestión de documentos**
   - Implementar vista de lista de documentos
   - Crear formulario de carga de archivos
   - Visualización básica de documentos procesados

3. **Día 5: Interfaz de administración**
   - Implementar pantalla de configuración
   - Conexión con base de datos y APIs
   - Gestión de categorías y clasificaciones

### Semana 10: Funcionalidades Avanzadas e Integración

1. **Día 1-2: Panel de análisis con IA**
   - Implementar consola de pruebas para IA
   - Visualización de respuestas
   - Configuración de parámetros de análisis

2. **Día 3-4: Visualización de datos**
   - Implementar gráficos y estadísticas
   - Panel de métricas
   - Exportación de resultados

3. **Día 5: Integración y pruebas**
   - Conexión completa con el core
   - Pruebas de flujo completo
   - Refinamiento de la experiencia de usuario

## Fase 6: API y Servicios Web (Semanas 11-12)

### Semana 11: Desarrollo de API REST

1. **Día 1-2: Configuración de FastAPI**
   - Configurar servidor FastAPI
   - Implementar middleware y dependencias
   - Configurar documentación automática

2. **Día 3-4: Endpoints de documentos**
   - Implementar endpoint de carga de archivos
   - Endpoint de consulta de documentos
   - Endpoint de análisis manual

3. **Día 5: Endpoints de consulta**
   - Implementar endpoints de búsqueda
   - Endpoints para estadísticas
   - Documentación de API

### Semana 12: Autenticación y Seguridad

1. **Día 1-2: Sistema de autenticación**
   - Implementar JWT para autenticación
   - Gestión de usuarios y roles
   - Protección de endpoints

2. **Día 3-4: Seguridad**
   - Validación de entradas
   - Limitación de tasa
   - Logging de actividad

3. **Día 5: Pruebas de integración**
   - Pruebas end-to-end
   - Validación de seguridad
   - Documentación final

## Fase 7: Operaciones Asíncronas y Optimización (Semanas 13-14)

### Semana 13: Procesamiento Asíncrono

1. **Día 1-2: Cola de tareas**
   - Implementar sistema de cola con Celery/RQ
   - Configurar workers
   - Monitoreo de tareas

2. **Día 3-4: Procesamiento en background**
   - Convertir análisis de IA a tareas asíncronas
   - Implementar notificaciones de finalización
   - Gestión de errores en procesamiento asíncrono

3. **Día 5: Escalabilidad**
   - Optimizar uso de recursos
   - Implementar paralelización
   - Pruebas de carga

### Semana 14: Refinamiento y Documentación

1. **Día 1-2: Pruebas finales**
   - Pruebas de integración completas
   - Pruebas de rendimiento
   - Corrección de bugs

2. **Día 3-4: Documentación**
   - Documentación técnica
   - Manuales de usuario
   - Guía de desarrollo

3. **Día 5: Despliegue**
   - Preparación para producción
   - Configuración de entorno
   - Estrategia de backup y recuperación

## Fase 8: Extensibilidad y Plugins (Semanas 15-16)

### Semana 15: Diseño de Plugins

1. **Día 1-2: Arquitectura de Plugins**
   - Diseñar arquitectura para soportar plugins
   - Definir interfaces y contratos para plugins

2. **Día 3-4: Implementación de Plugins**
   - Crear ejemplos de plugins (e.g., procesador de UASSET)
   - Documentar cómo crear y registrar plugins

3. **Día 5: Pruebas de Plugins**
   - Pruebas unitarias y de integración para plugins
   - Validación de compatibilidad con el core

### Semana 16: Integración y Documentación

1. **Día 1-2: Integración de Plugins**
   - Integrar plugins con el sistema principal
   - Validar la carga dinámica de plugins

2. **Día 3-4: Documentación de Plugins**
   - Crear guía de desarrollo de plugins
   - Documentar API y ejemplos de uso

3. **Día 5: Pruebas y Refinamiento**
   - Pruebas de flujo completo con plugins
   - Refinamiento de la experiencia de usuario

## Consejos Adicionales para el Desarrollo de la Interfaz 

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

### Consejos para Desarrollo con PyQt5

1. **Diseño de interfaces**:
   - Usa Qt Designer para crear archivos .ui y convertirlos a Python con:
     ```bash
     pyuic5 -x input.ui -o output.py
     ```
   - Separa la lógica de la interfaz (Modelo-Vista-Controlador)

2. **Comunicación con el core**:
   - Crea una capa de servicio que conecte la UI con el core:
     ```python
     class CoreService:
         def analyze_document(self, file_path):
             # Conecta con la lógica del core
             processor = PDFProcessor()
             text = processor.extract_text(file_path)
             
             ai_client = OpenAIClient()
             result = ai_client.analyze_document(text)
             
             return result
     ```

3. **Manejo de eventos asíncronos**:
   - Usa QThreads para operaciones largas (análisis de IA, procesamiento de archivos)
   - Implementa señales y slots para actualizar la UI sin bloquearla

4. **Ejemplos de pantallas principales**:

   - **Panel principal**: Dashboard con métricas y accesos rápidos
   - **Gestor de documentos**: Lista de documentos con filtros y acciones
   - **Consola de análisis**: Área de texto para entrada/salida de IA
   - **Configuración**: Conexiones a bases de datos y APIs

### Consejos para Desarrollo de Plugins

1. **Diseño de Plugins:**

- Define interfaces claras para los plugins
- Usa patrones de diseño como el patrón de estrategia para facilitar la integración de nuevos procesadores de archivos

2. **Registro de Plugins:**

- Implementa un sistema de registro de plugins que permita la carga dinámica de nuevos procesadores
- Documenta cómo registrar y utilizar plugins en el sistema

3. **Pruebas y Validación:**

- Escribe pruebas unitarias y de integración para cada plugin
- Asegúrate de que los plugins sean compatibles con el core y no introduzcan errores

4. **Documentación y Ejemplos:**

- Proporciona ejemplos claros de cómo desarrollar y registrar plugins
- Mantén una documentación actualizada sobre la arquitectura de plugins y las interfaces disponibles

```python
class PluginInterface:
    def process(self, file_path):
        raise NotImplementedError("Plugins must implement the process method")

# filepath: /d:/Proyectos/Analizador/src/core/plugins/uasset_plugin.py
from .plugin_interface.py import PluginInterface

class UAssetPlugin(PluginInterface):
    def process(self, file_path):
        # Lógica para procesar archivos UASSET
        pass

# filepath: /d:/Proyectos/Analizador/src/core/plugins/plugin_manager.py
import importlib
import os

class PluginManager:
    def __init__(self, plugin_folder):
        self.plugin_folder = plugin_folder
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_folder):
            if filename.endswith("_plugin.py"):
                module_name = filename[:-3]
                module = importlib.import_module(f"core.plugins.{module_name}")
                for attr in dir(module):
                    cls = getattr(module, attr)
                    if isinstance(cls, type) and issubclass(cls, PluginInterface) and cls is not PluginInterface:
                        self.plugins.append(cls())

    def get_plugins(self):
        return self.plugins
```

### Consejos para Aprendizaje de PyQt5

1. **Recursos de aprendizaje**:
   - Real Python tiene excelentes tutoriales sobre PyQt
   - La documentación oficial de Qt es muy completa
   - Curso "Create Simple GUI Applications with Python and Qt" de Martin Fitzpatrick

2. **Enfoque gradual**:
   - Comienza con una ventana simple y funcional
   - Agrega componentes uno a uno
   - Integra con el core cuando la UI básica esté funcionando

3. **Herramientas útiles**:
   - **QScintilla**: Para editor de código/texto avanzado
   - **Matplotlib + PyQt**: Para visualizaciones y gráficos
   - **Qt Resource System**: Para manejar recursos (iconos, estilos)

## Herramientas Recomendadas para Mantener el Orden

1. **Gestión de Proyecto**
   - **Trello**: Para seguimiento de tareas según este roadmap
   - **GitHub Projects**: Si prefieres mantener todo en GitHub
   - **Notion**: Para documentación y seguimiento integrado

2. **Control de Versiones**
   - **Git con ramas de desarrollo**: 
     - `main`: Código estable
     - `develop`: Desarrollo activo
     - `feature/nombre-funcionalidad`: Para nuevas funcionalidades

3. **Documentación**
   - **Sphinx**: Para documentación técnica de Python
   - **MkDocs**: Para documentación de usuario y guías
   - **Docstrings**: Documentar todas las funciones y clases

4. **Calidad de Código**
   - **Black**: Formateador automático de código
   - **Flake8**: Linter para detectar errores
   - **isort**: Para organizar imports
   - **pre-commit**: Hooks para verificar calidad antes de commits

5. **Pruebas**
   - **pytest**: Framework de pruebas
   - **coverage**: Para medir cobertura de pruebas

6. **Entorno de Desarrollo**
   - **VSCode** con extensiones:
     - Python
     - MySQL
     - GitLens
     - Python Docstring Generator
     - Python Test Explorer
     - PyQt integration

7. **Seguimiento de Dependencias**
   - **pip-tools**: Para mantener dependencies.txt actualizado
   - **dependabot**: Para actualizaciones automáticas

# Roadmap Actualizado: Sistema Core con Python y MySQL

## Estado General del Proyecto
- [x] Fase 1: Preparación y Configuración ✅
- [ ] Fase 2: Módulo de Procesamiento de Archivos
- [ ] Fase 3: Integración con IA
- [ ] Fase 4: Sistema de Almacenamiento y Consulta
- [ ] Fase 5: Interfaz de Administración Desktop
- [ ] Fase 6: API y Servicios Web
- [ ] Fase 7: Operaciones Asíncronas y Optimización
- [ ] Fase 8: Extensibilidad y Plugins

## Comandos Útiles de Inicialización

1. **Preparación del Entorno**:
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar en Windows
   venv\Scripts\activate
   
   # Activar en macOS/Linux
   source venv/bin/activate
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

2. **Configuración de Base de Datos**:
   ```bash
   # Opción 1: Usar schema.sql directamente en MySQL
   mysql -u root -p core_system < ScriptDB/schema.sql

   # Opción 2: Usar script de inicialización de SQLAlchemy
   python -m src.core.database.db_setup --force

   # Opción 3: Usar script de inicialización con schema.sql
   python -m src.core.database.db_setup --use-sql --force
   ```

3. **Ejecutar Pruebas**:
   ```bash
   # Ejecutar todas las pruebas
   pytest tests/ -v

   # Ejecutar pruebas específicas de base de datos
   pytest tests/test_database.py -v

   # Ejecutar pruebas con reporte HTML
   pytest tests/ --html=report.html
   ```

4. **Mantenimiento de Base de Datos**:
   ```bash
   # Limpiar y reinicializar base de datos
   python -m src.core.database.db_setup --force

   # Verificar estado de las tablas
   python -m src.core.database.db_setup
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

## Detalle de Progreso por Fase

### Fase 1: Preparación y Configuración ✅
#### Semana 1: Configuración del Entorno ✅
- [x] Día 1-2: Preparación del entorno de desarrollo
- [x] Día 3-4: Estructura inicial del proyecto
- [x] Día 5: Configuración de variables de entorno

#### Semana 2: Diseño y Configuración de Base de Datos ✅
- [x] Día 1-2: Diseño del esquema de base de datos
- [x] Día 3-4: Configuración ORM
- [x] Día 5: Pruebas de conexión

### Fase 2: Módulo de Procesamiento de Archivos
#### Semana 3: Procesamiento Básico
- [x] Día 1-2: Procesamiento de PDFs
- [ ] Día 3-4: Procesamiento de Excel
- [ ] Día 5: Sistema de almacenamiento

#### Semana 4: Procesamiento Avanzado
- [ ] Día 1-2: Detección de tipos de documento
- [ ] Día 3-4: Preprocesamiento para IA
- [ ] Día 5: Pruebas y refinamiento

### Fase 3: Integración con IA (Actualizado)
#### Semana 5: Sistema Multi-Proveedor
1. **Día 1-2: Arquitectura Base**
   - Implementación de interfaces abstractas
   - Sistema de proveedores intercambiables
   - Configuración centralizada

2. **Día 3-4: Implementación de Proveedores**
   - Cliente OpenAI
   - Cliente DeepSeek
   - Sistema de fallback

3. **Día 5: Sistema de Cache y Optimización**
   - Cache de resultados
   - Gestión de cuotas
   - Monitoreo de uso

#### Semana 6: Optimización y Pruebas
1. **Día 1-2: Prompts y Análisis**
   - Optimización de prompts por proveedor
   - Sistema de templating para prompts
   - Análisis de respuestas estructuradas

2. **Día 3-4: Sistema de Confianza**
   - Métricas de calidad por proveedor
   - Sistema de puntuación de respuestas
   - Lógica de selección de proveedor

3. **Día 5: Pruebas y Documentación**
   - Pruebas de integración
   - Documentación de uso
   - Ejemplos de implementación

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

## Fase 9: Monitoreo y Mantenimiento (Semanas 17-18)

### Semana 17: Sistema de Monitoreo

1. **Día 1-2: Implementación de Logs**
   - Sistema centralizado de logging
   - Rotación de logs
   - Niveles de severidad
   - Alertas automáticas

2. **Día 3-4: Dashboard de Monitoreo**
   - Métricas de rendimiento
   - Uso de recursos
   - Estado de plugins
   - Estadísticas de procesamiento

3. **Día 5: Sistema de Alertas**
   - Configuración de umbrales
   - Notificaciones por email/webhook
   - Integración con sistemas externos

### Semana 18: Mantenimiento y Backup

1. **Día 1-2: Sistema de Backup**
   - Backup automático de base de datos
   - Respaldo de configuraciones
   - Versionado de plugins
   - Scripts de recuperación

2. **Día 3-4: Herramientas de Mantenimiento**
   - Limpieza de archivos temporales
   - Optimización de base de datos
   - Gestión de caché
   - Actualización de plugins

3. **Día 5: Documentación de Mantenimiento**
   - Guías de troubleshooting
   - Procedimientos de recuperación
   - Manual de operaciones
   - Plan de contingencia

## Consejos Adicionales para el Desarrollo de la Interfaz 

### Estructura de la Aplicación

```
proyecto-core/
├── src/
│   ├── desktop_app/
│   │   ├── __init__.py
│   │   ├── main.py                  # Punto de entrada
│   │   ├── resources/               # Recursos (iconos, estilos)
│   │   ├── views/                   # Interfaces
│   │   │   ├── main_window.py
│   │   │   ├── document_view.py
│   │   │   ├── analysis_view.py
│   │   │   └── settings_view.py
│   │   ├── controllers/             # Lógica de la interfaz
│   │   │   ├── document_controller.py
│   │   │   ├── analysis_controller.py
│   │   │   └── settings_controller.py
│   │   ├── models/                  # Modelos específicos para la UI
│   │   │   └── table_models.py
│   │   └── utils/                   # Utilidades para la UI
│   │       ├── qt_helpers.py
│   │       └── config_manager.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── services/                # Servicios de negocio
│   │   │   ├── document_service.py
│   │   │   ├── analysis_service.py
│   │   │   └── file_processor_service.py
│   │   ├── repositories/            # Repositorios de datos
│   │   │   ├── document_repository.py
│   │   │   ├── category_repository.py
│   │   │   └── entity_repository.py
│   │   ├── models/                  # Modelos de datos
│   │   │   ├── __init__.py
│   │   │   └── models.py
│   │   ├── processors/              # Procesadores de archivos
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── excel_processor.py
│   │   │   ├── word_processor.py
│   │   │   ├── uasset_processor.py  # Procesador para archivos UASSET
│   │   │   └── processor_factory.py
│   │   ├── config/                  # Configuración centralizada
│   │   │   └── settings.py
│   │   └── api/                     # API RESTful
│   │       ├── __init__.py
│   │       ├── main.py              # Punto de entrada de la API
│   │       ├── endpoints/           # Endpoints de la API
│   │       │   ├── document_endpoints.py
│   │       │   ├── analysis_endpoints.py
│   │       │   └── file_endpoints.py
│   │       └── schemas/             # Esquemas de datos para la API
│   │           ├── document_schema.py
│   │           ├── analysis_schema.py
│   │           └── file_schema.py
│   ├── tests/                       # Pruebas unitarias y de integración
│   │   ├── __init__.py
│   │   ├── test_services.py
│   │   ├── test_repositories.py
│   │   ├── test_processors.py
│   │   └── test_api.py
│   ├── requirements.txt                    # Dependencias del proyecto
│   ├── .env.example
│   └── README.md                           # Documentación del proyecto
├── .gitignore
├── .env.example                         # Archivo de variables de entorno
└── python-mysql-core-roadmap-updated.md # Documento de referencia
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

## Leyenda de Estado
✅ Completado
🔄 En Progreso
⏸️ En Pausa
❌ Bloqueado
⭕ Pendiente

## Notas de Progreso
- Última actualización: [Fecha]
- Sprint actual: [Número de Sprint]
- Bloqueantes actuales: [Lista de bloqueantes si existen]

# Guía de Contribución

## Configuración del Entorno de Desarrollo

1. Clonar el repositorio
```bash
git clone https://github.com/yourusername/analizador.git
cd analizador
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias de desarrollo
```bash
pip install -r requirements-dev.txt
```

## Flujo de Trabajo

1. Actualizar tu rama main
```bash
git checkout main
git pull origin main
```

2. Crear una rama para tu feature
```bash
git checkout -b feature/nombre-descriptivo
```

3. Realizar cambios siguiendo las guías de estilo

4. Ejecutar pruebas
```bash
pytest
```

5. Crear Pull Request
   - Usar el template proporcionado
   - Incluir tests
   - Actualizar documentación

## Guías de Estilo

### Python
- Usar Black para formateo
- Docstrings en formato Google
- Type hints en funciones nuevas
- Nombres descriptivos en inglés

### Commits
- Usar commits atómicos
- Mensaje descriptivo en presente
- Referenciar issues cuando aplique

## Proceso de Review

1. El PR debe pasar CI/CD
2. Requiere al menos 1 review
3. Debe mantener cobertura
4. Documentación actualizada

## Contacto

- Discord: [Enlace]
- Email: desarrollo@tudominio.com

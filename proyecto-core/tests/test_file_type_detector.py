import pytest
import os
import tempfile
from pathlib import Path

from src.core.processors.file_type_detector import FileTypeDetector

# Definir ruta de recursos de prueba
TEST_RESOURCES = Path(__file__).parent / "resources"
TEST_RESOURCES.mkdir(exist_ok=True)

@pytest.fixture
def detector():
    """Fixture que proporciona una instancia de FileTypeDetector"""
    detector = FileTypeDetector()
    # Forzar la detección por extensión en este caso
    detector.magic_available = False
    return detector

@pytest.fixture
def sample_files():
    """Fixture que crea archivos de prueba de diferentes tipos"""
    files = {}
    
    # Crear archivo PDF
    pdf_path = TEST_RESOURCES / "detector_test.pdf"
    with open(pdf_path, 'wb') as f:
        f.write(b"%PDF-1.5\n")  # Cabecera PDF mínima
        f.write(b"Test PDF content")
    files["pdf"] = str(pdf_path)
    
    # Crear archivo DOCX (simplificado, sólo para detección por extensión)
    docx_path = TEST_RESOURCES / "detector_test.docx"
    with open(docx_path, 'wb') as f:
        f.write(b"Mock DOCX content")
    files["docx"] = str(docx_path)
    
    # Crear archivo XLSX (simplificado, sólo para detección por extensión)
    xlsx_path = TEST_RESOURCES / "detector_test.xlsx"
    with open(xlsx_path, 'wb') as f:
        f.write(b"Mock XLSX content")
    files["xlsx"] = str(xlsx_path)
    
    # Crear archivo TXT
    txt_path = TEST_RESOURCES / "detector_test.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("Test text file content")
    files["txt"] = str(txt_path)
    
    # Crear archivo CSV
    csv_path = TEST_RESOURCES / "detector_test.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("col1,col2,col3\nval1,val2,val3")
    files["csv"] = str(csv_path)
    
    # Crear archivo sin extensión
    no_ext_path = TEST_RESOURCES / "detector_test_no_extension"
    with open(no_ext_path, 'w', encoding='utf-8') as f:
        f.write("File without extension")
    files["no_ext"] = str(no_ext_path)
    
    return files

def test_initialize_mime_types(detector):
    """Prueba que se inicialicen correctamente los tipos MIME"""
    # Verificar que el detector esté listo para usar
    assert hasattr(detector, "_cache")
    
    # Intentar detectar un tipo de archivo común para verificar inicialización
    mime_type, _ = detector._mimetypes.guess_type("test.pdf")
    assert mime_type == "application/pdf"
    
    mime_type, _ = detector._mimetypes.guess_type("test.docx")
    assert mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def test_detect_pdf_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo PDF"""
    mime_type = detector.detect_file_type(sample_files["pdf"])
    # Si python-magic está disponible, podría detectar "application/pdf"
    # Si no, caerá en detección por extensión
    assert mime_type == "application/pdf"

def test_detect_docx_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo DOCX"""
    # Para esta prueba, forzamos la detección por extensión
    mime_type, _ = detector._mimetypes.guess_type(sample_files["docx"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    # Ahora sí probamos el método real
    mime_type = detector.detect_file_type(sample_files["docx"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def test_detect_xlsx_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo XLSX"""
    # Para esta prueba, forzamos la detección por extensión
    mime_type, _ = detector._mimetypes.guess_type(sample_files["xlsx"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    # Ahora sí probamos el método real
    mime_type = detector.detect_file_type(sample_files["xlsx"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_detect_txt_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo TXT"""
    mime_type = detector.detect_file_type(sample_files["txt"])
    assert mime_type in ["text/plain", "application/text", "text/x-python"]  # Diferentes implementaciones pueden devolver diferentes valores

def test_detect_csv_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo CSV"""
    mime_type = detector.detect_file_type(sample_files["csv"])
    assert mime_type in ["text/csv", "text/plain", "application/csv"]  # Diferentes implementaciones pueden devolver diferentes valores

def test_detect_no_extension_file_type(detector, sample_files):
    """Prueba detectar el tipo de un archivo sin extensión"""
    mime_type = detector.detect_file_type(sample_files["no_ext"])
    # Si python-magic está disponible, intentará detectar por contenido
    # Si no, probablemente devuelva application/octet-stream
    assert mime_type is not None

def test_detect_nonexistent_file(detector):
    """Prueba detectar el tipo de un archivo que no existe"""
    with pytest.raises(FileNotFoundError):
        detector.detect_file_type("nonexistent_file.xyz")

def test_cache_functionality(detector, sample_files):
    """Prueba la funcionalidad de caché"""
    # Primer acceso, debería almacenar en caché
    pdf_mime = detector.detect_file_type(sample_files["pdf"])
    
    # Verificar que se almacenó en caché
    assert sample_files["pdf"] in detector._cache
    assert detector._cache[sample_files["pdf"]] == pdf_mime
    
    # Modificar caché para verificar que se usa en la próxima llamada
    detector._cache[sample_files["pdf"]] = "modified/mime-type"
    
    # Segunda llamada, debería recuperar de caché
    second_mime = detector.detect_file_type(sample_files["pdf"])
    assert second_mime == "modified/mime-type"

def test_clear_cache(detector, sample_files):
    """Prueba la limpieza de caché"""
    # Almacenar algo en caché
    detector.detect_file_type(sample_files["pdf"])
    detector.detect_file_type(sample_files["docx"])
    
    # Verificar que hay elementos en la caché
    assert len(detector._cache) >= 2
    
    # Limpiar caché
    detector.clear_cache()
    
    # Verificar que la caché está vacía
    assert len(detector._cache) == 0

def test_get_cache_stats(detector, sample_files):
    """Prueba obtener estadísticas de caché"""
    # Limpiar caché primero
    detector.clear_cache()
    
    # Almacenar diferentes tipos en caché
    detector.detect_file_type(sample_files["pdf"])
    detector.detect_file_type(sample_files["docx"])
    detector.detect_file_type(sample_files["txt"])
    
    # Obtener estadísticas
    stats = detector.get_cache_stats()
    
    # Verificar estadísticas
    assert stats["cache_size"] == 3
    assert isinstance(stats["mime_types"], list)
    assert len(stats["mime_types"]) >= 2  # Al menos PDF y TXT deberían ser diferentes

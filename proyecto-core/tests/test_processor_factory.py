import pytest
import os
import shutil
from pathlib import Path
import tempfile
import docx
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from src.core.processors.processor_factory import ProcessorFactory
from src.core.processors.pdf_processor import PDFProcessor
from src.core.processors.excel_processor import ExcelProcessor
from src.core.processors.word_processor import WordProcessor
from src.core.processors.text_processor import TextProcessor

# Definir ruta de recursos de prueba
TEST_RESOURCES = Path(__file__).parent / "resources"
TEST_RESOURCES.mkdir(exist_ok=True)

@pytest.fixture
def processor_factory():
    """Fixture que proporciona una instancia de ProcessorFactory"""
    factory = ProcessorFactory()
    # Deshabilitamos la detección por contenido para usar solo extensión
    factory.type_detector.magic_available = False
    return factory

@pytest.fixture
def sample_files():
    """Fixture que crea archivos de prueba de diferentes tipos"""
    files = {}
    
    # Crear PDF
    pdf_path = TEST_RESOURCES / "factory_test.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.drawString(100, 750, "Test PDF for Factory")
    c.save()
    files["pdf"] = str(pdf_path)
    
    # Crear Excel
    excel_path = TEST_RESOURCES / "factory_test.xlsx"
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df.to_excel(excel_path, index=False)
    files["excel"] = str(excel_path)
    
    # Crear Word
    docx_path = TEST_RESOURCES / "factory_test.docx"
    doc = docx.Document()
    doc.add_paragraph('Test Word Document for Factory')
    doc.save(docx_path)
    files["docx"] = str(docx_path)
    
    # Crear archivo de texto
    txt_path = TEST_RESOURCES / "factory_test.txt"
    with open(txt_path, 'w') as f:
        f.write("Test text file for Factory")
    files["txt"] = str(txt_path)
    
    # Crear archivo desconocido
    unknown_path = TEST_RESOURCES / "factory_test.unknown"
    with open(unknown_path, 'w') as f:
        f.write("Unknown file type")
    files["unknown"] = str(unknown_path)
    
    return files

def test_get_processor_for_pdf(processor_factory, sample_files):
    """Prueba obtener el procesador correcto para PDF"""
    processor = processor_factory.get_processor(sample_files["pdf"])
    assert processor is not None
    assert isinstance(processor, PDFProcessor)
    assert processor.get_mime_type() == "application/pdf"

def test_get_processor_for_excel(processor_factory, sample_files):
    """Prueba obtener el procesador correcto para Excel"""
    # Verificar el tipo primero
    mime_type = processor_factory.type_detector.detect_file_type(sample_files["excel"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    
    processor = processor_factory.get_processor(sample_files["excel"])
    assert processor is not None
    assert isinstance(processor, ExcelProcessor)
    assert processor.get_mime_type() == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_get_processor_for_word(processor_factory, sample_files):
    """Prueba obtener el procesador correcto para Word"""
    # Verificar el tipo primero
    mime_type = processor_factory.type_detector.detect_file_type(sample_files["docx"])
    assert mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    
    processor = processor_factory.get_processor(sample_files["docx"])
    assert processor is not None
    assert isinstance(processor, WordProcessor)
    assert processor.get_mime_type() == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def test_get_processor_for_text(processor_factory, sample_files):
    """Prueba obtener el procesador correcto para texto plano"""
    processor = processor_factory.get_processor(sample_files["txt"])
    assert processor is not None
    assert isinstance(processor, TextProcessor)
    assert processor.get_mime_type() == "text/plain"

def test_get_processor_for_unknown_type(processor_factory, sample_files):
    """Prueba obtener el procesador para un tipo desconocido"""
    # Modificar el detector para asegurar que devuelve un tipo desconocido
    original_detect = processor_factory.type_detector.detect_file_type
    
    def mock_detect_file_type(file_path):
        if file_path == sample_files["unknown"]:
            return "application/x-unknown"
        return original_detect(file_path)
    
    processor_factory.type_detector.detect_file_type = mock_detect_file_type
    
    processor = processor_factory.get_processor(sample_files["unknown"])
    assert processor is None

def test_get_processor_for_nonexistent_file(processor_factory):
    """Prueba obtener el procesador para un archivo que no existe"""
    processor = processor_factory.get_processor("nonexistent_file.xyz")
    assert processor is None

def test_register_custom_processor(processor_factory):
    """Prueba registrar un procesador personalizado"""
    class CustomProcessor(TextProcessor):
        def get_mime_type(self):
            return "application/custom"
    
    custom_processor = CustomProcessor()
    processor_factory.register_processor("application/custom", custom_processor)
    
    # Crear un archivo temporal para probar
    with tempfile.NamedTemporaryFile(suffix='.custom', delete=False) as temp:
        temp.write(b"Custom content")
        temp_path = temp.name
    
    try:
        # Modificar el detector de tipos para que devuelva el tipo personalizado
        def mock_detect_file_type(file_path):
            if file_path.endswith('.custom'):
                return "application/custom"
            return "application/octet-stream"
        
        original_detect = processor_factory.type_detector.detect_file_type
        processor_factory.type_detector.detect_file_type = mock_detect_file_type
        
        # Probar que se usa el procesador personalizado
        processor = processor_factory.get_processor(temp_path)
        assert processor is not None
        assert isinstance(processor, CustomProcessor)
        assert processor.get_mime_type() == "application/custom"
    
    finally:
        # Restaurar la función original y eliminar el archivo temporal
        processor_factory.type_detector.detect_file_type = original_detect
        os.unlink(temp_path)

def test_get_supported_types(processor_factory):
    """Prueba obtener los tipos MIME soportados"""
    supported_types = processor_factory.get_supported_types()
    
    # Verificar que contiene los tipos principales
    assert "application/pdf" in supported_types
    assert "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in supported_types
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in supported_types
    assert "text/plain" in supported_types
    
    # Verificar que las descripciones son correctas
    assert supported_types["application/pdf"] == "PDF Document"
    assert supported_types["application/vnd.openxmlformats-officedocument.wordprocessingml.document"] == "Microsoft Word Document"

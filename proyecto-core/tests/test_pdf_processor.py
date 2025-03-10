import pytest
from pathlib import Path
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from src.core.processors.pdf_processor import PDFProcessor
from src.core.ai.providers import AIProvider

# Definir ruta de recursos de prueba
TEST_RESOURCES = Path(__file__).parent / "resources"
TEST_RESOURCES.mkdir(exist_ok=True)

@pytest.fixture
def pdf_processor():
    return PDFProcessor()

@pytest.fixture
def sample_pdf_path():
    """Crea un PDF de prueba simple usando reportlab"""
    pdf_path = TEST_RESOURCES / "sample.pdf"
    
    # Crear un PDF básico con reportlab
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # Agregar texto de prueba
    test_text = "This is a test document for PDF processing.\n" * 5
    y_position = 750  # Empezar desde arriba
    for line in test_text.split('\n'):
        c.drawString(50, y_position, line)
        y_position -= 15  # Espacio entre líneas
    
    # Agregar metadatos usando los métodos disponibles
    c.setAuthor("Test Author")
    c.setTitle("Test Document")
    c.setSubject("Test Subject")
    c.setCreator("Test Creator")
    c.setProducer("ReportLab PDF Library")
    
    # La fecha de creación se establece automáticamente por ReportLab
    
    # Guardar el PDF
    c.save()
    
    return str(pdf_path)

@pytest.fixture
def sample_pdf_path_with_content():
    """Crea un PDF de prueba con contenido más significativo"""
    pdf_path = TEST_RESOURCES / "sample_content.pdf"
    
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # Contenido de prueba más estructurado
    test_content = """
    Informe de Análisis de Mercado
    Fecha: 15 de Febrero 2024
    
    Este informe analiza las tendencias del mercado tecnológico en 2024.
    Los principales hallazgos incluyen:
    
    1. Aumento en la demanda de soluciones de IA
    2. Crecimiento del mercado de cloud computing
    3. Nuevas regulaciones en privacidad de datos
    
    Empresas mencionadas:
    - Microsoft Corporation
    - Amazon Web Services
    - Google Cloud Platform
    
    Conclusiones:
    El mercado muestra un crecimiento sostenido con énfasis en tecnologías emergentes.
    """
    
    y_position = 750
    for line in test_content.split('\n'):
        c.drawString(50, y_position, line.strip())
        y_position -= 15
    
    c.setAuthor("Market Analyst")
    c.setTitle("Market Analysis Report 2024")
    c.setSubject("Technology Market Trends")
    c.save()
    
    return str(pdf_path)

def test_validate_with_valid_pdf(pdf_processor, sample_pdf_path):
    assert pdf_processor.validate(sample_pdf_path) is True

def test_validate_with_invalid_path(pdf_processor):
    assert pdf_processor.validate("nonexistent.pdf") is False

def test_get_mime_type(pdf_processor):
    assert pdf_processor.get_mime_type() == "application/pdf"

def test_process_valid_pdf(pdf_processor, sample_pdf_path):
    result = pdf_processor.process(sample_pdf_path)
    assert isinstance(result.content, str)
    assert isinstance(result.metadata, dict)
    assert isinstance(result.summary, str)
    assert isinstance(result.keywords, list)
    assert isinstance(result.confidence_score, float)
    assert 0 <= result.confidence_score <= 1

def test_process_invalid_pdf(pdf_processor):
    with pytest.raises(ValueError):
        pdf_processor.process("nonexistent.pdf")

def test_extract_keywords(pdf_processor):
    content = "This is a test document with some repeated words. Test document keywords."
    keywords = pdf_processor._extract_keywords(content)
    assert isinstance(keywords, list)
    assert len(keywords) <= 10
    assert all(isinstance(k, str) for k in keywords)

def test_ai_analysis_integration(pdf_processor, sample_pdf_path_with_content):
    """Prueba la integración con DeepSeek"""
    result = pdf_processor.process(sample_pdf_path_with_content)
    
    # Verificar que el análisis de IA está presente y tiene la estructura correcta
    assert "ai_analysis" in result.metadata
    ai_analysis = result.metadata["ai_analysis"]
    
    # Verificar estructura básica
    assert isinstance(ai_analysis, dict)
    
    # Verificar campos requeridos
    required_fields = ["success", "analysis_result", "confidence_score"]
    for field in required_fields:
        assert field in ai_analysis, f"Falta el campo {field} en ai_analysis"
    
    # Verificar campos del analysis_result
    analysis_result = ai_analysis["analysis_result"]
    assert isinstance(analysis_result, dict)
    assert "summary" in analysis_result
    assert "keywords" in analysis_result
    assert "entities" in analysis_result
    
    # Verificar tipos de datos
    assert isinstance(ai_analysis["success"], bool)
    assert isinstance(ai_analysis["confidence_score"], float)
    assert isinstance(analysis_result["keywords"], list)
    assert isinstance(analysis_result["entities"], list)
    assert isinstance(analysis_result["summary"], str)

def test_ai_analysis_failure_handling(pdf_processor, sample_pdf_path_with_content):
    """Prueba el manejo de fallos"""
    # Simular fallo
    original_key = pdf_processor.ai_analyzer.client.api_key
    pdf_processor.ai_analyzer.client.api_key = "invalid_key"
    
    try:
        result = pdf_processor.process(sample_pdf_path_with_content)
        
        # Verificar estructura de error
        assert "ai_analysis" in result.metadata
        ai_analysis = result.metadata["ai_analysis"]
        assert "fallback_analysis" in ai_analysis
        assert "error" in ai_analysis
        assert not ai_analysis["success"]
        assert ai_analysis["confidence_score"] == 0.3
        
        # Verificar contenido de fallback
        assert "summary" in ai_analysis["analysis_result"]
        assert "keywords" in ai_analysis["analysis_result"]
        assert "entities" in ai_analysis["analysis_result"]
    finally:
        # Restaurar API key original
        pdf_processor.ai_analyzer.client.api_key = original_key

# TODO: Agregar más pruebas para _extract_entities y _parse_date

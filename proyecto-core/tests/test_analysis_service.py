import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.services.analysis_service import AnalysisService
from src.core.processors.base_processor import ProcessedContent
from src.core.models.models import File, AnalysisResult

@pytest.fixture
def analysis_service(db: Session):
    return AnalysisService(db)

@pytest.fixture
def sample_file(db: Session):
    """Crea un archivo de prueba en la base de datos"""
    file = File(
        filename="test.pdf",
        file_path="/path/to/test.pdf",
        file_type="pdf",
        file_size=1024,
        mime_type="application/pdf",
        user_id=1
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

@pytest.fixture
def sample_processed_content():
    """Crea un ProcessedContent de prueba"""
    return ProcessedContent(
        content="Test content",
        metadata={
            "ai_analysis": {
                "success": True,
                "analysis_result": {
                    "summary": "Test summary",
                    "keywords": ["test", "sample"],
                    "entities": []
                },
                "confidence_score": 0.95
            }
        },
        summary="Test summary",
        keywords=["test", "sample"],
        created_date=datetime.now(),
        modified_date=datetime.now(),
        author="Test Author",
        title="Test Document",
        num_pages=1,
        language="en",
        entities=[],
        confidence_score=0.95
    )

def test_save_analysis(analysis_service, sample_file, sample_processed_content):
    """Prueba el guardado de un análisis"""
    result = analysis_service.save_analysis(sample_file.id, sample_processed_content)
    
    assert isinstance(result, AnalysisResult)
    assert result.file_id == sample_file.id
    assert result.analysis_type == "pdf_analysis"
    assert result.confidence == 0.95
    assert "summary" in result.result_data
    assert result.language == "en"
    assert isinstance(result.processing_time, float)

def test_get_latest_analysis(analysis_service, sample_file, sample_processed_content):
    """Prueba obtener el análisis más reciente"""
    # Crear múltiples análisis
    analysis_service.save_analysis(sample_file.id, sample_processed_content)
    second_analysis = analysis_service.save_analysis(sample_file.id, sample_processed_content)
    
    latest = analysis_service.get_latest_analysis(sample_file.id)
    assert latest.id == second_analysis.id

def test_save_analysis_invalid_file(analysis_service, sample_processed_content):
    """Prueba guardar análisis con un archivo inexistente"""
    with pytest.raises(ValueError):
        analysis_service.save_analysis(999, sample_processed_content)

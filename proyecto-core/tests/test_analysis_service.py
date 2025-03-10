import pytest
import time
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.services.analysis_service import AnalysisService
from src.core.processors.base_processor import ProcessedContent
from src.core.models.models import File, AnalysisResult, User

@pytest.fixture
def test_user(db_session: Session):
    """Crea un usuario de prueba en la base de datos"""
    # Verificar si ya existe
    user = db_session.query(User).filter(User.username == "test_user").first()
    
    if not user:
        user = User(
            username="test_user",
            email="test@example.com",
            password="test_password",  # En producción debería estar hash
            role="user",
            is_active=True,
            created_at=datetime.now()
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
    
    return user

@pytest.fixture
def analysis_service(db_session: Session):
    """Usar db_session en lugar de db para evitar conflictos con la base de datos real"""
    return AnalysisService(db_session)

@pytest.fixture
def sample_file(db_session: Session, test_user: User):
    """Crea un archivo de prueba en la base de datos de prueba"""
    file = File(
        filename="test.pdf",
        file_path="/path/to/test.pdf",
        file_type="pdf",
        file_size=1024,
        mime_type="application/pdf",
        user_id=test_user.id  # Usar el ID del usuario creado
    )
    db_session.add(file)
    db_session.commit()
    db_session.refresh(file)
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

@pytest.mark.db
@pytest.mark.analysis_service
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

@pytest.mark.db
@pytest.mark.analysis_service
def test_get_latest_analysis(analysis_service, sample_file, sample_processed_content):
    """Prueba obtener el análisis más reciente"""
    # Limpiar análisis previos para asegurar consistencia
    db_session = analysis_service.db
    db_session.query(AnalysisResult).filter(AnalysisResult.file_id == sample_file.id).delete()
    db_session.commit()
    
    # Crear primer análisis
    first_analysis = analysis_service.save_analysis(sample_file.id, sample_processed_content)
    
    # Esperar un momento para asegurar timestamps diferentes
    time.sleep(0.1)
    
    # Crear una copia profunda del metadata para modificarlo sin afectar el original
    import copy
    updated_metadata = copy.deepcopy(sample_processed_content.metadata)
    
    # Modificar el resultado del análisis dentro del metadata
    updated_metadata["ai_analysis"]["analysis_result"]["summary"] = "Test summary (updated)"
    
    # Modificar ligeramente el contenido para el segundo análisis
    second_content = ProcessedContent(
        content=sample_processed_content.content + " (updated)",
        metadata=updated_metadata,  # Usar el metadata actualizado
        summary=sample_processed_content.summary + " (updated)",
        keywords=sample_processed_content.keywords,
        created_date=datetime.now(),
        modified_date=datetime.now(),
        author=sample_processed_content.author,
        title=sample_processed_content.title,
        num_pages=sample_processed_content.num_pages,
        language=sample_processed_content.language,
        entities=sample_processed_content.entities,
        confidence_score=sample_processed_content.confidence_score
    )
    
    # Crear segundo análisis
    second_analysis = analysis_service.save_analysis(sample_file.id, second_content)
    
    # Verificar que son diferentes
    assert first_analysis.id != second_analysis.id
    
    # Obtener el análisis más reciente
    latest = analysis_service.get_latest_analysis(sample_file.id)
    
    # Verificar que es el segundo análisis
    assert latest is not None
    assert latest.id == second_analysis.id
    
    # Verificar que el contenido es el esperado (contenido modificado)
    assert "updated" in latest.result_data.get("summary", "")

@pytest.mark.db
@pytest.mark.analysis_service
def test_save_analysis_invalid_file(analysis_service, sample_processed_content):
    """Prueba guardar análisis con un archivo inexistente"""
    with pytest.raises(ValueError):
        analysis_service.save_analysis(999, sample_processed_content)

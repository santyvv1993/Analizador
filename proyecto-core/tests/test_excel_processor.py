import pytest
from pathlib import Path
import pandas as pd
from src.core.processors.excel_processor import ExcelProcessor

# Definir ruta de recursos de prueba
TEST_RESOURCES = Path(__file__).parent / "resources"
TEST_RESOURCES.mkdir(exist_ok=True)

@pytest.fixture
def excel_processor():
    return ExcelProcessor()

@pytest.fixture
def sample_excel_path():
    """Crea un Excel de prueba"""
    excel_path = TEST_RESOURCES / "sample.xlsx"
    
    # Crear datos de prueba
    df1 = pd.DataFrame({
        'Name': ['John', 'Alice', 'Bob'],
        'Age': [30, 25, 35],
        'Department': ['IT', 'HR', 'Sales']
    })
    
    df2 = pd.DataFrame({
        'Product': ['Laptop', 'Phone', 'Tablet'],
        'Price': [1000, 500, 300],
        'Stock': [50, 100, 75]
    })
    
    # Guardar en Excel con múltiples hojas
    with pd.ExcelWriter(excel_path) as writer:
        df1.to_excel(writer, sheet_name='Employees', index=False)
        df2.to_excel(writer, sheet_name='Products', index=False)
    
    return str(excel_path)

def test_validate_with_valid_excel(excel_processor, sample_excel_path):
    assert excel_processor.validate(sample_excel_path) is True

def test_validate_with_invalid_path(excel_processor):
    assert excel_processor.validate("nonexistent.xlsx") is False

def test_get_mime_type(excel_processor):
    assert excel_processor.get_mime_type() == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

def test_process_valid_excel(excel_processor, sample_excel_path):
    result = excel_processor.process(sample_excel_path)
    
    # Verificar estructura básica
    assert isinstance(result.content, str)
    assert isinstance(result.metadata, dict)
    assert isinstance(result.summary, str)
    assert isinstance(result.keywords, list)
    assert isinstance(result.confidence_score, float)
    
    # Verificar metadatos específicos de Excel
    assert "sheets" in result.metadata
    assert len(result.metadata["sheets"]) == 2
    assert result.metadata["total_rows"] > 0
    assert result.metadata["total_columns"] > 0

def test_process_invalid_excel(excel_processor):
    with pytest.raises(ValueError):
        excel_processor.process("nonexistent.xlsx")

def test_ai_analysis_integration(excel_processor, sample_excel_path):
    result = excel_processor.process(sample_excel_path)
    
    assert "ai_analysis" in result.metadata
    ai_analysis = result.metadata["ai_analysis"]
    
    assert "success" in ai_analysis
    assert "analysis_result" in ai_analysis
    assert "confidence_score" in ai_analysis

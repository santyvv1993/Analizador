"""
Pruebas para el procesador por lotes.
"""
import pytest
from unittest.mock import MagicMock, patch
from src.core.ai.batch_processor import BatchProcessor

@pytest.fixture
def batch_processor():
    return BatchProcessor(max_batch_size=1000, overlap=200, max_workers=2)

def test_split_into_batches(batch_processor):
    """Prueba la función de división en lotes"""
    # Crear un contenido de prueba
    content = "Este es un texto de prueba " * 100  # 2600 caracteres aprox.
    
    # Dividir en lotes
    batches = batch_processor._split_into_batches(content)
    
    # Verificar que se dividió correctamente
    assert len(batches) > 1
    assert len(batches[0]) <= batch_processor.max_batch_size
    
    # Verificar superposición
    first_batch_end = batches[0][-100:]
    second_batch_start = batches[1][:100]
    # Debe haber alguna superposición
    assert any(word in second_batch_start for word in first_batch_end.split())

def test_process_document_small(batch_processor):
    """Prueba procesamiento de documentos pequeños"""
    # Contenido pequeño que cabe en un solo lote
    content = "Documento de prueba pequeño"
    
    # Mock de procesador
    mock_processor = MagicMock(return_value={"result": "procesado"})
    
    # Procesar documento
    result = batch_processor.process_document(content, mock_processor)
    
    # Verificar que se procesó correctamente
    assert "processing_details" in result
    assert result["processing_details"]["batches"] == 1
    assert result["result"] == "procesado"
    
    # Verificar que el procesador se llamó solo una vez
    mock_processor.assert_called_once()

def test_process_document_large(batch_processor):
    """Prueba procesamiento de documentos grandes"""
    # Contenido grande que requiere múltiples lotes
    content = "Palabra " * 500  # Más de 4000 caracteres
    
    # Mock de procesador
    mock_processor = MagicMock(return_value={"result": "procesado", "score": 0.5})
    
    # Procesar documento
    result = batch_processor.process_document(content, mock_processor)
    
    # Verificar que se procesó correctamente
    assert "processing_details" in result
    assert result["processing_details"]["batches"] > 1
    
    # Verificar que el procesador se llamó múltiples veces
    assert mock_processor.call_count > 1

def test_cancel_processing(batch_processor):
    """Prueba la cancelación del procesamiento"""
    # Contenido grande que requiere múltiples lotes
    content = "Palabra " * 1000
    
    # Mock que simula un procesamiento lento
    def slow_processor(text, **kwargs):
        import time
        # El primer lote se procesa correctamente
        if kwargs.get("batch_metadata", {}).get("batch_idx", 0) == 0:
            return {"result": f"procesado lote 0"}
        
        # Solicitar cancelación antes del segundo lote
        batch_processor.cancel_processing()
        time.sleep(0.1)  # Pequeña espera para simular procesamiento
        return {"result": f"procesado lote adicional"}
    
    # Procesar documento con procesador lento y cancelación
    result = batch_processor.process_document(content, slow_processor)
    
    # Verificar que la operación se canceló
    assert "error" in result or result["processing_details"]["completed"] is False

def test_cluster_related_entities(batch_processor):
    """Prueba el agrupamiento de entidades relacionadas"""
    # Entidades de ejemplo
    entities = [
        {"type": "PERSON", "value": "Juan Pérez", "relevance": 0.9},
        {"type": "PERSON", "value": "María López", "relevance": 0.8},
        {"type": "ORG", "value": "Empresa ABC", "relevance": 0.95},
        {"type": "ORG", "value": "Empresa XYZ", "relevance": 0.85},
        {"type": "LOCATION", "value": "Madrid", "relevance": 0.7},
        {"type": "PERSON", "value": "Carlos Ruiz", "relevance": 0.75},
    ]
    
    # Relaciones entre entidades
    relations = [
        {"source": "Juan Pérez", "type": "works_for", "target": "Empresa ABC"},
        {"source": "María López", "type": "works_for", "target": "Empresa ABC"},
        {"source": "Carlos Ruiz", "type": "works_for", "target": "Empresa XYZ"},
        {"source": "Empresa XYZ", "type": "located_in", "target": "Madrid"},
    ]
    
    # Agrupar entidades
    clusters = batch_processor.cluster_related_entities(entities, relations)
    
    # Verificar resultado
    assert isinstance(clusters, list)
    assert len(clusters) >= 1  # Al menos un cluster
    
    # Verificar que las entidades relacionadas están en el mismo cluster
    for cluster in clusters:
        entities_in_cluster = [e["value"] for e in cluster["entities"]]
        
        # Si "Juan Pérez" está en el cluster, "Empresa ABC" también debe estarlo
        if "Juan Pérez" in entities_in_cluster:
            assert "Empresa ABC" in entities_in_cluster
            
        # Si "Carlos Ruiz" está en el cluster, "Empresa XYZ" y "Madrid" también deben estarlo
        if "Carlos Ruiz" in entities_in_cluster:
            assert "Empresa XYZ" in entities_in_cluster
            assert "Madrid" in entities_in_cluster

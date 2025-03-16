"""
Tests para el optimizador de prompts
"""
import json
import pytest
import time
from unittest.mock import patch, MagicMock

from src.core.ai.prompt_optimizer import PromptOptimizer
from src.core.ai.prompt_templates import AnalysisType

@pytest.fixture
def prompt_optimizer():
    """Fixture que proporciona un optimizador de prompts"""
    return PromptOptimizer()

def test_build_optimized_prompt(prompt_optimizer):
    """Verifica la construcción de prompts optimizados"""
    content = "Este es un contenido de prueba"
    metadata = {
        "mime_type": "application/pdf",
        "file_name": "documento.pdf",
        "file_size": 1024
    }
    
    # Probar con OpenAI
    openai_prompt = prompt_optimizer.build_optimized_prompt(
        content=content,
        metadata=metadata,
        provider="openai"
    )
    
    assert content in openai_prompt
    assert "JSON" in openai_prompt
    
    # Probar con DeepSeek
    deepseek_prompt = prompt_optimizer.build_optimized_prompt(
        content=content,
        metadata=metadata,
        provider="deepseek"
    )
    
    assert content in deepseek_prompt
    assert "JSON" in deepseek_prompt
    # Verificar que contiene texto específico de DeepSeek
    assert "Responde únicamente con un objeto JSON válido sin explicaciones adicionales" in deepseek_prompt

def test_truncate_content(prompt_optimizer):
    """Verifica la truncación de contenido según límites del proveedor"""
    long_content = "a" * 10000  # Contenido largo que debe truncarse
    
    # Probar truncado para OpenAI
    openai_truncated = prompt_optimizer._truncate_content_for_provider(long_content, "openai")
    assert len(openai_truncated) < len(long_content)
    assert "[contenido truncado]" in openai_truncated
    
    # Probar con contenido corto (no debe truncarse)
    short_content = "Contenido corto"
    not_truncated = prompt_optimizer._truncate_content_for_provider(short_content, "openai")
    assert not_truncated == short_content
    assert "[contenido truncado]" not in not_truncated

def test_evaluate_response(prompt_optimizer):
    """Verifica la evaluación de respuestas"""
    prompt = "Analiza el siguiente contenido..."
    valid_response = json.dumps({
        "summary": "Resumen de prueba",
        "keywords": ["palabra1", "palabra2", "palabra3"],
        "entities": [
            {"type": "PERSON", "value": "Juan", "relevance": 0.9},
            {"type": "ORG", "value": "Empresa", "relevance": 0.8}
        ],
        "main_topic": "Tema de prueba",
        "document_type": "Documento",
        "purpose": "Testing"
    })
    
    # Mock para el logger
    with patch('src.core.ai.prompt_optimizer.ai_logger') as mock_logger:
        # Evaluar respuesta válida
        metrics = prompt_optimizer.evaluate_response(
            prompt=prompt,
            response=valid_response,
            provider="openai",
            analysis_type=AnalysisType.FULL_ANALYSIS,
            processing_time=1.5,
            file_path="test.pdf"
        )
        
        # Verificar que se llamó al logger
        mock_logger.log_prompt_evaluation.assert_called_once()
        
        # Verificar métricas
        assert metrics["success"] is True
        assert "confidence_score" in metrics
        assert metrics["confidence_score"] > 0.5  # Debería ser buena puntuación
        
        # Verificar actualización de estadísticas internas
        assert "openai" in prompt_optimizer.success_rates
        assert AnalysisType.FULL_ANALYSIS.value in prompt_optimizer.success_rates["openai"]
        assert prompt_optimizer.success_rates["openai"][AnalysisType.FULL_ANALYSIS.value]["success"] == 1

def test_evaluate_invalid_response(prompt_optimizer):
    """Verifica la evaluación de respuestas inválidas"""
    prompt = "Analiza el siguiente contenido..."
    # Respuesta incompleta (falta entities)
    invalid_response = json.dumps({
        "summary": "Resumen de prueba",
        "keywords": ["palabra1", "palabra2"],
        # Falta "entities"
        "main_topic": "Tema principal",
        "document_type": "Documento",
        "purpose": "Informativo"
    })
    
    # Mock para el logger
    with patch('src.core.ai.prompt_optimizer.ai_logger') as mock_logger:
        # Evaluar respuesta inválida
        metrics = prompt_optimizer.evaluate_response(
            prompt=prompt,
            response=invalid_response,
            provider="openai",
            analysis_type=AnalysisType.FULL_ANALYSIS,
            processing_time=1.2,
            file_path="test.pdf"
        )
        
        # Verificar métricas
        assert metrics["success"] is False
        assert metrics["completeness"] < 1.0
        
        # Verificar actualización de estadísticas internas
        assert prompt_optimizer.success_rates["openai"][AnalysisType.FULL_ANALYSIS.value]["success"] == 0
        assert prompt_optimizer.success_rates["openai"][AnalysisType.FULL_ANALYSIS.value]["total"] == 1

def test_evaluate_non_json_response(prompt_optimizer):
    """Verifica la evaluación de respuestas que no son JSON"""
    prompt = "Analiza el siguiente contenido..."
    invalid_response = "Esta respuesta no es un JSON válido"
    
    # Mock para el logger
    with patch('src.core.ai.prompt_optimizer.ai_logger') as mock_logger:
        # Evaluar respuesta no-JSON
        metrics = prompt_optimizer.evaluate_response(
            prompt=prompt,
            response=invalid_response,
            provider="deepseek",
            analysis_type=AnalysisType.FULL_ANALYSIS,
            processing_time=0.8,
            file_path="test.pdf"
        )
        
        # Verificar métricas
        assert metrics["success"] is False
        assert metrics["confidence_score"] == 0.0
        assert "error" in metrics
        assert "JSON inválido" in metrics["error"]

def test_get_provider_success_rates(prompt_optimizer):
    """Verifica la obtención de tasas de éxito por proveedor"""
    # Preparar datos de prueba
    prompt_optimizer.success_rates = {
        "openai": {
            "full_analysis": {"success": 8, "total": 10},
            "document_summary": {"success": 5, "total": 5}
        },
        "deepseek": {
            "full_analysis": {"success": 7, "total": 10}
        }
    }
    
    # Obtener tasas
    rates = prompt_optimizer.get_provider_success_rates()
    
    # Verificar resultados
    assert rates["openai"]["full_analysis"]["success_rate"] == 0.8
    assert rates["openai"]["document_summary"]["success_rate"] == 1.0
    assert rates["deepseek"]["full_analysis"]["success_rate"] == 0.7

def test_get_best_provider(prompt_optimizer):
    """Verifica la selección del mejor proveedor según estadísticas"""
    # Preparar datos de prueba
    prompt_optimizer.success_rates = {
        "openai": {
            "full_analysis": {"success": 8, "total": 10}
        },
        "deepseek": {
            "full_analysis": {"success": 9, "total": 10}
        }
    }
    
    # Verificar que se elija el mejor proveedor
    best_provider = prompt_optimizer.get_best_provider_for_analysis(AnalysisType.FULL_ANALYSIS)
    assert best_provider == "deepseek"  # Deepseek tiene mejor tasa

def test_get_best_provider_insufficient_data(prompt_optimizer):
    """Verifica comportamiento cuando no hay suficientes datos"""
    # Preparar datos con insuficientes muestras
    prompt_optimizer.success_rates = {
        "openai": {
            "full_analysis": {"success": 2, "total": 4}  # Menos de 5 muestras
        },
        "deepseek": {
            "full_analysis": {"success": 3, "total": 3}  # Menos de 5 muestras
        }
    }
    
    # Debería devolver el proveedor por defecto
    best_provider = prompt_optimizer.get_best_provider_for_analysis(AnalysisType.FULL_ANALYSIS)
    assert best_provider == "deepseek"  # Proveedor por defecto

def test_multiple_analysis_types(prompt_optimizer):
    """Verifica el manejo de múltiples tipos de análisis"""
    # Mock para el logger
    with patch('src.core.ai.prompt_optimizer.ai_logger') as mock_logger:
        # Evaluar respuestas para diferentes tipos de análisis
        prompt_optimizer.evaluate_response(
            prompt="Resumen...",
            response=json.dumps({"summary": "Un resumen"}),
            provider="openai",
            analysis_type=AnalysisType.DOCUMENT_SUMMARY,
            processing_time=0.5
        )
        
        prompt_optimizer.evaluate_response(
            prompt="Extracción de entidades...",
            response=json.dumps({"entities": [{"type": "PERSON", "value": "Juan"}]}),
            provider="deepseek",
            analysis_type=AnalysisType.ENTITY_EXTRACTION,
            processing_time=0.7
        )
        
        # Verificar que se hayan registrado diferentes tipos
        assert AnalysisType.DOCUMENT_SUMMARY.value in prompt_optimizer.success_rates["openai"]
        assert AnalysisType.ENTITY_EXTRACTION.value in prompt_optimizer.success_rates["deepseek"]

def test_integration_with_real_content():
    """Prueba de integración con contenido real"""
    optimizer = PromptOptimizer()
    
    # Contenido de muestra
    content = """
    Informe Anual de Resultados 2023
    
    Empresa: Tecnología Innovadora S.A.
    
    Resumen Ejecutivo:
    Durante el año fiscal 2023, Tecnología Innovadora S.A. alcanzó un crecimiento significativo 
    en todas sus áreas de negocio, con un incremento del 27% en ingresos respecto al año anterior.
    El departamento de Inteligencia Artificial mostró el mayor crecimiento (42%), seguido por
    el área de Desarrollo de Software (31%).
    
    Principales logros:
    - Lanzamiento de 3 nuevos productos en el mercado
    - Expansión a 5 nuevos países
    - Contratación de 120 nuevos empleados
    - Adquisición de la startup DataMiners por 15 millones de euros
    
    El Director General, Juan García, destacó la importancia de la innovación continua
    como factor clave del éxito de la compañía durante la reunión anual celebrada
    el 15 de diciembre de 2023 en Madrid.
    
    Para el año 2024, la empresa planea invertir 25 millones de euros en investigación y desarrollo,
    centrándose en tecnologías emergentes como computación cuántica y blockchain.
    """
    
    file_name = "informe_anual_2023.txt"
    metadata = {
        "mime_type": "text/plain",
        "file_name": file_name, 
        "file_size": len(content)
    }
    
    # Generar prompt para cada proveedor
    openai_prompt = optimizer.build_optimized_prompt(
        content=content,
        metadata=metadata,
        provider="openai",
        analysis_type=AnalysisType.FULL_ANALYSIS
    )
    
    deepseek_prompt = optimizer.build_optimized_prompt(
        content=content,
        metadata=metadata,
        provider="deepseek",
        analysis_type=AnalysisType.FULL_ANALYSIS
    )
    
    # Verificar diferencias entre prompts
    assert openai_prompt != deepseek_prompt
    assert content in openai_prompt
    assert content in deepseek_prompt
    
    # Verificar que los prompts incluyen los metadatos relevantes
    assert file_name in openai_prompt, "El nombre del archivo debe estar en el prompt de OpenAI"
    assert file_name in deepseek_prompt, "El nombre del archivo debe estar en el prompt de DeepSeek"
    
    # Verificar que se incluye información sobre el tipo de archivo
    assert "text/plain" in openai_prompt or "text/plain" in deepseek_prompt
    
    # Verificar que cada prompt contiene texto específico de su proveedor
    assert "Genera una respuesta en JSON" in openai_prompt
    assert "Responde únicamente con un objeto JSON válido sin explicaciones adicionales" in deepseek_prompt

if __name__ == "__main__":
    pytest.main()

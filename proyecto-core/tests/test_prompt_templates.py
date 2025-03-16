"""
Tests para el módulo de templates de prompts
"""
import pytest
import json
from src.core.ai.prompt_templates import (
    PromptTemplate, 
    AnalysisType, 
    get_prompt_for_analysis,
    validate_response
)

def test_prompt_template_format():
    """Verifica la formatación básica de templates"""
    template = PromptTemplate(
        template="Hola {nombre}, bienvenido a {lugar}.",
        required_variables=["nombre", "lugar"]
    )
    
    result = template.format(nombre="Juan", lugar="Madrid")
    assert result == "Hola Juan, bienvenido a Madrid."

def test_prompt_template_missing_variables():
    """Verifica que se lancen errores con variables faltantes"""
    template = PromptTemplate(
        template="Hola {nombre}, bienvenido a {lugar}.",
        required_variables=["nombre", "lugar"]
    )
    
    with pytest.raises(ValueError) as excinfo:
        template.format(nombre="Juan")
    
    assert "Faltan variables requeridas" in str(excinfo.value)
    assert "lugar" in str(excinfo.value)

def test_provider_specific_adjustments():
    """Verifica ajustes específicos por proveedor"""
    template = PromptTemplate(
        template="Template estándar {variable}",
        provider_specific_adjustments={
            "openai": {
                "template": "Template para OpenAI {variable}"
            },
            "deepseek": {
                "defaults": {"variable": "valor_predeterminado"}
            }
        }
    )
    
    # Probar con OpenAI (template diferente)
    openai_result = template.adjust_for_provider("openai", variable="test")
    assert openai_result == "Template para OpenAI test"
    
    # Probar con DeepSeek (valor predeterminado)
    deepseek_result = template.adjust_for_provider("deepseek")
    assert deepseek_result == "Template estándar valor_predeterminado"
    
    # Probar con DeepSeek pero sobrescribiendo el valor predeterminado
    deepseek_custom = template.adjust_for_provider("deepseek", variable="personalizado")
    assert deepseek_custom == "Template estándar personalizado"
    
    # Probar con un proveedor sin ajustes específicos
    default_result = template.adjust_for_provider("otro_proveedor", variable="test")
    assert default_result == "Template estándar test"

def test_get_prompt_for_analysis():
    """Verifica la obtención de prompts por tipo de análisis"""
    # Probar análisis completo
    full_analysis_prompt = get_prompt_for_analysis(
        AnalysisType.FULL_ANALYSIS,
        "openai",
        content="Este es un texto de prueba",
        document_info="Archivo: documento_prueba.txt (text/plain, 25 bytes)\n\n"
    )
    
    assert "Este es un texto de prueba" in full_analysis_prompt
    assert "JSON" in full_analysis_prompt
    
    # Verificar que se usa el template específico para OpenAI
    assert "Genera una respuesta en JSON" in full_analysis_prompt
    
    # Probar con un tipo diferente
    summary_prompt = get_prompt_for_analysis(
        AnalysisType.DOCUMENT_SUMMARY,
        "openai",
        content="Contenido a resumir",
        document_info="Archivo: resumen.txt (text/plain, 19 bytes)\n\n"
    )
    
    assert "Contenido a resumir" in summary_prompt
    assert "3 párrafos" in summary_prompt  # Default para OpenAI es 3 párrafos
    
    # Probar con DeepSeek el mismo tipo
    deepseek_summary = get_prompt_for_analysis(
        AnalysisType.DOCUMENT_SUMMARY,
        "deepseek",
        content="Contenido a resumir",
        document_info="Archivo: resumen.txt (text/plain, 19 bytes)\n\n"
    )
    
    assert "Contenido a resumir" in deepseek_summary
    assert "2 párrafos" in deepseek_summary  # Default para DeepSeek es 2 párrafos

def test_validate_response():
    """Verifica la validación de respuestas"""
    # Respuesta válida para análisis completo
    valid_response = json.dumps({
        "summary": "Este es un resumen",
        "keywords": ["palabra1", "palabra2"],
        "entities": [{"type": "PERSON", "value": "Juan", "relevance": 0.9}],
        "main_topic": "Tema principal",
        "document_type": "Artículo",
        "purpose": "Informativo"
    })
    
    assert validate_response(valid_response, AnalysisType.FULL_ANALYSIS) is True
    
    # Respuesta inválida (falta un campo requerido)
    invalid_response = json.dumps({
        "summary": "Este es un resumen",
        "keywords": ["palabra1", "palabra2"],
        # Falta "entities"
        "main_topic": "Tema principal",
        "document_type": "Artículo",
        "purpose": "Informativo"
    })
    
    assert validate_response(invalid_response, AnalysisType.FULL_ANALYSIS) is False
    
    # Respuesta que no es JSON válido
    not_json = "Esto no es JSON"
    assert validate_response(not_json, AnalysisType.FULL_ANALYSIS) is False

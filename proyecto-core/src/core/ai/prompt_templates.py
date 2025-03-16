"""
Módulo para gestionar y optimizar los prompts utilizados con diferentes proveedores de IA.
Proporciona templates optimizados por proveedor y tipo de análisis.
"""

from enum import Enum
from typing import Dict, Any, Optional, List
import json

class AnalysisType(Enum):
    """Tipos de análisis que puede realizar el sistema"""
    DOCUMENT_SUMMARY = "document_summary"
    ENTITY_EXTRACTION = "entity_extraction"
    CLASSIFICATION = "classification"
    KEYWORD_EXTRACTION = "keyword_extraction"
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    FULL_ANALYSIS = "full_analysis"
    CONTEXTUAL_ANALYSIS = "contextual_analysis"  # Nuevo tipo de análisis


class PromptTemplate:
    """
    Clase que encapsula un template de prompt con capacidad
    de personalización según proveedor y tipo de análisis.
    """
    
    def __init__(
        self, 
        template: str, 
        required_variables: List[str] = None,
        provider_specific_adjustments: Dict[str, Dict] = None,
        max_tokens: int = 4000
    ):
        self.template = template
        self.required_variables = required_variables or []
        self.provider_specific_adjustments = provider_specific_adjustments or {}
        self.max_tokens = max_tokens
    
    def format(self, **kwargs) -> str:
        """
        Formatea el template con las variables proporcionadas.
        
        Args:
            **kwargs: Variables para insertar en el template
            
        Returns:
            str: Prompt formateado
            
        Raises:
            ValueError: Si falta alguna variable requerida
        """
        # Verificar que todas las variables requeridas están presentes
        missing_vars = [var for var in self.required_variables if var not in kwargs]
        if missing_vars:
            raise ValueError(f"Faltan variables requeridas: {', '.join(missing_vars)}")
            
        # Formatear el template
        return self.template.format(**kwargs)
    
    def adjust_for_provider(self, provider: str, **kwargs) -> str:
        """
        Adapta el prompt para un proveedor específico y lo formatea.
        
        Args:
            provider: Nombre del proveedor (ej: "openai", "deepseek")
            **kwargs: Variables para el template
            
        Returns:
            str: Prompt optimizado para el proveedor específico
        """
        # Obtener ajustes específicos para el proveedor o usar valores por defecto
        adjustments = self.provider_specific_adjustments.get(provider, {})
        
        # Aplicar ajustes al template
        template = adjustments.get("template", self.template)
        
        # Fusionar kwargs con valores predeterminados del proveedor
        provider_defaults = adjustments.get("defaults", {})
        merged_kwargs = {**provider_defaults, **kwargs}
        
        # Formatear con los valores ajustados
        return template.format(**merged_kwargs)


# Templates optimizados por tipo de análisis
TEMPLATES = {
    AnalysisType.FULL_ANALYSIS: PromptTemplate(
        template="""Analiza el siguiente contenido y proporciona un análisis completo con el siguiente formato JSON:

{document_info}{content}

El análisis debe incluir:
1. Un resumen conciso (máximo 3 párrafos)
2. Palabras clave principales (5-10)
3. Entidades detectadas (personas, organizaciones, lugares, fechas)
4. Tema principal del documento
5. Tipo de documento
6. Propósito aparente del documento
        
Responde únicamente con un objeto JSON válido con la siguiente estructura:
{{
    "summary": "resumen del documento",
    "keywords": ["palabra1", "palabra2", ...],
    "entities": [
        {{"type": "PERSON", "value": "nombre", "relevance": 0.95}},
        {{"type": "ORG", "value": "organización", "relevance": 0.87}},
        ...
    ],
    "main_topic": "tema principal",
    "document_type": "tipo de documento",
    "purpose": "propósito del documento"
}}""",
        required_variables=["content"],
        provider_specific_adjustments={
            "deepseek": {
                "template": """Analiza el siguiente contenido y proporciona un análisis completo con el siguiente formato JSON:

{document_info}{content}

El análisis debe incluir:
1. Un resumen conciso (máximo 3 párrafos)
2. Palabras clave principales (5-10)
3. Entidades detectadas (personas, organizaciones, lugares, fechas)
4. Tema principal del documento
5. Tipo de documento
6. Propósito aparente del documento
        
Responde únicamente con un objeto JSON válido sin explicaciones adicionales usando la siguiente estructura exacta:
{{
    "summary": "resumen del documento",
    "keywords": ["palabra1", "palabra2", ...],
    "entities": [
        {{"type": "PERSON", "value": "nombre", "relevance": 0.95}},
        {{"type": "ORG", "value": "organización", "relevance": 0.87}},
        ...
    ],
    "main_topic": "tema principal",
    "document_type": "tipo de documento",
    "purpose": "propósito del documento"
}}"""
            },
            "openai": {
                "template": """Analiza el siguiente documento y extrae información estructurada:

{document_info}{content}

Genera una respuesta en JSON con la siguiente estructura exacta:
{{
    "summary": "resumen conciso del documento (máximo 3 párrafos)",
    "keywords": ["array de 5-10 palabras clave relevantes"],
    "entities": [
        {{"type": "PERSON/ORG/LOCATION/DATE/OTHER", "value": "texto de la entidad", "relevance": "número entre 0 y 1"}}
    ],
    "main_topic": "tema principal en 2-4 palabras",
    "document_type": "tipo de documento",
    "purpose": "propósito o intención del documento"
}}"""
            }
        }
    ),
    
    AnalysisType.DOCUMENT_SUMMARY: PromptTemplate(
        template="""Resume el siguiente contenido en {max_paragraphs} párrafos:

{document_info}{content}

El resumen debe capturar los puntos principales y mantener la esencia del documento original.""",
        required_variables=["content"],
        provider_specific_adjustments={
            "deepseek": {
                "defaults": {"max_paragraphs": 2}
            },
            "openai": {
                "defaults": {"max_paragraphs": 3}
            }
        }
    ),
    
    AnalysisType.ENTITY_EXTRACTION: PromptTemplate(
        template="""Analiza el siguiente contenido y extrae las relaciones entre las entidades identificadas:

{document_info}{content}

Identifica las relaciones semánticas entre las entidades mencionadas, como "trabaja para", "es parte de", "ubicado en", etc.

Responde únicamente con un objeto JSON con la siguiente estructura:
{{
    "relations": [
        {{
            "source": "entidad origen",
            "type": "tipo de relación",
            "target": "entidad destino",
            "confidence": valor entre 0 y 1
        }},
        ...
    ]
}}""",
        required_variables=["content"],
        provider_specific_adjustments={
            "deepseek": {
                "template": """Analiza el siguiente contenido y extrae las relaciones entre las entidades identificadas:

{document_info}{content}

Identifica las relaciones semánticas entre las entidades mencionadas.
Ejemplos de relaciones: "trabaja para", "es parte de", "ubicado en", "creado por", "asociado con", etc.

Responde únicamente con un objeto JSON válido sin explicaciones adicionales usando la siguiente estructura exacta:
{{
    "relations": [
        {{
            "source": "entidad origen",
            "type": "tipo de relación",
            "target": "entidad destino",
            "confidence": valor entre 0 y 1
        }},
        ...
    ]
}}"""
            },
            "openai": {
                "template": """Analiza el siguiente contenido y extrae las relaciones entre entidades:

{document_info}{content}

Identifica las relaciones semánticas presentes entre las entidades mencionadas en el texto.
Considera relaciones como "trabaja para", "es parte de", "ubicado en", "asociado con", etc.

Genera una respuesta en JSON con la siguiente estructura exacta:
{{
    "relations": [
        {{
            "source": "entidad origen",
            "type": "tipo de relación (verbo o frase descriptiva)",
            "target": "entidad destino",
            "confidence": "número entre 0 y 1 que indica la certeza"
        }}
    ]
}}"""
            }
        }
    ),
    
    AnalysisType.CLASSIFICATION: PromptTemplate(
        template="""Analiza el siguiente contenido y clasifica la intención o propósito principal del documento:

{document_info}{content}

Determina la intención principal del documento (informativo, persuasivo, instructivo, etc.),
posibles intenciones secundarias, audiencia objetivo y si existe algún llamado a la acción.

Responde únicamente con un objeto JSON con la siguiente estructura:
{{
    "intent": {{
        "primary": "intención principal",
        "confidence": valor entre 0 y 1,
        "secondary": [
            {{"type": "intención secundaria 1", "confidence": valor}},
            {{"type": "intención secundaria 2", "confidence": valor}}
        ]
    }},
    "target_audience": "audiencia objetivo",
    "call_to_action": "llamado a la acción si existe, o null"
}}""",
        required_variables=["content"],
        provider_specific_adjustments={
            "deepseek": {
                "template": """Analiza el siguiente contenido y clasifica la intención o propósito principal del documento:

{document_info}{content}

Determina:
1. La intención principal del documento (informativo, persuasivo, instructivo, etc.)
2. Posibles intenciones secundarias
3. Audiencia objetivo
4. Si existe algún llamado a la acción

Responde únicamente con un objeto JSON válido sin explicaciones adicionales usando la siguiente estructura exacta:
{{
    "intent": {{
        "primary": "intención principal",
        "confidence": valor entre 0 y 1,
        "secondary": [
            {{"type": "intención secundaria 1", "confidence": valor}},
            {{"type": "intención secundaria 2", "confidence": valor}}
        ]
    }},
    "target_audience": "audiencia objetivo",
    "call_to_action": "llamado a la acción si existe, o null"
}}"""
            }
        }
    ),
    
    AnalysisType.CONTEXTUAL_ANALYSIS: PromptTemplate(
        template="""Analiza el siguiente contenido y extrae los contextos semánticos principales:

{document_info}{content}

Identifica los temas, conceptos y entidades principales en el documento y proporciona información 
contextual relevante para cada uno, incluyendo cómo se relacionan con el tema general.

Responde únicamente con un objeto JSON con la siguiente estructura:
{{
    "contexts": [
        {{
            "entity": "nombre de la entidad o concepto",
            "type": "TEMA/CONCEPTO/TECNOLOGIA/PROCESO/ORGANIZACION",
            "description": "descripción contextual detallada",
            "references": ["referencia 1 en el documento", "referencia 2 en el documento"],
            "importance": valor entre 0 y 1
        }},
        ...
    ]
}}""",
        required_variables=["content"],
        provider_specific_adjustments={
            "deepseek": {
                "template": """Analiza el siguiente contenido y extrae los contextos semánticos principales:

{document_info}{content}

Identifica los temas, conceptos y entidades principales en el documento y proporciona información 
contextual relevante para cada uno, incluyendo cómo se relacionan con el tema general.

Responde únicamente con un objeto JSON válido sin explicaciones adicionales usando la siguiente estructura exacta:
{{
    "contexts": [
        {{
            "entity": "nombre de la entidad o concepto",
            "type": "TEMA/CONCEPTO/TECNOLOGIA/PROCESO/ORGANIZACION",
            "description": "descripción contextual detallada",
            "references": ["referencia 1 en el documento", "referencia 2 en el documento"],
            "importance": valor entre 0 y 1
        }},
        ...
    ]
}}"""
            }
        }
    ),
    
    # Otros templates pueden agregarse aquí
}


def get_prompt_for_analysis(
    analysis_type: AnalysisType,
    provider: str,
    **kwargs
) -> str:
    """
    Obtiene un prompt optimizado para un tipo específico de análisis y proveedor.
    
    Args:
        analysis_type: Tipo de análisis a realizar
        provider: Proveedor de IA a utilizar
        **kwargs: Variables para el template
        
    Returns:
        str: Prompt optimizado
        
    Raises:
        ValueError: Si el tipo de análisis no está soportado
    """
    if analysis_type not in TEMPLATES:
        raise ValueError(f"Tipo de análisis no soportado: {analysis_type}")
    
    template = TEMPLATES[analysis_type]
    return template.adjust_for_provider(provider, **kwargs)


def validate_response(response: str, analysis_type: AnalysisType) -> bool:
    """
    Valida que la respuesta del modelo cumpla con el formato esperado.
    
    Args:
        response: Respuesta del modelo
        analysis_type: Tipo de análisis que se realizó
        
    Returns:
        bool: True si la respuesta es válida, False en caso contrario
    """
    try:
        # Intentar parsear como JSON
        parsed = json.loads(response)
        
        # Validar estructura según el tipo de análisis
        if analysis_type == AnalysisType.FULL_ANALYSIS:
            required_fields = ["summary", "keywords", "entities", "main_topic", "document_type", "purpose"]
            return all(field in parsed for field in required_fields)
            
        elif analysis_type == AnalysisType.CONTEXTUAL_ANALYSIS:
            if "contexts" not in parsed:
                return False
            if not isinstance(parsed["contexts"], list) or len(parsed["contexts"]) == 0:
                return False
            # Verificar al menos el primer elemento
            if len(parsed["contexts"]) > 0:
                first_ctx = parsed["contexts"][0]
                required_ctx_fields = ["entity", "type", "description"]
                return all(field in first_ctx for field in required_ctx_fields)
        
        # Agregar validaciones para otros tipos de análisis
            
        return True
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

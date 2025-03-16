"""
Configuraciones para el sistema de inteligencia artificial.
Incluye ajustes para proveedores, optimización de memoria y procesamiento.
"""
from typing import Dict, Any
import os
from enum import Enum

# Niveles de uso de memoria
class MemoryUsageLevel(Enum):
    LOW = "low"          # Para equipos con recursos limitados
    MEDIUM = "medium"    # Configuración balanceada (por defecto)
    HIGH = "high"        # Para equipos con muchos recursos

# Configuraciones por proveedor de IA
PROVIDER_SETTINGS = {
    "deepseek": {
        "base_url": os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
        "api_key_env": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
        "max_tokens_input": 8000,
        "max_tokens_output": 2000,
        "temperature": 0.3,
        "timeout": 60,  # segundos
        "retry_attempts": 3,
        "retry_delay": 2,  # segundos
        "batch_size": 5500  # caracteres por batch para este proveedor
    },
    # OpenAI está comentado ya que no se está utilizando actualmente
    # "openai": {
    #     "api_key_env": "OPENAI_API_KEY",
    #     "model": "gpt-4",
    #     "max_tokens_input": 6000,
    #     "max_tokens_output": 1000,
    #     "temperature": 0.3,
    #     "timeout": 45,  # segundos
    #     "retry_attempts": 3,
    #     "retry_delay": 1,  # segundos
    #     "batch_size": 4000  # caracteres por batch para este proveedor
    # }
}

# Configuraciones para procesamiento por lotes
BATCH_PROCESSING = {
    MemoryUsageLevel.LOW.value: {
        "max_workers": 2,
        "max_batch_size": 3500,
        "batch_overlap": 350,
        "max_retries": 2,
        "max_queue_size": 10,
        "concurrent_batches": 2
    },
    MemoryUsageLevel.MEDIUM.value: {
        "max_workers": 4,
        "max_batch_size": 5000,
        "batch_overlap": 500,
        "max_retries": 3,
        "max_queue_size": 20,
        "concurrent_batches": 4
    },
    MemoryUsageLevel.HIGH.value: {
        "max_workers": 8,
        "max_batch_size": 7000,
        "batch_overlap": 700,
        "max_retries": 4,
        "max_queue_size": 50,
        "concurrent_batches": 8
    }
}

# Configuraciones para análisis semántico
SEMANTIC_ANALYSIS = {
    "context_window_size": 2000,  # Tamaño máximo para análisis de contexto
    "max_entities_per_batch": 15,  # Número máximo de entidades por lote
    "relation_threshold": 0.6,     # Umbral para incluir relaciones
    "confidence_threshold": 0.7,   # Umbral de confianza para clasificaciones
    "cache_duration": 3600,        # Duración de caché (1 hora)
    "max_summary_length": 1000     # Longitud máxima de resúmenes generados
}

# Configuración de proveedores para fallback
PROVIDER_PRIORITY = ["deepseek"]  # Actualmente solo usando DeepSeek

def get_memory_settings(level: str = None) -> Dict[str, Any]:
    """
    Obtiene la configuración según el nivel de uso de memoria.
    
    Args:
        level: Nivel de uso de memoria (low, medium, high)
        
    Returns:
        Dict[str, Any]: Configuración para el nivel especificado
    """
    # Usar valor de entorno o valor por defecto
    if not level:
        level = os.environ.get("AI_MEMORY_USAGE", MemoryUsageLevel.MEDIUM.value)
    
    # Validar que el nivel sea válido
    if level not in [e.value for e in MemoryUsageLevel]:
        level = MemoryUsageLevel.MEDIUM.value
        
    return BATCH_PROCESSING[level]

def get_provider_settings(provider: str) -> Dict[str, Any]:
    """
    Obtiene la configuración para un proveedor específico.
    
    Args:
        provider: Nombre del proveedor (deepseek, openai, etc.)
        
    Returns:
        Dict[str, Any]: Configuración del proveedor
    """
    if provider not in PROVIDER_SETTINGS:
        raise ValueError(f"Proveedor no configurado: {provider}")
        
    settings = PROVIDER_SETTINGS[provider].copy()
    
    # Añadir API key desde variables de entorno
    api_key_env = settings.pop("api_key_env", None)
    if api_key_env:
        settings["api_key"] = os.environ.get(api_key_env, "")
        
    return settings

def get_semantic_settings() -> Dict[str, Any]:
    """
    Obtiene las configuraciones para análisis semántico.
    
    Returns:
        Dict[str, Any]: Configuración de análisis semántico
    """
    # Se podría mejorar para leer valores de entorno o archivo de configuración
    return SEMANTIC_ANALYSIS

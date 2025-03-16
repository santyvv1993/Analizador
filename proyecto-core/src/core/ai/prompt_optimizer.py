"""
Sistema de optimización de prompts para mejorar resultados de análisis con IA.
"""

import json
from typing import Dict, Any, List, Tuple
import logging
from datetime import datetime

from .prompt_templates import AnalysisType, get_prompt_for_analysis, validate_response
from .providers import AIProvider
from ..utils.ai_logger import AILogger

logger = logging.getLogger(__name__)
ai_logger = AILogger()

class PromptOptimizer:
    """
    Clase para optimizar y evaluar prompts usados con proveedores de IA.
    Implementa estrategias de mejora continua y adaptabilidad.
    """
    
    def __init__(self):
        self.success_rates = {
            AIProvider.OPENAI.value: {},
            AIProvider.DEEPSEEK.value: {}
        }
        self.response_metrics = {}
        
    def build_optimized_prompt(
        self, 
        content: str, 
        metadata: Dict[str, Any], 
        provider: str,
        analysis_type: AnalysisType = AnalysisType.FULL_ANALYSIS
    ) -> str:
        """
        Construye un prompt optimizado para el proveedor específico.
        
        Args:
            content: Contenido del documento a analizar
            metadata: Metadatos del documento que podrían mejorar el análisis
            provider: Proveedor de IA a utilizar
            analysis_type: Tipo de análisis a realizar
            
        Returns:
            str: Prompt optimizado
        """
        # Extraer metadatos relevantes para el prompt
        document_type = metadata.get("mime_type", "desconocido")
        file_name = metadata.get("file_name", "documento")
        file_size = metadata.get("file_size", 0)
        
        # Crear un contexto para el prompt que incluye los metadatos
        context = f"Archivo: {file_name} ({document_type}, {file_size} bytes)\n\n"
        
        # Truncar contenido si es necesario (según el proveedor)
        content = self._truncate_content_for_provider(content, provider)
        
        # Obtener el prompt optimizado desde las plantillas
        prompt_kwargs = {
            "content": content,
            "document_info": context,
            "document_type": document_type,
            "file_name": file_name,
            "file_size": file_size
        }
        
        return get_prompt_for_analysis(analysis_type, provider, **prompt_kwargs)
        
    def evaluate_response(
        self,
        prompt: str,
        response: str,
        provider: str,
        analysis_type: AnalysisType,
        processing_time: float,
        file_path: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Evalúa la calidad de la respuesta y registra métricas.
        
        Args:
            prompt: Prompt utilizado
            response: Respuesta del modelo
            provider: Proveedor utilizado
            analysis_type: Tipo de análisis realizado
            processing_time: Tiempo de procesamiento en segundos
            file_path: Ruta del archivo analizado
            
        Returns:
            Dict[str, Any]: Métricas de evaluación
        """
        # Validar formato de la respuesta
        is_valid = validate_response(response, analysis_type)
        
        # Calcular métricas de calidad
        metrics = self._calculate_quality_metrics(response, analysis_type)
        metrics["success"] = is_valid
        metrics["processing_time"] = processing_time
        metrics["timestamp"] = datetime.now().isoformat()
        metrics["provider"] = provider
        metrics["analysis_type"] = analysis_type.value
        
        # Actualizar estadísticas internas
        self._update_success_rates(provider, analysis_type, is_valid)
        
        # Registrar con el logger
        ai_logger.log_prompt_evaluation(
            file_path=file_path,
            prompt=prompt,
            response=response,
            metrics=metrics,
            provider=provider
        )
        
        logger.info(
            f"Evaluación de prompt - Proveedor: {provider} - "
            f"Tipo: {analysis_type.value} - "
            f"Éxito: {is_valid} - "
            f"Confianza: {metrics.get('confidence_score', 0):.2f}"
        )
        
        return metrics

    def _truncate_content_for_provider(self, content: str, provider: str) -> str:
        """
        Trunca el contenido según los límites del proveedor.
        
        Args:
            content: Contenido a truncar
            provider: Proveedor de IA
            
        Returns:
            str: Contenido truncado
        """
        # Límites por proveedor (en caracteres)
        provider_limits = {
            "openai": 6000,  # Aproximadamente 1500 tokens para GPT-4
            "deepseek": 8000,  # Ajustar según la capacidad real
            "default": 4000
        }
        
        limit = provider_limits.get(provider, provider_limits["default"])
        
        if len(content) > limit:
            truncated = content[:limit]
            # Intentar no cortar a mitad de una palabra
            last_space = truncated.rfind(" ")
            if last_space > limit * 0.9:  # Si está cerca del final, cortar ahí
                truncated = truncated[:last_space]
            truncated += "... [contenido truncado]"
            return truncated
        
        return content
    
    def _calculate_quality_metrics(
        self, 
        response: str, 
        analysis_type: AnalysisType
    ) -> Dict[str, Any]:
        """
        Calcula métricas de calidad para la respuesta.
        
        Args:
            response: Respuesta del modelo
            analysis_type: Tipo de análisis realizado
            
        Returns:
            Dict[str, Any]: Métricas de calidad
        """
        metrics = {
            "confidence_score": 0.0,
            "completeness": 0.0,
            "structure_quality": 0.0
        }
        
        try:
            # Intentar parsear como JSON
            parsed = json.loads(response)
            
            if analysis_type == AnalysisType.FULL_ANALYSIS:
                # Verificar campos requeridos
                required_fields = ["summary", "keywords", "entities", "main_topic", "document_type", "purpose"]
                completeness = sum(1 for field in required_fields if field in parsed) / len(required_fields)
                metrics["completeness"] = completeness
                
                # Evaluar calidad estructural
                structure_quality = 1.0
                if "keywords" in parsed and not isinstance(parsed["keywords"], list):
                    structure_quality *= 0.8
                if "entities" in parsed and not isinstance(parsed["entities"], list):
                    structure_quality *= 0.8
                metrics["structure_quality"] = structure_quality
                
                # Calcular confianza compuesta
                metrics["confidence_score"] = completeness * structure_quality * 0.9
                
                # Bonificar respuestas detalladas
                if "keywords" in parsed and len(parsed["keywords"]) >= 5:
                    metrics["confidence_score"] += 0.05
                if "entities" in parsed and len(parsed["entities"]) >= 3:
                    metrics["confidence_score"] += 0.05
            
            # Limitar confianza a 1.0
            metrics["confidence_score"] = min(metrics["confidence_score"], 1.0)
            
        except json.JSONDecodeError:
            metrics["confidence_score"] = 0.0
            metrics["error"] = "JSON inválido"
        except Exception as e:
            metrics["confidence_score"] = 0.0
            metrics["error"] = str(e)
            
        return metrics
    
    def _update_success_rates(
        self, 
        provider: str, 
        analysis_type: AnalysisType,
        success: bool
    ) -> None:
        """
        Actualiza las tasas de éxito internas para cada proveedor y tipo de análisis.
        
        Args:
            provider: Proveedor de IA
            analysis_type: Tipo de análisis
            success: Si la respuesta fue exitosa
        """
        if provider not in self.success_rates:
            self.success_rates[provider] = {}
            
        analysis_key = analysis_type.value
        if analysis_key not in self.success_rates[provider]:
            self.success_rates[provider][analysis_key] = {"success": 0, "total": 0}
            
        self.success_rates[provider][analysis_key]["total"] += 1
        if success:
            self.success_rates[provider][analysis_key]["success"] += 1
    
    def get_provider_success_rates(self) -> Dict[str, Dict]:
        """
        Obtiene las tasas de éxito actuales por proveedor y tipo de análisis.
        
        Returns:
            Dict: Tasas de éxito
        """
        result = {}
        for provider, analysis_types in self.success_rates.items():
            result[provider] = {}
            for analysis_type, counts in analysis_types.items():
                if counts["total"] > 0:
                    success_rate = counts["success"] / counts["total"]
                    result[provider][analysis_type] = {
                        "success_rate": success_rate,
                        "total_requests": counts["total"]
                    }
                    
        return result
    
    def get_best_provider_for_analysis(self, analysis_type: AnalysisType) -> str:
        """
        Determina el mejor proveedor para un tipo específico de análisis
        basado en las tasas históricas de éxito.
        
        Args:
            analysis_type: Tipo de análisis
            
        Returns:
            str: Nombre del mejor proveedor
        """
        analysis_key = analysis_type.value
        best_provider = None
        best_rate = -1.0
        
        for provider, analysis_types in self.success_rates.items():
            if analysis_key in analysis_types:
                counts = analysis_types[analysis_key]
                if counts["total"] >= 5:  # Mínimo de muestras requerido
                    success_rate = counts["success"] / counts["total"]
                    if success_rate > best_rate:
                        best_rate = success_rate
                        best_provider = provider
                        
        # Si no hay suficientes datos, usar el proveedor predeterminado
        return best_provider if best_provider else "deepseek"

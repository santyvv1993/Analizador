from typing import Dict
import json
from openai import OpenAI
from ..config.settings import DEEPSEEK_API_KEY
from ..utils.ai_logger import AILogger

class AIAnalyzer:
    """Clase simplificada para análisis usando DeepSeek"""
    
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        self.logger = AILogger()

    def analyze_content(self, content: str, metadata: Dict = None, file_path: str = "unknown") -> Dict:
        """Analiza el contenido usando DeepSeek"""
        prompt = self._build_analysis_prompt(content, metadata)
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": """Eres un asistente especializado en análisis de documentos.
                     Debes responder en formato JSON con la siguiente estructura:
                     {
                         "summary": "resumen del documento",
                         "keywords": ["palabra1", "palabra2", ...],
                         "entities": [{"type": "tipo", "value": "valor"}, ...],
                         "main_topic": "tema principal",
                         "document_type": "tipo de documento",
                         "purpose": "propósito del documento"
                     }"""},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            try:
                analysis_result = json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                # Si falla el parseo JSON, usar el análisis básico
                analysis_result = self._basic_analysis(content)
            
            result = {
                "success": True,
                "analysis_result": analysis_result,
                "confidence_score": 0.85
            }
            
            # Registrar análisis exitoso
            self.logger.log_analysis(file_path, result)
            
            return result
                
        except Exception as e:
            # Registrar error
            self.logger.log_error(file_path, e)
            
            return {
                "success": False,
                "error": str(e),
                "fallback_analysis": self._basic_analysis(content),
                "analysis_result": self._basic_analysis(content),
                "confidence_score": 0.3
            }

    def _build_analysis_prompt(self, content: str, metadata: Dict) -> str:
        return f"""Analiza el siguiente documento y proporciona un JSON con:
        - Un resumen ejecutivo de máximo 250 palabras
        - Hasta 10 palabras clave relevantes
        - Entidades mencionadas (personas, organizaciones, lugares, fechas)
        - Tema principal
        - Tipo de documento
        - Propósito o intención del documento
        
        Contenido:
        {content[:4000]}
        """

    def _basic_analysis(self, content: str) -> Dict:
        """Análisis básico en caso de fallo"""
        return {
            "summary": content[:500],
            "keywords": self._extract_fallback_keywords(content),
            "entities": []
        }

    def _extract_fallback_keywords(self, content: str, max_keywords: int = 10) -> list:
        """Extrae palabras clave básicas del contenido"""
        words = [word for word in content.lower().split() if len(word) > 4]
        from collections import Counter
        return [word for word, _ in Counter(words).most_common(max_keywords)]

import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class AILogger:
    """Sistema de logging para respuestas de IA"""

    def __init__(self, log_dir: str = "logs/ai_analysis"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurar logger principal
        self.logger = logging.getLogger("ai_analysis")
        self.logger.setLevel(logging.INFO)
        
        # Configurar handler para archivo
        log_file = self.log_dir / "ai_analysis.log"
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_analysis(self, 
                    file_path: str, 
                    analysis_result: Dict[str, Any],
                    provider: str = "deepseek") -> None:
        """Registra un análisis de IA"""
        
        # Crear nombre de archivo para el registro detallado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = Path(file_path).stem
        detail_log_file = self.log_dir / f"{file_name}_{timestamp}.json"

        # Registrar resumen en el log principal
        self.logger.info(
            f"Análisis completado - Archivo: {file_path} - "
            f"Proveedor: {provider} - "
            f"Estado: {analysis_result.get('success', False)} - "
            f"Confianza: {analysis_result.get('confidence_score', 0)}"
        )

        # Guardar respuesta detallada en archivo JSON
        analysis_log = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "provider": provider,
            "analysis_result": analysis_result
        }

        with open(detail_log_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_log, f, indent=2, ensure_ascii=False)

    def log_error(self, 
                  file_path: str, 
                  error: Exception,
                  provider: str = "deepseek") -> None:
        """Registra un error en el análisis"""
        self.logger.error(
            f"Error en análisis - Archivo: {file_path} - "
            f"Proveedor: {provider} - "
            f"Error: {str(error)}",
            exc_info=True
        )

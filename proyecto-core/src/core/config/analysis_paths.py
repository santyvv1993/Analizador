from pathlib import Path
from typing import List

class AnalysisPaths:
    """Configuración de rutas para análisis"""
    
    @staticmethod
    def get_default_scan_paths() -> List[str]:
        """Retorna las rutas por defecto para escanear"""
        return [
            str(Path.home() / "Documents"),
            str(Path.home() / "Desktop")
        ]
    
    @staticmethod
    def is_valid_scan_path(path: str) -> bool:
        """Valida si una ruta es válida para escanear"""
        path_obj = Path(path)
        return path_obj.exists() and (path_obj.is_file() or path_obj.is_dir())

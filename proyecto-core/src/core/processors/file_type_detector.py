import os
import mimetypes
from pathlib import Path
from typing import Dict, Optional

class FileTypeDetector:
    """
    Clase para detectar el tipo de archivo basado en extensión y contenido.
    Utiliza python-magic para la detección por contenido cuando está disponible.
    """
    
    def __init__(self):
        self._cache = {}  # Cache para resultados de detección
        self._mimetypes = mimetypes  # Para facilitar pruebas
        self._initialize_mime_types()
        self._load_magic_module()
    
    def _initialize_mime_types(self):
        """Inicializa el mapeo de tipos MIME"""
        self._mimetypes.init()
        
        # Asegurar que las extensiones comunes estén mapeadas correctamente
        self._mimetypes.add_type('application/pdf', '.pdf')
        self._mimetypes.add_type('application/vnd.openxmlformats-officedocument.wordprocessingml.document', '.docx')
        self._mimetypes.add_type('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx')
        self._mimetypes.add_type('application/vnd.ms-excel', '.xls')
        self._mimetypes.add_type('text/plain', '.txt')
        self._mimetypes.add_type('text/csv', '.csv')
        self._mimetypes.add_type('text/log', '.log')
    
    def _load_magic_module(self):
        """Intenta cargar el módulo python-magic para detección por contenido"""
        self.magic_available = False
        try:
            import magic
            self.magic = magic.Magic(mime=True)
            self.magic_available = True
        except ImportError:
            print("python-magic no encontrado. Se utilizará solo la detección por extensión.")
    
    def detect_file_type(self, file_path: str) -> str:
        """
        Detecta el tipo MIME de un archivo.
        Primero intenta usar python-magic y luego cae en detección por extensión.
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            str: Tipo MIME del archivo
        """
        # Verificar si el archivo existe
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo no existe: {file_path}")
        
        # Comprobar en caché
        if file_path in self._cache:
            return self._cache[file_path]
        
        # Usar python-magic si está disponible
        if self.magic_available:
            try:
                mime_type = self.magic.from_file(file_path)
                self._cache[file_path] = mime_type
                return mime_type
            except Exception as e:
                print(f"Error al detectar tipo con magic: {e}")
        
        # Detección por extensión
        mime_type, _ = self._mimetypes.guess_type(file_path)
        if mime_type:
            self._cache[file_path] = mime_type
            return mime_type
        
        # Si no se puede determinar, usar application/octet-stream
        return "application/octet-stream"
    
    def clear_cache(self):
        """Limpia la caché de tipos MIME"""
        self._cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """
        Devuelve estadísticas sobre la caché
        
        Returns:
            Dict: Diccionario con estadísticas de caché
        """
        return {
            "cache_size": len(self._cache),
            "mime_types": list(set(self._cache.values()))
        }

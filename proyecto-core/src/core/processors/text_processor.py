from pathlib import Path
from typing import List, Dict, Optional
from .base_processor import BaseProcessor, ProcessedContent

class TextProcessor(BaseProcessor):
    """Procesador para archivos de texto plano (.txt, .csv, .log, etc.)"""

    def __init__(self):
        pass

    def validate(self, file_path: str) -> bool:
        """
        Valida si el archivo existe y es un archivo de texto
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            bool: True si el archivo es válido, False en caso contrario
        """
        if not Path(file_path).exists():
            return False
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1024)  # Leer primeros 1024 bytes para verificar que sea texto
            return True
        except UnicodeDecodeError:
            return False
        except Exception:
            return False

    def get_mime_type(self) -> str:
        """
        Devuelve el tipo MIME del archivo
        
        Returns:
            str: Tipo MIME del archivo
        """
        return "text/plain"

    def process(self, file_path: str) -> ProcessedContent:
        """
        Procesa el archivo de texto y devuelve su contenido procesado
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            ProcessedContent: Contenido procesado del archivo
        """
        if not self.validate(file_path):
            raise ValueError(f"Archivo inválido o no existe: {file_path}")
        
        # Leer el contenido del archivo
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Extraer metadatos básicos
        file_info = Path(file_path)
        
        # Crear metadatos
        metadata = {
            "file_name": file_info.name,
            "file_size": file_info.stat().st_size,
            "file_extension": file_info.suffix,
            "line_count": content.count('\n') + 1,
            "character_count": len(content)
        }
        
        # Extraer keywords básicos (palabras más frecuentes)
        words = [word.lower() for word in content.split() if len(word) > 4]
        from collections import Counter
        most_common = [word for word, _ in Counter(words).most_common(10)]
        
        return ProcessedContent(
            content=content,
            metadata=metadata,
            summary=content[:500] + "..." if len(content) > 500 else content,
            keywords=most_common,
            created_date=None,
            modified_date=file_info.stat().st_mtime,
            author=None,
            title=file_info.name,
            num_pages=1,
            language=self._detect_language(content),
            entities=[],
            confidence_score=0.7
        )
    
    def _detect_language(self, text: str) -> str:
        """
        Detecta el idioma del texto
        
        Args:
            text: Texto a analizar
            
        Returns:
            str: Código ISO del idioma detectado
        """
        try:
            import langdetect
            return langdetect.detect(text[:1000])
        except:
            return "en"  # Default to English

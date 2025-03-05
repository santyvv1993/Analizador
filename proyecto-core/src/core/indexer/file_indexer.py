from pathlib import Path
from typing import Dict, List, Optional
import hashlib
from datetime import datetime
from ..processors.processor_factory import ProcessorFactory

class FileIndexer:
    """Indexador de archivos que analiza archivos en su ubicación original"""

    def __init__(self):
        self.processor_factory = ProcessorFactory()

    def index_path(self, path: str) -> Dict:
        """Indexa un archivo o directorio sin moverlo"""
        path_obj = Path(path)
        
        if path_obj.is_file():
            return self._index_file(path_obj)
        elif path_obj.is_dir():
            return self._index_directory(path_obj)
        else:
            raise ValueError(f"La ruta no existe: {path}")

    def _index_file(self, file_path: Path) -> Dict:
        """Analiza un archivo individual"""
        # Calcular hash del archivo para identificación única
        file_hash = self._calculate_file_hash(file_path)
        
        # Obtener metadatos básicos
        stats = file_path.stat()
        basic_info = {
            "file_path": str(file_path.absolute()),
            "file_name": file_path.name,
            "file_type": file_path.suffix.lower(),
            "file_size": stats.st_size,
            "created_at": datetime.fromtimestamp(stats.st_ctime),
            "modified_at": datetime.fromtimestamp(stats.st_mtime),
            "hash": file_hash
        }

        # Intentar procesar el contenido si hay un procesador disponible
        try:
            processor = self.processor_factory.get_processor(str(file_path))
            content_analysis = processor.process(str(file_path))
            
            return {
                **basic_info,
                "processed": True,
                "analysis": content_analysis
            }
        except ValueError:
            # No hay procesador disponible para este tipo de archivo
            return {
                **basic_info,
                "processed": False,
                "analysis": None
            }

    def _index_directory(self, dir_path: Path) -> Dict:
        """Analiza un directorio completo"""
        files = []
        total_size = 0
        
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                file_info = self._index_file(file_path)
                files.append(file_info)
                total_size += file_info["file_size"]

        return {
            "directory_path": str(dir_path.absolute()),
            "directory_name": dir_path.name,
            "total_files": len(files),
            "total_size": total_size,
            "files": files,
            "indexed_at": datetime.now().isoformat()
        }

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calcula un hash único del archivo"""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            # Leer solo los primeros 64KB para archivos grandes
            hasher.update(f.read(65536))
        return hasher.hexdigest()

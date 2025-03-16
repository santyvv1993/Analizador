"""
Utilidad para monitorear el uso de memoria durante el procesamiento.
"""
import os
import time
import logging
from typing import Dict, Any, Callable, Optional, List
from functools import wraps

logger = logging.getLogger(__name__)

# Intentar importar psutil, pero no fallar si no está disponible
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.warning("psutil no está instalado. El monitoreo de memoria estará limitado.")
    # Para evitar errores, crear un stub básico
    class DummyProcess:
        def memory_info(self):
            class DummyMemInfo:
                rss = 0
                vms = 0
            return DummyMemInfo()
    
    class DummyPsutil:
        @staticmethod
        def Process(pid):
            return DummyProcess()
            
    psutil = DummyPsutil()

class MemoryMonitor:
    """
    Monitorea el uso de memoria durante la ejecución de funciones.
    Útil para optimizar el procesamiento de documentos grandes.
    """
    
    def __init__(self):
        """Inicializa el monitor de memoria"""
        self.process = psutil.Process(os.getpid())
        self.measurements = []
    
    def get_memory_usage(self) -> Dict[str, float]:
        """
        Obtiene el uso actual de memoria del proceso.
        
        Returns:
            Dict[str, float]: Uso de memoria en MB
        """
        # Si psutil no está disponible, devolver valores predeterminados
        if not PSUTIL_AVAILABLE:
            return {
                "rss": 0.0,  # MB
                "vms": 0.0,  # MB
            }
            
        try:
            # Forzar recolección de basura para obtener medición más precisa
            import gc
            gc.collect()
            
            # Obtener uso de memoria
            memory_info = self.process.memory_info()
            
            return {
                "rss": memory_info.rss / (1024 * 1024),  # MB
                "vms": memory_info.vms / (1024 * 1024),  # MB
            }
        except Exception as e:
            logger.error(f"Error al obtener uso de memoria: {e}")
            return {
                "rss": 0.0,
                "vms": 0.0,
            }
    
    def measure_function(self, func: Callable, *args, **kwargs) -> tuple:
        """
        Mide el uso de memoria durante la ejecución de una función.
        
        Args:
            func: Función a medir
            *args: Argumentos posicionales para la función
            **kwargs: Argumentos por nombre para la función
            
        Returns:
            tuple: (resultado_de_función, estadísticas_de_memoria)
        """
        # Medir uso inicial de memoria
        initial_memory = self.get_memory_usage()
        
        # Registrar tiempo y ejecutar función
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            end_time = time.time()
            # Medir uso final de memoria
            final_memory = self.get_memory_usage()
            
            # Calcular estadísticas
            stats = {
                "initial_memory_mb": initial_memory["rss"],
                "final_memory_mb": final_memory["rss"],
                "peak_memory_mb": final_memory["rss"],  # Si no podemos medir pico, usar final
                "memory_diff_mb": final_memory["rss"] - initial_memory["rss"],
                "execution_time_sec": end_time - start_time,
                "success": False,
                "error": str(e)
            }
            
            # Registrar medición
            self.measurements.append(stats)
            
            # Relanzar excepción
            raise
        
        end_time = time.time()
        
        # Medir uso final de memoria
        final_memory = self.get_memory_usage()
        
        # Calcular estadísticas
        stats = {
            "initial_memory_mb": initial_memory["rss"],
            "final_memory_mb": final_memory["rss"],
            "peak_memory_mb": final_memory["rss"],  # Estimado, no podemos medir pico exacto en todas las plataformas
            "memory_diff_mb": final_memory["rss"] - initial_memory["rss"],
            "execution_time_sec": end_time - start_time,
            "success": True,
            "error": None
        }
        
        # Registrar medición
        self.measurements.append(stats)
        
        return result, stats
    
    def get_average_stats(self) -> Dict[str, float]:
        """
        Calcula estadísticas promedio de todas las mediciones.
        
        Returns:
            Dict[str, float]: Estadísticas promedio
        """
        if not self.measurements:
            return {}
            
        successful_measurements = [m for m in self.measurements if m["success"]]
        if not successful_measurements:
            return {}
            
        # Calcular promedios
        avg_stats = {
            "avg_initial_memory_mb": sum(m["initial_memory_mb"] for m in successful_measurements) / len(successful_measurements),
            "avg_final_memory_mb": sum(m["final_memory_mb"] for m in successful_measurements) / len(successful_measurements),
            "avg_memory_diff_mb": sum(m["memory_diff_mb"] for m in successful_measurements) / len(successful_measurements),
            "avg_execution_time_sec": sum(m["execution_time_sec"] for m in successful_measurements) / len(successful_measurements),
            "total_measurements": len(self.measurements),
            "successful_measurements": len(successful_measurements),
            "success_rate": len(successful_measurements) / len(self.measurements)
        }
        
        return avg_stats
    
    def get_peak_memory_usage(self) -> float:
        """
        Obtiene el uso máximo de memoria registrado.
        
        Returns:
            float: Uso máximo de memoria en MB
        """
        if not self.measurements:
            return 0.0
            
        return max(m["peak_memory_mb"] for m in self.measurements)
    
    def clear_measurements(self):
        """Limpia todas las mediciones registradas."""
        self.measurements = []


def measure_memory(func: Callable) -> Callable:
    """
    Decorador para medir uso de memoria de una función.
    
    Args:
        func: Función a decorar
        
    Returns:
        Callable: Función decorada
    """
    monitor = MemoryMonitor()
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not PSUTIL_AVAILABLE:
            # Si psutil no está disponible, simplemente ejecutar la función sin medición
            return func(*args, **kwargs)
        
        result, stats = monitor.measure_function(func, *args, **kwargs)
        logger.info(
            f"Memoria para {func.__name__}: "
            f"Inicial={stats['initial_memory_mb']:.2f}MB, "
            f"Final={stats['final_memory_mb']:.2f}MB, "
            f"Diferencia={stats['memory_diff_mb']:.2f}MB, "
            f"Tiempo={stats['execution_time_sec']:.2f}s"
        )
        return result
    
    return wrapper

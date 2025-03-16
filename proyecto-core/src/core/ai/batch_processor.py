"""
Procesador por lotes para documentos extensos.
Maneja la división, procesamiento y consolidación de resultados.
"""
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor
import threading

logger = logging.getLogger(__name__)

class BatchProcessor:
    """
    Gestor de procesamiento por lotes para documentos grandes.
    Implementa estrategias de paralelización y gestión de memoria.
    """
    
    def __init__(
        self, 
        max_batch_size: int = 4000, 
        overlap: int = 500,
        max_workers: int = 3
    ):
        """
        Inicializa el procesador por lotes.
        
        Args:
            max_batch_size: Tamaño máximo de cada lote en caracteres
            overlap: Superposición entre lotes para mantener contexto
            max_workers: Número máximo de trabajadores paralelos
        """
        self.max_batch_size = max_batch_size
        self.overlap = overlap
        self.max_workers = max_workers
        self._lock = threading.Lock()
        self._cancel_requested = False
        
    def process_document(
        self, 
        content: str, 
        processor_func: Callable[[str, Dict], Dict[str, Any]],
        processor_args: Dict = None,
        progress_callback: Callable[[int, int], None] = None
    ) -> Dict[str, Any]:
        """
        Procesa un documento grande dividiéndolo en lotes.
        
        Args:
            content: Contenido completo del documento
            processor_func: Función para procesar cada lote
            processor_args: Argumentos adicionales para processor_func
            progress_callback: Función para reportar progreso
            
        Returns:
            Dict[str, Any]: Resultados consolidados
        """
        if not content:
            logger.warning("Contenido vacío proporcionado para procesamiento por lotes")
            return {"error": "Contenido vacío", "success": False}
            
        if len(content) <= self.max_batch_size:
            # Documento lo suficientemente pequeño para procesarlo directamente
            logger.info("Documento procesado como lote único")
            start_time = time.time()
            result = processor_func(content, **(processor_args or {}))
            processing_time = time.time() - start_time
            return {
                **result, 
                "processing_details": {
                    "batches": 1,
                    "total_time": processing_time,
                    "avg_batch_time": processing_time
                }
            }
        
        # Dividir documento en lotes
        batches = self._split_into_batches(content)
        total_batches = len(batches)
        logger.info(f"Documento dividido en {total_batches} lotes")
        
        # Reiniciar flag de cancelación
        self._cancel_requested = False
        
        # Procesar lotes (potencialmente en paralelo)
        batch_results = []
        processing_times = []
        
        if self.max_workers > 1:
            # Procesamiento paralelo
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Preparar futures
                future_to_batch = {
                    executor.submit(
                        self._process_single_batch, 
                        batch, 
                        idx, 
                        total_batches, 
                        processor_func, 
                        processor_args or {},
                        progress_callback
                    ): idx 
                    for idx, batch in enumerate(batches)
                }
                
                # Recoger resultados a medida que se completan
                for future in future_to_batch:
                    if self._cancel_requested:
                        logger.info("Procesamiento por lotes cancelado")
                        break
                        
                    try:
                        result, processing_time = future.result()
                        batch_results.append(result)
                        processing_times.append(processing_time)
                    except Exception as e:
                        logger.error(f"Error en procesamiento de lote: {e}")
        else:
            # Procesamiento secuencial
            for idx, batch in enumerate(batches):
                if self._cancel_requested:
                    logger.info("Procesamiento por lotes cancelado")
                    break
                    
                try:
                    result, processing_time = self._process_single_batch(
                        batch, idx, total_batches, processor_func, 
                        processor_args or {}, progress_callback
                    )
                    batch_results.append(result)
                    processing_times.append(processing_time)
                except Exception as e:
                    logger.error(f"Error en procesamiento de lote {idx+1}/{total_batches}: {e}")
        
        # Consolidar resultados
        if not batch_results:
            return {"error": "No se completó ningún lote", "success": False}
            
        consolidated = self._consolidate_results(batch_results)
        
        # Añadir metadatos de procesamiento
        total_time = sum(processing_times)
        avg_time = total_time / len(processing_times) if processing_times else 0
        
        consolidated["processing_details"] = {
            "batches": len(batch_results),
            "total_batches": total_batches,
            "completed": len(batch_results) == total_batches,
            "total_time": total_time,
            "avg_batch_time": avg_time
        }
        
        return consolidated
        
    def cancel_processing(self):
        """Cancela cualquier procesamiento en curso"""
        with self._lock:
            self._cancel_requested = True
            logger.info("Solicitud de cancelación de procesamiento recibida")
    
    def _split_into_batches(self, content: str) -> List[str]:
        """
        Divide el contenido en lotes manejables con superposición.
        
        Args:
            content: Contenido a dividir
            
        Returns:
            List[str]: Lista de lotes
        """
        batches = []
        start = 0
        
        while start < len(content):
            # Determinar el final de este lote
            end = min(start + self.max_batch_size, len(content))
            
            # Si no estamos al final, buscar un buen punto de corte
            if end < len(content):
                # Intentar encontrar un párrafo
                paragraph_end = content.find('\n\n', end - 200, end + 200)
                if paragraph_end != -1:
                    end = paragraph_end + 2  # Incluir los saltos de línea
                else:
                    # Intentar encontrar un final de oración
                    sentence_end = max(
                        content.find('. ', end - 100, end + 100),
                        content.find('! ', end - 100, end + 100),
                        content.find('? ', end - 100, end + 100)
                    )
                    if sentence_end != -1:
                        end = sentence_end + 2  # Incluir el espacio
                    else:
                        # Como último recurso, un espacio
                        space = content.find(' ', end - 50, end + 50)
                        if space != -1:
                            end = space + 1
            
            # Añadir el lote actual
            batches.append(content[start:end])
            
            # Calcular inicio del próximo lote (con superposición)
            if end >= len(content):
                break
                
            # Avanzar el inicio teniendo en cuenta la superposición
            start = max(end - self.overlap, start + 1)
        
        return batches
    
    def _process_single_batch(
        self,
        batch: str, 
        batch_idx: int, 
        total_batches: int,
        processor_func: Callable[[str, Dict], Dict[str, Any]],
        processor_args: Dict,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> tuple:
        """
        Procesa un solo lote y mide el tiempo.
        
        Args:
            batch: Contenido del lote
            batch_idx: Índice del lote actual
            total_batches: Número total de lotes
            processor_func: Función de procesamiento
            processor_args: Argumentos para la función
            progress_callback: Función para reportar progreso
            
        Returns:
            tuple: (resultado, tiempo_de_procesamiento)
        """
        logger.info(f"Procesando lote {batch_idx+1}/{total_batches}")
        
        # Añadir metadatos de lote
        batch_args = processor_args.copy()
        batch_args["batch_metadata"] = {
            "batch_idx": batch_idx,
            "total_batches": total_batches,
            "is_first_batch": batch_idx == 0,
            "is_last_batch": batch_idx == total_batches - 1
        }
        
        start_time = time.time()
        result = processor_func(batch, **batch_args)
        processing_time = time.time() - start_time
        
        logger.info(f"Lote {batch_idx+1}/{total_batches} completado en {processing_time:.2f}s")
        
        # Reportar progreso si hay callback
        if progress_callback:
            progress_callback(batch_idx + 1, total_batches)
            
        return result, processing_time
    
    def _consolidate_results(self, batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Consolida los resultados de múltiples lotes.
        
        Args:
            batch_results: Resultados de todos los lotes procesados
            
        Returns:
            Dict[str, Any]: Resultado consolidado
        """
        if not batch_results:
            return {}
            
        # Implementación básica: tomar el primer resultado como base
        consolidated = batch_results[0].copy()
        
        # Para cada tipo de resultado, implementar estrategias de consolidación específicas
        
        # Consolidar entidades (combinar y eliminar duplicados)
        if "entities" in consolidated:
            all_entities = consolidated.get("entities", [])
            entity_map = {f"{e['type']}:{e['value']}": e for e in all_entities}
            
            for result in batch_results[1:]:
                batch_entities = result.get("entities", [])
                for entity in batch_entities:
                    key = f"{entity['type']}:{entity['value']}"
                    if key in entity_map:
                        # Actualizar relevancia si es mayor
                        if entity.get('relevance', 0) > entity_map[key].get('relevance', 0):
                            entity_map[key]['relevance'] = entity['relevance']
                    else:
                        entity_map[key] = entity
            
            consolidated["entities"] = list(entity_map.values())
        
        # Consolidar keywords (combinar y mantener las más relevantes)
        if "keywords" in consolidated:
            keyword_set = set(consolidated.get("keywords", []))
            
            for result in batch_results[1:]:
                keywords = result.get("keywords", [])
                keyword_set.update(keywords)
            
            consolidated["keywords"] = list(keyword_set)[:15]  # Limitar a 15 keywords
        
        # Para resúmenes, combinar o seleccionar el mejor
        if "summary" in consolidated:
            summaries = [result.get("summary", "") for result in batch_results]
            # Seleccionar el resumen más largo como potencialmente más completo
            best_summary = max(summaries, key=len) if summaries else ""
            consolidated["summary"] = best_summary
            
        return consolidated

    def cluster_related_entities(
        self, 
        entities: List[Dict[str, Any]], 
        relations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Agrupa entidades que están relacionadas según el análisis de relaciones.
        Útil para consolidar resultados de múltiples lotes.
        
        Args:
            entities: Lista de entidades detectadas
            relations: Lista de relaciones entre entidades
            
        Returns:
            List[Dict[str, Any]]: Entidades agrupadas por clústeres relacionados
        """
        # Si no hay suficientes entidades o relaciones, devolver las entidades originales
        if len(entities) < 3 or len(relations) < 2:
            return [{"cluster_id": 0, "entities": entities}]
            
        # Construir grafo de relaciones entre entidades
        entity_graph = {}
        for entity in entities:
            entity_id = f"{entity['type']}:{entity['value']}"
            entity_graph[entity_id] = {"entity": entity, "connections": []}
        
        # Añadir conexiones basadas en relaciones
        for relation in relations:
            source = relation["source"]
            target = relation["target"]
            
            # Buscar IDs de entidades que coincidan
            source_ids = [eid for eid in entity_graph.keys() if source in eid or eid.endswith(f":{source}")]
            target_ids = [eid for eid in entity_graph.keys() if target in eid or eid.endswith(f":{target}")]
            
            # Conectar entidades relacionadas
            for sid in source_ids:
                for tid in target_ids:
                    if sid != tid:  # Evitar autorelaciones
                        entity_graph[sid]["connections"].append(tid)
                        entity_graph[tid]["connections"].append(sid)  # Relación bidireccional
        
        # Función para buscar componentes conectados (DFS)
        visited = set()
        clusters = []
        
        def dfs(node_id, current_cluster):
            visited.add(node_id)
            current_cluster.append(entity_graph[node_id]["entity"])
            for connected_id in entity_graph[node_id]["connections"]:
                if connected_id not in visited:
                    dfs(connected_id, current_cluster)
        
        # Encontrar todos los clusters
        cluster_id = 0
        for entity_id in entity_graph:
            if entity_id not in visited:
                current_cluster = []
                dfs(entity_id, current_cluster)
                if current_cluster:  # Si no está vacío
                    clusters.append({
                        "cluster_id": cluster_id,
                        "entities": current_cluster
                    })
                    cluster_id += 1
        
        # Añadir entidades aisladas (sin conexiones) como clusters individuales
        for entity_id, data in entity_graph.items():
            if entity_id not in visited:
                clusters.append({
                    "cluster_id": cluster_id,
                    "entities": [data["entity"]]
                })
                cluster_id += 1
        
        return clusters

#!/usr/bin/env python3
"""
AGENTE DE GRAFO — Navegação e Expansão de Grafo Ontológico.

Encapsula o OntologyGraph com navegação inteligente, expansão de contexto
via BFS ponderado e descoberta de caminhos semânticos.

FASE 7c do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))
if str(_PROJECT_ROOT / "runtime") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "runtime"))

from core.agent_base import BaseAgent, AgentResult, AgentMemory
from core.ontology_graph import OntologyGraph


@dataclass
class GraphExpansionResult:
    """Resultado de uma expansão de grafo."""
    seed_nodes: List[str] = field(default_factory=list)
    neighbors: List[dict] = field(default_factory=list)
    paths: List[dict] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    latency_ms: float = 0.0

    def to_dict(self) -> dict:
        return {
            "seed_nodes": self.seed_nodes,
            "neighbors": self.neighbors,
            "paths": self.paths,
            "metrics": self.metrics,
            "latency_ms": round(self.latency_ms, 2),
        }


@dataclass
class SemanticWalkStep:
    """Um passo em um passeio semântico pelo grafo."""
    node_id: str
    nome: str
    tipo_aresta: str
    peso: float
    step: int
    nivel: int = 0

    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "nome": self.nome,
            "tipo_aresta": self.tipo_aresta,
            "peso": round(self.peso, 4),
            "step": self.step,
            "nivel": self.nivel,
        }


class GraphAgent(BaseAgent):
    """
    Agente especializado em navegação e expansão do grafo ontológico.

    Responsabilidades:
    - Expandir vizinhança de células a partir de seeds do retrieval
    - Encontrar caminhos semânticos entre conceitos
    - Realizar passeios semânticos guiados por estratégia
    - Calcular métricas topológicas para contexto
    - Fornecer contexto relacional para o synthesis agent

    Diferencial em relação ao uso direto do OntologyGraph:
    - Cache de expansões frequentes
    - Navegação guiada por tipo de relação (priorizando dependências)
    - Filtragem de vizinhos por relevância
    - Resumo contextual para o pipeline
    """

    AGENT_NAME: str = "GraphAgent"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = ["expand_neighbors", "find_paths", "semantic_walk", "get_metrics"]

    def __init__(
        self,
        memory: Optional[AgentMemory] = None,
        config: Optional[Dict[str, Any]] = None,
        graph: Optional[OntologyGraph] = None,
    ):
        super().__init__(
            name=self.AGENT_NAME,
            memory=memory,
            config=config or {},
        )
        self._graph = graph or OntologyGraph()
        if not self._graph.registry:
            self._graph.load_registry()
            self._graph.build_graph()

        self._expansion_cache: Dict[str, GraphExpansionResult] = {}
        self._cache_max_size = 500

        logger.info("GraphAgent inicializado: %d nós, %d arestas",
                     self._graph.G.number_of_nodes(),
                     self._graph.G.number_of_edges())

    # ── Core Execution ──────────────────────────────────────────────────

    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Executa operação de grafo baseada na task.

        Args:
            task: Tipo de operação ("expand", "paths", "walk", "metrics")
            context: Dict com parâmetros da operação:
                - seed_uids: List[str] para expansão
                - source/target: Para busca de caminhos
                - start_node: Para passeio semântico
                - depth: Profundidade de expansão

        Returns:
            AgentResult com o resultado da operação de grafo.
        """
        t0 = time.time()
        context = context or {}

        try:
            operation = task.strip().lower()

            if operation == "expand" or operation == "neighbors":
                result = self._handle_expand(context)
            elif operation == "paths":
                result = self._handle_paths(context)
            elif operation == "walk":
                result = self._handle_walk(context)
            elif operation == "metrics":
                result = self._handle_metrics(context)
            elif operation == "subgraph":
                result = self._handle_subgraph(context)
            else:
                # Default: expand neighbors
                result = self._handle_expand(context)

            latency_ms = (time.time() - t0) * 1000

            return AgentResult(
                agent_name=self.name,
                task=task,
                output=result.to_dict(),
                confidence=self._estimate_confidence(result),
                latency_ms=latency_ms,
                reasoning_steps=self._build_reasoning(result),
                metadata={
                    "operation": operation,
                    "graph_nodes": self._graph.G.number_of_nodes(),
                    "graph_edges": self._graph.G.number_of_edges(),
                },
            )

        except Exception as e:
            logger.error("GraphAgent falhou na operação '%s': %s", task, e, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": str(e)},
                confidence=0.0,
                latency_ms=(time.time() - t0) * 1000,
                errors=[str(e)],
            )

    # ── Operation Handlers ──────────────────────────────────────────────

    def _handle_expand(self, context: Dict[str, Any]) -> GraphExpansionResult:
        """Expande vizinhos a partir de nós seed."""
        seed_uids = context.get("seed_uids", [])
        depth = context.get("depth", 3)
        relation_filter = context.get("relation_type", None)

        if not seed_uids:
            return GraphExpansionResult()

        # Verificar cache
        cache_key = self._expansion_cache_key(seed_uids, depth, relation_filter)
        if cache_key in self._expansion_cache:
            return self._expansion_cache[cache_key]

        all_neighbors = []
        seen_targets = set()

        for uid in seed_uids:
            neighbors = self._graph.query_neighbors(
                uid,
                relation_type=relation_filter,
                depth=depth,
            )
            for nb in neighbors:
                target = nb["target"]
                if target not in seen_targets:
                    seen_targets.add(target)
                    all_neighbors.append({
                        **nb,
                        "seed": uid,
                    })

        # Ordenar por peso absoluto
        all_neighbors.sort(key=lambda x: abs(x.get("peso", 0)), reverse=True)

        # Limitar para top-N
        max_neighbors = context.get("max_neighbors", 50)
        all_neighbors = all_neighbors[:max_neighbors]

        result = GraphExpansionResult(
            seed_nodes=seed_uids,
            neighbors=all_neighbors,
            metrics={
                "total_seeds": len(seed_uids),
                "total_neighbors": len(all_neighbors),
                "unique_targets": len(seen_targets),
                "depth": depth,
            },
        )

        # Cache
        if len(self._expansion_cache) < self._cache_max_size:
            self._expansion_cache[cache_key] = result

        return result

    def _handle_paths(self, context: Dict[str, Any]) -> GraphExpansionResult:
        """Encontra caminhos entre dois nós."""
        source = context.get("source", "")
        target = context.get("target", "")
        max_length = context.get("max_length", 5)
        max_paths = context.get("max_paths", 20)
        directed = context.get("directed", False)

        if not source or not target:
            return GraphExpansionResult()

        paths = self._graph.infer_paths(
            source=source,
            target=target,
            max_length=max_length,
            max_paths=max_paths,
            directed=directed,
        )

        return GraphExpansionResult(
            seed_nodes=[source],
            paths=paths,
            metrics={
                "source": source,
                "target": target,
                "total_paths": len(paths),
                "max_length": max_length,
            },
        )

    def _handle_walk(self, context: Dict[str, Any]) -> GraphExpansionResult:
        """Realiza um passeio semântico pelo grafo."""
        start_node = context.get("start_node", "")
        steps = context.get("steps", 5)
        strategy = context.get("strategy", "weighted")
        allow_negative = context.get("allow_negative", False)
        allow_revisit = context.get("allow_revisit", False)

        if not start_node or start_node not in self._graph.G:
            return GraphExpansionResult()

        path = self._graph.semantic_walk(
            start_node=start_node,
            steps=steps,
            strategy=strategy,
            allow_negative=allow_negative,
            allow_revisit=allow_revisit,
        )

        walk_steps = []
        for i, step in enumerate(path):
            node_data = self._graph._node_index.get(step["node_id"], {})
            walk_steps.append(SemanticWalkStep(
                node_id=step["node_id"],
                nome=step.get("nome", step["node_id"]),
                tipo_aresta=step.get("tipo_aresta", ""),
                peso=step.get("peso", 0),
                step=i,
                nivel=node_data.get("nivel", 0),
            ))

        return GraphExpansionResult(
            seed_nodes=[start_node],
            metrics={
                "start_node": start_node,
                "steps_taken": len(walk_steps),
                "strategy": strategy,
            },
            neighbors=[{
                "target": ws.node_id,
                "nome": ws.nome,
                "tipo": ws.tipo_aresta,
                "peso": ws.peso,
                "step": ws.step,
                "nivel": ws.nivel,
            } for ws in walk_steps],
        )

    def _handle_metrics(self, context: Dict[str, Any]) -> GraphExpansionResult:
        """Calcula métricas topológicas do grafo ou de uma subárvore."""
        subtree_root = context.get("subtree_root", None)

        if subtree_root:
            # Métricas de uma subárvore específica
            neighbors = self._graph.query_neighbors(subtree_root, depth=3)
            node_ids = {subtree_root} | {n["target"] for n in neighbors}
            subgraph = self._graph.G.subgraph(node_ids)
            metrics = self._compute_subgraph_metrics(subgraph)
        else:
            # Métricas do grafo completo (usar cache se disponível)
            cache_key = "__full_graph_metrics__"
            if cache_key in self._expansion_cache:
                metrics = self._expansion_cache[cache_key].metrics
            else:
                metrics = self._compute_full_graph_metrics()
                result = GraphExpansionResult(metrics=metrics)
                self._expansion_cache[cache_key] = result

        return GraphExpansionResult(metrics=metrics)

    def _handle_subgraph(self, context: Dict[str, Any]) -> GraphExpansionResult:
        """Extrai um subgrafo ao redor de um conjunto de nós."""
        center_uids = context.get("center_uids", [])
        depth = context.get("depth", 2)

        if not center_uids:
            return GraphExpansionResult()

        all_nodes = set(center_uids)
        for uid in center_uids:
            neighbors = self._graph.query_neighbors(uid, depth=depth)
            all_nodes.update(n["target"] for n in neighbors)

        subgraph_data = []
        for uid in all_nodes:
            node_data = self._graph._node_index.get(uid, {})
            neighbors_data = self._graph.query_neighbors(uid, depth=1)
            subgraph_data.append({
                "uid": uid,
                "node": node_data,
                "connections": len(neighbors_data),
            })

        return GraphExpansionResult(
            seed_nodes=center_uids,
            neighbors=subgraph_data,
            metrics={"nodes": len(all_nodes), "depth": depth},
        )

    # ── Metrics Computation ─────────────────────────────────────────────

    def _compute_subgraph_metrics(self, subgraph) -> Dict[str, Any]:
        """Calcula métricas para um subgrafo."""
        import networkx as nx
        return {
            "nodes": subgraph.number_of_nodes(),
            "edges": subgraph.number_of_edges(),
            "density": nx.density(subgraph) if subgraph.number_of_nodes() > 1 else 0,
            "avg_clustering": nx.average_clustering(subgraph.to_undirected()) if subgraph.number_of_nodes() > 2 else 0,
        }

    def _compute_full_graph_metrics(self) -> Dict[str, Any]:
        """Calcula métricas do grafo completo (com cache)."""
        return self._graph.compute_metrics()

    # ── Utilities ───────────────────────────────────────────────────────

    def _expansion_cache_key(
        self,
        seed_uids: List[str],
        depth: int,
        relation_type: Optional[str],
    ) -> str:
        """Gera chave de cache para expansão."""
        seeds_str = "|".join(sorted(seed_uids))
        return f"{seeds_str}:d={depth}:r={relation_type or 'all'}"

    def _estimate_confidence(self, result: GraphExpansionResult) -> float:
        """Estima confiança baseada na qualidade da expansão."""
        if not result.neighbors and not result.paths:
            return 0.0
        n_results = len(result.neighbors) + len(result.paths)
        if n_results == 0:
            return 0.0
        return min(1.0, 0.3 + 0.7 * (n_results / max(len(result.seed_nodes) * 3, 1)))

    def _build_reasoning(self, result: GraphExpansionResult) -> List[str]:
        """Gera explicação da operação de grafo."""
        reasoning = []
        if result.seed_nodes:
            reasoning.append(f"Seeds: {result.seed_nodes[:5]}")
        if result.metrics:
            reasoning.append(f"Métricas: {json.dumps(result.metrics, default=str)[:200]}")
        if result.neighbors:
            top5 = result.neighbors[:5]
            reasoning.append(
                f"Top vizinhos: {[(n.get('target', '?'), n.get('tipo', '?')) for n in top5]}"
            )
        return reasoning

    # ── Batch Operations ────────────────────────────────────────────────

    def expand_multiple(
        self,
        seed_groups: List[List[str]],
        depth: int = 3,
    ) -> List[GraphExpansionResult]:
        """Expande múltiplos grupos de seeds."""
        return [
            self._handle_expand({"seed_uids": group, "depth": depth})
            for group in seed_groups
        ]

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.REQUIRED_TOOLS,
            "description": "Navegação e expansão do grafo ontológico",
            "graph_stats": {
                "nodes": self._graph.G.number_of_nodes(),
                "edges": self._graph.G.number_of_edges(),
                "cache_size": len(self._expansion_cache),
            },
            "operations": ["expand", "paths", "walk", "metrics", "subgraph"],
        }
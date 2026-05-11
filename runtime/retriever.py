#!/usr/bin/env python3
"""Motor de Retrieval Híbrido para a Ontologia Fractal.

Combina três fontes de recuperação:
  1. Similaridade vetorial (embeddings 384-dim)
  2. Navegação por grafo (vizinhança ontológica)
  3. Filtragem simbólica (tags, natureza, metadados)

O pipeline é:
  query → embedding → top-K vetorial → expansão via grafo → filtro simbólico → rerank
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Optional

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from core.ontology_graph import OntologyGraph

logger = logging.getLogger(__name__)

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))


class HybridRetriever:
    """Retriever híbrido que combina similaridade vetorial, navegação por grafo
    e filtragem simbólica sobre a ontologia fractal de 162 células N4.

    Attributes:
        embedding_dir: Diretório com arquivos .npy de embeddings.
        graph: Instância do grafo ontológico.
        registry: Dicionário de metadados das células N4.
        config: Configurações de retrieval (thresholds, pesos, limites).
        embeddings: Cache de vetores carregados em memória {uid: np.ndarray}.
        embedding_dim: Dimensão dos vetores (default 384).
    """

    def __init__(
        self,
        embedding_dir: str = "data/embeddings",
        json_dir: str = "data/json",
        graph_engine: OntologyGraph | None = None,
        config_path: str = "config/retrieval.yaml",
    ):
        """Inicializa o retriever híbrido.

        Args:
            embedding_dir: Caminho para diretório de embeddings .npy.
            json_dir: Caminho para diretório de JSONs N4 enriquecidos.
            graph_engine: Instância pré-construída do OntologyGraph (opcional).
            config_path: Caminho para arquivo de configuração YAML.
        """
        # Resolver caminhos relativos ao diretório raiz do projeto
        if not Path(embedding_dir).is_absolute():
            embedding_dir = str(_PROJECT_ROOT / embedding_dir)
        if not Path(json_dir).is_absolute():
            json_dir = str(_PROJECT_ROOT / json_dir)
        if not Path(config_path).is_absolute():
            config_path = str(_PROJECT_ROOT / config_path)

        self.embedding_dir = Path(embedding_dir)
        self.embedding_dim = 384

        # Carregar configuração
        self.config = self._load_config(config_path)
        hybrid_cfg = self.config.get("fusao", {})
        self.weights = hybrid_cfg.get("pesos", {
            "vetorial": 0.50,
            "grafico": 0.30,
            "simbolico": 0.20,
        })
        self.threshold = self.config.get("vetorial", {}).get(
            "limiar_minimo", 0.15
        )
        self.top_k_semantic = self.config.get("vetorial", {}).get("top_k", 20)
        self.top_k_final = hybrid_cfg.get("top_k_saida", 12)
        self.graph_depth = self.config.get("grafico", {}).get(
            "profundidade_max", 3
        )

        # Inicializar grafo ontológico
        if graph_engine is not None:
            self.graph = graph_engine
        else:
            self.graph = OntologyGraph(json_dir=json_dir)
            self.graph.load_registry()
            self.graph.build_graph()

        self.registry = self.graph.registry

        # Carregar embeddings em memória
        self.embeddings = self._load_embeddings()
        logger.info(
            "HybridRetriever inicializado: %d células, threshold=%.2f",
            len(self.embeddings),
            self.threshold,
        )

    # ------------------------------------------------------------------
    # Carregamento
    # ------------------------------------------------------------------

    def _load_config(self, config_path: str) -> dict[str, Any]:
        """Carrega configuração YAML com fallback para defaults."""
        try:
            import yaml

            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except (ImportError, FileNotFoundError):
            logger.warning(
                "Config YAML não encontrado (%s), usando defaults", config_path
            )
            return self._default_config()

    @staticmethod
    def _default_config() -> dict[str, Any]:
        """Configuração padrão quando YAML indisponível."""
        return {
            "vetorial": {
                "limiar_minimo": 0.15,
                "top_k": 20,
            },
            "grafico": {
                "profundidade_max": 3,
            },
            "fusao": {
                "pesos": {
                    "vetorial": 0.50,
                    "grafico": 0.30,
                    "simbolico": 0.20,
                },
                "top_k_saida": 12,
                "limiar_final": 0.40,
            },
        }

    def _load_embeddings(self) -> dict[str, np.ndarray]:
        """Carrega todos os embeddings .npy do diretório em memória."""
        embeddings = {}
        if not self.embedding_dir.exists():
            logger.error("Diretório de embeddings não encontrado: %s", self.embedding_dir)
            return embeddings

        for f in sorted(self.embedding_dir.glob("N4_*.npy")):
            uid = f.stem
            vec = np.load(f)
            if vec.shape[0] != self.embedding_dim:
                logger.warning(
                    "Dimensão inesperada para %s: esperado %d, got %d",
                    uid,
                    self.embedding_dim,
                    vec.shape[0],
                )
            embeddings[uid] = vec.astype(np.float32)

        logger.info("Carregados %d embeddings de %s", len(embeddings), self.embedding_dir)
        return embeddings

    # ------------------------------------------------------------------
    # BUSCA VETORIAL
    # ------------------------------------------------------------------

    def embed_query(self, query: str) -> np.ndarray:
        """Gera embedding para uma query usando o modelo sentence-transformers."""
        from sentence_transformers import SentenceTransformer

        if not hasattr(self, "_query_model") or self._query_model is None:
            model_name = self.config.get("modelo", {}).get(
                "nome", "sentence-transformers/all-MiniLM-L6-v2"
            )
            self._query_model = SentenceTransformer(model_name)
        vector = self._query_model.encode(query, normalize_embeddings=True, convert_to_numpy=True)
        return vector.astype(np.float32)

    def retrieve_semantic(
        self, query_embedding: np.ndarray, top_k: int | None = None
    ) -> list[tuple[str, float]]:
        """Busca por similaridade vetorial (coseno).

        Retorna lista de (uid, score) ordenada por score decrescente,
        filtrada pelo threshold mínimo.
        """
        if top_k is None:
            top_k = self.top_k_semantic

        if not self.embeddings:
            return []

        all_uids = list(self.embeddings.keys())
        all_vectors = np.stack([self.embeddings[uid] for uid in all_uids])

        similarities = cosine_similarity(
            query_embedding.reshape(1, -1), all_vectors
        )[0]

        results = []
        for uid, sim in zip(all_uids, similarities):
            if sim >= self.threshold:
                results.append((uid, float(sim)))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # BUSCA GRÁFICA
    # ------------------------------------------------------------------

    def retrieve_graph(
        self, seed_uids: list[tuple[str, float]], depth: int | None = None
    ) -> dict[str, float]:
        """Expande candidatos via navegação no grafo ontológico.

        Para cada seed (uid, sim), coleta vizinhos até a profundidade especificada
        e atribui score baseado na proximidade hierárquica e peso das arestas.

        Args:
            seed_uids: Lista de tuplas (uid, similaridade_vetorial).
            depth: Profundidade máxima de expansão no grafo.

        Returns:
            Dicionário {uid: score_grafico}
        """
        if depth is None:
            depth = self.graph_depth
        if depth is None:
            depth = 3

        expanded: dict[str, float] = {}

        for uid, seed_sim in seed_uids:
            # Score direto da similaridade vetorial
            if uid not in expanded or seed_sim > expanded[uid]:
                expanded[uid] = float(seed_sim)

            # Busca em largura no grafo
            neighbors = self.graph.query_neighbors(uid, depth=depth)
            for neighbor in neighbors:
                n_uid = neighbor["target"]
                edge_weight = abs(neighbor.get("peso", 0))

                # Score de proximidade: similaridade original × peso da aresta × fator de decaimento
                graph_score = seed_sim * edge_weight * 0.5

                if n_uid not in expanded or graph_score > expanded[n_uid]:
                    expanded[n_uid] = graph_score

        return expanded

    # ------------------------------------------------------------------
    # FILTRO SIMBÓLICO
    # ------------------------------------------------------------------

    def _symbolic_filter(
        self, candidates: dict[str, float], query_concepts: list[str]
    ) -> dict[str, float]:
        """Aplica boost simbólico baseado em tags, natureza e metadados.

        Células cujas tags/natureza coincidem com conceitos da query
        recebem um multiplicador de relevância.
        """
        filtered: dict[str, float] = {}

        for uid, score in candidates.items():
            data = self.registry.get(uid, {})
            boost = 1.0

            # Verificar tags
            cell_tags = data.get("tags", [])
            cell_tags_lower = [t.lower() for t in cell_tags]
            for concept in query_concepts:
                if concept.lower() in cell_tags_lower:
                    boost += 0.2

            # Verificar natureza
            natureza = data.get("natureza", "").lower()
            if natureza and any(c.lower() == natureza for c in query_concepts):
                boost += 0.15

            # Verificar nome e nome_normalizado
            nome = data.get("nome", "").lower()
            nome_norm = data.get("nome_normalizado", "").lower()
            for concept in query_concepts:
                if concept.lower() in nome or concept.lower() in nome_norm:
                    boost += 0.1

            # Cap do boost
            filtered[uid] = score * min(boost, 1.8)

        return filtered

    # ------------------------------------------------------------------
    # RETRIEVAL HÍBRIDO
    # ------------------------------------------------------------------

    def hybrid_rank(
        self,
        query: str,
        top_k: int | None = None,
        return_scores: bool = True,
    ) -> list[dict[str, Any]]:
        """Pipeline completo de retrieval híbrido.

        Etapas:
        1. Query → embedding vetorial → top-K candidatos (similaridade vetorial)
        2. Expansão via grafo ontológico (vizinhança + profundidade)
        3. Filtragem simbólica (tags, natureza, nomes)
        4. Fusão ponderada e reranking final

        Score final = (peso_vetorial × sim_vetorial)
                    + (peso_grafico × sim_grafico)
                    + (peso_simbolico × boost_simbolico)

        Args:
            query: Texto da consulta.
            top_k: Número de resultados desejados (default do config).
            return_scores: Se True, inclui scores detalhados.

        Returns:
            Lista de dicts com uid, conceito, path, pilar, natureza, score e detalhes.
        """
        if top_k is None:
            top_k = self.top_k_final

        t0 = time.time()

        # 1. Embedding da query e busca vetorial
        query_emb = self.embed_query(query)
        semantic_results = self.retrieve_semantic(query_emb, top_k=self.top_k_semantic)

        if not semantic_results:
            logger.info("Nenhum resultado vetorial acima do threshold para query: %s", query)
            return []

        # 2. Expansão via grafo (passa tuplas completas)
        expanded = self.retrieve_graph(semantic_results, depth=self.graph_depth)

        # 3. Filtragem simbólica
        query_words = [w for w in query.lower().split() if len(w) > 2]
        filtered = self._symbolic_filter(expanded, query_words)

        # 4. Fusão ponderada e reranking
        # Normalizar scores para [0, 1] antes da fusão
        if not filtered:
            return []

        max_score = max(filtered.values())
        if max_score < 1e-8:
            return []

        normalized = {uid: score / max_score for uid, score in filtered.items()}

        # Aplicar pesos de fusão
        final_scores = {}
        component_scores = {}
        for uid, norm_score in normalized.items():
            # Determinar componentes
            sem_score = next((s for u, s in semantic_results if u == uid), 0.0)
            sem_norm = sem_score / max_score if max_score > 0 else 0.0

            graph_raw = expanded.get(uid, 0.0)
            graph_score = graph_raw / max_score if max_score > 0 else 0.0

            sym_score = (
                filtered[uid] / expanded[uid] if expanded.get(uid, 0) > 0 else 1.0
            )
            sym_norm = min(sym_score, 1.8) / 1.8  # normalizar boost simbólico

            w_v = self.weights.get("vetorial", 0.50)
            w_g = self.weights.get("grafico", 0.30)
            w_s = self.weights.get("simbolico", 0.20)

            final = (w_v * sem_norm) + (w_g * graph_score) + (w_s * sym_norm)
            final_scores[uid] = round(final, 6)
            component_scores[uid] = {
                "semantic_sim": round(sem_norm, 6),
                "graph_score": round(graph_score, 6),
                "symbolic_boost": round(sym_norm, 6),
            }

        # Ordenar e limitar
        ranked = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        # Construir resultados detalhados
        results = []
        for uid, score in ranked:
            data = self.registry.get(uid, {})
            comps = component_scores.get(uid, {})
            results.append({
                "uid": uid,
                "score": score,
                "conceito": data.get("nome", uid),
                "path": data.get("path", ""),
                "pilar": data.get("pilar", ""),
                "dominio": data.get("dominio", ""),
                "natureza": data.get("natureza", ""),
                "axis": data.get("axis", ""),
                "n3_name": data.get("n3_name", ""),
                "semantic_sim": comps.get("semantic_sim", 0.0),
                "graph_score": comps.get("graph_score", 0.0),
            })

        elapsed = time.time() - t0
        logger.info(
            "Retrieval híbrido: query='%s' → %d resultados em %.3fs",
            query,
            len(results),
            elapsed,
        )

        return results

    # ------------------------------------------------------------------
    # API DE BUSCA PRINCIPAL
    # ------------------------------------------------------------------

    def search(
        self, query: str, top_k: int | None = None
    ) -> list[dict[str, Any]]:
        """Busca híbrida principal — alias para hybrid_rank.

        Mantém compatibilidade com a API esperada pelo sistema.
        """
        return self.hybrid_rank(query, top_k=top_k)

    def warm_up(self) -> None:
        """Pré-aquece o modelo de embeddings com uma query de teste."""
        try:
            _ = self.embed_query("warmup")
            logger.info("Modelo de embeddings pré-aquecido com sucesso.")
        except Exception as e:
            logger.warning("Falha no warm-up do modelo: %s", e)

    def get_candidates_count(self) -> int:
        """Retorna o número de candidatos (embeddings) disponíveis."""
        return len(self.embeddings)

    # ------------------------------------------------------------------
    # UTILIDADES
    # ------------------------------------------------------------------

    def get_cell_details(self, uid: str) -> dict[str, Any] | None:
        """Retorna todos os metadados de uma célula N4."""
        return self.registry.get(uid)

    def get_neighbors(
        self, uid: str, relation_type: str | None = None, depth: int = 1
    ) -> list[dict]:
        """Retorna vizinhos de uma célula no grafo."""
        return self.graph.query_neighbors(uid, relation_type, depth)

    def health_check(self) -> dict[str, Any]:
        """Verifica integridade do retriever."""
        return {
            "embeddings_loaded": len(self.embeddings),
            "registry_size": len(self.registry),
            "graph_nodes": self.graph.G.number_of_nodes(),
            "graph_edges": self.graph.G.number_of_edges(),
            "threshold": self.threshold,
            "weights": self.weights,
            "embedding_dim": self.embedding_dim,
        }
#!/usr/bin/env python3
"""Retriever Híbrido para Busca Ontológica Multimodal.

Combina três fontes de recuperação:
1. Similaridade vetorial (embeddings semânticos)
2. Navegação por grafo ontológico (hierarquia + relações)
3. Filtragem simbólica (tags, natureza, correspondência exata)

O pipeline de reranking combina os scores das três fontes com pesos
configuráveis, aplicando expansão de grafo e filtragem simbólica
sobre os candidatos iniciais.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """Representa um resultado de retrieval com score e metadados."""
    uid: str
    score: float
    conceito: str = ""
    path: str = ""
    pilar: str = ""
    dominio: str = ""
    natureza: str = ""
    n3_name: str = ""
    axis: str = ""
    semantic_sim: float = 0.0
    graph_score: float = 0.0
    symbolic_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "score": round(self.score, 4),
            "conceito": self.conceito,
            "path": self.path,
            "pilar": self.pilar,
            "dominio": self.dominio,
            "natureza": self.natureza,
            "n3_name": self.n3_name,
            "axis": self.axis,
            "semantic_sim": round(self.semantic_sim, 4),
            "graph_score": round(self.graph_score, 4),
            "symbolic_score": round(self.symbolic_score, 4),
        }


@dataclass
class HybridRetrieverConfig:
    """Configuração do retriever híbrido."""
    # Thresholds
    min_semantic_similarity: float = 0.65
    min_final_score: float = 0.40
    high_confidence_threshold: float = 0.85

    # Top-K limits
    top_k_semantic: int = 50
    top_k_graph: int = 50
    top_k_final: int = 12

    # Graph expansion
    graph_depth: int = 3
    graph_weight: float = 0.30

    # Fusion weights (must sum to 1.0)
    weight_semantic: float = 0.50
    weight_graph: float = 0.30
    weight_symbolic: float = 0.20

    # Symbolic boost
    tag_match_boost: float = 0.20
    nature_match_boost: float = 0.10
    max_symbolic_boost: float = 1.5

    # Query expansion
    expand_query: bool = True
    max_expansion_terms: int = 5

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "HybridRetrieverConfig":
        """Carrega configuração de arquivo YAML."""
        try:
            import yaml
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except ImportError:
            data = {}

        if not data:
            return cls()

        fusao = data.get("fusao", {})
        vetorial = data.get("vetorial", {})
        grafico = data.get("grafico", {})
        simbolico = data.get("simbolico", {})

        pesos = fusao.get("pesos", {})

        return cls(
            min_semantic_similarity=vetorial.get("limiar_minimo", 0.65),
            high_confidence_threshold=vetorial.get("limiar_alta_confianca", 0.85),
            top_k_semantic=vetorial.get("top_k", 50),
            graph_depth=grafico.get("profundidade_max", 3),
            min_final_score=fusao.get("limiar_final", 0.40),
            weight_semantic=pesos.get("vetorial", 0.50),
            weight_graph=pesos.get("grafico", 0.30),
            weight_symbolic=pesos.get("simbolico", 0.20),
            expand_query=vetorial.get("expandir_query", True),
            max_expansion_terms=vetorial.get("expansao_max", 5),
        )


class HybridRetriever:
    """Retriever híbrido que combina busca vetorial, navegação por grafo
    e filtragem simbólica para recuperação de conceitos ontológicos N4.

    Pipeline:
    1. Query → embedding → top-K candidatos (similaridade vetorial)
    2. Expansão via grafo (vizinhos, relações, hierarquia)
    3. Filtragem simbólica (tags, natureza, correspondência)
    4. Re-ranking por score combinado ponderado
    """

    def __init__(
        self,
        embedding_dir: str = "data/embeddings",
        graph_engine=None,
        registry: Optional[dict] = None,
        config_path: str = "config/retrieval.yaml",
    ):
        """Inicializa o retriever híbrido.

        Args:
            embedding_dir: Diretório com arquivos .npy de embeddings.
            graph_engine: Instância do OntologyGraph (opcional).
            registry: Dicionário de registro de células (opcional).
            config_path: Caminho para config YAML.
        """
        self.config = HybridRetrieverConfig.from_yaml(config_path)
        self.embedding_dir = Path(embedding_dir)
        self.graph = graph_engine
        self.registry = registry or self._load_registry()
        self.embeddings = self._load_embeddings()
        self._model = None  # Lazy loading

        logger.info(
            f"HybridRetriever inicializado: {len(self.embeddings)} embeddings, "
            f"{len(self.registry)} registros"
        )

    def _load_registry(self) -> dict:
        """Carrega registry a partir dos JSONs se não fornecido externamente."""
        registry = {}
        json_dir = Path("data/json")
        if json_dir.exists():
            for f in sorted(json_dir.glob("N4_*.json")):
                with open(f, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    uid = data.get("uid", f.stem)
                    registry[uid] = data
        return registry

    def _load_embeddings(self) -> dict[str, np.ndarray]:
        """Carrega embeddings do disco (.npy)."""
        embeddings = {}
        if not self.embedding_dir.exists():
            logger.warning(f"Diretório de embeddings não encontrado: {self.embedding_dir}")
            return embeddings

        for f in self.embedding_dir.glob("N4_*.npy"):
            uid = f.stem
            try:
                emb = np.load(f)
                # Garantir float32 e normalização
                emb = emb.astype(np.float32)
                norm = np.linalg.norm(emb)
                if norm > 1e-8:
                    emb = emb / norm
                embeddings[uid] = emb
            except Exception as e:
                logger.warning(f"Erro ao carregar embedding {f}: {e}")

        logger.info(f"Carregados {len(embeddings)} embeddings de {self.embedding_dir}")
        return embeddings

    @property
    def model(self) -> SentenceTransformer:
        """Lazy loading do modelo de sentence-transformers."""
        if self._model is None:
            self._model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return self._model

    def embed_query(self, query: str) -> np.ndarray:
        """Gera embedding para uma query de busca.

        Args:
            query: Texto da consulta.

        Returns:
            Vetor de embedding normalizado (L2), dtype float32.
        """
        vector = self.model.encode(
            query, normalize_embeddings=True, convert_to_numpy=True
        )
        return vector.astype(np.float32)

    # ------------------------------------------------------------------
    # Busca Vetorial (Similaridade Semântica)
    # ------------------------------------------------------------------

    def retrieve_semantic(
        self, query_embedding: np.ndarray, top_k: int = None
    ) -> list[tuple[str, float]]:
        """Busca por similaridade vetorial (coseno).

        Args:
            query_embedding: Embedding da query (normalizado).
            top_k: Número máximo de resultados (usa config se None).

        Returns:
            Lista de (uid, score) ordenada por relevância decrescente.
        """
        if top_k is None:
            top_k = self.config.top_k_semantic

        if not self.embeddings:
            return []

        similarities = {}
        all_embeddings = np.stack(list(self.embeddings.values()))
        all_uids = list(self.embeddings.keys())

        # Calcular similaridade em batch
        sim_matrix = cosine_similarity(
            query_embedding.reshape(1, -1), all_embeddings
        )[0]

        for i, uid in enumerate(all_uids):
            sim = float(sim_matrix[i])
            if sim >= self.config.min_semantic_similarity:
                similarities[uid] = sim

        return sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]

    # ------------------------------------------------------------------
    # Busca por Grafo (Navegação Hierárquica e Relacional)
    # ------------------------------------------------------------------

    def retrieve_structural(self, query_path: str, depth: int = 2) -> list[tuple[str, float]]:
        """Busca por navegação hierárquica no grafo ontológico.

        Encontra células que compartilham caminho hierárquico com a query.

        Args:
            query_path: Caminho ontológico (ex: "S1.L1.1.1").
            depth: Profundidade de navegação.

        Returns:
            Lista de (uid, score) ordenada por proximidade hierárquica.
        """
        results = []
        path_parts = query_path.split(".")

        for uid, data in self.registry.items():
            cell_path = data.get("path", "")
            cell_parts = cell_path.split(".")
            score = 0.0

            # Mesmo eixo (primeiro segmento)
            if path_parts and cell_parts and path_parts[0] == cell_parts[0]:
                score = 0.9
                # Mesmo pilar (segundo segmento)
                if len(path_parts) > 1 and len(cell_parts) > 1 and path_parts[1] == cell_parts[1]:
                    score = 0.95
                    # Mesmo domínio (terceiro segmento)
                    if len(path_parts) > 2 and len(cell_parts) > 2 and path_parts[2] == cell_parts[2]:
                        score = 1.0

            if score > 0:
                results.append((uid, score))

        return sorted(results, key=lambda x: x[1], reverse=True)[:self.config.top_k_graph]

    def _graph_expansion(self, candidates: list[tuple[str, float]], depth: int = None) -> dict[str, float]:
        """Expande candidatos via navegação no grafo ontológico.

        Para cada candidato inicial, explora vizinhos no grafo (relações,
        hierarquia, oposição) e atribui scores proporcionais ao peso
        da aresta e à relevância original.

        Args:
            candidates: Lista de (uid, score) candidatos iniciais.
            depth: Profundidade máxima de expansão.

        Returns:
            Dicionário {uid: score_expandido}.
        """
        if depth is None:
            depth = self.config.graph_depth

        expanded: dict[str, float] = {}

        if not self.graph:
            # Sem grafo, retornar apenas candidatos originais
            return {uid: score for uid, score in candidates}

        for uid, base_score in candidates:
            # Manter o candidato original
            if uid not in expanded or base_score > expanded[uid]:
                expanded[uid] = base_score

            # Buscar vizinhos no grafo
            try:
                neighbors = self.graph.query_neighbors(uid, depth=depth)
                for neighbor in neighbors:
                    n_uid = neighbor.get("target", "")
                    edge_weight = abs(neighbor.get("peso", 0))

                    if not n_uid or n_uid not in self.registry:
                        continue

                    # Score de expansão: score_base × peso_aresta × fator_atenuação
                    expansion_score = base_score * edge_weight * 0.5

                    if n_uid not in expanded or expansion_score > expanded[n_uid]:
                        expanded[n_uid] = expansion_score
            except Exception as e:
                logger.debug(f"Erro na expansão de grafo para {uid}: {e}")

        return expanded

    # ------------------------------------------------------------------
    # Filtragem Simbólica (Tags, Natureza, Correspondência)
    # ------------------------------------------------------------------

    def retrieve_symbolic(
        self, tags: list[str], nature: str = None
    ) -> list[tuple[str, float]]:
        """Busca por filtro simbólico e taxonômico.

        Avalia correspondência de tags, natureza e atributos simbólicos
        das células com os termos da query.

        Args:
            tags: Lista de tags/conceitos para correspondência.
            nature: Natureza para filtragem (ex: "processo", "mecanismo").

        Returns:
            Lista de (uid, score) ordenada por correspondência.
        """
        results = []
        query_tags_lower = [t.lower() for t in tags]

        for uid, data in self.registry.items():
            score = 0.0

            # Verificar tags da célula
            cell_tags = data.get("tags", [])
            cell_tags_lower = [t.lower() for t in cell_tags]
            for tag in query_tags_lower:
                if tag in cell_tags_lower:
                    score += self.config.tag_match_boost

            # Verificar correspondência parcial (fuzzy simples)
            if score == 0 and query_tags_lower:
                for tag in query_tags_lower:
                    for cell_tag in cell_tags_lower:
                        if tag in cell_tag or cell_tag in tag:
                            score += self.config.tag_match_boost * 0.5
                            break

            # Verificar natureza
            if nature and data.get("natureza") == nature:
                score += self.config.nature_match_boost

            # Verificar nome e conceito
            nome = data.get("nome", "").lower()
            nome_normalizado = data.get("nome_normalizado", "").lower()
            for tag in query_tags_lower:
                if tag in nome or tag in nome_normalizado:
                    score += self.config.tag_match_boost * 0.8

            if score > 0:
                results.append((uid, min(score, self.config.max_symbolic_boost)))

        return sorted(results, key=lambda x: x[1], reverse=True)[:self.config.top_k_graph]

    def _symbolic_filter(self, candidates: dict[str, float], query_concepts: list[str]) -> dict[str, float]:
        """Aplica boost simbólico a candidatos baseado em tags e natureza.

        Args:
            candidates: Dicionário {uid: score} de candidatos.
            query_concepts: Lista de conceitos extraídos da query.

        Returns:
            Dicionário {uid: score_ajustado} com boost simbólico aplicado.
        """
        if not query_concepts:
            return candidates

        filtered = {}
        query_lower = [c.lower() for c in query_concepts]

        for uid, score in candidates.items():
            data = self.registry.get(uid, {})
            boost = 1.0

            # Verificar tags
            cell_tags = data.get("tags", [])
            cell_tags_lower = [t.lower() for t in cell_tags]
            for concept in query_lower:
                if concept in cell_tags_lower:
                    boost += self.config.tag_match_boost
                # Correspondência parcial
                for cell_tag in cell_tags_lower:
                    if concept in cell_tag or cell_tag in concept:
                        boost += self.config.tag_match_boost * 0.5
                        break

            # Verificar natureza
            if data.get("natureza") in query_lower:
                boost += self.config.nature_match_boost

            # Verificar nome
            nome = data.get("nome", "").lower()
            nome_normalizado = data.get("nome_normalizado", "").lower()
            for concept in query_lower:
                if concept in nome or concept in nome_normalizado:
                    boost += self.config.tag_match_boost * 0.8

            filtered[uid] = score * min(boost, self.config.max_symbolic_boost)

        return filtered

    # ------------------------------------------------------------------
    # Pipeline de Retrieval Híbrido
    # ------------------------------------------------------------------

    def hybrid_rank(self, query: str, top_k: int = None) -> list[RetrievalResult]:
        """Pipeline completo de retrieval híbrido.

        Etapas:
        1. Gera embedding da query
        2. Busca vetorial → top-K candidatos
        3. Expansão via grafo → vizinhos dos candidatos
        4. Filtragem simbólica → boost por tags/natureza
        5. Fusão de scores (pesos configuráveis)
        6. Re-ranking final

        Args:
            query: Texto da consulta.
            top_k: Número de resultados (usa config se None).

        Returns:
            Lista de RetrievalResult ordenados por score.
        """
        if top_k is None:
            top_k = self.config.top_k_final

        start_time = time.time()

        # 1. Geração do embedding da query
        query_emb = self.embed_query(query)

        # 2. Busca vetorial (candidatos iniciais)
        semantic_results = self.retrieve_semantic(query_emb)

        if not semantic_results:
            logger.info("Nenhum resultado semântico encontrado")
            return []

        # 3. Expansão via grafo
        expanded = self._graph_expansion(semantic_results)

        # 4. Extrair conceitos da query para filtragem simbólica
        query_concepts = self._extract_query_concepts(query)

        # 5. Filtragem simbólica (boost)
        filtered = self._symbolic_filter(expanded, query_concepts)

        # 6. Fusão de scores
        results = self._fuse_scores(semantic_results, expanded, filtered, top_k)

        elapsed = time.time() - start_time
        logger.info(f"Retrieval híbrido: {len(results)} resultados em {elapsed:.3f}s")

        return results

    def _fuse_scores(
        self,
        semantic_results: list[tuple[str, float]],
        expanded: dict[str, float],
        filtered: dict[str, float],
        top_k: int,
    ) -> list[RetrievalResult]:
        """Fusa scores das três fontes com pesos configuráveis.

        Score final = (w_semantic × sim_semantic) + (w_graph × sim_graph) + (w_symbolic × sim_symbolic)

        Args:
            semantic_results: Resultados da busca vetorial.
            expanded: Scores expandidos via grafo.
            filtered: Scores após filtragem simbólica.
            top_k: Número de resultados finais.

        Returns:
            Lista de RetrievalResult com scores fusing.
        """
        w_sem = self.config.weight_semantic
        w_graph = self.config.weight_graph
        w_sym = self.config.weight_symbolic

        # Normalizar pesos
        total_w = w_sem + w_graph + w_sym
        if total_w > 0:
            w_sem /= total_w
            w_graph /= total_w
            w_sym /= total_w

        # Converter resultados semânticos para dict
        semantic_dict = dict(semantic_results)

        # Coletar todos os UIDs candidatos
        all_uids = set(semantic_dict.keys()) | set(expanded.keys()) | set(filtered.keys())

        fused_results = []
        for uid in all_uids:
            sem_score = semantic_dict.get(uid, 0.0)
            graph_score = expanded.get(uid, 0.0)
            sym_score = filtered.get(uid, 0.0)

            # Normalizar scores para [0, 1] range antes da fusão
            norm_sem = sem_score
            norm_graph = graph_score  # Já está em escala razoável
            norm_sym = sym_score / self.config.max_symbolic_boost if self.config.max_symbolic_boost > 0 else sym_score

            final_score = (w_sem * norm_sem) + (w_graph * norm_graph) + (w_sym * norm_sym)

            if final_score >= self.config.min_final_score:
                data = self.registry.get(uid, {})
                result = RetrievalResult(
                    uid=uid,
                    score=final_score,
                    conceito=data.get("nome", ""),
                    path=data.get("path", ""),
                    pilar=data.get("pilar", ""),
                    dominio=data.get("dominio", ""),
                    natureza=data.get("natureza", ""),
                    n3_name=data.get("n3_name", ""),
                    axis=data.get("axis", ""),
                    semantic_sim=sem_score,
                    graph_score=graph_score,
                    symbolic_score=sym_score,
                )
                fused_results.append(result)

        # Ordenar por score final
        fused_results.sort(key=lambda x: x.score, reverse=True)
        return fused_results[:top_k]

    def _extract_query_concepts(self, query: str) -> list[str]:
        """Extrai conceitos-chave da query para filtragem simbólica.

        Args:
            query: Texto da consulta.

        Returns:
            Lista de conceitos (palavras significativas em minúsculas).
        """
        # Stopwords básicas em português e inglês
        stopwords = {
            "a", "o", "e", "é", "de", "do", "da", "em", "no", "na", "para",
            "por", "com", "um", "uma", "que", "como", "se", "não", "mais",
            "mas", "ou", "ao", "os", "as", "dos", "das", "sobre", "entre",
            "the", "a", "an", "is", "are", "was", "were", "in", "on", "at",
            "to", "for", "of", "with", "and", "or", "but", "not", "from",
            "this", "that", "it", "its",
        }

        # Tokenização simples
        words = query.lower().replace(".", " ").replace(",", " ").split()
        concepts = [w for w in words if len(w) > 2 and w not in stopwords]
        return concepts

    # ------------------------------------------------------------------
    # Métodos de conveniência
    # ------------------------------------------------------------------

    def search(self, query: str, top_k: int = 12) -> list[dict]:
        """Interface simplificada para busca.

        Args:
            query: Texto da consulta.
            top_k: Número de resultados.

        Returns:
            Lista de dicionários com uid, score, conceito, path, etc.
        """
        results = self.hybrid_rank(query, top_k=top_k)
        return [r.to_dict() for r in results]

    def get_candidates_count(self) -> int:
        """Retorna o número total de candidatos indexados."""
        return len(self.embeddings)

    def warm_up(self):
        """Pré-carrega o modelo de embedding para reduzir latência na primeira query."""
        _ = self.model.encode("warm-up", normalize_embeddings=True)
        logger.info("Modelo de embedding pré-carregado")
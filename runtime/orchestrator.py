"""
ORCHESTRATOR — Pipeline E2E do Sistema Cognitivo Ontológico.

Integra todos os módulos da FASE 6 em um fluxo unificado:

INPUT → CLASSIFIER → ROUTER → RETRIEVER → SYNTHESIZER → VALIDATOR → OUTPUT

Fase 6d do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "core"))

from core.ontology_graph import OntologyGraph

from runtime.classifier import OntologicalClassifier
from runtime.router import CognitiveRouter, RoutingDecision
from runtime.retriever import HybridRetriever
from runtime.synthesizer import OntologySynthesizer, SynthesisInput
from runtime.validator import OntologyValidator, ValidationReport

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuração do pipeline E2E."""
    json_dir: str = "data/json"
    embeddings_dir: str = "data/embeddings"
    graph_dir: str = "data/graphs"
    config_dir: str = "config"
    index_path: str = "data/json/ontology_index.json"

    # Thresholds
    retrieval_threshold: float = 0.15
    semantic_threshold: float = 0.72
    graph_depth: int = 3
    rerank_limit: int = 12
    validation_threshold: float = 0.6

    # Pesos de fusão
    fusion_weights: Dict[str, float] = field(default_factory=lambda: {
        "vetorial": 0.50,
        "grafico": 0.30,
        "simbolico": 0.20,
    })


@dataclass
class PipelineResult:
    """Resultado completo do pipeline cognitivo."""
    query: str
    classification: dict
    routing: dict
    retrieved_cells: List[dict]
    graph_context: Optional[dict]
    synthesis: Optional[Any]
    validation: Optional[dict]
    latency_ms: float
    status: str  # "success", "partial", "failed"
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "status": self.status,
            "latency_ms": round(self.latency_ms, 2),
            "classification": self.classification,
            "routing": self.routing,
            "retrieved_cells": self.retrieved_cells,
            "graph_context": self.graph_context,
            "synthesis": {
                "prompt": self.synthesis.prompt if self.synthesis else None,
                "context_summary": str(self.synthesis.context_summary) if self.synthesis else None,
                "cell_references": self.synthesis.cell_references if self.synthesis else [],
                "metadata": self.synthesis.metadata if self.synthesis else {},
            } if self.synthesis else None,
            "validation": self.validation if self.validation else None,
            "metadata": self.metadata,
        }

    @property
    def formatted_output(self) -> str:
        """Extrai o prompt formatado do resultado da síntese."""
        if self.synthesis and self.synthesis.prompt:
            return self.synthesis.prompt
        return "[Sem output formatado]"

    def summary(self) -> str:
        """Sumário legível do resultado."""
        lines = [
            f"{'='*60}",
            f"PIPELINE COGNITIVO — RESULTADO",
            f"{'='*60}",
            f"Query: {self.query}",
            f"Status: {self.status.upper()}",
            f"Latência: {self.latency_ms:.0f}ms",
            f"",
            f"Classificação:",
            f"  Eixo: {self.classification.get('classificacao', {}).get('n0_eixo', {}).get('eixo', 'N/A')}",
            f"  Pilar: {self.classification.get('classificacao', {}).get('n1_pilar', {}).get('pilar', 'N/A')}",
            f"  Domínio: {self.classification.get('classificacao', {}).get('n2_dominio', {}).get('dominio', 'N/A')}",
            f"",
            f"Roteamento:",
            f"  Estratégia: {self.routing.get('estrategia', 'N/A')}",
            f"  Score: {self.routing.get('score', 0):.4f}",
            f"",
            f"Retrieval: {len(self.retrieved_cells)} células recuperadas",
            f"Síntese: {'Gerada' if self.synthesis else 'N/A'}",
            f"Validação: {'Aprovado' if self.validation and self.validation.get('valido') else 'Reprovado' if self.validation else 'N/A'}",
            f"{'='*60}",
        ]
        return "\n".join(lines)


class OntologyOrchestrator:
    """
    Orchestrator Cognitivo — Pipeline E2E do Sistema Ontológico.

    Integra:
    1. Classificador Ontológico (N0→N4)
    2. Router Cognitivo (seleção de estratégia por pilar)
    3. Retrieval Híbrido (vetorial + grafo + simbólico)
    4. Engine de Síntese (montagem de prompts dinâmicos)
    5. Validador Ontológico (verificações de coerência)

    Opcionalmente utiliza:
    - Grafo semântico (NetworkX) para expansão de contexto
    - Embeddings para busca vetorial
    """

    def __init__(
        self,
        config: Optional[PipelineConfig] = None,
        classifier: Optional[OntologicalClassifier] = None,
        router: Optional[CognitiveRouter] = None,
        retriever: Optional[HybridRetriever] = None,
        synthesizer: Optional[OntologySynthesizer] = None,
        validator: Optional[OntologyValidator] = None,
        graph: Optional[OntologyGraph] = None,
    ):
        self.config = config or PipelineConfig()

        # Inicializar grafo PRIMEIRO — componentes dependem dele
        self.graph = graph or self._init_graph()

        # Inicializar componentes restantes (com fallback para instâncias default)
        self.classifier = classifier or self._init_classifier()
        self.router = router or self._init_router()
        self.retriever = retriever or self._init_retriever(self.graph)
        self.synthesizer = synthesizer or self._init_synthesizer()
        self.validator = validator or self._init_validator()

        # Warm-up do modelo de embeddings
        self._warm_up()

        logger.info("OntologyOrchestrator inicializado com sucesso.")

    def _init_classifier(self) -> OntologicalClassifier:
        """Inicializa o classificador ontológico."""
        try:
            clf = OntologicalClassifier()
            # Warm-up da classificação
            _ = clf.classify("teste")
            return clf
        except Exception as e:
            logger.warning("Falha ao inicializar classificador: %s", e)
            raise

    def _init_router(self) -> CognitiveRouter:
        """Inicializa o router cognitivo."""
        return CognitiveRouter(
            config_path=str(Path(self.config.config_dir) / "retrieval.yaml")
        )

    def _init_retriever(self, graph: OntologyGraph) -> HybridRetriever:
        """Inicializa o retriever híbrido, reutilizando o grafo compartilhado."""
        try:
            retriever = HybridRetriever(
                embedding_dir=self.config.embeddings_dir,
                json_dir=self.config.json_dir,
                graph_engine=graph,
                config_path=str(Path(self.config.config_dir) / "retrieval.yaml"),
            )
            return retriever
        except Exception as e:
            logger.warning("Falha ao inicializar retriever: %s", e)
            raise

    def _init_synthesizer(self) -> OntologySynthesizer:
        """Inicializa a engine de síntese."""
        return OntologySynthesizer(
            json_dir=self.config.json_dir,
            index_path=self.config.index_path,
        )

    def _init_validator(self) -> OntologyValidator:
        """Inicializa o validador ontológico."""
        return OntologyValidator(
            json_dir=self.config.json_dir,
            index_path=self.config.index_path,
        )

    def _init_graph(self) -> OntologyGraph:
        """Inicializa o grafo ontológico."""
        graph = OntologyGraph(json_dir=self.config.json_dir)
        graph.load_registry()
        graph.build_graph()
        return graph

    def _warm_up(self) -> None:
        """Pré-aquece os modelos para reduzir latência na primeira query."""
        try:
            self.retriever.warm_up()
            logger.info("Warm-up concluído.")
        except Exception as e:
            logger.warning("Falha no warm-up: %s", e)

    def process(
        self,
        query: str,
        return_full: bool = True,
    ) -> PipelineResult:
        """
        Executa o pipeline cognitivo completo.

        Fluxo:
        1. Classificação N0→N4
        2. Roteamento cognitivo (seleção de estratégia)
        3. Retrieval híbrido (busca de células relevantes)
        4. Expansão via grafo (vizinhança ontológica)
        5. Síntese (montagem do prompt/resposta)
        6. Validação (verificação de coerência)

        Args:
            query: Pergunta ou instrução do usuário
            return_full: Se True, retorna todos os dados; se False, retorna sumário

        Returns:
            PipelineResult com todos os resultados intermediários
        """
        t0 = time.time()
        status = "success"

        # ── PASSO 1: Classificação ──
        try:
            raw_classification = self.classifier.classify(query)
            # FullClassification → dict (cast explícito para type-checkers)
            classification: dict = cast(dict, raw_classification.to_dict())
            logger.info(
                "Classificação: eixo=%s, pilar=%s, dominio=%s",
                classification.get("classificacao", {}).get("n0_eixo", {}).get("eixo"),
                classification.get("classificacao", {}).get("n1_pilar", {}).get("pilar"),
                classification.get("classificacao", {}).get("n2_dominio", {}).get("dominio"),
            )
        except Exception as e:
            logger.error("Falha na classificação: %s", e)
            classification = {"error": str(e)}
            status = "failed"

        # ── PASSO 2: Roteamento ──
        try:
            routing = self.router.route(classification, query)
            routing_dict = routing.to_dict()
            logger.info(
                "Roteamento: pilar=%s, estrategia=%s, score=%.4f",
                routing.pilar, routing.estrategia, routing.score,
            )
        except Exception as e:
            logger.error("Falha no roteamento: %s", e)
            routing_dict = {"error": str(e)}
            status = "failed" if status != "failed" else status

        # ── PASSO 3: Retrieval Híbrido ──
        retrieved_cells = []
        graph_context = None
        try:
            # Busca vetorial + grafo
            retrieved_cells = self.retriever.hybrid_rank(
                query,
                top_k=self.config.rerank_limit,
            )
            logger.info("Retrieval: %d células recuperadas", len(retrieved_cells))

            # Expansão via grafo para as top células
            if retrieved_cells:
                seed_uids = [r["uid"] for r in retrieved_cells[:5]]
                neighbors = self.graph.query_neighbors_multi(
                    seed_uids, depth=self.config.graph_depth
                )
                graph_context = {
                    "seeds": seed_uids,
                    "neighbors": neighbors,
                    "depth": self.config.graph_depth,
                }
        except Exception as e:
            logger.error("Falha no retrieval: %s", e)
            if status == "success":
                status = "partial"

        # ── PASSO 4: Síntese ──
        synthesis = None
        try:
            synthesis_input = SynthesisInput(
                query=query,
                routing_decision=routing_dict,
                retrieved_cells=retrieved_cells,
                graph_context=graph_context,
                classification=classification,
            )
            synthesis = self.synthesizer.synthesize(synthesis_input)
            logger.info(
                "Síntese: prompt gerado com %d referências",
                len(synthesis.cell_references),
            )
        except Exception as e:
            logger.error("Falha na síntese: %s", e)
            if status == "success":
                status = "partial"

        # ── PASSO 5: Validação ──
        validation = None
        try:
            validation_context = {
                "cell_references": (
                    synthesis.cell_references if synthesis else []
                ),
            }
            validation = self.validator.validate(
                routing_dict,
                validation_context,
                retrieved_cells=retrieved_cells,
            )
            logger.info(
                "Validação: %s (score=%.4f)",
                "APROVADO" if validation.valido else "REJEITADO",
                validation.score_geral,
            )
        except Exception as e:
            logger.error("Falha na validação: %s", e)
            if status == "success":
                status = "partial"

        # Calcular latência total
        latency_ms = (time.time() - t0) * 1000

        # Se validação reprovou, ajustar status
        if validation and not validation.valido and status == "success":
            status = "validated_with_warnings"

        return PipelineResult(
            query=query,
            classification=classification,
            routing=routing_dict,
            retrieved_cells=retrieved_cells,
            graph_context=graph_context,
            synthesis=synthesis,
            validation=validation.to_dict() if validation else None,
            latency_ms=latency_ms,
            status=status,
            metadata={
                "classifier_latency_ms": classification.get("_latency_ms", 0)
                if isinstance(classification, dict)
                else 0,
                "retrieval_count": len(retrieved_cells),
                "synthesis_refs": len(synthesis.cell_references) if synthesis else 0,
                "validation_score": validation.score_geral if validation else 0,
                "config": {
                    "threshold": self.config.retrieval_threshold,
                    "graph_depth": self.config.graph_depth,
                    "rerank_limit": self.config.rerank_limit,
                },
            },
        )

    def process_simple(
        self,
        query: str,
    ) -> PipelineResult:
        """
        Versão simplificada do pipeline — sem classificador completo.
        Usa apenas sinais linguísticos para roteamento.

        Útil para testes rápidos e cenários de baixa latência.
        """
        t0 = time.time()

        # Roteamento simplificado
        routing = self.router.route_simple(query)
        routing_dict = routing.to_dict()

        # Retrieval
        retrieved_cells = self.retriever.hybrid_rank(
            query, top_k=self.config.rerank_limit
        )

        # Síntese
        synthesis_input = SynthesisInput(
            query=query,
            routing_decision=routing_dict,
            retrieved_cells=retrieved_cells,
        )
        synthesis = self.synthesizer.synthesize(synthesis_input)

        # Validação
        validation_context = {
            "cell_references": synthesis.cell_references if synthesis else []
        }
        validation = self.validator.validate(
            routing_dict, validation_context, retrieved_cells=retrieved_cells
        )

        latency_ms = (time.time() - t0) * 1000

        return PipelineResult(
            query=query,
            classification={},
            routing=routing_dict,
            retrieved_cells=retrieved_cells,
            graph_context=None,
            synthesis=synthesis,
            validation=validation.to_dict() if validation else None,
            latency_ms=latency_ms,
            status="success",
            metadata={"mode": "simple"},
        )

    def health_check(self) -> dict:
        """Verifica integridade de todos os componentes do pipeline."""
        checks = {}

        # Classificador
        try:
            _ = self.classifier.classify("teste rápido")
            checks["classifier"] = {"status": "ok"}
        except Exception as e:
            checks["classifier"] = {"status": "error", "detail": str(e)}

        # Retriever
        try:
            health = self.retriever.health_check()
            checks["retriever"] = {"status": "ok", **health}
        except Exception as e:
            checks["retriever"] = {"status": "error", "detail": str(e)}

        # Grafo
        try:
            checks["graph"] = {
                "status": "ok",
                "nodes": self.graph.G.number_of_nodes(),
                "edges": self.graph.G.number_of_edges(),
            }
        except Exception as e:
            checks["graph"] = {"status": "error", "detail": str(e)}

        # Registry do synthesizer
        try:
            checks["synthesizer"] = {
                "status": "ok",
                "registry_size": len(self.synthesizer.registry),
            }
        except Exception as e:
            checks["synthesizer"] = {"status": "error", "detail": str(e)}

        # Validator
        try:
            checks["validator"] = {
                "status": "ok",
                "registry_size": len(self.validator.registry),
            }
        except Exception as e:
            checks["validator"] = {"status": "error", "detail": str(e)}

        overall = all(
            c.get("status") == "ok" for c in checks.values()
        )
        return {
            "status": "healthy" if overall else "degraded",
            "checks": checks,
        }

    def get_pipeline_stats(self) -> dict:
        """Retorna estatísticas do pipeline."""
        return {
            "components": [
                "classifier",
                "router",
                "retriever",
                "synthesizer",
                "validator",
                "graph",
            ],
            "config": {
                "json_dir": self.config.json_dir,
                "embeddings_dir": self.config.embeddings_dir,
                "retrieval_threshold": self.config.retrieval_threshold,
                "semantic_threshold": self.config.semantic_threshold,
                "graph_depth": self.config.graph_depth,
                "rerank_limit": self.config.rerank_limit,
            },
            "registry_sizes": {
                "classifier_labels": len(self.classifier.registry)
                if hasattr(self.classifier, "registry")
                else 0,
                "retriever_embeddings": self.retriever.get_candidates_count(),
                "synthesizer_cells": len(self.synthesizer.registry),
                "validator_cells": len(self.validator.registry),
                "graph_nodes": self.graph.G.number_of_nodes(),
                "graph_edges": self.graph.G.number_of_edges(),
            },
        }


# ── Router import (para referência cruzada) ─────────────────────────

# Import necessário para type hints — definido acima no módulo router
# from runtime.router import CognitiveRouter, RoutingDecision


# ── Ponto de entrada para testes ────────────────────────────────────

if __name__ == "__main__":
    print("Inicializando OntologyOrchestrator...")
    orchestrator = OntologyOrchestrator()

    # Health check
    health = orchestrator.health_check()
    print(f"\nHealth Check: {health['status']}")
    for comp, info in health["checks"].items():
        status = info.get("status", "unknown")
        detail = info.get("detail", "")
        print(f"  {comp}: {status}" + (f" ({detail})" if detail else ""))

    # Teste com query
    print("\n" + "=" * 60)
    test_query = "Como decompor um problema complexo em partes menores?"
    print(f"Query: {test_query}")
    print("=" * 60)

    result = orchestrator.process(test_query)
    print(result.summary())

    # Mostrar prompt gerado (primeiros 300 chars)
    if result.synthesis:
        print(f"\nPrompt gerado ({len(result.synthesis.prompt)} chars):")
        print("-" * 40)
        print(result.synthesis.prompt[:500])
        print("...")

    # Stats
    print("\n" + "=" * 60)
    stats = orchestrator.get_pipeline_stats()
    print("Pipeline Stats:")
    for section, data in stats.items():
        if isinstance(data, dict):
            for k, v in data.items():
                print(f"  {section}.{k}: {v}")
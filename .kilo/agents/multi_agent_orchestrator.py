#!/usr/bin/env python3
"""
MULTI-AGENT ORCHESTRATOR — Coordenação de Agentes Cognitivos.

FASE 7g do Roadmap da Ontologia Fractal.

Integra todos os agentes especializados em um pipeline coerente:
1. ClassifierAgent    → Classificação ontológica N0→N4
2. CognitiveRouter    → Roteamento por pilar/estratégia
3. HybridRetriever    → Busca híbrida vetorial+grafo+simbólico
4. GraphAgent         → Expansão e navegação do grafo
5. DialecticAgent     → Inferência de opostos e tensões dialéticas
6. SynthesisAgent     → Geração de resposta composta
7. ValidatorAgent     → Verificação de coerência ontológica
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

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))
if str(_PROJECT_ROOT / "runtime") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "runtime"))

from core.agent_base import AgentResult
from core.ontology_graph import OntologyGraph

from runtime.classifier import OntologicalClassifier, FullClassification
from runtime.router import CognitiveRouter, RoutingDecision
from runtime.retriever import HybridRetriever
from runtime.synthesizer import OntologySynthesizer, SynthesisInput, SynthesisOutput
from runtime.validator import OntologyValidator, ValidationReport

from .classifier_agent import ClassifierAgent, ClassificationResult
from .graph_agent import GraphAgent, GraphExpansionResult
from .synthesis_agent import SynthesisAgent
from .validator_agent import ValidatorAgent, ValidationVerdict
from .dialectic_agent import DialecticAgent, OppositionResult, DialecticDistance


@dataclass
class PipelineStepResult:
    """Resultado de uma etapa no pipeline multi-agente."""
    step: str
    agent_name: str
    success: bool
    output: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    latency_ms: float = 0.0
    reasoning: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "step": self.step,
            "agent_name": self.agent_name,
            "success": self.success,
            "confidence": round(self.confidence, 4),
            "latency_ms": round(self.latency_ms, 2),
            "reasoning": self.reasoning,
            "errors": self.errors,
            "output_summary": {
                k: (str(v)[:200] if not isinstance(v, (dict, list)) else
                    {kk: vv for kk, vv in v.items()})
                if isinstance(v, dict)
                else v[:20] if isinstance(v, list) else v
                for k, v in self.output.items()
            } if self.output else {},
        }


@dataclass
class MultiAgentPipelineResult:
    """Resultado completo do pipeline multi-agente."""
    query: str
    pipeline_mode: str  # "full", "simple", "custom"
    steps: List[PipelineStepResult] = field(default_factory=list)
    final_output: Dict[str, Any] = field(default_factory=dict)
    total_latency_ms: float = 0.0
    status: str = "success"  # "success", "partial", "failed"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "pipeline_mode": self.pipeline_mode,
            "status": self.status,
            "total_latency_ms": round(self.total_latency_ms, 2),
            "steps": [s.to_dict() for s in self.steps],
            "final_output": self.final_output,
            "metadata": self.metadata,
        }

    def summary(self) -> str:
        """Sumário legível do resultado do pipeline multi-agente."""
        lines = [
            f"{'='*60}",
            f"PIPELINE MULTI-AGENTE — RESULTADO",
            f"{'='*60}",
            f"Query: {self.query}",
            f"Modo: {self.pipeline_mode}",
            f"Status: {self.status.upper()}",
            f"Latência total: {self.total_latency_ms:.0f}ms",
            f"Etapas executadas: {len(self.steps)}",
            f"",
            f"Detalhamento por etapa:",
        ]
        for step in self.steps:
            status_icon = "✓" if step.success else "✗"
            lines.append(
                f"  [{status_icon}] {step.agent_name} "
                f"({step.latency_ms:.0f}ms, confiança={step.confidence:.3f})"
            )
            if step.reasoning:
                for r in step.reasoning[:2]:
                    lines.append(f"      → {r}")
            if step.errors:
                for err in step.errors[:1]:
                    lines.append(f"      ⚠ {err}")

        if self.final_output:
            lines.append(f"")
            lines.append(f"Output final:")
            prompt = self.final_output.get("prompt", "")
            if prompt:
                lines.append(f"  Prompt ({len(prompt)} chars):")
                lines.append(f"  {prompt[:300]}...")

            validation = self.final_output.get("validation")
            if validation:
                aprovado = validation.get("aprovado", "?")
                score = validation.get("score_geral", "?")
                lines.append(f"  Validação: {'Aprovado' if aprovado else 'Reprovado'} "
                             f"(score={score})")

        lines.append(f"{'='*60}")
        return "\n".join(lines)


class MultiAgentOrchestrator:
    """
    Orquestrador Multi-Agente — Coordena o pipeline cognitivo completo.

    Integra agentes especializados em uma cadeia de processamento onde:
    - Cada etapa recebe contexto acumulado das etapas anteriores
    - Falhas são tratadas com degradação graciosa (não bloqueiam o pipeline)
    - O contexto dialético enriquece a síntese com perspectivas opostas

    Pipeline completo (7 etapas):
    1. CLASSIFIER    → ClassifierAgent: classificação ontológica N0→N4
    2. ROUTER        → CognitiveRouter: roteamento por pilar/estratégia
    3. RETRIEVER     → HybridRetriever: busca híbrida vetorial+grafo+simbólico
    4. GRAPH         → GraphAgent: expansão do grafo ontológico
    5. DIALECTIC     → DialecticAgent: inferência de opostos e tensões
    6. SYNTHESIS     → SynthesisAgent: geração de resposta composta
    7. VALIDATOR     → ValidatorAgent: verificação de coerência ontológica

    Pipeline simplificado (4 etapas):
    ROUTER → RETRIEVER → SYNTHESIS → VALIDATOR
    """

    # Nomes de etapas do pipeline
    STEP_CLASSIFIER = "classifier"
    STEP_ROUTER = "router"
    STEP_RETRIEVER = "retriever"
    STEP_GRAPH = "graph"
    STEP_DIALECTIC = "dialectic"
    STEP_SYNTHESIS = "synthesis"
    STEP_VALIDATOR = "validator"

    PIPELINE_FULL = [
        STEP_CLASSIFIER, STEP_ROUTER, STEP_RETRIEVER,
        STEP_GRAPH, STEP_DIALECTIC, STEP_SYNTHESIS, STEP_VALIDATOR,
    ]
    PIPELINE_SIMPLE = [
        STEP_ROUTER, STEP_RETRIEVER, STEP_SYNTHESIS, STEP_VALIDATOR,
    ]

    AGENT_NAME: str = "MultiAgentOrchestrator"
    AGENT_VERSION: str = "1.0.0"

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        classifier_agent: Optional[ClassifierAgent] = None,
        graph_agent: Optional[GraphAgent] = None,
        synthesis_agent: Optional[SynthesisAgent] = None,
        validator_agent: Optional[ValidatorAgent] = None,
        dialectic_agent: Optional[DialecticAgent] = None,
        router: Optional[CognitiveRouter] = None,
        retriever: Optional[HybridRetriever] = None,
        graph: Optional[OntologyGraph] = None,
    ):
        self.config = config or {}
        json_dir = self.config.get("json_dir", "data/json")
        index_path = self.config.get("index_path", "data/json/ontology_index.json")
        embeddings_dir = self.config.get("embeddings_dir", "data/embeddings")
        config_dir = self.config.get("config_dir", "config")

        # Inicializar grafo PRIMEIRO — todos dependem dele
        self.graph = graph or OntologyGraph(json_dir=json_dir)
        if not self.graph.registry:
            self.graph.load_registry()
        self.graph.build_graph()

        # Inicializar agentes (com fallback para instâncias default)
        self.classifier_agent = classifier_agent or ClassifierAgent(
            config={"json_dir": json_dir, "index_path": index_path}
        )
        self.graph_agent = graph_agent or GraphAgent(
            graph=self.graph,
            config={"json_dir": json_dir},
        )
        self.synthesis_agent = synthesis_agent or SynthesisAgent(
            config={"json_dir": json_dir, "index_path": index_path}
        )
        self.validator_agent = validator_agent or ValidatorAgent(
            config={"json_dir": json_dir, "index_path": index_path}
        )
        self.dialectic_agent = dialectic_agent or DialecticAgent(
            config={"json_dir": json_dir}
        )

        # Componentes não-agentes (router + retriever)
        self.router = router or CognitiveRouter(
            config_path=str(Path(config_dir) / "retrieval.yaml")
        )
        self.retriever = retriever or HybridRetriever(
            embedding_dir=embeddings_dir,
            json_dir=json_dir,
            graph_engine=self.graph,
            config_path=str(Path(config_dir) / "retrieval.yaml"),
        )

        # Carregar registry para uso compartilhado
        self._registry = self.graph._node_index

        # Warm-up
        self._warm_up()

        logger.info(
            "%s v%s inicializado: %d nós, %d arestas no grafo",
            self.AGENT_NAME, self.AGENT_VERSION,
            self.graph.G.number_of_nodes(),
            self.graph.G.number_of_edges(),
        )

    # ── Warm-up ─────────────────────────────────────────────────────────

    def _warm_up(self) -> None:
        """Pré-aquece componentes para reduzir latência na primeira query."""
        try:
            self.retriever.warm_up()
        except Exception as e:
            logger.warning("Falha no warm-up do retriever: %s", e)

        # Warm-up do classificador com query de teste
        try:
            _ = self.classifier_agent.execute("teste rápido")
        except Exception as e:
            logger.warning("Falha no warm-up do classificador: %s", e)

    # ── Pipeline Execution ──────────────────────────────────────────────

    def full_pipeline(self, query: str) -> MultiAgentPipelineResult:
        """Executa o pipeline completo com todos os agentes."""
        return self.run_pipeline(query, steps=self.PIPELINE_FULL)

    def simple_pipeline(self, query: str) -> MultiAgentPipelineResult:
        """Executa pipeline simplificado (sem classificador, grafo ou dialético)."""
        return self.run_pipeline(query, steps=self.PIPELINE_SIMPLE)

    def run_pipeline(
        self,
        query: str,
        steps: Optional[List[str]] = None,
    ) -> MultiAgentPipelineResult:
        """
        Executa o pipeline multi-agente com as etapas especificadas.

        Args:
            query: Query ou instrução do usuário.
            steps: Lista de etapas a executar. Se None, usa PIPELINE_FULL.

        Returns:
            MultiAgentPipelineResult com todos os resultados intermediários.
        """
        t0 = time.time()
        steps = steps or self.PIPELINE_FULL
        pipeline_context: Dict[str, Any] = {"query": query}
        step_results: List[PipelineStepResult] = []
        status = "success"

        for step_name in steps:
            step_result = self._run_step(step_name, pipeline_context)
            step_results.append(step_result)

            if step_result.success:
                # Atualizar contexto compartilhado com output da etapa
                self._update_context(step_name, pipeline_context, step_result.output)
                logger.info(
                    "Etapa '%s' concluída: %.0fms, confiança=%.3f",
                    step_name, step_result.latency_ms, step_result.confidence,
                )
            else:
                # Degradação graciosa: registrar erro e continuar
                logger.warning(
                    "Etapa '%s' falhou: %s",
                    step_name, step_result.errors,
                )
                if status == "success":
                    status = "partial"

        # Determinar status final
        critical_steps = {self.STEP_SYNTHESIS}
        critical_failures = [
            s for s in step_results
            if not s.success and s.step in critical_steps
        ]
        if critical_failures:
            status = "failed"

        total_latency = (time.time() - t0) * 1000

        # Montar output final
        final_output = self._build_final_output(pipeline_context)

        return MultiAgentPipelineResult(
            query=query,
            pipeline_mode="custom" if len(steps) < len(self.PIPELINE_FULL) else "full",
            steps=step_results,
            final_output=final_output,
            total_latency_ms=total_latency,
            status=status,
            metadata=self._build_metadata(step_results, pipeline_context),
        )

    # ── Step Execution ──────────────────────────────────────────────────

    def _run_step(
        self,
        step_name: str,
        pipeline_context: Dict[str, Any],
    ) -> PipelineStepResult:
        """
        Executa uma única etapa do pipeline com tratamento de erros.

        Cada etapa é isolada: falhas não propagam para etapas subsequentes.
        """
        t0 = time.time()

        try:
            if step_name == self.STEP_CLASSIFIER:
                return self._step_classify(pipeline_context)
            elif step_name == self.STEP_ROUTER:
                return self._step_route(pipeline_context)
            elif step_name == self.STEP_RETRIEVER:
                return self._step_retrieve(pipeline_context)
            elif step_name == self.STEP_GRAPH:
                return self._step_graph(pipeline_context)
            elif step_name == self.STEP_DIALECTIC:
                return self._step_dialectic(pipeline_context)
            elif step_name == self.STEP_SYNTHESIS:
                return self._step_synthesize(pipeline_context)
            elif step_name == self.STEP_VALIDATOR:
                return self._step_validate(pipeline_context)
            else:
                return PipelineStepResult(
                    step=step_name,
                    agent_name=self.AGENT_NAME,
                    success=False,
                    errors=[f"Etapa desconhecida: {step_name}"],
                )

        except Exception as e:
            latency_ms = (time.time() - t0) * 1000
            logger.error("Etapa '%s' errou: %s", step_name, e, exc_info=True)
            return PipelineStepResult(
                step=step_name,
                agent_name=self.AGENT_NAME,
                success=False,
                latency_ms=latency_ms,
                errors=[str(e)],
            )

    # ── Individual Step Implementations ─────────────────────────────────

    def _step_classify(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 1: Classificação ontológica N0→N4 via ClassifierAgent."""
        query = context.get("query", "")
        agent_result = self.classifier_agent.execute(query)

        output = {}
        if agent_result.output and isinstance(agent_result.output, dict):
            # Extrair classificação do output do agente
            agent_output = agent_result.output
            if "classification" in agent_output:
                output["classification"] = agent_output["classification"]
            else:
                output["classification"] = agent_output

        return PipelineStepResult(
            step=self.STEP_CLASSIFIER,
            agent_name=self.classifier_agent.name,
            success="error" not in (agent_result.output or {}),
            output=output,
            confidence=agent_result.confidence,
            latency_ms=agent_result.latency_ms,
            reasoning=agent_result.reasoning_steps,
            errors=agent_result.errors,
        )

    def _step_route(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 2: Roteamento cognitivo via CognitiveRouter."""
        query = context.get("query", "")
        classification = context.get("classification", {})

        # Fallback: se classificação falhou, usar classificação vazia
        if not classification:
            classification = {"classificacao": {}}

        routing = self.router.route(classification, query)
        routing_dict = routing.to_dict() if hasattr(routing, "to_dict") else {}

        return PipelineStepResult(
            step=self.STEP_ROUTER,
            agent_name="CognitiveRouter",
            success=True,
            output={"routing": routing_dict},
            confidence=routing.score if hasattr(routing, "score") else 0.5,
            latency_ms=0.0,  # CPU-bound, latência desprezível
            reasoning=[
                f"Estratégia: {routing.estrategia}" if hasattr(routing, "estrategia") else "",
                f"Pilar: {routing.pilar}" if hasattr(routing, "pilar") else "",
            ],
        )

    def _step_retrieve(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 3: Retrieval híbrido via HybridRetriever."""
        query = context.get("query", "")

        retrieved_cells = self.retriever.hybrid_rank(
            query,
            top_k=self.config.get("rerank_limit", 12),
        )

        return PipelineStepResult(
            step=self.STEP_RETRIEVER,
            agent_name="HybridRetriever",
            success=len(retrieved_cells) > 0,
            output={"retrieved_cells": retrieved_cells},
            confidence=min(1.0, len(retrieved_cells) / 3.0),
            latency_ms=0.0,
            reasoning=[
                f"{len(retrieved_cells)} células recuperadas",
            ],
        )

    def _step_graph(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 4: Expansão do grafo ontológico via GraphAgent."""
        retrieved_cells = context.get("retrieved_cells", [])

        if not retrieved_cells:
            return PipelineStepResult(
                step=self.STEP_GRAPH,
                agent_name=self.graph_agent.name,
                success=False,
                output={"graph_context": None},
                errors=["Nenhuma célula recuperada para expansão"],
            )

        seed_uids = [
            r["uid"] for r in retrieved_cells[:5]
            if isinstance(r, dict) and "uid" in r
        ]

        if not seed_uids:
            return PipelineStepResult(
                step=self.STEP_GRAPH,
                agent_name=self.graph_agent.name,
                success=False,
                output={"graph_context": None},
                errors=["Nenhum UID válido nas células recuperadas"],
            )

        # Executar expansão via GraphAgent
        agent_result = self.graph_agent.execute(
            "expand",
            context={
                "seed_uids": seed_uids,
                "depth": self.config.get("graph_depth", 3),
            },
        )

        output = {}
        if agent_result.output and isinstance(agent_result.output, dict):
            output["graph_context"] = agent_result.output

        return PipelineStepResult(
            step=self.STEP_GRAPH,
            agent_name=self.graph_agent.name,
            success="error" not in (agent_result.output or {}),
            output=output,
            confidence=agent_result.confidence,
            latency_ms=agent_result.latency_ms,
            reasoning=agent_result.reasoning_steps,
            errors=agent_result.errors,
        )

    def _step_dialectic(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 5: Inferência dialética via DialecticAgent."""
        retrieved_cells = context.get("retrieved_cells", [])

        if not retrieved_cells:
            return PipelineStepResult(
                step=self.STEP_DIALECTIC,
                agent_name=self.dialectic_agent.name,
                success=False,
                output={"dialectic_opposites": []},
                errors=["Nenhuma célula para análise dialética"],
            )

        cell_references = [
            r["uid"] for r in retrieved_cells[:10]
            if isinstance(r, dict) and "uid" in r
        ]

        if not cell_references:
            return PipelineStepResult(
                step=self.STEP_DIALECTIC,
                agent_name=self.dialectic_agent.name,
                success=False,
                output={"dialectic_opposites": []},
                errors=["Nenhum UID válido para análise dialética"],
            )

        # Executar inferência de opostos
        agent_result = self.dialectic_agent.execute(
            "find_dialectical_pairs",
            context={
                "cell_references": cell_references,
                "registry": self._registry,
                "max_pairs": 10,
            },
        )

        output = {}
        if agent_result.output and isinstance(agent_result.output, dict):
            # Extrair pares dialéticos do output
            if "output" in agent_result.output and isinstance(agent_result.output["output"], dict):
                output["dialectic_opposites"] = agent_result.output["output"].get("pairs", [])
            else:
                output["dialectic_opposites"] = agent_result.output.get("pairs", [])

        return PipelineStepResult(
            step=self.STEP_DIALECTIC,
            agent_name=self.dialectic_agent.name,
            success="error" not in (agent_result.output or {}),
            output=output,
            confidence=agent_result.confidence,
            latency_ms=agent_result.latency_ms,
            reasoning=agent_result.reasoning_steps,
            errors=agent_result.errors,
        )

    def _step_synthesize(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 6: Síntese de resposta via SynthesisAgent."""
        query = context.get("query", "")
        routing = context.get("routing", {})
        retrieved_cells = context.get("retrieved_cells", [])
        graph_context = context.get("graph_context")
        classification = context.get("classification", {})
        dialectic_opposites = context.get("dialectic_opposites")

        # Montar contexto de síntese
        synthesis_input_context = {
            "query": query,
            "routing_decision": routing,
            "retrieved_cells": retrieved_cells,
            "graph_context": graph_context,
            "classification": classification,
            "dialectic_opposites": dialectic_opposites,
        }

        agent_result = self.synthesis_agent.execute(
            "synthesize",
            context=synthesis_input_context,
        )

        output = {}
        if agent_result.output and isinstance(agent_result.output, dict):
            output["synthesis"] = agent_result.output

        return PipelineStepResult(
            step=self.STEP_SYNTHESIS,
            agent_name=self.synthesis_agent.name,
            success="error" not in (agent_result.output or {}),
            output=output,
            confidence=agent_result.confidence,
            latency_ms=agent_result.latency_ms,
            reasoning=agent_result.reasoning_steps,
            errors=agent_result.errors,
        )

    def _step_validate(self, context: Dict[str, Any]) -> PipelineStepResult:
        """Etapa 7: Validação ontológica via ValidatorAgent."""
        routing = context.get("routing", {})
        synthesis = context.get("synthesis", {})
        retrieved_cells = context.get("retrieved_cells", [])

        # Montar contexto de validação
        response_context = {}
        if synthesis and isinstance(synthesis, dict):
            response_context = {
                "cell_references": synthesis.get("cell_references", []),
                "prompt": synthesis.get("prompt", "")[:500],
            }

        agent_result = self.validator_agent.execute(
            "full",
            context={
                "routing": routing,
                "response_context": response_context,
                "retrieved_cells": retrieved_cells,
            },
        )

        output = {}
        if agent_result.output and isinstance(agent_result.output, dict):
            output["validation"] = agent_result.output

        return PipelineStepResult(
            step=self.STEP_VALIDATOR,
            agent_name=self.validator_agent.name,
            success="error" not in (agent_result.output or {}),
            output=output,
            confidence=agent_result.confidence,
            latency_ms=agent_result.latency_ms,
            reasoning=agent_result.reasoning_steps,
            errors=agent_result.errors,
        )

    # ── Context Management ──────────────────────────────────────────────

    def _update_context(
        self,
        step_name: str,
        pipeline_context: Dict[str, Any],
        step_output: Dict[str, Any],
    ) -> None:
        """Atualiza o contexto compartilhado com o output de uma etapa."""
        if step_name == self.STEP_CLASSIFIER:
            pipeline_context["classification"] = step_output.get("classification", {})
        elif step_name == self.STEP_ROUTER:
            routing = step_output.get("routing", {})
            pipeline_context["routing"] = routing
        elif step_name == self.STEP_RETRIEVER:
            pipeline_context["retrieved_cells"] = step_output.get("retrieved_cells", [])
        elif step_name == self.STEP_GRAPH:
            pipeline_context["graph_context"] = step_output.get("graph_context")
        elif step_name == self.STEP_DIALECTIC:
            pipeline_context["dialectic_opposites"] = step_output.get("dialectic_opposites", [])
        elif step_name == self.STEP_SYNTHESIS:
            pipeline_context["synthesis"] = step_output.get("synthesis", {})
        elif step_name == self.STEP_VALIDATOR:
            pipeline_context["validation"] = step_output.get("validation", {})

    # ── Output Building ─────────────────────────────────────────────────

    def _build_final_output(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Monta o output final consolidado a partir do contexto."""
        synthesis = context.get("synthesis", {})
        validation = context.get("validation", {})

        return {
            "prompt": synthesis.get("prompt", "") if synthesis else "",
            "context_summary": synthesis.get("context_summary", "") if synthesis else "",
            "cell_references": synthesis.get("cell_references", []) if synthesis else [],
            "synthesis_metadata": synthesis.get("metadata", {}) if synthesis else {},
            "validation": validation,
            "classification": context.get("classification", {}),
            "routing": context.get("routing", {}),
            "retrieved_cells_count": len(context.get("retrieved_cells", [])),
            "graph_context": context.get("graph_context"),
            "dialectic_opposites": context.get("dialectic_opposites", []),
        }

    def _build_metadata(
        self,
        step_results: List[PipelineStepResult],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Constrói metadados do pipeline."""
        successful = sum(1 for s in step_results if s.success)
        failed = len(step_results) - successful

        return {
            "total_steps": len(step_results),
            "successful_steps": successful,
            "failed_steps": failed,
            "step_latencies": {
                s.step: s.latency_ms for s in step_results
            },
            "step_confidences": {
                s.step: s.confidence for s in step_results
            },
            "retrieved_cells_count": len(context.get("retrieved_cells", [])),
            "graph_nodes": self.graph.G.number_of_nodes(),
            "graph_edges": self.graph.G.number_of_edges(),
            "agent_versions": {
                "classifier": self.classifier_agent.version,
                "graph": self.graph_agent.version,
                "synthesis": self.synthesis_agent.version,
                "validator": self.validator_agent.version,
                "dialectic": self.dialectic_agent.version,
            },
        }

    # ── Health Check ────────────────────────────────────────────────────

    def health_check(self) -> dict:
        """Verifica integridade de todos os componentes do pipeline multi-agente."""
        checks = {}

        # ClassifierAgent
        try:
            result = self.classifier_agent.execute("teste rápido")
            checks["classifier_agent"] = {
                "status": "ok" if "error" not in (result.output or {}) else "degraded",
                "version": self.classifier_agent.version,
            }
        except Exception as e:
            checks["classifier_agent"] = {"status": "error", "detail": str(e)}

        # GraphAgent
        try:
            result = self.graph_agent.execute("metrics", {})
            checks["graph_agent"] = {
                "status": "ok",
                "nodes": self.graph.G.number_of_nodes(),
                "edges": self.graph.G.number_of_edges(),
                "version": self.graph_agent.version,
            }
        except Exception as e:
            checks["graph_agent"] = {"status": "error", "detail": str(e)}

        # SynthesisAgent
        try:
            checks["synthesis_agent"] = {
                "status": "ok",
                "cache_size": len(self.synthesis_agent._prompt_cache),
                "version": self.synthesis_agent.version,
            }
        except Exception as e:
            checks["synthesis_agent"] = {"status": "error", "detail": str(e)}

        # ValidatorAgent
        try:
            checks["validator_agent"] = {
                "status": "ok",
                "registry_size": len(self.validator_agent._validator.registry),
                "version": self.validator_agent.version,
            }
        except Exception as e:
            checks["validator_agent"] = {"status": "error", "detail": str(e)}

        # DialecticAgent
        try:
            checks["dialectic_agent"] = {
                "status": "ok",
                "opposites_cache": len(self.dialectic_agent._opposites_cache),
                "distance_cache": len(self.dialectic_agent._distance_cache),
                "version": self.dialectic_agent.version,
            }
        except Exception as e:
            checks["dialectic_agent"] = {"status": "error", "detail": str(e)}

        # Retriever
        try:
            health = self.retriever.health_check()
            checks["retriever"] = {"status": "ok", **health}
        except Exception as e:
            checks["retriever"] = {"status": "error", "detail": str(e)}

        # Router
        try:
            checks["router"] = {
                "status": "ok",
                "strategy_count": len(self.router._strategies) if hasattr(self.router, "_strategies") else 0,
            }
        except Exception as e:
            checks["router"] = {"status": "error", "detail": str(e)}

        # Graph
        try:
            checks["graph"] = {
                "status": "ok",
                "nodes": self.graph.G.number_of_nodes(),
                "edges": self.graph.G.number_of_edges(),
                "registry_size": len(self._registry),
            }
        except Exception as e:
            checks["graph"] = {"status": "error", "detail": str(e)}

        overall = all(c.get("status") == "ok" for c in checks.values())
        return {
            "status": "healthy" if overall else "degraded",
            "components": checks,
            "pipeline_modes": {
                "full": len(self.PIPELINE_FULL),
                "simple": len(self.PIPELINE_SIMPLE),
            },
        }

    # ── Statistics ──────────────────────────────────────────────────────

    def get_pipeline_stats(self) -> dict:
        """Retorna estatísticas do pipeline multi-agente."""
        return {
            "agents": {
                "classifier": {
                    "name": self.classifier_agent.name,
                    "version": self.classifier_agent.version,
                    "cache_size": len(self.classifier_agent._cache),
                    "stats": self.classifier_agent._stats,
                },
                "graph": {
                    "name": self.graph_agent.name,
                    "version": self.graph_agent.version,
                    "cache_size": len(self.graph_agent._expansion_cache),
                    "graph_nodes": self.graph.G.number_of_nodes(),
                    "graph_edges": self.graph.G.number_of_edges(),
                },
                "synthesis": {
                    "name": self.synthesis_agent.name,
                    "version": self.synthesis_agent.version,
                    "cache_size": len(self.synthesis_agent._prompt_cache),
                },
                "validator": {
                    "name": self.validator_agent.name,
                    "version": self.validator_agent.version,
                    "cache_size": len(self.validator_agent._validation_cache),
                    "history_size": len(self.validator_agent._validation_history),
                },
                "dialectic": {
                    "name": self.dialectic_agent.name,
                    "version": self.dialectic_agent.version,
                    "opposites_cache": len(self.dialectic_agent._opposites_cache),
                    "distance_cache": len(self.dialectic_agent._distance_cache),
                },
            },
            "pipeline_modes": {
                "full_steps": self.PIPELINE_FULL,
                "simple_steps": self.PIPELINE_SIMPLE,
            },
            "graph_summary": {
                "nodes": self.graph.G.number_of_nodes(),
                "edges": self.graph.G.number_of_edges(),
                "registry_size": len(self._registry),
            },
        }

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do orchestrator."""
        return {
            "name": self.AGENT_NAME,
            "version": self.AGENT_VERSION,
            "pipeline_modes": {
                "full": self.PIPELINE_FULL,
                "simple": self.PIPELINE_SIMPLE,
            },
            "agents": {
                "classifier": self.classifier_agent.get_capabilities(),
                "graph": self.graph_agent.get_capabilities(),
                "synthesis": self.synthesis_agent.get_capabilities(),
                "validator": self.validator_agent.get_capabilities(),
                "dialectic": self.dialectic_agent.get_capabilities(),
            },
            "features": [
                "full_pipeline",
                "simple_pipeline",
                "custom_pipeline",
                "health_check",
                "multi_agent_coordination",
                "dialectical_enrichment",
                "graceful_degradation",
            ],
        }


# ── Ponto de entrada para testes ────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("INICIALIZANDO MULTI-AGENT ORCHESTRATOR...")
    print("=" * 60)

    orchestrator = MultiAgentOrchestrator()

    # Health check
    health = orchestrator.health_check()
    print(f"\nHealth Check: {health['status']}")
    for comp, info in health["components"].items():
        status = info.get("status", "unknown")
        detail = info.get("detail", "")
        extra = ""
        if "nodes" in info:
            extra = f" ({info['nodes']} nós, {info['edges']} arestas)"
        if "registry_size" in info:
            extra += f" registry={info['registry_size']}"
        print(f"  {comp}: {status}{extra}" + (f" ({detail})" if detail else ""))

    # Teste com query — Pipeline completo
    print("\n" + "=" * 60)
    test_query = "Como decompor um problema complexo em partes menores?"
    print(f"Query: {test_query}")
    print("=" * 60)

    result = orchestrator.full_pipeline(test_query)
    print(result.summary())

    # Teste com pipeline simplificado
    print("\n" + "=" * 60)
    test_query_2 = "O que é recursão e como ela se aplica na resolução de problemas?"
    print(f"Query (simple): {test_query_2}")
    print("=" * 60)

    result_simple = orchestrator.simple_pipeline(test_query_2)
    print(result_simple.summary())

    # Stats
    print("\n" + "=" * 60)
    stats = orchestrator.get_pipeline_stats()
    print("Pipeline Stats:")
    for section, data in stats.items():
        if isinstance(data, dict):
            print(f"  [{section}]")
            for k, v in data.items():
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        print(f"    {kk}: {vv}")
                else:
                    print(f"    {k}: {v}")
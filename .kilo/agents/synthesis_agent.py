#!/usr/bin/env python3
"""
AGENTE DE SÍNTESE — Geração de Respostas a partir de Contexto Ontológico.

Encapsula o OntologySynthesizer com montagem dinâmica de prompts,
seleção de template por pilar e composição de contexto multi-fonte.

FASE 7d do Roadmap da Ontologia Fractal.
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
from runtime.synthesizer import OntologySynthesizer, SynthesisInput, SynthesisOutput


@dataclass
class SynthesisContext:
    """Contexto enriquecido para síntese."""
    query: str
    routing_decision: Dict[str, Any] = field(default_factory=dict)
    retrieved_cells: List[dict] = field(default_factory=list)
    graph_context: Optional[Dict[str, Any]] = None
    classification: Optional[Dict[str, Any]] = None
    dialectic_opposites: Optional[List[Dict[str, Any]]] = None
    validator_feedback: Optional[Dict[str, Any]] = None


class SynthesisAgent(BaseAgent):
    """
    Agente especializado em síntese de respostas ontológicas.

    Responsabilidades:
    - Receber contexto classificado e enriquecido
    - Montar prompt dinâmico usando template do pilar
    - Combinar retrieved cells com contexto de grafo
    - Gerar resposta final composta
    - Suportar re-síntese com feedback do validador

    Diferencial em relação ao uso direto do OntologySynthesizer:
    - Gerenciamento de contexto multi-fonte
    - Re-síntese iterativa com feedback
    - Cache de prompts gerados
    - Enriquecimento com dados dialéticos
    """

    AGENT_NAME: str = "SynthesisAgent"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = ["synthesize", "resynthesize", "build_context"]

    def __init__(
        self,
        memory: Optional[AgentMemory] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            name=self.AGENT_NAME,
            memory=memory,
            config=config or {},
        )
        json_dir = config.get("json_dir", "data/json") if config else "data/json"
        index_path = config.get("index_path", "data/json/ontology_index.json") if config else "data/json/ontology_index.json"
        self._synthesizer = OntologySynthesizer(
            json_dir=json_dir,
            index_path=index_path,
        )
        self._prompt_cache: Dict[str, SynthesisOutput] = {}
        self._cache_max_size = 1000

    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Executa síntese de resposta.

        Args:
            task: A query original ou instrução.
            context: Dict com:
                - routing_decision: decisão de roteamento
                - retrieved_cells: células recuperadas
                - graph_context: contexto do grafo
                - classification: classificação ontológica
                - dialectic_opposites: opostos dialéticos (opcional)
                - validator_feedback: feedback do validador para re-síntese

        Returns:
            AgentResult com o prompt sintetizado e metadados.
        """
        t0 = time.time()
        context = context or {}

        try:
            # Verificar se é re-síntese (com feedback de validador)
            validator_feedback = context.get("validator_feedback")
            original_output = context.get("original_output")

            if validator_feedback and original_output:
                result = self._resynthesize(validator_feedback, original_output, context)
            else:
                result = self._synthesize(context)

            latency_ms = (time.time() - t0) * 1000

            return AgentResult(
                agent_name=self.name,
                task=task,
                output={
                    "prompt": result.prompt,
                    "context_summary": result.context_summary,
                    "cell_references": result.cell_references,
                    "metadata": result.metadata,
                },
                confidence=self._estimate_confidence(result),
                latency_ms=latency_ms,
                reasoning_steps=self._build_reasoning(result, context),
                metadata={
                    "pilar": context.get("routing_decision", {}).get("pilar"),
                    "cell_count": len(result.cell_references),
                    "prompt_length": len(result.prompt),
                },
            )

        except Exception as e:
            logger.error("SynthesisAgent falhou: %s", e, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": str(e)},
                confidence=0.0,
                latency_ms=(time.time() - t0) * 1000,
                errors=[str(e)],
            )

    def _synthesize(self, context: Dict[str, Any]) -> SynthesisOutput:
        """Realiza síntese inicial."""
        synthesis_input = SynthesisInput(
            query=context.get("query", ""),
            routing_decision=context.get("routing_decision", {}),
            retrieved_cells=context.get("retrieved_cells", []),
            graph_context=context.get("graph_context"),
            classification=context.get("classification"),
        )

        # Cache key
        cache_key = self._cache_key(synthesis_input)
        if cache_key in self._prompt_cache:
            return self._prompt_cache[cache_key]

        result = self._synthesizer.synthesize(synthesis_input)

        if len(self._prompt_cache) < self._cache_max_size:
            self._prompt_cache[cache_key] = result

        return result

    def _resynthesize(
        self,
        validator_feedback: Dict[str, Any],
        original_output: Dict[str, Any],
        context: Dict[str, Any],
    ) -> SynthesisOutput:
        """
        Re-sintetiza com base no feedback do validador.

        Ajusta o prompt para corrigir problemas de coerência identificados.
        """
        # Extrair problemas do feedback
        issues = []
        for v in validator_feedback.get("verificacoes", []):
            if not v.get("passou"):
                issues.append(f"{v['tipo']}: {v['detalhes']}")

        # Montar contexto enriquecido com restrições adicionais
        synthesis_input = SynthesisInput(
            query=context.get("query", ""),
            routing_decision=context.get("routing_decision", {}),
            retrieved_cells=context.get("retrieved_cells", []),
            graph_context=context.get("graph_context"),
            classification=context.get("classification"),
        )

        # Adicionar restrições baseadas nos problemas
        synthesis_input.metadata = {
            "validation_issues": issues,
            "original_output": original_output,
            "resynthesis": True,
        }

        cache_key = self._cache_key(synthesis_input) + "_resynth"
        if cache_key in self._prompt_cache:
            return self._prompt_cache[cache_key]

        result = self._synthesizer.synthesize(synthesis_input)

        if len(self._prompt_cache) < self._cache_max_size:
            self._prompt_cache[cache_key] = result

        return result

    def build_context(
        self,
        routing: Dict[str, Any],
        retrieved_cells: List[dict],
        graph_context: Optional[Dict[str, Any]] = None,
        classification: Optional[Dict[str, Any]] = None,
    ) -> SynthesisContext:
        """Monta contexto estruturado para síntese."""
        return SynthesisContext(
            query="",  # Será preenchido na execução
            routing_decision=routing,
            retrieved_cells=retrieved_cells,
            graph_context=graph_context,
            classification=classification,
        )

    def _cache_key(self, synthesis_input: SynthesisInput) -> str:
        """Gera chave de cache determinística."""
        key_parts = [
            synthesis_input.query[:100],
            str(synthesis_input.routing_decision.get("pilar", "")),
            str(synthesis_input.routing_decision.get("dominio", "")),
            str(len(synthesis_input.retrieved_cells)),
        ]
        return "|".join(key_parts)

    def _estimate_confidence(self, result: SynthesisOutput) -> float:
        """Estima confiança da síntese."""
        if not result.prompt:
            return 0.0
        # Mais referências = mais confiança
        ref_count = len(result.cell_references)
        base = 0.5
        ref_bonus = min(0.4, ref_count * 0.05)
        length_penalty = max(0, 1.0 - len(result.prompt) / 5000) * 0.1
        return round(base + ref_bonus - length_penalty, 4)

    def _build_reasoning(
        self,
        result: SynthesisOutput,
        context: Dict[str, Any],
    ) -> List[str]:
        """Gera explicação da síntese."""
        reasoning = []
        pilar = context.get("routing_decision", {}).get("pilar", "N/A")
        reasoning.append(f"Template de síntese: pilar {pilar}")
        reasoning.append(f"Células referenciadas: {len(result.cell_references)}")
        if result.metadata:
            reasoning.append(f"Metadados: {json.dumps(result.metadata, default=str)[:200]}")
        return reasoning

    # ── Batch Operations ────────────────────────────────────────────────

    def synthesize_batch(
        self,
        contexts: List[Dict[str, Any]],
    ) -> List[AgentResult]:
        """Síntese em lote para múltiplos contextos."""
        return [self.execute(f"batch_{i}", ctx) for i, ctx in enumerate(contexts)]

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.REQUIRED_TOOLS,
            "description": "Síntese de respostas ontológicas com templates por pilar",
            "cache_size": len(self._prompt_cache),
            "cache_max": self._cache_max_size,
            "features": ["synthesize", "resynthesize", "multi_perspective"],
        }
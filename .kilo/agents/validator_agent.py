#!/usr/bin/env python3
"""
AGENTE DE VALIDAÇÃO — Verificação de Coerência Ontológica.

Encapsula o OntologyValidator com verificações multi-camada e
recomendações acionáveis para correção de respostas.

FASE 7e do Roadmap da Ontologia Fractal.
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

from core.agent_base import BaseAgent, AgentResult, AgentMemory
from runtime.validator import (
    OntologyValidator,
    ValidationReport,
    VerificationResult,
)


@dataclass
class ValidationVerdict:
    """Veredito estruturado da validação."""
    aprovado: bool
    score_geral: float
    verificacoes: List[dict]
    recomendacoes: List[str]
    criticidade: str  # "alta", "media", "baixa"
    pode_resintetizar: bool = True

    def to_dict(self) -> dict:
        return {
            "aprovado": self.aprovado,
            "score_geral": round(self.score_geral, 4),
            "criticidade": self.criticidade,
            "verificacoes": self.verificacoes,
            "recomendacoes": self.recomendacoes,
            "pode_resintetizar": self.pode_resintetizar,
        }


class ValidatorAgent(BaseAgent):
    """
    Agente especializado em validação de coerência ontológica.

    Responsabilidades:
    - Verificar coerência de respostas geradas pelo pipeline
    - Avaliar consistência de eixo, assinatura e polaridades
    - Detectar conceitos inválidos e relações quebradas
    - Gerar recomendações acionáveis para re-síntese
    - Manter histórico de qualidade para auto-avaliação

    Diferencial em relação ao uso direto do OntologyValidator:
    - Veredito estruturado com criticidade e recomendações
    - Cache de resultados para queries similares
    - Análise de tendência de qualidade ao longo do tempo
    - Suporte a validação incremental (por camada)
    """

    AGENT_NAME: str = "ValidatorAgent"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = [
        "validate_full",
        "validate_partial",
        "check_concepts",
        "check_relations",
        "assess_quality",
    ]

    # Thresholds de qualidade
    SCORE_CRITICO = 0.4
    SCORE_AVISO = 0.7
    SCORE_APROVACAO = 0.6

    def __init__(
        self,
        memory: Optional[AgentMemory] = None,
        config: Optional[Dict[str, Any]] = None,
        validator: Optional[OntologyValidator] = None,
    ):
        super().__init__(
            name=self.AGENT_NAME,
            memory=memory,
            config=config or {},
        )
        json_dir = config.get("json_dir", "data/json") if config else "data/json"
        index_path = config.get("index_path", "data/json/ontology_index.json") if config else "data/json/ontology_index.json"

        if validator:
            self._validator = validator
        else:
            self._validator = OntologyValidator(
                json_dir=json_dir,
                index_path=index_path,
            )

        self._validation_cache: Dict[str, ValidationVerdict] = {}
        self._cache_max_size = 500
        self._validation_history: List[Dict[str, Any]] = []

    # ── Core Execution ──────────────────────────────────────────────────

    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Executa validação ontológica.

        Args:
            task: Tipo de validação ("full", "partial", "concepts", "relations", "assess")
            context: Dict com:
                - routing: decisão de roteamento
                - response_context: contexto da resposta
                - retrieved_cells: células recuperadas
                - synthesis_output: saída da síntese (opcional)
                - previous_verdict: veredito anterior para comparação

        Returns:
            AgentResult com o veredito de validação.
        """
        t0 = time.time()
        context = context or {}

        try:
            operation = task.strip().lower()

            if operation == "full":
                verdict = self._validate_full(context)
            elif operation == "partial":
                verdict = self._validate_partial(context)
            elif operation == "concepts":
                verdict = self._check_concepts(context)
            elif operation == "relations":
                verdict = self._check_relations(context)
            elif operation == "assess":
                verdict = self._assess_quality(context)
            else:
                verdict = self._validate_full(context)

            latency_ms = (time.time() - t0) * 1000

            # Registrar no histórico
            self._validation_history.append({
                "timestamp": time.time(),
                "task": task,
                "score": verdict.score_geral,
                "aprovado": verdict.aprovado,
                "criticidade": verdict.criticidade,
            })

            return AgentResult(
                agent_name=self.name,
                task=task,
                output=verdict.to_dict(),
                confidence=self._estimate_confidence(verdict),
                latency_ms=latency_ms,
                reasoning_steps=self._build_reasoning(verdict),
                metadata={
                    "registry_size": len(self._validator.registry),
                    "history_size": len(self._validation_history),
                    "criticidade": verdict.criticidade,
                },
            )

        except Exception as e:
            logger.error("ValidatorAgent falhou na operação '%s': %s", task, e, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": str(e)},
                confidence=0.0,
                latency_ms=(time.time() - t0) * 1000,
                errors=[str(e)],
            )

    # ── Validation Handlers ─────────────────────────────────────────────

    def _validate_full(self, context: Dict[str, Any]) -> ValidationVerdict:
        """Validação completa — todas as verificações."""
        routing = context.get("routing", {})
        response_context = context.get("response_context", {})
        retrieved_cells = context.get("retrieved_cells")

        # Cache key
        cache_key = self._cache_key(routing, response_context)
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]

        report = self._validator.validate(
            routing=routing,
            response_context=response_context,
            retrieved_cells=retrieved_cells,
        )

        verdict = self._report_to_verdict(report)

        if len(self._validation_cache) < self._cache_max_size:
            self._validation_cache[cache_key] = verdict

        return verdict

    def _validate_partial(self, context: Dict[str, Any]) -> ValidationVerdict:
        """Validação parcial — apenas verificações especificadas."""
        routing = context.get("routing", {})
        response_context = context.get("response_context", {})
        checks = context.get("checks", ["eixo_coerente", "conceitos_validos"])

        cache_key = self._cache_key(routing, response_context) + "_partial_" + "_".join(checks)
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]

        # Executa validação completa e filtra resultados
        report = self._validator.validate(
            routing=routing,
            response_context=response_context,
            retrieved_cells=context.get("retrieved_cells"),
        )

        # Filtra verificações relevantes
        verificacoes_filtradas = [
            v for v in report.verificacoes if v.tipo in checks
        ]

        if not verificacoes_filtradas:
            verificacoes_filtradas = report.verificacoes

        # Recalcula score baseado apenas nas verificações filtradas
        scores = [v.score for v in verificacoes_filtradas]
        score_parcial = float(sum(scores) / len(scores)) if scores else 0.0

        report_parcial = ValidationReport(
            valido=bool(score_parcial >= self._validator.threshold),
            verificacoes=verificacoes_filtradas,
            score_geral=score_parcial,
            recomendacoes=report.recomendacoes,
        )

        verdict = self._report_to_verdict(report_parcial)

        if len(self._validation_cache) < self._cache_max_size:
            self._validation_cache[cache_key] = verdict

        return verdict

    def _check_concepts(self, context: Dict[str, Any]) -> ValidationVerdict:
        """Verifica apenas a validade dos conceitos referenciados."""
        routing = context.get("routing", {})
        response_context = context.get("response_context", {})
        retrieved_cells = context.get("retrieved_cells")

        cache_key = self._cache_key(routing, response_context) + "_concepts"
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]

        report = self._validator.validate(
            routing=routing,
            response_context=response_context,
            retrieved_cells=retrieved_cells,
        )

        # Extrai apenas a verificação de conceitos
        conceito_verif = next(
            (v for v in report.verificacoes if v.tipo == "conceitos_validos"),
            VerificationResult(
                tipo="conceitos_validos",
                passou=True,
                score=1.0,
                detalhes="Nenhuma verificação de conceitos disponível.",
            ),
        )

        report_filtrado = ValidationReport(
            valido=bool(conceito_verif.score >= self._validator.threshold),
            verificacoes=[conceito_verif],
            score_geral=conceito_verif.score,
            recomendacoes=report.recomendacoes,
        )

        verdict = self._report_to_verdict(report_filtrado)

        if len(self._validation_cache) < self._cache_max_size:
            self._validation_cache[cache_key] = verdict

        return verdict

    def _check_relations(self, context: Dict[str, Any]) -> ValidationVerdict:
        """Verifica apenas a consistência das relações."""
        routing = context.get("routing", {})
        response_context = context.get("response_context", {})
        retrieved_cells = context.get("retrieved_cells")

        cache_key = self._cache_key(routing, response_context) + "_relations"
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]

        report = self._validator.validate(
            routing=routing,
            response_context=response_context,
            retrieved_cells=retrieved_cells,
        )

        # Extrai apenas a verificação de relações
        rel_verif = next(
            (v for v in report.verificacoes if v.tipo == "relacoes_consistentes"),
            VerificationResult(
                tipo="relacoes_consistentes",
                passou=True,
                score=1.0,
                detalhes="Nenhuma verificação de relações disponível.",
            ),
        )

        report_filtrado = ValidationReport(
            valido=bool(rel_verif.score >= self._validator.threshold),
            verificacoes=[rel_verif],
            score_geral=rel_verif.score,
            recomendacoes=report.recomendacoes,
        )

        verdict = self._report_to_verdict(report_filtrado)

        if len(self._validation_cache) < self._cache_max_size:
            self._validation_cache[cache_key] = verdict

        return verdict

    def _assess_quality(self, context: Dict[str, Any]) -> ValidationVerdict:
        """Avalia a qualidade geral sem validar (apenas score)."""
        routing = context.get("routing", {})
        response_context = context.get("response_context", {})

        cache_key = self._cache_key(routing, response_context) + "_quality"
        if cache_key in self._validation_cache:
            return self._validation_cache[cache_key]

        report = self._validator.validate(
            routing=routing,
            response_context=response_context,
            retrieved_cells=context.get("retrieved_cells"),
        )

        verdict = self._report_to_verdict(report)

        if len(self._validation_cache) < self._cache_max_size:
            self._validation_cache[cache_key] = verdict

        return verdict

    # ── Conversion ──────────────────────────────────────────────────────

    def _report_to_verdict(self, report: ValidationReport) -> ValidationVerdict:
        """Converte ValidationReport em ValidationVerdict."""
        criticidade = self._classify_criticidade(report)

        return ValidationVerdict(
            aprovado=report.valido,
            score_geral=report.score_geral,
            verificacoes=[v.to_dict() for v in report.verificacoes],
            recomendacoes=report.recomendacoes,
            criticidade=criticidade,
            pode_resintetizar=not report.valido or report.score_geral < self.SCORE_AVISO,
        )

    def _classify_criticidade(self, report: ValidationReport) -> str:
        """Classifica a criticidade do veredito."""
        score = report.score_geral
        if score < self.SCORE_CRITICO:
            return "alta"
        elif score < self.SCORE_AVISO:
            return "media"
        else:
            return "baixa"

    # ── Utility ─────────────────────────────────────────────────────────

    def _cache_key(self, routing: dict, response_context: dict) -> str:
        """Gera chave de cache determinística."""
        key_parts = [
            str(routing.get("pilar", "")),
            str(routing.get("eixo", "")),
            str(routing.get("dominio", "")),
            str(len(response_context.get("cell_references", []))),
        ]
        return "|".join(key_parts)

    def _estimate_confidence(self, verdict: ValidationVerdict) -> float:
        """Estima a confiança da validação."""
        # Score alto + baixa criticidade = alta confiança
        base = verdict.score_geral
        criticidade_penalty = {
            "alta": 0.3,
            "media": 0.15,
            "baixa": 0.0,
        }.get(verdict.criticidade, 0.15)
        return round(max(0.0, min(1.0, base - criticidade_penalty)), 4)

    def _build_reasoning(self, verdict: ValidationVerdict) -> List[str]:
        """Gera explicação do veredito."""
        reasoning = []
        reasoning.append(f"Criticidade: {verdict.criticidade}")
        reasoning.append(f"Score geral: {verdict.score_geral:.2%}")
        reasoning.append(f"Aprovado: {'Sim' if verdict.aprovado else 'Não'}")

        if verdict.verificacoes:
            falhas = [
                v["tipo"] for v in verdict.verificacoes if not v.get("passou", True)
            ]
            if falhas:
                reasoning.append(f"Verificações que falharam: {', '.join(falhas)}")
            else:
                reasoning.append("Todas as verificações passaram.")

        if verdict.recomendacoes:
            reasoning.append(
                f"Recomendações: {len(verdict.recomendacoes)} ação(ões) sugerida(s)"
            )

        return reasoning

    # ── Batch Operations ────────────────────────────────────────────────

    def validate_batch(
        self,
        contexts: List[Dict[str, Any]],
    ) -> List[AgentResult]:
        """Valida múltiplos contextos em lote."""
        return [
            self.execute("full", ctx) for ctx in contexts
        ]

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.REQUIRED_TOOLS,
            "description": "Validação de coerência ontológica com criticidade e recomendações",
            "cache_size": len(self._validation_cache),
            "cache_max": self._cache_max_size,
            "features": [
                "validate_full",
                "validate_partial",
                "check_concepts",
                "check_relations",
                "assess_quality",
                "criticidade_classification",
            ],
        }
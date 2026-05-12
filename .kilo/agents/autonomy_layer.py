#!/usr/bin/env python3
"""
AUTONOMY LAYER — Auto-avaliação, Feedback Loops e Thresholds Adaptativos.

FASE 9 do Roadmap da Ontologia Fractal.

Este módulo transforma o pipeline multi-agente em um sistema autônomo
que:
- Avalia continuamente a qualidade de suas próprias respostas
- Ajusta thresholds de decisão com base em feedback acumulado
- Detecta drift semântico e degradação de performance
- Implementa ciclos de retroalimentação para auto-melhoria
- Mantém memória de episódios para aprendizado longitudinal

Design Principles:
- Separation of Concerns: cada mecanismo de auto-regulação é isolado
- Graceful Degradation: falhas no autonomy layer não quebram o pipeline
- Observability: todas as decisões de auto-regulação são logadas
- Adaptabilidade: thresholds evoluem com base em evidência empírica
"""

from __future__ import annotations

import json
import logging
import math
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))
if str(_PROJECT_ROOT / "runtime") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "runtime"))

from core.agent_base import AgentMemory, EpisodeEntry


# ─────────────────────────────────────────────────────────────────────
# 1. MODELOS DE DADOS
# ─────────────────────────────────────────────────────────────────────

@dataclass
class QualityMetrics:
    """Métricas de qualidade de uma resposta do pipeline."""
    episode_id: str = ""
    timestamp: str = ""

    # Scores por etapa
    classification_confidence: float = 0.0
    routing_score: float = 0.0
    retrieval_relevance: float = 0.0
    synthesis_confidence: float = 0.0
    validation_score: float = 0.0
    validation_aprovado: bool = False
    validation_criticidade: str = "media"

    # Composites
    quality_score: float = 0.0       # Score geral ponderado
    coherence_score: float = 0.0     # Coerência entre etapas
    consistency_score: float = 0.0   # Consistência ontológica

    # Latência
    total_latency_ms: float = 0.0
    step_latencies: Dict[str, float] = field(default_factory=dict)

    # Feedback explícito (quando disponível)
    user_feedback: Optional[float] = None  # -1.0 a 1.0
    implicit_feedback: float = 0.0         # sinais implícitos

    # Meta
    pipeline_mode: str = "full"
    query_length: int = 0
    num_retrieved_cells: int = 0
    num_dialectic_pairs: int = 0

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "timestamp": self.timestamp,
            "scores": {
                "classification": self.classification_confidence,
                "routing": self.routing_score,
                "retrieval": self.retrieval_relevance,
                "synthesis": self.synthesis_confidence,
                "validation": self.validation_score,
            },
            "composites": {
                "quality": round(self.quality_score, 4),
                "coherence": round(self.coherence_score, 4),
                "consistency": round(self.consistency_score, 4),
            },
            "validation": {
                "aprovado": self.validation_aprovado,
                "criticidade": self.validation_criticidade,
            },
            "latency": {
                "total_ms": round(self.total_latency_ms, 2),
                "by_step": {k: round(v, 2) for k, v in self.step_latencies.items()},
            },
            "feedback": {
                "user": self.user_feedback,
                "implicit": round(self.implicit_feedback, 4),
            },
            "metadata": {
                "pipeline_mode": self.pipeline_mode,
                "query_length": self.query_length,
                "retrieved_cells": self.num_retrieved_cells,
                "dialectic_pairs": self.num_dialectic_pairs,
            },
        }


@dataclass
class AdaptiveThresholds:
    """Thresholds adaptativos calibrados pelo AutonomyLayer."""
    # Thresholds de qualidade
    min_quality_score: float = 0.5
    min_validation_score: float = 0.6
    min_classification_confidence: float = 0.4
    min_synthesis_confidence: float = 0.4

    # Thresholds de roteamento
    routing_score_floor: float = 0.3
    max_ambiguity_ratio: float = 0.3

    # Thresholds de retrieval
    semantic_similarity_min: float = 0.72
    graph_relevance_min: float = 0.5
    min_cells_for_synthesis: int = 2

    # Thresholds dialéticos
    dialectic_distance_threshold: float = 0.7
    tension_min_for_enrichment: float = 0.3

    # Controle de adaptação
    adaptation_rate: float = 0.05        # Taxa de ajuste incremental
    min_samples_for_adaptation: int = 10  # Amostras mínimas antes de ajustar
    max_deviation: float = 0.15          # Máxima variação por ciclo

    # Pesos de composição do quality score
    weights: Dict[str, float] = field(default_factory=lambda: {
        "classification": 0.15,
        "routing": 0.05,
        "retrieval": 0.20,
        "synthesis": 0.25,
        "validation": 0.35,
    })

    def to_dict(self) -> dict:
        return {
            "min_quality_score": self.min_quality_score,
            "min_validation_score": self.min_validation_score,
            "min_classification_confidence": self.min_classification_confidence,
            "min_synthesis_confidence": self.min_synthesis_confidence,
            "routing_score_floor": self.routing_score_floor,
            "max_ambiguity_ratio": self.max_ambiguity_ratio,
            "semantic_similarity_min": self.semantic_similarity_min,
            "graph_relevance_min": self.graph_relevance_min,
            "min_cells_for_synthesis": self.min_cells_for_synthesis,
            "dialectic_distance_threshold": self.dialectic_distance_threshold,
            "tension_min_for_enrichment": self.tension_min_for_enrichment,
            "adaptation_rate": self.adaptation_rate,
            "min_samples_for_adaptation": self.min_samples_for_adaptation,
            "max_deviation": self.max_deviation,
            "weights": self.weights,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AdaptiveThresholds":
        """Recria thresholds a partir de dicionário serializado."""
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance


@dataclass
class AdaptationEvent:
    """Registro de um evento de adaptação."""
    timestamp: str
    trigger: str           # O que disparou a adaptação
    parameter: str         # Qual parâmetro foi ajustado
    old_value: float
    new_value: float
    rationale: str         # Justificativa da adaptação
    metrics_snapshot: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "trigger": self.trigger,
            "parameter": self.parameter,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "rationale": self.rationale,
            "metrics_snapshot": self.metrics_snapshot,
        }


@dataclass
class DriftDetection:
    """Detecção de drift semântico no pipeline."""
    drift_detected: bool = False
    drift_type: str = ""           # "quality_decline", "distribution_shift", "confidence_drop"
    severity: float = 0.0          # 0.0 a 1.0
    window_size: int = 0
    current_avg_quality: float = 0.0
    baseline_avg_quality: float = 0.0
    affected_metrics: List[str] = field(default_factory=list)
    recommended_action: str = ""

    def to_dict(self) -> dict:
        return {
            "drift_detected": self.drift_detected,
            "drift_type": self.drift_type,
            "severity": round(self.severity, 4),
            "window_size": self.window_size,
            "current_avg_quality": round(self.current_avg_quality, 4),
            "baseline_avg_quality": round(self.baseline_avg_quality, 4),
            "affected_metrics": self.affected_metrics,
            "recommended_action": self.recommended_action,
        }


# ─────────────────────────────────────────────────────────────────────
# 2. MECANISMO DE AUTO-AVALIAÇÃO
# ─────────────────────────────────────────────────────────────────────

class SelfEvaluator:
    """
    Avalia continuamente a qualidade do pipeline usando múltiplos sinais:
    - Scores de validação ontológica
    - Consistência entre etapas
    - Feedback explícito e implícito
    - Métricas de latência e cobertura
    """

    def __init__(self, thresholds: AdaptiveThresholds):
        self.thresholds = thresholds
        self._history: List[QualityMetrics] = []
        self._max_history = 1000

    def evaluate(self, pipeline_result: Dict[str, Any]) -> QualityMetrics:
        """
        Avalia o resultado do pipeline e produz métricas de qualidade.

        Combina sinais de múltiplas fontes em um score composto.
        """
        metrics = QualityMetrics()
        metrics.timestamp = datetime.now(timezone.utc).isoformat()

        # Extrair scores de validação
        validation = pipeline_result.get("final_output", {}).get("validation", {})
        if validation:
            metrics.validation_score = validation.get("score_geral", 0.0)
            metrics.validation_aprovado = validation.get("aprovado", False)
            metrics.validation_criticidade = validation.get("criticidade", "media")

        # Extrair confiança da classificação
        classification = pipeline_result.get("steps", [{}])
        for step in classification:
            step_name = step.get("step", "")
            if step_name == "classifier":
                metrics.classification_confidence = step.get("confidence", 0.0)
            elif step_name == "router":
                metrics.routing_score = step.get("confidence", 0.0)
            elif step_name == "retriever":
                metrics.retrieval_relevance = step.get("confidence", 0.0)
            elif step_name == "synthesis":
                metrics.synthesis_confidence = step.get("confidence", 0.0)

        # Calcular latências
        for step in pipeline_result.get("steps", []):
            step_name = step.get("step", "")
            metrics.step_latencies[step_name] = step.get("latency_ms", 0.0)
        metrics.total_latency_ms = pipeline_result.get("total_latency_ms", 0.0)

        # Metadados
        metrics.pipeline_mode = pipeline_result.get("pipeline_mode", "full")
        metrics.query_length = len(pipeline_result.get("query", "").split())

        # Contar células recuperadas
        retrieved = pipeline_result.get("steps", [])
        for step in retrieved:
            if step.get("step") == "retriever":
                metrics.num_retrieved_cells = len(
                    step.get("output", {}).get("retrieved_cells", [])
                )
            elif step.get("step") == "dialectic":
                metrics.num_dialectic_pairs = len(
                    step.get("output", {}).get("dialectic_opposites", [])
                )

        # Calcular coerência entre etapas
        metrics.coherence_score = self._compute_coherence(pipeline_result)

        # Calcular consistência ontológica
        metrics.consistency_score = self._compute_consistency(pipeline_result)

        # Composição do quality score
        metrics.quality_score = self._compute_composite_score(metrics)

        # Gerar episode_id
        if pipeline_result.get("steps"):
            for step in pipeline_result["steps"]:
                if step.get("step") == "classifier":
                    output = step.get("output", {})
                    cls_data = output.get("classification", {})
                    metrics.episode_id = cls_data.get("classificacao", {}).get(
                        "n4_celula", {}
                    ).get("uid", "")[:16]
                    break

        # Feedback implícito (derivado da qualidade)
        metrics.implicit_feedback = self._compute_implicit_feedback(metrics)

        return metrics

    def _compute_coherence(self, pipeline_result: Dict[str, Any]) -> float:
        """
        Avalia a coerência entre as etapas do pipeline.
        Verifica se a classificação é consistente com o roteamento,
        se o retrieval é relevante para a classificação, etc.
        """
        scores = []

        # Extrair classificação e roteamento
        class_data = {}
        route_data = {}
        for step in pipeline_result.get("steps", []):
            if step.get("step") == "classifier":
                class_data = step.get("output", {}).get("classification", {})
            elif step.get("step") == "router":
                route_data = step.get("output", {}).get("routing", {})

        # Coerência: pilar da classificação deve corresponder ao pilar do roteamento
        class_pilar = class_data.get("classificacao", {}).get("n1_pilar", {}).get("pilar", "")
        route_pilar = route_data.get("pilar", "")
        if class_pilar and route_pilar:
            pilar_match = 1.0 if class_pilar.upper() == route_pilar.upper() else 0.0
            scores.append(("pillar_alignment", pilar_match))

        # Coerência: domínio deve corresponder
        class_dominio = class_data.get("classificacao", {}).get("n2_dominio", {}).get("dominio", "")
        route_dominio = route_data.get("dominio", "")
        if class_dominio and route_dominio:
            dominio_match = 1.0 if class_dominio.upper() == route_dominio.upper() else 0.0
            scores.append(("domain_alignment", dominio_match))

        # Coerência: retrieval deve ter retornado células
        retriever_output = {}
        retrieval_confidence = 0.0
        for step in pipeline_result.get("steps", []):
            if step.get("step") == "retriever":
                retriever_output = step.get("output", {})
                retrieval_confidence = step.get("confidence", 0.0)
                break

        cells = retriever_output.get("retrieved_cells", [])
        if not cells:
            retrieval_confidence = 0.0
        scores.append(("retrieval_quality", retrieval_confidence))

        # Coerência: síntese deve referenciar células
        synth_output = {}
        for step in pipeline_result.get("steps", []):
            if step.get("step") == "synthesis":
                synth_output = step.get("output", {})
                break

        synth_data = synth_output.get("synthesis", {})
        if synth_data:
            cell_refs = synth_data.get("cell_references", [])
            if cell_refs and cells:
                ref_coverage = min(len(cell_refs) / max(len(cells), 1), 1.0)
                scores.append(("reference_coverage", ref_coverage))
            else:
                scores.append(("reference_coverage", 0.0))

        if not scores:
            return 0.5

        return sum(s[1] for s in scores) / len(scores)

    def _compute_consistency(self, pipeline_result: Dict[str, Any]) -> float:
        """
        Avalia a consistência ontológica do resultado.
        Verifica se conceitos contraditórios não foram misturados,
        se o eixo é respeitado, se assinaturas são compatíveis.
        """
        # Extrair validação
        validation = pipeline_result.get("final_output", {}).get("validation", {})
        if validation:
            verificacoes = validation.get("verificacoes", [])
            if verificacoes:
                scores = [v.get("score", 0.0) for v in verificacoes]
                return sum(scores) / len(scores) if scores else 0.5

        return 0.5

    def _compute_composite_score(self, metrics: QualityMetrics) -> float:
        """Calcula o score de qualidade composto usando pesos configuráveis."""
        weights = self.thresholds.weights

        components = {
            "classification": metrics.classification_confidence,
            "routing": metrics.routing_score,
            "retrieval": metrics.retrieval_relevance,
            "synthesis": metrics.synthesis_confidence,
            "validation": metrics.validation_score,
        }

        weighted_sum = sum(
            weights.get(key, 0.0) * value
            for key, value in components.items()
        )

        # Bônus por coerência e consistência
        coherence_bonus = metrics.coherence_score * 0.1
        consistency_bonus = metrics.consistency_score * 0.1

        raw_score = weighted_sum + coherence_bonus + consistency_bonus
        return round(max(0.0, min(1.0, raw_score)), 4)

    def _compute_implicit_feedback(self, metrics: QualityMetrics) -> float:
        """
        Deriva feedback implícito a partir das métricas de qualidade.
        Combina sinais positivos e negativos.
        """
        score = 0.0

        # Score de qualidade alto = feedback positivo
        score += metrics.quality_score * 0.4

        # Validação aprovada = feedback positivo
        if metrics.validation_aprovado:
            score += 0.3
        else:
            score -= 0.2

        # Baixa latência = feedback positivo
        if metrics.total_latency_ms < 2000:
            score += 0.1
        elif metrics.total_latency_ms > 5000:
            score -= 0.1

        # Cobertura de retrieval boa
        if metrics.num_retrieved_cells >= 3:
            score += 0.1
        elif metrics.num_retrieved_cells == 0:
            score -= 0.2

        # Criticidade baixa = positivo
        if metrics.validation_criticidade == "baixa":
            score += 0.1
        elif metrics.validation_criticidade == "alta":
            score -= 0.2

        return round(max(-1.0, min(1.0, score)), 4)

    def add_to_history(self, metrics: QualityMetrics) -> None:
        """Adiciona métricas ao histórico."""
        self._history.append(metrics)
        if len(self._history) > self._max_history:
            self._history = self._history[-self._max_history:]

    def get_recent_quality(self, window: int = 20) -> List[float]:
        """Retorna scores de qualidade recentes."""
        return [m.quality_score for m in self._history[-window:]]

    def get_average_quality(self, window: int = 50) -> float:
        """Calcula qualidade média em uma janela."""
        recent = self.get_recent_quality(window)
        return sum(recent) / len(recent) if recent else 0.0

    @property
    def history_size(self) -> int:
        return len(self._history)


# ─────────────────────────────────────────────────────────────────────
# 3. DETECÇÃO DE DRIFT
# ─────────────────────────────────────────────────────────────────────

class DriftDetector:
    """
    Detecta drift semântico e degradação de performance no pipeline.

    Monitora:
    - Queda na qualidade média das respostas
    - Mudança na distribuição de classificações
    - Degradação na confiança dos agentes
    - Aumento na taxa de falhas
    """

    def __init__(
        self,
        baseline_window: int = 100,
        detection_window: int = 20,
        quality_threshold: float = 0.15,    # Queda mínima para alertar
        confidence_threshold: float = 0.10,
    ):
        self.baseline_window = baseline_window
        self.detection_window = detection_window
        self.quality_threshold = quality_threshold
        self.confidence_threshold = confidence_threshold

    def detect(self, evaluator: SelfEvaluator) -> DriftDetection:
        """
        Analisa o histórico de métricas para detectar drift.

        Compara a janela recente com a baseline para identificar
        degradação significativa.
        """
        result = DriftDetection()

        if evaluator.history_size < self.baseline_window + self.detection_window:
            result.recommended_action = "Histórico insuficiente para detecção"
            return result

        history = evaluator._history

        # Baseline: janela inicial
        baseline_scores = [
            m.quality_score
            for m in history[:self.baseline_window]
        ]
        baseline_avg = sum(baseline_scores) / len(baseline_scores) if baseline_scores else 0.5

        # Janela atual
        current_scores = [
            m.quality_score
            for m in history[-self.detection_window:]
        ]
        current_avg = sum(current_scores) / len(current_scores) if current_scores else 0.5

        result.baseline_avg_quality = baseline_avg
        result.current_avg_quality = current_avg
        result.window_size = self.detection_window

        # Detectar queda de qualidade
        quality_drop = baseline_avg - current_avg
        if quality_drop >= self.quality_threshold:
            result.drift_detected = True
            result.drift_type = "quality_decline"
            result.severity = min(1.0, quality_drop / 0.5)
            result.affected_metrics.append("quality_score")

        # Detectar queda de confiança
        baseline_conf = [
            m.classification_confidence for m in history[:self.baseline_window]
        ]
        current_conf = [
            m.classification_confidence for m in history[-self.detection_window:]
        ]
        baseline_conf_avg = sum(baseline_conf) / len(baseline_conf) if baseline_conf else 0.5
        current_conf_avg = sum(current_conf) / len(current_conf) if current_conf else 0.5

        conf_drop = baseline_conf_avg - current_conf_avg
        if conf_drop >= self.confidence_threshold:
            result.drift_detected = True
            if result.drift_type:
                result.drift_type += " + confidence_drop"
            else:
                result.drift_type = "confidence_drop"
            result.severity = max(result.severity, min(1.0, conf_drop / 0.5))
            result.affected_metrics.append("classification_confidence")

        # Detectar aumento de criticidade
        recent_criticidades = [
            m.validation_criticidade for m in history[-self.detection_window:]
        ]
        high_crit_count = sum(1 for c in recent_criticidades if c == "alta")
        crit_ratio = high_crit_count / len(recent_criticidades) if recent_criticidades else 0

        if crit_ratio > 0.5:
            result.drift_detected = True
            if result.drift_type:
                result.drift_type += " + distribution_shift"
            else:
                result.drift_type = "distribution_shift"
            result.affected_metrics.append("criticidade_distribution")

        # Recomendação de ação
        if result.drift_detected:
            result.recommended_action = self._recommend_action(result)

        return result

    def _recommend_action(self, drift: DriftDetection) -> str:
        """Gera recomendação de ação baseada no tipo de drift detectado."""
        actions = []

        if "quality_decline" in drift.drift_type:
            actions.append(
                "Revisar pipeline: qualidade em queda. "
                "Considerar recalibração de thresholds ou expansão do corpus."
            )

        if "confidence_drop" in drift.drift_type:
            actions.append(
                "Confiança dos agentes em queda. "
                "Verificar atualizações na ontologia ou dados de treinamento."
            )

        if "distribution_shift" in drift.drift_type:
            actions.append(
                "Mudança na distribuição de criticidade. "
                "Investigar se há novos padrões de query ou mudança no domínio."
            )

        if drift.severity > 0.7:
            actions.append(
                "ALERTA: Drift severo detectado. Recomenda-se avaliação manual imediata."
            )

        return " | ".join(actions) if actions else "Monitorar continuamente."


# ─────────────────────────────────────────────────────────────────────
# 4. FEEDBACK LOOP
# ─────────────────────────────────────────────────────────────────────

class FeedbackLoop:
    """
    Ciclo de retroalimentação que coleta, agrega e aplica feedback
    para melhorar o pipeline continuamente.

    Tipos de feedback:
    1. Explícito: avaliação manual do usuário (thumbs up/down, scores)
    2. Implícito: derivado de métricas de qualidade automáticas
    3. Diferido: feedback recebido após processamento assíncrono
    """

    def __init__(self, evaluator: SelfEvaluator, thresholds: AdaptiveThresholds):
        self.evaluator = evaluator
        self.thresholds = thresholds
        self._pending_feedback: List[Dict[str, Any]] = []
        self._feedback_history: List[Dict[str, Any]] = []
        self._max_feedback_history = 500

    def record_explicit_feedback(
        self,
        episode_id: str,
        score: float,           # -1.0 a 1.0
        comment: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Registra feedback explícito do usuário."""
        feedback = {
            "episode_id": episode_id,
            "type": "explicit",
            "score": max(-1.0, min(1.0, score)),
            "comment": comment,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._pending_feedback.append(feedback)
        self._feedback_history.append(feedback)
        self._trim_feedback_history()

        logger.info(
            "Feedback explícito registrado: episode=%s, score=%.3f",
            episode_id, score,
        )

    def record_implicit_feedback(self, metrics: QualityMetrics) -> None:
        """Registra feedback implícito derivado das métricas."""
        feedback = {
            "episode_id": metrics.episode_id,
            "type": "implicit",
            "score": metrics.implicit_feedback,
            "derived_from": {
                "quality": metrics.quality_score,
                "validation": metrics.validation_score,
                "coherence": metrics.coherence_score,
                "latency": metrics.total_latency_ms,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._pending_feedback.append(feedback)

    def _trim_feedback_history(self) -> None:
        """Limita o tamanho do histórico de feedback."""
        if len(self._feedback_history) > self._max_feedback_history:
            self._feedback_history = self._feedback_history[-self._max_feedback_history:]

    def get_aggregated_feedback(
        self,
        window: int = 50,
    ) -> Dict[str, float]:
        """
        Agrega feedback recente para calcular tendências.
        """
        recent = self._feedback_history[-window:]
        if not recent:
            return {"avg_score": 0.0, "count": 0, "positive_ratio": 0.0}

        scores = [f["score"] for f in recent]
        positive = sum(1 for s in scores if s > 0)
        negative = sum(1 for s in scores if s < 0)

        return {
            "avg_score": sum(scores) / len(scores),
            "count": len(scores),
            "positive_ratio": positive / len(scores),
            "negative_ratio": negative / len(scores),
            "std_dev": self._std_dev(scores),
        }

    @staticmethod
    def _std_dev(values: List[float]) -> float:
        """Calcula o desvio padrão de uma lista de valores."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)


# ─────────────────────────────────────────────────────────────────────
# 5. THRESHOLDS ADAPTATIVOS
# ─────────────────────────────────────────────────────────────────────

class ThresholdAdaptor:
    """
    Ajusta automaticamente os thresholds do pipeline com base em
    feedback acumulado e métricas históricas.

    Estratégia:
    - Se qualidade média > target + margem → aumentar threshold (exigir mais)
    - Se qualidade média < target - margem → diminuir threshold (ser mais permissivo)
    - Ajustes são incrementais e limitados por max_deviation
    """

    def __init__(
        self,
        thresholds: AdaptiveThresholds,
        target_quality: float = 0.75,
        adaptation_margin: float = 0.05,
    ):
        self.thresholds = thresholds
        self.target_quality = target_quality
        self.adaptation_margin = adaptation_margin
        self._adaptation_log: List[AdaptationEvent] = []

    def adapt(self, feedback_loop: FeedbackLoop) -> List[AdaptationEvent]:
        """
        Executa um ciclo de adaptação dos thresholds.

        Retorna a lista de eventos de adaptação realizados.
        """
        events = []

        # Só adapta se houver amostras suficientes
        if feedback_loop.evaluator.history_size < self.thresholds.min_samples_for_adaptation:
            logger.debug(
                "Amostras insuficientes (%d < %d) para adaptação",
                feedback_loop.evaluator.history_size,
                self.thresholds.min_samples_for_adaptation,
            )
            return events

        # Calcular qualidade média recente
        recent_quality = feedback_loop.evaluator.get_average_quality(window=50)
        target = self.target_quality
        margin = self.adaptation_margin
        rate = self.thresholds.adaptation_rate

        # Ajustar threshold de qualidade mínima
        if recent_quality > target + margin:
            # Qualidade consistentemente alta → aumentar exigência
            new_val = self.thresholds.min_quality_score + rate
            new_val = min(new_val, 1.0)
            self._apply_adaptation(
                "min_quality_score",
                self.thresholds.min_quality_score,
                new_val,
                "qualidade_alta",
                events,
            )

        elif recent_quality < target - margin:
            # Qualidade consistentemente baixa → reduzir exigência
            new_val = self.thresholds.min_quality_score - rate
            new_val = max(new_val, 0.2)  # Floor mínimo
            self._apply_adaptation(
                "min_quality_score",
                self.thresholds.min_quality_score,
                new_val,
                "qualidade_baixa",
                events,
            )

        # Ajustar threshold de validação
        validation_scores = [
            m.validation_score for m in feedback_loop.evaluator._history[-50:]
        ]
        if validation_scores:
            avg_validation = sum(validation_scores) / len(validation_scores)
            if avg_validation > target + margin:
                new_val = self.thresholds.min_validation_score + rate * 0.5
                new_val = min(new_val, 1.0)
                self._apply_adaptation(
                    "min_validation_score",
                    self.thresholds.min_validation_score,
                    new_val,
                    "validacao_alta",
                    events,
                )
            elif avg_validation < target - margin:
                new_val = self.thresholds.min_validation_score - rate * 0.5
                new_val = max(new_val, 0.3)
                self._apply_adaptation(
                    "min_validation_score",
                    self.thresholds.min_validation_score,
                    new_val,
                    "validacao_baixa",
                    events,
                )

        # Ajustar threshold semântico de retrieval
        retrieval_scores = [
            m.retrieval_relevance for m in feedback_loop.evaluator._history[-50:]
        ]
        if retrieval_scores:
            avg_retrieval = sum(retrieval_scores) / len(retrieval_scores)
            if avg_retrieval > 0.8:
                new_val = self.thresholds.semantic_similarity_min + rate * 0.2
                new_val = min(new_val, 0.95)
                self._apply_adaptation(
                    "semantic_similarity_min",
                    self.thresholds.semantic_similarity_min,
                    new_val,
                    "retrieval_alto",
                    events,
                )
            elif avg_retrieval < 0.5:
                new_val = self.thresholds.semantic_similarity_min - rate * 0.2
                new_val = max(new_val, 0.4)
                self._apply_adaptation(
                    "semantic_similarity_min",
                    self.thresholds.semantic_similarity_min,
                    new_val,
                    "retrieval_baixo",
                    events,
                )

        # Ajustar threshold de ambiguidade
        feedback_agg = feedback_loop.get_aggregated_feedback(window=50)
        if feedback_agg["count"] > 10:
            std = feedback_agg.get("std_dev", 0)
            if std > 0.3:
                # Alta variabilidade → reduzir ambiguidade permitida
                new_val = self.thresholds.max_ambiguity_ratio - rate
                new_val = max(new_val, 0.05)
                self._apply_adaptation(
                    "max_ambiguity_ratio",
                    self.thresholds.max_ambiguity_ratio,
                    new_val,
                    "alta_variabilidade",
                    events,
                )

        # Logar adaptações
        for event in events:
            logger.info(
                "Adaptação: %s %.4f → %.4f (%s)",
                event.parameter, event.old_value, event.new_value, event.rationale,
            )

        return events

    def _apply_adaptation(
        self,
        param: str,
        old_val: float,
        new_val: float,
        trigger: str,
        events: List[AdaptationEvent],
    ) -> None:
        """Aplica uma adaptação individual com controle de desvio máximo."""
        deviation = abs(new_val - old_val)
        max_dev = self.thresholds.max_deviation

        # Limitar variação por ciclo
        if deviation > max_dev:
            if new_val > old_val:
                new_val = old_val + max_dev
            else:
                new_val = old_val - max_dev

        # Só registrar se houver mudança efetiva
        if abs(new_val - old_val) > 1e-6:
            setattr(self.thresholds, param, round(new_val, 4))
            events.append(AdaptationEvent(
                timestamp=datetime.now(timezone.utc).isoformat(),
                trigger=trigger,
                parameter=param,
                old_value=old_val,
                new_value=round(new_val, 4),
                rationale=f"Adaptação automática: {trigger}",
            ))


# ─────────────────────────────────────────────────────────────────────
# 6. CONTROLE DE QUALIDADE
# ─────────────────────────────────────────────────────────────────────

class Decision:
    """Verdictos possíveis do controle de qualidade."""
    ACCEPT = "accept"
    REJECT = "reject"
    RETAKE = "retake"


class QualityController:
    """
    Controlador de qualidade que decide se uma resposta deve ser
    aceita, rejeitada ou re-processada.

    Implementa uma máquina de estados com três saídas:
    - ACCEPT: resposta atende aos critérios
    - REJECT: resposta falhou criticamente
    - RETAKE: resposta pode ser melhorada com re-síntese
    """

    def __init__(self, thresholds: AdaptiveThresholds):
        self.thresholds = thresholds
        self._decisions: List[Dict[str, Any]] = []

    def evaluate(self, metrics: QualityMetrics) -> Tuple[str, Dict[str, Any]]:
        """
        Avalia se a resposta do pipeline atende aos critérios de qualidade.

        Returns:
            Tupla (decisão, detalhes)
        """
        details: Dict[str, Any] = {
            "quality_score": metrics.quality_score,
            "checks": [],
            "reasons": [],
        }

        # Check 1: Score de qualidade mínimo
        if metrics.quality_score < self.thresholds.min_quality_score:
            details["checks"].append(("min_quality", False))
            details["reasons"].append(
                f"Quality score {metrics.quality_score:.3f} < "
                f"threshold {self.thresholds.min_quality_score:.3f}"
            )
        else:
            details["checks"].append(("min_quality", True))

        # Check 2: Score de validação
        if metrics.validation_score < self.thresholds.min_validation_score:
            details["checks"].append(("min_validation", False))
            details["reasons"].append(
                f"Validation score {metrics.validation_score:.3f} < "
                f"threshold {self.thresholds.min_validation_score:.3f}"
            )
        else:
            details["checks"].append(("min_validation", True))

        # Check 3: Classificação confiante
        if metrics.classification_confidence < self.thresholds.min_classification_confidence:
            details["checks"].append(("classification_confidence", False))
            details["reasons"].append(
                f"Classification confidence {metrics.classification_confidence:.3f} < "
                f"threshold {self.thresholds.min_classification_confidence:.3f}"
            )
        else:
            details["checks"].append(("classification_confidence", True))

        # Check 4: Síntese confiante
        if metrics.synthesis_confidence < self.thresholds.min_synthesis_confidence:
            details["checks"].append(("synthesis_confidence", False))
            details["reasons"].append(
                f"Synthesis confidence {metrics.synthesis_confidence:.3f} < "
                f"threshold {self.thresholds.min_synthesis_confidence:.3f}"
            )
        else:
            details["checks"].append(("synthesis_confidence", True))

        # Check 5: Validation aprovada
        if not metrics.validation_aprovado:
            details["checks"].append(("validation_approved", False))
            details["reasons"].append(
                f"Validation not approved (criticidade={metrics.validation_criticidade})"
            )
        else:
            details["checks"].append(("validation_approved", True))

        # Check 6: Retrieval mínimo
        if metrics.num_retrieved_cells < self.thresholds.min_cells_for_synthesis:
            details["checks"].append(("min_cells", False))
            details["reasons"].append(
                f"Only {metrics.num_retrieved_cells} cells retrieved "
                f"(minimum {self.thresholds.min_cells_for_synthesis})"
            )
        else:
            details["checks"].append(("min_cells", True))

        # Check 7: Coerência mínima
        if metrics.coherence_score < 0.5:
            details["checks"].append(("coherence", False))
            details["reasons"].append(
                f"Coherence score {metrics.coherence_score:.3f} below 0.5"
            )
        else:
            details["checks"].append(("coherence", True))

        # Decisão
        passed_checks = sum(1 for _, passed in details["checks"] if passed)
        total_checks = len(details["checks"])
        pass_ratio = passed_checks / total_checks if total_checks > 0 else 0

        if pass_ratio >= 0.85:
            decision = Decision.ACCEPT
        elif pass_ratio >= 0.5:
            decision = Decision.RETAKE
        else:
            decision = Decision.REJECT

        details["decision"] = decision
        details["pass_ratio"] = round(pass_ratio, 4)
        details["passed_checks"] = passed_checks
        details["total_checks"] = total_checks

        # Registrar decisão
        self._decisions.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision": decision,
            "details": details,
        })

        return decision, details

    def get_decision_stats(self) -> Dict[str, int]:
        """Retorna estatísticas das decisões."""
        stats = {"accept": 0, "reject": 0, "retake": 0}
        for d in self._decisions:
            decision = d.get("decision", "")
            if decision in stats:
                stats[decision] += 1
        stats["total"] = len(self._decisions)
        return stats


# ─────────────────────────────────────────────────────────────────────
# 7. ORCHESTRADOR DE AUTONOMIA
# ─────────────────────────────────────────────────────────────────────

class AutonomyLayer:
    """
    Camada de autonomia que integra auto-avaliação, feedback loops
    e thresholds adaptativos em um sistema coeso.

    Este é o sistema nervoso central do pipeline cognitivo:
    - Recebe resultados do pipeline multi-agente
    - Avalia qualidade automaticamente
    - Detecta drift e degradação
    - Ajusta thresholds adaptativamente
    - Coleta e agrega feedback
    - Decide aceitar/rejeitar/re-processar
    """

    def __init__(
        self,
        thresholds: Optional[AdaptiveThresholds] = None,
        target_quality: float = 0.75,
        adaptation_margin: float = 0.05,
        baseline_window: int = 100,
        detection_window: int = 20,
    ):
        self.thresholds = thresholds or AdaptiveThresholds()
        self.evaluator = SelfEvaluator(self.thresholds)
        self.drift_detector = DriftDetector(
            baseline_window=baseline_window,
            detection_window=detection_window,
        )
        self.feedback_loop = FeedbackLoop(self.evaluator, self.thresholds)
        self.threshold_adaptor = ThresholdAdaptor(
            self.thresholds,
            target_quality=target_quality,
            adaptation_margin=adaptation_margin,
        )
        self.quality_controller = QualityController(self.thresholds)

        # Estado interno
        self._episode_count = 0
        self._total_processed = 0
        self._total_accepted = 0
        self._total_rejected = 0
        self._total_retaken = 0

        logger.info(
            "AutonomyLayer inicializado: target_quality=%.2f, adaptation_margin=%.3f",
            target_quality, adaptation_margin,
        )

    def process_result(self, pipeline_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa o resultado do pipeline multi-agente.

        Este é o método principal chamado após cada execução do pipeline.
        Realiza avaliação, controle de qualidade e registro.

        Args:
            pipeline_result: Resultado completo do MultiAgentPipelineResult.to_dict()

        Returns:
            Dict com decisão, métricas e recomendações.
        """
        t0 = time.time()

        # 1. Avaliar qualidade
        metrics = self.evaluator.evaluate(pipeline_result)
        self.evaluator.add_to_history(metrics)
        self._episode_count += 1

        # 2. Controlar qualidade
        decision, decision_details = self.quality_controller.evaluate(metrics)

        # 3. Atualizar contadores
        self._total_processed += 1
        if decision == Decision.ACCEPT:
            self._total_accepted += 1
        elif decision == Decision.REJECT:
            self._total_rejected += 1
        else:
            self._total_retaken += 1

        # 4. Detectar drift
        drift = self.drift_detector.detect(self.evaluator)

        # 5. Adaptar thresholds (periodicamente)
        adaptation_events = []
        if self._episode_count % 10 == 0:  # A cada 10 episódios
            adaptation_events = self.threshold_adaptor.adapt(self.feedback_loop)

        # 6. Construir resultado
        processing_time = (time.time() - t0) * 1000
        result = {
            "episode_id": metrics.episode_id,
            "episode_number": self._episode_count,
            "decision": decision,
            "decision_details": decision_details,
            "quality_metrics": metrics.to_dict(),
            "drift": drift.to_dict(),
            "adaptation_events": [e.to_dict() for e in adaptation_events],
            "thresholds_snapshot": self.thresholds.to_dict(),
            "processing_time_ms": round(processing_time, 2),
            "statistics": self.get_statistics(),
        }

        logger.info(
            "Episódio %d: decisão=%s, qualidade=%.3f, drift=%s",
            self._episode_count, decision,
            metrics.quality_score,
            "detectado" if drift.drift_detected else "nenhum",
        )

        return result

    def add_feedback(self, episode_id: str, score: float, comment: Optional[str] = None) -> None:
        """Adiciona feedback explícito do usuário."""
        self.feedback_loop.record_explicit_feedback(episode_id, score, comment)

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas gerais do AutonomyLayer."""
        feedback_agg = self.feedback_loop.get_aggregated_feedback()
        decision_stats = self.quality_controller.get_decision_stats()

        return {
            "total_episodes": self._episode_count,
            "total_processed": self._total_processed,
            "accepted": self._total_accepted,
            "rejected": self._total_rejected,
            "retaken": self._total_retaken,
            "acceptance_rate": (
                self._total_accepted / self._total_processed
                if self._total_processed > 0 else 0.0
            ),
            "avg_quality_10": self.evaluator.get_average_quality(10),
            "avg_quality_50": self.evaluator.get_average_quality(50),
            "avg_quality_all": self.evaluator.get_average_quality(
                self.evaluator.history_size
            ),
            "feedback_stats": feedback_agg,
            "decision_stats": decision_stats,
            "current_thresholds": {
                "min_quality": self.thresholds.min_quality_score,
                "min_validation": self.thresholds.min_validation_score,
                "min_classification_conf": self.thresholds.min_classification_confidence,
                "semantic_similarity_min": self.thresholds.semantic_similarity_min,
            },
        }

    def get_health_report(self) -> Dict[str, Any]:
        """
        Gera relatório de saúde do sistema autônomo.
        """
        stats = self.get_statistics()
        drift = self.drift_detector.detect(self.evaluator)

        # Determinar saúde geral
        issues = []
        if drift.drift_detected:
            issues.append(f"Drift detectado: {drift.drift_type}")
        if stats["acceptance_rate"] < 0.5:
            issues.append("Taxa de aceitação baixa (<50%)")
        if stats["avg_quality_10"] < self.thresholds.min_quality_score:
            issues.append("Qualidade recente abaixo do threshold")

        health_status = "healthy"
        if len(issues) >= 2:
            health_status = "critical"
        elif len(issues) == 1:
            health_status = "warning"

        return {
            "status": health_status,
            "issues": issues,
            "statistics": stats,
            "drift": drift.to_dict(),
            "recommendations": self._generate_recommendations(issues, drift),
        }

    def _generate_recommendations(
        self,
        issues: List[str],
        drift: DriftDetection,
    ) -> List[str]:
        """Gera recomendações baseadas nos problemas detectados."""
        recommendations = []

        if drift.drift_detected:
            recommendations.append(
                f"Investigar drift: {drift.drift_type}. "
                f"Severidade: {drift.severity:.2f}. "
                f"Ação sugerida: {drift.recommended_action}"
            )

        if any("aceitação" in i for i in issues):
            recommendations.append(
                "Revisar thresholds de qualidade. "
                "Considere reduzir min_quality_score temporariamente "
                "enquanto investiga a causa raiz."
            )

        if any("qualidade" in i.lower() for i in issues):
            recommendations.append(
                "Qualidade em queda. Verificar: "
                "(1) dados de treinamento, "
                "(2) completude do registry ontológico, "
                "(3) qualidade dos embeddings."
            )

        if not recommendations:
            recommendations.append("Sistema operando normalmente. Nenhuma ação necessária.")

        return recommendations

    def reset(self) -> None:
        """Reseta o estado do AutonomyLayer (útil para testes)."""
        self.evaluator._history.clear()
        self.feedback_loop._pending_feedback.clear()
        self.feedback_loop._feedback_history.clear()
        self.quality_controller._decisions.clear()
        self._episode_count = 0
        self._total_processed = 0
        self._total_accepted = 0
        self._total_rejected = 0
        self._total_retaken = 0

    def to_dict(self) -> Dict[str, Any]:
        """Serializa o estado completo do AutonomyLayer."""
        return {
            "episode_count": self._episode_count,
            "statistics": self.get_statistics(),
            "thresholds": self.thresholds.to_dict(),
            "health": self.get_health_report(),
        }


# ─────────────────────────────────────────────────────────────────────
# 8. INTEGRAÇÃO COM PIPELINE
# ─────────────────────────────────────────────────────────────────────

class AutonomousPipeline:
    """
    Wrapper que combina o MultiAgentOrchestrator com o AutonomyLayer,
    criando um pipeline cognitivo totalmente autônomo.

    Fluxo:
    Query → Orchestrator → AutonomyLayer → Decisão → (Retake se necessário)
    """

    def __init__(
        self,
        orchestrator: Optional[Any] = None,
        autonomy_layer: Optional[AutonomyLayer] = None,
        max_retakes: int = 2,
    ):
        # Importação tardia para evitar circular
        if orchestrator is None:
            from .multi_agent_orchestrator import MultiAgentOrchestrator
            self.orchestrator = MultiAgentOrchestrator()
        else:
            self.orchestrator = orchestrator

        self.autonomy_layer = autonomy_layer or AutonomyLayer()
        self.max_retakes = max_retakes

    def run(self, query: str, mode: str = "full") -> Dict[str, Any]:
        """
        Executa o pipeline autônomo com auto-avaliação.

        Args:
            query: Query do usuário
            mode: "full" ou "simple"

        Returns:
            Dict com resultado final, incluindo decisão de qualidade.
        """
        # Executar pipeline
        if mode == "full":
            pipeline_result = self.orchestrator.full_pipeline(query)
        else:
            pipeline_result = self.orchestrator.simple_pipeline(query)

        result_dict = pipeline_result.to_dict()

        # Auto-avaliação
        autonomy_result = self.autonomy_layer.process_result(result_dict)

        # Se rejeitado e temos retakes disponíveis, tentar novamente
        retake_count = 0
        while (
            autonomy_result["decision"] == "reject"
            and retake_count < self.max_retakes
        ):
            retake_count += 1
            logger.info(
                "Retake %d/%d para query: %s",
                retake_count, self.max_retakes, query[:50],
            )

            # Modificar levemente o contexto para tentar resultado diferente
            # (em implementação completa, poderia ajustar parâmetros)
            if mode == "full":
                pipeline_result = self.orchestrator.full_pipeline(query)
            else:
                pipeline_result = self.orchestrator.simple_pipeline(query)

            result_dict = pipeline_result.to_dict()
            autonomy_result = self.autonomy_layer.process_result(result_dict)

        # Consolidar resultado final
        return {
            "query": query,
            "pipeline_result": result_dict,
            "autonomy_result": autonomy_result,
            "retakes": retake_count,
            "final_decision": autonomy_result["decision"],
        }

    def add_feedback(self, episode_id: str, score: float, comment: Optional[str] = None) -> None:
        """Registra feedback do usuário para aprendizado contínuo."""
        self.autonomy_layer.add_feedback(episode_id, score, comment)

    def get_health(self) -> Dict[str, Any]:
        """Verifica saúde do sistema autônomo."""
        return self.autonomy_layer.get_health_report()

    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema."""
        return self.autonomy_layer.get_statistics()


# ─────────────────────────────────────────────────────────────────────
# 9. PONTO DE ENTRADA PARA TESTES
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("INICIALIZANDO AUTONOMY LAYER...")
    print("=" * 60)

    # Testar AutonomyLayer isoladamente
    autonomy = AutonomyLayer()

    # Simular resultados de pipeline para testar avaliação
    sample_result = {
        "query": "Como decompor um problema complexo?",
        "pipeline_mode": "full",
        "total_latency_ms": 1250.0,
        "steps": [
            {
                "step": "classifier",
                "agent_name": "ClassifierAgent",
                "success": True,
                "confidence": 0.85,
                "output": {
                    "classification": {
                        "classificacao": {
                            "n0_eixo": {"eixo": "SINTRÓPICO"},
                            "n1_pilar": {"pilar": "LOGOS", "score": 0.85},
                            "n2_dominio": {"dominio": "ALGORITMIA"},
                            "n3_subarvore": {"subarvore": "RESOLUÇÃO"},
                            "n4_celula": {"uid": "N4_DECOMPOSICAO", "nome": "Decomposição"},
                        }
                    }
                },
            },
            {
                "step": "router",
                "agent_name": "CognitiveRouter",
                "success": True,
                "confidence": 0.90,
                "output": {
                    "routing": {
                        "pilar": "LOGOS",
                        "dominio": "ALGORITMIA",
                        "estrategia": "analitica",
                        "score": 0.90,
                    }
                },
            },
            {
                "step": "retriever",
                "agent_name": "HybridRetriever",
                "success": True,
                "confidence": 0.75,
                "output": {
                    "retrieved_cells": [
                        {"uid": "N4_DECOMPOSICAO", "nome": "Decomposição", "score": 0.92},
                        {"uid": "N4_SEQUENCIA", "nome": "Sequência", "score": 0.78},
                        {"uid": "N4_CASO_BASE", "nome": "Caso Base", "score": 0.65},
                    ]
                },
            },
            {
                "step": "synthesis",
                "agent_name": "SynthesisAgent",
                "success": True,
                "confidence": 0.80,
                "output": {
                    "synthesis": {
                        "prompt": "Analise o conceito de decomposição...",
                        "context_summary": "Resposta sobre decomposição de problemas",
                        "cell_references": ["N4_DECOMPOSICAO", "N4_SEQUENCIA"],
                        "metadata": {},
                    }
                },
            },
            {
                "step": "validator",
                "agent_name": "ValidatorAgent",
                "success": True,
                "confidence": 0.88,
                "output": {
                    "validation": {
                        "aprovado": True,
                        "score_geral": 0.82,
                        "criticidade": "baixa",
                        "verificacoes": [
                            {"tipo": "eixo_coerente", "passou": True, "score": 0.9},
                            {"tipo": "conceitos_validos", "passou": True, "score": 0.85},
                            {"tipo": "relacoes_consistentes", "passou": True, "score": 0.8},
                        ],
                    }
                },
            },
        ],
    }

    print("\nTestando avaliação de resultado simulado...")
    result = autonomy.process_result(sample_result)

    print(f"\nDecisão: {result['decision'].upper()}")
    print(f"Quality Score: {result['quality_metrics']['scores']['quality']:.4f}")
    print(f"Coerência: {result['quality_metrics']['composites']['coherence']:.4f}")
    print(f"Consistência: {result['quality_metrics']['composites']['consistency']:.4f}")
    print(f"Drift detectado: {result['drift']['drift_detected']}")

    print("\n--- Estatísticas ---")
    stats = autonomy.get_statistics()
    for key, value in stats.items():
        if not isinstance(value, dict):
            print(f"  {key}: {value}")

    print("\n--- Relatório de Saúde ---")
    health = autonomy.get_health_report()
    print(f"Status: {health['status']}")
    if health["issues"]:
        print(f"Issues: {health['issues']}")
    if health["recommendations"]:
        print("Recomendações:")
        for rec in health["recommendations"]:
            print(f"  - {rec}")

    print("\n" + "=" * 60)
    print("AUTONOMY LAYER TESTADO COM SUCESSO")
    print("=" * 60)
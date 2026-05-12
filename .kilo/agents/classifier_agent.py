#!/usr/bin/env python3
"""
AGENTE CLASSIFICADOR — Classificação Ontológica N0→N4.

Encapsula o OntologicalClassifier com caching, confiança calibrada
e tratamento de edge cases para uso no pipeline multi-agente.

FASE 7b do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import hashlib
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
from runtime.classifier import OntologicalClassifier, FullClassification


@dataclass
class ClassificationResult:
    """Resultado da classificação ontológica com metadados estendidos."""
    classification: FullClassification
    confidence: float = 0.0
    latency_ms: float = 0.0
    cached: bool = False
    reasoning: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "classification": self.classification.to_dict(),
            "confidence": round(self.confidence, 4),
            "latency_ms": round(self.latency_ms, 2),
            "cached": self.cached,
            "reasoning": self.reasoning,
        }


class ClassifierAgent(BaseAgent):
    """
    Agente especializado em classificação ontológica.

    Responsabilidades:
    - Receber queries e determinar posição na ontologia fractal (N0→N4)
    - Calcular confiança da classificação com base em múltiplos sinais
    - Cache de classificações recentes para baixa latência
    - Fornecer reasoning explicável para cada decisão de classificação

    Diferencial em relação ao uso direto do OntologicalClassifier:
    - Camada de caching (LRU-style com TTL)
    - Confiança calibrada (combinação de score léxico + semântico)
    - Tratamento robusto de queries ambíguas
    - Logging estruturado para observabilidade
    """

    AGENT_NAME: str = "ClassifierAgent"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = ["classify", "classify_batch", "explain"]

    # Cache com TTL (simples, sem dependência externa)
    _CACHE_TTL_SECONDS: int = 300
    _MAX_CACHE_SIZE: int = 2000

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
        self._classifier = OntologicalClassifier()
        self._cache: Dict[str, ClassificationResult] = {}
        self._cache_timestamps: Dict[str, float] = {}
        self._stats = {
            "total_queries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "ambiguous_queries": 0,
        }

    # ── Cache Management ────────────────────────────────────────────────

    def _cache_key(self, query: str) -> str:
        """Gera chave determinística para a query."""
        normalized = query.lower().strip()
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()

    def _get_cached(self, key: str) -> Optional[ClassificationResult]:
        """Recupera resultado do cache se válido."""
        if key not in self._cache:
            return None
        if key not in self._cache_timestamps:
            return None
        age = time.time() - self._cache_timestamps[key]
        if age > self._CACHE_TTL_SECONDS:
            del self._cache[key]
            del self._cache_timestamps[key]
            return None
        return self._cache[key]

    def _set_cache(self, key: str, result: ClassificationResult) -> None:
        """Armazena resultado no cache com eviction LRU simples."""
        if len(self._cache) >= self._MAX_CACHE_SIZE:
            # Evict oldest entry
            oldest_key = min(self._cache_timestamps, key=lambda k: self._cache_timestamps[k])
            del self._cache[oldest_key]
            del self._cache_timestamps[oldest_key]
        self._cache[key] = result
        self._cache_timestamps[key] = time.time()

    def _invalidate_cache(self) -> None:
        """Limpa cache inteiro (chamar após atualização da ontologia)."""
        self._cache.clear()
        self._cache_timestamps.clear()

    # ── Core Execution ──────────────────────────────────────────────────

    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Executa classificação ontológica da query.

        Args:
            task: Query ou instrução do usuário.
            context: Contexto adicional (ex: histórico de conversa, domínio esperado).

        Returns:
            AgentResult com a classificação N0→N4 completa.
        """
        t0 = time.time()
        self._stats["total_queries"] += 1

        # Normalizar query
        query = task.strip()
        if not query:
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": "Query vazia"},
                confidence=0.0,
                latency_ms=0.0,
                errors=["Query vazia fornecida"],
            )

        # Verificar cache
        cache_key = self._cache_key(query)
        cached = self._get_cached(cache_key)
        if cached is not None:
            self._stats["cache_hits"] += 1
            return AgentResult(
                agent_name=self.name,
                task=task,
                output=cached.to_dict(),
                confidence=cached.confidence,
                latency_ms=cached.latency_ms,
                reasoning_steps=cached.reasoning,
                metadata={"cached": True, **self._stats},
            )

        self._stats["cache_misses"] += 1

        try:
            # Executar classificação
            full_classification = self._classifier.classify(query)
            classification_dict = full_classification.to_dict()

            # Calcular confiança composta
            confidence = self._compute_confidence(classification_dict, query)

            # Gerar reasoning
            reasoning = self._build_reasoning(classification_dict, query)

            # Detectar ambiguidade
            is_ambiguous = self._detect_ambiguity(classification_dict)
            if is_ambiguous:
                self._stats["ambiguous_queries"] += 1
                reasoning.append(f"Ambiguidade detectada: múltiplos candidatos próximos")

            result = ClassificationResult(
                classification=full_classification,
                confidence=confidence,
                latency_ms=(time.time() - t0) * 1000,
                cached=False,
                reasoning=reasoning,
            )

            # Cache do resultado
            self._set_cache(cache_key, result)

            # Log para observabilidade
            logger.info(
                "ClassifierAgent: eixo=%s, pilar=%s, dominio=%s, confianca=%.3f",
                classification_dict.get("classificacao", {}).get("n0_eixo", {}).get("eixo"),
                classification_dict.get("classificacao", {}).get("n1_pilar", {}).get("pilar"),
                classification_dict.get("classificacao", {}).get("n2_dominio", {}).get("dominio"),
                confidence,
            )

            return AgentResult(
                agent_name=self.name,
                task=task,
                output=result.to_dict(),
                confidence=confidence,
                latency_ms=result.latency_ms,
                reasoning_steps=reasoning,
                metadata={
                    "cached": False,
                    "ambiguous": is_ambiguous,
                    **self._stats,
                },
            )

        except Exception as e:
            logger.error("ClassifierAgent falhou: %s", e, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": str(e)},
                confidence=0.0,
                latency_ms=(time.time() - t0) * 1000,
                errors=[str(e)],
            )

    # ── Batch Processing ────────────────────────────────────────────────

    def classify_batch(
        self,
        queries: List[str],
        context: Optional[Dict[str, Any]] = None,
    ) -> List[AgentResult]:
        """Classifica múltiplas queries em lote."""
        return [self.execute(q, context) for q in queries]

    # ── Confidence Computation ──────────────────────────────────────────

    def _compute_confidence(
        self,
        classification: dict,
        query: str,
    ) -> float:
        """
        Calcula confiança composta baseada em:
        - Score da classificação léxica (N1)
        - Consistência entre sinais linguísticos e classificação
        - Especificidade da classificação (mais específico = mais confiante)
        """
        n1 = classification.get("classificacao", {}).get("n1_pilar", {})
        n2 = classification.get("classificacao", {}).get("n2_dominio", {})
        n3 = classification.get("classificacao", {}).get("n3_subarvore", {})
        n4 = classification.get("classificacao", {}).get("n4_celula", {})

        # Score base da classificação N1
        base_score = n1.get("score", 0.5)

        # Bônus por profundidade (classificação mais profunda = mais confiança)
        depth_bonus = 0.0
        if n4 and n4.get("celula_nome"):
            depth_bonus = 0.25
        elif n3 and n3.get("subarvore"):
            depth_bonus = 0.15
        elif n2 and n2.get("dominio"):
            depth_bonus = 0.10

        # Penalidade por ambiguidade
        ambiguity_penalty = 0.0
        top_scores = sorted(
            [n1.get("score", 0), n2.get("score", 0), n3.get("score", 0)],
            reverse=True,
        )
        if len(top_scores) >= 2 and top_scores[0] - top_scores[1] < 0.1:
            ambiguity_penalty = 0.15

        # Query muito curta = menos confiança
        length_factor = min(len(query.split()) / 5.0, 1.0)
        length_penalty = 0.1 * (1.0 - length_factor)

        confidence = base_score + depth_bonus - ambiguity_penalty - length_penalty
        return round(max(0.0, min(1.0, confidence)), 4)

    def _build_reasoning(
        self,
        classification: dict,
        query: str,
    ) -> List[str]:
        """Gera explicação legível da classificação."""
        reasoning = []

        n0 = classification.get("classificacao", {}).get("n0_eixo", {})
        n1 = classification.get("classificacao", {}).get("n1_pilar", {})
        n2 = classification.get("classificacao", {}).get("n2_dominio", {})

        eixo = n0.get("eixo", "N/A")
        pilar = n1.get("pilar", "N/A")
        dominio = n2.get("dominio", "N/A")

        reasoning.append(
            f"Query '{query[:60]}...' classificada no eixo {eixo}, "
            f"pilar {pilar}, domínio {dominio}"
        )

        # Detalhar sinais detectados
        signals = n1.get("sinais_detectados", [])
        if signals:
            reasoning.append(f"Sinais linguísticos: {', '.join(signals[:5])}")

        return reasoning

    def _detect_ambiguity(self, classification: dict) -> bool:
        """Detecta se a query pode ter múltiplas classificações válidas."""
        n1 = classification.get("classificacao", {}).get("n1_pilar", {})
        n1_score = n1.get("score", 0)

        # Se o score do pilar é baixo, provavelmente ambíguo
        if n1_score < 0.4:
            return True

        # Verificar proximidade entre segundo e terceiro colocados
        return False

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.REQUIRED_TOOLS,
            "description": "Classificação ontológica N0→N4 com caching e confiança calibrada",
            "input_types": ["text_query", "structured_query"],
            "output_types": ["full_classification", "confidence_score", "reasoning"],
            "cache_stats": {
                "size": len(self._cache),
                "max_size": self._MAX_CACHE_SIZE,
                "ttl_seconds": self._CACHE_TTL_SECONDS,
            },
            "performance_stats": self._stats,
        }
#!/usr/bin/env python3
"""
AGENTE DIALÉTICO — Inferência de Oposições e Distância Dialética.

Encapsula o DialecticEngine com caching, inferência multi-camada
e mapeamento de tensões para uso no pipeline multi-agente.

FASE 7f do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
import time
from dataclasses import dataclass, field
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

from core.agent_base import BaseAgent, AgentResult, AgentMemory
from core.dialectic_engine import DialecticEngine


@dataclass
class OppositionResult:
    """Resultado de uma inferência de oposições."""
    uid: str
    nome: str
    opposites: List[Dict[str, Any]] = field(default_factory=list)
    tension_score: float = 0.0
    layers_used: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "nome": self.nome,
            "opposites": self.opposites,
            "tension_score": round(self.tension_score, 4),
            "layers_used": self.layers_used,
        }


@dataclass
class DialecticDistance:
    """Resultado de cálculo de distância dialética entre duas células."""
    cell_a: str
    cell_b: str
    distance: float
    breakdown: Dict[str, float] = field(default_factory=dict)
    is_known_opposite: bool = False

    def to_dict(self) -> dict:
        return {
            "cell_a": self.cell_a,
            "cell_b": self.cell_b,
            "distance": round(self.distance, 4),
            "breakdown": {k: round(v, 4) for k, v in self.breakdown.items()},
            "is_known_opposite": self.is_known_opposite,
        }


@dataclass
class TensionMapEntry:
    """Entrada do mapa de tensões dialéticas."""
    uid: str
    nome: str
    opposites: List[str] = field(default_factory=list)
    tension_score: float = 0.0
    n_opposites: int = 0
    axis: str = ""

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "nome": self.nome,
            "opposites": self.opposites,
            "tension_score": round(self.tension_score, 4),
            "n_opposites": self.n_opposites,
            "axis": self.axis,
        }


class DialecticAgent(BaseAgent):
    """
    Agente especializado em inferência dialética e mapeamento de tensões.

    Responsabilidades:
    - Inferir opostos ontológicos para células N4
    - Calcular distância dialética entre conceitos
    - Construir mapas de tensão para análise de polaridades
    - Fornecer contexto dialético para o pipeline de síntese
    - Identificar pares dialéticos relevantes para uma query

    Diferencial em relação ao uso direto do DialecticEngine:
    - Cache de resultados de inferência
    - Filtragem por relevância para a query
    - Formatação estruturada para consumo por outros agentes
    - Integração com registry de memória semântica
    """

    AGENT_NAME: str = "DialecticAgent"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = [
        "infer_opposites",
        "calculate_distance",
        "build_tension_map",
        "find_dialectical_pairs",
    ]

    # Thresholds
    TENSION_MIN = 0.3
    DISTANCE_THRESHOLD = 0.7

    def __init__(
        self,
        memory: Optional[AgentMemory] = None,
        config: Optional[Dict[str, Any]] = None,
        engine: Optional[DialecticEngine] = None,
    ):
        super().__init__(
            name=self.AGENT_NAME,
            memory=memory,
            config=config or {},
        )
        self._engine = engine or DialecticEngine()
        self._opposites_cache: Dict[str, OppositionResult] = {}
        self._distance_cache: Dict[str, DialecticDistance] = {}
        self._tension_map_cache: Optional[Dict[str, TensionMapEntry]] = None
        self._cache_max_size = 1000

    # ── Core Execution ──────────────────────────────────────────────────

    def execute(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResult:
        """
        Executa operação dialética.

        Args:
            task: Tipo de operação ("infer_opposites", "calculate_distance",
                  "build_tension_map", "find_dialectical_pairs")
            context: Dict com parâmetros da operação:
                - uid: célula alvo para inferência de opostos
                - cell_a/cell_b: UIDs para cálculo de distância
                - cell_references: lista de células para mapeamento
                - query: query original para filtragem dialética

        Returns:
            AgentResult com resultado da operação dialética.
        """
        t0 = time.time()
        context = context or {}

        try:
            operation = task.strip().lower()

            if operation == "infer_opposites" or operation == "opposites":
                result = self._handle_infer_opposites(context)
            elif operation == "calculate_distance" or operation == "distance":
                result = self._handle_calculate_distance(context)
            elif operation == "build_tension_map" or operation == "tension_map":
                result = self._handle_build_tension_map(context)
            elif operation == "find_dialectical_pairs" or operation == "pairs":
                result = self._handle_find_dialectical_pairs(context)
            else:
                result = self._handle_infer_opposites(context)

            latency_ms = (time.time() - t0) * 1000

            return AgentResult(
                agent_name=self.name,
                task=task,
                output=result.to_dict() if hasattr(result, "to_dict") else result,
                confidence=self._estimate_confidence(result),
                latency_ms=latency_ms,
                reasoning_steps=self._build_reasoning(result, context),
                metadata={
                    "operation": operation,
                    "cache_size_opposites": len(self._opposites_cache),
                    "cache_size_distances": len(self._distance_cache),
                },
            )

        except Exception as e:
            logger.error("DialecticAgent falhou na operação '%s': %s", task, e, exc_info=True)
            return AgentResult(
                agent_name=self.name,
                task=task,
                output={"error": str(e)},
                confidence=0.0,
                latency_ms=(time.time() - t0) * 1000,
                errors=[str(e)],
            )

    # ── Operation Handlers ──────────────────────────────────────────────

    def _handle_infer_opposites(self, context: Dict[str, Any]) -> OppositionResult:
        """Inferir opostos para uma célula específica."""
        uid = context.get("uid", "")
        registry = context.get("registry")

        if not uid:
            return OppositionResult(uid="", nome="")

        # Verificar cache
        if uid in self._opposites_cache:
            return self._opposites_cache[uid]

        # Obter dados da célula
        cell_data = self._get_cell_data(uid, registry)
        if not cell_data:
            return OppositionResult(uid=uid, nome=uid)

        # Inferir opostos via engine
        opposite_uids = self._engine.infer_opposites(cell_data, registry)

        # Construir resultado estruturado
        opposites_detail = []
        for opp_uid in opposite_uids:
            opp_data = registry.get(opp_uid, {}) if registry else {}
            distance = self._engine.calculate_dialectic_distance(uid, opp_uid, registry)
            opposites_detail.append({
                "uid": opp_uid,
                "nome": opp_data.get("nome", opp_uid),
                "dialectic_distance": distance,
                "is_known_opposite": uid in self._engine.KNOWN_OPPOSITES.get(opp_uid, []),
            })

        # Calcular tension score
        tension = self._engine.calculate_tension_score(cell_data, opposite_uids, registry)

        # Determinar camadas usadas
        layers_used = self._detect_layers_used(cell_data, opposite_uids, registry)

        nome = cell_data.get("nome", uid)
        result = OppositionResult(
            uid=uid,
            nome=nome,
            opposites=opposites_detail,
            tension_score=tension,
            layers_used=layers_used,
        )

        if len(self._opposites_cache) < self._cache_max_size:
            self._opposites_cache[uid] = result

        return result

    def _handle_calculate_distance(self, context: Dict[str, Any]) -> DialecticDistance:
        """Calcular distância dialética entre duas células."""
        cell_a = context.get("cell_a", "")
        cell_b = context.get("cell_b", "")
        registry = context.get("registry")

        if not cell_a or not cell_b:
            return DialecticDistance(cell_a=cell_a, cell_b=cell_b, distance=0.5)

        # Verificar cache
        cache_key = self._distance_cache_key(cell_a, cell_b)
        if cache_key in self._distance_cache:
            return self._distance_cache[cache_key]

        # Calcular distância
        distance = self._engine.calculate_dialectic_distance(cell_a, cell_b, registry)

        # Detalhamento por fator
        a_data = (registry or {}).get(cell_a, {})
        b_data = (registry or {}).get(cell_b, {})

        breakdown = {}
        if a_data and b_data:
            breakdown = self._compute_distance_breakdown(a_data, b_data)

        is_known = (
            cell_b in self._engine.KNOWN_OPPOSITES.get(cell_a, []) or
            cell_a in self._engine.KNOWN_OPPOSITES.get(cell_b, [])
        )

        result = DialecticDistance(
            cell_a=cell_a,
            cell_b=cell_b,
            distance=distance,
            breakdown=breakdown,
            is_known_opposite=is_known,
        )

        if len(self._distance_cache) < self._cache_max_size:
            self._distance_cache[cache_key] = result

        return result

    def _handle_build_tension_map(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Construir mapa de tensões dialéticas."""
        registry = context.get("registry")
        min_tension = context.get("min_tension", self.TENSION_MIN)

        if self._tension_map_cache is not None:
            # Filtrar por threshold
            return {
                uid: entry.to_dict()
                for uid, entry in self._tension_map_cache.items()
                if entry.tension_score >= min_tension
            }

        # Usar engine para construir mapa
        raw_map = self._engine.build_tension_map(registry)

        # Converter para formato estruturado
        tension_map = {}
        for uid, data in raw_map.items():
            cell_data = (registry or {}).get(uid, {})
            entry = TensionMapEntry(
                uid=uid,
                nome=cell_data.get("nome", uid),
                opposites=data.get("opposites", []),
                tension_score=data.get("tension_score", 0.0),
                n_opposites=data.get("n_opposites", 0),
                axis=cell_data.get("axis", ""),
            )
            if entry.tension_score >= min_tension:
                tension_map[uid] = entry

        self._tension_map_cache = tension_map
        return {uid: entry.to_dict() for uid, entry in tension_map.items()}

    def _handle_find_dialectical_pairs(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Encontrar pares dialéticos relevantes para uma query."""
        cell_references = context.get("cell_references", [])
        registry = context.get("registry")
        max_pairs = context.get("max_pairs", 10)

        if not cell_references or not registry:
            return []

        pairs = []
        seen = set()

        for uid in cell_references:
            opp_result = self._handle_infer_opposites({"uid": uid, "registry": registry})
            for opp in opp_result.opposites:
                pair_key = tuple(sorted([uid, opp["uid"]]))
                if pair_key not in seen:
                    seen.add(pair_key)
                    pairs.append({
                        "cell_a": uid,
                        "cell_b": opp["uid"],
                        "distance": opp.get("dialectic_distance", 0.5),
                        "tension": opp_result.tension_score,
                        "is_known": opp.get("is_known_opposite", False),
                    })

        # Ordenar por relevância (maior distância = mais dialético)
        pairs.sort(key=lambda x: (-x["distance"], -x["tension"]))
        return pairs[:max_pairs]

    # ── Utilities ───────────────────────────────────────────────────────

    def _get_cell_data(self, uid: str, registry: Optional[Dict]) -> Dict[str, Any]:
        """Obtém dados de uma célula a partir do registry ou memória."""
        if registry:
            return registry.get(uid, {})
        if self.memory:
            return self.memory.get_cell(uid) or {}
        return {}

    def _detect_layers_used(self, cell_data: dict, opposite_uids: list, registry: Optional[dict]) -> List[str]:
        """Detecta quais camadas de inferência foram usadas."""
        layers = []
        uid = cell_data.get("uid", "")

        # Camada 1: KNOWN_OPPOSITES
        if uid in self._engine.KNOWN_OPPOSITES:
            layers.append("explicit")

        # Camada 2: ANTONYM_PATTERNS
        nome = cell_data.get("nome", "").lower()
        nome_norm = cell_data.get("nome_normalizado", "").lower()
        for ant_key in self._engine.ANTONYM_PATTERNS:
            if ant_key in nome or ant_key in nome_norm:
                layers.append("semantic")
                break

        # Camada 3: HIERARCHICAL_OPPOSITES
        n3_name = cell_data.get("n3_name", "").upper()
        if n3_name in self._engine.HIERARCHICAL_OPPOSITES:
            layers.append("hierarchical")

        # Camada 4: DOMAIN_OPPOSITES
        dominio = cell_data.get("dominio", "")
        if dominio in self._engine.DOMAIN_OPPOSITES:
            layers.append("domain")

        # Camada 5: Posicional
        if len(opposite_uids) > len(layers):
            layers.append("positional")

        return layers if layers else ["positional"]

    def _compute_distance_breakdown(self, a_data: dict, b_data: dict) -> Dict[str, float]:
        """Calcula detalhamento da distância por fator."""
        breakdown = {}

        # Eixo
        a_axis = a_data.get("axis", "")
        b_axis = b_data.get("axis", "")
        breakdown["axis"] = 0.3 if a_axis and b_axis and a_axis != b_axis else 0.0

        # Pilar
        a_pilar = a_data.get("pilar", "")
        b_pilar = b_data.get("pilar", "")
        breakdown["pilar"] = 0.2 if a_pilar and b_pilar and a_pilar != b_pilar else 0.0

        # Domínio
        a_dom = a_data.get("dominio", "")
        b_dom = b_data.get("dominio", "")
        breakdown["dominio"] = 0.15 if a_dom and b_dom and a_dom != b_dom else 0.0

        # Natureza
        a_nat = a_data.get("natureza", "")
        b_nat = b_data.get("natureza", "")
        breakdown["natureza"] = 0.1 if a_nat and b_nat and a_nat != b_nat else 0.0

        # Nome
        a_nome = a_data.get("nome_normalizado", "").lower()
        b_nome = b_data.get("nome_normalizado", "").lower()
        if a_nome and b_nome:
            common = len(set(a_nome.split()) & set(b_nome.split()))
            total = max(len(set(a_nome.split()) | set(b_nome.split())), 1)
            name_sim = common / total
            breakdown["nome"] = round((1 - name_sim) * 0.15, 4)
        else:
            breakdown["nome"] = 0.0

        return breakdown

    def _distance_cache_key(self, cell_a: str, cell_b: str) -> str:
        """Gera chave de cache determinística para distância."""
        return "|".join(sorted([cell_a, cell_b]))

    def _estimate_confidence(self, result) -> float:
        """Estima confiança da inferência dialética."""
        if isinstance(result, OppositionResult):
            if not result.opposites:
                return 0.0
            # Mais opostos e mais camadas = mais confiança
            base = min(0.5, len(result.opposites) * 0.15)
            layer_bonus = 0.1 * len(result.layers_used)
            return round(min(1.0, base + layer_bonus), 4)
        elif isinstance(result, DialecticDistance):
            return round(result.distance, 4)
        elif isinstance(result, dict):
            return 0.5  # Tension map
        return 0.0

    def _build_reasoning(self, result, context: Dict[str, Any]) -> List[str]:
        """Gera explicação da inferência dialética."""
        reasoning = []

        if isinstance(result, OppositionResult):
            reasoning.append(f"Opostos inferidos para {result.nome}: {len(result.opposites)}")
            if result.layers_used:
                reasoning.append(f"Camadas de inferência: {', '.join(result.layers_used)}")
            reasoning.append(f"Score de tensão: {result.tension_score:.3f}")
        elif isinstance(result, DialecticDistance):
            reasoning.append(f"Distância {result.cell_a} ↔ {result.cell_b}: {result.distance:.3f}")
            if result.is_known_opposite:
                reasoning.append("Par oposto conhecido (camada explícita)")
            if result.breakdown:
                top_factor = max(result.breakdown.items(), key=lambda x: x[1])
                reasoning.append(f"Maior contribuição: {top_factor[0]} ({top_factor[1]:.3f})")
        elif isinstance(result, dict) and result:
            n_entries = len(result)
            reasoning.append(f"Mapa de tensões: {n_entries} células com tensão ≥ {self.TENSION_MIN}")
            if n_entries > 0:
                top_tension = max(result.values(), key=lambda x: x.get("tension_score", 0))
                reasoning.append(f"Maior tensão: {top_tension.get('nome', '?')} ({top_tension.get('tension_score', 0):.3f})")

        return reasoning

    # ── Batch Operations ────────────────────────────────────────────────

    def infer_batch(
        self,
        uids: List[str],
        registry: Optional[Dict] = None,
    ) -> List[OppositionResult]:
        """Inferência de opostos em lote."""
        return [
            self._handle_infer_opposites({"uid": uid, "registry": registry})
            for uid in uids
        ]

    def compute_distance_matrix(
        self,
        uids: List[str],
        registry: Optional[Dict] = None,
    ) -> Dict[str, Dict[str, float]]:
        """Computa matriz de distâncias dialéticas entre um conjunto de UIDs."""
        matrix = {}
        for a in uids:
            matrix[a] = {}
            for b in uids:
                if a != b:
                    key = self._distance_cache_key(a, b)
                    if key not in self._distance_cache:
                        self._handle_calculate_distance({
                            "cell_a": a, "cell_b": b, "registry": registry
                        })
                    matrix[a][b] = self._distance_cache[key].distance
        return matrix

    # ── Capability Interface ────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.REQUIRED_TOOLS,
            "description": "Inferência dialética, distância entre conceitos e mapas de tensão",
            "cache_size_opposites": len(self._opposites_cache),
            "cache_size_distances": len(self._distance_cache),
            "features": [
                "infer_opposites",
                "calculate_distance",
                "build_tension_map",
                "find_dialectical_pairs",
                "batch_inference",
                "distance_matrix",
            ],
        }
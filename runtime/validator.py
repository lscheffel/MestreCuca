"""
VALIDADOR ONTOLÓGICO — Verificações de coerência para respostas geradas.

Garante que a saída do pipeline cognitivo respeita as restrições
da ontologia fractal, evitando contradições, rupturas de assinatura
e misturas de polaridades incompatíveis.

Fase 6c do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))


# ── Tipos de verificação ────────────────────────────────────────────

VERIFICATION_TYPES = [
    "eixo_coerente",
    "assinatura_preservada",
    "polaridades_compativeis",
    "conceitos_validos",
    "relacoes_consistentes",
]

# Limites de assinatura semântica por pilar (min/max esperados)
PILLAR_SIGNATURE_RANGES: Dict[str, Dict[str, tuple]] = {
    "LOGOS": {
        "abstracao": (0.30, 0.80),
        "complexidade": (0.40, 0.90),
        "causalidade": (0.30, 0.80),
        "emocionalidade": (0.00, 0.40),
        "materialidade": (0.20, 0.60),
        "simbolismo": (0.00, 0.35),
        "dinamismo": (0.30, 0.70),
        "temporalidade": (0.30, 0.70),
        "ambiguidade": (0.00, 0.35),
    },
    "BIOS": {
        "abstracao": (0.10, 0.50),
        "complexidade": (0.30, 0.70),
        "causalidade": (0.20, 0.60),
        "emocionalidade": (0.20, 0.60),
        "materialidade": (0.50, 0.90),
        "simbolismo": (0.00, 0.30),
        "dinamismo": (0.40, 0.80),
        "temporalidade": (0.40, 0.80),
        "ambiguidade": (0.00, 0.30),
    },
    "PATHOS": {
        "abstracao": (0.10, 0.50),
        "complexidade": (0.30, 0.70),
        "causalidade": (0.10, 0.50),
        "emocionalidade": (0.40, 0.90),
        "materialidade": (0.10, 0.50),
        "simbolismo": (0.20, 0.60),
        "dinamismo": (0.20, 0.60),
        "temporalidade": (0.20, 0.60),
        "ambiguidade": (0.10, 0.50),
    },
    "KHAOS": {
        "abstracao": (0.30, 0.70),
        "complexidade": (0.50, 0.95),
        "causalidade": (0.20, 0.60),
        "emocionalidade": (0.20, 0.70),
        "materialidade": (0.10, 0.50),
        "simbolismo": (0.10, 0.50),
        "dinamismo": (0.60, 0.95),
        "temporalidade": (0.30, 0.70),
        "ambiguidade": (0.30, 0.80),
    },
    "APEIRON": {
        "abstracao": (0.60, 0.95),
        "complexidade": (0.50, 0.90),
        "causalidade": (0.30, 0.70),
        "emocionalidade": (0.00, 0.30),
        "materialidade": (0.05, 0.35),
        "simbolismo": (0.30, 0.70),
        "dinamismo": (0.30, 0.60),
        "temporalidade": (0.40, 0.80),
        "ambiguidade": (0.20, 0.60),
    },
    "MYTHOS": {
        "abstracao": (0.30, 0.70),
        "complexidade": (0.30, 0.70),
        "causalidade": (0.10, 0.50),
        "emocionalidade": (0.30, 0.80),
        "materialidade": (0.05, 0.40),
        "simbolismo": (0.50, 0.95),
        "dinamismo": (0.20, 0.60),
        "temporalidade": (0.30, 0.70),
        "ambiguidade": (0.20, 0.60),
    },
}

# Mapeamento de eixo → pilares válidos
AXIS_PILARS: Dict[str, List[str]] = {
    "SINTRÓPICO": ["LOGOS", "BIOS", "PATHOS"],
    "ENTRÓPICO": ["KHAOS", "APEIRON", "MYTHOS"],
}

# Pilares com polaridade oposta (para detecção de mistura)
OPPOSITE_POLES: Dict[str, str] = {
    "LOGOS": "KHAOS",
    "BIOS": "ENTROPIA",  # domínio, não pilar — tratado separadamente
    "PATHOS": "LOGOS",   # tensão natural
    "KHAOS": "LOGOS",
    "APEIRON": "PATHOS",
    "MYTHOS": "ALGORITMIA",  # domínio — tensão narrativa vs. lógica
}


@dataclass
class VerificationResult:
    """Resultado de uma verificação de coerência ontológica."""
    tipo: str
    passou: bool
    score: float = 1.0
    detalhes: str = ""
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "tipo": self.tipo,
            "passou": self.passou,
            "score": round(self.score, 4),
            "detalhes": self.detalhes,
            "warnings": self.warnings,
        }


@dataclass
class ValidationReport:
    """Relatório completo de validação ontológica."""
    valido: bool
    verificacoes: List[VerificationResult]
    score_geral: float
    recomendacoes: List[str]

    def to_dict(self) -> dict:
        return {
            "valido": self.valido,
            "score_geral": round(self.score_geral, 4),
            "verificacoes": [v.to_dict() for v in self.verificacoes],
            "recomendacoes": self.recomendacoes,
        }

    def __str__(self) -> str:
        lines = [
            f"{'='*50}",
            f"VALIDAÇÃO ONTOLÓGICA — {'APROVADO' if self.valido else 'REJEITADO'}",
            f"Score geral: {self.score_geral:.2%}",
            f"{'='*50}",
        ]
        for v in self.verificacoes:
            status = "✓" if v.passou else "✗"
            lines.append(f"  {status} {v.tipo}: {v.score:.2%} — {v.detalhes}")
            for w in v.warnings:
                lines.append(f"    ⚠ {w}")
        if self.recomendacoes:
            lines.append(f"\nRecomendações:")
            for r in self.recomendacoes:
                lines.append(f"  → {r}")
        return "\n".join(lines)


class OntologyValidator:
    """
    Validador Ontológico — Verifica coerência de respostas
    geradas pelo pipeline cognitivo com a ontologia fractal.

    Verificações:
    1. Eixo coerente — pilar pertence ao eixo correto
    2. Assinatura preservada — dimensões semânticas dentro dos limites
    3. Polaridades compatíveis — sem mistura de opostos
    4. Conceitos válidos — referências N4 existentes
    5. Relações consistentes — sem contradições no grafo
    """

    def __init__(
        self,
        registry: Optional[Dict[str, dict]] = None,
        json_dir: str = "data/json",
        index_path: str = "data/json/ontology_index.json",
    ):
        self.registry = registry or {}
        # Resolver caminhos relativos ao diretório raiz do projeto
        if not Path(json_dir).is_absolute():
            json_dir = str(_PROJECT_ROOT / json_dir)
        if not Path(index_path).is_absolute():
            index_path = str(_PROJECT_ROOT / index_path)
        if not self.registry:
            self._load_registry(json_dir, index_path)
        self.threshold = 0.6  # score mínimo para aprovação

    def _load_registry(
        self, json_dir: str, index_path: str
    ) -> None:
        """Carrega o registro de células N4."""
        try:
            idx_path = Path(index_path)
            if idx_path.exists():
                with open(idx_path, "r", encoding="utf-8") as f:
                    index = json.load(f)
                if isinstance(index, list):
                    # Índice é lista de UIDs
                    for uid in index:
                        self._load_cell(uid, json_dir)
                elif isinstance(index, dict):
                    # Índice é dict (ex: {"schema_version": ..., "total_celulas": 162, ...})
                    # Tentar extrair UIDs do campo "celulas" ou similar
                    celulas = index.get("celulas") or index.get("uids") or index.get("cells")
                    if isinstance(celulas, list):
                        for uid in celulas:
                            self._load_cell(uid, json_dir)
                    else:
                        # Fallback: glob direto nos JSONs
                        logger.info(
                            "Índice é dict sem lista de UIDs (%d chaves), "
                            "usando glob fallback",
                            len(index),
                        )
                        for f in sorted(Path(json_dir).glob("N4_*.json")):
                            self._load_cell(f.stem, json_dir)
            else:
                # Fallback: carregar todos os JSONs do diretório
                for f in sorted(Path(json_dir).glob("N4_*.json")):
                    self._load_cell(f.stem, json_dir)
            logger.info(
                "Validator registry: %d células carregadas", len(self.registry)
            )
        except Exception as e:
            logger.warning("Erro ao carregar registry para validação: %s", e)

    def _load_cell(self, uid: str, json_dir: str) -> None:
        """Carrega uma célula N4 no registry."""
        path = Path(json_dir) / f"{uid}.json"
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self.registry[uid] = json.load(f)
            except Exception as e:
                logger.debug("Erro ao carregar %s: %s", uid, e)

    def validate(
        self,
        routing: dict,
        response_context: dict,
        retrieved_cells: Optional[List[dict]] = None,
    ) -> ValidationReport:
        """
        Executa todas as verificações de validação.

        Args:
            routing: Decisão de roteamento (do CognitiveRouter)
            response_context: Contexto da resposta gerada
            retrieved_cells: Células recuperadas (opcional)

        Returns:
            ValidationReport com resultados de todas as verificações
        """
        verificacoes = []

        # 1. Eixo coerente
        v1 = self._verify_axis_coherence(routing)
        verificacoes.append(v1)

        # 2. Assinatura preservada
        v2 = self._verify_signature(routing, response_context)
        verificacoes.append(v2)

        # 3. Polaridades compatíveis
        v3 = self._verify_polarity(routing, response_context)
        verificacoes.append(v3)

        # 4. Conceitos válidos
        v4 = self._verify_concepts(response_context, retrieved_cells)
        verificacoes.append(v4)

        # 5. Relações consistentes
        v5 = self._verify_relations(retrieved_cells)
        verificacoes.append(v5)

        # Calcular score geral
        scores = [v.score for v in verificacoes]
        score_geral = np.mean(scores) if scores else 0.0

        # Gerar recomendações
        recomendacoes = self._generate_recommendations(verificacoes)

        return ValidationReport(
            valido=score_geral >= self.threshold,
            verificacoes=verificacoes,
            score_geral=score_geral,
            recomendacoes=recomendacoes,
        )

    def _verify_axis_coherence(self, routing: dict) -> VerificationResult:
        """
        Verifica se o pilar é coerente com o eixo classificado.

        LOGOS, BIOS, PATHOS → SINTRÓPICO
        KHAOS, APEIRON, MYTHOS → ENTRÓPICO
        """
        pilar = routing.get("pilar", "")
        eixo = routing.get("eixo", "")

        if not pilar or not eixo:
            return VerificationResult(
                tipo="eixo_coerente",
                passou=True,  # Não pode validar sem dados
                score=0.8,
                detalhes="Eixo ou pilar não especificado, assumido coerente.",
                warnings=["Classificação N0/N1 incompleta."],
            )

        eixo_upper = eixo.upper().replace("Í", "I")
        pilares_validos = AXIS_PILARS.get(eixo_upper, [])

        if pilar in pilares_validos:
            return VerificationResult(
                tipo="eixo_coerente",
                passou=True,
                score=1.0,
                detalhes=f"Pilar {pilar} coerente com eixo {eixo_upper}.",
            )
        else:
            return VerificationResult(
                tipo="eixo_coerente",
                passou=False,
                score=0.2,
                detalhes=(
                    f"Pilar {pilar} NÃO pertence ao eixo {eixo_upper}. "
                    f"Pilares válidos: {pilares_validos}"
                ),
                warnings=[
                    f"Possível erro de classificação: {pilar} → {eixo_upper}",
                    "Recomenda reclassificação ou revisão manual.",
                ],
            )

    def _verify_signature(
        self, routing: dict, context: dict
    ) -> VerificationResult:
        """
        Verifica se a assinatura semântica das células ativadas
        está dentro dos limites esperados para o pilar.
        """
        pilar = routing.get("pilar", "LOGOS")
        ranges = PILLAR_SIGNATURE_RANGES.get(pilar, {})

        if not ranges:
            return VerificationResult(
                tipo="assinatura_preservada",
                passou=True,
                score=0.9,
                detalhes="Sem limites de assinatura definidos para este pilar.",
            )

        # Obtém assinaturas das células ativadas
        cell_uids = context.get("cell_references", [])
        if not cell_uids:
            return VerificationResult(
                tipo="assinatura_preservada",
                passou=True,
                score=0.8,
                detalhes="Nenhuma célula ativada para verificação.",
            )

        violations = []
        total_checks = 0
        passed_checks = 0

        for uid in cell_uids:
            cell_data = self.registry.get(uid, {})
            assinatura = cell_data.get("assinatura_semantica", {})

            for dim, (min_val, max_val) in ranges.items():
                total_checks += 1
                val = assinatura.get(dim)
                if val is not None:
                    if val < min_val or val > max_val:
                        violations.append(
                            f"{uid}.{dim}={val:.3f} fora de [{min_val:.2f}, {max_val:.2f}]"
                        )
                    else:
                        passed_checks += 1
                else:
                    passed_checks += 1  # Dimensão ausente = OK

        score = passed_checks / max(total_checks, 1)

        if violations:
            return VerificationResult(
                tipo="assinatura_preservada",
                passou=score >= 0.7,
                score=score,
                detalhes=f"{passed_checks}/{total_checks} dimensões dentro dos limites.",
                warnings=[f"Assinatura fora do esperado: {v}" for v in violations[:5]],
            )
        else:
            return VerificationResult(
                tipo="assinatura_preservada",
                passou=True,
                score=1.0,
                detalhes="Todas as dimensões dentro dos limites do pilar.",
            )

    def _verify_polarity(
        self, routing: dict, context: dict
    ) -> VerificationResult:
        """
        Verifica se não há mistura de polaridades incompatíveis
        entre os conceitos ativados.
        """
        pilar = routing.get("pilar", "")
        cell_uids = context.get("cell_references", [])

        if not cell_uids or not pilar:
            return VerificationResult(
                tipo="polaridades_compativeis",
                passou=True,
                score=0.9,
                detalhes="Dados insuficientes para verificação de polaridade.",
            )

        # Coleta opostos de todas as células ativadas
        all_opposites = set()
        cell_pilares = set()

        for uid in cell_uids:
            cell_data = self.registry.get(uid, {})
            # Verifica pilar da célula
            cell_pilar = cell_data.get("pilar", "")
            if cell_pilar:
                cell_pilares.add(cell_pilar)

            # Coleta opostos
            for opp_uid in cell_data.get("opostos", []):
                all_opposites.add(opp_uid)
                opp_data = self.registry.get(opp_uid, {})
                if opp_data.get("pilar"):
                    cell_pilares.add(opp_data["pilar"])

        # Verifica se opostos estão entre as células ativadas
        activated_set = set(cell_uids)
        conflicting = activated_set.intersection(all_opposites)

        if conflicting:
            conflict_details = ", ".join(list(conflicting)[:3])
            return VerificationResult(
                tipo="polaridades_compativeis",
                passou=False,
                score=0.3,
                detalhes=f"Células opostas coativadas: {conflict_details}",
                warnings=[
                    "Mistura de opostos detectada pode gerar incoerência.",
                    "Considere separar em camadas de processamento.",
                ],
            )

        # Verifica se há pilares conflitantes
        incompatible_pairs = [
            ("LOGOS", "KHAOS"),
            ("PATHOS", "APEIRON"),
        ]
        for p1, p2 in incompatible_pairs:
            if p1 in cell_pilares and p2 in cell_pilares:
                return VerificationResult(
                    tipo="polaridades_compativeis",
                    passou=False,
                    score=0.4,
                    detalhes=f"Pilares incompatíveis coativados: {p1} + {p2}",
                    warnings=[
                        f"Tensão entre {p1} e {p2} detectada.",
                        "Avaliar se a tensão é intencional (dialética).",
                    ],
                )

        return VerificationResult(
            tipo="polaridades_compativeis",
            passou=True,
            score=1.0,
            detalhes="Polaridades compatíveis.",
        )

    def _verify_concepts(
        self,
        context: dict,
        retrieved_cells: Optional[List[dict]] = None,
    ) -> VerificationResult:
        """
        Verifica se todos os conceitos referenciados existem
        na ontologia e possuem estrutura válida.
        """
        cell_uids = context.get("cell_references", [])
        invalid = []
        valid_count = 0

        for uid in cell_uids:
            if uid not in self.registry:
                invalid.append(uid)
            else:
                cell = self.registry[uid]
                # Verifica campos obrigatórios
                required = ["uid", "nome", "nivel", "pilar", "dominio"]
                missing = [f for f in required if f not in cell]
                if missing:
                    invalid.append(f"{uid} (campos ausentes: {missing})")
                else:
                    valid_count += 1

        total = len(cell_uids)
        if total == 0:
            return VerificationResult(
                tipo="conceitos_validos",
                passou=True,
                score=0.8,
                detalhes="Nenhum conceito para validar.",
            )

        score = valid_count / total
        if invalid:
            return VerificationResult(
                tipo="conceitos_validos",
                passou=score >= 0.9,
                score=score,
                detalhes=f"{valid_count}/{total} conceitos válidos.",
                warnings=[f"Conceito inválido ou ausente: {i}" for i in invalid[:5]],
            )
        else:
            return VerificationResult(
                tipo="conceitos_validos",
                passou=True,
                score=1.0,
                detalhes=f"Todos os {total} conceitos são válidos.",
            )

    def _verify_relations(
        self, retrieved_cells: Optional[List[dict]] = None
    ) -> VerificationResult:
        """
        Verifica consistência das relações entre células ativadas.
        Detecta relações quebradas, referências circulares e pesos inválidos.
        """
        if not retrieved_cells:
            return VerificationResult(
                tipo="relacoes_consistentes",
                passou=True,
                score=0.9,
                detalhes="Nenhuma célula para verificar relações.",
            )

        issues = []
        total_rels = 0
        valid_rels = 0

        for cell_info in retrieved_cells:
            uid = cell_info if isinstance(cell_info, str) else cell_info.get("uid", "")
            cell = self.registry.get(uid, {})
            rels = cell.get("relacoes", [])

            for rel in rels:
                if isinstance(rel, str):
                    # Relação legada (string pura)
                    issues.append(f"{uid}: relação legada (string): {rel}")
                    total_rels += 1
                    continue

                total_rels += 1
                target = rel.get("alvo", "")
                peso = rel.get("peso", 0)
                tipo = rel.get("tipo", "")

                # Verifica peso
                if not (-1.0 <= peso <= 1.0):
                    issues.append(f"{uid}→{target}: peso {peso} fora de [-1, 1]")
                else:
                    valid_rels += 1

                # Verifica tipo
                valid_types = [
                    "depende_de", "complementa", "contrasta", "expande",
                    "implementa", "generaliza", "especializa", "causa",
                    "equilibra", "transforma",
                ]
                if tipo not in valid_types:
                    issues.append(f"{uid}→{target}: tipo desconhecido '{tipo}'")

                # Verifica se o alvo existe no registry
                if target and target not in self.registry:
                    issues.append(f"{uid}→{target}: alvo não encontrado no registry")

        score = valid_rels / max(total_rels, 1)

        if issues:
            return VerificationResult(
                tipo="relacoes_consistentes",
                passou=score >= 0.8,
                score=score,
                detalhes=f"{valid_rels}/{total_rels} relações válidas.",
                warnings=[f"Relação: {i}" for i in issues[:5]],
            )
        else:
            return VerificationResult(
                tipo="relacoes_consistentes",
                passou=True,
                score=1.0,
                detalhes=f"Todas as {total_rels} relações são consistentes.",
            )

    def _generate_recommendations(
        self, verificacoes: List[VerificationResult]
    ) -> List[str]:
        """Gera recomendações baseadas nas verificações que falharam."""
        recs = []
        for v in verificacoes:
            if not v.passou:
                if v.tipo == "eixo_coerente":
                    recs.append(
                        "Revisar classificação N0/N1: pilar incompatível com eixo."
                    )
                elif v.tipo == "assinatura_preservada":
                    recs.append(
                        "Ajustar seleção de células para manter coerência semântica "
                        "com o pilar dominante."
                    )
                elif v.tipo == "polaridades_compativeis":
                    recs.append(
                        "Separar opostos em camadas dialéticas ou justificar tensão "
                        "como recurso retórico."
                    )
                elif v.tipo == "conceitos_validos":
                    recs.append(
                        "Verificar UIDs referenciados contra o índice da ontologia."
                    )
                elif v.tipo == "relacoes_consistentes":
                    recs.append(
                        "Revisar relações tipadas e garantir pesos em [-1, 1]."
                    )
        return recs


# ── Função utilitária ───────────────────────────────────────────────


def validate_response(
    routing: dict,
    response_context: dict,
    json_dir: str = "data/json",
) -> ValidationReport:
    """
    Validação rápida de uma resposta do pipeline.

    Args:
        routing: Decisão de roteamento
        response_context: Contexto da resposta (inclui cell_references)
        json_dir: Diretório dos JSONs N4

    Returns:
        ValidationReport
    """
    validator = OntologyValidator(json_dir=json_dir)
    return validator.validate(routing, response_context)


# ── Ponto de entrada para testes ────────────────────────────────────

if __name__ == "__main__":
    validator = OntologyValidator()

    # Teste 1: Configuração coerente
    routing_ok = {
        "pilar": "LOGOS",
        "eixo": "SINTRÓPICO",
        "estrategia": "Lógica-Estrutural",
        "dominio": "ALGORITMIA",
    }
    context_ok = {
        "cell_references": [
            "N4_ALGORITMIA_1_A",
            "N4_ALGORITMIA_1_B",
            "N4_ALGORITMIA_2_A",
        ]
    }

    report1 = validator.validate(routing_ok, context_ok)
    print("=== TESTE 1: Configuração coerente ===")
    print(report1)

    # Teste 2: Pilar incompatível com eixo
    routing_bad = {
        "pilar": "KHAOS",
        "eixo": "SINTRÓPICO",
        "estrategia": "Transformacional-Criativo",
    }
    report2 = validator.validate(routing_bad, context_ok)
    print("\n=== TESTE 2: Pilar incompatível com eixo ===")
    print(report2)

    # Teste 3: Conceito inválido
    context_bad = {"cell_references": ["N4_ALGORITMIA_1_A", "N4_INEXISTENTE_X"]}
    report3 = validator.validate(routing_ok, context_bad)
    print("\n=== TESTE 3: Conceito inválido ===")
    print(report3)
"""
ENGINE DE SÍNTESE — Montagem dinâmica de prompts e respostas.

Transforma contexto ontológico (classificação + retrieval + grafo)
em prompts enriquecidos e respostas compostas, respeitando a estratégia
do pilar selecionado e a assinatura semântica das células.

Fase 6b do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np

logger = logging.getLogger(__name__)

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))


# ── Templates de síntese por pilar ──────────────────────────────────

SYNTHESIS_TEMPLATES: Dict[str, str] = {
    "LOGOS": (
        "Você é um analista lógico-estrutural operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: LOGOS (Lógica-Estrutural)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Relações Identificadas\n"
        "{relacoes}\n\n"
        "## Restrições Lógicas\n"
        "- Manter coerência dedutiva entre premissas e conclusão.\n"
        "- Cada passo deve ser verificável.\n"
        "- Respeitar a hierarquia ontológica (N0→N4).\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Decomponha a questão em premissas explícitas.\n"
        "2. Aplique os conceitos ativados de forma sequencial.\n"
        "3. Indique relações causais e dependências.\n"
        "4. Apresente uma conclusão verificável.\n"
        "{restricoes_adicionais}"
    ),
    "BIOS": (
        "Você é um analista orgânico-vital operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: BIOS (Orgânico-Vital)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Ciclos e Interdependências\n"
        "{ciclos}\n\n"
        "## Restrições Orgânicas\n"
        "- Considerar ciclos de retroalimentação.\n"
        "- Respeitar limites de capacidade (homeostase).\n"
        "- Preservar integridade do sistema.\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Identifique os ciclos de vida envolvidos.\n"
        "2. Mapeie interdependências ecossistêmicas.\n"
        "3. Proponha soluções sustentáveis e adaptativas.\n"
        "4. Respeite os limites orgânicos do sistema.\n"
        "{restricoes_adicionais}"
    ),
    "PATHOS": (
        "Você é um analista relacional-significativo operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: PATHOS (Relacional-Significativo)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Conexões Humanas\n"
        "{conexoes}\n\n"
        "## Restrições Relacionais\n"
        "- Priorizar empatia e reconhecimento.\n"
        "- Considerar impacto emocional e social.\n"
        "- Respeitar dignidade e valores.\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Reconheça a dimensão humana da questão.\n"
        "2. Estabeleça conexões significativas entre os elementos.\n"
        "3. Proponha ações com impacto positivo verificável.\n"
        "4. Considere múltiplas perspectivas e vozes.\n"
        "{restricoes_adicionais}"
    ),
    "KHAOS": (
        "Você é um analista transformacional-criativo operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: KHAOS (Transformacional-Criativo)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Tensões e Rupturas\n"
        "{tensões}\n\n"
        "## Restrições Transformacionais\n"
        "- Explorar além das fronteiras convencionais.\n"
        "- Considerar rupturas como oportunidades.\n"
        "- Equilibrar destruição e reconstrução.\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Identifique pontos de ruptura e disrupção.\n"
        "2. Explore possibilidades emergentes.\n"
        "3. Proponha caminhos criativos e adaptativos.\n"
        "4. Considere a evolução e a transformação contínua.\n"
        "{restricoes_adicionais}"
    ),
    "APEIRON": (
        "Você é um analista estratégico-transcendente operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: APEIRON (Estratégico-Transcendente)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Padrões Sistêmicos\n"
        "{padroes}\n\n"
        "## Restrições Estratégicas\n"
        "- Considerar múltiplas escalas e perspectivas.\n"
        "- Buscar padrões universais e transcendentes.\n"
        "- Integrar visão de curto e longo prazo.\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Escale a análise para múltiplas dimensões.\n"
        "2. Identifique padrões abstratos e universais.\n"
        "3. Proponha uma visão estratégica integradora.\n"
        "4. Transcenda limitações imediatas.\n"
        "{restricoes_adicionais}"
    ),
    "MYTHOS": (
        "Você é um analista narrativo-simbólico operando sobre a Ontologia Fractal.\n"
        "Sua tarefa: {tarefa}\n\n"
        "## Contexto Ontológico\n"
        "Pilar: MYTHOS (Narrativo-Simbólico)\n"
        "Domínio: {dominio}\n"
        "Subárvore: {subarvore}\n"
        "Célula focal: {celula}\n\n"
        "## Conceitos Ativados\n"
        "{conceitos_ativados}\n\n"
        "## Arquétipos e Símbolos\n"
        "{simbolos}\n\n"
        "## Restrições Narrativas\n"
        "- Respeitar a profundidade simbólica.\n"
        "- Conectar com padrões arquetípicos.\n"
        "- Honrar a tradição e a sabedoria.\n\n"
        "## Instrução\n"
        "Produza uma resposta que:\n"
        "1. Enquadre a questão em uma narrativa significativa.\n"
        "2. Identifique símbolos e arquétipos relevantes.\n"
        "3. Proponha uma jornada ou transformação simbólica.\n"
        "4. Extraia significado profundo e aplicável.\n"
        "{restricoes_adicionais}"
    ),
}


@dataclass
class SynthesisInput:
    """Inputs para a engine de síntese."""
    query: str
    routing_decision: dict
    retrieved_cells: List[dict] = field(default_factory=list)
    graph_context: Optional[dict] = None
    classification: Optional[dict] = None


@dataclass
class SynthesisOutput:
    """Saída da engine de síntese."""
    prompt: str
    context_summary: str
    cell_references: List[str]
    metadata: dict


class OntologySynthesizer:
    """
    Engine de Síntese — Monta prompts e respostas dinâmicas
    combinando contexto ontológico multi-fonte.

    Integra:
    - Classificação N0→N4
    - Retrieval híbrido (células similares)
    - Navegação de grafo (vizinhança)
    - Assinaturas semânticas
    - Relações tipadas
    - Opostos dialéticos
    """

    def __init__(
        self,
        json_dir: str = "data/json",
        index_path: str = "data/json/ontology_index.json",
    ):
        # Resolver caminhos relativos ao diretório raiz do projeto
        if not Path(json_dir).is_absolute():
            json_dir = str(_PROJECT_ROOT / json_dir)
        if not Path(index_path).is_absolute():
            index_path = str(_PROJECT_ROOT / index_path)
        self.json_dir = Path(json_dir)
        self.index_path = Path(index_path)
        self.registry: Dict[str, dict] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Carrega o índice global da ontologia."""
        try:
            with open(self.index_path, "r", encoding="utf-8") as f:
                index = json.load(f)
            # Index pode ser lista de UIDs ou dicionário
            if isinstance(index, list):
                # Carrega cada JSON individualmente
                for uid in index:
                    self._load_cell(uid)
            elif isinstance(index, dict):
                for uid, meta in index.items():
                    if isinstance(meta, dict) and "uid" in meta:
                        self.registry[uid] = meta
                # Carrega JSONs completos
                for f in sorted(self.json_dir.glob("N4_*.json")):
                    uid = f.stem
                    if uid not in self.registry:
                        self._load_cell(uid)
            logger.info(
                "Registry carregado: %d células", len(self.registry)
            )
        except FileNotFoundError:
            logger.warning("Index não encontrado em %s", self.index_path)
        except Exception as e:
            logger.error("Erro ao carregar registry: %s", e)

    def _load_cell(self, uid: str) -> Optional[dict]:
        """Carrega uma célula N4 do JSON."""
        path = self.json_dir / f"{uid}.json"
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.registry[uid] = data
            return data
        except Exception as e:
            logger.warning("Erro ao carregar %s: %s", uid, e)
            return None

    def synthesize(
        self, synthesis_input: SynthesisInput
    ) -> SynthesisOutput:
        """
        Executa a síntese completa.

        1. Determina template base pelo pilar
        2. Monta contexto ontológico enriquecido
        3. Combina retrieved cells com grafo
        4. Gera prompt final
        """
        routing = synthesis_input.routing_decision
        pilar = routing.get("pilar", "LOGOS")

        # Obtém template
        template = SYNTHESIS_TEMPLATES.get(
            pilar, SYNTHESIS_TEMPLATES["LOGOS"]
        )

        # Monta referências de células
        cell_refs = self._build_cell_references(synthesis_input)

        # Monta conceitos ativados
        conceitos = self._build_concepts(cell_refs)

        # Monta relações
        relacoes = self._build_relations(cell_refs)

        # Monta componentes específicos por pilar
        extras = self._build_pilar_extras(pilar, cell_refs)

        # Monta restrições adicionais
        restricoes = self._build_restrictions(synthesis_input)

        # Preenche template
        prompt = template.format(
            tarefa=synthesis_input.query,
            dominio=routing.get("dominio", "N/A"),
            subarvore=routing.get("subarvore", "N/A"),
            celula=routing.get("conceito_foco", "N/A"),
            conceitos_ativados=conceitos,
            relacoes=relacoes,
            restricoes_adicionais=restricoes,
            **extras,
        )

        # Monta sumário de contexto
        context_summary = self._build_context_summary(
            synthesis_input, cell_refs
        )

        return SynthesisOutput(
            prompt=prompt,
            context_summary=context_summary,
            cell_references=[r["uid"] for r in cell_refs],
            metadata={
                "pilar": pilar,
                "num_cells": len(cell_refs),
                "template_usado": pilar,
                "dominio": routing.get("dominio"),
                "subarvore": routing.get("subarvore"),
            },
        )

    def _build_cell_references(
        self, synthesis_input: SynthesisInput
    ) -> List[dict]:
        """
        Constrói lista de células de referência a partir de
        retrieved cells e grafo.
        """
        refs = []
        seen_uids = set()

        # Prioridade 1: células do retrieval
        for cell in synthesis_input.retrieved_cells:
            uid = cell if isinstance(cell, str) else cell.get("uid", "")
            if uid and uid not in seen_uids:
                data = self.registry.get(uid, {})
                if data:
                    refs.append({
                        "uid": uid,
                        "data": data,
                        "source": "retrieval",
                        "score": cell.get("score", 0.0)
                        if isinstance(cell, dict)
                        else 0.0,
                    })
                    seen_uids.add(uid)

        # Prioridade 2: vizinhos do grafo
        graph = synthesis_input.graph_context
        if graph and "neighbors" in graph:
            for neighbor in graph["neighbors"]:
                n_uid = neighbor if isinstance(neighbor, str) else neighbor.get(
                    "uid", ""
                )
                if n_uid and n_uid not in seen_uids:
                    data = self.registry.get(n_uid, {})
                    if data:
                        refs.append({
                            "uid": n_uid,
                            "data": data,
                            "source": "graph",
                            "score": neighbor.get("score", 0.0)
                            if isinstance(neighbor, dict)
                            else 0.0,
                        })
                        seen_uids.add(n_uid)

        # Limitar a 15 referências para manter o prompt gerenciável
        return refs[:15]

    def _build_concepts(self, cell_refs: List[dict]) -> str:
        """Monta bloco de conceitos ativados."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            uid = ref.get("uid", "")
            nome = data.get("nome", uid)
            desc = data.get("descricao", data.get("descricao_resumida", ""))
            funcoes = data.get("funcao_cognitiva", [])
            natureza = data.get("natureza", "")

            line = f"- **{nome}** ({uid}): {desc[:120]}"
            if funcoes:
                line += f" [funções: {', '.join(funcoes[:3])}]"
            if natureza:
                line += f" [natureza: {natureza}]"
            lines.append(line)

        return "\n".join(lines) if lines else "- Nenhum conceito ativado."

    def _build_relations(self, cell_refs: List[dict]) -> str:
        """Monta bloco de relações entre células ativadas."""
        lines = []
        uids = {ref["uid"] for ref in cell_refs}

        for ref in cell_refs:
            data = ref.get("data", {})
            uid = ref.get("uid", "")
            rels = data.get("relacoes", [])

            for rel in rels[:5]:  # Limitar por célula
                if isinstance(rel, dict):
                    tipo = rel.get("tipo", "")
                    alvo = rel.get("alvo", "")
                    peso = rel.get("peso", 0)

                    if alvo in uids:
                        emoji = self._relation_emoji(tipo)
                        lines.append(
                            f"  {emoji} {uid} → {alvo} "
                            f"[{tipo}, peso={peso:.2f}]"
                        )

        if not lines:
            return "- Sem relações diretas entre conceitos ativados."

        return "\n".join(sorted(set(lines)))

    def _relation_emoji(self, tipo: str) -> str:
        """Retorna emoji representativo para tipo de relação."""
        emoji_map = {
            "depende_de": "🔗",
            "complementa": "🟢",
            "contrasta": "🔴",
            "expande": "📈",
            "implementa": "⚙️",
            "generaliza": "⬆️",
            "especializa": "⬇️",
            "causa": "⚡",
            "equilibra": "⚖️",
            "transforma": "🔄",
        }
        return emoji_map.get(tipo, "➡️")

    def _build_pilar_extras(
        self, pilar: str, cell_refs: List[dict]
    ) -> Dict[str, str]:
        """Monta campos extras específicos por pilar."""
        extras = {}

        if pilar == "BIOS":
            extras["ciclos"] = self._build_cycles(cell_refs)
        elif pilar == "PATHOS":
            extras["conexoes"] = self._build_connections(cell_refs)
        elif pilar == "KHAOS":
            extras["tensões"] = self._build_tensions(cell_refs)
        elif pilar == "APEIRON":
            extras["padroes"] = self._build_patterns(cell_refs)
        elif pilar == "MYTHOS":
            extras["simbolos"] = self._build_symbols(cell_refs)
        else:
            # LOGOS e outros: campos vazios são ignorados no template
            extras["ciclos"] = ""
            extras["conexoes"] = ""
            extras["tensões"] = ""
            extras["padroes"] = ""
            extras["simbolos"] = ""

        return extras

    def _build_cycles(self, cell_refs: List[dict]) -> str:
        """Identifica ciclos e retroalimentações."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            nome = data.get("nome", "")
            natureza = data.get("natureza", "")
            if natureza in ("processo", "dinamica", "mecanismo"):
                lines.append(
                    f"- {nome}: processo dinâmico com potencial de "
                    f"ciclagem e retroalimentação"
                )
        return "\n".join(lines) if lines else "- Ciclos naturais do sistema identificados."

    def _build_connections(self, cell_refs: List[dict]) -> str:
        """Identifica conexões relacionais."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            nome = data.get("nome", "")
            tags = data.get("tags", [])
            if any(t in ["relacao", "conexao", "dialogo"] for t in tags):
                lines.append(f"- {nome}: ponto de conexão relacional")
        return "\n".join(lines) if lines else "- Pontos de conexão identificados."

    def _build_tensions(self, cell_refs: List[dict]) -> str:
        """Identifica tensões e rupturas."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            nome = data.get("nome", "")
            opostos = data.get("opostos", [])
            if opostos:
                lines.append(
                    f"- {nome} ↔ {opostos[0]}: tensão dialética "
                    f"({len(opostos)} opostos mapeados)"
                )
        return "\n".join(lines) if lines else "- Tensões transformadoras identificadas."

    def _build_patterns(self, cell_refs: List[dict]) -> str:
        """Identifica padrões sistêmicos e escalares."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            nome = data.get("nome", "")
            assinatura = data.get("assinatura_semantica", {})
            abstracao = assinatura.get("abstracao", 0)
            if abstracao > 0.6:
                lines.append(
                    f"- {nome}: alto grau de abstração ({abstracao:.2f}), "
                    f"padrão sistêmico potencial"
                )
        return "\n".join(lines) if lines else "- Padrões sistêmicos identificados."

    def _build_symbols(self, cell_refs: List[dict]) -> str:
        """Identifica símbolos e arquétipos."""
        lines = []
        for ref in cell_refs:
            data = ref.get("data", {})
            nome = data.get("nome", "")
            tags = data.get("tags", [])
            if any(t in ["arquetipo", "simbolo", "mito"] for t in tags):
                lines.append(f"- {nome}: símbolo/arquétipo ativo")
        return "\n".join(lines) if lines else "- Padrões simbólicos identificados."

    def _build_restrictions(
        self, synthesis_input: SynthesisInput
    ) -> str:
        """Monta restrições adicionais baseadas na classificação."""
        restrictions = []
        classification = synthesis_input.classification or {}
        n0 = classification.get("classificacao", {}).get("n0_eixo", {})
        eixo = n0.get("eixo", "")

        if eixo == "SINTRÓPICO":
            restrictions.append(
                "- Foco em resolução concreta e aplicável."
            )
        elif eixo == "ENTRÓPICO":
            restrictions.append(
                "- Explorar múltiplas possibilidades e perspectivas."
            )

        return "\n".join(restrictions)

    def _build_context_summary(
        self, synthesis_input: SynthesisInput, cell_refs: List[dict]
    ) -> str:
        """Gera sumário de contexto para logging/auditoria."""
        routing = synthesis_input.routing_decision
        lines = [
            f"Pilar: {routing.get('pilar', 'N/A')}",
            f"Estrategia: {routing.get('estrategia', 'N/A')}",
            f"Domínio: {routing.get('dominio', 'N/A')}",
            f"Subárvore: {routing.get('subarvore', 'N/A')}",
            f"Score de roteamento: {routing.get('score', 0):.4f}",
            f"Células ativadas: {len(cell_refs)}",
            f"Uids: {[r['uid'] for r in cell_refs]}",
        ]
        return "\n".join(lines)


# ── Função utilitária para síntese rápida ───────────────────────────


def build_synthesis_prompt(
    query: str,
    routing: dict,
    retrieved_cells: List[dict],
    graph_context: Optional[dict] = None,
    classification: Optional[dict] = None,
    json_dir: str = "data/json",
) -> SynthesisOutput:
    """
    Função de conveniência para síntese rápida.

    Args:
        query: Pergunta original do usuário
        routing: Decisão de roteamento do CognitiveRouter
        retrieved_cells: Células recuperadas pelo HybridRetriever
        graph_context: Contexto adicional do grafo (opcional)
        classification: Classificação N0→N4 completa
        json_dir: Diretório dos JSONs N4

    Returns:
        SynthesisOutput com prompt montado
    """
    synthesizer = OntologySynthesizer(json_dir=json_dir)
    synthesis_input = SynthesisInput(
        query=query,
        routing_decision=routing,
        retrieved_cells=retrieved_cells,
        graph_context=graph_context,
        classification=classification,
    )
    return synthesizer.synthesize(synthesis_input)


# ── Ponto de entrada para testes ────────────────────────────────────

if __name__ == "__main__":
    synthesizer = OntologySynthesizer()

    # Teste com dados simulados
    test_routing = {
        "pilar": "LOGOS",
        "estrategia": "Lógica-Estrutural",
        "dominio": "ALGORITMIA",
        "subarvore": "RESOLUÇÃO",
        "conceito_foco": "DECOMPOSICAO",
        "score": 0.85,
        "confianca": 0.88,
    }

    test_cells = [
        {"uid": "N4_ALGORITMIA_1_A", "score": 0.92},
        {"uid": "N4_ALGORITMIA_1_B", "score": 0.87},
        {"uid": "N4_ALGORITMIA_2_A", "score": 0.78},
    ]

    result = synthesizer.synthesize(
        SynthesisInput(
            query="Como decompor um problema complexo em partes menores?",
            routing_decision=test_routing,
            retrieved_cells=test_cells,
        )
    )

    print("=== SYNTHESIS OUTPUT ===")
    print(f"Contexto:\n{result.context_summary}")
    print(f"\nPrompt ({len(result.prompt)} chars):")
    print(result.prompt[:500])
    print(f"\nCélulas referenciadas: {result.cell_references}")
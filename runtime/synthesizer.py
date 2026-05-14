"""
ENGINE DE SÍNTESE — Montagem dinâmica de prompts e respostas.

Transforma contexto ontológico (classificação + retrieval + grafo)
em prompts enriquecidos e respostas compostas, respeitando a estratégia
do pilar selecionado e a assinatura semântica das células.

Fase 6b do Roadmap da Ontologia Fractal.

Versão do Roadmap Gemini: implementa Formato Canônico do Arquiteto de Prompts
com as 4 seções obrigatórias e persona de Arquiteto Sênior.
"""

from __future__ import annotations

import json
import logging
import os
import re
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


# ── Contexto por pilar (injetado no Master Template) ──────────────────────

PILAR_CONTEXTOS: Dict[str, str] = {
    "LOGOS": (
        "Pilar LOGOS (Lógica-Estrutural): foco em decomposição lógica, "
        "verificabilidade e coerência dedutiva. Cada passo deve ser "
        "estruturado, sequencial e rastreável."
    ),
    "BIOS": (
        "Pilar BIOS (Orgânico-Vital): foco em ciclos de vida, homeostase, "
        "interdependências ecossistêmicas e sustentabilidade adaptativa."
    ),
    "PATHOS": (
        "Pilar PATHOS (Relacional-Significativo): foco em impacto humano, "
        "empatia, conexões significativas e múltiplas perspectivas."
    ),
    "KHAOS": (
        "Pilar KHAOS (Transformacional-Criativo): foco em rupturas, "
        "disrupção criativa, possibilidades emergentes e evolução contínua."
    ),
    "APEIRON": (
        "Pilar APEIRON (Estratégico-Transcendente): foco em padrões universais, "
        "visão sistêmica multi-escala e transcendência de limitações imediatas."
    ),
    "MYTHOS": (
        "Pilar MYTHOS (Narrativo-Simbólico): foco em narrativas profundas, "
        "arquétipos, simbolismo e significado transformador."
    ),
}

# ── Master Template — Formato Canônico do Arquiteto de Prompts ────────────
# Este template é o wrapper final que impõe as 4 seções obrigatórias.
# O LLM DEVE seguir este formato EXATAMENTE.

MASTER_TEMPLATE = """Você é um Arquiteto de Prompts Sênior operando sob a Ontologia Fractal MestreCuca.
Sua tarefa é receber um problema, classificá-lo ontologicamente e produzir
um Prompt Arquitetado completo e executável.

{contexto_pilar}

## Dados de Entrada
- **Query original:** {query}
- **Domínio:** {dominio}
- **Subárvore:** {subarvore}
- **Célula focal:** {celula}
- **Classificação:** {classificacao_texto}

## Conceitos Ativados ({num_cells} células)
{conceitos_ativados}

## Relações Identificadas
{relacoes}

{restricoes_adicionais}

---

INSTRUÇÃO: Produza a resposta FINAL no seguinte formato canônico, com EXATAMENTE
4 seções. Não adicione prólogo, epílogo, resumos ou comentários fora deste formato.
O output deve ser utilizável diretamente como prompt de engenharia.

### 1. CLASSIFICAÇÃO
- Vetor: {eixo}
- Pilar: {pilar}
- Domínio: {dominio}
- Subárvore: {subarvore}
- Célula: {celula}

### 2. LEITURA ESTRATÉGICA
{leitura_estrategica}

### 3. RESPOSTA EXECUTÁVEL
{resposta_executavel}

### 4. OTIMIZAÇÃO
{otimizacao}
"""


def _build_classificacao_texto(classification: Optional[dict]) -> str:
    """Gera texto legível da classificação N0→N4."""
    if not classification:
        return "Não classificada"
    classif = classification.get("classificacao", {})
    n0 = classif.get("n0_eixo", {})
    n1 = classif.get("n1_pilar", {})
    n2 = classif.get("n2_dominio", {})
    n3 = classif.get("n3_subarvore", {})
    n4 = classif.get("n4_celula", {})
    parts = []
    if n0.get("eixo"):
        parts.append(f"Eixo: {n0['eixo']}")
    if n1.get("pilar"):
        parts.append(f"Pilar: {n1['pilar']}")
    if n2.get("dominio"):
        parts.append(f"Domínio: {n2['dominio']}")
    if n3.get("subarvore"):
        parts.append(f"Subárvore: {n3['subarvore']}")
    if n4.get("celula_nome"):
        parts.append(f"Célula: {n4['celula_nome']}")
    return " | ".join(parts) if parts else "Não classificada"


def _gerar_leitura_estrategica(
    query: str,
    pilar: str,
    dominio: str,
    subarvore: str,
    celula: str,
    conceitos: List[dict],
) -> str:
    """
    Gera a seção de Leitura Estratégica (2-3 parágrafos).
    Analisa o problema real sob a perspectiva ontológica do pilar.
    """
    nomes = [c.get("data", {}).get("nome", c.get("uid", "")) for c in conceitos[:8]]
    nomes_unicos = list(dict.fromkeys(nomes))

    contexto = " ".join(nomes_unicos) if nomes_unicos else "conhecimento disponível"

    leituras = {
        "LOGOS": (
            f"A query '{query}' revela uma necessidade de decomposição lógica "
            f"estrutural. O domínio {dominio} na subárvore {subarvore} aponta "
            f"para uma arquitetura de resolução baseada em relações causais "
            f"entre os conceitos ativados: {contexto}. A célula focal {celula} "
            f"sugere que o problema central reside na estruturação e organização "
            f"das dependências. A abordagem deve priorizar clareza, verificabilidade "
            f"e progressão lógica de premissas para conclusões."
        ),
        "BIOS": (
            f"A query '{query}' indica uma questão sistêmica orgânica que exige "
            f"análise de interdependências vivas. No domínio {dominio}, subárvore "
            f"{subarvore}, os conceitos ativados — {contexto} — formam um ecossistema "
            f"com ciclos de retroalimentação. A célula focal {celula} destaca um "
            f"ponto crítico de homeostase. A leitura estratégica deve considerar "
            f"limites de capacidade, ciclos de vida e equilíbrio dinâmico."
        ),
        "PATHOS": (
            f"A query '{query}' expressa uma necessidade relacional e significativa. "
            f"No contexto do domínio {dominio} ({subarvore}), os conceitos "
            f"ativados — {contexto} — revelam tensões e conexões humanas profundas. "
            f"A célula focal {celula} indica que o impacto emocional e social é "
            f"central. A leitura deve considerar múltiplas perspectivas, empatia "
            f"e o reconhecimento da dimensão subjetiva envolvida."
        ),
        "KHAOS": (
            f"A query '{query}' sinaliza uma necessidade de ruptura e transformação. "
            f"No domínio {dominio}, subárvore {subarvore}, os conceitos "
            f"ativados — {contexto} — apontam para tensões criativas e "
            f"oportunidades de disrupção. A célula focal {celula} marca um ponto "
            f"de inflexão. A leitura estratégica deve explorar fronteiras, "
            f"questionar premissas e abraçar a ambiguidade como catalisador."
        ),
        "APEIRON": (
            f"A query '{query}' exige visão sistêmica e transcendência de limites "
            f"imediatos. No domínio {dominio}, subárvore {subarvore}, os conceitos "
            f"ativados — {contexto} — revelam padrões em múltiplas escalas. "
            f"A célula focal {celula} sugere uma conexão com princípios universais. "
            f"A leitura deve escalar a análise, buscar analogias estruturais e "
            f"propor uma visão integradora que transcenda o contexto imediato."
        ),
        "MYTHOS": (
            f"A query '{query}' carrega uma dimensão narrativa e simbólica. "
            f"No domínio {dominio}, subárvore {subarvore}, os conceitos "
            f"ativados — {contexto} — evocam arquétipos e padrões simbólicos. "
            f"A célula focal {celula} conecta-se a uma narrativa profunda. "
            f"A leitura deve enquadrar a questão em uma jornada significativa, "
            f"extraindo significado e conectando com tradições de sabedoria."
        ),
    }
    return leituras.get(pilar, leituras["LOGOS"])


def _gerar_resposta_executavel(
    query: str,
    pilar: str,
    dominio: str,
    subarvore: str,
    celula: str,
    conceitos: List[dict],
) -> str:
    """
    Gera a seção de Resposta Executável (checklist + passos algorítmicos).
    """
    nomes = [c.get("data", {}).get("nome", c.get("uid", "")) for c in conceitos[:6]]

    passos = {
        "LOGOS": [
            f"1. Decompor '{query}' em premissas atômicas verificáveis.",
            f"2. Mapear dependências lógicas entre os conceitos: {', '.join(nomes[:4])}.",
            "3. Construir cadeia dedutiva: premissa → inferência → conclusão.",
            "4. Validar cada passo com contraexemplos e testes de consistência.",
            "5. Consolidar resultado final com critérios de aceitação explícitos.",
        ],
        "BIOS": [
            f"1. Mapear o ecossistema envolvido em '{query}' e seus ciclos ativos.",
            f"2. Identificar pontos de homeostase e alavancas de mudança.",
            f"3. Avaliar impactos de curto e longo prazo nos conceitos: {', '.join(nomes[:4])}.",
            "4. Propor soluções adaptativas com mecanismos de feedback.",
            "5. Definir indicadores de saúde do sistema e limiares de alerta.",
        ],
        "PATHOS": [
            f"1. Identificar os stakeholders e suas perspectivas em '{query}'.",
            f"2. Mapear conexões emocionais e relacionais entre: {', '.join(nomes[:4])}.",
            "3. Avaliar o impacto humano de cada possível ação.",
            "4. Propor abordagens que respeitem dignidade e valores.",
            "5. Validar com múltiplas perspectivas antes de consolidar.",
        ],
        "KHAOS": [
            f"1. Questionar as premissas fundamentais de '{query}'.",
            f"2. Explorar possibilidades disruptivas com: {', '.join(nomes[:4])}.",
            "3. Identificar pontos de ruptura e oportunidades emergentes.",
            "4. Propor caminhos criativos que equilibrem destruição e reconstrução.",
            "5. Definir critérios de evolução e adaptação contínua.",
        ],
        "APEIRON": [
            f"1. Escalar '{query}' para múltiplas dimensões e perspectivas.",
            f"2. Identificar padrões universais com: {', '.join(nomes[:4])}.",
            "3. Buscar analogias estruturais em domínios aparentemente distantes.",
            "4. Propor uma visão integradora que transcenda limitações imediatas.",
            "5. Definir princípios orientadores de longo prazo.",
        ],
        "MYTHOS": [
            f"1. Enquadrar '{query}' em uma narrativa significativa e coerente.",
            f"2. Identificar arquétipos e símbolos em: {', '.join(nomes[:4])}.",
            "3. Mapear a jornada simbólica do problema à solução.",
            "4. Extrair significado profundo e aplicável.",
            "5. Consolidar como história transformadora com morale prático.",
        ],
    }
    passos_list = passos.get(pilar, passos["LOGOS"])

    checklist = "\n".join([f"- [ ] {p}" for p in passos_list])
    return f"**Passos ({pilar}):**\n\n{checklist}"


def _gerar_otimizacao(
    pilar: str,
    dominio: str,
    subarvore: str,
    celula: str,
    routing: dict,
) -> str:
    """Gera a seção de Otimização (variáveis estratégicas e edge cases)."""
    score = routing.get("score", 0)
    confianca = routing.get("confianca", 0)

    otimizacoes = {
        "LOGOS": [
            "Melhorias incrementais: refinar premissas com dados adicionais.",
            "Alternativas: considerar abordagens dedutivas vs. indutivas.",
            f"Edge case: score de roteamento {score:.4f} — verificar se abaixo de 0.5.",
            "Ponto de atenção: consistência lógica entre premissas e conclusão.",
        ],
        "BIOS": [
            "Melhorias incrementais: monitorar ciclos de feedback em tempo real.",
            "Alternativas: intervenção gradual vs. transformação radical.",
            f"Edge case: confiança {confianca:.4f} — avaliar estabilidade do ecossistema.",
            "Ponto de atenção: respeitar limites de capacidade (homeostase).",
        ],
        "PATHOS": [
            "Melhorias incrementais: aprofundar escuta ativa com stakeholders.",
            "Alternativas: mediação direta vs. facilitação indireta.",
            f"Edge case: tensões entre perspectivas divergentes.",
            "Ponto de atenção: equilibrar empatia com objetividade.",
        ],
        "KHAOS": [
            "Melhorias incrementais: testar micro-rupturas antes de disrupções grandes.",
            "Alternativas: inovação incremental vs. revolucionária.",
            f"Edge case: score {score:.4f} — risco de transformação descontrolada.",
            "Ponto de atenção: equilibrar destruição criativa com estabilidade.",
        ],
        "APEIRON": [
            "Melhorias incrementais: expandir análise para escalas superiores.",
            "Alternativas: visão de sistema vs. análise de componentes.",
            f"Edge case: abrangência excessiva pode diluir foco.",
            "Ponto de atenção: manter coerência entre escalas.",
        ],
        "MYTHOS": [
            "Melhorias incrementais: enriquecer narrativa com arquétipos complementares.",
            "Alternativas: narrativa heroica vs. narrativa de transformação.",
            f"Edge case: simbolismo pode obscurecer ação prática.",
            "Ponto de atenção: ancorar significado simbólico em resultados concretos.",
        ],
    }
    items = otimizacoes.get(pilar, otimizacoes["LOGOS"])
    return "\n".join([f"- {item}" for item in items])


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
        Executa a síntese completa com Formato Canônico do Arquiteto de Prompts.

        Fluxo:
        1. Determina pilar e contexto
        2. Monta referências de células
        3. Monta conceitos ativados
        4. Monta relações
        5. Gera as 4 seções canônicas via Master Template
        6. Retorna output estruturado
        """
        routing = synthesis_input.routing_decision
        pilar = routing.get("pilar", "LOGOS")
        dominio = routing.get("dominio", "N/A")
        subarvore = routing.get("subarvore", "N/A")
        celula = routing.get("conceito_foco", "N/A")
        
        # Extrai o eixo da classificação em vez do roteamento
        classif_dict = synthesis_input.classification.get("classificacao", {}) if synthesis_input.classification else {}
        eixo = classif_dict.get("n0_eixo", {}).get("eixo", "N/A")

        # Obtém contexto do pilar
        contexto_pilar = PILAR_CONTEXTOS.get(
            pilar, PILAR_CONTEXTOS["LOGOS"]
        )

        # Monta referências de células
        cell_refs = self._build_cell_references(synthesis_input)

        # Monta conceitos ativados
        conceitos = self._build_concepts(cell_refs)

        # Monta relações
        relacoes = self._build_relations(cell_refs)

        # Monta restrições adicionais
        restricoes = self._build_restrictions(synthesis_input)

        # Gera classificação textual
        classificacao_texto = _build_classificacao_texto(
            synthesis_input.classification
        )

        # Gera Leitura Estratégica (Seção 2)
        leitura_estrategica = _gerar_leitura_estrategica(
            query=synthesis_input.query,
            pilar=pilar,
            dominio=dominio,
            subarvore=subarvore,
            celula=celula,
            conceitos=cell_refs,
        )

        # Gera Resposta Executável (Seção 3)
        resposta_executavel = _gerar_resposta_executavel(
            query=synthesis_input.query,
            pilar=pilar,
            dominio=dominio,
            subarvore=subarvore,
            celula=celula,
            conceitos=cell_refs,
        )

        # Gera Otimização (Seção 4)
        otimizacao = _gerar_otimizacao(
            pilar=pilar,
            dominio=dominio,
            subarvore=subarvore,
            celula=celula,
            routing=routing,
        )

        # Monta prompt final via Master Template
        prompt = MASTER_TEMPLATE.format(
            contexto_pilar=contexto_pilar,
            query=synthesis_input.query,
            dominio=dominio,
            subarvore=subarvore,
            celula=celula,
            classificacao_texto=classificacao_texto,
            num_cells=len(cell_refs),
            conceitos_ativados=conceitos,
            relacoes=relacoes,
            restricoes_adicionais=restricoes,
            eixo=eixo,
            pilar=pilar,
            leitura_estrategica=leitura_estrategica,
            resposta_executavel=resposta_executavel,
            otimizacao=otimizacao,
        )

        # Monta sumário de contexto para logging/auditoria
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
                "template_usado": "MASTER_CANONICO",
                "dominio": dominio,
                "subarvore": subarvore,
                "formato": "ARQUITETO_PROMPTS_V1",
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
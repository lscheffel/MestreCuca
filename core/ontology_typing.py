#!/usr/bin/env python3
"""Módulo de inferência de natureza ontológica.

Fornece funções para classificar células N4 por natureza ontológica
com base em análise de keywords no contexto do domínio/pilar.

Naturezas suportadas:
  - processo: ações dinâmicas (decompor, transformar, iterar...)
  - estado: condições estáveis (integridade, equilíbrio, consistência...)
  - fenomeno: manifestações observáveis (ressonância, entropia, caos...)
  - principio: leis fundamentais (causa, efeito, conservação...)
  - mecanismo: padrões operacionais (feedback, cascata, recursão...)
  - estrutura: organização espacial/lógica (hierarquia, rede, camada...)
  - arquétipo: padrões simbólicos (herói, sombra, trickster...)
  - dinamica: padrões de mudança (transformação, evolução, ciclo...)
  - restricao: limites e condições (limiar, fronteira, proibição...)
  - vetor: direção e magnitude (convergência, divergência, gradiente...)
"""

from __future__ import annotations

import re
import unicodedata

# ---------------------------------------------------------------------------
# Base de conhecimento: keywords por natureza
# ---------------------------------------------------------------------------

NATURE_KEYWORDS: dict[str, list[str]] = {
    "processo": [
        "decompor", "transformar", "iterar", "resolver",
        "executar", "processar", "calcular", "ordenar",
        "construir", "gerar", "produzir", "criar",
        "identificar", "analisar", "avaliar", "verificar",
        "definir", "modelar", "planejar", "implementar",
        "otimizar", "validar", "testar", "revisar",
    ],
    "estado": [
        "integridade", "equilíbrio", "estabilidade", "consistência",
        "coerência", "harmonia", "estrutura", "organização",
        "funcionalidade", "saúde", "normalidade", "adequação",
        "alinhamento", "convergência", "estabilidade", "permanência",
    ],
    "fenomeno": [
        "ressonância", "entropia", "caos", "emergência",
        "complexidade", "padrão", "frequência", "onda",
        "campo", "potencial", "magnitude", "escala",
        "ciclo", "fluxo", "propagação", "manifestação",
    ],
    "principio": [
        "causa", "efeito", "conservação", "inércia",
        "ação_reação", "determinismo", "probabilidade",
        "universalidade", "relatividade", "limitação",
        "irreversibilidade", "necessidade", "suficiência",
    ],
    "mecanismo": [
        "feedback", "cascata", "recursão", "iteração",
        "loops", "ciclo", "regulação", "controle",
        "automação", "sincronização", "amplificação",
        "dampagem", "buffer", "cache", "pipeline",
    ],
    "estrutura": [
        "hierarquia", "rede", "camada", "nó", "aresta",
        "árvore", "grafo", "malha", "topologia",
        "composição", "modularidade", "encapsulamento",
        "fronteira", "interface", "protocolo",
    ],
    "arquétipo": [
        "herói", "sombra", "trickster", "mentor",
        "guardião", "criador", "destruidor", "sábio",
        "amante", "bufão", "inocente", "explorador",
        "rebelde", "mago", "governante", "mártir",
    ],
    "dinamica": [
        "transformação", "evolução", "ciclo", "fluxo",
        "mudança", "transição", "adaptação", "migração",
        "crescimento", "decadência", "renascimento",
        "metamorfose", "progressão", "regressão",
    ],
    "restricao": [
        "limiar", "fronteira", "proibição", "condição",
        "prerequisito", "dependência", "limitação", "vínculo",
        "obrigação", "restrição", "regra", "norma",
        "tolerância", "margem", "limite",
    ],
    "vetor": [
        "convergência", "divergência", "gradiente", "direção",
        "magnitude", "intensidade", "aceleração", "trajetória",
        "tendência", "impulso", "força", "energia",
    ],
}

# Mapeamento de pilar → naturezas mais prováveis (ordem de prioridade)
PILLAR_NATURE_PRIORITIES: dict[str, list[str]] = {
    "LOGOS": ["processo", "estrutura", "mecanismo", "principio", "restricao"],
    "BIOS": ["estado", "processo", "dinamica", "mecanismo", "fenomeno"],
    "PATHOS": ["dinamica", "arquétipo", "fenomeno", "processo", "estado"],
    "KHAOS": ["fenomeno", "dinamica", "processo", "vetor", "mecanismo"],
    "APEIRON": ["fenomeno", "vetor", "principio", "processo", "estado"],
    "MYTHOS": ["arquétipo", "fenomeno", "dinamica", "processo", "estado"],
}

# Mapeamento de domínio → naturezas mais prováveis
DOMAIN_NATURE_PRIORITIES: dict[str, list[str]] = {
    "ALGORITMIA": ["processo", "mecanismo", "estrutura"],
    "NOMOS": ["restricao", "principio", "estrutura"],
    "MECÂNICA": ["processo", "mecanismo", "principio"],
    "OIKOS": ["estado", "estrutura", "processo"],
    "SOMA": ["estado", "processo", "mecanismo"],
    "METABOLISMO": ["processo", "dinamica", "mecanismo"],
    "ETHOS": ["restricao", "principio", "processo"],
    "ALTERIDADE": ["dinamica", "processo", "estado"],
    "ESTÉTICA": ["fenomeno", "vetor", "dinamica"],
    "ENTROPIA": ["fenomeno", "processo", "dinamica"],
    "SINGULARIDADE": ["fenomeno", "principio", "vetor"],
    "SÍNTESE": ["processo", "mecanismo", "dinamica"],
    "ESCALA": ["vetor", "fenomeno", "principio"],
    "VIBRATIO": ["fenomeno", "vetor", "mecanismo"],
    "VÁCUO": ["estado", "fenomeno", "principio"],
    "ARQUÉTIPO": ["arquétipo", "fenomeno", "dinamica"],
    "NARRATIVA": ["dinamica", "processo", "arquétipo"],
    "MISTÉRIO": ["fenomeno", "principio", "estado"],
}


# ---------------------------------------------------------------------------
# Inferência de natureza
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Tokeniza texto em palavras normalizadas (sem acento, lowercase)."""
    import unicodedata
    normalized = unicodedata.normalize("NFKD", text.lower())
    cleaned = "".join(
        ch for ch in normalized if unicodedata.category(ch) != "Mn"
    )
    return re.findall(r"[a-záàâãéèêíìîóòôõúùûüçñ]+", cleaned)


def infer_natureza(cell_data: dict) -> str:
    """Inferir natureza ontológica a partir do conteúdo da célula.

    Usa análise de keywords no contexto do domínio/pilar.
    Combina score de keyword matching com prioridade de domínio e pilar.

    Args:
        cell_data: Dicionário com campos 'nome', 'gatilho', 'acao',
                   'dominio', 'pilar' (opcional).

    Returns:
        A natureza com maior score de correspondência.

    Examples:
        >>> infer_natureza({"nome": "DECOMPOSIÇÃO", "acao": "Dividir em subpartes", "dominio": "ALGORITMIA"})
        'processo'
        >>> infer_natureza({"nome": "EQUILÍBRIO", "acao": "Manter estabilidade", "dominio": "SOMA"})
        'estado'
    """
    nome = cell_data.get("nome", "")
    gatilho = cell_data.get("gatilho", "")
    acao = cell_data.get("acao", "")
    dominio = cell_data.get("dominio", "")
    pilar = cell_data.get("pilar", "")

    # Concatenar todos os campos textuais para análise
    full_text = f"{nome} {gatilho} {acao}"
    tokens = _tokenize(full_text)

    # Calcular scores por natureza
    scores: dict[str, float] = {}
    for natureza, keywords in NATURE_KEYWORDS.items():
        score = 0.0
        for kw in keywords:
            if kw in tokens:
                score += 1.0
        if score > 0:
            scores[natureza] = score

    # Aplicar bônus de domínio
    domain_priorities = DOMAIN_NATURE_PRIORITIES.get(dominio, [])
    for rank, natureza in enumerate(domain_priorities):
        if natureza in scores:
            scores[natureza] += (len(domain_priorities) - rank) * 0.5

    # Aplicar bônus de pilar
    pillar_priorities = PILLAR_NATURE_PRIORITIES.get(pilar, [])
    for rank, natureza in enumerate(pillar_priorities):
        if natureza in scores:
            scores[natureza] += (len(pillar_priorities) - rank) * 0.3

    # Se não há correspondência, usar fallback baseado no domínio
    if not scores:
        fallback = DOMAIN_NATURE_PRIORITIES.get(dominio, ["processo"])
        return fallback[0]

    # Retornar natureza com maior score
    return max(scores, key=scores.get)


def validate_natureza(natureza: str, allowed_natures: list[str] | None = None) -> bool:
    """Valida se a natureza é reconhecida na taxonomia.

    Args:
        natureza: Nome da natureza a validar.
        allowed_natures: Lista opcional de naturezas permitidas. Se None,
                         usa todas as naturezas conhecidas.

    Returns:
        True se a natureza é válida, False caso contrário.

    Examples:
        >>> validate_natureza("processo")
        True
        >>> validate_natureza("desconhecido")
        False
        >>> validate_natureza("processo", ["processo", "estado"])
        True
    """
    valid = natureza in NATURE_KEYWORDS
    if allowed_natures is not None:
        valid = valid and natureza in allowed_natures
    return valid


def normalize_natureza(natureza: str) -> str:
    """Normaliza para minúsculas, sem acentos, singular.

    Args:
        natureza: Nome da natureza a normalizar.

    Returns:
        Natureza normalizada.

    Examples:
        >>> normalize_natureza("Processos")
        'processo'
        >>> normalize_natureza("ESTADOS")
        'estado'
    """
    import unicodedata
    normalized = unicodedata.normalize("NFKD", natureza.lower().strip())
    without_accents = "".join(
        ch for ch in normalized if unicodedata.category(ch) != "Mn"
    )
    # Remover plural simples (s final)
    singular = without_accents.rstrip("s")
    # Mapear variantes comuns
    variantes = {
        "process": "processo",
        "estad": "estado",
        "fenomen": "fenomeno",
        "principi": "principio",
        "mecanism": "mecanismo",
        "estrutur": "estrutura",
        "arquetip": "arquétipo",
        "dinamic": "dinamica",
        "restrica": "restricao",
        "vetor": "vetor",
    }
    return variantes.get(singular, singular)
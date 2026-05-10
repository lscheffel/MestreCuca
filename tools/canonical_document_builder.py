#!/usr/bin/env python3
"""Construtor de Documentos Canônicos para Células N4.

Gera textos expandidos a partir dos dados enriquecidos de cada célula N4,
servindo como input para geração de embeddings vetoriais.

Cada documento canônico é composto por múltiplas seções que capturam
diferentes aspectos semânticos da célula, permitindo a construção de
embeddings especializados (estrutural, semântico, operacional, simbólico).
"""

from __future__ import annotations


def build_canonical_document(cell_data: dict) -> str:
    """Gera o documento canônico completo para uma célula N4.

    Combina todas as perspectivas em um texto expandido, otimizado para
    geração de embeddings densos que capturem a totalidade semântica da célula.

    Args:
        cell_data: Dicionário com os dados enriquecidos da célula N4.

    Returns:
        Texto expandido contendo todos os atributos relevantes.
    """
    nome = cell_data.get("nome", "DESCONHECIDO")
    descricao = _build_description(cell_data)
    natureza = cell_data.get("natureza", "")
    funcoes = cell_data.get("funcao_cognitiva", [])
    eixo = cell_data.get("axis", "")
    pilar = cell_data.get("pilar", "")
    dominio = cell_data.get("dominio", "")
    subarvore = cell_data.get("n3_name", "")
    relacoes = _format_relations(cell_data.get("relacoes", []))
    opostos = cell_data.get("opostos", [])
    exemplos = _format_examples(cell_data.get("exemplos", []))
    analogias = _format_analogies(cell_data.get("analogias", []))
    aplicacoes = _build_applications(cell_data)
    vetor_simbolico = _build_symbolic_vector(cell_data)
    gatilho = cell_data.get("gatilho", "")
    acao = cell_data.get("acao", "")
    restricao = cell_data.get("restricao", "")
    verificacao = cell_data.get("verificacao", "")
    assinatura = cell_data.get("assinatura_semantica", {})

    parts = [
        f"CONCEITO: {nome}",
        f"DESCRIÇÃO: {descricao}",
        f"NATUREZA: {natureza}",
        f"FUNÇÕES COGNITIVAS: {', '.join(funcoes) if funcoes else 'não definidas'}",
        f"CONTEXTO ONTOLÓGICO: {eixo} > {pilar} > {dominio} > {subarvore}",
        f"GATILHO: {gatilho}",
        f"AÇÃO: {acao}",
        f"RESTRICAO: {restricao}",
        f"VERIFICAÇÃO: {verificacao}",
    ]

    if relacoes:
        parts.append(f"RELAÇÕES: {relacoes}")
    if opostos:
        parts.append(f"OPOSTOS: {', '.join(opostos)}")
    if exemplos:
        parts.append(f"EXEMPLOS: {exemplos}")
    if analogias:
        parts.append(f"ANALOGIAS: {analogias}")

    parts.extend([
        f"APLICAÇÕES: {aplicacoes}",
        f"VETOR SIMBÓLICO: {vetor_simbolico}",
    ])

    # Incluir assinatura semântica como metadados
    if assinatura:
        sig_parts = [f"{k}:{v:.3f}" for k, v in assinatura.items()]
        parts.append(f"ASSINATURA SEMÂNTICA: {', '.join(sig_parts)}")

    return " | ".join(parts)


def build_structural_embedding_text(cell_data: dict) -> str:
    """Gera texto para embedding estrutural (hierarquia e posição ontológica).

    Foca na localização da célula na árvore fractal e suas conexões
    hierárquicas, capturando a estrutura N0→N1→N2→N3→N4.

    Args:
        cell_data: Dicionário com os dados da célula N4.

    Returns:
        Texto estrutural expandido.
    """
    eixo = cell_data.get("axis", "")
    pilar = cell_data.get("pilar", "")
    dominio = cell_data.get("dominio", "")
    subarvore = cell_data.get("n3_name", "")
    nome = cell_data.get("nome", "")
    path = cell_data.get("path", "")
    hierarchical_id = cell_data.get("hierarchical_id", "")
    cell_letter = cell_data.get("cell_letter", "")
    n3_ref = cell_data.get("n3_ref", "")
    legacy_id = cell_data.get("legacy_id", "")

    return (
        f"EIXO {eixo} | PILAR {pilar} | DOMÍNIO {dominio} | "
        f"SUBÁRVORE {subarvore} | CÉLULA {nome} | "
        f"Caminho: {path} | ID Hierárquico: {hierarchical_id} | "
        f"Célula {cell_letter} da subárvore {n3_ref} | "
        f"Legacy: {legacy_id} | "
        f"Posição: nível N4 na hierarquia fractal da ontologia"
    )


def build_semantic_embedding_text(cell_data: dict) -> str:
    """Gera texto para embedding semântico (descrição expandida).

    Captura o significado profundo da célula através de descrição,
    gatilho, ação, restrição e verificação em linguagem natural expandida.

    Args:
        cell_data: Dicionário com os dados da célula N4.

    Returns:
        Texto semântico expandido.
    """
    nome = cell_data.get("nome", "")
    nome_normalizado = cell_data.get("nome_normalizado", "")
    descricao = _build_description(cell_data)
    gatilho = cell_data.get("gatilho", "")
    acao = cell_data.get("acao", "")
    restricao = cell_data.get("restricao", "")
    verificacao = cell_data.get("verificacao", "")
    natureza = cell_data.get("natureza", "")
    assinatura = cell_data.get("assinatura_semantica", {})

    # Expandir assinatura semântica em texto descritivo
    sig_desc = _expand_signature(assinatura)

    return (
        f"Conceito {nome} ({nome_normalizado}): {descricao}. "
        f"Este conceito é de natureza {natureza}. "
        f"É acionado quando: {gatilho}. "
        f"A ação prescrita é: {acao}. "
        f"A restrição aplicável é: {restricao}. "
        f"Critério de verificação: {verificacao}. "
        f"Perfil semântico: {sig_desc}"
    )


def build_operational_embedding_text(cell_data: dict) -> str:
    """Gera texto para embedding operacional (funções cognitivas e ações).

    Foca nas funções cognitivas que esta célula executa e nas operações
    concretas que ela define, facilitando o matching com queries de ação.

    Args:
        cell_data: Dicionário com os dados da célula N4.

    Returns:
        Texto operacional expandido.
    """
    nome = cell_data.get("nome", "")
    funcoes = cell_data.get("funcao_cognitiva", [])
    acao = cell_data.get("acao", "")
    gatilho = cell_data.get("gatilho", "")
    verificacao = cell_data.get("verificacao", "")
    restricao = cell_data.get("restricao", "")
    pilar = cell_data.get("pilar", "")
    dominio = cell_data.get("dominio", "")
    subarvore = cell_data.get("n3_name", "")
    exemplos = cell_data.get("exemplos", [])

    funcoes_str = ", ".join(funcoes) if funcoes else "não especificadas"

    ex_texts = []
    for ex in exemplos[:3]:  # Limitar a 3 exemplos
        ex_texts.append(ex.get("texto", ""))
    exemplos_str = " | ".join(ex_texts) if ex_texts else "sem exemplos"

    return (
        f"Operacional: {nome} no contexto de {pilar}/{dominio}/{subarvore}. "
        f"Funções cognitivas executadas: {funcoes_str}. "
        f"Ação definida: {acao}. "
        f"Condição de ativação: {gatilho}. "
        f"Critério de verificação: {verificacao}. "
        f"Restrição operacional: {restricao}. "
        f"Exemplos de aplicação: {exemplos_str}"
    )


def build_symbolic_embedding_text(cell_data: dict) -> str:
    """Gera texto para embedding simbólico (tags, arquétipos, opostos).

    Captura a camada simbólica e relacional da célula, incluindo tags,
    naturezas, analogias, oposições e padrões arquetípicos.

    Args:
        cell_data: Dicionário com os dados da célula N4.

    Returns:
        Texto simbólico expandido.
    """
    nome = cell_data.get("nome", "")
    tags = cell_data.get("tags", [])
    natureza = cell_data.get("natureza", "")
    opostos = cell_data.get("opostos", [])
    analogias = cell_data.get("analogias", [])
    relacoes = cell_data.get("relacoes", [])
    pilar = cell_data.get("pilar", "")
    dominio = cell_data.get("dominio", "")
    axis = cell_data.get("axis", "")
    uid = cell_data.get("uid", "")

    tags_str = ", ".join(tags) if tags else "sem tags"

    # Formatar opostos como nomes legíveis
    oposto_nomes = []
    for opp_uid in opostos[:5]:  # Limitar
        oposto_nomes.append(opp_uid)
    opostos_str = ", ".join(oposto_nomes) if oposto_nomes else "sem opositos"

    # Formatar analogias
    analogia_texts = []
    for a in analogias[:3]:
        analogia_texts.append(a.get("texto", ""))
    analogias_str = " | ".join(analogia_texts) if analogia_texts else "sem analogias"

    # Formatar relações tipadas
    rel_tipos = set()
    for rel in relacoes:
        rel_tipos.add(rel.get("tipo", "desconhecido"))
    relacoes_str = ", ".join(sorted(rel_tipos)) if rel_tipos else "sem relações"

    return (
        f"Simbólico: {nome} ({uid}) | "
        f"Pilar: {pilar} | Domínio: {dominio} | Eixo: {axis} | "
        f"Natureza: {natureza} | "
        f"Tags: {tags_str} | "
        f"Tipos de relação: {relacoes_str} | "
        f"Opostos: {opostos_str} | "
        f"Analogias: {analogias_str}"
    )


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def _build_description(cell_data: dict) -> str:
    """Constrói uma descrição rica a partir dos campos disponíveis."""
    nome = cell_data.get("nome", "")
    nome_normalizado = cell_data.get("nome_normalizado", "")
    gatilho = cell_data.get("gatilho", "")
    acao = cell_data.get("acao", "")
    restricao = cell_data.get("restricao", "")
    verificacao = cell_data.get("verificacao", "")

    parts = []
    if nome_normalizado:
        parts.append(f"{nome} ({nome_normalizado})")
    if gatilho:
        parts.append(f"Acionado por: {gatilho}")
    if acao:
        parts.append(f"Executa: {acao}")
    if restricao:
        parts.append(f"Restrição: {restricao}")
    if verificacao:
        parts.append(f"Verificação: {verificacao}")

    return ". ".join(parts) if parts else nome


def _format_relations(relations: list) -> str:
    """Formata relações tipadas em texto legível."""
    if not relations:
        return ""
    parts = []
    for rel in relations:
        target = rel.get("alvo", "desconhecido")
        tipo = rel.get("tipo", "relaciona")
        peso = rel.get("peso", 0)
        parts.append(f"{tipo}→{target}(peso:{peso})")
    return "; ".join(parts)


def _format_examples(exemplos: list) -> str:
    """Formata exemplos em texto concatenado."""
    if not exemplos:
        return ""
    return " | ".join(ex.get("texto", "") for ex in exemplos[:5])


def _format_analogies(analogias: list) -> str:
    """Formata analogias em texto concatenado."""
    if not analogias:
        return ""
    parts = []
    for a in analogias[:5]:
        texto = a.get("texto", "")
        tipo = a.get("tipo", "")
        parts.append(f"[{tipo}] {texto}")
    return " | ".join(parts)


def _build_applications(cell_data: dict) -> str:
    """Constrói texto de aplicações a partir de exemplos e funções cognitivas."""
    funcoes = cell_data.get("funcao_cognitiva", [])
    nome = cell_data.get("nome", "")
    dominio = cell_data.get("dominio", "")
    pilar = cell_data.get("pilar", "")

    aplicacoes = [
        f"Aplicação direta de {nome} em contextos de {dominio} sob o pilar {pilar}"
    ]
    for func in funcoes[:3]:
        aplicacoes.append(f"Execução de {func} como função cognitiva primária")

    return "; ".join(aplicacoes)


def _build_symbolic_vector(cell_data: dict) -> str:
    """Constrói representação simbólica compacta da célula."""
    tags = cell_data.get("tags", [])
    natureza = cell_data.get("natureza", "")
    axis = cell_data.get("axis", "")
    pilar = cell_data.get("pilar", "")
    dominio = cell_data.get("dominio", "")
    n3_name = cell_data.get("n3_name", "")
    nome = cell_data.get("nome", "")

    simbolos = [
        f"[{axis}]",
        f"[{pilar}]",
        f"[{dominio}]",
        f"[{n3_name}]",
        f"[natureza:{natureza}]",
    ]
    simbolos.extend(f"[{tag}]" for tag in tags[:10])

    return " ".join(simbolos)


def _expand_signature(assinatura: dict) -> str:
    """Expande a assinatura semântica em descrição textual."""
    if not assinatura:
        return "não disponível"
    dimensoes = {
        "abstracao": "nível de abstração",
        "complexidade": "grau de complexidade",
        "causalidade": "grau de causalidade",
        "emocionalidade": "carga emocional",
        "materialidade": "grau de materialidade",
        "simbolismo": "densidade simbólica",
        "dinamismo": "nível de dinamismo",
        "temporalidade": "ancoragem temporal",
        "ambiguidade": "grau de ambiguidade",
    }
    parts = []
    for chave, valor in assinatura.items():
        label = dimensoes.get(chave, chave)
        nivel = "baixo" if valor < 0.35 else ("médio" if valor < 0.65 else "alto")
        parts.append(f"{label}:{nivel}({valor:.2f})")
    return "; ".join(parts)
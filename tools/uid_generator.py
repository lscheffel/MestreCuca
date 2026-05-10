#!/usr/bin/env python3
"""Módulo de geração e validação de identificadores únicos permanentes (UIDs).

Fornece funções para normalização de texto, geração de UIDs em múltiplos
formatos, validação e construção de mapeamentos entre sistemas de identificação.

Sistemas de ID suportados:
  - UID permanente: N4_DECOMPOSICAO_BINARIA
  - Path estrutural: S1.L1.1.1-A
  - ID hierárquico: 1.1.1.1
  - ID legado: R1.1.1-A
"""

import re
import unicodedata

# ---------------------------------------------------------------------------
# Constantes de mapeamento
# ---------------------------------------------------------------------------

# Mapa de substituição de caracteres acentuados para ASCII
_ACCENT_MAP = str.maketrans(
    "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑáàâãäéèêëíìîïóòôõöúùûüçñ",
    "AAAAAEEEEIIIIOOOOOUUUUCNaaaaaeeeeiiiiooooouuuucn"
)

# Mapeamento de pilares para códigos de path
PILLAR_TO_PATH_CODE = {
    "LOGOS":   "L1",
    "BIOS":    "B2",
    "PATHOS":  "P3",
    "KHAOS":   "K1",
    "APEIRON": "A2",
    "MYTHOS":  "M3",
}

# Mapeamento inverso: código de path → pilar
PATH_CODE_TO_PILLAR = {v: k for k, v in PILLAR_TO_PATH_CODE.items()}

# Mapeamento de eixo (vetor) para código de path
AXIS_TO_PATH_CODE = {
    "SINTRÓPICO": "S1",
    "ENTRÓPICO":  "E2",
}

# Mapeamento numérico do eixo
PILLAR_NUM_TO_AXIS = {
    1: "SINTRÓPICO", 2: "SINTRÓPICO", 3: "SINTRÓPICO",
    4: "ENTRÓPICO",  5: "ENTRÓPICO",  6: "ENTRÓPICO",
}

PILLAR_NUM_TO_NAME = {
    1: "LOGOS", 2: "BIOS", 3: "PATHOS",
    4: "KHAOS", 5: "APEIRON", 6: "MYTHOS",
}

PILLAR_NAME_TO_NUM = {v: k for k, v in PILLAR_NUM_TO_NAME.items()}

# Domínios N2 por pilar (3 domínios por pilar)
PILLAR_DOMAINS = {
    "LOGOS":   ["ALGORITMIA", "NOMOS",     "MECÂNICA"],
    "BIOS":    ["OIKOS",      "SOMA",      "METABOLISMO"],
    "PATHOS":  ["ETHOS",      "ALTERIDADE","ESTÉTICA"],
    "KHAOS":   ["ENTROPIA",   "SINGULARIDADE", "SÍNTESE"],
    "APEIRON": ["ESCALA",     "VIBRATIO",  "VÁCUO"],
    "MYTHOS":  ["ARQUÉTIPO",  "NARRATIVA", "MISTÉRIO"],
}

# ---------------------------------------------------------------------------
# Normalização de texto
# ---------------------------------------------------------------------------

def normalize_text(text: str) -> str:
    """Remove acentos, converte para uppercase, substitui espaços por underscore.

    Aplica normalização NFKD para decompor caracteres compostos, remove
    acentos (diacríticos), converte para maiúsculas, substitui espaços e
    caracteres especiais por underscore, e mantém apenas [A-Z0-9_].

    Args:
        text: Texto a ser normalizado.

    Returns:
        String normalizada contendo apenas [A-Z0-9_].

    Examples:
        >>> normalize_text("Decomposição Binária")
        'DECOMPOSICAO_BINARIA'
        >>> normalize_text("Ressonância")
        'RESONANCIA'
    """
    if not isinstance(text, str) or not text.strip():
        return ""
    normalized = unicodedata.normalize("NFKD", text)
    without_accents = "".join(
        ch for ch in normalized if unicodedata.category(ch) != "Mn"
    )
    result = re.sub(r"[^A-Za-z0-9]+", "_", without_accents).upper()
    result = re.sub(r"_+", "_", result).strip("_")
    return result

# ---------------------------------------------------------------------------
# Geração de UIDs
# ---------------------------------------------------------------------------

def generate_uid(concept_name: str, nivel: str = "N4") -> str:
    """Gera UID permanente e imutável.

    Formato: {NIVEL}_{NOME_NORMALIZADO}

    O UID é determinístico: o mesmo concept_name sempre produz o mesmo UID.
    Serve como identificador primário imutável para cada célula N4.

    Args:
        concept_name: Nome do conceito (ex: "DECOMPOSIÇÃO BINÁRIA").
        nivel: Nível ontológico (N2, N3, N4). Padrão: "N4".

    Returns:
        UID no formato {NIVEL}_{NOME_NORMALIZADO}.

    Raises:
        ValueError: Se concept_name normaliza para string vazia ou nivel é inválido.

    Examples:
        >>> generate_uid("DECOMPOSIÇÃO BINÁRIA")
        'N4_DECOMPOSICAO_BINARIA'
        >>> generate_uid("RESOLUÇÃO", nivel="N3")
        'N3_RESOLUCAO'
    """
    normalized = normalize_text(concept_name)
    if not normalized:
        raise ValueError(f"concept_name '{concept_name}' normaliza para string vazia")
    nivel_upper = nivel.upper().strip()
    if not re.match(r"^N[0-9]+$", nivel_upper):
        raise ValueError(f"nivel inválido: '{nivel}'. Esperado formato N<numero>")
    return f"{nivel_upper}_{normalized}"


def generate_path(axis_code: str, pillar_code: str,
                  domain_num: str, subtree_num: str,
                  cell_letter: str) -> str:
    """Gera path estrutural no formato S1.L1.1.1-A.

    Formato: {AXIS}.{PILLAR}.{DOMAIN}.{SUBTREE}-{CELL}

    Args:
        axis_code: Código do eixo ('S1' para SINTRÓPICO, 'E2' para ENTRÓPICO).
        pillar_code: Código do pilar ('L1', 'B2', 'P3', 'K1', 'A2', 'M3').
        domain_num: Número do domínio N2 (1-3 dentro do pilar).
        subtree_num: Número da subárvore N3 (1-3 dentro do domínio).
        cell_letter: Letra da célula N4 ('A', 'B' ou 'C').

    Returns:
        Path no formato S1.L1.1.1-A.

    Raises:
        ValueError: Se qualquer argumento for inválido.

    Examples:
        >>> generate_path("S1", "L1", "1", "1", "A")
        'S1.L1.1.1-A'
        >>> generate_path("E2", "K1", "1", "1", "C")
        'E2.K1.1.1-C'
    """
    if axis_code not in ("S1", "E2"):
        raise ValueError(f"axis_code inválido: '{axis_code}'. Esperado 'S1' ou 'E2'")
    if pillar_code not in PILLAR_TO_PATH_CODE.values():
        raise ValueError(f"pillar_code inválido: '{pillar_code}'. "
                         f"Esperado um de {list(PILLAR_TO_PATH_CODE.values())}")
    if domain_num not in ("1", "2", "3"):
        raise ValueError(f"domain_num inválido: '{domain_num}'. Esperado '1', '2' ou '3'")
    if subtree_num not in ("1", "2", "3"):
        raise ValueError(f"subtree_num inválido: '{subtree_num}'. Esperado '1', '2' ou '3'")
    if cell_letter not in ("A", "B", "C"):
        raise ValueError(f"cell_letter inválido: '{cell_letter}'. Esperado 'A', 'B' ou 'C'")

    return f"{axis_code}.{pillar_code}.{domain_num}.{subtree_num}-{cell_letter}"


def generate_hierarchical_id(pillar: int,
                              domain: int, subtree: int,
                              cell: int) -> str:
    """Gera ID hierárquico no formato X.Y.Z.W.

    Onde:
      X = grupo de pilar (1-6, mapeado em PILLAR_NUM_TO_NAME)
      Y = domínio N2 (1-3)
      Z = subárvore N3 (1-3)
      W = célula N4 (1-3)

    Args:
        pillar: Número do pilar (1-6).
        domain: Número do domínio (1-3).
        subtree: Número da subárvore (1-3).
        cell: Número da célula (1-3).

    Returns:
        ID hierárquico no formato X.Y.Z.W.

    Raises:
        ValueError: Se qualquer argumento estiver fora do intervalo válido.

    Examples:
        >>> generate_hierarchical_id(1, 1, 1, 1)
        '1.1.1.1'
        >>> generate_hierarchical_id(4, 1, 1, 3)
        '4.1.1.3'
    """
    if not (1 <= pillar <= 6):
        raise ValueError(f"pillar deve estar em [1-6], recebido: {pillar}")
    if not (1 <= domain <= 3):
        raise ValueError(f"domain deve estar em [1-3], recebido: {domain}")
    if not (1 <= subtree <= 3):
        raise ValueError(f"subtree deve estar em [1-3], recebido: {subtree}")
    if not (1 <= cell <= 3):
        raise ValueError(f"cell deve estar em [1-3], recebido: {cell}")

    return f"{pillar}.{domain}.{subtree}.{cell}"

# ---------------------------------------------------------------------------
# Validação
# ---------------------------------------------------------------------------

def validate_uid(uid: str) -> bool:
    """Valida formato do UID permanente.

    Formato esperado: N{nivel}_{NOME_NORMALIZADO}
    Onde NOME_NORMALIZADO contém apenas [A-Z0-9_].

    Args:
        uid: UID a ser validado.

    Returns:
        True se o UID é válido, False caso contrário.

    Examples:
        >>> validate_uid("N4_DECOMPOSICAO_BINARIA")
        True
        >>> validate_uid("N3_RESOLUCAO")
        True
        >>> validate_uid("invalido")
        False
    """
    if not isinstance(uid, str):
        return False
    return bool(re.match(r"^N\d+_[A-Z0-9_]+$", uid))

# ---------------------------------------------------------------------------
# Construção do mapeamento global
# ---------------------------------------------------------------------------

def build_id_mapping() -> list:
    """Constrói mapeamento completo entre os três sistemas de ID.

    Gera mapeamento para todas as 162 células N4, cobrindo:
      - UID permanente (ex: N4_ALGORITMIA_A)
      - Path estrutural (ex: S1.L1.1.1-A)
      - ID hierárquico (ex: 1.1.1.1)
      - ID legado (ex: R1.1.1-A)

    Returns:
        Lista de dicts, cada um com as 4 representações de ID e metadados.
    """
    mapping = []

    for pillar_num in range(1, 7):  # 1 a 6
        pillar_name = PILLAR_NUM_TO_NAME[pillar_num]
        domains = PILLAR_DOMAINS[pillar_name]
        axis = PILLAR_NUM_TO_AXIS[pillar_num]
        axis_code = AXIS_TO_PATH_CODE[axis]
        pillar_code = PILLAR_TO_PATH_CODE[pillar_name]

        for domain_num, domain_name in enumerate(domains, start=1):
            for subtree_num in range(1, 4):  # 3 subárvores por domínio
                for cell_num in range(1, 4):  # 3 células por subárvore
                    cell_letter = "ABC"[cell_num - 1]

                    hier_id = generate_hierarchical_id(
                        pillar=pillar_num,
                        domain=domain_num,
                        subtree=subtree_num,
                        cell=cell_num,
                    )

                    path_id = generate_path(
                        axis_code=axis_code,
                        pillar_code=pillar_code,
                        domain_num=str(domain_num),
                        subtree_num=str(subtree_num),
                        cell_letter=cell_letter,
                    )

                    legacy_prefix = {
                        1: "R", 2: "B", 3: "P",
                        4: "K", 5: "A", 6: "M",
                    }[pillar_num]
                    legacy_id = f"{legacy_prefix}{pillar_num}.{domain_num}.{subtree_num}-{cell_letter}"

                    # Gerar UID único incluindo subárvore para evitar colisões
                    # Formato: N4_{DOMAIN}_{SUBTREE_NUM}_{CELL_LETTER}
                    # Ex: N4_ALGORITMIA_1_A
                    subtree_names = {
                        1: "RESOLUCAO", 2: "OTIMIZACAO", 3: "VALIDACAO",
                    }
                    # Usar posição numérica da subárvore para garantir unicidade
                    uid = f"N4_{normalize_text(domain_name)}_{subtree_num}_{cell_letter}"

                    mapping.append({
                        "uid": uid,
                        "path": path_id,
                        "hierarchical_id": hier_id,
                        "legacy_id": legacy_id,
                        "axis": axis,
                        "pillar": pillar_name,
                        "domain": domain_name,
                        "subtree_num": subtree_num,
                        "cell_num": cell_num,
                    })

    return mapping


# Construir mapeamento global no carregamento do módulo
ID_MAPPING = build_id_mapping()

# Índices de busca rápida
_BY_UID: dict[str, dict] = {m["uid"]: m for m in ID_MAPPING}
_BY_PATH: dict[str, dict] = {m["path"]: m for m in ID_MAPPING}
_BY_HIER: dict[str, dict] = {m["hierarchical_id"]: m for m in ID_MAPPING}
_BY_LEGACY: dict[str, dict] = {m["legacy_id"]: m for m in ID_MAPPING}


def lookup_by_uid(uid: str) -> dict | None:
    """Busca mapeamento por UID permanente."""
    return _BY_UID.get(uid)


def lookup_by_path(path: str) -> dict | None:
    """Busca mapeamento por path estrutural."""
    return _BY_PATH.get(path)


def lookup_by_hierarchical(hier_id: str) -> dict | None:
    """Busca mapeamento por ID hierárquico."""
    return _BY_HIER.get(hier_id)


def lookup_by_legacy(legacy_id: str) -> dict | None:
    """Busca mapeamento por ID legado."""
    return _BY_LEGACY.get(legacy_id)


def resolve_id(from_id: str, from_format: str = "legacy",
                to_format: str = "uid") -> str:
    """Converte entre formatos de ID.

    Args:
        from_id: O ID de origem.
        from_format: Formato de origem ('legacy', 'uid', 'path', 'hierarchical').
        to_format: Formato de destino ('legacy', 'uid', 'path', 'hierarchical').

    Returns:
        ID convertido no formato desejado.

    Raises:
        ValueError: Se formato for desconhecido.
        KeyError: Se ID não encontrado no mapeamento.

    Examples:
        >>> resolve_id("R1.1.1-A", from_format="legacy", to_format="uid")
        'N4_ALGORITMIA_A'
        >>> resolve_id("R1.1.1-A", from_format="legacy", to_format="path")
        'S1.L1.1.1-A'
    """
    lookup_map = {
        "legacy": _BY_LEGACY,
        "uid": _BY_UID,
        "path": _BY_PATH,
        "hierarchical": _BY_HIER,
    }
    if from_format not in lookup_map:
        raise ValueError(f"from_format desconhecido: '{from_format}'")
    if to_format not in lookup_map:
        raise ValueError(f"to_format desconhecido: '{to_format}'")

    entry = lookup_map[from_format].get(from_id)
    if entry is None:
        raise KeyError(f"ID '{from_id}' (formato: {from_format}) não encontrado no mapeamento")
    return entry[to_format]
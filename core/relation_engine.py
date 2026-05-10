#!/usr/bin/env python3
"""Motor de construção e validação de relações tipadas entre células N4.

Fornece funções para:
- Construir relações a partir de dados hierárquicos, semânticos e declarados
- Validar integridade das relações (tipos, pesos, ciclos, alvos)
- Inferir relações reversas automaticamente
"""

from __future__ import annotations

from typing import Optional

# ---------------------------------------------------------------------------
# Vocabulário controlado de tipos de relação
# ---------------------------------------------------------------------------

VALID_RELATION_TYPES: dict[str, float] = {
    "depende_de":  1.0,
    "complementa":  0.8,
    "contrasta":   -0.7,
    "expande":      0.6,
    "implementa":   0.9,
    "generaliza":   0.7,
    "especializa":  0.8,
    "causa":        0.5,
    "equilibra":   -0.5,
    "transforma":   0.4,
}

REVERSE_RELATIONS: dict[str, str] = {
    "depende_de":      "é_requisito_de",
    "generaliza":      "especializa",
    "especializa":     "generaliza",
    "complementa":     "complementa",   # simétrica
    "contrasta":       "contrasta",     # simétrica
    "causa":           "é_causado_por",
    "transforma":      "é_transformado_em",
    "expande":         "é_expandido_por",
    "implementa":      "é_implementado_por",
    "equilibra":       "equilibra",     # simétrica
}

# Relações implícitas por proximidade hierárquica (mesma subárvore)
HIERARCHICAL_RELATION = "complementa"
HIERARCHICAL_WEIGHT = 0.6

# Mapeamento de prefixo legado → nome do pilar
LEGACY_PREFIX_TO_PILLAR: dict[str, str] = {
    "R": "LOGOS",
    "B": "BIOS",
    "P": "PATHOS",
    "K": "KHAOS",
    "A": "APEIRON",
    "M": "MYTHOS",
}

# Domínios por pilar — usado para detectar relações cross-domain
PILLAR_DOMAINS: dict[str, list[str]] = {
    "LOGOS":   ["ALGORITMIA", "NOMOS",     "MECÂNICA"],
    "BIOS":    ["OIKOS",      "SOMA",      "METABOLISMO"],
    "PATHOS":  ["ETHOS",      "ALTERIDADE","ESTÉTICA"],
    "KHAOS":   ["ENTROPIA",   "SINGULARIDADE", "SÍNTESE"],
    "APEIRON": ["ESCALA",     "VIBRATIO",  "VÁCUO"],
    "MYTHOS":  ["ARQUÉTIPO",  "NARRATIVA", "MISTÉRIO"],
}

# Subárvores por domínio (ordem fixa)
DOMAIN_SUBTREES: dict[str, list[str]] = {
    "ALGORITMIA":   ["RESOLUÇÃO", "OTIMIZAÇÃO", "VALIDAÇÃO"],
    "NOMOS":        ["LEGISLAÇÃO", "CONTORNO", "PACTO"],
    "MECÂNICA":     ["ESTATICA", "DINAMICA", "TERMOTRANSDINÂMICA"],
    "OIKOS":        ["MORADA", "TERRITORIO", "PROVISAO"],
    "SOMA":         ["INTEGRIDADE", "VITALIDADE", "HOMEOSTASE"],
    "METABOLISMO":  ["ANABOLISMO", "CATABOLISMO", "CICLO"],
    "ETHOS":        ["VALORES", "VIRTUDE", "RESPONSABILIDADE"],
    "ALTERIDADE":   ["RECONHECIMENTO", "EMPATIA", "DIALOGO"],
    "ESTÉTICA":     ["HARMONIA", "EXPRESSAO", "IMPACTO"],
    "ENTROPIA":     ["DEGRADAÇÃO", "DISSIPAÇÃO", "CAOS"],
    "SINGULARIDADE": ["EXCEPCAO", "INFINITO", "TRANSFORMAÇÃO"],
    "SÍNTESE":      ["FUSÃO", "HIBRIDISMO", "TRANSCENDENCIA"],
    "ESCALA":       ["PROPORÇÃO", "MAGNITUDE", "LEI"],
    "VIBRATIO":     ["FREQUENCIA", "RESONÂNCIA", "ONDA"],
    "VÁCUO":        ["POTENCIAL", "SILÊNCIO", "CAMPO"],
    "ARQUÉTIPO":    ["PADRAO_PRIMORDIAL", "COMPORTAMENTO", "SÍMBOLO"],
    "NARRATIVA":    ["TEIA", "LINHA_SENTIDO", "HISTÓRIA_VIVIDA"],
    "MISTÉRIO":     ["INCOMPREENSÃO", "INTUIÇÃO", "REVELAÇÃO"],
}

# ---------------------------------------------------------------------------
# Mapeamento de letras de célula para números
# ---------------------------------------------------------------------------

CELL_LETTER_TO_NUM: dict[str, int] = {"A": 1, "B": 2, "C": 3}
CELL_NUM_TO_LETTER: dict[int, str] = {1: "A", 2: "B", 3: "C"}


def _parse_legacy_id(legacy_id: str) -> Optional[dict]:
    """Parseia ID legado (ex: R1.1.1-A) em componentes.

    Returns dict com pillar_num, domain_num, subtree_num, cell_letter
    ou None se formato inválido.
    """
    import re
    match = re.match(r"^([RBPKAM])(\d+)\.(\d+)\.(\d+)-([A-C])$", legacy_id)
    if not match:
        return None
    prefix, domain_num, subtree_num, cell_num, cell_letter = match.groups()
    # Mapear prefixo → número do pilar diretamente
    _PREFIX_TO_NUM = {"R": 1, "B": 2, "P": 3, "K": 4, "A": 5, "M": 6}
    pillar_num = _PREFIX_TO_NUM.get(prefix)
    if pillar_num is None:
        return None
    return {
        "pillar_num": pillar_num,
        "domain_num": int(domain_num),
        "subtree_num": int(subtree_num),
        "cell_num": int(cell_num),
        "cell_letter": cell_letter,
    }


def _get_sibling_cells(legacy_id: str, registry: dict) -> list[str]:
    """Retorna UIDs das células irmãs (mesma subárvore N3, letras diferentes)."""
    parsed = _parse_legacy_id(legacy_id)
    if not parsed:
        return []
    siblings = []
    for letter in "ABC":
        if letter == parsed["cell_letter"]:
            continue
        sib_legacy = f"{legacy_id[0]}{parsed['domain_num']}.{parsed['subtree_num']}.{parsed['cell_num']}-{letter}"
        # Buscar no registry por legacy_id
        for uid, data in registry.items():
            if data.get("legacy_id") == sib_legacy:
                siblings.append(uid)
                break
    return siblings


def _get_subtree_cells(subtree_key: str, registry: dict) -> list[str]:
    """Retorna UIDs de todas as células na mesma subárvore N3."""
    cells = []
    for uid, data in registry.items():
        if data.get("n3_ref") == subtree_key:
            cells.append(uid)
    return cells


def _infer_opposite_relations(registry: dict) -> dict[str, list[str]]:
    """Inferir pares de células opostas por semântica de domínio.

    Regras:
    - Processo ↔ Estado (criação vs manutenção)
    - Degradação ↔ Síntese (destruição vs construção)
    - Entropia ↔ Negociação (desordem vs ordem)
    - Exceção ↔ Regra (ruptura vs norma)
    """
    opposites: dict[str, list[str]] = {}

    # Mapeamento de nomes que indicam oposição semântica
    opposition_pairs = [
        # (padrão nome A, padrão nome B, justificativa)
        ("DECOMPOSIÇÃO", "SÍNTESE", "decompor vs unir"),
        ("COMPLEXIDADE_CAÓTICA", "SÍNTESE", "caos vs ordem"),
        ("ENTROPIA_SISTEMA", "NEGOCIAÇÃO", "desordem vs ordem"),
        ("DEGRADAÇÃO", "SÍNTESE", "degradar vs construir"),
        ("DISSIPAÇÃO", "CICLO", "dispersar vs circular"),
        ("ALEATORIEDADE", "PADRÕES_EMERGENTES", "acaso vs padrão"),
        ("PONTO_EXCEPCIONAL", "CODIFICAÇÃO_NORMA", "exceção vs regra"),
        ("MUDANÇA_RADICAL", "ESTABILIZAÇÃO", "mudança vs estabilidade"),
        ("COMPLEXIFICAÇÃO", "DECOMPOSIÇÃO", "complexificar vs simplificar"),
        ("EXPANSÃO_CONTÍNUA", "REGULAÇÃO_INTERNA", "expansão vs controle"),
    ]

    uid_by_nome: dict[str, str] = {}
    for uid, data in registry.items():
        nome = data.get("nome", "").upper()
        uid_by_nome[nome] = uid

    for nome_a, nome_b, _ in opposition_pairs:
        uid_a = uid_by_nome.get(nome_a)
        uid_b = uid_by_nome.get(nome_b)
        if uid_a and uid_b:
            opposites.setdefault(uid_a, []).append(uid_b)
            opposites.setdefault(uid_b, []).append(uid_a)

    return opposites


def build_relations(cell_id: str, cell_data: dict,
                    registry: dict) -> list[dict]:
    """Constrói relações tipadas para uma célula.

    Fontes de relação:
    1. Relações declaradas (campo 'relacoes' no registry, se existir)
    2. Proximidade hierárquica (mesma subárvore N3 → complementa)
    3. Inferência semântica (opostos → contrasta)
    4. Relações cross-domain dentro do mesmo pilar (generaliza/especializa)
    5. Dependência funcional (domínios anteriores → depende_de)

    Args:
        cell_id: UID da célula (ex: N4_ALGORITMIA_A)
        cell_data: Dados da célula do registry
        registry: Dicionário global de todas as células

    Returns:
        Lista de dicts: [{"tipo": str, "alvo": str, "peso": float}]
    """
    relations: list[dict] = []
    seen_targets: set[str] = set()

    n3_ref = cell_data.get("n3_ref", "")
    dominio = cell_data.get("dominio", "")
    pilar = cell_data.get("pilar", "")
    uid = cell_data.get("uid", cell_id)

    # ------------------------------------------------------------------
    # 1. Relações hierárquicas (mesma subárvore N3)
    # ------------------------------------------------------------------
    subtree_cells = _get_subtree_cells(n3_ref, registry)
    for sib_uid in subtree_cells:
        if sib_uid == uid or sib_uid in seen_targets:
            continue
        relations.append({
            "tipo": HIERARCHICAL_RELATION,
            "alvo": sib_uid,
            "peso": HIERARCHICAL_WEIGHT,
        })
        seen_targets.add(sib_uid)

    # ------------------------------------------------------------------
    # 2. Relações cross-domain dentro do mesmo pilar
    #    (domínios anteriores são pré-requisito dos posteriores)
    # ------------------------------------------------------------------
    pillar_domains = PILLAR_DOMAINS.get(pilar, [])
    try:
        dom_idx = pillar_domains.index(dominio)
    except ValueError:
        dom_idx = -1

    if dom_idx > 0:
        prev_domain = pillar_domains[dom_idx - 1]
        # Buscar células do domínio anterior na mesma subárvore posição
        for other_uid, other_data in registry.items():
            if (other_data.get("dominio") == prev_domain and
                    other_data.get("pilar") == pilar and
                    other_uid not in seen_targets):
                relations.append({
                    "tipo": "depende_de",
                    "alvo": other_uid,
                    "peso": 0.7,
                })
                seen_targets.add(other_uid)

    # ------------------------------------------------------------------
    # 3. Relações de generalização entre domínios do mesmo pilar
    #    Domínios "mais abstratos" generalizam os "mais concretos"
    # ------------------------------------------------------------------
    if dom_idx >= 0 and len(pillar_domains) > 1:
        # Primeiro domínio generaliza os demais
        if dom_idx > 0:
            first_domain = pillar_domains[0]
            for other_uid, other_data in registry.items():
                if (other_data.get("dominio") == first_domain and
                        other_data.get("pilar") == pilar and
                        other_uid not in seen_targets):
                    relations.append({
                        "tipo": "generaliza",
                        "alvo": other_uid,
                        "peso": 0.5,
                    })
                    seen_targets.add(other_uid)

    # ------------------------------------------------------------------
    # 4. Relações de inferência semântica (opostos → contrasta)
    # ------------------------------------------------------------------
    opposites_map = _infer_opposite_relations(registry)
    for opp_uid in opposites_map.get(uid, []):
        if opp_uid not in seen_targets:
            relations.append({
                "tipo": "contrasta",
                "alvo": opp_uid,
                "peso": -0.6,
            })
            seen_targets.add(opp_uid)

    # ------------------------------------------------------------------
    # 5. Relação de implementação entre N3 e suas N4
    #    (a subárvore N3 "implementa" suas células concretas,
    #     mas apenas para referência — peso menor)
    # ------------------------------------------------------------------
    # Não aplicável diretamente pois N3 não está no registry de N4

    return relations


def validate_relations(relations: list[dict], registry: dict) -> list[dict]:
    """Valida lista de relações:
    - Alvos existem no registry
    - Pesos em [-1.0, 1.0]
    - Tipos no vocabulário controlado
    - Sem auto-referência
    - Sem duplicatas

    Args:
        relations: Lista de relações a validar.
        registry: Dicionário global de células.

    Returns:
        Lista de relações válidas (inválidas são filtradas).
    """
    valid_types = set(VALID_RELATION_TYPES.keys())
    valid: list[dict] = []
    seen_pairs: set[tuple[str, str]] = set()

    for rel in relations:
        tipo = rel.get("tipo", "")
        alvo = rel.get("alvo", "")
        peso = rel.get("peso", 0.0)

        # Verificar tipo válido
        if tipo not in valid_types:
            continue

        # Verificar alvo existe no registry
        if alvo not in registry:
            continue

        # Verificar peso em range válido
        if not (-1.0 <= peso <= 1.0):
            continue

        # Verificar auto-referência
        if alvo == rel.get("source"):
            continue

        # Verificar duplicatas (mesmo tipo + mesmo alvo)
        pair_key = (tipo, alvo)
        if pair_key in seen_pairs:
            continue
        seen_pairs.add(pair_key)

        valid.append(rel)

    return valid


def infer_reverse_relations(relations: list[dict]) -> list[dict]:
    """Inferir relações reversas automaticamente.

    Para cada relação, gera a relação inversa com peso equivalente
    (usando o mapeamento REVERSE_RELATIONS).

    Args:
        relations: Lista de relações originais.

    Returns:
        Lista de relações reversas.
    """
    reverse: list[dict] = []

    for rel in relations:
        tipo = rel.get("tipo", "")
        alvo = rel.get("alvo", "")
        peso = rel.get("peso", 0.0)
        source = rel.get("source", "")

        inverse_type = REVERSE_RELATIONS.get(tipo)
        if inverse_type is None:
            continue

        # Para relações simétricas, não duplicar
        if inverse_type == tipo:
            continue

        reverse.append({
            "tipo": inverse_type,
            "alvo": source,
            "peso": peso,
            "source": alvo,
        })

    return reverse


def build_all_relations(registry: dict) -> dict[str, list[dict]]:
    """Constrói e valida relações para todas as células do registry.

    Args:
        registry: Dicionário global {uid: cell_data}.

    Returns:
        Dict mapeando cada UID para sua lista de relações válidas.
    """
    all_relations: dict[str, list[dict]] = {}

    for uid, cell_data in registry.items():
        raw_relations = build_relations(uid, cell_data, registry)

        # Adicionar source a cada relação para rastreabilidade
        for rel in raw_relations:
            rel["source"] = uid

        validated = validate_relations(raw_relations, registry)

        # Inferir reversas
        reverses = infer_reverse_relations(validated)

        # Combinar diretas e reversas, removendo duplicatas
        combined = validated + reverses
        seen = set()
        unique: list[dict] = []
        for rel in combined:
            key = (rel["tipo"], rel["alvo"])
            if key not in seen:
                seen.add(key)
                unique.append(rel)

        all_relations[uid] = unique

    return all_relations
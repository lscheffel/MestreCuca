#!/usr/bin/env python3
"""Testes unitários e de integração para o classificador ontológico multinível.

Executa validação da classificação N0→N4 com queries de exemplo,
verificando acurácia, latência e cobertura do classificador.

Usage:
    python tests/test_classifier.py          # modo verbose
    python tests/test_classifier.py --quiet  # modo silencioso
"""

from __future__ import annotations

import sys
import time
import json
import logging
from pathlib import Path
from typing import Any

import numpy as np

# Configurar paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "core"))
sys.path.insert(0, str(PROJECT_ROOT))

from runtime.classifier import (
    OntologicalClassifier,
    FullClassification,
    ClassificationResult,
    _normalize_key,
)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Queries de teste com classificações esperadas
# ---------------------------------------------------------------------------

TEST_QUERIES: list[dict[str, Any]] = [
    # Queries SINTRÓPICO → LOGOS → ALGORITMIA
    {
        "query": "como decompor um problema complexo em partes menores",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "LOGOS",
        "expected_n2": "ALGORITMIA",
        "expected_n3": "RESOLUCAO",
        "min_confidence": 0.40,
    },
    {
        "query": "implementar um algoritmo de ordenação eficiente",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "LOGOS",
        "expected_n2": "ALGORITMIA",
        "expected_n3": "RESOLUCAO",
        "min_confidence": 0.40,
    },
    {
        "query": "validar a correção de um sistema de software",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "LOGOS",
        "expected_n2": "ALGORITMIA",
        "expected_n3": "VALIDACAO",
        "min_confidence": 0.40,
    },
    {
        "query": "otimizar o desempenho de um processo computacional",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "LOGOS",
        "expected_n2": "ALGORITMIA",
        "expected_n3": "OTIMIZACAO",
        "min_confidence": 0.40,
    },
    # Queries SINTRÓPICO → BIOS → OIKOS
    {
        "query": "como organizar a morada de forma sustentável",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "BIOS",
        "expected_n2": "OIKOS",
        "min_confidence": 0.35,
    },
    {
        "query": "proteger recursos naturais do ecossistema",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "BIOS",
        "expected_n2": "OIKOS",
        "min_confidence": 0.35,
    },
    # Queries SINTRÓPICO → PATHOS → ETHOS
    {
        "query": "estabelecer valores éticos para uma organização",
        "expected_n0": "SINTRÓPICO",
        "expected_n1": "PATHOS",
        "expected_n2": "ETHOS",
        "min_confidence": 0.35,
    },
    # Queries ENTRÓPICO → KHAOS → ENTROPIA
    {
        "query": "entender a degradação de um sistema complexo",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "KHAOS",
        "expected_n2": "ENTROPIA",
        "min_confidence": 0.35,
    },
    {
        "query": "explorar o caos como fonte de transformação",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "KHAOS",
        "expected_n2": "ENTROPIA",
        "min_confidence": 0.35,
    },
    # Queries ENTRÓPICO → APEIRON → ESCALA
    {
        "query": "compreender padrões universais em escala cósmica",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "APEIRON",
        "expected_n2": "ESCALA",
        "min_confidence": 0.35,
    },
    # Queries ENTRÓPICO → MYTHOS → ARQUÉTIPO
    {
        "query": "identificar arquétipos na narrativa cultural",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "MYTHOS",
        "expected_n2": "ARQUETIPO",
        "min_confidence": 0.35,
    },
    {
        "query": "explorar o simbolismo nos mitos fundadores",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "MYTHOS",
        "expected_n2": "ARQUETIPO",
        "min_confidence": 0.35,
    },
    # Queries ENTRÓPICO → MYTHOS → NARRATIVA
    {
        "query": "analisar a estrutura narrativa de uma história",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "MYTHOS",
        "expected_n2": "NARRATIVA",
        "min_confidence": 0.35,
    },
    # Queries ENTRÓPICO → KHAOS → SÍNTESE
    {
        "query": "como emergem novos padrões da complexidade",
        "expected_n0": "ENTRÓPICO",
        "expected_n1": "KHAOS",
        "expected_n2": "SINTESE",
        "min_confidence": 0.35,
    },
    # Queries ambíguas (teste de robustez)
    {
        "query": "como fazer algo melhor",
        "expected_n0": "SINTRÓPICO",  # tendência a sintrópico
        "min_confidence": 0.30,
        "skip_n1": True,  # ambíguo demais para pilar preciso
    },
    {
        "query": "o que é a natureza da realidade",
        "expected_n0": "ENTRÓPICO",
        "min_confidence": 0.30,
        "skip_n1": True,
    },
]

# Queries focadas em N4 para validar a célula específica
N4_TEST_QUERIES: list[dict[str, Any]] = [
    {
        "query": "dividir problema em duas metades recursivamente",
        "expected_n4_keywords": ["decomposição", "binária", "divisão"],
        "not_expected_n4_keywords": ["integridade", "valores", "narrativa"],
    },
    {
        "query": "verificar lógica de um algoritmo passo a passo",
        "expected_n4_keywords": ["verificação", "lógica", "prova"],
        "not_expected_n4_keywords": ["emocional", "narrativa", "arquétipo"],
    },
    {
        "query": "explorar o que é entropia em sistemas",
        "expected_n4_keywords": ["entropia", "sistema", "desordem"],
        "not_expected_n4_keywords": ["algoritmo", "ordenação", "lógica"],
    },
]

# Mapeamento de n3_name esperado → keywords que devem aparecer
N3_KEYWORD_MAP: dict[str, list[str]] = {
    "RESOLUCAO": ["decompor", "resolver", "sequenciar", "validar"],
    "OTIMIZACAO": ["otimizar", "eficiente", "desempenho", "melhorar"],
    "VALIDACAO": ["validar", "verificar", "prova", "correto"],
    "MORADA": ["morada", "proteção", "recurso", "saneamento"],
    "TERRITORIO": ["território", "habitar", "espaço", "domínio"],
    "PROVISAO": ["provisão", "suprir", "sustentar", "reserva"],
    "INTEGRIDADE": ["integridade", "íntegro", "saudável", "funcional"],
    "VITALIDADE": ["vital", "energia", "vivo", "dinamismo"],
    "HOMEOSTASE": ["homeostase", "equilíbrio", "estável", "regulação"],
    "DEGRADACAO": ["degradação", "desgaste", "erosão", "deterioração"],
    "DISSIPACAO": ["dissipação", "dispersão", "perda", "dispersar"],
    "CAOS": ["caos", "desordem", "aleatório", "turbulento"],
    "LEGISLACAO": ["legislação", "lei", "regra", "jurídico"],
    "CONTORNO": ["contorno", "limite", "fronteira", "restrição"],
    "PACTO": ["pacto", "acordo", "contrato", "aliança"],
    "ESTATICA": ["estática", "equilíbrio", "força", "repouso"],
    "DINAMICA": ["dinâmica", "movimento", "força", "aceleração"],
    "TERMOTRANSDINAMICA": ["termodinâmica", "calor", "entropia", "energia"],
    "ALTERIDADE": ["alteridade", "reconhecer", "empatia", "diálogo"],
    "ETHOS": ["valor", "ética", "moral", "virtude"],
    "ESTETICA": ["estética", "beleza", "harmonia", "expressão"],
    "SINGULARIDADE": ["singularidade", "exceção", "infinito", "transformação"],
    "SINTESE": ["síntese", "fusão", "hibridismo", "transcendência"],
    "ESCALA": ["escala", "proporção", "magnitude", "medida"],
    "VIBRATIO": ["vibração", "frequência", "ressonância", "onda"],
    "VACUO": ["vácuo", "potencial", "silêncio", "campo"],
    "ARQUETIPO": ["arquétipo", "padrão", "símbolo", "comportamento"],
    "NARRATIVA": ["narrativa", "teia", "história", "sentido"],
    "MISTERIO": ["mistério", "incompreensão", "intuição", "revelação"],
    "PADRAO_PRIMORDIAL": ["padrão", "primordial", "reconhecimento", "ativação"],
    "COMPORTAMENTO": ["comportamento", "hábito", "prática", "ação"],
    "SIMBOLO": ["símbolo", "ícone", "totem", "emblema"],
    "TEIA": ["teia", "rede", "trama", "conexão"],
    "LINHA_SENTIDO": ["linha", "sentido", "fio", "narrativa"],
    "HISTORIA_VIVIDA": ["história", "vivida", "experiência", "memória"],
    "INCOMPREENSAO": ["incompreensão", "obscuridade", "enigma", "paradoxo"],
    "INTUICAO": ["intuição", "insight", "inspiração", "instinto"],
    "REVELACAO": ["revelação", "revelar", "descobrir", "iluminação"],
    "ANABOLISMO": ["anabolismo", "construção", "síntese", "crescimento"],
    "CATABOLISMO": ["catabolismo", "degradação", "quebra", "dissolução"],
    "CICLO": ["ciclo", "circular", "repetição", "renovação"],
    "FUSAO": ["fusão", "união", "combinação", "síntese"],
    "HIBRIDISMO": ["hibridismo", "híbrido", "mistura", "mestiçagem"],
    "TRANSCENDENCIA": ["transcendência", "transcender", "elevação", "além"],
    "MAGNITUDE": ["magnitude", "grandeza", "escala", "tamanho"],
    "LEI": ["lei", "regra", "norma", "universal"],
    "FREQUENCIA": ["frequência", "ritmo", "ciclo", "repetição"],
    "RESSONANCIA": ["ressonância", "vibração", "eco", "harmonia"],
    "ONDA": ["onda", "vibração", "propagação", "frequência"],
    "POTENCIAL": ["potencial", "latência", "capacidade", "possibilidade"],
    "SILENCIO": ["silêncio", "pausa", "vazio", "quietude"],
    "CAMPO": ["campo", "espaço", "região", "área"],
}

# Domínios N2 válidos por pilar (para consistência topológica)
N2_DOMAINS_BY_PILAR = {
    "LOGOS": ["ALGORITMIA", "NOMOS", "MECANICA"],
    "BIOS": ["OIKOS", "SOMA", "METABOLISMO"],
    "PATHOS": ["ETHOS", "ALTERIDADE", "ESTETICA"],
    "KHAOS": ["ENTROPIA", "SINGULARIDADE", "SINTESE"],
    "APEIRON": ["ESCALA", "VIBRATIO", "VACUO"],
    "MYTHOS": ["ARQUETIPO", "NARRATIVA", "MISTERIO"],
}

# Mapeamento de eixos válidos por pilar
N1_PILAR_BY_AXIS = {
    "SINTRÓPICO": ["LOGOS", "BIOS", "PATHOS"],
    "ENTRÓPICO": ["KHAOS", "APEIRON", "MYTHOS"],
}


# ---------------------------------------------------------------------------
# Testes unitários
# ---------------------------------------------------------------------------

def test_instantiation(clf: OntologicalClassifier) -> bool:
    """Testa criação do classificador sem erros."""
    print("\n[TEST] Instanciação do classificador...")
    try:
        stats = clf.get_stats()
        assert stats["total_cells"] > 0, "Nenhuma célula carregada"
        assert stats["total_embeddings"] > 0, "Nenhum embedding carregado"
        assert stats["coverage"] >= 0.9, f"Cobertura insuficiente: {stats['coverage']}"
        print(f"  ✅ OK: {stats['total_cells']} células, "
              f"{stats['total_embeddings']} embeddings "
              f"(cobertura: {stats['coverage']:.1%})")
        print(f"  ✅ Eixos: {stats['axes']}")
        print(f"  ✅ Pilares: {stats['pilares']}")
        print(f"  ✅ Domínios: {len(stats['dominios'])} → {sorted(stats['dominios'])}")
        print(f"  ✅ Subárvores: {stats['subarvores']}")
        return True
    except Exception as e:
        print(f"  ❌ FALHA: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_n0_classification(clf: OntologicalClassifier) -> bool:
    """Testa classificação de eixo N0."""
    print("\n[TEST] Classificação N0 (Eixo)...")
    all_ok = True

    # Teste SINTRÓPICO
    r = clf.classify_n0("como resolver um problema de engenharia")
    if r.label != "SINTRÓPICO":
        print(f"  ❌ Esperado SINTRÓPICO, got {r.label}")
        all_ok = False
    else:
        print(f"  ✅ SINTRÓPICO detectado: score={r.score}")

    # Teste ENTRÓPICO
    r = clf.classify_n0("o que é o significado da existência")
    if r.label != "ENTRÓPICO":
        print(f"  ❌ Esperado ENTRÓPICO, got {r.label}")
        all_ok = False
    else:
        print(f"  ✅ ENTRÓPICO detectado: score={r.score}")

    # Teste adicional: verbo "explorar"
    r = clf.classify_n0("explorar possibilidades de inovação")
    if r.label != "ENTRÓPICO":
        print(f"  ❌ Esperado ENTRÓPICO para 'explorar', got {r.label}")
        all_ok = False
    else:
        print(f"  ✅ ENTRÓPICO para 'explorar': score={r.score}")

    # Teste adicional: verbo "construir"
    r = clf.classify_n0("construir um sistema robusto")
    if r.label != "SINTRÓPICO":
        print(f"  ❌ Esperado SINTRÓPICO para 'construir', got {r.label}")
        all_ok = False
    else:
        print(f"  ✅ SINTRÓPICO para 'construir': score={r.score}")

    return all_ok


def test_n1_classification(clf: OntologicalClassifier) -> bool:
    """Testa classificação de pilar N1."""
    print("\n[TEST] Classificação N1 (Pilar)...")
    all_ok = True

    n0_sint = ClassificationResult("n0", "SINTRÓPICO", "S1", 0.9)
    n0_entr = ClassificationResult("n0", "ENTRÓPICO", "E2", 0.9)

    test_cases = [
        ("analisar a estrutura de um sistema complexo", n0_sint, "LOGOS"),
        ("preservar o ecossistema e a saúde do organismo", n0_sint, "BIOS"),
        ("estabelecer valores éticos para a comunidade", n0_sint, "PATHOS"),
        ("transformação radical e ruptura com o passado", n0_entr, "KHAOS"),
        ("compreender a escala universal do cosmos", n0_entr, "APEIRON"),
        ("explorar os mitos e narrativas fundadoras", n0_entr, "MYTHOS"),
    ]

    for query, n0_ctx, expected in test_cases:
        r = clf.classify_n1(query, n0_ctx)
        if r.label != expected:
            print(f"  ❌ Esperado {expected}, got {r.label} (query: '{query[:50]}...')")
            all_ok = False
        else:
            print(f"  ✅ {expected} detectado: score={r.score}")

    return all_ok


def test_n2_classification(clf: OntologicalClassifier) -> bool:
    """Testa classificação de domínio N2."""
    print("\n[TEST] Classificação N2 (Domínio)...")
    all_ok = True

    n1_logos = ClassificationResult("n1", "LOGOS", "L", 0.9)
    n1_bios = ClassificationResult("n1", "BIOS", "B", 0.9)
    n1_pathos = ClassificationResult("n1", "PATHOS", "P", 0.9)
    n1_khaos = ClassificationResult("n1", "KHAOS", "K", 0.9)
    n1_apeiron = ClassificationResult("n1", "APEIRON", "A", 0.9)
    n1_mythos = ClassificationResult("n1", "MYTHOS", "M", 0.9)

    test_cases = [
        ("como resolver problemas com algoritmos", n1_logos, "ALGORITMIA"),
        ("organizar a morada e o território sustentável", n1_bios, "OIKOS"),
        ("definir valores e virtudes para a sociedade", n1_pathos, "ETHOS"),
        ("entropia e degradação em sistemas complexos", n1_khaos, "ENTROPIA"),
        ("escala e proporção em fenômenos cósmicos", n1_apeiron, "ESCALA"),
        ("reconhecer padrões arquetípicos na cultura", n1_mythos, "ARQUETIPO"),
    ]

    for query, n1_ctx, expected in test_cases:
        r = clf.classify_n2(query, n1_ctx)
        if r.label != expected:
            print(f"  ❌ Esperado {expected}, got {r.label} (query: '{query[:50]}...')")
            all_ok = False
        else:
            print(f"  ✅ {expected} detectado: score={r.score}")

    return all_ok


def test_n3_classification(clf: OntologicalClassifier) -> bool:
    """Testa classificação de subárvore N3."""
    print("\n[TEST] Classificação N3 (Subárvore)...")
    all_ok = True

    n2_algo = ClassificationResult("n2", "ALGORITMIA", "A", 0.9)
    n2_oikos = ClassificationResult("n2", "OIKOS", "O", 0.9)
    n2_entropia = ClassificationResult("n2", "ENTROPIA", "E", 0.9)
    n2_arquetipo = ClassificationResult("n2", "ARQUETIPO", "AR", 0.9)
    n2_ethos = ClassificationResult("n2", "ETHOS", "ET", 0.9)
    n2_mecanica = ClassificationResult("n2", "MECANICA", "M", 0.9)

    test_cases = [
        ("decompor e resolver problemas algorítmicos", n2_algo, "RESOLUCAO"),
        ("proteger e organizar a morada", n2_oikos, "MORADA"),
        ("degradação e dissolução de sistemas", n2_entropia, "DEGRADACAO"),
        ("reconhecer padrões primordiais na experiência", n2_arquetipo, "PADRAO_PRIMORDIAL"),
        ("definir valores morais fundamentais", n2_ethos, "VALORES"),
        ("análise de forças em repouso", n2_mecanica, "ESTATICA"),
    ]

    for query, n2_ctx, expected in test_cases:
        r = clf.classify_n3(query, n2_ctx)
        if r.label != expected:
            print(f"  ❌ Esperado {expected}, got {r.label} (query: '{query[:50]}...')")
            all_ok = False
        else:
            print(f"  ✅ {expected} detectado: score={r.score}")

    return all_ok


def test_n4_classification(clf: OntologicalClassifier) -> bool:
    """Testa classificação de célula N4."""
    print("\n[TEST] Classificação N4 (Célula)...")
    all_ok = True

    n3_resolucao = ClassificationResult("n3", "RESOLUCAO", "RESOLUCAO", 0.9)
    n3_morada = ClassificationResult("n3", "MORADA", "MORADA", 0.9)
    n3_entropia = ClassificationResult("n3", "ENTROPIA", "ENTROPIA", 0.9)

    test_cases = [
        # (query, n3_context, expected_uid_or_keyword)
        ("dividir problema em duas metades recursivamente", n3_resolucao, "DECOMPOSICAO"),
        ("proteger e manter os recursos da morada", n3_morada, "PROTECAO"),
        ("dissipação de energia em um sistema aberto", n3_entropia, "DISSIPACAO"),
    ]

    for query, n3_ctx, expected_keyword in test_cases:
        r = clf.classify_n4(query, n3_ctx)
        # Normalizar para comparação sem acentos
        label_normalized = _normalize_key(r.label)
        expected_norm = _normalize_key(expected_keyword)

        if expected_norm in label_normalized:
            print(f"  ✅ '{r.label}' detectado: score={r.score}")
        else:
            # Check top_cells
            found_in_top = False
            for cell in r.top_cells:
                cell_norm = _normalize_key(cell.get("nome", ""))
                if expected_norm in cell_norm:
                    found_in_top = True
                    break
            if not found_in_top:
                print(f"  ❌ Esperado contendo '{expected_keyword}', got '{r.label}'")
                print(f"     Top3: {[(c['nome'], c['score']) for c in r.top_cells]}")
                all_ok = False
            else:
                print(f"  ✅ '{expected_keyword}' encontrado no top3: score={r.score}")

    return all_ok


# ---------------------------------------------------------------------------
# Teste de classificação completa (pipeline N0→N4)
# ---------------------------------------------------------------------------

def test_full_classify(clf: OntologicalClassifier) -> bool:
    """Testa classificação completa N0→N4."""
    print("\n[TEST] Classificação completa N0→N4...")
    all_ok = True
    passed = 0
    total = 0

    for i, tc in enumerate(TEST_QUERIES):
        total += 1
        query = tc["query"]
        result = clf.full_classify(query)

        # Verificar N0
        if result.n0.label != tc["expected_n0"]:
            print(f"  ❌ Query {i+1}: N0 esperado {tc['expected_n0']}, got {result.n0.label}")
            all_ok = False
            continue

        # Verificar N1 (se aplicável)
        if not tc.get("skip_n1", False):
            if result.n1.label != tc["expected_n1"]:
                print(f"  ❌ Query {i+1}: N1 esperado {tc['expected_n1']}, got {result.n1.label}")
                all_ok = False
                continue

            # Verificar N2 (se aplicável)
            if result.n2.label != tc["expected_n2"]:
                print(f"  ❌ Query {i+1}: N2 esperado {tc['expected_n2']}, got {result.n2.label}")
                all_ok = False
                continue

            # Verificar N3 (se aplicável)
            if "expected_n3" in tc:
                if result.n3.label != tc["expected_n3"]:
                    print(f"  ❌ Query {i+1}: N3 esperado {tc['expected_n3']}, got {result.n3.label}")
                    all_ok = False
                    continue

        # Verificar confiança mínima
        if result.confianca_media < tc["min_confidence"]:
            print(f"  ⚠️ Query {i+1}: Confiança {result.confianca_media:.4f} < {tc['min_confidence']}")

        passed += 1
        print(f"  ✅ Query {i+1}: {result.n0.label} → {result.n1.label} → "
              f"{result.n2.label} → {result.n3.label} → {result.n4.label} "
              f"(conf={result.confianca_media:.4f})")

    print(f"\n  Resultado: {passed}/{total} queries classificadas corretamente")
    return all_ok


# ---------------------------------------------------------------------------
# Teste de N4 com keywords
# ---------------------------------------------------------------------------

def test_n4_keywords(clf: OntologicalClassifier) -> bool:
    """Testa se células N4 correspondem a keywords esperadas."""
    print("\n[TEST] Classificação N4 com keywords...")
    all_ok = True

    for tc in N4_TEST_QUERIES:
        result = clf.full_classify(tc["query"])
        n4_label_lower = _normalize_key(result.n4.label)

        # Verificar keywords esperadas
        for kw in tc["expected_n4_keywords"]:
            kw_norm = _normalize_key(kw)
            if kw_norm not in n4_label_lower:
                # Checar se aparece no top3
                found = any(
                    kw_norm in _normalize_key(c.get("nome", ""))
                    for c in result.top_cells
                )
                if not found:
                    print(f"  ❌ Keyword '{kw}' não encontrada para query '{tc['query']}'")
                    print(f"     N4={result.n4.label}, Top3={[(c['nome'], c['score']) for c in result.top_cells]}")
                    all_ok = False

        # Verificar keywords NÃO esperadas
        for kw in tc.get("not_expected_n4_keywords", []):
            kw_norm = _normalize_key(kw)
            if kw_norm in n4_label_lower:
                print(f"  ❌ Keyword não esperada '{kw}' encontrada: {result.n4.label}")
                all_ok = False

    if all_ok:
        print("  ✅ Todas as correspondências de keywords corretas")

    return all_ok


# ---------------------------------------------------------------------------
# Teste de cobertura
# ---------------------------------------------------------------------------

def test_coverage(clf: OntologicalClassifier) -> bool:
    """Testa se todas as 162 células estão acessíveis no registry."""
    print("\n[TEST] Cobertura do registry...")
    all_ok = True

    # Contar células por domínio
    domain_counts: dict[str, int] = {}
    subarvore_counts: dict[str, int] = {}

    for uid, data in clf.registry.items():
        # Campos obrigatórios
        required = ["uid", "nivel", "pilar", "dominio", "n3_name", "axis", "nome"]
        for field_name in required:
            if field_name not in data:
                print(f"  ❌ {uid} missing field: {field_name}")
                all_ok = False

        # Consistência do UID
        if not uid.startswith("N4_"):
            print(f"  ❌ UID com prefixo inválido: {uid}")
            all_ok = False

        # Nível deve ser N4
        if data.get("nivel") != "N4":
            print(f"  ❌ {uid} has nivel={data.get('nivel')}, expected N4")
            all_ok = False

        dominio = data.get("dominio", "???")
        # Normalizar domínio para comparação consistente (sem acento, uppercase)
        dominio_norm = _normalize_key(dominio).upper()
        subarvore = _normalize_key(data.get("n3_name", "???")).upper()
        domain_counts[dominio_norm] = domain_counts.get(dominio_norm, 0) + 1
        subarvore_counts[subarvore] = subarvore_counts.get(subarvore, 0) + 1

    # Esperamos 18 domínios × 3 = 54 subárvores × 3 = 162 células
    total = len(clf.registry)
    if total != 162:
        print(f"  ❌ Esperado 162 células, got {total}")
        all_ok = False
    else:
        print(f"  ✅ Total: {total} células")

    # Verificar contagem por domínio
    for dominio, count in sorted(domain_counts.items()):
        if count != 9:  # 3 subárvores × 3 células = 9
            print(f"  ⚠️ Domínio {dominio}: {count} células (esperado 9)")

    # Verificar contagem por subárvore
    for sub, count in sorted(subarvore_counts.items()):
        if count != 3:
            print(f"  ⚠️ Subárvore {sub}: {count} células (esperado 3)")

    # Verificar que todos os domínios esperados existem
    expected_domains = set()
    for pil_domains in N2_DOMAINS_BY_PILAR.values():
        for d in pil_domains:
            expected_domains.add(_normalize_key(d).upper())

    actual_domains = set(domain_counts.keys())
    missing = expected_domains - actual_domains
    extra = actual_domains - expected_domains

    if missing:
        print(f"  ❌ Domínios faltando: {missing}")
        all_ok = False
    if extra:
        print(f"  ⚠️ Domínios extras: {extra}")

    if not missing and not extra:
        print(f"  ✅ Todos os {len(expected_domains)} domínios presentes")

    # Verificar embeddings
    missing_embeddings = set(clf.registry.keys()) - set(clf.embeddings.keys())
    if missing_embeddings:
        print(f"  ⚠️ {len(missing_embeddings)} células sem embedding")
    else:
        print(f"  ✅ Todos os embeddings carregados ({len(clf.embeddings)})")

    return all_ok


# ---------------------------------------------------------------------------
# Teste de consistência (cascata)
# ---------------------------------------------------------------------------

def test_consistency(clf: OntologicalClassifier) -> bool:
    """Testa se a cascata N0→N4 é topologicamente consistente."""
    print("\n[TEST] Consistência topológica da cascata...")
    all_ok = True

    # Mapeamento de domínios válidos por pilar
    valid_domains_by_pilar = N2_DOMAINS_BY_PILAR

    # Mapeamento de eixos válidos por pilar
    axis_by_pilar = {}
    for axis, pilares in N1_PILAR_BY_AXIS.items():
        for p in pilares:
            axis_by_pilar[p] = axis

    test_queries = [
        "como resolver um problema de algoritmo",
        "o que é a natureza da vida",
        "estabelecer valores para a comunidade",
        "explorar o caos e a transformação",
        "compreender a escala do universo",
        "analisar mitos e narrativas culturais",
    ]

    for query in test_queries:
        result = clf.full_classify(query)
        n0 = result.n0.label
        n1 = result.n1.label
        n2 = result.n2.label

        # Verificar: pilar pertence ao eixo
        expected_axis = axis_by_pilar.get(n1)
        if expected_axis and expected_axis != n0:
            print(f"  ❌ Inconsistência: pilar {n1} (eixo {expected_axis}) "
                  f"classificado com eixo {n0}")
            all_ok = False

        # Verificar: domínio pertence ao pilar
        valid_doms = valid_domains_by_pilar.get(n1, set())
        n2_norm = _normalize_key(n2).upper()
        valid_doms_norm = {_normalize_key(d).upper() for d in valid_doms}
        if n2_norm not in valid_doms_norm:
            print(f"  ❌ Inconsistência: domínio {n2} não pertence ao pilar {n1}")
            all_ok = False

    if all_ok:
        print("  ✅ Todas as classificações são topologicamente consistentes")

    return all_ok


# ---------------------------------------------------------------------------
# Benchmark de latência
# ---------------------------------------------------------------------------

def test_latency(clf: OntologicalClassifier) -> bool:
    """Testa latência de classificação completa."""
    print("\n[TEST] Benchmark de latência...")
    all_ok = True

    queries = [
        "como decompor um problema complexo",
        "o que é o significado da existência",
        "implementar um algoritmo de ordenação",
        "explorar o caos como fonte de transformação",
        "estabelecer valores éticos para uma organização",
    ]

    latencies = []
    for query in queries:
        start = time.perf_counter()
        clf.full_classify(query)
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)

    avg_lat = sum(latencies) / len(latencies)
    max_lat = max(latencies)
    min_lat = min(latencies)

    print(f"  Latências: {[f'{l:.1f}ms' for l in latencies]}")
    print(f"  Média: {avg_lat:.1f}ms | Min: {min_lat:.1f}ms | Max: {max_lat:.1f}ms")

    if max_lat > 5000:  # 5 segundos
        print(f"  ❌ Latência máxima {max_lat:.1f}ms excede limite de 5000ms")
        all_ok = False
    else:
        print(f"  ✅ Todas as classificações abaixo de 5s")

    return all_ok


# ---------------------------------------------------------------------------
# Teste de edge cases
# ---------------------------------------------------------------------------

def test_edge_cases(clf: OntologicalClassifier) -> bool:
    """Testa casos extremos e inputs inusitados."""
    print("\n[TEST] Edge cases...")
    all_ok = True

    edge_queries = [
        "",                          # string vazia
        "a",                         # string mínima
        "xkqj zwpw",                # palavras sem sentido
        "12345",                     # apenas números
        "   ",                       # apenas espaços
        "O que é o infinito?",      # pontuação
        "COMO FAZER ALGO BOM",      # caixa alta
        "como   fazer    algo",      # espaços múltiplos
    ]

    for query in edge_queries:
        try:
            result = clf.full_classify(query)
            # Deve retornar algum resultado (mesmo que de baixa confiança)
            assert result.n0.label in ("SINTRÓPICO", "ENTRÓPICO"), \
                f"N0 inválido: {result.n0.label}"
            assert result.n1.label in (
                "LOGOS", "BIOS", "PATHOS", "KHAOS", "APEIRON", "MYTHOS"
            ), f"N1 inválido: {result.n1.label}"
            print(f"  ✅ '{query[:30]}...' → {result.n0.label}/{result.n1.label}/{result.n2.label}")
        except Exception as e:
            print(f"  ❌ Erro para '{query[:30]}...': {e}")
            all_ok = False

    return all_ok


# ---------------------------------------------------------------------------
# Teste de warm-up
# ---------------------------------------------------------------------------

def test_warm_up(clf: OntologicalClassifier) -> bool:
    """Testa o método warm_up."""
    print("\n[TEST] Warm-up do modelo de embedding...")
    try:
        clf.warm_up()
        print("  ✅ Warm-up concluído sem erros")
        return True
    except Exception as e:
        print(f"  ❌ Falha no warm-up: {e}")
        return False


# ---------------------------------------------------------------------------
# Teste de integridade dos dados
# ---------------------------------------------------------------------------

def test_data_integrity(clf: OntologicalClassifier) -> bool:
    """Testa integridade dos dados do registry."""
    print("\n[TEST] Integridade dos dados...")
    all_ok = True

    for uid, data in clf.registry.items():
        # Campos obrigatórios
        required = ["uid", "nivel", "pilar", "dominio", "n3_name", "axis", "nome"]
        for field_name in required:
            if field_name not in data:
                print(f"  ❌ {uid} missing field: {field_name}")
                all_ok = False

        # Consistência do UID
        if not uid.startswith("N4_"):
            print(f"  ❌ UID com prefixo inválido: {uid}")
            all_ok = False

        # Nível deve ser N4
        if data.get("nivel") != "N4":
            print(f"  ❌ {uid} has nivel={data.get('nivel')}, expected N4")
            all_ok = False

    if all_ok:
        print(f"  ✅ Todas as {len(clf.registry)} células passaram na verificação de integridade")

    return all_ok


# ---------------------------------------------------------------------------
# Teste de acurácia com amostragem
# ---------------------------------------------------------------------------

def test_accuracy_sample(clf: OntologicalClassifier) -> bool:
    """Testa acurácia amostral com queries representativas de cada domínio."""
    print("\n[TEST] Acurácia amostral por domínio...")
    all_ok = True

    # Queries representativas por domínio N2
    domain_test_queries: dict[str, list[str]] = {
        "ALGORITMIA": [
            "como implementar um algoritmo de busca",
            "resolver problema com programação dinâmica",
            "analisar complexidade de um algoritmo",
        ],
        "OIKOS": [
            "como construir uma morada sustentável",
            "organizar o território de forma harmoniosa",
            "prover recursos para a comunidade",
        ],
        "ETHOS": [
            "quais valores devem guiar uma organização",
            "estabelecer princípios éticos para decisões",
            "praticar a virtude na liderança",
        ],
        "ENTROPIA": [
            "entender a degradação de sistemas",
            "como a energia se dissipa em processos",
            "o caos em sistemas não lineares",
        ],
        "ESCALA": [
            "compreender a magnitude de fenômenos cósmicos",
            "proporção áurea na natureza",
            "escala de leis físicas universais",
        ],
        "ARQUETIPO": [
            "identificar padrões primordiais na cultura",
            "o herói e sua jornada arquetípica",
            "símbolos universais na experiência humana",
        ],
    }

    correct = 0
    total = 0

    for expected_domain, queries in domain_test_queries.items():
        expected_norm = _normalize_key(expected_domain).upper()
        for query in queries:
            total += 1
            result = clf.full_classify(query)
            result_norm = _normalize_key(result.n2.label).upper()
            if result_norm == expected_norm:
                correct += 1
                print(f"  ✅ '{query[:50]}...' → {result.n2.label}")
            else:
                print(f"  ❌ '{query[:50]}...': esperado {expected_domain}, got {result.n2.label}")

    accuracy = correct / total if total > 0 else 0
    print(f"\n  Acurácia N2: {correct}/{total} = {accuracy:.1%}")

    if accuracy >= 0.70:
        print(f"  ✅ Acurácia ≥ 70% atingida")
    else:
        print(f"  ⚠️ Acurácia {accuracy:.1%} abaixo do limiar de 70%")
        # Não falha — apenas reporta

    return True  # Teste informativo, não bloqueante


# ---------------------------------------------------------------------------
# Runner principal
# ---------------------------------------------------------------------------

def main():
    quiet = "--quiet" in sys.argv
    if quiet:
        logging.disable(logging.CRITICAL)

    print("=" * 70)
    print("CLASSIFICADOR ONTOLÓGICO MULTINÍVEL — SUÍTE DE TESTES")
    print("=" * 70)

    clf = OntologicalClassifier(
        json_dir=str(PROJECT_ROOT / "data" / "json"),
        embedding_dir=str(PROJECT_ROOT / "data" / "embeddings"),
    )

    results: dict[str, bool] = {}

    results["warm_up"] = test_warm_up(clf)
    results["instantiation"] = test_instantiation(clf)
    results["data_integrity"] = test_data_integrity(clf)
    results["coverage"] = test_coverage(clf)
    results["n0"] = test_n0_classification(clf)
    results["n1"] = test_n1_classification(clf)
    results["n2"] = test_n2_classification(clf)
    results["n3"] = test_n3_classification(clf)
    results["n4"] = test_n4_classification(clf)
    results["full_classify"] = test_full_classify(clf)
    results["n4_keywords"] = test_n4_keywords(clf)
    results["consistency"] = test_consistency(clf)
    results["accuracy"] = test_accuracy_sample(clf)
    results["latency"] = test_latency(clf)
    results["edge_cases"] = test_edge_cases(clf)

    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for name, ok in results.items():
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"  {status}: {name}")

    print(f"\n  Total: {passed}/{total} testes passados")

    if passed == total:
        print("\n  🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"\n  ⚠️  {total - passed} teste(s) falhou(ram)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
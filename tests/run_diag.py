#!/usr/bin/env python3
"""Diagnostico completo - grava resultado em arquivo."""
import json, os, sys, unicodedata

os.chdir("e:/Arquivos/Área de Trabalho/MestreCuca")
sys.path.insert(0, '.')

from runtime.classifier import (
    OntologicalClassifier, _normalize_key,
    N0_AXIS_KEYWORDS, N2_DOMAINS_BY_PILAR, N3_SUBTREES_BY_DOMAIN,
    ClassificationResult
)

clf = OntologicalClassifier()
out = []
def p(s=""): out.append(s)

# 1. Sample registry
p("=== SAMPLE REGISTRY ===")
for i, (uid, data) in enumerate(clf.registry.items()):
    if i < 3:
        for k in ['uid','axis','eixo','pilar','dominio','n3_name','nome','nome_normalizado']:
            p(f"  {uid}: {k}={repr(data.get(k))}")
        p()

# 2. Index sizes
p("=== INDEX SIZES ===")
for name, idx in [("_uid_by_axis", clf._uid_by_axis), ("_uid_by_pilar", clf._uid_by_pilar),
                   ("_uid_by_dominio", clf._uid_by_dominio), ("_uid_by_subarvore", clf._uid_by_subarvore)]:
    p(f"{name}: {len(idx)} keys")
    for k, v in sorted(idx.items()):
        p(f"  {k}: {len(v)} items")
p()

# 3. Domain mismatch
p("=== DOMAIN KEY MISMATCH ===")
all_static = set()
for pil, doms in N2_DOMAINS_BY_PILAR.items():
    all_static.update(doms)
for dom in sorted(all_static):
    norm = _normalize_key(dom).upper()
    in_index = norm in clf._uid_by_dominio
    p(f"  {dom:15s} -> norm={norm:15s} in_index={in_index} count={len(clf._uid_by_dominio.get(norm,[]))}")
p()

# 4. Subtree mismatch
p("=== SUBTREE KEY MISMATCH ===")
for dom, subs in sorted(N3_SUBTREES_BY_DOMAIN.items()):
    for sub in subs:
        norm = _normalize_key(sub).upper()
        in_index = norm in clf._uid_by_subarvore
        p(f"  {sub:25s} -> norm={norm:25s} in_index={in_index}")
p()

# 5. n3_name values
p("=== ALL n3_name VALUES ===")
n3_vals = sorted(set(d.get("n3_name","") for d in clf.registry.values()))
for v in n3_vals:
    norm = _normalize_key(v).upper()
    in_idx = norm in clf._uid_by_subarvore
    p(f"  registry={v:30s} norm={norm:30s} in_index={in_idx}")
p()

# 6. N0 debug
p("=== N0 DEBUG ===")
for q in ["explorar o desconhecido", "o que e o significado da existencia", "como resolver um problema"]:
    r = clf.classify_n0(q)
    p(f"  '{q}' -> {r.label} score={r.score} candidates={r.candidates}")
p()

# 7. N2 debug
p("=== N2 DEBUG ===")
for query, pilar, expected_d in [
    ("como implementar um algoritmo de busca", "LOGOS", "ALGORITMIA"),
    ("organizar o territorio de forma harmoniosa", "BIOS", "OIKOS"),
    ("quais valores devem guiar uma organizacao", "PATHOS", "ETHOS"),
    ("entender a degradacao de sistemas", "KHAOS", "ENTROPIA"),
]:
    n1 = ClassificationResult("n1", pilar, pilar[:1], 0.9)
    r = clf.classify_n2(query, n1)
    p(f"  '{query[:50]}' pilar={pilar} -> {r.label} (expected {expected_d}) cand={r.candidates}")
p()

# 8. N4 debug
p("=== N4 DEBUG ===")
for sub_name in ["RESOLUCAO", "DEGRADACAO", "ENTROPIA", "MORADA", "PADRAO_PRIMORDIAL"]:
    n3 = ClassificationResult("n3", sub_name, sub_name, 0.9)
    r = clf.classify_n4("dividir problema em duas metades recursivamente", n3)
    p(f"  n3={sub_name}: label={r.label} score={r.score} top3={[(c['nome'],c['score']) for c in r.top_cells]}")
p()

# 9. Full classify failing
p("=== FULL CLASSIFY FAILING ===")
for q in [
    "o que e o significado da existencia",
    "como implementar um algoritmo de busca",
    "organizar o territorio de forma harmoniosa",
    "quais valores devem guiar uma organizacao",
    "entender a degradacao de sistemas",
    "reconhecer padroes primordiais na experiencia",
    "explorar o desconhecido",
    "o caos em sistemas nao lineares",
    "simbolos universais na experiencia humana",
]:
    r = clf.full_classify(q)
    p(f"  '{q[:60]}'")
    p(f"    -> {r.n0.label} -> {r.n1.label} -> {r.n2.label} -> {r.n3.label} -> {r.n4.label} conf={r.confianca_media:.4f}")

with open("tests/diagnostic_output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print("Diagnostic written to tests/diagnostic_output.txt")
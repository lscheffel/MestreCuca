#!/usr/bin/env python3
"""Diagnóstico rápido dos dados para ajustar o classificador."""
import json, os
from collections import Counter

json_dir = "data/json"
jsons = [f for f in os.listdir(json_dir) if f.startswith("N4_") and f.endswith(".json")]

dominios = Counter()
n3_names = Counter()
pilares = Counter()
axes = Counter()

for f in sorted(jsons):
    with open(os.path.join(json_dir, f)) as fp:
        d = json.load(fp)
        dominios[d.get("dominio", "???")] += 1
        n3_names[d.get("n3_name", "???")] += 1
        pilares[d.get("pilar", "???")] += 1
        axes[d.get("axis", "???")] += 1

print("=== DOMÍNIOS ===")
for k, v in sorted(dominios.items()):
    print(f"  {k}: {v}")

print("\n=== N3_NAMES ===")
for k, v in sorted(n3_names.items()):
    print(f"  {k}: {v}")

print("\n=== PILARES ===")
for k, v in sorted(pilares.items()):
    print(f"  {k}: {v}")

print("\n=== AXES ===")
for k, v in sorted(axes.items()):
    print(f"  {k}: {v}")

# Verificar campos funcao_cognitiva e tags
print("\n=== CAMPOS OPCIONAIS ===")
has_funcao = sum(1 for f in jsons if json.load(open(os.path.join(json_dir, f))).get("funcao_cognitiva"))
has_tags = sum(1 for f in jsons if json.load(open(os.path.join(json_dir, f))).get("tags"))
has_gatilho = sum(1 for f in jsons if json.load(open(os.path.join(json_dir, f))).get("gatilho"))
has_acao = sum(1 for f in jsons if json.load(open(os.path.join(json_dir, f))).get("acao"))
print(f"  funcao_cognitiva: {has_funcao}/{len(jsons)}")
print(f"  tags: {has_tags}/{len(jsons)}")
print(f"  gatilho: {has_gatilho}/{len(jsons)}")
print(f"  acao: {has_acao}/{len(jsons)}")
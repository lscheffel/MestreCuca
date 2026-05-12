#!/usr/bin/env python3
"""Reconstrói o ontology_index.json com os dados corretos dos 162 N4 JSONs."""
import json, os, sys
from pathlib import Path
from datetime import datetime, timezone

project_root = Path("e:/Arquivos/Área de Trabalho/MestreCuca")
json_dir = project_root / "data" / "json"
index_path = json_dir / "ontology_index.json"

# Carregar todos os N4 JSONs
cells = []
id_mapping = {}
natureza_count = {}
dominio_count = {}
pilar_count = {}
axis_count = {}

for f in sorted(os.listdir(json_dir)):
    if f.startswith("N4_") and f.endswith(".json"):
        with open(json_dir / f) as fp:
            data = json.load(fp)
        uid = data["uid"]
        cells.append({
            "uid": uid,
            "legacy_id": data.get("legacy_id", ""),
            "path": data.get("path", ""),
            "hierarchical_id": data.get("hierarchical_id", ""),
            "nome": data.get("nome", ""),
            "dominio": data.get("dominio", ""),
            "pilar": data.get("pilar", ""),
            "natureza": data.get("natureza", ""),
            "axis": data.get("axis", ""),
            "n3_ref": data.get("n3_ref", ""),
            "num_relacoes": len(data.get("relacoes", [])),
        })
        id_mapping[uid] = {
            "legacy_id": data.get("legacy_id", ""),
            "path": data.get("path", ""),
            "hierarchical_id": data.get("hierarchical_id", ""),
        }
        natureza_count[data.get("natureza", "")] = natureza_count.get(data.get("natureza", ""), 0) + 1
        dominio_count[data.get("dominio", "")] = dominio_count.get(data.get("dominio", ""), 0) + 1
        pilar_count[data.get("pilar", "")] = pilar_count.get(data.get("pilar", ""), 0) + 1
        axis_count[data.get("axis", "")] = axis_count.get(data.get("axis", ""), 0) + 1

print(f"Total de células carregadas: {len(cells)}")
print(f"Naturezas: {dict(sorted(natureza_count.items()))}")
print(f"Domínios: {dict(sorted(dominio_count.items()))}")
print(f"Pilares: {dict(sorted(pilar_count.items()))}")
print(f"Eixos: {dict(sorted(axis_count.items()))}")

# Reconstruir o índice
index = {
    "schema_version": "1.0.0",
    "gerado_em": datetime.now(timezone.utc).isoformat(),
    "total_celulas": len(cells),
    "estatisticas": {
        "por_natureza": dict(sorted(natureza_count.items())),
        "por_dominio": dict(sorted(dominio_count.items())),
        "por_pilar": dict(sorted(pilar_count.items())),
        "por_axis": dict(sorted(axis_count.items())),
    },
    "id_mapping": id_mapping,
    "celulas": cells,
}

with open(index_path, "w", encoding="utf-8") as fp:
    json.dump(index, fp, ensure_ascii=False, indent=2)

print(f"\n✅ Índice reconstruído: {index_path}")
print(f"   {len(id_mapping)} entradas em id_mapping")
print(f"   {len(cells)} entradas em celulas")
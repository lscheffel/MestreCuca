#!/usr/bin/env python3
import json, os
JSON_DIR = r"E:\Arquivos\Área de Trabalho\MestreCuca\data\json"

# Check first cell structure
with open(os.path.join(JSON_DIR, 'N4_ALGORITMIA_1_A.json')) as f:
    d = json.load(f)

with open(os.path.join(JSON_DIR, '_inspect.txt'), 'w') as out:
    out.write("Keys in N4_ALGORITMIA_1_A.json:\n")
    for k in d.keys():
        out.write(f"  {k}\n")
    out.write("\nFull content (non-list fields):\n")
    for k, v in d.items():
        if not isinstance(v, list):
            out.write(f"  {k}: {repr(v)[:300]}\n")
        else:
            out.write(f"  {k}: list[{len(v)} items]\n")

# Check index structure
with open(os.path.join(JSON_DIR, 'ontology_index.json')) as f:
    idx = json.load(f)
with open(os.path.join(JSON_DIR, '_inspect.txt'), 'a') as out:
    out.write(f"\n\nIndex entries: {len(idx)}\n")
    first_key = list(idx.keys())[0]
    out.write(f"First entry keys: {list(idx[first_key].keys())}\n")
    out.write(f"First entry uid: {idx[first_key].get('uid')}\n")

print("Done - check _inspect.txt")
#!/usr/bin/env python3
"""Verifica o formato do campo 'celulas' no ontology_index.json."""
import json, os, sys
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
sys.path.insert(0, 'runtime')

PROJECT_ROOT = os.path.abspath('.')
index_path = os.path.join(PROJECT_ROOT, "data", "json", "ontology_index.json")

with open(index_path, "r", encoding="utf-8") as f:
    idx = json.load(f)

celulas = idx.get("celulas")
print(f"=== campo 'celulas' ===")
print(f"type: {type(celulas)}")
if isinstance(celulas, list):
    print(f"len: {len(celulas)}")
    if len(celulas) > 0:
        print(f"first element type: {type(celulas[0])}")
        print(f"first element: {celulas[0]}")
elif isinstance(celulas, dict):
    print(f"len: {len(celulas)}")
    if len(celulas) > 0:
        firstk = list(celulas.keys())[0]
        print(f"first key: {firstk}")
        print(f"first value: {celulas[firstk]}")
else:
    print(f"value: {celulas}")

id_mapping = idx.get("id_mapping", {})
print(f"\n=== campo 'id_mapping' ===")
print(f"type: {type(id_mapping)}")
print(f"len: {len(id_mapping)}")
if id_mapping:
    firstk = list(id_mapping.keys())[0]
    print(f"first key: {firstk}")
    print(f"first value: {id_mapping[firstk]}")
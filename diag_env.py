#!/usr/bin/env python3
"""Diagnóstico do ambiente do projeto."""
import os
import sys
from pathlib import Path

# Forçar CWD correto
os.chdir("e:/Arquivos/Área de Trabalho/MestreCuca")

print(f"CWD: {os.getcwd()}")
print(f"Python: {sys.executable}")
print(f"sys.path: {sys.path[:5]}")
print()

# Listar raiz
print("=== ARQUIVOS NA RAIZ ===")
for f in sorted(os.listdir('.')):
    print(f"  {f}")

print()
for d in ['data/json', 'data/embeddings', 'config', 'core', 'runtime', 'tools']:
    exists = os.path.isdir(d)
    print(f"{d}: exists={exists}")
    if exists:
        files = sorted(os.listdir(d))
        print(f"  count={len(files)}, files={files[:5]}")

print()
print("=== PYTHON IMPORT TEST ===")
try:
    import numpy as np
    print(f"numpy OK: {np.__version__}")
except Exception as e:
    print(f"numpy FAIL: {e}")

try:
    import networkx as nx
    print(f"networkx OK: {nx.__version__}")
except Exception as e:
    print(f"networkx FAIL: {e}")

try:
    from sentence_transformers import SentenceTransformer
    print("sentence_transformers OK")
except Exception as e:
    print(f"sentence_transformers FAIL: {e}")

try:
    import yaml
    print("yaml OK")
except Exception as e:
    print(f"yaml FAIL: {e}")

try:
    from sklearn.metrics.pairwise import cosine_similarity
    print("sklearn OK")
except Exception as e:
    print(f"sklearn FAIL: {e}")

print()
print("=== JSON INDEX CHECK ===")
idx_path = "data/json/ontology_index.json"
if os.path.exists(idx_path):
    import json
    with open(idx_path) as f:
        idx = json.load(f)
    print(f"Type: {type(idx).__name__}")
    print(f"Keys: {list(idx.keys())[:10]}")
    print(f"id_mapping count: {len(idx.get('id_mapping', {}))}")
    # Check if any N4_*.json exist
    n4_jsons = [f for f in os.listdir('data/json') if f.startswith('N4_') and f.endswith('.json')]
    print(f"N4_*.json files: {len(n4_jsons)}")
    if n4_jsons:
        print(f"  Sample: {n4_jsons[:3]}")
        # Check first one
        with open(f'data/json/{n4_jsons[0]}') as f:
            cell = json.load(f)
        print(f"  Sample cell keys: {list(cell.keys())[:10]}")
        print(f"  Sample uid: {cell.get('uid')}")
        print(f"  Sample path: {cell.get('path')}")
else:
    print("Index not found!")
#!/usr/bin/env python3
"""Diagnóstico do validador — por que validator_cells == 0?"""
import json, os, sys
from pathlib import Path

# Garantir CWD correto
# diag_validator.py está na raiz do projeto, então .parent já é o diretório do projeto
PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "core"))

print(f"CWD: {os.getcwd()}")
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print()

# 1. Verificar índice
idx_path = Path("data/json/ontology_index.json")
print(f"=== INDEX: {idx_path} ===")
print(f"  exists: {idx_path.exists()}")
if idx_path.exists():
    sz = idx_path.stat().st_size
    print(f"  size: {sz} bytes")
    with open(idx_path, encoding="utf-8") as f:
        index = json.load(f)
    print(f"  type: {type(index).__name__}, len: {len(index)}")
    if isinstance(index, list) and len(index) > 0:
        print(f"  first 3: {index[:3]}")
        print(f"  last 3: {index[-3:]}")
    elif isinstance(index, dict):
        print(f"  sample keys: {list(index.keys())[:3]}")
print()

# 2. Verificar N4 JSONs
json_dir = Path("data/json")
n4_files = sorted(json_dir.glob("N4_*.json"))
print(f"=== N4 JSON FILES ===")
print(f"  count: {len(n4_files)}")
if n4_files:
    print(f"  first: {n4_files[0].name}")
    print(f"  last: {n4_files[-1].name}")
    with open(n4_files[0]) as f:
        sample = json.load(f)
    print(f"  sample uid: {sample.get('uid')}")
    print(f"  sample keys: {list(sample.keys())[:8]}")
print()

# 3. Simular _load_registry do validador
print("=== SIMULANDO VALIDATOR._load_registry ===")
registry = {}
try:
    idx_path = Path("data/json/ontology_index.json")
    if idx_path.exists():
        with open(idx_path, encoding="utf-8") as f:
            index = json.load(f)
        print(f"  Index loaded: type={type(index).__name__}, len={len(index)}")
        if isinstance(index, list):
            missing = []
            for uid in index[:5]:
                path = json_dir / f"{uid}.json"
                exists = path.exists()
                if not exists:
                    missing.append(uid)
                print(f"    uid={uid} -> {path} exists={exists}")
            if missing:
                print(f"  MISSING files (first 5): {missing}")
        elif isinstance(index, dict):
            for uid in list(index.keys())[:3]:
                path = json_dir / f"{uid}.json"
                print(f"    uid={uid} -> {path} exists={path.exists()}")
    else:
        print("  Index NOT found, falling back to glob")
        for f in sorted(json_dir.glob("N4_*.json")):
            uid = f.stem
            registry[uid] = json.load(open(f))
        print(f"  Loaded {len(registry)} via glob fallback")
except Exception as e:
    print(f"  ERROR: {e}")
    import traceback
    traceback.print_exc()

print(f"  Registry size: {len(registry)}")
print()

# 4. Verificar embeddings
emb_dir = Path("data/embeddings")
print(f"=== EMBEDDINGS ===")
if emb_dir.exists():
    files = list(emb_dir.glob("*"))
    print(f"  files: {len(files)}")
    for f in files[:5]:
        print(f"    {f.name}: {f.stat().st_size} bytes")
else:
    print("  NO embeddings directory")
print()

# 5. Verificar graph
print("=== GRAPH CHECK ===")
from core.ontology_graph import OntologyGraph
g = OntologyGraph(json_dir="data/json")
loaded = g.load_registry()
print(f"  Registry loaded: {loaded}")
g.build_graph()
print(f"  Graph nodes: {g.G.number_of_nodes()}")
print(f"  Graph edges: {g.G.number_of_edges()}")
print()

# 6. Testar validador diretamente
print("=== VALIDATOR DIRECT TEST ===")
from runtime.validator import OntologyValidator
v = OntologyValidator(json_dir="data/json", index_path="data/json/ontology_index.json")
print(f"  Validator registry size: {len(v.registry)}")
if v.registry:
    print(f"  Sample keys: {list(v.registry.keys())[:3]}")
else:
    print("  Registry is EMPTY — this is the bug!")
    # Try glob fallback
    print("  Trying glob-based load...")
    for f in sorted(Path("data/json").glob("N4_*.json")):
        uid = f.stem
        v.registry[uid] = json.load(open(f))
    print(f"  After glob fallback: {len(v.registry)}")
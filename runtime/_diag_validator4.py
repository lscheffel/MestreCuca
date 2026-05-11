"""Diagnóstico do carregamento do validator registry — executado de dentro de runtime/."""
import json
import sys
import traceback
from pathlib import Path

# O validator.py usa Path(__file__).resolve().parent.parent
# Como este script está em runtime/, parent.parent = MestreCuca
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

print(f"SCRIPT_DIR: {_SCRIPT_DIR}")
print(f"PROJECT_ROOT: {_PROJECT_ROOT}")

json_dir = str(_PROJECT_ROOT / "data/json")
index_path = str(_PROJECT_ROOT / "data/json/ontology_index.json")

print(f"json_dir: {json_dir}")
print(f"json_dir exists: {Path(json_dir).exists()}")
print(f"index_path: {index_path}")
print(f"index_path exists: {Path(index_path).exists()}")
print()

# Load index
with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

print(f"Index keys: {list(index.keys())}")
print(f"'id_mapping' in index: {'id_mapping' in index}")

id_mapping = index.get("id_mapping", {})
print(f"id_mapping type: {type(id_mapping)}")
print(f"id_mapping length: {len(id_mapping)}")
if id_mapping:
    first_key = list(id_mapping.keys())[0]
    print(f"First key: {first_key}")
    print(f"First value: {id_mapping[first_key]}")

# Simulate validator _load_registry
registry = {}
try:
    if isinstance(id_mapping, dict) and len(id_mapping) > 0:
        print(f"\nLoading {len(id_mapping)} cells from id_mapping...")
        missing = 0
        for uid in id_mapping:
            p = Path(json_dir) / f"{uid}.json"
            if p.exists():
                registry[uid] = True
            else:
                missing += 1
                if missing <= 3:
                    print(f"  MISSING: {uid}.json (expected at {p})")
        print(f"Loaded {len(registry)} cells, {missing} missing")
    else:
        print("id_mapping is empty or not a dict, using glob fallback")
        n4_files = sorted(Path(json_dir).glob("N4_*.json"))
        print(f"Glob found {len(n4_files)} N4 files")
except Exception as e:
    print(f"Exception: {e}")
    traceback.print_exc()

print(f"\nFinal registry size: {len(registry)}")
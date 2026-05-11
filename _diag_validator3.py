"""Diagnóstico do carregamento do validator registry."""
import json
import sys
import traceback
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "core"))

json_dir = str(_PROJECT_ROOT / "data/json")
index_path = str(_PROJECT_ROOT / "data/json/ontology_index.json")

print(f"PROJECT_ROOT: {_PROJECT_ROOT}")
print(f"json_dir: {json_dir}")
print(f"json_dir exists: {Path(json_dir).exists()}")
print(f"index_path: {index_path}")
print(f"index_path exists: {Path(index_path).exists()}")
print()

# Load index
with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

print(f"Index keys: {list(index.keys())}")
print(f"'celulas' in index: {'celulas' in index}")

celulas = index.get("celulas")
print(f"celulas type: {type(celulas)}")
print(f"celulas is None: {celulas is None}")

if isinstance(celulas, list):
    print(f"celulas length: {len(celulas)}")
    print(f"celulas first 3: {celulas[:3]}")
    print(f"celulas last 3: {celulas[-3:]}")
elif isinstance(celulas, dict):
    print(f"celulas is dict! keys: {list(celulas.keys())[:5]}")
else:
    print(f"celulas value: {celulas}")

# Check glob fallback
n4_files = sorted(Path(json_dir).glob("N4_*.json"))
print(f"\nGlob N4_*.json found: {len(n4_files)} files")
if n4_files:
    print(f"Sample stems: {[f.stem for f in n4_files[:5]]}")

# Simulate exact validator logic
print("\n--- Simulating validator _load_registry ---")
registry = {}
try:
    if isinstance(celulas, list):
        print(f"Loading from celulas list ({len(celulas)} entries)")
        missing = 0
        for uid in celulas:
            p = Path(json_dir) / f"{uid}.json"
            if p.exists():
                registry[uid] = True
            else:
                missing += 1
                if missing <= 3:
                    print(f"  MISSING: {uid}.json at {p}")
        print(f"Loaded {len(registry)} cells, {missing} missing")
    else:
        print("celulas is NOT a list, using glob fallback")
        for f in n4_files:
            registry[f.stem] = True
        print(f"Loaded {len(registry)} from glob fallback")
except Exception as e:
    print(f"Exception during loading: {e}")
    traceback.print_exc()

print(f"\nFinal registry size: {len(registry)}")
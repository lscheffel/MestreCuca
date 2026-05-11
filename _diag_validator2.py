"""Diagnóstico do carregamento do validator registry."""
import json
import sys
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))
sys.path.insert(0, str(_PROJECT_ROOT / "core"))

json_dir = str(_PROJECT_ROOT / "data/json")
index_path = str(_PROJECT_ROOT / "data/json/ontology_index.json")

print(f"PROJECT_ROOT: {_PROJECT_ROOT}")
print(f"json_dir exists: {Path(json_dir).exists()}")
print(f"index_path exists: {Path(index_path).exists()}")

with open(index_path, "r", encoding="utf-8") as f:
    index = json.load(f)

print(f"Index keys: {list(index.keys())}")
print(f"'celulas' in index: {'celulas' in index}")
print(f"'uids' in index: {'uids' in index}")
print(f"'cells' in index: {'cells' in index}")

celulas = index.get("celulas") or index.get("uids") or index.get("cells")
print(f"celulas value type: {type(celulas)}")
print(f"celulas value: {celulas}")

# Check glob fallback
n4_files = sorted(Path(json_dir).glob("N4_*.json"))
print(f"\nGlob N4_*.json found: {len(n4_files)} files")
print(f"Sample stems: {[f.stem for f in n4_files[:5]]}")

# Try loading like the validator does
registry = {}
if isinstance(celulas, list):
    for uid in celulas:
        p = Path(json_dir) / f"{uid}.json"
        if p.exists():
            registry[uid] = True
        else:
            print(f"  MISSING: {uid}.json")
    print(f"Loaded {len(registry)} from celulas list")
else:
    print("celulas is NOT a list, using glob fallback")
    for f in n4_files:
        registry[f.stem] = True
    print(f"Loaded {len(registry)} from glob fallback")

print(f"\nFinal registry size: {len(registry)}")
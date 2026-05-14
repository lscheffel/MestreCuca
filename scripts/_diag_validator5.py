#!/usr/bin/env python3
"""Diagnóstico do validator no contexto do orchestrator."""
import sys
import os

# Forçar output não-buffered
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

print(f"[DEBUG] Python: {sys.version}", flush=True)
print(f"[DEBUG] CWD: {os.getcwd()}", flush=True)
print(f"[DEBUG] argv: {sys.argv}", flush=True)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"[DEBUG] PROJECT_ROOT: {PROJECT_ROOT}", flush=True)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
    print(f"[DEBUG] Added PROJECT_ROOT to sys.path", flush=True)

core_path = os.path.join(PROJECT_ROOT, "core")
if core_path not in sys.path:
    sys.path.insert(0, core_path)
    print(f"[DEBUG] Added core to sys.path", flush=True)

print(f"[DEBUG] sys.path[:5] = {sys.path[:5]}", flush=True)

# Testar import básico
try:
    import numpy as np
    print(f"[DEBUG] numpy: {np.__version__}", flush=True)
except Exception as e:
    print(f"[ERROR] numpy import failed: {e}", flush=True)

try:
    from pathlib import Path
    print(f"[DEBUG] pathlib ok", flush=True)
except Exception as e:
    print(f"[ERROR] pathlib import failed: {e}", flush=True)

# Testar import do validator
try:
    from runtime.validator import OntologyValidator
    print(f"[DEBUG] OntologyValidator imported successfully", flush=True)
except Exception as e:
    print(f"[ERROR] OntologyValidator import failed: {e}", flush=True)
    import traceback
    traceback.print_exc()

# Testar instanciação
try:
    json_dir = os.path.join(PROJECT_ROOT, "data", "json")
    index_path = os.path.join(PROJECT_ROOT, "data", "json", "ontology_index.json")
    print(f"[DEBUG] json_dir: {json_dir}", flush=True)
    print(f"[DEBUG] index_path: {index_path}", flush=True)
    print(f"[DEBUG] json_dir exists: {os.path.isdir(json_dir)}", flush=True)
    print(f"[DEBUG] index_path exists: {os.path.isfile(index_path)}", flush=True)

    v = OntologyValidator(json_dir=json_dir, index_path=index_path)
    print(f"[RESULT] Registry size: {len(v.registry)}", flush=True)
    if v.registry:
        print(f"[RESULT] First 5 keys: {list(v.registry.keys())[:5]}", flush=True)
    else:
        print(f"[WARN] Registry is EMPTY", flush=True)
except Exception as e:
    print(f"[ERROR] OntologyValidator instantiation failed: {e}", flush=True)
    import traceback
    traceback.print_exc()

print("[DONE] Diagnostic complete", flush=True)
#!/usr/bin/env python3
"""Diagnóstico do estado dos dados do sistema cognitivo."""
import os, sys, json, glob

project_root = "e:/Arquivos/Área de Trabalho/MestreCuca"
os.chdir(project_root)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "core"))
sys.path.insert(0, os.path.join(project_root, "runtime"))
sys.path.insert(0, os.path.join(project_root, ".kilo", "agents"))

print("=" * 60)
print("DIAGNÓSTICO DE DADOS")
print("=" * 60)

# 1. Check data/json
json_dir = os.path.join(project_root, "data", "json")
print(f"\n📁 data/json exists: {os.path.isdir(json_dir)}")
if os.path.isdir(json_dir):
    all_files = os.listdir(json_dir)
    n4_files = [f for f in all_files if f.startswith("N4_") and f.endswith(".json")]
    other_files = [f for f in all_files if not f.startswith("N4_") or not f.endswith(".json")]
    print(f"   Total files: {len(all_files)}")
    print(f"   N4 JSON files: {len(n4_files)}")
    print(f"   Other files: {other_files}")
    
    idx_path = os.path.join(json_dir, "ontology_index.json")
    print(f"\n📄 ontology_index.json exists: {os.path.exists(idx_path)}")
    if os.path.exists(idx_path):
        with open(idx_path) as f:
            idx = json.load(f)
        print(f"   Keys: {list(idx.keys())}")
        print(f"   cells: {len(idx.get('cells', []))}")
        print(f"   files: {len(idx.get('files', [])) if isinstance(idx.get('files'), list) else 'N/A'}")
    else:
        print("   ❌ Index not found - will need to generate")

    # Sample a N4 file
    if n4_files:
        sample_path = os.path.join(json_dir, n4_files[0])
        with open(sample_path) as f:
            sample = json.load(f)
        print(f"\n📋 Sample N4 ({n4_files[0]}):")
        print(f"   Keys: {list(sample.keys())}")
        print(f"   uid: {sample.get('uid', 'N/A')}")
        print(f"   path: {sample.get('path', 'N/A')}")
        print(f"   natureza: {sample.get('natureza', 'N/A')}")
        print(f"   relacoes count: {len(sample.get('relacoes', []))}")
        if sample.get('relacoes'):
            print(f"   relacoes[0]: {sample['relacoes'][0]}")

# 2. Check data/embeddings
emb_dir = os.path.join(project_root, "data", "embeddings")
print(f"\n📁 data/embeddings exists: {os.path.isdir(emb_dir)}")
if os.path.isdir(emb_dir):
    emb_files = glob.glob(os.path.join(emb_dir, "*.npy"))
    print(f"   .npy files: {len(emb_files)}")
    for f in emb_files[:3]:
        print(f"     - {os.path.basename(f)}")

# 3. Check data/graphs
graph_dir = os.path.join(project_root, "data", "graphs")
print(f"\n📁 data/graphs exists: {os.path.isdir(graph_dir)}")
if os.path.isdir(graph_dir):
    graph_files = os.listdir(graph_dir)
    print(f"   Files: {len(graph_files)}")

# 4. Check data/indexes
idx_dir = os.path.join(project_root, "data", "indexes")
print(f"\n📁 data/indexes exists: {os.path.isdir(idx_dir)}")
if os.path.isdir(idx_dir):
    idx_files = os.listdir(idx_dir)
    print(f"   Files: {len(idx_files)}")

print("\n" + "=" * 60)
print("FIM DO DIAGNÓSTICO")
print("=" * 60)
#!/usr/bin/env python3
"""Diagnostico do bug infer_paths - versao arquivo."""
import sys
import os
os.chdir(r"e:\Arquivos\Área de Trabalho\MestreCuca")
sys.path.insert(0, 'core')

import networkx as nx
print(f"NetworkX version: {nx.__version__}")

# Verificar NetworkXNoPath
print(f"Has NetworkXNoPath: {hasattr(nx, 'NetworkXNoPath')}")

# Verificar excecoes
for name in dir(nx):
    obj = getattr(nx, name)
    if isinstance(obj, type) and issubclass(obj, BaseException):
        print(f"  NX Exception: {name}")

from ontology_graph import OntologyGraph

g = OntologyGraph()
g.load_registry()
g.build_graph()

print(f"\nNodes: {g.G.number_of_nodes()}")
print(f"Edges: {g.G.number_of_edges()}")

src = 'N4_ALGORITMIA_1_A'
tgt = 'N4_MISTERIO_3_A'
print(f"\n{src} in G: {src in g.G}")
print(f"{tgt} in G: {tgt in g.G}")

# Testar all_simple_paths diretamente
import traceback
search_graph = g.G.to_undirected()
try:
    paths = list(nx.all_simple_paths(search_graph, src, tgt, cutoff=8))
    print(f"all_simple_paths OK: {len(paths)} paths found")
except Exception as e:
    print(f"all_simple_paths Exception: {type(e).__name__}: {e}")
    traceback.print_exc()

# Testar infer_paths
try:
    result = g.infer_paths(src, tgt, max_length=8)
    print(f"infer_paths OK: {len(result)} paths")
except Exception as e:
    print(f"infer_paths Exception: {type(e).__name__}: {e}")
    traceback.print_exc()
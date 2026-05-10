#!/usr/bin/env python3
"""Diagnostico do bug infer_paths."""
import sys
import os
os.chdir(r"e:\Arquivos\Área de Trabalho\MestreCuca")
sys.path.insert(0, 'core')

import networkx as nx
from ontology_graph import OntologyGraph

g = OntologyGraph()
g.load_registry()
g.build_graph()

print(f"Nodes: {g.G.number_of_nodes()}")
print(f"Edges: {g.G.number_of_edges()}")

# Verificar se os nós existem
src = 'N4_ALGORITMIA_1_A'
tgt = 'N4_MISTERIO_3_A'
print(f"{src} in G: {src in g.G}")
print(f"{tgt} in G: {tgt in g.G}")

# Verificar componentes conexas
undirected = g.G.to_undirected()
cc = list(nx.connected_components(undirected))
print(f"Componentes conexas: {len(cc)}")
for i, comp in enumerate(cc):
    has_algo = src in comp
    has_mist = tgt in comp
    if has_algo or has_mist:
        print(f"  Componente {i}: tamanho={len(comp)}, ALGO={has_algo}, MIST={has_mist}")

# Testar all_simple_paths diretamente
try:
    search_graph = g.G.to_undirected()
    paths = list(nx.all_simple_paths(search_graph, src, tgt, cutoff=8))
    print(f"all_simple_paths found: {len(paths)} paths")
    if paths:
        print(f"  Primeiro caminho: {paths[0]}")
except Exception as e:
    print(f"Exception type: {type(e).__name__}")
    print(f"Exception module: {type(e).__module__}")
    print(f"Exception message: '{e}'")
    import traceback
    traceback.print_exc()

# Testar infer_paths
try:
    result = g.infer_paths(src, tgt, max_length=8)
    print(f"infer_paths result type: {type(result)}")
    print(f"infer_paths result len: {len(result)}")
except Exception as e:
    print(f"infer_paths Exception: {type(e).__name__}: '{e}'")
    import traceback
    traceback.print_exc()

# Verificar NetworkXNoPath
print(f"\nHas NetworkXNoPath: {hasattr(nx, 'NetworkXNoPath')}")
print(f"Has NoPath: {hasattr(nx, 'NoPath')}")
excs = [a for a in dir(nx) if 'Error' in a or 'Exception' in a or 'NoPath' in a]
print(f"NX exceptions: {excs}")
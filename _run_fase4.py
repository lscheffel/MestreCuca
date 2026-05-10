#!/usr/bin/env python3
"""Teste FASE 4 - Retrieval Hibrido"""
import sys, time, json, numpy as np
from pathlib import Path

sys.path.insert(0, str(Path('tools')))
sys.path.insert(0, str(Path('core')))

from runtime.retriever import HybridRetriever
from core.ontology_graph import OntologyGraph

print('=== FASE 4 TESTE ===')

# Grafo
g = OntologyGraph('data/json')
g.load_registry()
g.build_graph()
nos = g.G.number_of_nodes()
arestas = g.G.number_of_edges()
print(f'Grafo: {nos} nos, {arestas} arestas')

# Retriever
r = HybridRetriever(embedding_dir='data/embeddings', graph_engine=g)
print(f'Embeddings carregados: {r.get_candidates_count()}')
r.warm_up()

# Queries
qs = [
    'decomposicao problemas complexos',
    'validacao sistemas',
    'metabolismo ciclos',
    'reconhecimento padroes',
    'homeostase equilibrio',
    'transformacao ruptura',
]

ok = True
for q in qs:
    t0 = time.time()
    res = r.search(q, top_k=12)
    dt = time.time() - t0
    if not res:
        print(f'FALHA {q}: sem resultados')
        ok = False
        continue
    top_score = res[0]['score']
    has_high = any(x['score'] >= 0.72 for x in res)
    has_graph = any(x['graph_score'] > 0 for x in res)
    has_sem = any(x['semantic_sim'] > 0 for x in res)
    fast = dt < 1.0
    top3 = ', '.join(x['conceito'] for x in res[:3])
    tag = 'OK' if fast else 'LENTO'
    print(f'[{tag}] {q}: {dt:.3f}s top={top_score:.4f} -> {top3}')
    if not fast:
        ok = False
    if not has_sem:
        ok = False

# Embeddings
emb_dir = Path('data/embeddings')
npy_files = sorted(emb_dir.glob('N4_*.npy'))
print(f'Arquivos .npy: {len(npy_files)}')
if npy_files:
    dims_ok = all(np.load(f).shape == (384,) for f in npy_files)
    print(f'Todas dimensao 384: {"SIM" if dims_ok else "NAO"}')
    if not dims_ok:
        ok = False

ix = json.load(open('data/embeddings/embeddings_index.json'))
print(f'Index: {len(ix.get("embeddings",{}))} entradas')

print('=' * 50)
print(f'RESULTADO: {"APROVADO" if ok else "COM AVARIAS"}')
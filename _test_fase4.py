#!/usr/bin/env python3
"""Teste de validacao end-to-end do pipeline de retrieval hibrido - FASE 4."""
import sys, time, json, numpy as np
from pathlib import Path

PROJECT_ROOT = Path('.')
sys.path.insert(0, str(PROJECT_ROOT / 'tools'))
sys.path.insert(0, str(PROJECT_ROOT / 'core'))

from runtime.retriever import HybridRetriever
from core.ontology_graph import OntologyGraph

print('=' * 70)
print('  TESTE FASE 4 — RETRIEVAL HIBRIDO')
print('=' * 70)

# 1. Carregar grafo
print('\n[1/5] Carregando grafo...')
graph = OntologyGraph('data/json')
graph.load_registry()
graph.build_graph()
print(f'  OK: {graph.G.number_of_nodes()} nos, {graph.G.number_of_edges()} arestas')

# 2. Inicializar retriever
print('\n[2/5] Inicializando HybridRetriever...')
retriever = HybridRetriever(embedding_dir='data/embeddings', graph_engine=graph)
print(f'  OK: {retriever.get_candidates_count()} embeddings')

# 3. Warm-up
print('\n[3/5] Pre-carregando modelo...')
retriever.warm_up()

# 4. Testes
queries = [
    'decomposicao de problemas complexos',
    'validacao e verificacao de sistemas',
    'ciclos metabolicos e transformacoes',
    'reconhecimento de padroes',
    'equilibrio dinamico e homeostase',
    'transformacao e ruptura criativa',
]

all_ok = True
for q in queries:
    start = time.time()
    results = retriever.search(q, top_k=12)
    elapsed = time.time() - start
    if not results:
        print(f'  FAIL "{q}": sem resultados ({elapsed:.3f}s)')
        all_ok = False
        continue
    top = results[0]
    has_high = any(r['score'] >= 0.72 for r in results)
    has_graph = any(r['graph_score'] > 0 for r in results)
    has_sem = any(r['semantic_sim'] > 0 for r in results)
    fast = elapsed < 1.0
    top3 = ', '.join(r['conceito'] for r in results[:3])
    tag = 'OK' if fast else 'SLOW'
    print(f'  [{tag}] "{q}": {elapsed:.3f}s | top={top["score"]:.4f} | {top3}')
    if not fast:
        all_ok = False
    if not has_sem:
        all_ok = False
    if not has_graph:
        print(f'    WARN sem expansao de grafo')

# 5. Verificar embeddings
print('\n[4/5] Verificando embeddings...')
emb_dir = Path('data/embeddings')
npy_files = sorted(emb_dir.glob('N4_*.npy'))
print(f'  Arquivos .npy: {len(npy_files)}')
if npy_files:
    dims_ok = all(np.load(f).shape == (384,) for f in npy_files)
    print(f'  Dimensao 384: {"OK" if dims_ok else "FAIL"}')
    if not dims_ok:
        all_ok = False

idx_path = emb_dir / 'embeddings_index.json'
if idx_path.exists():
    with open(idx_path) as f:
        idx = json.load(f)
    print(f'  Index: {len(idx.get("embeddings", {}))} entradas')

print('\n[5/5] Resultado:')
print('=' * 70)
if all_ok:
    print('  FASE 4 APROVADA — Pipeline operacional!')
else:
    print('  FASE 4 COM AVARIAS')
print('=' * 70)
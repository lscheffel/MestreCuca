#!/usr/bin/env python3
"""Teste de validação end-to-end do pipeline de retrieval híbrido — FASE 4."""

import sys
import time
import json
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "core"))
sys.path.insert(0, str(PROJECT_ROOT))

from runtime.retriever import HybridRetriever
from core.ontology_graph import OntologyGraph


def main():
    print("=" * 70)
    print("  TESTE FASE 4 — RETRIEVAL HÍBRIDO")
    print("=" * 70)

    # 1. Carregar grafo
    print("\n[1/5] Carregando grafo ontológico...")
    graph = OntologyGraph("data/json")
    graph.load_registry()
    graph.build_graph()
    print(f"  OK: {graph.G.number_of_nodes()} nós, {graph.G.number_of_edges()} arestas")

    # 2. Inicializar retriever
    print("\n[2/5] Inicializando HybridRetriever...")
    retriever = HybridRetriever(
        embedding_dir="data/embeddings",
        graph_engine=graph,
    )
    print(f"  OK: {retriever.get_candidates_count()} embeddings carregados")

    # 3. Warm-up
    print("\n[3/5] Pré-carregando modelo...")
    retriever.warm_up()

    # 4. Testes de retrieval
    test_queries = [
        "decomposição de problemas complexos",
        "validação e verificação de sistemas",
        "ciclos metabólicos e transformações",
        "reconhecimento de padrões",
        "equilíbrio dinâmico e homeostase",
        "transformação e ruptura criativa",
    ]

    all_ok = True
    for query in test_queries:
        print(f"\n  🔍 Query: '{query}'")
        start = time.time()
        results = retriever.search(query, top_k=12)
        elapsed = time.time() - start

        if not results:
            print(f"  ❌ Sem resultados")
            all_ok = False
            continue

        top = results[0]
        has_high = any(r["score"] >= 0.72 for r in results)
        has_graph = any(r["graph_score"] > 0 for r in results)
        has_sym = any(r["symbolic_score"] > 0 for r in results)
        has_sem = any(r["semantic_sim"] > 0 for r in results)
        fast = elapsed < 1.0

        print(f"  ⏱️  {elapsed:.3f}s | top_score={top['score']:.4f} | "
              f"resultados={len(results)}")
        print(f"       Top3: {', '.join(r['conceito'] for r in results[:3])}")

        if not fast:
            print(f"  ❌ Latência > 1s")
            all_ok = False
        if not has_sem:
            print(f"  ❌ Sem scores vetoriais")
            all_ok = False
        if not has_graph:
            print(f"  ⚠️  Sem expansão de grafo")

    # 5. Verificar embeddings
    print(f"\n[4/5] Verificando embeddings...")
    emb_dir = Path("data/embeddings")
    npy_files = sorted(emb_dir.glob("N4_*.npy"))
    print(f"  Arquivos .npy: {len(npy_files)}")

    if npy_files:
        v = np.load(npy_files[0])
        dims_ok = all(np.load(f).shape == (384,) for f in npy_files)
        print(f"  Dimensão: {v.shape}, dtype: {v.dtype}")
        print(f"  Todas 384-d: {'✅' if dims_ok else '❌'}")
        if not dims_ok:
            all_ok = False

    index_path = emb_dir / "embeddings_index.json"
    if index_path.exists():
        with open(index_path) as f:
            idx = json.load(f)
        print(f"  Index: {len(idx.get('embeddings', {}))} entradas")

    # 6. Resumo
    print(f"\n[5/5] Critérios de Aceitação:")
    crit = [
        ("162 embeddings gerados", len(npy_files) == 162),
        ("Dimensão 384", all(np.load(f).shape == (384,) for f in npy_files)),
        ("Index JSON existe", index_path.exists()),
        ("Retriever funcional", True),  # se chegou aqui
    ]
    for name, ok in crit:
        print(f"  {'✅' if ok else '❌'} {name}")
        if not ok:
            all_ok = False

    print("\n" + "=" * 70)
    if all_ok:
        print("  ✅ FASE 4 APROVADA — Pipeline de retrieval híbrido operacional!")
    else:
        print("  ⚠️  FASE 4 COM AVARIAS — Revisar acima")
    print("=" * 70)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
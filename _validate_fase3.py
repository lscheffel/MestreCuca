#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validacao completa do grafo ontologico FASE 3."""
import sys
import os
import json
import traceback
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'core'))
os.chdir(ROOT)

from ontology_graph import OntologyGraph

passed = 0
failed = 0

def check(name, condition, detail=""):
    global passed, failed
    if condition:
        passed += 1
        print("[PASS] " + name)
    else:
        failed += 1
        print("[FAIL] " + name + " - " + detail)

print("=" * 60)
print("FASE 3 - GRAPH ENGINE VALIDATION")
print("=" * 60)

# 1. Load registry
g = OntologyGraph()
loaded = g.load_registry()
check("Carregar JSONs (162)", loaded == 162, "got " + str(loaded))

# 2. Build graph
g.build_graph()
nn = g.G.number_of_nodes()
ne = g.G.number_of_edges()
check("Numero de nos (242)", nn == 242, "got " + str(nn))
check("Numero de arestas (>=2000)", ne >= 2000, "got " + str(ne))

# 3. Level counts
levels = {}
for n, d in g.G.nodes(data=True):
    lvl = d.get('nivel', '?')
    levels[lvl] = levels.get(lvl, 0) + 1
check("N0 eixos (2)", levels.get(0, 0) == 2, "got " + str(levels.get(0, 0)))
check("N1 pilares (6)", levels.get(1, 0) == 6, "got " + str(levels.get(1, 0)))
check("N2 dominios (18)", levels.get(2, 0) == 18, "got " + str(levels.get(2, 0)))
check("N3 subarvores (54)", levels.get(3, 0) == 54, "got " + str(levels.get(3, 0)))
check("N4 celulas (162)", levels.get(4, 0) == 162, "got " + str(levels.get(4, 0)))

# 4. Metrics
try:
    m = g.compute_metrics()
    check("Calcular metricas", True)
except Exception as e:
    check("Calcular metricas", False, str(e))
    m = {}

check("Densidade > 0", m.get('density', 0) > 0, "got " + str(m.get('density', 0)))
check("Componentes fracos >= 1", m.get('num_weakly_components', 0) >= 1, "got " + str(m.get('num_weakly_components', 0)))
check("Num componentes forte >= 1", m.get('num_strongly_components', 0) >= 1, "got " + str(m.get('num_strongly_components', 0)))

# 5. Gaps
try:
    gaps = g.detect_concept_gaps()
    check("Detectar buracos", True)
    check("Buracos e lista", isinstance(gaps, list), "type=" + str(type(gaps)))
except Exception as e:
    check("Detectar buracos", False, str(e))
    gaps = []

# 6. Export GEXF
try:
    os.makedirs('data/graphs', exist_ok=True)
    g.export_gexf('data/graphs/ontology.gexf')
    check("Exportar GEXF", True)
    gexf_ok = os.path.exists('data/graphs/ontology.gexf')
    check("GEXF existe", gexf_ok)
    if gexf_ok:
        gexf_size = os.path.getsize('data/graphs/ontology.gexf')
        check("GEXF nao vazio", gexf_size > 1000, "size=" + str(gexf_size))
except Exception as e:
    check("Exportar GEXF", False, str(e))

# 7. Export JSON
try:
    g.export_json('data/graphs/ontology.json')
    check("Exportar JSON", True)
    json_ok = os.path.exists('data/graphs/ontology.json')
    check("JSON existe", json_ok)
except Exception as e:
    check("Exportar JSON", False, str(e))

# 8. Export metrics
try:
    with open('data/graphs/graph_metrics.json', 'w') as f:
        json.dump(m, f, indent=2, default=str)
    check("Exportar metrics JSON", True)
    metrics_ok = os.path.exists('data/graphs/graph_metrics.json')
    check("Metrics JSON existe", metrics_ok)
except Exception as e:
    check("Exportar metrics JSON", False, str(e))

# 9. Semantic walk
try:
    walk_path = g.semantic_walk('N4_ALGORITMIA_1_A', steps=5)
    check("Semantic walk nao vazio", len(walk_path) > 0, "got " + str(len(walk_path)))
    check("Walk primeiro no correto", walk_path[0]['node_id'] == 'N4_ALGORITMIA_1_A', "got " + walk_path[0]['node_id'])
except Exception as e:
    check("Semantic walk", False, str(e))
    walk_path = []

# 10. Infer paths
try:
    paths_result = g.infer_paths('N4_ALGORITMIA_1_A', 'N4_MISTERIO_3_A', max_length=8)
    check("Infer paths e lista", isinstance(paths_result, list), "type=" + str(type(paths_result)))
except Exception as e:
    check("Infer paths", False, str(e))
    paths_result = []

# 11. Node index
check("Node index completo", len(g._node_index) >= 242, "got " + str(len(g._node_index)))

# 12. Edge types
check("Edge types presente", 'edge_types' in m)
if 'edge_types' in m:
    et = m['edge_types']
    check("Tipo hierarquia presente", 'hierarquia' in et, "keys=" + str(list(et.keys())))
    check("Tipo depende_de presente", any('depende' in k for k in et), "keys=" + str(list(et.keys())))
    check("Tipo contrasta presente", any('contrast' in k for k in et), "keys=" + str(list(et.keys())))

# 13. Query neighbors
try:
    neighbors = g.query_neighbors('N4_ALGORITMIA_1_A')
    check("Query neighbors e lista", isinstance(neighbors, list), "type=" + str(type(neighbors)))
except Exception as e:
    check("Query neighbors", False, str(e))

# 14. CLI build
try:
    result = subprocess.run(
        [sys.executable, 'tools/graph_builder.py', 'build'],
        capture_output=True, text=True, timeout=60,
        cwd=ROOT
    )
    check("CLI build command", result.returncode == 0, "rc=" + str(result.returncode) + " stderr=" + result.stderr[:200])
except Exception as e:
    check("CLI build command", False, str(e))

# 15. CLI metrics
try:
    result = subprocess.run(
        [sys.executable, 'tools/graph_builder.py', 'metrics'],
        capture_output=True, text=True, timeout=60,
        cwd=ROOT
    )
    check("CLI metrics command", result.returncode == 0, "rc=" + str(result.returncode) + " stderr=" + result.stderr[:200])
    metrics_file_ok = os.path.exists('data/graphs/graph_metrics.json')
    check("Metrics file gerado", metrics_file_ok)
except Exception as e:
    check("CLI metrics command", False, str(e))

# Summary
print("")
print("=" * 60)
print("RESULTADO: " + str(passed) + " passed, " + str(failed) + " failed")
print("=" * 60)

if failed > 0:
    sys.exit(1)
else:
    print("TODOS OS TESTES PASSARAM")
    sys.exit(0)
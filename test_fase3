#!/usr/bin/env python3
"""Validação completa do FASE 3 — Graph Engine."""
import sys, json, os
sys.path.insert(0, 'core')
from ontology_graph import OntologyGraph

g = OntologyGraph()
loaded = g.load_registry()
print(f'JSONs carregados: {loaded}')
g.build_graph()
print(f'Nos: {g.G.number_of_nodes()}, Arestas: {g.G.number_of_edges()}')

levels = {}
for n, d in g.G.nodes(data=True):
    lvl = d.get('nivel', '?')
    levels[lvl] = levels.get(lvl, 0) + 1
print(f'Por nivel: {dict(sorted(levels.items()))}')

m = g.compute_metrics()
print(f'Densidade: {m["density"]:.4f}')
print(f'Diametro: {m.get("diameter", "N/A")}')
print(f'Caminho medio: {m.get("average_shortest_path_length", "N/A"):.4f}')
print(f'Componentes fracos: {m["num_weakly_components"]}')
print(f'Componentes fortes: {m["num_strongly_components"]}')
print(f'Pontes: {len(m["bridges"])}')
print(f'Isolados: {len(m["isolates"])}')
print(f'Assortatividade: {m.get("degree_assortativity", "N/A"):.4f}')

gaps = g.detect_concept_gaps()
print(f'Buracos ontologicos: {len(gaps)}')

os.makedirs('data/graphs', exist_ok=True)
g.export_gexf('data/graphs/ontology.gexf')
g.export_json('data/graphs/ontology.json')
with open('data/graphs/graph_metrics.json', 'w') as f:
    json.dump(m, f, indent=2, default=str)
print('Exportacoes concluidas.')

# Semantic walk
path = g.semantic_walk('N4_ALGORITMIA_1_A', steps=5)
print(f'\nWalk (5 passos):')
for p in path:
    print(f'  Passo {p["step"]}: {p["node_id"]} ({p.get("nome", "")})')

# Paths
paths = g.infer_paths('N4_ALGORITMIA_1_A', 'N4_MISTERIO_3_A', max_length=8)
print(f'\nCaminhos N4_ALGORITMIA_1_A -> N4_MISTERIO_3_A: {len(paths)} encontrados')
for p in paths[:3]:
    print(f'  {p["path"]} (peso: {p["total_weight"]:.2f})')

# Edge type stats
print(f'\nTipos de aresta:')
for t, c in sorted(m['edge_types'].items(), key=lambda x: -x[1]):
    print(f'  {t}: {c}')

print('\n=== VALIDACAO CONCLUIDA ===')
@echo off
cd /d "e:\Arquivos\Área de Trabalho\MestreCuca"
python -c "
import sys, json, os
sys.path.insert(0, 'core')
from ontology_graph import OntologyGraph

g = OntologyGraph()
loaded = g.load_registry()
print('JSONs carregados: %d' % loaded)
g.build_graph()
print('Nos: %d, Arestas: %d' % (g.G.number_of_nodes(), g.G.number_of_edges()))

levels = {}
for n, d in g.G.nodes(data=True):
    lvl = d.get('nivel', '?')
    levels[lvl] = levels.get(lvl, 0) + 1
print('Por nivel: %s' % dict(sorted(levels.items())))

m = g.compute_metrics()
print('Densidade: %.4f' % m['density'])
print('Diametro: %s' % m.get('diameter', 'N/A'))
print('Caminho medio: %.4f' % m.get('average_shortest_path_length', 0))
print('Componentes fracos: %d' % m['num_weakly_components'])
print('Componentes fortes: %d' % m['num_strongly_components'])
print('Pontes: %d' % len(m['bridges']))
print('Isolados: %d' % len(m['isolates']))
print('Assortatividade: %.4f' % m.get('degree_assortativity', 0))

gaps = g.detect_concept_gaps()
print('Buracos ontologicos: %d' % len(gaps))

os.makedirs('data/graphs', exist_ok=True)
g.export_gexf('data/graphs/ontology.gexf')
g.export_json('data/graphs/ontology.json')
with open('data/graphs/graph_metrics.json', 'w') as f:
    json.dump(m, f, indent=2, default=str)
print('Exportacoes concluidas.')

path = g.semantic_walk('N4_ALGORITMIA_1_A', steps=5)
print('Walk (5 passos):')
for p in path:
    print('  Passo %d: %s (%s)' % (p['step'], p['node_id'], p.get('nome', '')))

paths = g.infer_paths('N4_ALGORITMIA_1_A', 'N4_MISTERIO_3_A', max_length=8)
print('Caminhos N4_ALGORITMIA_1_A -> N4_MISTERIO_3_A: %d encontrados' % len(paths))
for p in paths[:3]:
    print('  %s (peso: %.2f)' % (p['path'], p['total_weight']))

print('Tipos de aresta:')
for t, c in sorted(m['edge_types'].items(), key=lambda x: -x[1]):
    print('  %s: %d' % (t, c))

print('=== VALIDACAO CONCLUIDA ===')
" > fase3_output.txt 2>&1
type fase3_output.txt
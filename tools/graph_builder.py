#!/usr/bin/env python3
"""
Graph Builder CLI — FASE 3: Motor de Grafo Ontológico

Ferramenta de linha de comando para construção, análise e exploração
do grafo semântico fractal a partir dos 162 JSONs enriquecidos.

Comandos disponíveis:
    build       — Constrói o grafo e exporta para GEXF/JSON
    metrics     — Calcula e exibe métricas topológicas
    analyze     — Build + métricas + detecção de buracos
    walk        — Passeio semântico a partir de um nó
    paths       — Encontra caminhos entre dois nós
    validate    — Valida integridade do grafo construído

Uso:
    python tools/graph_builder.py build
    python tools/graph_builder.py metrics
    python tools/graph_builder.py analyze
    python tools/graph_builder.py walk --start N4_ALGORITMIA_1_A --steps 5
    python tools/graph_builder.py paths --source N4_ALGORITMIA_1_A --target N4_BIOS_1_A
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# Garantir que o root do projeto está no path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.ontology_graph import OntologyGraph


# ---------------------------------------------------------------------------
# Helpers de output
# ---------------------------------------------------------------------------

def _header(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def _ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def _warn(msg: str) -> None:
    print(f"  ⚠️  {msg}")


def _info(msg: str) -> None:
    print(f"  ℹ️  {msg}")


# ---------------------------------------------------------------------------
# Comandos
# ---------------------------------------------------------------------------

def _ensure_graph(output_dir: str = "data/graphs") -> OntologyGraph:
    """Carrega registry e constrói o grafo."""
    g = OntologyGraph()
    _info("Carregando registry de JSONs...")
    count = g.load_registry()
    _ok(f"{count} células carregadas")
    _info("Construindo grafo...")
    g.build_graph()
    _ok(f"Grafo construído: {g.G.number_of_nodes()} nós, {g.G.number_of_edges()} arestas")

    # Exportar
    os.makedirs(output_dir, exist_ok=True)
    gexf_path = os.path.join(output_dir, "ontology.gexf")
    json_path = os.path.join(output_dir, "ontology.json")
    g.export_gexf(gexf_path)
    _ok(f"Exportado GEXF → {gexf_path}")
    g.export_json(json_path)
    _ok(f"Exportado JSON → {json_path}")
    return g


def cmd_build(args: argparse.Namespace) -> None:
    """Constrói o grafo e exporta."""
    _header("BUILD — Construção do Grafo Ontológico")
    output_dir = getattr(args, 'output', 'data/graphs')
    g = _ensure_graph(output_dir)
    print(g.summary())


def cmd_metrics(args: argparse.Namespace) -> None:
    """Calcula e exibe métricas topológicas."""
    _header("METRICS — Métricas Topológicas")
    output_dir = getattr(args, 'output', 'data/graphs')
    g = _ensure_graph(output_dir)

    m = g.compute_metrics()

    print(f"\n  📊 MÉTRICAS DO GRAFO")
    print(f"  {'─' * 40}")
    print(f"  Nós:                    {m['nodes']}")
    print(f"  Arestas:                {m['edges']}")
    print(f"  Densidade:              {m['density']:.6f}")
    print(f"  Diâmetro:               {m.get('diameter', 'N/A')}")
    print(f"  Caminho médio:          {m.get('average_shortest_path_length', 'N/A'):.4f}")
    print(f"  Clustering médio:       {m['avg_clustering']:.4f}")
    print(f"  Assortatividade grau:   {m['degree_assortativity']:.4f}")
    print(f"  Componentes fracos:     {m['num_weakly_components']}")
    print(f"  Componentes fortes:     {m['num_strongly_components']}")
    print(f"  Pontes (bridges):       {len(m['bridges'])}")
    print(f"  Pontos articulação:     {len(m['articulation_points'])}")
    print(f"  Nós isolados:           {len(m['isolates'])}")

    print(f"\n  📈 Nós por Nível:")
    for level in sorted(m['nodes_by_level'].keys()):
        bar = "█" * m['nodes_by_level'][level]
        print(f"    N{level}: {m['nodes_by_level'][level]:>3}  {bar}")

    print(f"\n  🔗 Tipos de Aresta:")
    for t, count in sorted(m['edge_types'].items(), key=lambda x: -x[1]):
        print(f"    {t:<20s} {count:>4}")

    print(f"\n  📊 Peso das Arestas por Tipo:")
    for t, stats in sorted(m['edge_weight_stats'].items()):
        print(f"    {t:<20s}  count={stats['count']:>3}  "
              f"mean={stats['mean']:>+.4f}  "
              f"[{stats['min']:>+.4f}, {stats['max']:>+.4f}]")

    print(f"\n  🏆 Top 10 Betweenness Centrality:")
    for i, (node, score) in enumerate(m['top_betweenness'], 1):
        label = g._node_index.get(node, {}).get('nome', node)
        nivel = g._node_index.get(node, {}).get('nivel', '?')
        print(f"    {i:>2}. [{nivel}] {label:<30s} {score:.6f}  ({node})")

    print(f"\n  🏆 Top 10 Degree Centrality:")
    for i, (node, score) in enumerate(m['top_degree'], 1):
        label = g._node_index.get(node, {}).get('nome', node)
        nivel = g._node_index.get(node, {}).get('nivel', '?')
        print(f"    {i:>2}. [{nivel}] {label:<30s} {score:.6f}  ({node})")

    if m.get('top_eigenvector'):
        print(f"\n  🏆 Top 10 Eigenvector Centrality:")
        for i, (node, score) in enumerate(m['top_eigenvector'], 1):
            label = g._node_index.get(node, {}).get('nome', node)
            nivel = g._node_index.get(node, {}).get('nivel', '?')
            print(f"    {i:>2}. [{nivel}] {label:<30s} {score:.6f}  ({node})")

    # Salvar métricas em JSON
    metrics_path = os.path.join(output_dir, "graph_metrics.json")
    # Converter para serializável
    serializable = {}
    for k, v in m.items():
        if isinstance(v, dict):
            serializable[k] = {str(kk): vv for kk, vv in v.items()}
        elif isinstance(v, list):
            serializable[k] = [str(x) if not isinstance(x, (str, int, float)) else x for x in v]
        else:
            serializable[k] = v

    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(serializable, f, indent=2, ensure_ascii=False, default=str)
    _ok(f"Métricas salvas → {metrics_path}")


def cmd_analyze(args: argparse.Namespace) -> None:
    """Build + métricas + detecção de buracos ontológicos."""
    _header("ANALYZE — Análise Completa do Grafo")
    output_dir = getattr(args, 'output', 'data/graphs')
    g = _ensure_graph(output_dir)

    # Métricas
    m = g.compute_metrics()
    print(f"\n  📊 Resumo: {m['nodes']} nós | {m['edges']} arestas | "
          f"densidade={m['density']:.4f} | diâmetro={m.get('diameter', 'N/A')}")

    # Detecção de buracos
    _header("DETECÇÃO DE BURACOS ONTOLÓGICOS")
    gaps = g.detect_concept_gaps()

    if not gaps:
        _ok("Nenhum buraco ontológico detectado!")
    else:
        print(f"\n  ⚠️  {len(gaps)} potenciais buracos/irregularidades encontrados:\n")

        by_severity = {}
        for gap in gaps:
            sev = gap.get('severity', 'unknown')
            by_severity.setdefault(sev, []).append(gap)

        for sev in ['high', 'medium', 'low']:
            if sev not in by_severity:
                continue
            emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[sev]
            print(f"  {emoji} Severidade: {sev.upper()} ({len(by_severity[sev])} ocorrências)")
            print(f"  {'─' * 50}")
            for gap in by_severity[sev][:10]:  # Limitar output
                node = gap['node']
                issue = gap['issue']
                detail = gap.get('detail', '')
                if detail:
                    print(f"    • {node}: {issue} — {detail}")
                else:
                    print(f"    • {node}: {issue}")
            if len(by_severity[sev]) > 10:
                print(f"    ... e mais {len(by_severity[sev]) - 10}")
            print()

    # Resumo por domínio
    _header("DISTRIBUIÇÃO POR DOMÍNIO")
    domain_nodes: dict[str, int] = {}
    for uid in g.registry:
        dom = g.registry[uid].get('dominio', '???')
        domain_nodes[dom] = domain_nodes.get(dom, 0) + 1

    for dom in sorted(domain_nodes.keys()):
        count = domain_nodes[dom]
        expected = 9
        status = "✅" if count == expected else "⚠️"
        print(f"  {status} {dom:<20s} {count}/{expected} células")


def cmd_walk(args: argparse.Namespace) -> None:
    """Passeio semântico pelo grafo."""
    _header("WALK — Passeio Semântico")
    g = OntologyGraph()
    g.load_registry()
    g.build_graph()

    start = args.start
    steps = args.steps
    strategy = args.strategy

    if start not in g.G:
        print(f"\n  ❌ Nó '{start}' não encontrado no grafo.")
        print(f"  Dica: use 'python tools/graph_builder.py metrics' para ver os nós disponíveis.")
        sys.exit(1)

    print(f"\n  🚶 Passeio semântico: {start}")
    print(f"  Estratégia: {strategy} | Passos: {steps}\n")

    path = g.semantic_walk(start, steps=steps, strategy=strategy,
                            allow_negative=args.allow_negative,
                            allow_revisit=args.allow_revisit)

    for i, step in enumerate(path):
        prefix = "  🏁" if i == 0 else "  ➡️ "
        node_id = step['node_id']
        nome = step.get('nome', node_id)
        nivel = g._node_index.get(node_id, {}).get('nivel', '?')

        if i > 0:
            tipo = step.get('tipo_aresta', '')
            peso = step.get('peso', 0)
            print(f"{prefix} [{nivel}] {nome}  (via {tipo}, peso={peso:+.2f})  [{node_id}]")
        else:
            print(f"{prefix} [{nivel}] {nome}  [{node_id}]")

    # Mostrar vizinhos do último nó
    last = path[-1]['node_id']
    neighbors = g.query_neighbors(last, depth=2)
    if neighbors:
        print(f"\n  🔍 Vizinhos de '{last}' (profundidade 2):")
        for nb in neighbors[:5]:
            nb_label = g._node_index.get(nb['target'], {}).get('nome', nb['target'])
            print(f"     → {nb_label} ({nb['tipo']}, peso={nb['peso']:+.2f})")


def cmd_paths(args: argparse.Namespace) -> None:
    """Encontra caminhos entre dois nós."""
    _header("PATHS — Caminhos Semânticos")
    g = OntologyGraph()
    g.load_registry()
    g.build_graph()

    source = args.source
    target = args.target
    max_len = args.max_length

    if source not in g.G:
        print(f"\n  ❌ Nó de origem '{source}' não encontrado.")
        sys.exit(1)
    if target not in g.G:
        print(f"\n  ❌ Nó de destino '{target}' não encontrado.")
        sys.exit(1)

    print(f"\n  🔗 Caminhos de {source} → {target} (máx. {max_len} passos)\n")

    paths = g.infer_paths(source, target, max_length=max_len)

    if not paths:
        print("  Nenhum caminho encontrado.")
    else:
        # Ordenar por peso total (mais positivo primeiro)
        paths_sorted = sorted(paths, key=lambda p: p['total_weight'], reverse=True)

        for i, p in enumerate(paths_sorted[:10], 1):
            path_nodes = p['path']
            readable = []
            for nid in path_nodes:
                label = g._node_index.get(nid, {}).get('nome', nid)
                nivel = g._node_index.get(nid, {}).get('nivel', '?')
                readable.append(f"[{nivel}]{label}")

            print(f"  Caminho {i:>2}: {' → '.join(readable)}")
            print(f"           comprimento={p['length']}  peso_total={p['total_weight']:+.4f}\n")


def cmd_validate(args: argparse.Namespace) -> None:
    """Valida a integridade do grafo."""
    _header("VALIDATE — Validação do Grafo")
    g = OntologyGraph()
    g.load_registry()
    g.build_graph()

    errors = []
    warnings = []

    # 1. Verificar contagem de nós
    n4_count = sum(1 for _, d in g.G.nodes(data=True) if d.get('nivel') == 4)
    if n4_count != 162:
        errors.append(f"Esperados 162 nós N4, encontrados {n4_count}")
    else:
        _ok(f"162 nós N4 presentes (células)")

    n3_count = sum(1 for _, d in g.G.nodes(data=True) if d.get('nivel') == 3)
    if n3_count != 54:
        errors.append(f"Esperados 54 nós N3, encontrados {n3_count}")
    else:
        _ok(f"54 nós N3 presentes (subárvores)")

    n2_count = sum(1 for _, d in g.G.nodes(data=True) if d.get('nivel') == 2)
    if n2_count != 18:
        errors.append(f"Esperados 18 nós N2, encontrados {n2_count}")
    else:
        _ok(f"18 nós N2 presentes (domínios)")

    n1_count = sum(1 for _, d in g.G.nodes(data=True) if d.get('nivel') == 1)
    if n1_count != 6:
        errors.append(f"Esperados 6 nós N1, encontrados {n1_count}")
    else:
        _ok(f"6 nós N1 presentes (pilares)")

    n0_count = sum(1 for _, d in g.G.nodes(data=True) if d.get('nivel') == 0)
    if n0_count != 2:
        errors.append(f"Esperados 2 nós N0, encontrados {n0_count}")
    else:
        _ok(f"2 nós N0 presentes (eixos)")

    total_expected = 2 + 6 + 18 + 54 + 162
    total = g.G.number_of_nodes()
    if total < total_expected:
        errors.append(f"Total de nós: {total}, esperado pelo menos {total_expected}")
    else:
        _ok(f"Total de nós: {total} (≥{total_expected})")

    # 2. Verificar arestas hierárquicas
    hier_edges = [(u, v, d) for u, v, d in g.G.edges(data=True)
                  if d.get('tipo') == 'hierarquia']
    _info(f"Arestas hierárquicas: {len(hier_edges)}")

    # 3. Verificar arestas relacionais
    rel_edges = [(u, v, d) for u, v, d in g.G.edges(data=True)
                 if d.get('tipo') != 'hierarquia']
    _info(f"Arestas relacionais/oposição: {len(rel_edges)}")

    # 4. Verificar nós N4 sem arestas de saída (além de hierarquia)
    isolated_n4 = []
    for node, data in g.G.nodes(data=True):
        if data.get('nivel') != 4:
            continue
        non_hier_out = [(u, v, d) for u, v, d in g.G.out_edges(node, data=True)
                        if d.get('tipo') != 'hierarquia']
        if not non_hier_out:
            isolated_n4.append(node)

    if isolated_n4:
        _warn(f"{len(isolated_n4)} células N4 sem relações não-hierárquicas")
    else:
        _ok("Todas as células N4 possuem relações tipadas")

    # 5. Verificar consistência de opostos
    opp_errors = 0
    for uid, data in g.registry.items():
        for opp in data.get('opostos', []):
            if opp not in g.registry:
                opp_errors += 1
    if opp_errors:
        errors.append(f"{opp_errors} referências de opostos apontam para UIDs inexistentes")
    else:
        _ok("Todas as referências de opostos são válidas")

    # Resultado
    print()
    if errors:
        print(f"  ❌ {len(errors)} ERRO(S) DE VALIDAÇÃO:")
        for e in errors:
            print(f"     • {e}")
    else:
        _ok("Todas as validações passaram!")

    if warnings:
        print(f"\n  ⚠️  {len(warnings)} AVISO(S):")
        for w in warnings:
            print(f"     • {w}")


# ---------------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Graph Builder CLI — Motor de Grafo Ontológico (FASE 3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python tools/graph_builder.py build
  python tools/graph_builder.py metrics
  python tools/graph_builder.py analyze
  python tools/graph_builder.py walk --start N4_ALGORITMIA_1_A --steps 5
  python tools/graph_builder.py paths --source N4_ALGORITMIA_1_A --target N4_BIOS_1_A
  python tools/graph_builder.py validate
        """,
    )

    parser.add_argument(
        '--output', '-o',
        default='data/graphs',
        help='Diretório de saída para exports (padrão: data/graphs)',
    )

    sub = parser.add_subparsers(dest='command', required=True)

    # build
    sub.add_parser('build', help='Constrói o grafo e exporta para GEXF/JSON')

    # metrics
    sub.add_parser('metrics', help='Calcula e exibe métricas topológicas')

    # analyze
    sub.add_parser('analyze', help='Build + métricas + detecção de buracos')

    # walk
    p_walk = sub.add_parser('walk', help='Passeio semântico pelo grafo')
    p_walk.add_argument('--start', '-s', required=True,
                        help='Nó de início (ex: N4_ALGORITMIA_1_A)')
    p_walk.add_argument('--steps', type=int, default=3,
                        help='Número de passos (padrão: 3)')
    p_walk.add_argument('--strategy', choices=['weighted', 'positive', 'negative', 'random'],
                        default='weighted', help='Estratégia de seleção (padrão: weighted)')
    p_walk.add_argument('--allow-negative', action='store_true',
                        help='Permitir arestas com peso negativo')
    p_walk.add_argument('--allow-revisit', action='store_true',
                        help='Permitir revisitar nós')

    # paths
    p_paths = sub.add_parser('paths', help='Encontra caminhos entre dois nós')
    p_paths.add_argument('--source', required=True,
                         help='Nó de origem')
    p_paths.add_argument('--target', required=True,
                         help='Nó de destino')
    p_paths.add_argument('--max-length', type=int, default=5,
                         help='Comprimento máximo do caminho (padrão: 5)')

    # validate
    sub.add_parser('validate', help='Valida integridade do grafo')

    args = parser.parse_args()

    commands = {
        'build': cmd_build,
        'metrics': cmd_metrics,
        'analyze': cmd_analyze,
        'walk': cmd_walk,
        'paths': cmd_paths,
        'validate': cmd_validate,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
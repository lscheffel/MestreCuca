#!/usr/bin/env python3
"""
Motor de Grafo Ontológico — FASE 3

Constrói o grafo semântico fractal a partir dos 162 JSONs enriquecidos,
com nós hierárquicos N0–N4, arestas tipadas, métricas topológicas
e exportação para visualização.
"""

from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from typing import Any, Optional

import networkx as nx

# ---------------------------------------------------------------------------
# Mapeamentos ontológicos derivados da especificação
# ---------------------------------------------------------------------------

AXES = {
    "SINTRÓPICO": {"code": "0.1", "pillars": ["LOGOS", "BIOS", "PATHOS"]},
    "ENTRÓPICO":  {"code": "0.2", "pillars": ["KHAOS", "APEIRON", "MYTHOS"]},
}

PILLAR_META = {
    "LOGOS":     {"code": "L1", "axis": "SINTRÓPICO"},
    "BIOS":      {"code": "B2", "axis": "SINTRÓPICO"},
    "PATHOS":    {"code": "P3", "axis": "SINTRÓPICO"},
    "KHAOS":     {"code": "K4", "axis": "ENTRÓPICO"},
    "APEIRON":   {"code": "A5", "axis": "ENTRÓPICO"},
    "MYTHOS":    {"code": "M6", "axis": "ENTRÓPICO"},
}

# Domínios N2 por pilar (ordem fixa)
PILLAR_DOMAINS: dict[str, list[str]] = {
    "LOGOS":     ["ALGORITMIA", "NOMOS",     "MECÂNICA"],
    "BIOS":      ["OIKOS",      "SOMA",      "METABOLISMO"],
    "PATHOS":    ["ETHOS",      "ALTERIDADE","ESTÉTICA"],
    "KHAOS":     ["ENTROPIA",   "SINGULARIDADE", "SÍNTESE"],
    "APEIRON":   ["ESCALA",     "VIBRATIO",  "VÁCUO"],
    "MYTHOS":    ["ARQUÉTIPO",  "NARRATIVA", "MISTÉRIO"],
}

# Subárvores N3 por domínio (ordem fixa)
DOMAIN_SUBTREES: dict[str, list[str]] = {
    "ALGORITMIA":   ["RESOLUÇÃO", "OTIMIZAÇÃO", "VALIDAÇÃO"],
    "NOMOS":        ["LEGISLAÇÃO", "CONTORNO", "PACTO"],
    "MECÂNICA":     ["ESTATICA", "DINAMICA", "TERMOTRANSDINÂMICA"],
    "OIKOS":        ["MORADA", "TERRITORIO", "PROVISAO"],
    "SOMA":         ["INTEGRIDADE", "VITALIDADE", "HOMEOSTASE"],
    "METABOLISMO":  ["ANABOLISMO", "CATABOLISMO", "CICLO"],
    "ETHOS":        ["VALORES", "VIRTUDE", "RESPONSABILIDADE"],
    "ALTERIDADE":   ["RECONHECIMENTO", "EMPATIA", "DIALOGO"],
    "ESTÉTICA":     ["HARMONIA", "EXPRESSAO", "IMPACTO"],
    "ENTROPIA":     ["DEGRADAÇÃO", "DISSIPAÇÃO", "CAOS"],
    "SINGULARIDADE": ["EXCEPCAO", "INFINITO", "TRANSFORMAÇÃO"],
    "SÍNTESE":      ["FUSÃO", "HIBRIDISMO", "TRANSCENDENCIA"],
    "ESCALA":       ["PROPORÇÃO", "MAGNITUDE", "LEI"],
    "VIBRATIO":     ["FREQUENCIA", "RESONÂNCIA", "ONDA"],
    "VÁCUO":        ["POTENCIAL", "SILÊNCIO", "CAMPO"],
    "ARQUÉTIPO":    ["PADRAO_PRIMORDIAL", "COMPORTAMENTO", "SÍMBOLO"],
    "NARRATIVA":    ["TEIA", "LINHA_SENTIDO", "HISTÓRIA_VIVIDA"],
    "MISTÉRIO":     ["INCOMPREENSÃO", "INTUIÇÃO", "REVELAÇÃO"],
}

# Números de subárvores e células por domínio
NUM_SUBTREES = 3
NUM_CELLS = 3


class OntologyGraph:
    """Grafo semântico direcionado da ontologia fractal.

    Estrutura:
        N0 (2 eixos) → N1 (6 pilares) → N2 (18 domínios) →
        N3 (54 subárvores) → N4 (162 células)

    Arestas:
        - Hierárquicas: pai→filho com peso 1.0
        - Relacionais: entre N4s (depende_de, complementa, contrasta, etc.)
        - Opostos: entre N4s com tipo 'contrasta' e peso negativo
    """

    def __init__(self, json_dir: str = "data/json"):
        self.G = nx.DiGraph()
        self.json_dir = json_dir
        self.registry: dict[str, dict] = {}
        self._node_index: dict[str, dict] = {}  # cache de metadados de nós

    # ------------------------------------------------------------------
    # Carga de dados
    # ------------------------------------------------------------------

    def load_registry(self) -> int:
        """Carrega todos os JSONs de data/json/ no registry.

        Returns:
            Número de células carregadas.
        """
        loaded = 0
        for f in sorted(os.listdir(self.json_dir)):
            if f.endswith('.json') and f.startswith('N4_'):
                fpath = os.path.join(self.json_dir, f)
                with open(fpath, 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                    uid = data['uid']
                    self.registry[uid] = data
                    loaded += 1
        return loaded

    # ------------------------------------------------------------------
    # Construção do grafo
    # ------------------------------------------------------------------

    def build_graph(self) -> None:
        """Constrói o grafo completo em 4 etapas:

        1. Nós hierárquicos N0, N1, N2, N3
        2. Nós N4 (células) a partir dos JSONs
        3. Arestas hierárquicas N0→N1→N2→N3→N4
        4. Arestas relacionais e de oposição entre N4s
        """
        self._add_hierarchy_nodes()
        self._add_hierarchy_edges()
        self._add_relation_edges()
        self._add_opposition_edges()
        self._add_implicit_relations()

    def _add_hierarchy_nodes(self) -> None:
        """Adiciona nós N0, N1, N2, N3 da hierarquia."""
        # --- N0: Eixos ---
        for axis_name, axis_info in AXES.items():
            node_id = f"N0_{axis_name}"
            self.G.add_node(node_id,
                           nivel=0,
                           nome=axis_name,
                           code=axis_info["code"],
                           type="axis",
                           label=axis_name)
            self._node_index[node_id] = {
                "nivel": 0, "nome": axis_name, "code": axis_info["code"]
            }

        # --- N1: Pilares ---
        for axis_name, axis_info in AXES.items():
            for pillar in axis_info["pillars"]:
                meta = PILLAR_META[pillar]
                node_id = f"N1_{pillar}"
                self.G.add_node(node_id,
                               nivel=1,
                               nome=pillar,
                               code=meta["code"],
                               type="pillar",
                               axis=axis_name,
                               label=pillar)
                self._node_index[node_id] = {
                    "nivel": 1, "nome": pillar, "code": meta["code"],
                    "axis": axis_name,
                }

        # --- N2: Domínios ---
        domain_code_index: dict[str, int] = defaultdict(int)
        for pillar, domains in PILLAR_DOMAINS.items():
            for dom in domains:
                domain_code_index[dom] += 1
                code_num = domain_code_index[dom]
                node_id = f"N2_{dom}"
                self.G.add_node(node_id,
                               nivel=2,
                               nome=dom,
                               code=f"{dom}",
                               type="domain",
                               pillar=pillar,
                               domain_num=code_num,
                               label=dom)
                self._node_index[node_id] = {
                    "nivel": 2, "nome": dom, "pillar": pillar,
                }

        # --- N3: Subárvores ---
        subtree_index: dict[str, int] = defaultdict(int)
        for dom, subtrees in DOMAIN_SUBTREES.items():
            for st in subtrees:
                subtree_index[st] += 1
                node_id = f"N3_{st}"
                n3_ref = f"{dom}-{st}"
                self.G.add_node(node_id,
                               nivel=3,
                               nome=st,
                               code=n3_ref,
                               type="subtree",
                               dominio=dom,
                               n3_ref=n3_ref,
                               label=st)
                self._node_index[node_id] = {
                    "nivel": 3, "nome": st, "dominio": dom,
                    "n3_ref": n3_ref,
                }

        # --- N4: Células (folhas) ---
        for uid, data in self.registry.items():
            n4_attrs = {
                "nivel": 4,
                "nome": data.get("nome", ""),
                "nome_normalizado": data.get("nome_normalizado", ""),
                "uid": uid,
                "legacy_id": data.get("legacy_id", ""),
                "path": data.get("path", ""),
                "hierarchical_id": data.get("hierarchical_id", ""),
                "pilar": data.get("pilar", ""),
                "dominio": data.get("dominio", ""),
                "n3_ref": data.get("n3_ref", ""),
                "n3_name": data.get("n3_name", ""),
                "axis": data.get("axis", ""),
                "natureza": data.get("natureza", ""),
                "type": "cell",
                "label": data.get("nome", uid),
                "gatilho": data.get("gatilho", ""),
                "acao": data.get("acao", ""),
                "restricao": data.get("restricao", ""),
                "verificacao": data.get("verificacao", ""),
            }
            # Incluir assinatura semântica como atributos flat
            sig = data.get("assinatura_semantica", {})
            if isinstance(sig, dict):
                for k, v in sig.items():
                    n4_attrs[f"sig_{k}"] = v

            self.G.add_node(uid, **n4_attrs)
            self._node_index[uid] = n4_attrs

    def _add_hierarchy_edges(self) -> None:
        """Arestas hierárquicas com peso 1.0: N0→N1→N2→N3→N4."""
        # N0 → N1
        for axis_name, axis_info in AXES.items():
            n0_id = f"N0_{axis_name}"
            for pillar in axis_info["pillars"]:
                n1_id = f"N1_{pillar}"
                self.G.add_edge(n0_id, n1_id,
                               tipo="hierarquia",
                               peso=1.0,
                               label="contém")

        # N1 → N2
        for pillar, domains in PILLAR_DOMAINS.items():
            n1_id = f"N1_{pillar}"
            for dom in domains:
                n2_id = f"N2_{dom}"
                self.G.add_edge(n1_id, n2_id,
                               tipo="hierarquia",
                               peso=1.0,
                               label="contém")

        # N2 → N3
        for dom, subtrees in DOMAIN_SUBTREES.items():
            n2_id = f"N2_{dom}"
            for st in subtrees:
                n3_id = f"N3_{st}"
                self.G.add_edge(n2_id, n3_id,
                               tipo="hierarquia",
                               peso=1.0,
                               label="contém")

        # N3 → N4
        for uid, data in self.registry.items():
            n3_ref = data.get("n3_ref", "")
            n3_name = data.get("n3_name", "")
            n3_id = f"N3_{n3_name}"
            if n3_id in self.G:
                self.G.add_edge(n3_id, uid,
                               tipo="hierarquia",
                               peso=1.0,
                               label="instancia")

    def _add_relation_edges(self) -> None:
        """Arestas de relação tipada entre N4s (campo 'relacoes')."""
        for uid, data in self.registry.items():
            for rel in data.get('relacoes', []):
                target = rel.get('alvo')
                if target and target in self.registry:
                    self.G.add_edge(
                        uid, target,
                        tipo=rel.get('tipo', 'relaciona'),
                        peso=rel.get('peso', 0.5),
                        label=rel.get('tipo', 'relaciona'),
                    )

    def _add_opposition_edges(self) -> None:
        """Arestas de oposição entre N4s (campo 'opostos')."""
        for uid, data in self.registry.items():
            for opp in data.get('opostos', []):
                if opp in self.registry:
                    self.G.add_edge(
                        uid, opp,
                        tipo='contrasta',
                        peso=-0.7,
                        label='contrasta',
                    )

    def _add_implicit_relations(self) -> None:
        """Inferência de relações implícitas baseada na estrutura hierárquica.

        Regras:
        - Células irmãs (mesmo N3) → complementa (peso 0.5)
        - Domínios anteriores no mesmo pilar → depende_de (peso 0.6)
        - Generalização do 1º domínio sobre os demais (peso 0.4)
        """
        from collections import defaultdict

        # Agrupar células por N3
        by_n3: dict[str, list[str]] = defaultdict(list)
        for uid, data in self.registry.items():
            n3 = data.get('n3_ref', '')
            if n3:
                by_n3[n3].append(uid)

        # Agrupar células por (pilar, dominio)
        by_pillar_domain: dict[tuple[str, str], list[str]] = defaultdict(list)
        for uid, data in self.registry.items():
            p = data.get('pilar', '')
            d = data.get('dominio', '')
            if p and d:
                by_pillar_domain[(p, d)].append(uid)

        # Domínios ordenados por pilar
        pillar_domain_order: dict[str, dict[str, int]] = {}
        for pillar, domains in PILLAR_DOMAINS.items():
            pillar_domain_order[pillar] = {d: i for i, d in enumerate(domains)}

        added = 0
        for uid, data in self.registry.items():
            n3 = data.get('n3_ref', '')
            pilar = data.get('pilar', '')
            dominio = data.get('dominio', '')

            # 1. Irmãs no mesmo N3 → complementa
            siblings = by_n3.get(n3, [])
            for sib in siblings:
                if sib != uid and not self.G.has_edge(uid, sib):
                    self.G.add_edge(uid, sib,
                                    tipo='complementa',
                                    peso=0.5,
                                    label='complementa',
                                    _implicit=True)
                    added += 1

            # 2. Dependência de domínios anteriores
            pidx = pillar_domain_order.get(pilar, {}).get(dominio, -1)
            if pidx > 0:
                prev_dom = PILLAR_DOMAINS[pilar][pidx - 1]
                prev_cells = by_pillar_domain.get((pilar, prev_dom), [])
                for pc in prev_cells:
                    if pc != uid and not self.G.has_edge(uid, pc):
                        self.G.add_edge(uid, pc,
                                        tipo='depende_de',
                                        peso=0.6,
                                        label='depende_de',
                                        _implicit=True)
                        added += 1

            # 3. Generalização do 1º domínio
            if pidx > 0:
                first_dom = PILLAR_DOMAINS[pilar][0]
                first_cells = by_pillar_domain.get((pilar, first_dom), [])
                for fc in first_cells:
                    if fc != uid and not self.G.has_edge(uid, fc):
                        self.G.add_edge(uid, fc,
                                        tipo='generaliza',
                                        peso=0.4,
                                        label='generaliza',
                                        _implicit=True)
                        added += 1

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------

    def query_neighbors(self, node_id: str,
                        relation_type: Optional[str] = None,
                        depth: int = 1) -> list[dict]:
        """Consulta vizinhos com filtro opcional por tipo de relação.

        Args:
            node_id: ID do nó de origem.
            relation_type: Se informado, filtra por tipo de aresta.
            depth: Profundidade da busca (padrão 1 = vizinhos diretos).

        Returns:
            Lista de dicts com target, tipo, peso e dados do nó.
        """
        if node_id not in self.G:
            return []

        results = []
        seen = set()

        if depth == 1:
            edges = self.G.edges(node_id, data=True)
        else:
            # BFS até a profundidade solicitada
            edges = []
            frontier = [(node_id, 0)]
            visited = {node_id}
            while frontier:
                current, d = frontier.pop(0)
                if d >= depth:
                    continue
                for u, v, data in self.G.edges(current, data=True):
                    edges.append((u, v, data))
                    if v not in visited:
                        visited.add(v)
                        frontier.append((v, d + 1))

        for u, v, data in edges:
            if relation_type and data.get('tipo') != relation_type:
                continue
            if v in seen:
                continue
            seen.add(v)
            node_data = self._node_index.get(v, {})
            results.append({
                'target': v,
                'tipo': data.get('tipo', ''),
                'peso': data.get('peso', 0),
                'node_data': node_data,
            })

        return sorted(results, key=lambda x: abs(x['peso']), reverse=True)

    def semantic_walk(self, start_node: str, steps: int = 3,
                      strategy: str = "weighted",
                      allow_negative: bool = False,
                      allow_revisit: bool = False) -> list[dict]:
        """Passeio semântico pelo grafo.

        Estratégias:
            weighted: escolhe vizinho com maior peso absoluto
            positive: apenas arestas com peso > 0
            negative: apenas arestas com peso < 0
            random: vizinho aleatório

        Args:
            start_node: ID do nó de partida.
            steps: Número máximo de passos.
            strategy: Estratégia de seleção do próximo nó.
            allow_negative: Se False, filtra arestas com peso < 0 (default).
            allow_revisit: Se True, permite visitar nós já percorridos.

        Returns:
            Lista de dicts com node_id, nome, tipo_aresta, peso a cada passo.
        """
        import random

        if start_node not in self.G:
            return []

        path = [{'node_id': start_node,
                 'nome': self._node_index.get(start_node, {}).get('nome', start_node),
                 'step': 0}]
        current = start_node
        visited: set[str] = {start_node}

        for step in range(1, steps + 1):
            neighbors = self.query_neighbors(current)
            if not neighbors:
                break

            # Filtrar arestas negativas se não permitidas
            if not allow_negative:
                candidates = [n for n in neighbors if n['peso'] >= 0]
            else:
                candidates = list(neighbors)

            if not candidates:
                break

            # Remover nós já visitados (evita loops)
            if not allow_revisit:
                candidates = [n for n in candidates if n['target'] not in visited]
                if not candidates:
                    break

            # Selecionar próximo nó pela estratégia
            if strategy == "positive":
                next_node = max(candidates, key=lambda x: x['peso'])
            elif strategy == "negative":
                next_node = min(candidates, key=lambda x: x['peso'])
            elif strategy == "random":
                next_node = random.choice(candidates)
            else:  # weighted
                next_node = max(candidates, key=lambda x: abs(x['peso']))

            current = next_node['target']
            visited.add(current)
            path.append({
                'node_id': current,
                'nome': next_node['node_data'].get('nome', current),
                'tipo_aresta': next_node['tipo'],
                'peso': next_node['peso'],
                'step': step,
            })

        return path

    def infer_paths(self, source: str, target: str,
                    max_length: int = 5,
                    directed: bool = False) -> list[dict]:
        """Encontra todos os caminhos simples entre dois nós.

        Navega o grafo como não-dirigido por padrão (relações semânticas
        são bidirecionais), a menos que directed=True.

        Args:
            source: Nó de origem.
            target: Nó de destino.
            max_length: Comprimento máximo do caminho.
            directed: Se True, respeita direção das arestas.

        Returns:
            Lista de dicts com path, length, total_weight.
        """
        if source not in self.G or target not in self.G:
            return []

        search_graph = self.G if directed else self.G.to_undirected()

        try:
            paths = list(nx.all_simple_paths(
                search_graph, source, target, cutoff=max_length
            ))
        except nx.NetworkXNoPath:
            return []

        return [
            {
                'path': p,
                'length': len(p) - 1,
                'total_weight': round(self._path_weight(p), 4),
            }
            for p in paths
        ]

    def _path_weight(self, path: list[str]) -> float:
        """Calcula peso total de um caminho."""
        total = 0.0
        for i in range(len(path) - 1):
            edge_data = self.G.get_edge_data(path[i], path[i + 1])
            if edge_data:
                total += edge_data.get('peso', 0)
        return total

    # ------------------------------------------------------------------
    # Métricas topológicas
    # ------------------------------------------------------------------

    def compute_metrics(self) -> dict:
        """Calcula métricas topológicas do grafo.

        Returns:
            Dicionário com todas as métricas calculadas.
        """
        metrics: dict[str, Any] = {}
        n_nodes = self.G.number_of_nodes()
        n_edges = self.G.number_of_edges()

        # Contagem por nível
        level_counts = defaultdict(int)
        type_counts = defaultdict(int)
        for n, d in self.G.nodes(data=True):
            level_counts[d.get('nivel', -1)] += 1
            type_counts[d.get('type', 'unknown')] += 1

        metrics['nodes'] = n_nodes
        metrics['edges'] = n_edges
        metrics['nodes_by_level'] = dict(level_counts)
        metrics['nodes_by_type'] = dict(type_counts)

        # --- Centralidades ---
        metrics['degree_centrality'] = nx.degree_centrality(self.G)
        metrics['in_degree_centrality'] = nx.in_degree_centrality(self.G)
        metrics['out_degree_centrality'] = nx.out_degree_centrality(self.G)
        metrics['betweenness_centrality'] = nx.betweenness_centrality(self.G)
        metrics['closeness_centrality'] = nx.closeness_centrality(self.G)

        try:
            metrics['eigenvector_centrality'] = nx.eigenvector_centrality(
                self.G.to_undirected(), max_iter=2000
            )
        except Exception:
            metrics['eigenvector_centrality'] = {}

        # --- Densidade ---
        metrics['density'] = nx.density(self.G)

        # --- Clustering ---
        undirected = self.G.to_undirected()
        metrics['clustering_coefficient'] = nx.clustering(undirected)
        metrics['avg_clustering'] = nx.average_clustering(undirected)

        # --- Pontes e articulações ---
        metrics['bridges'] = list(nx.bridges(undirected))
        metrics['articulation_points'] = list(nx.articulation_points(undirected))

        # --- Componentes ---
        metrics['weakly_connected_components'] = [
            list(c) for c in nx.weakly_connected_components(self.G)
        ]
        metrics['num_weakly_components'] = len(metrics['weakly_connected_components'])
        metrics['strongly_connected_components'] = [
            list(c) for c in nx.strongly_connected_components(self.G)
        ]
        metrics['num_strongly_components'] = len(metrics['strongly_connected_components'])

        # --- Isolados ---
        metrics['isolates'] = list(nx.isolates(self.G))

        # --- Diâmetro e caminho médio (grafo não-dirigido) ---
        if nx.is_connected(undirected):
            metrics['diameter'] = nx.diameter(undirected)
            metrics['average_shortest_path_length'] = nx.average_shortest_path_length(undirected)
        else:
            # Usar maior componente
            largest_cc = max(nx.connected_components(undirected), key=len)
            subgraph = undirected.subgraph(largest_cc)
            metrics['diameter'] = nx.diameter(subgraph)
            metrics['average_shortest_path_length'] = nx.average_shortest_path_length(subgraph)
            metrics['largest_component_size'] = len(largest_cc)

        # --- Assortatividade ---
        metrics['degree_assortativity'] = nx.degree_assortativity_coefficient(self.G)

        # --- Top 10 rankings ---
        bc = metrics['betweenness_centrality']
        metrics['top_betweenness'] = sorted(
            bc.items(), key=lambda x: x[1], reverse=True
        )[:10]

        dc = metrics['degree_centrality']
        metrics['top_degree'] = sorted(
            dc.items(), key=lambda x: x[1], reverse=True
        )[:10]

        ec = metrics.get('eigenvector_centrality', {})
        if ec:
            metrics['top_eigenvector'] = sorted(
                ec.items(), key=lambda x: x[1], reverse=True
            )[:10]

        # --- Estatísticas de arestas por tipo ---
        edge_types: dict[str, int] = defaultdict(int)
        edge_weights: dict[str, list[float]] = defaultdict(list)
        for u, v, d in self.G.edges(data=True):
            t = d.get('tipo', 'unknown')
            edge_types[t] += 1
            w = d.get('peso', 0)
            edge_weights[t].append(w)

        metrics['edge_types'] = dict(edge_types)
        metrics['edge_weight_stats'] = {
            t: {
                'count': len(ws),
                'mean': round(sum(ws) / len(ws), 4) if ws else 0,
                'min': round(min(ws), 4) if ws else 0,
                'max': round(max(ws), 4) if ws else 0,
            }
            for t, ws in edge_weights.items()
        }

        return metrics

    # ------------------------------------------------------------------
    # Detecção de buracos ontológicos
    # ------------------------------------------------------------------

    def detect_concept_gaps(self) -> list[dict]:
        """Detecta buracos e anomalias ontológicas.

        Verifica:
        - Nós N4 com grau muito baixo (isolados ou pouco conectados)
        - Domínios/subárvores sub-representados
        - Assinaturas semânticas atípicas
        - Relações declaradas com alvos ausentes
        """
        gaps: list[dict] = []

        # 1. Nós N4 com grau total <= 1
        for node, data in self.G.nodes(data=True):
            if data.get('nivel') != 4:
                continue
            deg = self.G.degree(node)
            if deg <= 1:
                gaps.append({
                    'node': node,
                    'issue': 'low_connectivity',
                    'degree': deg,
                    'severity': 'high' if deg == 0 else 'medium',
                })

        # 2. Domínios com contagem anômala de células
        domain_counts: dict[str, int] = defaultdict(int)
        for uid, data in self.registry.items():
            dom = data.get('dominio', '')
            if dom:
                domain_counts[dom] += 1

        expected = 9  # 3 subtrees × 3 cells
        for dom, count in domain_counts.items():
            if count < expected:
                gaps.append({
                    'node': f"N2_{dom}",
                    'issue': 'underrepresented_domain',
                    'expected': expected,
                    'actual': count,
                    'severity': 'medium',
                })

        # 3. Células com opostos declarados mas sem aresta correspondente
        for uid, data in self.registry.items():
            for opp_uid in data.get('opostos', []):
                if opp_uid not in self.registry:
                    gaps.append({
                        'node': uid,
                        'issue': 'opposite_target_missing',
                        'missing_target': opp_uid,
                        'severity': 'high',
                    })
                elif not self.G.has_edge(uid, opp_uid):
                    gaps.append({
                        'node': uid,
                        'issue': 'opposite_edge_missing',
                        'missing_target': opp_uid,
                        'severity': 'low',
                    })

        # 4. Células sem assinatura semântica completa
        for uid, data in self.registry.items():
            sig = data.get('assinatura_semantica', {})
            if isinstance(sig, dict) and len(sig) < 9:
                gaps.append({
                    'node': uid,
                    'issue': 'incomplete_signature',
                    'dimensions_present': len(sig),
                    'severity': 'low',
                })

        return gaps

    # ------------------------------------------------------------------
    # Exportação
    # ------------------------------------------------------------------

    def export_gexf(self, path: str) -> None:
        """Exporta o grafo para formato GEXF (Gephi)."""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        nx.write_gexf(self.G, path)

    def export_graphviz(self, path: str) -> None:
        """Exporta para formato DOT (Graphviz)."""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        try:
            from networkx.drawing.nx_agraph import write_dot
            write_dot(self.G, path)
        except ImportError:
            # Fallback para pydot
            from networkx.drawing.nx_pydot import write_dot
            write_dot(self.G, path)

    def export_json(self, path: str) -> None:
        """Exporta o grafo como JSON (node_link_data)."""
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        data = nx.node_link_data(self.G)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def to_json(self) -> dict:
        """Retorna representação JSON serializável do grafo."""
        return nx.node_link_data(self.G)

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------

    def get_hierarchy(self) -> dict[str, list[str]]:
        """Retorna a hierarquia completa N0→N1→N2→N3→N4."""
        hierarchy: dict[str, list[str]] = {}
        for n0 in [f"N0_{a}" for a in AXES]:
            children = list(self.G.successors(n0))
            hierarchy[n0] = []
            for n1 in children:
                n1_children = list(self.G.successors(n1))
                hierarchy[n0].extend(n1_children)
                for n2 in n1_children:
                    n2_children = list(self.G.successors(n2))
                    hierarchy[n0].extend(n2_children)
                    for n3 in n2_children:
                        n3_children = list(self.G.successors(n3))
                        hierarchy[n0].extend(n3_children)
        return hierarchy

    def summary(self) -> str:
        """Retorna resumo textual do grafo."""
        m = self.compute_metrics()
        lines = [
            "=" * 60,
            "GRAFO ONTOLÓGICO — RESUMO",
            "=" * 60,
            f"  Nós: {m['nodes']}",
            f"  Arestas: {m['edges']}",
            f"  Densidade: {m['density']:.4f}",
            f"  Diâmetro: {m.get('diameter', 'N/A')}",
            f"  Caminho médio: {m.get('average_shortest_path_length', 'N/A'):.4f}",
            f"  Clustering médio: {m['avg_clustering']:.4f}",
            f"  Componentes fracos: {m['num_weakly_components']}",
            f"  Componentes fortes: {m['num_strongly_components']}",
            f"  Pontes: {len(m['bridges'])}",
            f"  Articulações: {len(m['articulation_points'])}",
            f"  Isolados: {len(m['isolates'])}",
            "",
            "  Nós por nível:",
        ]
        for level in sorted(m['nodes_by_level'].keys()):
            lines.append(f"    N{level}: {m['nodes_by_level'][level]}")

        lines.append("")
        lines.append("  Tipos de aresta:")
        for t, count in sorted(m['edge_types'].items(), key=lambda x: -x[1]):
            lines.append(f"    {t}: {count}")

        lines.append("")
        lines.append("  Top 10 Betweenness Centrality:")
        for node, score in m['top_betweenness']:
            label = self._node_index.get(node, {}).get('nome', node)
            lines.append(f"    {label} ({node}): {score:.4f}")

        lines.append("")
        lines.append("  Top 10 Degree Centrality:")
        for node, score in m['top_degree']:
            label = self._node_index.get(node, {}).get('nome', node)
            lines.append(f"    {label} ({node}): {score:.4f}")

        lines.append("=" * 60)
        return "\n".join(lines)
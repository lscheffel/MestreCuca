# PLANO DE IMPLEMENTAÇÃO — SISTEMA COGNITIVO ONTOLÓGICO (Kilo Code)

> **Status:** ARQUITETURA DEFINIDA — Pronto para implementação faseada
> **Data:** 2026-05-09
> **Base Ontológica:** 162 células N4 (2×3×3×3×3), 54 subárvores N3, 18 domínios N2, 6 pilares N1, 2 eixos N0

---

## VISÃO GERAL DA ARQUITETURA

```
┌─────────────────────────────────────────────────────────────────┐
│                     CAMADA DE DADOS                             │
│  /data/json/  /data/embeddings/  /data/indexes/  /data/graphs/ │
├─────────────────────────────────────────────────────────────────┤
│                     CAMADA DE NÚCLEO                            │
│  /core/ontology_loader.py    — Carrega e parseia N3/N4        │
│  /core/ontology_parser.py    — Extrai metadados e hierarquia   │
│  /core/ontology_registry.py  — Registry singleton de entidades │
│  /core/semantic_engine.py    — Assinaturas e similaridade      │
│  /core/graph_engine.py       — Grafo NetworkX + métricas       │
│  /core/dialectic_engine.py   — Opostos e inferência dialética  │
│  /core/cognitive_function_engine.py — Funções cognitivas       │
│  /core/relation_engine.py    — Relações tipadas e validação    │
├─────────────────────────────────────────────────────────────────┤
│                     CAMADA DE RUNTIME                           │
│  /runtime/classifier.py      — Classificador multinível N0→N4  │
│  /runtime/router.py          — Router cognitivo por pilar      │
│  /runtime/retriever.py       — Retrieval híbrido (vec+graph)   │
│  /runtime/orchestrator.py    — Orchestrator principal           │
│  /runtime/synthesizer.py     — Montagem de prompts dinâmicos   │
│  /runtime/validator.py       — Validador de coerência          │
├─────────────────────────────────────────────────────────────────┤
│                     CAMADA DE FERRAMENTAS                      │
│  /tools/n4_builder.py              — Gera/atualiza N4 JSON     │
│  /tools/embedding_builder.py       — Gera embeddings            │
│  /tools/graph_builder.py           — Constrói grafo             │
│  /tools/relation_mapper.py         — Mapeia relações            │
│  /tools/uid_generator.py           — Gera UIDs permanentes     │
│  /tools/validator.py               — Validação offline          │
├─────────────────────────────────────────────────────────────────┤
│                     CAMADA DE CONFIGURAÇÃO                      │
│  /config/ontology.yaml       — Configuração da ontologia       │
│  /config/embedding.yaml      — Parâmetros de embedding         │
│  /config/retrieval.yaml      — Thresholds e limites            │
│  /config/graph.yaml          — Parâmetros do grafo             │
├─────────────────────────────────────────────────────────────────┤
│                     CAMADA DE PROMPTS                          │
│  /prompts/classifier/        — Templates de classificação      │
│  /prompts/retrieval/         — Templates de retrieval          │
│  /prompts/synthesis/         — Templates de síntese            │
│  /prompts/validation/        — Templates de validação          │
│  /prompts/routing/           — Templates de routing            │
└─────────────────────────────────────────────────────────────────┘
```

---

## REQUISITOS E DEPENDÊNCIAS

### Requisitos do Sistema
- **Python:** 3.10+
- **Dependências:**
  - `numpy` — operações vetoriais
  - `networkx` — grafo semântico
  - `sentence-transformers` — embeddings (ou `openai`/`ollama` como backend)
  - `pyyaml` — configuração
  - `scikit-learn` — clusterização e métricas
  - `rich` — output formatado no terminal
  - `tqdm` — progresso de processamento

### Dependências de Ordem
```
Fase 0 (diretórios) → Fase 1 (normalização) → Fase 2 (expansão semântica)
    → Fase 3 (grafo) → Fase 4 (embeddings) → Fase 5 (classificador)
    → Fase 6 (orchestrator) → Fase 7 (router) → Fase 8 (síntese)
    → Fase 9 (validador) → Fase 10 (agentes) → Fase 11 (integração)
```

### Decisão Arquitetural Crítica: Duas Fontes de ID
O projeto possui dois sistemas de ID paralelos:
1. **ID Legado (flat):** `S1.L1.1.1-A` (usado no `plano_transformacao_n4_json.md`)
2. **ID Hierárquico (reestruturar_n4.py):** `1.1.1.1` com slug do conceito

**Decisão:** Adotar **ambos** em campos separados:
- `uid` = `N4_DECOMPOSICAO` (imutável, snake_case, sem acentos) — para código
- `path` = `S1.L1.1.1-A` (estrutural, pode mudar) — para navegação
- `hierarchical_id` = `1.1.1.1` (para reconstrução de árvore)

---

## FASE 0 — ESTRUTURA DE DIRETÓRIOS E CONFIGURAÇÃO INICIAL

### 0.1 Criar Estrutura de Diretórios
```bash
mkdir -p ontology/{n0,n1,n2,n3,n4}
mkdir -p data/{json,embeddings,indexes,graphs}
mkdir -p runtime
mkdir -p core
mkdir -p prompts/{classifier,retrieval,synthesis,validation,routing}
mkdir -p config
mkdir -p tools
```

### 0.2 Criar `requirements.txt`
```
numpy>=1.24
networkx>=3.0
sentence-transformers>=2.2
pyyaml>=6.0
scikit-learn>=1.2
rich>=13.0
tqdm>=4.65
```

### 0.3 Criar `config/ontology.yaml`
```yaml
ontology:
  version: "3.0"
  geometry: "2x3x3x3x3"
  total_cells: 162
  n0_axes:
    - id: "0.1"
      name: "SINTRÓPICO"
      code: "S1"
    - id: "0.2"
      name: "ENTRÓPICO"
      code: "E2"
  n1_pillars:
    SINTRÓPICO:
      - code: "L1"
        name: "LOGOS"
      - code: "B2"
        name: "BIOS"
      - code: "P3"
        name: "PATHOS"
    ENTRÓPICO:
      - code: "K1"
        name: "KHAOS"
      - code: "A2"
        name: "APEIRON"
      - code: "M3"
        name: "MYTHOS"

paths:
  n3_dir: "ontology/n3"
  n4_dir: "ontology/n4"
  json_dir: "data/json"
  embeddings_dir: "data/embeddings"
  indexes_dir: "data/indexes"
  graphs_dir: "data/graphs"

natures:
  - processo
  - estado
  - fenomeno
  - principio
  - mecanismo
  - estrutura
  - arquétipo
  - dinamica
  - restricao
  - vetor

relation_types:
  depende_de: 1.0
  complementa: 0.8
  contrasta: -0.7
  expande: 0.6
  implementa: 0.9
  generaliza: 0.7
  especializa: 0.8
  causa: 0.5
  equilibra: -0.5
  transforma: 0.4

semantic_signature_vectors:
  - abstracao
  - complexidade
  - causalidade
  - emocionalidade
  - materialidade
  - simbolismo
  - dinamismo
  - temporalidade
  - ambiguidade

retrieval:
  semantic_threshold: 0.72
  graph_depth: 3
  rerank_limit: 12
  signature_weights:
    abstraction: 1.2
    causality: 1.1
    symbolism: 0.9
```

### 0.4 Criar `config/embedding.yaml`
```yaml
embedding:
  model: "sentence-transformers/all-MiniLM-L6-v2"
  dimensions: 384
  normalize: true
  types:
    structural:
      weight: 0.3
      source: "hierarchy_path"
    semantic:
      weight: 0.4
      source: "description"
    operational:
      weight: 0.2
      source: "cognitive_functions"
    symbolic:
      weight: 0.1
      source: "archetype_tags"
```

### 0.5 Criar `config/retrieval.yaml`
```yaml
retrieval:
  hybrid:
    vector_weight: 0.5
    graph_weight: 0.3
    symbolic_weight: 0.2
  thresholds:
    min_semantic_similarity: 0.72
    min_graph_relevance: 0.5
  limits:
    max_candidates: 50
    rerank_top_k: 12
    graph_traversal_depth: 3
```

### 0.6 Criar `config/graph.yaml`
```yaml
graph:
  engine: "networkx"
  directed: true
  weighted: true
  default_edge_weight: 0.5
  metrics:
    compute_centrality: true
    compute_density: true
    detect_clusters: true
    find_bridges: true
    detect_isolates: true
  persistence:
    format: "gexf"
    path: "data/graphs/ontology.gexf"
```

**Entregáveis da Fase 0:**
- [ ] Diretórios criados
- [ ] `requirements.txt`
- [ ] `config/ontology.yaml`
- [ ] `config/embedding.yaml`
- [ ] `config/retrieval.yaml`
- [ ] `config/graph.yaml`

---

## FASE 1 — NORMALIZAÇÃO ONTOLÓGICA

### 1.1 Criar `tools/uid_generator.py`

**Funções:**
```python
def generate_uid(concept_name: str) -> str:
    """Gera UID imutável: N4_DECOMPOSICAO a partir do nome do conceito."""
    # Remove acentos, uppercase, snake_case
    # Prefixo N4_ para distinguir de outros níveis
    
def generate_path(axis_code: str, pillar_code: str, domain_id: str,
                  subtree_id: str, cell_letter: str) -> str:
    """Gera path estrutural: S1.L1.1.1-A"""
    
def validate_uid(uid: str) -> bool:
    """Valida formato do UID: sem acentos, uppercase, snake_case."""
    
def generate_hierarchical_id(axis: int, pillar: int, domain: int,
                              subtree: int, cell: int) -> str:
    """Gera ID hierárquico: 1.1.1.1"""
```

### 1.2 Criar `core/ontology_typing.py`

**Funções:**
```python
def infer_natureza(cell_data: dict) -> str:
    """Inferir natureza ontológica a partir do conteúdo da célula.
    Usa keywords e heurísticas baseadas no domínio/pilar."""
    # Keywords mapping:
    # processo: verbs (decompor, transformar, iterar, resolver)
    # estado: nouns estáticos (integridade, equilíbrio, estrutura)
    # fenomeno: observações (ressonância, entropia, caos)
    # principio: regras universais (causa, efeito, conservação)
    # mecanismo: como algo funciona (feedback, cascata, recursão)
    # estrutura: organização (hierarquia, rede, camada)
    # arquétipo: padrões simbólicos (herói, sombra, trickster)
    # dinamica: mudança e fluxo (transformação, evolução, ciclo)
    # restricao: limites e regras (limiar, fronteira, proibição)
    # vetor: direção e magnitude (convergência, divergência, gradiente)

def validate_natureza(natureza: str, allowed_natures: list) -> bool:
    """Valida se a natureza é reconhecida na taxonomia."""

def normalize_natureza(natureza: str) -> str:
    """Normaliza para minúsculas, sem acentos."""
```

### 1.3 Criar `core/relation_engine.py`

**Funções:**
```python
def build_relations(cell_id: str, cell_data: dict, registry: dict) -> list:
    """Constrói lista de relações tipadas a partir de:
    - Relações declaradas no campo 'relacoes' (legado)
    - Inferência baseada em proximidade hierárquica
    - Inferência baseada em oposições semânticas
    
    Retorna: [
        {"tipo": "depende_de", "alvo": "N4_RECURSAO", "peso": 0.82},
        {"tipo": "complementa", "alvo": "N4_HOLISMO", "peso": 0.75},
        ...
    ]"""

def validate_relations(relations: list, registry: dict) -> list:
    """Valida:
    - Todos os alvos existem no registry
    - Pesos estão em [-1.0, 1.0]
    - Tipos são do vocabulário controlado
    - Sem auto-referência circular direta"""

def infer_reverse_relations(relations: list) -> list:
    """Inferir relações reversas:
    - Se A depende_de B → B é_requisito_de A
    - Se A generaliza B → B especializa A
    - Se A complementa B → B complementa A"""
```

### 1.4 Script de Transformação Principal: `tools/n4_to_json.py`

Este é o script central que converte os N4 markdown em JSON enriquecido.

**Pipeline:**
```
1. Carregar dados N4 de create_n4_manual.py (celulas_n4)
2. Carregar mapeamentos de reestruturar_n4.py
3. Para cada célula:
   a. Gerar uid, path, hierarchical_id
   b. Inferir natureza
   c. Construir relações tipadas
   d. Gerar campos semânticos (exemplos, analogias, anti_exemplos)
   e. Gerar assinatura semântica (placeholder para Phase 2)
4. Salvar JSON individual em data/json/
5. Gerar index global em data/json/ontology_index.json
```

**Schema JSON Final:**
```json
{
  "uid": "N4_DECOMPOSICAO",
  "path": "S1.L1.1.1-A",
  "hierarchical_id": "1.1.1.1",
  "nivel": "N4",
  "eixo": {
    "codigo": "S1",
    "nome": "SINTRÓPICO",
    "descricao": "Convergência, colapso de incerteza, materialização"
  },
  "pilar": {
    "codigo": "L1",
    "nome": "LOGOS",
    "crenca": "Estrutura, hierarquia, lógica inquestionável"
  },
  "dominio": {
    "codigo": "1.1",
    "nome": "ALGORITMIA",
    "descricao": "Sistemas de resolução, otimização e validação"
  },
  "subarvore": {
    "codigo": "1.1.1",
    "nome": "RESOLUÇÃO",
    "foco": "Desdobramento de passos finitos em micro-procedimentos"
  },
  "celula": {
    "codigo": "1",
    "nome": "DECOMPOSIÇÃO",
    "id_legado": "R1.1.1-A"
  },
  "natureza": "processo",
  "conceito": "Divisão de problemas complexos em subproblemas independentes",
  "descricao": "Técnica de quebrar problemas complexos em partes menores e gerenciáveis.",
  "sinonimos": ["fragmentação", "particionamento", "análise de componentes"],
  "relacoes": [
    {"tipo": "depende_de", "alvo": "N4_RECURSAO", "peso": 0.82},
    {"tipo": "complementa", "alvo": "N4_HOLISMO", "peso": 0.75},
    {"tipo": "generaliza", "alvo": "N4_SEGMENTACAO", "peso": 0.6}
  ],
  "tags": ["algoritmos", "design", "engenharia"],
  "gatilho": "Problema complexo sem estrutura clara",
  "acao": "Identificar subproblemas independentes",
  "restricao": "Avaliar limites de decomposição",
  "verificacao": "Subproblemas resolvidos independentemente",
  "exemplos": [
    "Merge sort dividindo array",
    "Arquitetura de microserviços",
    "Análise de caso na advocacia"
  ],
  "anti_exemplos": [
    "Dividir sem unir",
    "Subproblemas interdependentes",
    "Over-engineering"
  ],
  "analogias": [
    "Quebrar um osso em pedaços para analisar",
    "Dividir tarefas domésticas entre familiares"
  ],
  "aplicacoes": [
    "Design de algoritmos",
    "Arquitetura de software",
    "Gestão de projetos"
  ],
  "funcao_cognitiva": ["decompor", "segmentar", "modularizar"],
  "assinatura_semantica": {
    "abstracao": 0.82,
    "complexidade": 0.71,
    "causalidade": 0.88,
    "emocionalidade": 0.12,
    "materialidade": 0.35,
    "simbolismo": 0.25,
    "dinamismo": 0.65,
    "temporalidade": 0.45,
    "ambiguidade": 0.15
  },
  "opostos": ["N4_HOLISMO", "N4_INTEGRACAO"],
  "relacoes_cruzadas": ["S1.L1.1.1-B", "S1.L1.1.1-C"],
  "polaridade": "sintrópica",
  "vetor_simbolico": ["divisão", "organização", "clareza"],
  "metadata": {
    "data_criacao": "2026-05-07",
    "status": "ATIVO",
    "versao_schema": "3.0",
    "fonte": "create_n4_manual.py"
  }
}
```

**Entregáveis da Fase 1:**
- [ ] `tools/uid_generator.py` — funções de geração e validação de UIDs
- [ ] `core/ontology_typing.py` — inferência e validação de natureza
- [ ] `core/relation_engine.py` — construção e validação de relações tipadas
- [ ] `tools/n4_to_json.py` — script principal de conversão
- [ ] 162 arquivos JSON em `data/json/`
- [ ] `data/json/ontology_index.json` — índice global

---

## FASE 2 — EXPANSÃO SEMÂNTICA

### 2.1 Criar `core/cognitive_function_engine.py`

**Funções:**
```python
def infer_functions(cell_data: dict) -> list:
    """Inferir funções cognitivas a partir do conteúdo da célula.
    Taxonomia de funções:
    - decompor: quebrar em partes
    - segmentar: dividir em segmentos lógicos
    - modularizar: criar módulos independentes
    - classificar: categorizar elementos
    - hierarquizar: organizar em níveis
    - sequenciar: determinar ordem
    - filtrar: selecionar critérios
    - transformar: mudar de estado
    - sintetizar: combinar em novo todo
    - avaliar: julgar qualidade
    - validar: verificar correção
    - otimizar: melhorar eficiência
    - generalizar: abstrair padrão
    - especializar: aplicar a caso específico
    - mapear: criar correspondências
    - comparar: identificar similaridades/diferenças
    - inferir: deduzir informações implícitas
    - prever: antecipar resultados
    - equilibrar: ajustar forças opostas
    - resolver: encontrar solução
    - etc.
    """

def expand_functions(functions: list, registry: dict) -> list:
    """Expandir funções com base em relações e vizinhos no grafo."""

def rank_functions(functions: list, query_context: dict) -> list:
    """Ranking de funções por relevância para um dado contexto."""
```

### 2.2 Criar `core/signature_engine.py`

**Funções:**
```python
def generate_signature(cell_data: dict) -> dict:
    """Gera assinatura semântica com scores 0.0-1.0 para cada dimensão:
    - abstracao: quão abstrato é o conceito
    - complexidade: grau de complexidade
    - causalidade: grau de relação causa-efeito
    - emocionalidade: carga emocional
    - materialidade: tangibilidade
    - simbolismo: carga simbólica
    - dinamismo: grau de mudança/movimento
    - temporalidade: relação com tempo
    - ambiguidade: grau de ambiguidade
    
    Scoring baseado em:
    - Natureza da célula
    - Pilar e domínio
    - Texto descritivo (via heurísticas ou modelo)
    - Relações com outras células
    """

def compare_signatures(sig1: dict, sig2: dict) -> float:
    """Calcula similaridade entre duas assinaturas (cosine similarity)."""

def cluster_signatures(signatures: list, n_clusters: int = 18) -> dict:
    """Clusteriza assinaturas para descoberta de padrões."""
```

### 2.3 Criar `core/dialectic_engine.py`

**Funções:**
```python
def infer_opposites(cell_data: dict, registry: dict) -> list:
    """Inferir opostos ontológicos baseados em:
    - Relações 'contrasta' explícitas
    - Posição no grafo (nós distantes em dimensões opostas)
    - Análise semântica do conceito
    - Regras de domínio (ex: DECOMPOSIÇÃO ↔ HOLISMO)
    """

def build_tension_map(graph: nx.DiGraph) -> dict:
    """Constrói mapa de tensões entre opostos no grafo."""

def calculate_dialectic_distance(cell_a: str, cell_b: str,
                                  graph: nx.DiGraph) -> float:
    """Calcula distância dialética entre duas células."""
```

### 2.4 Atualizar `tools/n4_to_json.py`

Adicionar geração de:
- `funcao_cognitiva` (via `cognitive_function_engine`)
- `assinatura_semantica` (via `signature_engine`)
- `opostos` (via `dialectic_engine`)

**Entregáveis da Fase 2:**
- [ ] `core/cognitive_function_engine.py`
- [ ] `core/signature_engine.py`
- [ ] `core/dialectic_engine.py`
- [ ] Atualização dos 162 JSONs com novos campos
- [ ] `data/json/ontology_index.json` atualizado

---

## FASE 3 — GRAPH ENGINE

### 3.1 Criar `core/graph_engine.py`

**Funções:**
```python
class OntologyGraph:
    def __init__(self, registry: dict):
        """Inicializa grafo NetworkX direcionado."""
    
    def build_graph(self, registry: dict, relations: list) -> nx.DiGraph:
        """Constrói grafo completo:
        - Nós: 162 células N4 + 54 N3 + 18 N2 + 6 N1 + 2 N0
        - Arestas: relações tipadas (depende_de, complementa, etc.)
        - Pesos: baseados nos scores de relação
        """
    
    def query_neighbors(self, node_id: str, 
                        relation_type: str = None,
                        depth: int = 1) -> list:
        """Consulta vizinhos com filtro por tipo de relação e profundidade."""
    
    def semantic_walk(self, start_node: str, steps: int = 3,
                      strategy: str = "weighted") -> list:
        """Passeio semântico pelo grafo:
        - 'weighted': segue arestas de maior peso
        - 'random': exploração aleatória
        - 'directed': segue direção das relações
        - 'bidirectional': explora ambos sentidos
        """
    
    def infer_paths(self, source: str, target: str,
                    max_length: int = 5) -> list:
        """Inferir caminhos entre dois nós (all_simple_paths)."""
    
    def compute_metrics(self) -> dict:
        """Calcula métricas de grafo:
        - centralidade (degree, betweenness, closeness, eigenvector)
        - densidade
        - coeficiente de clustering
        - pontes (bridges)
        - isolamentos (isolates)
        - componentes conectados
        """
    
    def detect_concept_gaps(self) -> list:
        """Detecta buracos ontológicos:
        - Nós com poucas conexões
        - Relações implícitas não declaradas
        - Domínios sub-representados
        """
    
    def export_graphviz(self, path: str):
        """Exporta para formato Graphviz/D3."""
    
    def export_gexf(self, path: str):
        """Exporta para formato GEXF (Gephi)."""
```

### 3.2 Criar `tools/graph_builder.py`

Script de linha de comando para construção e análise do grafo:
```
python tools/graph_builder.py --build      # Constrói grafo
python tools/graph_builder.py --metrics    # Calcula métricas
python tools/graph_builder.py --export     # Exporta para visualização
python tools/graph_builder.py --analyze    # Análise completa
```

**Entregáveis da Fase 3:**
- [ ] `core/graph_engine.py` — classe `OntologyGraph`
- [ ] `tools/graph_builder.py` — CLI para construção e análise
- [ ] `data/graphs/ontology.gexf` — grafo persistido
- [ ] `data/graphs/graph_metrics.json` — métricas calculadas

---

## FASE 4 — EMBEDDINGS E RAG

### 4.1 Criar `tools/canonical_document_builder.py`

**Função:**
```python
def build_canonical_document(cell_data: dict) -> str:
    """Gera documento canônico textual para embedding:
    
    CONCEITO: {nome}
    DESCRIÇÃO: {descricao}
    NATUREZA: {natureza}
    FUNÇÕES COGNITIVAS: {funcao_cognitiva}
    CONTEXTO ONTOLÓGICO: {eixo} > {pilar} > {dominio} > {subarvore}
    RELAÇÕES: {relacoes}
    OPOSTOS: {opostos}
    EXEMPLOS: {exemplos}
    ANALOGIAS: {analogias}
    APLICAÇÕES: {aplicacoes}
    """
```

### 4.2 Criar `tools/embedding_builder.py`

**Funções:**
```python
def build_embeddings(json_dir: str, output_dir: str,
                     model_name: str = None) -> dict:
    """Gera embeddings para cada célula N4.
    Retorna dicionário: {uid: embedding_vector}
    
    Tipos de embedding:
    1. Estrutural — baseado em path hierárquico
    2. Semântico — baseado em descrição expandida
    3. Operacional — baseado em função cognitiva
    4. Simbólico — baseado em tags e arquétipos
    """

def build_faiss_index(embeddings: dict, index_dir: str):
    """Constrói índice FAISS para busca vetorial."""

def build_chroma_collection(embeddings: dict, collection_name: str):
    """Constrói coleção ChromaDB (alternativa ao FAISS)."""
```

### 4.3 Criar `runtime/retriever.py`

**Funções:**
```python
class HybridRetriever:
    def __init__(self, embedding_index, graph_engine, registry):
        """Inicializa retriever híbrido."""
    
    def retrieve_semantic(self, query: str, top_k: int = 10) -> list:
        """Busca por similaridade vetorial."""
    
    def retrieve_structural(self, query_path: str, depth: int = 2) -> list:
        """Busca por navegação hierárquica."""
    
    def retrieve_symbolic(self, tags: list, nature: str = None) -> list:
        """Busca por filtro simbólico/taxonomia."""
    
    def hybrid_rank(self, query: str, top_k: int = 12) -> list:
        """
        Pipeline de retrieval híbrido:
        1. query → embeddings → top 50 candidatos
        2. graph expansion → expande para vizinhos (depth=3)
        3. symbolic filtering → filtra por natureza/tags
        4. rerank → reordena por relevância combinada
        
        Score final = (0.5 × semantic_sim) + (0.3 × graph_relevance) + (0.2 × symbolic_match)
        """
```

**Entregáveis da Fase 4:**
- [ ] `tools/canonical_document_builder.py`
- [ ] `tools/embedding_builder.py`
- [ ] `data/embeddings/*.npy` — vetores de embedding
- [ ] `data/indexes/faiss_index.idx` — índice FAISS
- [ ] `runtime/retriever.py` — classe `HybridRetriever`

---

## FASE 5 — CLASSIFICADOR ONTOLÓGICO

### 5.1 Criar `runtime/classifier.py`

**Arquitetura do Classificador:**
```
INPUT: "como lidar com conflito emocional?"
    ↓
Pré-processamento
    ↓
Classificação N0 (Vetor): SINTRÓPICO ou ENTRÓPICO
    ↓
Classificação N1 (Pilar): PATHOS
    ↓
Classificação N2 (Domínio): ALTERIDADE
    ↓
Classificação N3 (Subárvore): CONFLITO
    ↓
Classificação N4 (Célula): RESOLUÇÃO_DE_CONFLITO
    ↓
OUTPUT: Classificação multinível com scores de confiança
```

**Funções:**
```python
class OntologicalClassifier:
    def __init__(self, registry, embedding_model):
        """Inicializa classificador com registry e modelo de embedding."""
    
    def classify_n0(self, query: str) -> dict:
        """Classifica eixo (SINTRÓPICO/ENTRÓPICO).
        Método: embedding similarity + keyword rules
        """
    
    def classify_n1(self, query: str, n0_context: dict) -> dict:
        """Classifica pilar dentro do eixo determinado.
        Método: embedding similarity restrito ao eixo
        """
    
    def classify_n2(self, query: str, n1_context: dict) -> dict:
        """Classifica domínio dentro do pilar."""
    
    def classify_n3(self, query: str, n2_context: dict) -> dict:
        """Classifica subárvore dentro do domínio."""
    
    def classify_n4(self, query: str, n3_context: dict) -> dict:
        """Classifica célula específica."""
    
    def full_classify(self, query: str) -> dict:
        """Executa classificação completa N0→N4 em cascata."""
```

**Estratégia de Classificação (conforme roadmap):**
```
Método              Uso
─────────────────────────────────────────────
Embeddings          Similaridade semântica
Keywords            Precisão em termos técnicos
Symbolic Rules      Coerência ontológica
LLM (fallback)      Quando confiança < threshold
```

**Entregáveis da Fase 5:**
- [ ] `runtime/classifier.py` — classe `OntologicalClassifier`
- [ ] `prompts/classifier/` — templates de prompt para cada nível
- [ ] Testes de classificação com acurácia reportada

---

## FASE 6 — ORCHESTRATOR COGNITIVO

### 6.1 Criar `runtime/orchestrator.py`

**Classe Principal:**
```python
class OntologyOrchestrator:
    """Motor principal do sistema cognitivo ontológico."""
    
    def __init__(self, config_path: str = "config/"):
        """Inicializa todos os subsistemas."""
        self.registry = OntologyRegistry()
        self.classifier = OntologicalClassifier(...)
        self.router = CognitiveRouter(...)
        self.retriever = HybridRetriever(...)
        self.synthesizer = ResponseSynthesizer(...)
        self.validator = OntologicalValidator(...)
    
    def process_query(self, query: str, context: dict = None) -> dict:
        """Pipeline principal de processamento:
        
        INPUT (query)
            ↓
        1. CLASSIFIER → classificação N0→N4
        2. ROUTER → seleciona módulos cognitivos
        3. RETRIEVER → busca contexto (híbrido)
        4. GRAPH EXPANSION → expande via grafo
        5. SYNTHESIS → monta prompt/resposta
        6. VALIDATOR → verifica coerência
        7. OUTPUT
        """
    
    def route_query(self, classification: dict) -> dict:
        """Determina quais módulos ativar."""
    
    def retrieve_context(self, query: str, classification: dict) -> dict:
        """Recupera contexto via retrieval híbrido."""
    
    def build_reasoning_chain(self, context: dict, 
                              classification: dict) -> list:
        """Monta cadeia de raciocínio baseada em funções cognitivas."""
    
    def synthesize_response(self, context: dict, 
                            reasoning_chain: list) -> str:
        """Gera resposta final."""
    
    def validate_output(self, response: str, 
                        classification: dict) -> dict:
        """Valida coerência ontológica da resposta."""
```

**Entregáveis da Fase 6:**
- [ ] `runtime/orchestrator.py` — classe `OntologyOrchestrator`
- [ ] Integração com todos os módulos anteriores

---

## FASE 7 — ROUTER COGNITIVO

### 7.1 Criar `runtime/router.py`

**Estratégia de Routing:**
```python
class CognitiveRouter:
    """Seleciona módulos cognitivos baseado na classificação."""
    
    ROUTING_RULES = {
        "LOGOS": {
            "modules": ["decomposition", "validation", "optimization"],
            "approach": "estrutural",
            "temperature": 0.3
        },
        "BIOS": {
            "modules": ["integration", "balance", "regeneration"],
            "approach": "sistemico",
            "temperature": 0.4
        },
        "PATHOS": {
            "modules": ["empathy", "values", "connection"],
            "approach": "relacional",
            "temperature": 0.5
        },
        "KHAOS": {
            "modules": ["disruption", "transformation", "emergence"],
            "approach": "exploratorio",
            "temperature": 0.7
        },
        "APEIRON": {
            "modules": ["scaling", "abstraction", "transcendence"],
            "approach": "sistemico",
            "temperature": 0.6
        },
        "MYTHOS": {
            "modules": ["narrative", "archetype", "symbolism"],
            "approach": "narrativo",
            "temperature": 0.5
        }
    }
    
    def route(self, classification: dict) -> dict:
        """Retorna configuração de módulos para o pilar dado."""
    
    def adjust_parameters(self, route: dict, 
                          query_complexity: float) -> dict:
        """Ajusta parâmetros (temperature, top_k) baseado na complexidade."""
```

**Entregáveis da Fase 7:**
- [ ] `runtime/router.py` — classe `CognitiveRouter`
- [ ] `prompts/routing/` — templates de prompt por pilar

---

## FASE 8 — ENGINE DE SÍNTESE

### 8.1 Criar `runtime/synthesizer.py`

**Funções:**
```python
class ResponseSynthesizer:
    """Monta prompts dinâmicos e gera respostas."""
    
    def build_prompt(self, context: dict, classification: dict,
                     reasoning_chain: list) -> str:
        """Monta prompt dinamicamente:
        
        === SYSTEM ===
        [DNA Ontológico: axiomas do vetor + crenças do pilar]
        
        === CONTEXT ===
        [Contexto ontológico da célula classificada]
        [Relações relevantes]
        [Assinatura semântica]
        [Opostos para inferência dialética]
        
        === FUNÇÕES COGNITIVAS ===
        [Chain of functions aplicáveis]
        
        === TASK ===
        [Query original do usuário]
        [Restrições]
        [Formato de saída esperado]
        """
    
    def compose_answer(self, prompt: str, 
                       model_response: str,
                       classification: dict) -> dict:
        """Compor resposta final com metadados."""
    
    def generate_variations(self, base_response: str, 
                            n_variations: int = 3) -> list:
        """Gera variações estratégicas (camadas opcionais)."""
```

**Entregáveis da Fase 8:**
- [ ] `runtime/synthesizer.py` — classe `ResponseSynthesizer`
- [ ] `prompts/synthesis/` — templates de síntese

---

## FASE 9 — VALIDADOR ONTOLÓGICO

### 9.1 Criar `runtime/validator.py`

**Verificações:**
```python
class OntologicalValidator:
    """Garante coerência ontológica das respostas."""
    
    def validate_axis_consistency(self, response: str, 
                                   classification: dict) -> bool:
        """Resposta contradiz o eixo (SINTRÓPICO vs ENTRÓPICO)?"""
    
    def validate_signature(self, response: str, 
                           signature: dict) -> bool:
        """Resposta rompe a assinatura semântica?"""
    
    def validate_polarity(self, response: str, 
                          classification: dict) -> bool:
        """Mistura polaridades (SINTRÓPICO + ENTRÓPICO)?"""
    
    def validate_concepts(self, response: str, 
                          allowed_concepts: list) -> bool:
        """Usa conceitos incompatíveis?"""
    
    def validate_dna_compliance(self, response: str) -> dict:
        """Verifica conformidade com Regras Douradas."""
    
    def full_validate(self, response: str, 
                      classification: dict,
                      context: dict) -> dict:
        """Validação completa retornando score e issues."""
```

**Entregáveis da Fase 9:**
- [ ] `runtime/validator.py` — classe `OntologicalValidator`
- [ ] `prompts/validation/` — templates de validação

---

## FASE 10 — AGENTES ESPECIALIZADOS E MEMÓRIA

### 10.1 Criar Estrutura de Agentes

```
.kilo/
├── agents/
│   ├── classifier_agent.py       # Invoca classificador
│   ├── graph_agent.py            # Navegação e expansão de grafo
│   ├── synthesis_agent.py        # Geração de resposta
│   ├── validator_agent.py        # Verificação de coerência
│   └── dialectic_agent.py        # Exploração de opostos
├── memory/
│   ├── working_memory.py         # Contexto da sessão atual
│   ├── semantic_memory.py        # Memória vetorial persistente
│   ├── graph_memory.py           # Estado do grafo
│   └── episodic_memory.py        # Histórico de interações
├── prompts/
│   ├── classifier/
│   ├── retrieval/
│   ├── synthesis/
│   ├── validation/
│   └── routing/
└── orchestrators/
    └── cognitive_orchestrator.py
```

### 10.2 Implementar Agentes

Cada agente é uma classe com interface unificada:
```python
class BaseAgent:
    def __init__(self, config: dict):
        self.config = config
    
    def process(self, input_data: dict) -> dict:
        raise NotImplementedError
    
    def observe(self, feedback: dict):
        """Aprendizado contínuo a partir de feedback."""

class ClassifierAgent(BaseAgent):
    """Agente de classificação ontológica."""
    def process(self, input_data: dict) -> dict:
        # Delega ao OntologicalClassifier
        # Adiciona caching e logging

class GraphAgent(BaseAgent):
    """Agente de navegação de grafo."""
    def process(self, input_data: dict) -> dict:
        # Consulta OntologyGraph
        # Executa semantic_walk, infer_paths

class SynthesisAgent(BaseAgent):
    """Agente de geração de resposta."""
    def process(self, input_data: dict) -> dict:
        # Monta prompt via ResponseSynthesizer
        # Invoca LLM
        # Retorna resposta estruturada

class ValidatorAgent(BaseAgent):
    """Agente de validação."""
    def process(self, input_data: dict) -> dict:
        # Executa OntologicalValidator
        # Retorna score e issues

class DialecticAgent(BaseAgent):
    """Agente de exploração dialética."""
    def process(self, input_data: dict) -> dict:
        # Identifica opostos relevantes
        # Gera perspectivas alternativas
        # Calcula tensões
```

### 10.3 Implementar Memória

```python
class SemanticMemory:
    """Memória vetorial persistente usando ChromaDB/FAISS."""
    def store(self, uid: str, embedding: np.ndarray, metadata: dict):
    def query(self, embedding: np.ndarray, top_k: int = 10) -> list:
    def update(self, uid: str, new_embedding: np.ndarray):

class WorkingMemory:
    """Memória de trabalho para sessão ativa."""
    def __init__(self, max_items: int = 100):
    def add(self, item: dict):
    def get_context(self) -> list:
    def clear(self):

class EpisodicMemory:
    """Memória episódica de interações."""
    def log_interaction(self, query: str, response: str, 
                        classification: dict, score: float):
    def get_history(self, n: int = 10) -> list:
```

**Entregáveis da Fase 10:**
- [ ] `.kilo/agents/` — 5 agentes especializados
- [ ] `.kilo/memory/` — 4 tipos de memória
- [ ] `.kilo/prompts/` — templates organizados

---

## FASE 11 — INTEGRAÇÃO FINAL E TESTES

### 11.1 Testes de Integração

```python
# tests/test_integration.py

def test_full_pipeline():
    """Testa o pipeline completo com queries de exemplo."""
    orchestrator = OntologyOrchestrator()
    
    queries = [
        "como lidar com conflito emocional?",
        "quando usar recursão?",
        "o que é homeostase?",
        "como transformar um sistema?",
        "o que é decomposição de problemas?"
    ]
    
    for query in queries:
        result = orchestrator.process_query(query)
        assert result["classification"] is not None
        assert result["response"] is not None
        assert result["validation"]["passed"] is True
```

### 11.2 Testes de Aceitação

```python
# tests/test_acceptance.py

def test_ontological_consistency():
    """Verifica que todas as 162 células são consistentes."""
    registry = load_registry()
    for uid, cell in registry.items():
        assert cell["natureza"] in VALID_NATURES
        assert cell["assinatura_semantica"] is not None
        assert cell["relacoes"] is not None
        assert cell["funcao_cognitiva"] is not None

def test_graph_connectivity():
    """Verifica que o grafo é conexo."""
    g = build_graph()
    assert nx.is_weakly_connected(g)

def test_classifier_accuracy():
    """Testa acurácia do classificador com dados conhecidos."""
    classifier = OntologicalClassifier()
    test_cases = load_test_cases()
    correct = 0
    for query, expected in test_cases:
        result = classifier.full_classify(query)
        if result["n4"] == expected["n4"]:
            correct += 1
    accuracy = correct / len(test_cases)
    assert accuracy >= 0.70  # Mínimo 70%
```

### 11.3 Documentação Final

- `README.md` — Visão geral do sistema, instalação, uso
- `ARCHITECTURE.md` — Diagrama arquitetural detalhado
- `API_REFERENCE.md` — Documentação de todas as classes e funções
- `CONTRIBUTING.md` — Guia para contribuidores

**Entregáveis da Fase 11:**
- [ ] Testes de integração passando
- [ ] Testes de aceitação com acurácia ≥ 70%
- [ ] Grafo conexo verificado
- [ ] Todas as 162 células consistentes
- [ ] Documentação completa

---

## CRONOGRAMA ESTIMADO

| Fase | Descrição | Duração Estimada | Dependência |
|------|-----------|-----------------|-------------|
| 0 | Estrutura e configuração | 1 dia | — |
| 1 | Normalização (UIDs, tipos, relações, JSON) | 3-4 dias | Fase 0 |
| 2 | Assinaturas semânticas, opostos, funções | 2-3 dias | Fase 1 |
| 3 | Graph Engine (NetworkX) | 2 dias | Fase 1 |
| 4 | Embeddings e Retrieval Híbrido | 3-4 dias | Fase 1, 3 |
| 5 | Classificador Ontológico | 3-4 dias | Fase 1, 4 |
| 6 | Orchestrator | 2-3 dias | Fase 5 |
| 7 | Router Cognitivo | 1-2 dias | Fase 6 |
| 8 | Engine de Síntese | 2-3 dias | Fase 6, 7 |
| 9 | Validador | 1-2 dias | Fase 8 |
| 10 | Agentes e Memória | 3-4 dias | Fase 6-9 |
| 11 | Integração e Testes | 2-3 dias | Fase 10 |
| **Total** | | **~28-37 dias** | |

---

## RISCOS E MITIGAÇÕES

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| IDs inconsistentes entre sistemas | Alto | Script de reconciliação em Fase 1 |
| Embeddings de baixa qualidade | Médio | Avaliar múltiplos modelos; usar fine-tuning se necessário |
| Grafo desconexo | Médio | Adicionar relações inferidas; verificar na Fase 3 |
| Classificador com baixa acurácia | Alto | Iterar com mais exemplos; combinar métodos |
| Performance com 162 células | Baixo | Caching; índices otimizados |

---

## MÉTRICAS DE SUCESSO

1. **162 JSONs gerados** com schema completo e consistente
2. **Grafo conexo** com métricas calculadas
3. **Classificador** com acurácia ≥ 70% em testes
4. **Retrieval híbrido** retorna resultados relevantes em < 1s
5. **Orchestrator** processa queries completas sem erros
6. **Validador** detecta ≥ 95% das inconsistências simuladas
7. **Sistema end-to-end** funcional via CLI ou API
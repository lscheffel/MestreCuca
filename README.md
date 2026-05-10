# MestreCuca — Sistema Cognitivo Ontológico

## Arquitetura

Sistema cognitivo baseado em ontologia fractal com 162 células N4 (2×3×3×3×3).

### Estrutura de Diretórios

```
.
├── config/                    # Configurações YAML
│   ├── ontology.yaml          # Definição completa da ontologia
│   ├── embedding.yaml         # Configuração de modelos de embedding
│   ├── retrieval.yaml         # Thresholds e limites de retrieval
│   └── graph.yaml             # Configuração do grafo NetworkX
├── ontology/                  # Dados ontológicos por nível
│   ├── n0/                    # Vetores (SINTRÓPICO/ENTRÓPICO)
│   ├── n1/                    # Pilares (LOGOS/BIOS/PATHOS/KHAOS/APEIRON/MYTHOS)
│   ├── n2/                    # Domínios (18 domínios)
│   ├── n3/                    # Subárvores (54 subárvores)
│   └── n4/                    # Células operacionais (162 células)
├── data/                      # Dados persistentes
│   ├── json/                  # Documentos JSON
│   ├── embeddings/            # Vetores de embedding
│   ├── indexes/               # Índices de busca
│   └── graphs/                # Grafos persistidos (GEXF)
├── core/                      # Módulos centrais
├── tools/                     # Utilitários
├── runtime/                   # Configuração de execução
├── prompts/                   # Templates de prompt
│   ├── classifier/
│   ├── retrieval/
│   ├── synthesis/
│   ├── validation/
│   └── routing/
├── .kilo/                     # Configuração interna
│   ├── agents/
│   ├── memory/
│   ├── orchestrators/
│   └── prompts/
├── tests/                     # Testes
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Testes

```bash
python -m pytest tests/ -v
```

# AGENTS.md — runtime/

> Módulos de execução do pipeline cognitivo.  
> Regras globais em `../AGENTS.md`. Este arquivo só contém o que é específico de `runtime/`.

---

## Pipeline e Responsabilidades

```
Query → Classifier → Router → Retriever → Graph Agent → Dialectic Engine → Synthesizer → Validator → Output
                                                    ↑
                                          Autonomy Layer (modo autonomous)
```

| Módulo | Classe | Responsabilidade |
|---|---|---|
| `classifier.py` | `OntologicalClassifier` | Mapeia query para N0→N4; entrada do pipeline |
| `router.py` | `CognitiveRouter` | Seleciona pipeline (full / simple / autonomous) |
| `retriever.py` | `HybridRetriever` | Busca híbrida: FAISS vetorial + grafo + BM25 |
| `synthesizer.py` | `OntologySynthesizer` | Compõe resposta a partir dos contextos recuperados |
| `validator.py` | `OntologyValidator` | Verifica coerência ontológica do output |
| `orchestrator.py` | `MultiAgentOrchestrator` | Coordena todos os módulos; gerencia estado |
| `runtime.yaml` | — | Config de runtime — 🔒 não modificar sem instrução |

---

## Regras de Desenvolvimento

- **Validação em cada etapa** — cada módulo valida sua entrada antes de processar e sua saída antes de retornar
- **Nenhum módulo acessa `data/` diretamente** — usar as abstrações de `core/` (OntologyGraph, HybridRetriever)
- **`_diag_*.py` na pasta** são scripts de diagnóstico temporários — não modificar, não referenciar

```python
# ✅ Padrão de módulo runtime/
from pathlib import Path
from typing import Optional
from rich.console import Console
from core.agent_base import AgentResult

console = Console()

class OntologicalClassifier:
    """Classifica queries no espaço ontológico N0→N4."""

    def classify(self, query: str) -> AgentResult:
        """Retorna AgentResult com nível N e célula identificada."""
        if not query or not query.strip():
            raise ValueError("Query não pode ser vazia")

        console.print(f"[blue][→][/blue] Classificando: {query[:50]}...")
        # ...
        console.print(f"[green][✓][/green] Classificado em N{nivel}: {celula}")
        return AgentResult(...)
```

---

## FAISS e Embeddings

```python
import numpy as np
import faiss
from pathlib import Path

# Carregar índice FAISS — sempre verificar existência antes
index_path = Path("data/indexes/faiss.index")
if not index_path.exists():
    raise FileNotFoundError(f"Índice FAISS não encontrado: {index_path}")

index = faiss.read_index(str(index_path))

# Embeddings — sempre float32, nunca float64
embedding = model.encode([query], convert_to_numpy=True).astype(np.float32)
distances, indices = index.search(embedding, k=10)
```

- Modelo: `all-MiniLM-L6-v2` (384 dimensões)
- Configuração do índice: `IVFFlat`, `nlist=100`, `nprobe=10` — não alterar sem atualizar `config/embedding.yaml`
- Embeddings em `data/embeddings/` — regenerar via `tools/build_embeddings.py` se inválidos

---

## Logging

Usar `rich` — **nunca `print()` puro** neste módulo:

```python
from rich.console import Console
console = Console()

console.print("[green][✓][/green] Pipeline concluído")
console.print("[yellow][!][/yellow] Retrieval abaixo do limiar: {score:.3f}")
console.print("[red][✗][/red] Validação falhou: {motivo}")
console.print(f"[blue][→][/blue] Etapa: {etapa}")
```

---

## Modos de Pipeline

| Modo | Etapas ativas | Quando usar |
|---|---|---|
| `full` | todas | queries complexas, padrão |
| `simple` | Router → Retriever → Synthesizer → Validator | queries diretas, baixa complexidade |
| `autonomous` | full + Autonomy Layer | auto-avaliação, feedback loop, thresholds adaptativos |

---

## Alterações Críticas — Parar e Confirmar

- Mudar a ordem das etapas do pipeline em `orchestrator.py`
- Alterar limiares de retrieval (buscar em `config/retrieval.yaml` antes)
- Mudar o schema de `AgentResult` retornado por qualquer módulo
- Alterar parâmetros do FAISS (`nlist`, `nprobe`, dimensão)
- Qualquer mudança em `runtime.yaml`
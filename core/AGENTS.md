# AGENTS.md — core/

> Motores centrais do MestreCuca. Framework-agnostic — sem dependências de `runtime/`.  
> Regras globais em `../AGENTS.md`. Este arquivo só contém o que é específico de `core/`.

---

## Responsabilidade dos Módulos

| Arquivo | Classe principal | Responsabilidade |
|---|---|---|
| `ontology_graph.py` | `OntologyGraph` | Grafo NetworkX MultiDiGraph — nós N0→N4, arestas tipadas |
| `signature_engine.py` | `SignatureEngine` | Assinaturas semânticas 9D para cada célula N4 |
| `dialectic_engine.py` | `DialecticEngine` | Inferência de opostos em 5 níveis de tensão |
| `ontology_typing.py` | — | 10 naturezas ontológicas e seus tipos |
| `relation_engine.py` | `RelationEngine` | 10 tipos de relação com pesos (−1.0 a +1.0) |
| `cognitive_function_engine.py` | — | Funções cognitivas derivadas da ontologia |
| `agent_base.py` | `BaseAgent`, `AgentResult`, `AgentMemory` | Contratos base para todos os agentes |

---

## Regras de Desenvolvimento

- **Sem imports de `runtime/`** — `core/` não pode depender de módulos de execução
- **Sem efeitos colaterais** em construtores — inicialização leve, I/O somente em métodos explícitos
- **Type hints obrigatórios** em toda assinatura pública
- **Docstring obrigatória** em toda classe e método público

```python
# ✅ Padrão de módulo core/
from pathlib import Path
from typing import Optional
from rich.console import Console

console = Console()

class OntologyGraph:
    """Grafo principal da ontologia fractal N0→N4.
    
    Usa NetworkX MultiDiGraph internamente. Nós representam células
    ontológicas; arestas representam relações tipadas com peso.
    """

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self._graph = None  # inicializar lazy, não no __init__
        self._config_path = config_path or Path("config/ontology.yaml")

    def load(self) -> None:
        """Carrega o grafo a partir do config. Chamar explicitamente."""
        console.print("[blue][→][/blue] Carregando grafo ontológico...")
        # ...
```

---

## Logging

Usar `rich` — **nunca `print()` puro** neste módulo:

```python
from rich.console import Console
console = Console()

console.print("[green][✓][/green] Grafo carregado")
console.print("[yellow][!][/yellow] Nó não encontrado: {node_id}")
console.print("[red][✗][/red] Falha ao carregar config")
console.print(f"[blue][→][/blue] Processando: {item}")
```

---

## Tipos de Relação (referência rápida)

| Tipo | Peso típico | Semântica |
|---|---|---|
| `depende_de` | 0.8–1.0 | Pré-requisito |
| `complementa` | 0.6–0.9 | Completude |
| `contrasta` | −0.5 a −0.9 | Oposição |
| `expande` | 0.5–0.8 | Generalização |
| `implementa` | 0.7–0.9 | Concretização |
| `causa` | 0.7–0.95 | Causalidade |
| `equilibra` | 0.5–0.8 | Homeostase |
| `transforma` | 0.6–0.9 | Metamorfose |

---

## Alterações Críticas — Parar e Confirmar

- Mudar assinatura de qualquer método público de `OntologyGraph`, `SignatureEngine` ou `DialecticEngine`
- Alterar o schema de `AgentResult` ou `AgentMemory` em `agent_base.py`
- Adicionar ou remover tipos em `ontology_typing.py` ou `relation_engine.py`
- Qualquer mudança que afete como `runtime/` consome `core/`
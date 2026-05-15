---
version: "3.1.0"
type: "persistent_operational_memory"
project: "MestreCuca"
profile: "windows_cmd_runtime"
language: "pt-BR"
os: "Windows 11"
shell: "cmd.exe"
python: "python.exe"
encoding: "utf-8"

priority:
  - windows_compatibility
  - cmd_compatibility
  - utf8_safety
  - python_exe_only
  - ontology_consistency
  - retrieval_integrity

startup_sequence:
  - "READ STATE.md"
  - "READ README.md"
  - "READ config/*.yaml"
  - "READ docs/"

hard_constraints:
  - "NEVER USE UNIX COMMANDS"
  - "NEVER USE POWERSHELL"
  - "NEVER USE python3"
  - "NEVER ASSUME LINUX"
  - "CODE IS THE ONLY SOURCE OF TRUTH"

truth_source:
  primary: "source_code"
  secondary: "config/*.yaml"
  tertiary: "docs/"

last_updated: "2026-05-13"
updated_by: "Kilo Code Doc Spec"
---

# STATE.md — Persistent Operational Memory

## Runtime Identity

| Campo | Valor |
|---|---|
| OS | Windows 11 |
| Shell | cmd.exe |
| Python | python.exe |
| Encoding | UTF-8 |
| Runtime Policy | Windows-first |
| Filesystem | UTF-8 + paths acentuados suportados |

---

# Critical Runtime Constraints

## Invalid Runtime Assumptions

NEVER ASSUME:

- Linux
- macOS
- Bash
- WSL
- PowerShell
- Unix filesystem
- python3

---

## Forbidden Outputs

NEVER GENERATE:

```text
ls
cat
grep
bash
sh
zsh
powershell
pwsh
python3
py
source
chmod
sudo
```

NEVER GENERATE:

```text
/home/
~/ 
/usr/
```

---

## Valid Runtime Behavior

ONLY VALID SHELL:
- cmd.exe

ONLY VALID PYTHON:
- python.exe

VALID:

```cmd
python.exe run_kilo.py
python.exe diag_env.py
python.exe -m pytest tests -v
dir
type arquivo.txt
```

---

# Known Agent Failure Patterns

| Problema | Correção |
|---|---|
| Geração de `python3` | Usar `python.exe` |
| Comandos bash/Linux | Reescrever para CMD |
| Uso de PowerShell | Proibido |
| Paths Unix (`/home/`) | Usar pathlib + Windows |
| Parsing via shell | Mover para Python |
| Encoding implícito | Forçar UTF-8 explícito |
| Uso de `py` launcher | Usar `python.exe` |

---

# Recovery Protocol

IF INVALID COMMAND IS GENERATED:

1. STOP
2. RECHECK RUNTIME IDENTITY
3. REWRITE FOR CMD.EXE
4. REPLACE `python3` WITH `python.exe`
5. VALIDATE WINDOWS COMPATIBILITY
6. EXECUTE AGAIN

---

# Bootstrap Load Order

1. `STATE.md`
2. `README.md`
3. `config/*.yaml`
4. `docs/`
5. `runtime/`
6. `core/`

---

# System State

| Campo | Valor |
|---|---|
| Versão | 3.0.2 |
| Fase do Roadmap | Fase 1 — Arquitetura do Prompt Arquitetado (RFC-004) |
| Status | READY FOR DEVELOPMENT |
| Build | Estável |
| Ontologia | 162 células N4 operacionais |

---

# Operational Truths

| Verdade Operacional | Estado |
|---|---|
| `run_kilo.py` é o entrypoint principal | TRUE |
| Projeto é Windows-first | TRUE |
| Makefile não existe | TRUE |
| `.venv` é obrigatório | TRUE |
| `data/` contém artefatos gerados | TRUE |
| `config/ontology.yaml` é fonte canônica | TRUE |

---

# Active Components

## Core

| Arquivo | Função |
|---|---|
| `core/ontology_graph.py` | OntologyGraph (NetworkX MultiDiGraph) |
| `core/signature_engine.py` | Assinaturas semânticas 9D |
| `core/dialectic_engine.py` | Inferência dialética |
| `core/cognitive_function_engine.py` | Funções cognitivas |
| `core/ontology_typing.py` | Naturezas ontológicas |
| `core/relation_engine.py` | Relações ponderadas |
| `core/agent_base.py` | BaseAgent / AgentMemory |

---

## Runtime

| Arquivo | Função |
|---|---|
| `runtime/classifier.py` | OntologicalClassifier |
| `runtime/router.py` | CognitiveRouter |
| `runtime/retriever.py` | HybridRetriever |
| `runtime/synthesizer.py` | OntologySynthesizer |
| `runtime/validator.py` | OntologyValidator |
| `runtime/orchestrator.py` | MultiAgentOrchestrator |

---

## Agents

| Agente | Modelo | Função |
|---|---|---|
| OntoClassifier | GPT-4o | Classificação N0→N4 |
| OntoRetriever | GPT-4o | Retrieval híbrido |
| OntoSynthesizer | GPT-4o | Síntese multi-fonte |
| OntoValidator | GPT-4o | Validação |
| OntoRouter | GPT-4o-mini | Roteamento |
| AutonomyLayer | Interno | Feedback loop |

---

# Embedding Configuration

| Campo | Valor |
|---|---|
| Modelo | all-MiniLM-L6-v2 |
| Dimensão | 384 |
| Índice | FAISS IVFFlat |
| Similaridade | cosine |
| nlist | 100 |
| nprobe | 10 |
| Cache | LRU |
| TTL | 24h |

---

# Memory Architecture

| Nível | Tipo | Capacidade | TTL | Estratégia |
|---|---|---|---|---|
| Curto prazo | volatile | 500 | 30 min | LRU |
| Trabalho | managed | 200 | 1h | priority |
| Longo prazo | SQLite | 100k | ∞ | relevance |
| Embedding cache | LRU | 50k | 24h | similaridade |
| Retrieval cache | Redis TTL | 50k | 1h | cache |

---

# Ontological Structure

```text
N0 (Vetor):          2 nós
N1 (Pilar):          6 nós
N2 (Domínio):       18 nós
N3 (Subárvore):     54 nós
N4 (Célula):       162 nós

2×3×3×3×3 = 162
```

---

# Ontology Data Integrity

| Campo | Valor |
|---|---|
| Diretório | `data/json/` |
| Arquivos N4 | 162 |
| Índice | `ontology_index.json` |
| Estrutura | uid + relações + assinatura 9D |

---

# Hybrid Retrieval Configuration

| Método | Peso | Limiar |
|---|---|---|
| Vetorial | 0.50 | 0.15 |
| Gráfico | 0.30 | 0.50 |
| Simbólico | 0.20 | 0.80 |
| Fusão | weighted_sum | 0.40 |
| Reranking | cross-encoder | 0.50 |

---

# Recent Design Decisions

## 2026-05-13 — README Audit

- README sincronizado com filesystem real
- Entrypoints confirmados
- Makefile inexistente documentado
- Estrutura validada recursivamente
- Stack confirmada:
  - Python 3.13
  - NetworkX ≥3.0
  - sentence-transformers ≥2.2

---

## 2026-05-09 — Ontology V2 Consolidation

- Auditoria ontológica concluída
- Correções de herança aplicadas
- Migração para `config/ontology.yaml`

---

# Known Bugs and Workarounds

| Bug | Status | Workaround |
|---|---|---|
| `driver.py` path issues on Windows | Conhecido | Usar `run_kilo.py` |
| `CHANGELOG.md` ausente | Resolvido | — |
| `CONTRIBUTING.md` ausente | Resolvido | — |

---

# Operational Directives

ALWAYS:

- reload STATE.md every session
- validate runtime assumptions
- use UTF-8 explicitly
- use pathlib
- use python.exe
- treat source code as canonical truth

NEVER:

- hardcode runtime assumptions
- assume Linux compatibility
- use bash syntax
- generate python3
- trust stale documentation

---

# Context Role

THIS FILE IS:

- persistent operational memory
- runtime identity source
- architectural snapshot
- agent bootstrap context
- known-failures registry

THIS FILE IS NOT:

- marketing documentation
- roadmap
- manifesto
- speculative architecture
- source code replacement
---
version: "TEMPLATE"
type: "persistent_operational_memory"

project: "MestreCuca"

profile: "windows_cmd_runtime"

os: "Windows 11"
shell: "cmd.exe"
python: "python.exe"
encoding: "utf-8"

structure_policy: "canonical"
update_strategy: "incremental_patch"

truth_source:
  primary: "source_code"
  secondary: "config/*.yaml"

startup_sequence:
  - "READ STATE.md"
  - "READ README.md"
  - "READ config/*.yaml"

hard_constraints:
  - "NEVER USE UNIX COMMANDS"
  - "NEVER USE POWERSHELL"
  - "NEVER USE python3"
  - "NEVER ASSUME LINUX"
---

# STATE.md — Persistent Operational Memory

# Runtime Identity

| Campo | Valor |
|---|---|
| OS | Windows 11 |
| Shell | cmd.exe |
| Python | python.exe |
| Encoding | UTF-8 |

---

# Critical Runtime Constraints

## Invalid Runtime Assumptions

- Linux
- Bash
- PowerShell
- python3
- Unix filesystem

---

# Known Agent Failure Patterns

| Problema | Correção |
|---|---|
| python3 | python.exe |
| bash | cmd.exe |
| paths Unix | pathlib + Windows |
| PowerShell | proibido |

---

# Recovery Protocol

1. STOP
2. RECHECK RUNTIME IDENTITY
3. REWRITE FOR CMD.EXE
4. VALIDATE WINDOWS COMPATIBILITY

---

# Bootstrap Load Order

1. STATE.md
2. README.md
3. config/*.yaml
4. docs/

---

# System State

| Campo | Valor |
|---|---|
| Versão | — |
| Status | — |
| Build | — |

---

# Operational Truths

| Verdade | Estado |
|---|---|
| run_kilo.py é entrypoint principal | TRUE |

---

# Active Components

## Core

| Arquivo | Função |
|---|---|
| — | — |

---

## Runtime

| Arquivo | Função |
|---|---|
| — | — |

---

## Agents

| Agente | Modelo | Função |
|---|---|---|
| — | — | — |

---

# Embedding Configuration

| Campo | Valor |
|---|---|
| Modelo | — |

---

# Memory Architecture

| Nível | Tipo | Capacidade | TTL |
|---|---|---|---|
| — | — | — | — |

---

# Ontological Structure

```text
N0 → N4
```

---

# Hybrid Retrieval Configuration

| Método | Peso | Limiar |
|---|---|---|
| — | — | — |

---

# Recent Design Decisions

## YYYY-MM-DD

- —

---

# Known Bugs and Workarounds

| Bug | Status | Workaround |
|---|---|---|
| — | — | — |

---

# Operational Directives

ALWAYS:

- reload STATE.md
- preserve structure
- use UTF-8
- use pathlib
- use python.exe

NEVER:

- assume Linux
- rewrite structure
- use bash
- use python3

---

# Context Role

THIS FILE IS:

- persistent operational memory
- runtime identity source
- architectural snapshot

THIS FILE IS NOT:

- marketing
- roadmap
- speculative architecture
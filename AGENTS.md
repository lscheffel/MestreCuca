---
version: "5.1.0"
type: "bootstrap"
priority: "critical"

os: "Windows 11"
shell: "cmd.exe"
python: "python.exe"
encoding: "utf-8"

mandatory_reads:
  - ".kilo/STATE.md"
  - ".kilo/STATE_RULES.md"
  - ".kilo/templates/STATE.template.md"

hard_constraints:
  - "NEVER USE UNIX COMMANDS"
  - "NEVER USE POWERSHELL"
  - "NEVER USE python3"
  - "NEVER ASSUME LINUX"
  - "STATE STRUCTURE IS CANONICAL"

truth_source:
  primary: "source_code"
  secondary: "config/*.yaml"
  tertiary: "STATE.md"
---

# AGENTS.md

## CRITICAL RUNTIME IDENTITY

THIS PROJECT RUNS ON:

- Windows 11
- cmd.exe
- python.exe
- UTF-8

ASSUME:

- Linux does not exist
- Bash does not exist
- PowerShell does not exist
- python3 does not exist

---

# FIRST ACTIONS

READ IN THIS EXACT ORDER:

1. `.kilo/STATE.md`
2. `.kilo/STATE_RULES.md`
3. `.kilo/templates/STATE.template.md`
4. `README.md`

DO THIS BEFORE:
- coding
- refactoring
- debugging
- documentation updates
- config edits

---

# STATE.md MAINTENANCE RULES

`STATE.md` IS:

- persistent operational memory
- architectural snapshot
- runtime identity source
- known-failures registry

`STATE.md` IS NOT:

- prose documentation
- brainstorming
- roadmap
- speculative architecture

---

# STRUCTURE ENFORCEMENT

STATE STRUCTURE IS CANONICAL.

PRESERVE:

- YAML header
- section order
- tables
- runtime identity
- known failures
- operational truths

DO NOT:

- rewrite structure
- reorganize sections
- convert tables into prose
- summarize aggressively
- “improve” formatting

WHEN UPDATING:
- patch incrementally
- modify values only
- append chronologically

REFERENCE TEMPLATE:

`.kilo/templates/STATE.template.md`

---

# WINDOWS RUNTIME RULES

ONLY VALID SHELL:
- cmd.exe

ONLY VALID PYTHON:
- python.exe

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

IF GENERATED:
1. STOP
2. REWRITE FOR CMD.EXE
3. RECHECK BEFORE EXECUTION

---

# PYTHON EXECUTION

VALID:

```cmd
python.exe run_kilo.py
python.exe diag_env.py
python.exe -m pytest tests -v
```

INVALID:

```cmd
python3 script.py
py script.py
python script.py
```

---

# OPERATIONAL PRIORITIES

1. Windows compatibility
2. UTF-8 safety
3. Structural consistency
4. Incremental updates
5. Explicit runtime behavior
6. Source-code truth alignment
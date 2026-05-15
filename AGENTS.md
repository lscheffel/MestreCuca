---
version: "4.0"
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
  - explicit_errors
  - python_over_shell
  - never_assume_unix
startup:
  - "READ .kilo/STATE.md FIRST"
hard_constraints:
  - "NEVER USE UNIX COMMANDS"
  - "NEVER USE POWERSHELL"
  - "NEVER USE python3"
  - "NEVER ASSUME LINUX"
---

# AGENTS.md — WINDOWS CMD RUNTIME

## ENVIRONMENT

THIS PROJECT RUNS ON:

- Windows 11 only
- CMD.EXE only
- UTF-8 only
- Python via `python.exe`

ASSUME:

- Linux does not exist
- macOS does not exist
- Bash does not exist
- WSL does not exist
- PowerShell is not available

---

# FIRST ACTION

ALWAYS READ:

```cmd
type .kilo\STATE.md
```

DO THIS BEFORE:
- coding
- debugging
- refactoring
- running scripts
- editing configs

---

# HARD PROHIBITIONS

NEVER USE:

```text
ls
cat
grep
head
tail
touch
rm
mv
cp
pwd
export
source
chmod
sudo
bash
sh
zsh
powershell
pwsh
python3
py
python3.exe
```

NEVER USE:

- Unix paths
- `/home/`
- `~/`
- bash syntax
- shell chaining with `&&`
- shell chaining with `;`
- PowerShell syntax
- Unix shebangs

FORBIDDEN:

```bash
python3 script.py
ls -la
cat arquivo.txt
rm -rf pasta
#!/usr/bin/env python3
```

---

# CMD COMMANDS ONLY

| NEVER USE | USE INSTEAD |
|---|---|
| ls | dir |
| cat | type |
| rm | del / rmdir |
| cp | copy |
| mv | move |
| pwd | cd |
| touch | type nul > arquivo.txt |

VALID COMMANDS:

```cmd
dir
dir src
type arquivo.txt
copy a.txt b.txt
move a.txt pasta\
del arquivo.txt
rmdir /s /q pasta
cd
mkdir logs
```

---

# PYTHON EXECUTION — CRITICAL

ALWAYS USE:

```cmd
python.exe script.py
```

OR:

```cmd
python.exe -m modulo
```

VALID:

```cmd
python.exe run_kilo.py
python.exe diag_env.py
python.exe -m pytest tests -v
```

NEVER USE:

```cmd
python3 script.py
py script.py
python script.py
```

IF `python3` APPEARS:
1. STOP
2. REPLACE WITH `python.exe`
3. RECHECK BEFORE EXECUTION

ASSUME:
- `python3` DOES NOT EXIST
- ONLY `python.exe` IS VALID

THIS IS A HARD RUNTIME CONSTRAINT.

---

# PYTHON VS CMD

USE CMD ONLY FOR:

- navigation
- file copy
- directory listing
- launching Python

USE PYTHON FOR:

- loops
- parsing
- JSON
- transformations
- validation
- file processing
- business logic
- data manipulation

NEVER USE CMD FOR:

- parsing
- loops
- JSON handling
- text processing
- complex automation

---

# UTF-8 RULES

ALL FILE OPERATIONS MUST USE UTF-8.

ALWAYS:

```python
with open(arquivo, "r", encoding="utf-8") as f:
    dados = f.read()
```

```python
with open(arquivo, "w", encoding="utf-8") as f:
    f.write(conteudo)
```

NEVER OMIT ENCODING.

---

# PATH RULES

USE:

```python
from pathlib import Path
```

ALWAYS USE:
- pathlib
- Windows-compatible paths
- UTF-8-safe handling

NEVER:
- assume Linux paths
- use `/`
- hardcode Unix directories

IMPORTANT:

- Paths with accents MAY EXIST
- DO NOT break UTF-8 paths
- DO NOT normalize accents away
- HANDLE Unicode safely

GOOD:

```python
base = Path(r"E:\Projetos\MestreCuca")
arquivo = base / "data" / "arquivo.json"
```

BAD:

```python
path = "/home/user/project"
```

---

# VENV RULES

ALWAYS USE `.venv`

CREATE:

```cmd
python.exe -m venv .venv
```

ACTIVATE:

```cmd
.venv\Scripts\activate.bat
```

INSTALL:

```cmd
python.exe -m pip install -r requirements.txt
```

NEVER INSTALL GLOBALLY.

---

# PROJECT ENTRYPOINTS

MAIN:

```cmd
python.exe run_kilo.py
```

HEALTH:

```cmd
python.exe run_kilo.py --health
```

TESTS:

```cmd
python.exe -m pytest tests -v
```

DIAGNOSTICS:

```cmd
python.exe diag_env.py
python.exe diag_data.py
python.exe run_diag.py
```

---

# PROTECTED FILES

DO NOT MODIFY WITHOUT CONFIRMATION:

```text
config/
.kilo/agents/
.kilo/orchestrators/
.kilo/memory/
prompts/
data/
AGENTS.md
config/ontology.yaml
config/retrieval.yaml
config/embedding.yaml
config/graph.yaml
```

READING IS ALLOWED.

MODIFICATION REQUIRES CONFIRMATION.

---

# GENERATED FILES

DO NOT MANUALLY EDIT:

```text
data/json/
data/embeddings/
data/graphs/
```

REGENERATE USING:

```text
tools/n4_to_json.py
tools/build_embeddings.py
tools/graph_builder.py
```

---

# TEMP FILES

FILES STARTING WITH `_` ARE TEMPORARY.

EXAMPLES:

```text
_audit.py
_debug.py
_temp.py
```

DO NOT:
- import
- depend on
- treat as production code
- refactor around them

---

# STOP AND ASK BEFORE

ASK FOR CONFIRMATION BEFORE:

- deleting files outside `data/`
- changing public interfaces
- modifying configs
- changing schemas
- adding dependencies
- editing protected files
- refactoring multiple modules

WHEN UNSURE:
- create new file
- avoid overwriting existing implementations

---

# CODE RULES

ALWAYS USE:

- type hints
- descriptive names
- explicit exceptions
- pathlib
- UTF-8 encoding

NEVER USE:

- bare `except:`
- silent failures
- dead code
- placeholder `pass`
- commented legacy blocks

GOOD:

```python
except FileNotFoundError as e:
    print(f"Arquivo não encontrado: {e}")
    sys.exit(1)
```

BAD:

```python
except:
    pass
```

---

# ERROR RULES

ERRORS MUST:

- explain what failed
- explain where
- explain why
- explain how to fix

NEVER HIDE ERRORS.

NEVER REDIRECT STDERR.

GOOD:

```cmd
python.exe script.py
```

BAD:

```cmd
python.exe script.py 2> erro.txt
```

---

# FINAL RUNTIME RULES

PRIORITY ORDER:

1. WINDOWS COMPATIBILITY
2. CMD COMPATIBILITY
3. UTF-8 SAFETY
4. EXPLICIT FAILURES
5. PYTHON FOR COMPLEX TASKS
6. NEVER ASSUME UNIX

IF A COMMAND MAY FAIL ON WINDOWS:
1. STOP
2. RECHECK
3. USE PYTHON INSTEAD

THIS PROJECT IS WINDOWS-FIRST.

NEVER GENERATE:
- Linux commands
- Bash syntax
- PowerShell syntax
- python3
- Unix assumptions
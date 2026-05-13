# AGENTS.md

Instruções para agentes de IA trabalhando neste projeto.  
Ambiente: **Windows 11 pt-BR / Python 3.13 / VS Code + Kilo Code**.

---

## Environment

- OS: Windows 11, locale pt-BR, filesystem UTF-8 — paths com acentos são comuns
- Shell: PowerShell (5.1 ou 7+)
- Runtime: Python 3.13
- Package manager: `pip` + `venv`
- Frontend toolchain: Node.js / npm

**This is a Windows-only environment. Never emit Unix, Linux or macOS commands.**  
Commands `ls`, `cat`, `head`, `tail`, `touch`, `chmod`, `grep`, `export`, `source` do not exist here. Do not use them.

---

## Shell — PowerShell

Use PowerShell **only for simple, single-purpose operations** (create folder, copy file, set env var, run a script). Any logic, looping, parsing or error handling must be a Python script instead.

**Always use native PowerShell cmdlets:**

```powershell
Get-ChildItem -Path ".\src"                          # list files (never ls or dir)
New-Item -ItemType Directory -Path ".\logs"           # create folder (never mkdir bare)
New-Item -ItemType File -Path ".\arquivo.txt"         # create file (never touch)
Get-Content -Encoding UTF8 ".\arquivo.txt"            # read file (never cat)
Set-Content -Encoding UTF8 ".\arquivo.txt" -Value ""  # write file
Copy-Item ".\a.txt" -Destination ".\b.txt"
Move-Item ".\a.txt" -Destination ".\pasta\"
Remove-Item ".\pasta" -Recurse -Force
$env:VAR = "valor"                                    # set env var (never export)
```

**Never redirect stderr. Let output flow so the user can see execution:**

```powershell
# ❌ NEVER
python script.py 2>&1
python script.py 2> erros.txt

# ✅ ALWAYS
python script.py
```

**Set encoding before running Python or writing files:**

```powershell
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python script.py
```

Do not chain commands with `&&` or `;`. Use separate lines or a Python script.

---

## Python Scripts

Use a Python script for **any task with more than trivial complexity**: file manipulation, parsing, renaming, API calls, data processing, conditionals, loops, error handling.

**Paths — always use `pathlib`:**

```python
from pathlib import Path

base = Path("C:/Users/nome/Documentos/projeto")  # forward slashes work on Windows
arquivo = base / "dados" / "entrada.csv"          # never string concatenation

if not arquivo.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")
```

**File I/O — always explicit UTF-8:**

```python
with open(path, "r", encoding="utf-8") as f:
    conteudo = f.read()

with open(path, "w", encoding="utf-8") as f:
    f.write(conteudo)
```

**Progress output — always print so the user can follow execution:**

```python
print(f"[✓] Processando: {arquivo}")
print(f"[!] Aviso: {msg}")
print(f"[✗] Erro: {e}")
```

**Error handling — always explicit, never bare `except`:**

```python
import sys

try:
    resultado = processar(arquivo)
    print(f"[✓] Concluído: {resultado}")
except FileNotFoundError as e:
    print(f"[✗] Arquivo não encontrado: {e}")
    sys.exit(1)
except PermissionError as e:
    print(f"[✗] Sem permissão: {e}")
    sys.exit(1)
except Exception as e:
    print(f"[✗] Erro inesperado: {type(e).__name__}: {e}")
    sys.exit(1)
```

Scripts must exit with code `1` on failure and `0` on success.

---

## Virtual Environment

```powershell
# Create
python -m venv .venv

# Activate
.\.venv\Scripts\Activate.ps1

# If blocked by execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install
pip install -r requirements.txt

# Freeze
pip freeze > requirements.txt
```

- Never install packages globally — always activate `.venv` first
- Use `python -m pip` when in doubt about the active Python
- Check if `.venv` exists before creating it

---

## FastAPI / Flask / Django

- Load all configuration from `.env` via `python-dotenv` — never use shell `export`
- Config files and source files must declare `encoding="utf-8"` explicitly
- Use `uvicorn main:app --reload` for FastAPI dev server (run from PowerShell, not a bash script)
- Never assume Unix socket paths or `/tmp` — use `Path` for all temp/output dirs

```python
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
```

---

## React / Next.js

- Use `npm`; do not use `yarn` unless already configured in the project
- Environment variables go in `.env.local` — never in shell exports
- All path references in config files (`next.config.js`, `tailwind.config.js`) must use forward slashes
- Use functional components and hooks; no class components
- Default to TypeScript unless the project already uses plain JavaScript

```powershell
npx create-next-app@latest nome-do-projeto
cd nome-do-projeto
npm run dev
```

---

## Data Science / ML / AI

- Read CSVs with explicit encoding; for Brazilian data use `sep=";"` and `decimal=","`

```python
import pandas as pd
from pathlib import Path

df = pd.read_csv(Path("dados") / "arquivo.csv", encoding="utf-8")

# Brazilian format
df = pd.read_csv(Path("dados") / "br.csv", sep=";", decimal=",", encoding="utf-8")

# Always save with UTF-8
df.to_csv(output_path, index=False, encoding="utf-8")
```

- For large files use `chunksize` — never load everything into memory without checking size first
- Use `joblib` for model persistence; `scikit-learn` conventions for ML pipelines
- Jupyter kernel must point to the project `.venv`

---

## External APIs / Integration

- Always set request timeout — never leave connections open-ended
- Never hardcode secrets, tokens or passwords — load from `.env`
- Validate API responses with `raise_for_status()` before processing
- Use `pydantic` for response schema validation in FastAPI projects

```python
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("MINHA_API_KEY")

response = requests.get(url, headers={"Authorization": f"Bearer {API_KEY}"}, timeout=30)
response.raise_for_status()
data = response.json()
```

---

## File Management

- Create files and folders directly without asking for confirmation
- Follow the existing project structure when extending it
- For new Python projects, always scaffold: `requirements.txt`, `.gitignore`, `README.md`, `.env.example`
- Never commit `.env` — always add it to `.gitignore`; commit only `.env.example`

---

## Code Style

- Python: PEP 8, type hints on function signatures, docstrings for non-trivial functions
- Naming: `snake_case` Python · `camelCase` JS/TS · `kebab-case` files and routes
- Imports: grouped (stdlib → third-party → local), sorted within each group
- No dead code: no `TODO` blocks, no commented-out code, no placeholder `pass` in final output
- Comments: use the same language as the existing codebase; default to Portuguese for new projects

---

## Security

- Never commit API keys, tokens, passwords or secrets
- Always validate external inputs before processing
- Use parameterized queries for all database access — never string-format SQL
- `.env` must always be in `.gitignore`
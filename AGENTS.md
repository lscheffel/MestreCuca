# AGENTS.md — MestreCuca

> Sistema Cognitivo Ontológico · v3.0.0 · 162 células N4 (2×3×3×3×3)  
> Ambiente: **Windows 11 pt-BR / Python 3.13 / pip + venv / VS Code + Kilo Code**

**Primeira ação em qualquer sessão: leia `.kilo/STATE.md`** — estado atual, decisões recentes, bugs conhecidos e workarounds ativos.

Subdiretórios têm seus próprios `AGENTS.md` com regras específicas. Este arquivo contém apenas o que é universal.

---

## Environment

- OS: Windows 11, locale pt-BR, filesystem UTF-8 — paths com acentos são comuns
- Shell: PowerShell (5.1 ou 7+) — **nunca Unix/Linux/macOS**
- Proibido: `ls`, `cat`, `head`, `tail`, `touch`, `chmod`, `grep`, `export`, `source`, `&&`, `;`

---

## Shell — PowerShell

Use PowerShell **só para operações simples**. Qualquer lógica, loop ou parsing vira script Python.

```powershell
Get-ChildItem -Path ".\src"                           # nunca ls
New-Item -ItemType Directory -Path ".\logs"            # nunca mkdir bare
New-Item -ItemType File -Path ".\arquivo.txt"          # nunca touch
Get-Content -Encoding UTF8 ".\arquivo.txt"             # nunca cat
Set-Content -Encoding UTF8 ".\arquivo.txt" -Value ""
Copy-Item ".\a.txt" -Destination ".\b.txt"
Remove-Item ".\pasta" -Recurse -Force
$env:VAR = "valor"                                     # nunca export

# Encoding — sempre antes de rodar Python
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

**Nunca redirecionar stderr** — deixar o output fluir para o usuário acompanhar:

```powershell
# ❌  python script.py 2>&1   |   python script.py 2> erros.txt
# ✅  python script.py
```

---

## Python Scripts

Qualquer complexidade mínima → script Python, não PowerShell.

```python
from pathlib import Path  # sempre pathlib, nunca concatenação de string

base = Path("E:/Arquivos/Área de Trabalho/MestreCuca")
arquivo = base / "data" / "json" / "N4_ALGORITMIA_1_A.json"

# I/O sempre com UTF-8 explícito
with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

# Error handling sempre explícito
import sys
try:
    resultado = processar(arquivo)
except FileNotFoundError as e:
    print(f"[✗] Arquivo não encontrado: {e}"); sys.exit(1)
except Exception as e:
    print(f"[✗] {type(e).__name__}: {e}"); sys.exit(1)
```

- Exit `1` em falha, `0` em sucesso
- Nunca `except:` bare — sempre capturar exceção específica ou `Exception`

---

## Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # se bloqueado: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
pip install -r requirements.txt
pip freeze > requirements.txt
```

- Nunca instalar globalmente — sempre ativar `.venv` antes
- Usar `python -m pip` quando em dúvida sobre qual Python está ativo

---

## Project Map

```
MestreCuca/
├── run_kilo.py          # CLI principal — único entrypoint de produção
├── diag_env.py / diag_data.py / run_diag.py   # diagnósticos
├── rebuild_index.py     # reconstrói índices
├── _*.py                # ⚠️ temporários de auditoria — NÃO modificar/referenciar
│
├── core/                # ⚠️ CRÍTICO — motores (ver core/AGENTS.md)
├── runtime/             # ⚠️ CRÍTICO — pipeline (ver runtime/AGENTS.md)
├── tests/               # pytest (ver tests/AGENTS.md)
├── tools/               # builders de artefatos (ver tools/AGENTS.md)
│
├── config/              # 🔒 PROTEGIDO — fonte da verdade operacional
├── .kilo/               # STATE.md + agentes + memória + orquestradores
├── data/                # 🚫 gerado — nunca editar manualmente
│   ├── json/            # 162 N4 JSONs  →  regenerar: tools/n4_to_json.py
│   ├── embeddings/      # 162 .npy      →  regenerar: tools/build_embeddings.py
│   └── graphs/          # .gexf/.json   →  regenerar: tools/graph_builder.py
├── prompts/             # templates YAML por etapa do pipeline
├── scripts/             # geração em massa de artefatos
└── docs/                # arquitetura, USAGE, roadmaps
```

> `config/` na raiz é primário. `.kilo/config/` é espelho — em conflito, `config/` prevalece.  
> `_*.py` na raiz e em `runtime/` são diagnósticos temporários — não referenciar como padrão.

---

## Entrypoints

```powershell
python run_kilo.py --health                                      # 13 verificações — rodar primeiro
python run_kilo.py --query "como decompor este problema?"        # pipeline full
python run_kilo.py --mode simple     --query "o que é X?"
python run_kilo.py --mode autonomous --query "como otimizar?"
python run_kilo.py --mode interactive
python run_kilo.py --query "teste"   --verbose --log-level DEBUG

python run_diag.py    # grafo ontológico
python diag_env.py    # ambiente e dependências
python diag_data.py   # JSONs, embeddings, índices

python -m pytest tests/ -v
```

> Sem `Makefile`. `.bat` são wrappers — preferir Python direto.

---

## Code Style

- PEP 8, type hints em todas as assinaturas, docstrings em funções não-triviais
- `snake_case` Python · `camelCase` JS/TS · `UPPER_CASE` variáveis de config
- Imports: stdlib → third-party → local, ordenados dentro de cada grupo
- Código e comentários em **português** (padrão do projeto)
- Sem código morto: sem `TODO` soltos, sem blocos comentados, sem `pass` placeholder

---

## Security

- Nunca commitar API keys, tokens ou senhas — carregar do `.env` via `python-dotenv`
- `.env` sempre no `.gitignore`; commitar apenas `.env.example`
- Validar toda entrada externa antes de processar
- Queries SQL sempre parametrizadas — nunca string format

---

## Protected Files

Leia livremente; **nunca modifique sem instrução explícita:**

| Arquivo | Por quê |
|---|---|
| `config/ontology.yaml` | 162 células N4 — alteração quebra todo o pipeline |
| `config/embedding.yaml` | invalida embeddings em `data/embeddings/` |
| `config/graph.yaml` | quebra serialização GEXF |
| `config/retrieval.yaml` | afeta scoring global de retrieval |
| `.kilo/agents/agents.yaml` | configuração dos 6 agentes LLM |
| `.kilo/orchestrators/orchestrators.yaml` | define os 3 pipelines |
| `.kilo/memory/memory.yaml` | níveis de memória |
| `prompts/**/*.yaml` | muda comportamento dos agentes |
| `data/**` | artefatos gerados — regenerar via `tools/` |
| `_*.py` (raiz e runtime/) | diagnósticos temporários |
| `AGENTS.md` (qualquer) | protegido pelo Kilo Code |

---

## When to Stop and Ask

Agir diretamente é o padrão. **Parar e confirmar** antes de:

- Modificar `config/` ou `.kilo/agents/`
- Alterar interface pública em `core/` ou `runtime/` (assinatura, schema, tipo de retorno)
- Deletar arquivo fora de `data/` ou `__pycache__`
- Adicionar dependência ao `requirements.txt`
- Refatorar mais de 2 módulos simultaneamente

Em dúvida: implementar em arquivo novo, nunca sobrescrever sem confirmação.

---

## Engineering Laws (resumo)

1. **TDD** — teste antes do código; cobertura mínima 80% em `core/` e `runtime/`
2. **Zero-Trust** — validar toda entrada com `pydantic`; nunca confiar em retrieval sem verificação
3. **Atomicidade** — commits `tipo(escopo): descrição`; uma coisa por commit
4. **Legibilidade** — nomes descritivos; comentários explicam *por quê*, não *o quê*
5. **Rastreabilidade** — sem issue, sem merge; vincular PR com `Closes #N`
6. **Consistência** — terminologia de `config/ontology.yaml`; formatação via `ruff`/`black`
7. **Defesa em Profundidade** — validar na entrada, na saída e no armazenamento
8. **Falha Explícita** — erro deve dizer *o quê*, *por quê*, *onde* e *como corrigir*
9. **Documentação Viva** — atualizar README, STATE.md e CHANGELOG junto com o código
10. **Revisão Obrigatória** — todo PR precisa de ≥1 aprovação

**Branches:** `feat/123-descricao` · `fix/` · `docs/` · `refactor/` · `test/` · `chore/`
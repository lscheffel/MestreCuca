# Relatório de Verificação da Estrutura do Root

> **Gerado em:** 2026-05-13  
> **Fonte:** Saída de `tree /F /A` do terminal  
> **Status:** ⚠️ Problemas identificados

---

## ✅ Estrutura Correta

### Diretórios protegidos — OK
| Diretório | Status |
|-----------|--------|
| `.git/` | ✅ Presente |
| `.github/` | ✅ Presente |
| `.kilo/` | ✅ Presente (agentes, config, memory, orchestrators, prompts) |
| `.pytest_cache/` | ✅ Presente |
| `__pycache__/` | ✅ Presente (raiz) |
| `config/` | ✅ Presente (embedding.yaml, graph.yaml, ontology.yaml, retrieval.yaml) |
| `core/` | ✅ Presente (AGENTS.md + motores + __pycache__) |
| `data/` | ✅ Presente (subdirs: embeddings/, graphs/, indexes/, json/, sessions/) |
| `runtime/` | ✅ Presente (classifier, orchestrator, retriever, router, synthesizer, validator) |

### Diretórios reorganizados — OK
| Diretório | Status |
|-----------|--------|
| `docs/agentes-prompts/` | ✅ 8 arquivos |
| `docs/arquitetura/` | ✅ 6 arquivos |
| `docs/auditoria-qualidade/` | ✅ 1 arquivo |
| `docs/ontologia-taxonomia/` | ✅ 9 arquivos |
| `docs/planejamento-roadmap/` | ✅ 4 arquivos + `roadmap/` (4 itens) |
| `docs/referencia-historico/` | ✅ 1 arquivo |
| `docs/runtime-pipeline/` | ✅ 1 arquivo |
| `docs/uso-documentacao/` | ✅ 2 arquivos |
| `scripts/` | ✅ 12 arquivos (builders + auxiliares) |
| `tests/` | ✅ Presente (conftest.py, test_classifier.py, test_ontology.py, test_retrieval.py, test_fase3.py) |
| `tools/` | ✅ Presente (AGENTS.md + builders + __pycache__) |
| `prompts/` | ✅ Presente (classifier, retrieval, routing, synthesis, validation) |

### Entrypoints — OK
| Arquivo | Status |
|---------|--------|
| `run_kilo.py` | ✅ Presente |
| `run_diag.py` | ✅ Presente |
| `diag_env.py` | ✅ Presente |
| `diag_data.py` | ✅ Presente |
| `diag.py` | ✅ Presente |
| `diag2.py` | ✅ Presente |
| `diag_validator.py` | ✅ Presente |
| `rebuild_index.py` | ✅ Presente |

### Documentação raiz — OK
| Arquivo | Status |
|---------|--------|
| `README.md` | ✅ Presente |
| `AGENTS.md` | ✅ Presente |
| `CHANGELOG.md` | ✅ Presente |
| `CONTRIBUTING.md` | ✅ Presente |
| `MEMORY.md` | ✅ Presente |
| `STATES.md` | ✅ Presente |
| `requirements.txt` | ✅ Presente |

---

## ⚠️ Problemas Identificados

### PROBLEMA 1 — `ontology/` está vazio (CRÍTICO)

```
ontology/
├── n0/     (.gitkeep)
├── n1/     (.gitkeep)
├── n2/     (.gitkeep)
├── n3/     (.gitkeep)
└── n4/     (.gitkeep)
```

**O que aconteceu:** Os ~162+ arquivos N3 e N4 (ex.: `N3-1_1_1-LOGOS-RESOLUÇÃO.md`, `N4-1_1_1-LOGOS-DECOMPOSIÇÃO.md`, etc.) **não estão mais no `ontology/`** nem em nenhum outro diretório visível.

**Onde eles deveriam estar:**
- `data/json/` contém os JSONs gerados (162 arquivos) ✅
- Mas os `.md` originais da ontologia **sumiram**

**Ação necessária:** Verificar se foram deletados acidentalmente ou movidos para um local não rastreado. Se foram deletados, restaurar do git.

---

### PROBLEMA 2 — Arquivos soltos em `data/` (NÃO DEVERIAM ESTAR LÁ)

```
data/
├── semantic_expansion_report.md    ← deveria estar em docs/
├── taxo.txt                        ← deveria estar em docs/ontologia-taxonomia/
├── test_results.csv                ← output de teste (considerar remover)
├── test_results.json               ← output de teste (considerar remover)
```

**Ação necessária:**
- `semantic_expansion_report.md` → mover para `docs/ontologia-taxonomia/` ou `docs/runtime-pipeline/`
- `taxo.txt` → mover para `docs/ontologia-taxonomia/`
- `test_results.csv` / `test_results.json` → mover para `tests/` ou remover se obsoletos

---

### PROBLEMA 3 — Arquivo de documentação em `tests/`

```
tests/
├── ONTO_ENGINE_ROADMAP-DEEP.md    ← arquivo de documentação, não teste
```

**Ação necessária:** Mover para `docs/planejamento-roadmap/`

---

### PROBLEMA 4 — Scripts `.bat` em `scripts/`

```
scripts/
├── run_diag.bat
├── run_test.bat
```

**Conforme AGENTS.md:** "Sem Makefile. .bat são wrappers — preferir Python direto."

**Ação necessária:** Verificar se esses `.bat` são necessários. Se não forem, remover. Caso contrário, documentar a razão.

---

### PROBLEMA 5 — Diagnósticos temporários em `runtime/`

```
runtime/
├── _diag_check_celulas.py
├── _diag_validator4.py
├── _diag_validator5.py
```

**Conforme AGENTS.md:** `_*.py` na raiz e em `runtime/` são diagnósticos temporários — não referenciar como padrão.

**Ação necessária:** Mover para `scripts/` ou para o root (se são diagnósticos pontuais).

---

### PROBLEMA 6 — `data/indexes/` vazio

```
data/indexes/
├── .gitkeep
```

**Ação necessária:** Verificar se este diretório é necessário ou se é artefato de uma geração anterior.

---

## 📊 Resumo

| Categoria | Contagem |
|-----------|----------|
| ✅ OK | 13 diretórios, ~30+ arquivos corretos |
| ⚠️ Problemas | 6 itens |
| 🔴 Crítico | 1 (ontology/ vazio) |
| 🟡 Médio | 3 (arquivos em data/, doc em tests/, .bat em scripts/) |
| 🟢 Baixo | 2 (diagnósticos em runtime/, indexes/ vazio) |

---

## Próximos Passos

1. **Imediato:** Verificar se os arquivos `.md` da ontologia foram deletados ou estão em algum branch/stash do git
2. **Prioridade média:** Mover arquivos soltos de `data/` para seus destinos corretos
3. **Prioridade baixa:** Limpar `.bat`, diagnósticos em `runtime/`, `indexes/` vazio
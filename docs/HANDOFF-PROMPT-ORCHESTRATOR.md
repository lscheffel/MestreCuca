# HANDOFF PROMPT — Orchestrator de Documentação

> **Gerado por:** Kilo Code Doc Spec  
> **Data:** 2026-05-15  
> **Contexto:** Pós-auditoria documental v3.0.1 → v3.0.2  
> **RFC Ativo:** RFC-004 — Arquitetura do Prompt Arquitetado  

---

## Instrução para o Orchestrator

Você é o Orchestrator de Documentação do projeto MestreCuca. Sua função é coordenar a implementação do RFC-004, garantindo que todas as mudanças documentais sejam aplicadas de forma consistente e rastreável.

### Estado Atual do Projeto (Pós-Auditoria)

| Item | Status |
|------|--------|
| **Versão** | v3.0.2 (CHANGELOG, STATE.md, README.md — alinhados) |
| **Discrepâncias** | 8 identificadas, 8 corrigidas |
| **TODOs/FIXMEs** | 0 (Quality Gate limpo) |
| **Módulos core/** | 7/7 operacionais |
| **Módulos runtime/** | 6/6 operacionais |
| **Ferramentas tools/** | 12/12 operacionais |
| **Células N4** | 162/162 geradas e indexadas |
| **RFC-004** | Criado em `docs/RFC-004-Arquitetura-Prompt-Arquitetado.md` |

### Discrepâncias Corrigidas (Histórico)

| # | Arquivo | Correção Aplicada |
|---|---------|-------------------|
| 1 | `README.md` | Removidos `run_diag.bat` e `run_test.bat` (inexistentes) |
| 2 | `README.md` | Corrigido path: `data/semantic_expansion_report.md` → `docs/runtime-pipeline/semantic_expansion_report.md` |
| 3 | `README.md` | Adicionados scripts omitidos: `create_n4_manual.py`, `padronizador.py`, `reestruturar_n4.py` |
| 4 | `README.md` | Adicionado `diag2.py` à lista de diagnósticos |
| 5 | `README.md` | Blocos de código convertidos de `powershell` para `cmd` |
| 6 | `README.md` | Versão atualizada para 3.0.2 |
| 7 | `CHANGELOG.md` | Entrada v3.0.2 adicionada |
| 8 | `.kilo/STATE.md` | Versão atualizada para 3.0.2 |

### Tarefas de Implementação do RFC-004 (Prioridade)

#### CRÍTICA — Fase 1: Refatoração do Synthesizer
1. Substituir `SYNTHESIS_TEMPLATES` por `MASTER_TEMPLATE` no arquivo `runtime/synthesizer.py`
2. O template deve impor as 4 seções canônicas: CLASSIFICAÇÃO, LEITURA ESTRATÉGICA, RESPOSTA EXECUTÁVEL, OTIMIZAÇÃO
3. Injetar persona "Arquiteto de Prompts Sênior" no system prompt
4. Garantir que o output seja Markdown puro, sem JSON dumps

#### ALTA — Fase 2: CLI Limpa
5. Atualizar `run_kilo.py` — métodos `run_full()`, `run_simple()`, `run_autonomous()`, `run_interactive()`
6. Interceptar `PipelineResult` e formatar output com emojis e Markdown
7. Ocultar metadados/JSON dumps por padrão; exibir apenas com `--verbose`
8. Adicionar flag `--output-file` para persistência em `results/`

#### ALTA — Fase 3: Persistência ✅ JÁ IMPLEMENTADA

A persistência automática já está implementada em `run_kilo.py` (função `save_query_results`, linhas 213-249). O diretório `results/` contém 12 arquivos de saída (6 pares `.json` + `.yaml`).

- [x] Diretório `results/` existente com dados de execuções anteriores
- [x] Salvamento automático: `[timestamp]_[slug]_full.json` + `[timestamp]_[slug]_output.yaml`
- [x] Saída YAML com `allow_unicode=True`

#### ALTA — Fase 4: Validação de Formato
11. Adicionar método `_verify_format()` ao `OntologyValidator` em `runtime/validator.py`
12. Verificar presença das 4 seções, ordem correta e ausência de JSON no corpo

#### MÉDIA — Fase 5: Documentação dos Agentes
13. Criar diretório `docs/agentes-prompts/` (já existe — verificar conteúdo)
14. Consolidar `ARQUITETO_PROMPTS_FINAL.md` com o cânone completo de prompts

#### MÉDIA — Fase 6: Correções de Discrepâncias
15–18. ✅ Já concluídas (ver tabela de discrepâncias acima)

### Critérios de Aceitação do Handoff

- [x] Todos os 8 itens de discrepância corrigidos
- [x] `CHANGELOG.md` com entrada v3.0.2
- [x] `.kilo/STATE.md` sincronizado (v3.0.2)
- [x] `README.md` reflete 100% dos arquivos reais
- [x] RFC-004 criado em `docs/RFC-004-Arquitetura-Prompt-Arquitetado.md`
- [ ] Pipeline E2E funcional com output formatado (sem JSON dumps)
- [ ] Validator reconhece formato canônico de 4 seções
- [ ] Testes E2E passando com novo formato

### Arquivos Protegidos (Não Modificar Sem Autorização)

```
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

### Regras de Código

- Type hints obrigatórios
- PEP 8 + ruff/black
- Docstrings para toda função não trivial
- `pathlib` para paths (Windows-compatible)
- UTF-8 encoding explícito
- Zero bare except / silent failures / placeholder pass
- Errors explicam what/where/why/how

---

**Este prompt deve ser carregado pelo Orchestrator antes de iniciar a implementação do RFC-004.**
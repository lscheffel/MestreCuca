# Relatório de Classificação de Arquivos do Root

> Gerado em: 2026-05-13
> Diretório base: `E:/Arquivos/Área de Trabalho/MestreCuca`

---

## 1. Resumo Executivo

O root do projeto contém **~80+ arquivos** e **16 diretórios**. Grande parte dos arquivos soltos no root pertencem a categorias que já possuem diretórios existentes (`docs/`, `scripts/`, `tests/`, `data/`). Outros são diagnósticos temporários (prefixados com `_`) que, por convenção do projeto, devem permanecer no root.

---

## 2. Arquivos Movidos — Origem → Destino

### → `docs/` (Documentação)

| # | Arquivo | Justificativa |
|---|---------|---------------|
| 1 | `AGENTE - ARQUITETO DE PROMPTS FINAL V1.md` | Documentação de design de prompts |
| 2 | `agente_arquiteto_prompts_v_1_1_consolidado.md` | Documentação de design de prompts |
| 3 | `agente_arquiteto_prompts_v_2_arquitetura_cognitiva_consolidada.md` | Documentação de arquitetura cognitiva |
| 4 | `AGENTS (deprecated).md` | Documentação deprecada (manter para referência histórica) |
| 5 | `ARQUITETO_PROMPTS_FINAL.md` | Documentação de arquitetura |
| 6 | `arquitetura_cognitiva_v3.md` | Documentação de arquitetura |
| 7 | `auditoria_discrepancias_ontologicas.md` | Relatório de auditoria |
| 8 | `checklist_recursivo_N3.md` | Checklist/documentação de processo |
| 9 | `CORE.md` | Documentação do núcleo do sistema |
| 10 | `CORE2.md` | Documentação do núcleo do sistema (continuação) |
| 11 | `DSL.md` | Documentação de DSL |
| 12 | `expansao_fractal_n3.md` | Documentação de expansão fractal |
| 13 | `gpt 0.1 - arquiteto.md` | Registro de versão do arquiteto |
| 14 | `gpt 1.0 - arquiteto.md` | Registro de versão do arquiteto |
| 15 | `gpt 1.0.md` | Registro de versão |
| 16 | `ONTOLOGIA_MESTRA_DOMINANTE_V1.md` | Documentação da ontologia |
| 17 | `ONTOLOGIA_MESTRA_DOMINANTE_V2.md` | Documentação da ontologia (v2) |
| 18 | `plan.md` | Documentação de planejamento |
| 19 | `plano_transformacao_n4_json.md` | Plano de transformação |
| 20 | `PROMPT_MODULAR_N3.md` | Template/documentação de prompt |
| 21 | `relatorio_analise_ontologia.md` | Relatório de análise |
| 22 | `roadmap.md` | Roadmap do projeto |
| 23 | `RUNTIME.md` | Documentação de runtime |
| 24 | `SUMARIO_EXECUTIVO_MUDANÇAS.md` | Sumário executivo |
| 25 | `taxon_ontology_tree.mmd` | Diagrama de taxonomia |
| 26 | `Taxonomia_Ontologica.md` | Documentação de taxonomia |

### → `scripts/` (Scripts de Automação/Geração)

| # | Arquivo | Justificativa |
|---|---------|---------------|
| 1 | `create_n3_files.py` | Geração em massa de artefatos N3 |
| 2 | `create_n3_files_v2.py` | Geração em massa de artefatos N3 (v2) |
| 3 | `create_n4_files.py` | Geração em massa de artefatos N4 |
| 4 | `create_n4_from_taxonomy.py` | Geração de N4 a partir de taxonomia |
| 5 | `create_n4_manual.py` | Geração manual de N4 |
| 6 | `padronizador.py` | Utilitário de padronização |
| 7 | `reestruturar_n4.py` | Script de reestruturação de N4 |
| 8 | `run_diag.bat` | Wrapper de diagnóstico (.bat) |
| 9 | `run_test.bat` | Wrapper de teste (.bat) |

### → `tests/` (Testes)

| # | Arquivo | Justificativa |
|---|---------|---------------|
| 1 | `test_fase3` | Teste da fase 3 (sem extensão, renomear para `.py`) |
| 2 | `test_retrieval.py` | Teste de retrieval e2e |

### → `data/` (Dados)

| # | Arquivo | Justificativa |
|---|---------|---------------|
| 1 | `taxo.txt` | Dado de taxonomia (dado estruturado, não gerado) |

---

## 3. Diretórios Criados

Nenhum diretório novo precisa ser criado. Todos os diretórios-alvo já existem:
- `docs/` ✅ já existe
- `scripts/` ✅ já existe
- `tests/` ✅ já existe
- `data/` ✅ já existe

---

## 4. Arquivos que Permanecem no Root (com Justificativa)

### Protegidos / Manifesto do Ecossistema

| Arquivo | Justificativa |
|---------|---------------|
| `README.md` | Documentação principal de apresentação — obrigatório no root |
| `LICENSE` | Licença do projeto — obrigatório no root |
| `.gitignore` | Regras de exclusão VCS — obrigatório no root |
| `AGENTS.md` | Documentação de agentes LLM — protegido pelo Kilo Code |
| `CHANGELOG.md` | Changelog — obrigatório no root |
| `CONTRIBUTING.md` | Guia de contribuição — documentação de projeto |
| `requirements.txt` | Manifesto de dependências Python — obrigatório no root |

### Entrypoints de Produção/Diagnóstico

| Arquivo | Justificativa |
|---------|---------------|
| `run_kilo.py` | CLI principal — único entrypoint de produção |
| `run_diag.py` | Entrypoint de diagnóstico (listado em Entrypoints) |
| `diag_env.py` | Diagnóstico de ambiente (listado em Entrypoints) |
| `diag_data.py` | Diagnóstico de dados (listado em Entrypoints) |
| `rebuild_index.py` | Reconstrução de índices (listado em Entrypoints) |

### Diagnósticos Temporários (prefixo `_`)

> Estes arquivos são explicitamente marcados como "⚠️ temporários de auditoria — NÃO modificar/referenciar" no AGENTS.md do projeto.

| Arquivo | Tipo |
|---------|------|
| `_audit_refs.py` | Script de auditoria |
| `_audit_scripts.py` | Script de auditoria |
| `_check_n3_refs.py` | Script de verificação N3 |
| `_diag.py` | Diagnóstico |
| `_diag_output.txt` | Output de diagnóstico |
| `_diag_output2.txt` | Output de diagnóstico |
| `_diag_validator2.py` | Validador de diagnóstico |
| `_diag_validator3.py` | Validador de diagnóstico |
| `_explore.py` | Script de exploração |
| `_fase3_result.txt` | Resultado da fase 3 |
| `_fix_paths.py` | Utilitário de correção de paths |
| `_inspect_data.py` | Inspeção de dados |
| `_inspect_output.txt` | Output de inspeção |
| `_move_ontology.py` | Utilitário de movimentação |
| `_move_status.txt` | Status de movimentação |
| `_run_fase4.py` | Runner da fase 4 |
| `_run_validate.py` | Runner de validação |
| `_test_fase4.py` | Teste da fase 4 |
| `_test_retrieval_e2e.py` | Teste e2e de retrieval |
| `_validate_fase3.py` | Validador da fase 3 |

### Outros no Root

| Arquivo | Justificativa |
|---------|---------------|
| `diag.py` | Script de diagnóstico (entrypoint complementar) |
| `diag2.py` | Script de diagnóstico (variante) |
| `diag_validator.py` | Validador de diagnóstico |
| `diag_output.txt` | Output de diagnóstico |
| `MEMORY.md` | Memória do projeto (análogo a STATE.md) |
| `STATES.md` | Estados do projeto |

### Diretórios Protegidos / de Sistema

| Diretório | Justificativa |
|-----------|---------------|
| `.git/` | Sistema VCS — nunca mover |
| `.github/` | Configuração CI/CD — nunca mover |
| `.kilo/` | Estado do agente — protegido |
| `.pytest_cache/` | Cache de testes — sistema |
| `__pycache__/` | Bytecode Python — sistema |
| `config/` | Configuração protegida |
| `core/` | Código-fonte crítico |
| `runtime/` | Pipeline crítico |
| `data/` | Dados gerados |
| `prompts/` | Templates do pipeline |

---

## 5. Arquivos Não Categorizados

| Arquivo | Tamanho | Sugestão de Destino |
|---------|---------|---------------------|
| `null` | 49 bytes | Verificar conteúdo. Possivelmente um placeholder ou arquivo de erro remanescente. Se vazio/sem utilidade, deletar. Caso contenha dado, mover para `data/`. |

---

## 6. Diretório `ontology/` — Análise Especial

O diretório `ontology/` contém **162+ arquivos Markdown** de definição ontológica (N3 e N4) que são **dados fonte** do pipeline, não artefatos gerados. Não se encaixa perfeitamente em nenhuma categoria:

- **Não é `docs/`** — são dados estruturados do domínio, não documentação explicativa
- **Não é `data/json/`** — são fontes Markdown, não JSONs gerados
- **Não é `config/`** — não configura o sistema

**Recomendação:** Manter `ontology/` no root como diretório de primeiro-class citizen, ou renomear para `data/ontology-source/` para diferenciar dos dados gerados em `data/json/`.

---

## 7. Estado Final da Árvore (Proposto)

```
MestreCuca/
├── .git/
├── .github/
├── .kilo/
├── .pytest_cache/
├── __pycache__/
├── config/              🔒 protegido
├── core/                🔒 protegido
├── data/                🚫 gerado
│   ├── json/
│   ├── embeddings/
│   ├── graphs/
│   └── taxo.txt         ← MOVIDO do root
├── docs/                ✅ recebe 26 arquivos
│   ├── USAGE.md
│   ├── USAGE.pdf
│   ├── arquitetura_sistema_cognitivo.md/.pdf
│   ├── roadmap/
│   ├── + 21 arquivos movidos do root
├── ontology/            ⚠️ análise especial (ver seção 6)
├── prompts/
├── runtime/             🔒 protegido
├── scripts/             ✅ recebe 9 arquivos
├── tests/               ✅ recebe 2 arquivos
├── tools/
├── LICENSE
├── README.md
├── AGENTS.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── MEMORY.md
├── STATES.md
├── requirements.txt
├── run_kilo.py
├── run_diag.py
├── diag_env.py
├── diag_data.py
├── rebuild_index.py
├── diag.py
├── diag2.py
├── diag_validator.py
├── diag_output.txt
├── _audit_refs.py
├── _audit_scripts.py
├── _check_n3_refs.py
├── _diag.py
├── _diag_output.txt
├── _diag_output2.txt
├── _diag_validator2.py
├── _diag_validator3.py
├── _explore.py
├── _fase3_result.txt
├── _fix_paths.py
├── _inspect_data.py
├── _inspect_output.txt
├── _move_ontology.py
├── _move_status.txt
├── _run_fase4.py
├── _run_validate.py
├── _test_fase4.py
├── _test_retrieval_e2e.py
├── _validate_fase3.py
└── null                 ❓ não categorizado
```

---

## 8. Estatísticas

| Métrica | Quantidade |
|---------|------------|
| Arquivos no root (antes) | ~80 |
| Arquivos para mover | **38** |
| → `docs/` | 26 |
| → `scripts/` | 9 |
| → `tests/` | 2 |
| → `data/` | 1 |
| Arquivos que permanecem no root | **~42** |
| → Protegidos/manifesto | 7 |
| → Entrypoints | 5 |
| → Diagnósticos temporários (`_*.py/txt`) | 20 |
| → Outros | 5 |
| Diretórios protegidos/sistema | 12 |
| Não categorizados | 1 (`null`) |

---

## 9. Próximos Passos

Aguardando instrução do usuário para:
1. ✅ ou ❌ Aprovar o relatório
2. Executar as movimentações conforme aprovado
3. Decidir o destino do diretório `ontology/`
4. Decidir o destino do arquivo `null`
5. Limpar `_scan_tree.py` (script de varredura temporário)
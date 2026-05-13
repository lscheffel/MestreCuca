# Relatório de Classificação e Organização do Root — MestreCuca

> **Gerado em:** 2026-05-13  
> **Diretório base:** `E:/Arquivos/Área de Trabalho/MestreCuca`  
> **Status:** Fases 1–3 concluídas. Relatório final consolidado abaixo.

---

## 1. Resumo das Operações Realizadas

| Fase | Descrição | Resultado |
|------|-----------|-----------|
| **Fase 1** | Classificação e movimentação de arquivos soltos no root | 38 arquivos movidos, 3 deletados |
| **Fase 2** | Ajustes finais (scripts auxiliares → `scripts/`, rename de `test_fase3`) | 6 operações |
| **Fase 3** | Organização temática de `docs/` em 8 subdiretórios | 34 arquivos reorganizados |

---

## 2. Diretórios do Root — Classificação

### 2.1 Diretórios Protegidos / Sistema (não mexer)

| Diretório | Classificação | Justificativa |
|-----------|--------------|---------------|
| `.git/` | 🔒 Sistema | Controle de versão — nunca manipular |
| `.github/` | 🔒 Sistema | Configuração de CI/CD e templates |
| `.kilo/` | 🔒 Sistema | Configuração de agentes, memória, orquestradores |
| `.pytest_cache/` | 🔒 Sistema | Cache do pytest — gerado automaticamente |
| `__pycache__/` | 🔒 Sistema | Bytecode Python — gerado automaticamente |

### 2.2 Diretórios Protegidos / Funcionais (não mexer)

| Diretório | Classificação | Justificativa |
|-----------|--------------|---------------|
| `config/` | 🔒 Protegido | Fonte da verdade operacional (ontology.yaml, embedding.yaml, etc.) |
| `core/` | 🔒 Protegido | Motores do sistema — código-fonte principal |
| `runtime/` | 🔒 Protegido | Pipeline de execução |
| `data/` | 🔒 Protegido | Artefatos gerados (JSONs, embeddings, grafos) |

### 2.3 Diretórios Funcionais (já organizados)

| Diretório | Classificação | Conteúdo |
|-----------|--------------|----------|
| `docs/` | 📚 Documentação | 8 subdiretórios, 34 arquivos organizados por contexto |
| `scripts/` | 🔧 Ferramenta/Automação | Scripts auxiliares de build, reorganização e verificação |
| `tests/` | 🧪 Teste | Testes unitários e de integração |
| `tools/` | 🔧 Ferramenta/Automação | Builders de artefatos (N4→JSON, embeddings, grafos) |
| `prompts/` | ⚙️ Configuração | Templates YAML do pipeline |
| `ontology/` | 📁 Dados (fonte) | 162+ arquivos N3/N4 de origem (mantido no root por decisão) |

---

## 3. Arquivos no Root — Classificação Individual

### 3.1 Arquivos Protegidos — Permanecem no Root

| Arquivo | Classificação | Justificativa |
|---------|--------------|---------------|
| `README.md` | 📚 Documentação | Documentação principal de apresentação do projeto |
| `CHANGELOG.md` | 📚 Documentação | Registro de alterações do projeto |
| `CONTRIBUTING.md` | 📚 Documentação | Guia de contribuição |
| `MEMORY.md` | 📚 Documentação | Memória operacional do projeto |
| `STATES.md` | 📚 Documentação | Estados e decisões do projeto |
| `requirements.txt` | 📦 Manifesto | Dependências Python — manifesto do ecossistema |
| `run_kilo.py` | 🚀 Entrypoint | CLI principal — único entrypoint de produção |
| `AGENTS.md` | 📚 Documentação | Regras do sistema cognitivo — protegido pelo Kilo Code |

### 3.2 Entrypoints de Diagnóstico — Permanecem no Root

| Arquivo | Classificação | Justificativa |
|---------|--------------|---------------|
| `run_diag.py` | 🔧 Diagnóstico | Entrypoint de diagnóstico (documentado no AGENTS.md) |
| `diag_env.py` | 🔧 Diagnóstico | Diagnóstico de ambiente e dependências |
| `diag_data.py` | 🔧 Diagnóstico | Diagnóstico de dados (JSONs, embeddings, índices) |
| `diag.py` | 🔧 Diagnóstico | Diagnóstico principal (grafo ontológico) |
| `diag2.py` | 🔧 Diagnóstico | Diagnóstico secundário |
| `diag_validator.py` | 🔧 Diagnóstico | Validador de diagnóstico |
| `diag_output.txt` | 📋 Output | Resultado de execução de `diag.py` |
| `rebuild_index.py` | 🔧 Diagnóstico | Reconstrói índices de busca |

### 3.3 Arquivos Temporários de Diagnóstico (prefixo `_`) — Permanecem no Root

> Conforme AGENTS.md: `_*.py` na raiz são diagnósticos temporários — não referenciar como padrão.

| Arquivo | Tipo | Classificação |
|---------|------|--------------|
| `_audit_refs.py` | Script | Diagnóstico temporário |
| `_audit_scripts.py` | Script | Diagnóstico temporário |
| `_check_n3_refs.py` | Script | Diagnóstico temporário |
| `_diag.py` | Script | Diagnóstico temporário |
| `_diag_validator2.py` | Script | Diagnóstico temporário |
| `_diag_validator3.py` | Script | Diagnóstico temporário |
| `_explore.py` | Script | Diagnóstico temporário |
| `_fix_paths.py` | Script | Diagnóstico temporário |
| `_inspect_data.py` | Script | Diagnóstico temporário |
| `_move_ontology.py` | Script | Diagnóstico temporário |
| `_run_fase4.py` | Script | Diagnóstico temporário |
| `_run_validate.py` | Script | Diagnóstico temporário |
| `_test_fase4.py` | Script | Diagnóstico temporário |
| `_test_retrieval_e2e.py` | Script | ⚠️ Teste E2E real — considerar mover para `tests/` |
| `_validate_fase3.py` | Script | Diagnóstico temporário |
| `_final_adjustments.py` | Script | Script auxiliar de ajustes |
| `_organize_docs.py` | Script | Script auxiliar de organização de docs |
| `_verify_docs.py` | Script | Script auxiliar de verificação de docs |
| `_verify_final.py` | Script | Script auxiliar de verificação final |

### 3.4 Arquivos de Output / Log — Permanecem no Root

| Arquivo | Tipo | Classificação |
|---------|------|--------------|
| `_diag_output.txt` | Log | Output de diagnóstico temporário |
| `_diag_output2.txt` | Log | Output de diagnóstico temporário |
| `_docs_reorg_log.txt` | Log | Log da reorganização de docs/ |
| `_fase3_result.txt` | Log | Resultado da Fase 3 |
| `_inspect_output.txt` | Log | Output de inspeção |
| `_move_status.txt` | Log | Status de movimentação |
| `_reorg_log.txt` | Log | Log da reorganização do root |
| `_tree_final.txt` | Log | Árvore final do root |
| `diag_output.txt` | Log | Output de diag.py |
| `fase3_output.txt` | Log | Output da Fase 3 |
| `test_output.txt` | Log | Output de teste |

### 3.5 Relatórios — Permanecem no Root

| Arquivo | Classificação |
|---------|--------------|
| `_relatorio_classificacao.md` | Relatório de classificação inicial |
| `_relatorio_final.md` | Relatório final consolidado |

---

## 4. Arquivos Não Categorizados (com Sugestão de Destino)

| Arquivo | Sugestão de Destino | Razão |
|---------|---------------------|-------|
| `_test_retrieval_e2e.py` | `tests/` | É um teste E2E legítimo, apesar do prefixo `_`. Renomear para `test_retrieval_e2e.py`. |
| `_final_adjustments.py` | `scripts/` | Script auxiliar de ajustes pós-reorganização. |
| `_organize_docs.py` | `scripts/` | Script de organização de documentação. |
| `_verify_docs.py` | `scripts/` | Script de verificação de docs. |
| `_verify_final.py` | `scripts/` | Script de verificação final. |
| `_move_ontology.py` | `scripts/` | Script de movimentação de ontologia. |

> **Nota:** Todos os arquivos acima possuem prefixo `_` que os marca como temporários/diagnósticos. A decisão de movê-los para `scripts/` ou mantê-los no root depende da intenção do usuário: se são utilitários recorrentes, devem ir para `scripts/`; se são artefatos de uma sessão específica, podem permanecer no root.

---

## 5. Árvore Final do Root

```
MestreCuca/
│
├── .git/                          🔒 Sistema
├── .github/                       🔒 Sistema
├── .kilo/                         🔒 Sistema (agentes, memória, orquestradores)
├── .pytest_cache/                 🔒 Sistema
├── __pycache__/                   🔒 Sistema
│
├── config/                        🔒 Protegido (ontology, embedding, graph, retrieval)
├── core/                          🔒 Protegido (motores do sistema)
├── data/                          🔒 Protegido (JSONs, embeddings, grafos)
│   ├── json/
│   ├── embeddings/
│   └── graphs/
├── runtime/                       🔒 Protegido (pipeline de execução)
│
├── docs/                          📚 Documentação organizada
│   ├── arquitetura/               (6 arquivos)
│   ├── agentes-prompts/           (8 arquivos)
│   ├── ontologia-taxonomia/       (9 arquivos)
│   ├── planejamento-roadmap/      (4 arquivos + roadmap/)
│   ├── runtime-pipeline/          (1 arquivo)
│   ├── auditoria-qualidade/       (1 arquivo)
│   ├── referencia-historico/      (1 arquivo)
│   └── uso-documentacao/          (2 arquivos)
│
├── ontology/                      📁 Fonte N3/N4 (162+ arquivos, mantido por decisão)
├── prompts/                       ⚙️ Templates YAML do pipeline
├── scripts/                       🔧 Scripts auxiliares
├── tests/                         🧪 Testes
├── tools/                         🔧 Builders de artefatos
│
├── run_kilo.py                    🚀 CLI principal
├── run_diag.py                    🔧 Entrypoint de diagnóstico
├── diag_env.py                    🔧 Diagnóstico de ambiente
├── diag_data.py                   🔧 Diagnóstico de dados
├── diag.py                        🔧 Diagnóstico principal
├── diag2.py                       🔧 Diagnóstico secundário
├── diag_validator.py              🔧 Validador
├── rebuild_index.py               🔧 Reconstrói índices
│
├── _audit_refs.py                 ⚠️ Diagnóstico temporário
├── _audit_scripts.py              ⚠️ Diagnóstico temporário
├── _check_n3_refs.py              ⚠️ Diagnóstico temporário
├── _diag.py                       ⚠️ Diagnóstico temporário
├── _diag_output.txt               ⚠️ Output temporário
├── _diag_output2.txt              ⚠️ Output temporário
├── _diag_validator2.py            ⚠️ Diagnóstico temporário
├── _diag_validator3.py            ⚠️ Diagnóstico temporário
├── _docs_reorg_log.txt            ⚠️ Log temporário
├── _explore.py                    ⚠️ Diagnóstico temporário
├── _fase3_result.txt              ⚠️ Output temporário
├── _final_adjustments.py          ⚠️ Script auxiliar
├── _fix_paths.py                  ⚠️ Diagnóstico temporário
├── _inspect_data.py               ⚠️ Diagnóstico temporário
├── _inspect_output.txt            ⚠️ Output temporário
├── _move_ontology.py              ⚠️ Script auxiliar
├── _move_status.txt               ⚠️ Log temporário
├── _organize_docs.py              ⚠️ Script auxiliar
├── _relatorio_classificacao.md    ⚠️ Relatório temporário
├── _relatorio_final.md            ⚠️ Relatório final
├── _reorg_log.txt                 ⚠️ Log temporário
├── _run_fase4.py                  ⚠️ Diagnóstico temporário
├── _run_validate.py               ⚠️ Diagnóstico temporário
├── _test_fase4.py                 ⚠️ Diagnóstico temporário
├── _test_retrieval_e2e.py         ⚠️ Teste E2E (considerar → tests/)
├── _tree_final.txt                ⚠️ Log temporário
├── _validate_fase3.py             ⚠️ Diagnóstico temporário
├── _verify_docs.py                ⚠️ Script auxiliar
├── _verify_final.py               ⚠️ Script auxiliar
│
├── diag_output.txt                📋 Output de diag.py
├── fase3_output.txt               📋 Output da Fase 3
├── test_output.txt                📋 Output de teste
│
├── AGENTS.md                      📚 Protegido — regras do sistema
├── CHANGELOG.md                   📚 Documentação do projeto
├── CONTRIBUTING.md                📚 Guia de contribuição
├── MEMORY.md                      📚 Memória do projeto
├── STATES.md                      📚 Estados do projeto
├── README.md                      📚 Documentação principal
└── requirements.txt               📦 Manifesto Python
```

---

## 6. Estrutura de `docs/` (Detalhamento)

```
docs/
├── arquitetura/              → 6 arquivos (CORE, DSL, arquitetura cognitiva)
├── agentes-prompts/          → 8 arquivos (design de agentes LLM, prompts)
├── ontologia-taxonomia/      → 9 arquivos (N3/N4, taxonomia, relatórios)
├── planejamento-roadmap/     → 4 arquivos + subdiretório roadmap/
│   └── roadmap/              → 4 arquivos de roadmap
├── runtime-pipeline/         → 1 arquivo (RUNTIME.md)
├── auditoria-qualidade/      → 1 arquivo (auditoria ontológica)
├── referencia-historico/     → 1 arquivo (AGENTS deprecated)
└── uso-documentacao/         → 2 arquivos (USAGE.md/.pdf)

Total: 9 subdiretórios, 34 arquivos
```

---

## 7. Estatísticas

| Métrica | Valor |
|---------|-------|
| Total de itens no root (arquivos + dirs) | ~57 |
| Diretórios | 15 |
| Arquivos | ~42 |
| Arquivos protegidos/sistema | 5 dirs + 8 arquivos |
| Arquivos de diagnóstico temporário | 19 scripts + 11 outputs |
| Documentação no root | 6 arquivos |
| Entrypoints de diagnóstico | 7 |
| Arquivos não categorizados | 5 (com sugestão) |

---

## 8. Próximos Passos Sugeridos

1. **Validar funcionamento:** `python run_kilo.py --health`
2. **Decidir sobre `_test_retrieval_e2e.py`:** Mover para `tests/` e renomear?
3. **Decidir sobre scripts auxiliares com prefixo `_`:** Manter no root ou mover para `scripts/`?
4. **Considerar:** Renomear `ontology/` → `data/ontology-source/` para maior clareza semântica
5. **Limpar outputs antigos:** `diag_output.txt`, `test_output.txt`, `fase3_output.txt` podem ser removidos se não forem mais necessários
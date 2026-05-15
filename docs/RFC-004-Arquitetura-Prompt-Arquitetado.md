# RFC-004 — Arquitetura do Prompt Arquitetado e Próxima Fase

> **Status:** PROPOSTO  
> **Autor:** Kilo Code Doc Spec  
> **Data:** 2026-05-15  
> **Versão do Sistema:** 3.0.2  
> **RFC Anterior:** N/A (primeiro RFC formal)  

---

## 1. Escopo Arquitetural

### 1.1 Objetivo

Formalizar o formato canônico de saída do pipeline cognitivo como **Prompt Arquitetado** — um prompt de engenharia estruturado em exatamente 4 seções, gerado automaticamente a partir da ontologia fractal N0→N4, pronto para uso direto em qualquer LLM.

### 1.2 Motivação

O sistema atualmente produz output via `OntologySynthesizer` usando `MASTER_TEMPLATE` (em `runtime/synthesizer.py:71-113`), mas:

- O template não é validado formalmente pelo `OntologyValidator`
- O CLI (`run_kilo.py`) ainda faz `print()` direto de dicts/JSON dumps em alguns caminhos
- Não há persistência estruturada dos resultados em `results/`
- Agentes auxiliares (`docs/agentes-prompts/`) não possuem um cânone unificado de prompts

### 1.3 Escopo de Mudanças

| Camada | Muda | Não Muda |
|--------|------|----------|
| `runtime/synthesizer.py` | Refatorar `SYNTHESIS_TEMPLATES` → `MASTER_TEMPLATE` canônico | Lógica de geração por pilar |
| `runtime/validator.py` | Adicionar `_verify_format()` para validar 4 seções | Regras de coerência existentes |
| `run_kilo.py` | CLI limpa com output formatado, `--verbose`, `--output-file` | Lógica de inicialização de componentes |
| `docs/agentes-prompts/` | Criar diretório com cânone de prompts | — |
| `results/` | Criar diretório para persistência automática | — |

---

## 2. Formato Canônico — 4 Seções

Todo output do pipeline DEVE seguir este formato:

```
### 1. CLASSIFICAÇÃO
- Vetor: {eixo}
- Pilar: {pilar}
- Domínio: {dominio}
- Subárvore: {subarvore}
- Célula: {celula}

### 2. LEITURA ESTRATÉGICA
{2-3 parágrafos contextuais sob a perspectiva do pilar}

### 3. RESPOSTA EXECUTÁVEL
{checklist + passos algorítmicos acionáveis}

### 4. OTIMIZAÇÃO
{variáveis estratégicas, edge cases, métricas de roteamento}
```

### 2.1 Regras de Formato

| Regra | Descrição |
|-------|-----------|
| R1 | Exatamente 4 seções, nesta ordem |
| R2 | Cada seção inicia com `### N. TÍTULO` |
| R3 | Sem prólogo, epílogo ou resumo fora das seções |
| R4 | Output é Markdown puro — sem JSON dumps |
| R5 | Checklist usa `- [ ]` para passos não executados |
| R6 | Dados de roteamento (score, confiança) incluídos na seção 4 |

---

## 3. Metas de Desempenho

| Métrica | Valor Atual (Estimado) | Meta RFC-004 | Tolerância |
|---------|----------------------|--------------|------------|
| Latência pipeline Full | ~8-12s | ≤ 10s | ±2s |
| Latência pipeline Simple | ~3-5s | ≤ 4s | ±1s |
| Taxa de classificação correta (N0) | ~85% | ≥ 90% | — |
| Taxa de recuperação relevante (top-5) | ~70% | ≥ 80% | — |
| Formato canônico válido | ~60% (estimado) | 100% | 0% de JSON dumps |
| Persistência automática | Manual | 100% das queries | — |

---

## 4. Plano de Implementação

### Fase 1 — Refatorar Synthesizer (CRÍTICA)

| # | Tarefa | Arquivo | Status |
|---|--------|---------|--------|
| 1.1 | Consolidar `SYNTHESIS_TEMPLATES` em `MASTER_TEMPLATE` único | `runtime/synthesizer.py` | ✅ Já existe (linhas 71-113) |
| 1.2 | Garantir persona "Arquiteto Sênior" no template | `runtime/synthesizer.py` | ✅ Já implementado |
| 1.3 | Remover qualquer path de output JSON não formatado | `runtime/synthesizer.py` | 🔄 Verificar |
| 1.4 | Adicionar type hints completos ao `SynthesisOutput` | `runtime/synthesizer.py` | 🔄 Pendente |

### Fase 2 — CLI Limpa (ALTA)

| # | Tarefa | Arquivo | Status |
|---|--------|---------|--------|
| 2.1 | Refatorar `run_kilo.py` com métodos `run_full()`, `run_simple()`, `run_autonomous()`, `run_interactive()` | `run_kilo.py` | 🔄 Pendente |
| 2.2 | Formatar output com emojis e Markdown (remover JSON dumps) | `run_kilo.py` | 🔄 Pendente |
| 2.3 | Ocultar metadados por padrão; `--verbose` para exibir | `run_kilo.py` | 🔄 Pendente |
| 2.4 | Adicionar flag `--output-file` para persistência | `run_kilo.py` | 🔄 Pendente |

### Fase 3 — Persistência (ALTA) ✅ JÁ IMPLEMENTADA

A persistência automática já está implementada no `run_kilo.py` (função `save_query_results`, linhas 213-249). O diretório `results/` contém 12 arquivos de saída de execuções anteriores.

| # | Tarefa | Arquivo | Status |
|---|--------|---------|--------|
| 3.1 | Diretório `results/` | raiz | ✅ Existente (6 pares de arquivos) |
| 3.2 | Salvamento automático: `[timestamp]_[slug]_full.json` + `[timestamp]_[slug]_output.yaml` | `run_kilo.py:213-249` | ✅ Implementado |
| 3.3 | Padrão de saída YAML com `allow_unicode=True` | `run_kilo.py:243` | ✅ Confirmado |

### Fase 4 — Validação de Formato (ALTA)

| # | Tarefa | Arquivo | Status |
|---|--------|---------|--------|
| 4.1 | Adicionar `_verify_format()` ao `OntologyValidator` | `runtime/validator.py` | 🔄 Pendente |
| 4.2 | Verificar presença das 4 seções, ordem e ausência de JSON | `runtime/validator.py` | 🔄 Pendente |
| 4.3 | Integrar validação de formato no pipeline | `runtime/orchestrator.py` | 🔄 Pendente |

### Fase 5 — Documentação dos Agentes (MÉDIA)

| # | Tarefa | Arquivo | Status |
|---|--------|---------|--------|
| 5.1 | Criar `docs/agentes-prompts/` | diretório | 🔄 Pendente |
| 5.2 | Criar `ARQUITETO_PROMPTS_FINAL.md` com cânone de prompts | `docs/agentes-prompts/` | 🔄 Pendente |

### Fase 6 — Correções de Discrepâncias (MÉDIA)

| # | Tarefa | Status |
|---|--------|--------|
| 6.1 | `README.md`: remover `.bat` inexistentes | ✅ Concluído |
| 6.2 | `README.md`: corrigir path `semantic_expansion_report.md` | ✅ Concluído |
| 6.3 | `README.md`: adicionar scripts omitidos | ✅ Concluído |
| 6.4 | `README.md`: documentar `diag2.py` | ✅ Concluído |
| 6.5 | Alinhar versão v3.0.2 em todos os arquivos | ✅ Concluído |

### Fase 7 — Engines Pendentes (FUTURO — Pós-RFC)

| # | Tarefa | Observação |
|---|--------|------------|
| 7.1 | `core/learning_engine.py` | Aprendizado adaptativo — não implementado |
| 7.2 | `core/latent_space_engine.py` | Espaço latente — pós-N5 |
| 7.3 | `core/memory_engine.py` | Memória gerenciada via YAML atualmente |
| 7.4 | `core/calibration_engine.py` | Absorvido pelo validator |
| 7.5 | `core/cognition_engine.py` | Delegado ao `cognitive_function_engine.py` |
| 7.6 | Scripts N5 (`generate_n5.py`, etc.) | 5 scripts pendentes |

---

## 5. Riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Refatoração do synthesizer pode quebrar pipelines existentes | Alto | Manter `SYNTHESIS_TEMPLATES` como fallback durante transição |
| Validação de formato pode rejeitar outputs legados | Médio | Modo `--strict` opcional no validator |
| Persistência em `results/` pode gerar volume excessivo | Baixo | Rotação automática; `--no-persist` flag |
| Engines pendentes (N5) bloqueiam expansão fractal | Médio | N5 é planejado para fase futura; N4 está completo |

---

## 6. Critérios de Aceitação

- [ ] Output do pipeline segue formato canônico de 4 seções (100%)
- [ ] Zero JSON dumps no output padrão
- [ ] CLI com `--verbose`, `--output-file`, `--mode` funcionando
- [ ] Persistência automática em `results/`
- [ ] Validator reconhece e rejeita formato inválido
- [ ] `docs/agentes-prompts/ARQUITETO_PROMPTS_FINAL.md` criado
- [ ] Todos os 6 itens de correção de discrepâncias aplicados
- [ ] Testes E2E passando com novo formato

---

## 7. Compatibilidade

Este RFC é **backward-compatible**: o pipeline continua funcionando com os templates existentes até a refatoração ser concluída. A flag `--format=legacy` pode ser adicionada temporariamente.

---

## 8. Decisão

**APROVAR** — Este RFC formaliza a arquitetura de prompt como prática padrão e define o plano de implementação em 7 fases. Fases 1-6 são prioridade imediata para v3.1.0. Fase 7 é planejamento de longo prazo.
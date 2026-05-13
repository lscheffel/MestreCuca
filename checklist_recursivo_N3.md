# CHECKLIST RECURSIVO N3 - Desenvolvimento Modular e Verificação

---

## 1. SUMÁRIO EXECUTIVO

Este documento estabelece o framework de desenvolvimento iterativo para componentes N3, garantindo:
- **Reutilização** de artefatos N3 existentes (54 arquivos)
- **Consistência** ontológica e sintática
- **Rastreabilidade** completa N0→N3
- **Verificação** recursiva de conformidade
- **Entregáveis** incrementais auditáveis

**Geometria Base:** 2×3×3×3×3 (162 combinações)  
**Nível Atual:** N3 (54 subdomínios mapeados)  
**Status:** ATIVO - Desenvolvimento Iterativo

---

## 2. CONTEXTO ONTOLÓGICO

### 2.1 Base de Referência

- **Ontologia Mestre:** `ONTOLOGIA_MESTRA_DOMINANTE_V2.md`
- **Taxonomia Expandido:** `Taxonomia_Ontologica.md`
- **Prompt Modular:** `PROMPT_MODULAR_N3.md`
- **Artefatos Existentes:** 54 arquivos `data/ontology/N3-{ID}-{DOMÍNIO}-{SUBDOMÍNIO}.md`

### 2.2 Níveis Consolidados

| Nível | Entidades | Status |
|-------|-----------|--------|
| N0 | 2 Vetores | Consolidado |
| N1 | 6 Pilares | Consolidado |
| N2 | 18 Domínios | Consolidado |
| **N3** | **54 Subdomínios** | **Em Desenvolvimento** |
| N4 | ≥162 Células | Planejado |

### 2.3 Herança de DNA

Todo componente N3 deve herdar obrigatoriamente:
- **N0:** Axiomas dos vetores (Sintrópico/Entrópico)
- **N1:** Crenças dos pilares (Logos/Bios/Pathos/Khaos/Apeiron/Mythos)
- **N2:** Tags e crenças dos domínios
- **N3:** Crença específica da especialização

---

## 3. DEPENDÊNCIAS

### 3.1 Dependências de Entrada

**Arquivos Obrigatórios:**
1. `ONTOLOGIA_MESTRA_DOMINANTE_V2.md` - Definições N0-N2
2. `Taxonomia_Ontologica.md` - Estrutura N3/N4
3. `PROMPT_MODULAR_N3.md` - Template de desenvolvimento
4. `data/ontology/N3-{ID}-{DOMÍNIO}-{SUBDOMÍNIO}.md` - Artefatos existentes

**Dados de Configuração:**
- ID do subdomínio N3 (ex: 1.1.1)
- Domínio pai (ex: LOGOS)
- Subdomínio N2 (ex: ALGORITMIA)
- Especialização N3 (ex: RESOLUÇÃO)

### 3.2 Dependências Cruzadas

**Relações Intra-N3:**
- Componentes do mesmo domínio N2 compartilham tags e crenças
- Especializações devem ser coesas dentro do domínio
- Evitar contradições entre subdomínios irmãos

**Relações Inter-Níveis:**
- N3 depende de definições N2 (obrigatório)
- N4 dependerá de N3 (futuro)
- Alterações em N2 impactam todos os N3 derivados

### 3.3 Matriz de Dependências

| Componente | Depende de | Impacta |
|------------|-----------|----------|
| N3-1.1.1 | V2[1.1], V2[1.0], V2[0.1] | N4-1.1.1-* |
| N3-1.1.2 | V2[1.1], V2[1.0], V2[0.1] | N4-1.1.2-* |
| N3-1.1.3 | V2[1.1], V2[1.0], V2[0.1] | N4-1.1.3-* |
| ... | ... | ... |
| N3-6.3.3 | V2[6.3], V2[6.0], V2[0.2] | N4-6.3.3-* |

---

## 4. CRITÉRIOS DE REUSO

### 4.1 Reutilização de Artefatos Existentes

**Permitido:**
- Copiar estrutura de arquivos N3 existentes
- Reutilizar descrições de herança
- Adaptar checklists preenchidos
- Referenciar matrizes de rastreabilidade

**Não Permitido:**
- Modificar artefatos de outros subdomínios
- Alterar definições N0-N2
- Criar dependências circulares
- Duplicar conteúdo sem propósito

### 4.2 Padrões de Consistência

**Sintaxe Markdown:**
- Cabeçalhos: `#`, `##`, `###`
- Tabelas: Formato pipe `|`
- Listas: `-` ou `*`
- Código: \`inline\` ou blocos \`\`\`

**Terminologia:**
- Usar "N3-{ID}" para referências
- "Domínio Pai" para N1
- "Subdomínio N2" para N2
- "Especialização" para N3

**Metadados:**
- Formato de data: AAAA-MM-DD
- Status: ATIVO / EM_DESENVOLVIMENTO / CONCLUIDO
- Versão: SemVer (Maior.Menor.Patch)

---

## 5. PASSOS DE DESENVOLVIMENTO

### 5.1 Fase 1: Preparação

**Tarefas:**
- [ ] Identificar subdomínio N3 alvo
- [ ] Consultar V2 para dados base
- [ ] Verificar artefatos existentes
- [ ] Definir escopo da especialização

**Entregáveis:**
- Dados de entrada documentados
- Escopo definido
- Riscos identificados

### 5.2 Fase 2: Desenvolvimento

**Tarefas:**
- [ ] Criar/atualizar arquivo N3
- [ ] Definir herança de DNA
- [ ] Especificar crença e foco
- [ ] Mapear relações ontológicas

**Entregáveis:**
- Arquivo N3 completo
- Matriz de rastreabilidade
- Regras de derivação

### 5.3 Fase 3: Verificação

**Tarefas:**
- [ ] Validar conformidade ontológica
- [ ] Verificar herança N0-N2
- [ ] Testar consistência sintática
- [ ] Revisar dependências

**Entregáveis:**
- Checklist preenchido
- Status de conformidade
- Pendências identificadas

### 5.4 Fase 4: Integração

**Tarefas:**
- [ ] Atualizar índices
- [ ] Documentar alterações
- [ ] Preparar para revisão
- [ ] Registrar no changelog

**Entregáveis:**
- Artefato finalizado
- Documentação completa
- Pronto para revisão

---

## 6. VERIFICAÇÃO DE CONSISTÊNCIA

### 6.1 Checklist de Conformidade Ontológica

#### Herança (N0-N3)
- [ ] Axiomas N0 referenciados explicitamente
- [ ] Crenças N1 documentadas
- [ ] Tags N2 incluídas
- [ ] Crença N3 especificada
- [ ] Relação com domínio pai clara

#### Consistência com V2
- [ ] Geometria 2×3×3×3×3 preservada
- [ ] Sem introdução de novos eixos
- [ ] Escopo não expandido além de N3
- [ ] Referências V2 válidas
- [ ] Terminologia alinhada

#### Qualidade Documental
- [ ] Sumário executivo claro
- [ ] Matriz de rastreabilidade preenchida
- [ ] Regras de derivação especificadas
- [ ] Checklist completo
- [ ] Registro de alterações

### 6.2 Testes de Consistência

**Teste 1: Herança Completa**
```
Verificar: N3 herda de N0, N1, N2
Método: Revisar seção "Herança de DNA"
Critério: Todos os níveis referenciados
```

**Teste 2: Referências Válidas**
```
Verificar: Links para V2 funcionais
Método: Testar cada âncora
Critério: Nenhum link quebrado
```

**Teste 3: Formato Consistente**
```
Verificar: Sintaxe Markdown correta
Método: Validar com parser
Critério: Sem erros de formatação
```

**Teste 4: Escopo Restrito**
```
Verificar: Sem expansão além de N3
Método: Revisar conteúdo
Critério: Foco exclusivo em N3
```

---

## 7. MARCOS DE ACEITAÇÃO

### 7.1 Marcos por Componente

**Marco 1: Estrutura Básica**
- [ ] Arquivo N3 criado
- [ ] Metadados preenchidos
- [ ] Sumário executivo definido
- **Status:** PENDENTE

**Marco 2: Herança Completa**
- [ ] DNA N0-N3 documentado
- [ ] Tags herdadas incluídas
- [ ] Crenças especificadas
- **Status:** PENDENTE

**Marco 3: Rastreabilidade**
- [ ] Matriz preenchida
- [ ] Dependências mapeadas
- [ ] Vínculos V2 estabelecidos
- **Status:** PENDENTE

**Marco 4: Conformidade**
- [ ] Checklist validado
- [ ] Testes aprovados
- [ ] Revisão concluída
- **Status:** PENDENTE

**Marco 5: Integração**
- [ ] Índices atualizados
- [ ] Changelog registrado
- [ ] Pronto para produção
- **Status:** PENDENTE

### 7.2 Aceitação Global

**Critérios de Aceitação do Projeto N3:**
- [ ] Todos os 54 subdomínios desenvolvidos
- [ ] 100% de conformidade ontológica
- [ ] Zero referências quebradas
- [ ] Herança completa N0-N3
- [ ] Documentação completa
- [ ] Checklists aprovados

---

## 8. RASTREABILIDADE

### 8.1 Matriz de Rastreabilidade N3

| ID N3 | Domínio | Subdomínio N2 | Especialização | Status | Vínculo V2 |
|-------|---------|---------------|----------------|--------|------------|
| 1.1.1 | LOGOS | ALGORITMIA | RESOLUÇÃO | ✅ | [Ver](#) |
| 1.1.2 | LOGOS | ALGORITMIA | OTIMIZAÇÃO | ✅ | [Ver](#) |
| 1.1.3 | LOGOS | ALGORITMIA | VALIDAÇÃO | ✅ | [Ver](#) |
| ... | ... | ... | ... | ... | ... |
| 6.3.3 | MYTHOS | MISTÉRIO | REVELAÇÃO | ✅ | [Ver](#) |

### 8.2 Dependências de Nível

**N3 → N2:**
- Cada N3 depende de exatamente 1 N2
- N2 pode ter múltiplos N3 (máximo 3)
- Herança obrigatória de tags e crenças

**N3 → N1:**
- Herança indireta via N2
- Crenças do pilar devem ser referenciadas
- Tags do pilar devem ser consideradas

**N3 → N0:**
- Herança indireta via N1
- Axiomas devem guiar especialização
- Metas devem ser consideradas

### 8.3 Impacto de Alterações

**Alterações em N2:**
- Impacto: Alto (afeta todos os N3 derivados)
- Mitigação: Revisão de todos os N3 dependentes
- Teste: Validação de conformidade

**Alterações em N3:**
- Impacto: Médio (afeta N4 futuros)
- Mitigação: Revisão de dependências
- Teste: Consistência com N2

**Alterações em N0/N1:**
- Impacto: Crítico (afeta toda ontologia)
- Mitigação: Revisão completa
- Teste: Validação global

---

## 9. PRÓXIMOS CICLOS

### 9.1 Ciclo Atual: N3

**Objetivo:** Completar desenvolvimento de todos os 54 subdomínios N3
**Status:** Em andamento
**Entregáveis:** 54 arquivos N3 individuais
**Prazo:** Iterativo

### 9.2 Ciclo Futuro: N4

**Objetivo:** Desenvolver células semânticas operacionais
**Status:** Planejado
**Entregáveis:** ≥162 células N4
**Dependência:** Conclusão de N3

### 9.3 Ciclo Futuro: Integração

**Objetivo:** Integração completa N0-N4
**Status:** Planejado
**Entregáveis:** Ontologia fractal completa
**Dependência:** Conclusão de N3 e N4

---

## 10. SUMÁRIO DE MUDANÇAS E IMPACTOS

### 10.1 Mudanças Implementadas

**Arquivos Criados:**
- 54 arquivos N3 individuais
- `checklist_recursivo_N3.md`
- `PROMPT_MODULAR_N3.md`

**Arquivos Atualizados:**
- `Taxonomia_Ontologica.md` (expansão N3/N4)
- `ONTOLOGIA_MESTRA_DOMINANTE_V2.md` (conformidade)

**Scripts Desenvolvidos:**
- `create_n3_files_v2.py` (automação)

### 10.2 Impactos no Projeto

**Positivos:**
- Rastreabilidade granular N0-N3
- Consistência ontológica garantida
- Processo iterativo estabelecido
- Entregáveis auditáveis

**Riscos Mitigados:**
- Deriva ontológica (controle via checklist)
- Inconsistência sintática (validação automática)
- Dependências circulares (matriz de rastreabilidade)
- Escopo não controlado (limites definidos)

### 10.3 Métricas de Sucesso

**Quantitativas:**
- 54/54 subdomínios N3 desenvolvidos
- 100% de conformidade ontológica
- 0 referências quebradas
- 54/54 checklists aprovados

**Qualitativas:**
- Documentação clara e completa
- Processo iterativo eficiente
- Integração sem problemas
- Manutenibilidade garantida

---

## 11. CONCLUSÃO

Este checklist recursivo estabelece o framework para desenvolvimento modular de componentes N3, garantindo:

✅ **Reutilização** de artefatos existentes  
✅ **Consistência** ontológica e sintática  
✅ **Rastreabilidade** completa N0-N3  
✅ **Verificação** recursiva de conformidade  
✅ **Entregáveis** incrementais auditáveis  

O processo iterativo permite desenvolvimento independente de módulos N3 com qualidade, clareza e aderência estrita aos padrões da ontologia fractal.

**Próximos Passos:**
1. Completar desenvolvimento de todos os 54 N3
2. Iniciar planejamento de N4
3. Estabelecer CI/CD para validação contínua
4. Documentar lições aprendidas

---

*Este documento é parte integrante da governança ontológica do projeto "Arquiteto de Prompts - Expansão Fractal" e deve ser mantido em sincronia com os artefatos N3 e a ontologia mestre.*
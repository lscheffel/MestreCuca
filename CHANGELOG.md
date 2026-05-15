# CHANGELOG

> Registro de alterações significativas no projeto MestreCuca.
> Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).
> Este projeto adere ao [Semantic Versioning](https://semver.org/).

---

## [3.0.2] — 2026-05-15 (Auditoria Documental)

### Adicionado
- **`docs/RFC-004-Arquitetura-Prompt-Arquitetado.md`** — RFC para refatoração do synthesizer e CLI limpa
- **`docs/HANDOFF-PROMPT-ORCHESTRATOR.md`** — Prompt de handoff para implementação do RFC-004

### Alterado
- **README.md** — Corrigidas referências a `.bat` inexistentes (`run_diag.bat`, `run_test.bat`)
- **README.md** — Corrigido path de `semantic_expansion_report.md`
- **README.md** — Adicionados scripts omitidos: `create_n4_manual.py`, `padronizador.py`, `reestruturar_n4.py`
- **README.md** — Adicionado `diag2.py` à lista de diagnósticos
- **`.kilo/STATE.md`** — Versão atualizada para 3.0.2

### Contexto
- Auditoria documental completa: 8 discrepâncias identificadas e corrigidas
- Sem débitos técnicos (0 TODOs/FIXMEs) no código-fonte
- RFC-004 proposto para próxima fase de produto
- Versão alinhada: CHANGELOG, STATE.md e README.md agora consistentes em v3.0.2

---

## [3.0.1] — 2026-05-13 (Sync Completo)

### Adicionado
- **`.kilo/STATE.md`** — Fonte de contexto persistente para agentes de IA (estado, componentes, configurações, bugs conhecidos)
- **`CHANGELOG.md`** — Registro formal de alterações (Keep a Changelog)
- **`CONTRIBUTING.md`** — Diretrizes de contribuição com as 10 Leis de Engenharia

### Alterado
- **README.md v3.0.1** — Seção "Memória Técnica" atualizada para refletir `.kilo/STATE.md` existente
- **README.md v3.0.1** — Seção "Contribuição" atualizada com link para `CONTRIBUTING.md`
- **README.md v3.0.1** — Seção "Documentação & Roadmap" com links verificados

### Contexto
- Fase 0 do Roadmap (Consolidação da Interface Estática) concluída
- Auditoria recursiva de 100% do repositório realizada
- Todos os arquivos ausentes detectados foram criados
- Sincronia README ↔ Código ↔ Configurações completa

---

## [3.0.0] — 2026-05-13

### Adicionado
- **README.md v3** — Documentação completa com diagrama Mermaid, stack tecnológico, entrypoints verificados e estrutura de diretórios real
- **Diagrama de Arquitetura Macro** — Pipeline visual (Classifier → Router → Retriever → Graph → Dialectic → Synthesizer → Validator)

### Alterado
- **Reescrita completa do README.md** — Antigo README (55 linhas) substituído por documentação de 420 linhas com 10 seções
- **Correção de referências** — Todos os links internos agora apontam para arquivos que existem no filesystem
- **Atualização do Stack** — Confirmado Python 3.13, NetworkX ≥3.0, sentence-transformers ≥2.2

### Corrigido
- **Flags de ausência documentadas** — Makefile, CHANGELOG.md, CONTRIBUTING.md, .kilo/STATE.md agora explicitamente reportados
- **Entrypoints validados** — Todos os comandos listados no README confirmados contra o código real

### Contexto
- Fase 0 do Roadmap (Consolidação da Interface Estática) concluída
- Auditoria recursiva de 100% do repositório realizada
- 25+ arquivos verificados e documentados
- Avaliação do projeto: 7.5/10 → documentação agora sincronizada com o código

---

## [2.0.0] — 2026-05-09

### Adicionado
- Consolidação da Arquitetura Cognitiva V3
- CORE V1.1 — Especificação atualizada
- Correção da ontologia base (V2) após auditoria de discrepâncias
- Expansão fractal completa: 162 células N4 (2×3×3×3×3)

### Alterado
- Migração da definição ontológica para `config/ontology.yaml` (1.708 linhas)
- Atualização dos agentes para configuração via `.kilo/agents/agents.yaml`

---

## [1.0.0] — 2026-04 (Estimativa)

### Adicionado
- Estrutura inicial do sistema cognitivo ontológico
- 6 pilares: LOGOS, BIOS, PATHOS, KHAOS, APEIRON, MYTHOS
- 18 domínios, 54 subárvores, 162 células N4
- Pipeline de inferência: Classifier → Router → Retriever → Synthesizer → Validator
- Retrieval híbrido: vetorial + gráfico + simbólico
- Modelo de embedding: all-MiniLM-L6-v2 (384d)
- Índice vetorial: FAISS IVFFlat (cosine)
- Motor de grafo: NetworkX MultiDiGraph
- 6 agentes LLM configurados (GPT-4o / GPT-4o-mini)
- Autonomy Layer com auto-avaliação e feedback loop
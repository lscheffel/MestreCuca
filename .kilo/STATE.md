# STATE.md — Memória Técnica do Sistema

> **Propósito:** Fonte de contexto persistente para agentes de IA que operam sobre o projeto MestreCuca.
> **Atualizado por:** Kilo Code Doc Spec (README Sync)
> **Última atualização:** 2026-05-13

---

## Estado Atual do Sistema

| Campo | Valor |
|---|---|
| **Versão** | 3.0.2 |
| **Fase do Roadmap** | Fase 1 — Arquitetura do Prompt Arquitetado (RFC-004) |
| **Status** | READY FOR DEVELOPMENT |
| **Avaliação** | 7.5 / 10 (pós-roadmap: 10/10) |
| **Build** | Estável (162 células N4 operacionais) |

---

## Componentes Ativos

### Core (framework agnóstico)
- `core/ontology_graph.py` — OntologyGraph (NetworkX MultiDiGraph, 242+ nós, 2557+ arestas)
- `core/signature_engine.py` — Assinaturas semânticas 9D
- `core/dialectic_engine.py` — Inferência de opostos (5 níveis de profundidade)
- `core/cognitive_function_engine.py` — Funções cognitivas auxiliares
- `core/ontology_typing.py` — 10 naturezas ontológicas
- `core/relation_engine.py` — 10 tipos de relação ponderados
- `core/agent_base.py` — BaseAgent, AgentResult, AgentMemory

### Runtime (pipeline de execução)
- `runtime/classifier.py` — OntologicalClassifier (N0→N4)
- `runtime/router.py` — CognitiveRouter (seleção adaptativa de pipeline)
- `runtime/retriever.py` — HybridRetriever (vetorial + gráfico + simbólico)
- `runtime/synthesizer.py` — OntologySynthesizer (composição multi-fonte)
- `runtime/validator.py` — OntologyValidator (coerência ontológica)
- `runtime/orchestrator.py` — MultiAgentOrchestrator (3 pipelines configuráveis)

### Agents (.kilo/agents/)
- **OntoClassifier** — GPT-4o, T=0.2, classificação N0→N4
- **OntoRetriever** — GPT-4o, T=0.0, retrieval híbrido (top_k=20)
- **OntoSynthesizer** — GPT-4o, T=0.4, síntese multi-fonte
- **OntoValidator** — GPT-4o, T=0.0, validação de consistência
- **OntoRouter** — GPT-4o-mini, T=0.3, roteamento inteligente
- **AutonomyLayer** — Auto-avaliação, feedback loop, thresholds adaptativos

### Modelos de Embedding
- Modelo: `all-MiniLM-L6-v2` (sentence-transformers)
- Dimensão: 384
- Índice: FAISS IVFFlat (cosine, nlist=100, nprobe=10)
- Cache: LRU, 2048 MB, TTL 24h

---

## Arquitetura de Memória

| Nível | Tipo | Capacidade | TTL | Estratégia |
|---|---|---|---|---|
| Curto prazo | volatile | 500 itens | 30 min | LRU |
| Trabalho | managed | 200 itens | 1 hora | priority |
| Longo prazo | persistent (SQLite) | 100k itens | ∞ | relevance |
| Embedding cache | LRU | 50k itens | 24h | similaridade |
| Retrieval cache | TTL (Redis) | 50k itens | 1h | — |

---

## Ontologia Fractal — Estrutura Verificada

```
N0 (Vetor):          2 nós    — SINTRÓPICO | ENTRÓPICO
N1 (Pilar):          6 nós    — LOGOS | BIOS | PATHOS | KHAOS | APEIRON | MYTHOS
N2 (Domínio):       18 nós    — 3 por pilar
N3 (Subárvore):     54 nós    — 3 por domínio
N4 (Célula):       162 nós    — 3 por subárvore
                    ───────
                    2×3×3×3×3 = 162
```

### Arquivos N4 JSON Verificados
- Diretório: `data/json/`
- Contagem: 162 arquivos `N4_*.json`
- Índice: `data/json/ontology_index.json`
- Formato: JSON com uid, path, nome, natureza, relações, assinatura semântica 9D

---

## Configuração de Retrieval Híbrido

| Método | Peso | Limiar | Descrição |
|---|---|---|---|
| Vetorial (cosine) | 0.50 | 0.15 min / 0.85 alta_confiança | Similaridade semântica |
| Gráfico (ponderado) | 0.30 | 0.5 min | Navegação ontológica (profundidade 3) |
| Simbólico (exato) | 0.20 | 0.8 parcial | Match por uid/tipo/pilar |
| **Fusão** | weighted_sum | 0.40 limiar final | Deduplicação ativa |
| **Reranking** | cross-encoder | 0.50 limiar | Top 50 → Top 10 |

---

## Decisões de Design Recentes

### 2026-05-13 — Auditoria de README (Fase 1–3 concluída)
- README.md reescrito com base em varredura recursiva de 100% do repositório
- Entrypoints documentados como scripts Python (Makefile não existe)
- Flags de ausência documentadas: Makefile, CHANGELOG.md, CONTRIBUTING.md, .kilo/STATE.md
- Árvore de diretórios verificada contra filesystem real
- Stack tecnológico confirmado: Python 3.13, NetworkX ≥3.0, sentence-transformers ≥2.2

### 2026-05-09 — Consolidação da Ontologia V2
- Auditoria ontológica concluída (auditoria_discrepancias_ontologicas.md)
- Correções de herança de tags e metas vetoriais aplicadas
- Configuração ontológica migrada para `config/ontology.yaml` (1.708 linhas)

---

## Bugs Conhecidos e Workarounds

| Bug | Status | Workaround |
|---|---|---|
| `driver.py` — issues de path no Windows | Conhecido | Usar `run_kilo.py` (resolve paths automaticamente) |
| `CHANGELOG.md` inexistente | ✅ Resolvido (v3.0.1) | — |
| `CONTRIBUTING.md` inexistente | ✅ Resolvido (v3.0.1) | — |

---

## Contexto para IAs

Este arquivo serve como **fonte canônica de contexto** para qualquer agente de IA que precise entender o estado do projeto MestreCuca. Ao iniciar operação, agentes devem:

1. Ler este arquivo para entender o estado atual
2. Consultar `config/*.yaml` para parâmetros operacionais
3. Consultar `README.md` para documentação de usuário
4. Consultar `docs/` para documentação técnica detalhada

**Não hardcodar valores deste arquivo** — sempre recarregar a cada sessão.
# MEMORY.md — Memória Operacional para Arquitetura Cognitiva Ontológica V3

## Versão 1.0 — Sistema de Gerenciamento de Memória Cognitiva

---

# 🎯 PROPÓSITO

O módulo MEMORY define a arquitetura de memória operacional do sistema, estabelecendo:

- **Hierarquia de memórias** (operacional, contextual, persistente)
- **Mecanismos de TTL cognitivo** (Time To Live semântico)
- **Políticas de invalidação** e garbage collection
- **Persistência e recuperação** de estados
- **Histórico inferencial** e rastreamento de decisões
- **Integração** com RUNTIME.md e STATES.md

O sistema de memória opera como subsistema crítico, garantindo:

1. **Estabilidade semântica** — evita contaminação inferencial
2. **Degradação controlada** — limpa resíduos obsoletos
3. **Auditoria completa** — rastreia origem e evolução de inferências
4. **Recuperação robusta** — permite rollback com preservação de aprendizados
5. **Escalabilidade cognitiva** — gerencia recursos de forma adaptativa

---

# 📋 DEPENDÊNCIAS

- **CORE.md** — princípios fundamentais e governança
- **RUNTIME.md** — orquestração de execução e ciclo de vida
- **STATES.md** — máquina de estados e transições
- **DSL.md** — diretivas de configuração (opcional)

---

# 🧠 ARQUITETURA DE MEMÓRIA OPERACIONAL

## 1. Hierarquia de Camadas

```text
┌─────────────────────────────────────────┐
│  MEMÓRIA PERSISTENTE (Long-term)       │
│  — Snapshots de estado                  │
│  — Histórico inferencial completo       │
│  — Metadados de aprendizagem            │
│  TTL: ∞ (até substituição explícita)    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  MEMÓRIA CONTEXTUAL (Mid-term)          │
│  — Contexto ativo da sessão            │
│  — Classificações N0-N4 recentes       │
│  — Vínculos ontológicos temporários    │
│  TTL: 300s após última referência      │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  MEMÓRIA OPERACIONAL (Short-term)       │
│  — Registradores ativos                │
│  — Cache de inferências                │
│  — Estado atual do pipeline            │
│  TTL: Ciclo atual ou 60s (o menor)     │
└─────────────────────────────────────────┘
```

---

## 2. Componentes da Memória Operacional

### 2.1 Registradores do Sistema

| Registrador | Tipo | Descrição | TTL |
|-------------|------|-----------|-----|
| **REG_INPUT** | Raw | Input bruto normalizado | Ciclo atual |
| **REG_FEI_PSI** | Float | Potencial de Resolução Ψ | Ciclo atual |
| **REG_ONTOLOGY** | Struct | Classificação N0-N4 | Ciclo atual |
| **REG_DEPENDENCIES** | Array | Dependências resolvidas | Ciclo atual |
| **REG_COMPILATION** | String | Instruções executáveis | Ciclo atual |
| **REG_VALIDATION** | Bool | Status de validação | Ciclo atual |
| **REG_CONTEXT_HASH** | Hash | Hash do contexto atual | 60s |
| **REG_SESSION_ID** | UUID | ID da sessão ativa | Ciclo atual |

### 2.2 Cache de Inferências

**Estrutura:**
```yaml
cache_key: "{input_hash}:{classification}"
entries:
  - key: "a1b2c3:LOGOS-RESOLUÇÃO"
    result: "Instruções compiladas..."
    confidence: 0.92
    created_at: "2025-05-08T01:00:00Z"
    last_accessed: "2025-05-08T01:05:00Z"
    hit_count: 3
    ttl_remaining: 240s
```

**Políticas:**
- **Hit rate mínimo:** 50% para manter cache ativo
- **Tamanho máximo:** 1000 entradas ou 50MB
- **Estratégia de evicção:** LRU (Least Recently Used) com peso por confiança
- **Invalidação:** por TTL ou por dependência alterada

### 2.3 Memória Contextual

Armazena o contexto ativo da sessão, incluindo:

- **Classificação ontológica** atual (N0-N4)
- **Variável dominante** identificada
- **Restrições ativas** e limites operacionais
- **Histórico recente** (últimos 5 ciclos)
- **Metadados de qualidade** (Ψ, confiança, entropia)

**Persistência:** 300s após última referência, estendível por reutilização.

---

# ⏱ SISTEMA DE TTL COGNITIVO

## 1. Princípios do TTL Semântico

O TTL (Time To Live) cognitivo difere de TTL técnico tradicional:

| Aspecto | TTL Técnico | TTL Cognitivo |
|---------|-------------|---------------|
| **Base** | Tempo absoluto | Relevância semântica |
| **Trigger** | Clock system | Última referência + atividade |
| **Renovação** | Manual ou periódica | Automática por uso |
| **Invalidante** | Expirado | Contaminação ou obsolescência |

## 2. Níveis de TTL

### 2.1 TTL de Ciclo (Ciclo Atual)

**Aplicação:** Registradores operacionais, estado do pipeline.

**Duração:** Até conclusão do ciclo atual (OUTPUT_RENDER → IDLE).

**Invalidantes:**
- Transição para IDLE
- Início de novo INPUT_CAPTURE
- ROLLBACK para estado anterior

**Exemplos:**
- `REG_INPUT`, `REG_FEI_PSI`, `REG_ONTOLOGY`
- Estado de validação em andamento
- Buffer de tokens normalizados

### 2.2 TTL de Sessão (60 segundos)

**Aplicação:** Contexto ativo, hash de sessão, classificações recentes.

**Duração:** 60 segundos após última referência.

**Renovação:** Qualquer acesso (read ou write) reinicia contador.

**Invalidantes:**
- Inatividade por 60s
- Transição para MAINTENANCE
- ROLLBACK com limpeza de contexto

**Exemplos:**
- `REG_CONTEXT_HASH`
- Cache de classificação N0-N4
- Metadados de qualidade (Ψ, H_sem)

### 2.3 TTL de Snapshot (300 segundos)

**Aplicação:** Snapshots de estado, memória contextual persistente.

**Duração:** 300 segundos (5 minutos) após última referência.

**Renovação:** Acesso por RUNTIME ou STATES.

**Invalidantes:**
- Inatividade por 300s
- Substituição por snapshot mais recente
- ROLLBACK_WITH_PRESERVATION (preserva apenas se Ω ≥ 0.80)

**Exemplos:**
- Snapshots de estado (últimos 3 válidos)
- Histórico de classificações
- Logs de auditoria resumidos

### 2.4 TTL Infinito (Persistente)

**Aplicação:** Dados estruturais, metadados de aprendizagem.

**Duração:** Até substituição explícita ou remoção manual.

**Invalidantes:**
- Comando explícito de limpeza
- Migração de versão do sistema
- Corrupção detectada

**Exemplos:**
- Histórico inferencial completo
- Metadados de treinamento/aprendizado
- Configurações de políticas de memória

---

## 3. Algoritmo de TTL Cognitivo

```python
class CognitiveTTL:
    def __init__(self, base_ttl, decay_factor=0.8):
        self.base_ttl = base_ttl  # segundos
        self.decay_factor = decay_factor  # 0.0-1.0
        self.access_history = []  # [(timestamp, relevance_score)]
    
    def calculate_remaining_ttl(self, current_time, last_access, access_count, relevance):
        """
        Calcula TTL restante com decaimento baseado em relevância.
        
        Fórmula:
        TTL_eff = TTL_base × (decay_factor ^ (time_since_last_access / TTL_base))
        TTL_final = TTL_eff × (1 + log(access_count + 1) × 0.1)
        """
        time_since = current_time - last_access
        
        # Decaimento exponencial
        decay = self.decay_factor ** (time_since / self.base_ttl)
        effective_ttl = self.base_ttl * decay
        
        # Bônus por reutilização
        reuse_bonus = 1 + (math.log(access_count + 1) * 0.1)
        final_ttl = effective_ttl * reuse_bonus
        
        return max(0, final_ttl)
```

**Parâmetros padrão:**
- `base_ttl`: conforme camada (ciclo/60/300/∞)
- `decay_factor`: 0.8 (20% de decaimento por período)
- `reuse_bonus`: +10% por cada 10 acessos (logarítmico)

---

# 🗑 POLÍTICAS DE INVALIDAÇÃO E GARBAGE COLLECTION

## 1. Gatilhos de Invalidação

### 1.1 Invalidação por Tempo (TTL Expirado)

**Condição:** `remaining_ttl <= 0`

**Ação:** Remover entrada da memória operacional.

**Log:** Registrar em `audit_log` com motivo `"TTL_EXPIRED"`.

**Exemplo:**
```
[2025-05-08T01:10:00Z] INVALIDATION: key=REG_CONTEXT_HASH reason=TTL_EXPIRED ttl_remaining=0
```

### 1.2 Invalidação por Contaminação

**Condição:** Detecção de contaminação semântica (RUNTIME.md, III. Governança de Contexto).

**Sinais de contaminação:**
- `H_sem` (Entropia Semântica) > 0.4
- Conflito entre classificações sucessivas
- Contexto com múltiplos vetores conflitantes
- Inferência degradada (confiança < 0.3)

**Ação:**
1. Isolar entrada contaminada
2. Registrar em `contamination_log`
3. Disparar ROLLBACK se crítico
4. Limpar contexto relacionado

**Exemplo:**
```
[2025-05-08T01:12:00Z] CONTAMINATION_DETECTED: key=REG_ONTOLOGY entropy=0.47 action=ISOLATE
```

### 1.3 Invalidação por Obsolescência

**Condição:** Estrutura ou classificação substituída por versão mais recente.

**Caso 1:** Nova classificação N0-N4 invalida anterior.
- **Ação:** Invalidar cache de inferências baseadas na classificação antiga.
- **Preservação:** Manter logs para auditoria.

**Caso 2:** Mudança de pilar ou vetor.
- **Ação:** Limpar todas as memórias contextuais relacionadas ao pilar anterior.
- **Justificativa:** Mudança ontológica profunda invalida inferências anteriores.

### 1.4 Invalidação por Recurso (Resource-based)

**Condição:** `RESOURCE_THRESHOLD_EXCEEDED` (STATES.md, linha 124).

**Limites:**
- Memória RAM > 90% por >5s
- Cache size > 80% do limite configurado
- CPU > 85% por >5s (indireto, aciona limpeza agressiva)

**Ação:** Iniciar `MAINTENANCE` state com foco em limpeza.

**Política de limpeza:**
1. Expirar TTLs com `remaining_ttl < 30s`
2. Evict cache entries com `hit_rate < 20%`
3. Compactar logs antigos (>24h)
4. Se ainda insuficiente: limpar memória contextual não crítica

---

## 2. Garbage Collection Estratégico

### 2.1 Coleta Passiva (Contínua)

**Frequência:** A cada 30 segundos em background.

**Ações:**
- Verificar TTLs expirados
- Compactar entradas de cache com baixa frequência
- Atualizar estatísticas de hit rate

**Impacto:** Baixo (<1% CPU, memória mínima).

### 2.2 Coleta Ativa (Por Evento)

**Gatilhos:**
- Transição para `MAINTENANCE` state
- `RESOURCE_THRESHOLD_EXCEEDED`
- Comando explícito `GC_FORCE`

**Ações:**
1. **Fase 1 — Marcação:**
   - Varrer todas as entradas
   - Marcar para preservação:
     - Entradas com `hit_rate > 50%`
     - Snapshots com `Ω ≥ 0.80`
     - Logs de auditoria críticos (<1h)
   
2. **Fase 2 — Remoção:**
   - Remover entradas não marcadas
   - Compactar memória
   - Atualizar métricas

3. **Fase 3 — Reconstrução:**
   - Reconstruir índices
   - Validar integridade referencial
   - Gerar relatório de coleta

**Impacto:** Moderado (5-10% CPU por 2-5s).

### 2.3 Coleta Profunda (Preventiva)

**Frequência:** A cada 6 horas (configurável).

**Ações:**
- Limpar todos os TTLs de sessão (60s)
- Compactar histórico inferencial (arquivamento)
- Validar checksums de snapshots persistentes
- Otimizar estruturas de índice

**Agendamento:** Durante períodos de baixa carga (detectado automaticamente).

---

## 3. Políticas de Preservação

### 3.1 Critérios de Preservação

Uma entrada NÃO deve ser coletada se:

| Critério | Condição | Prioridade |
|----------|----------|------------|
| **Alta confiança** | `confidence ≥ 0.90` | 1 (máxima) |
| **Alta utilidade** | `hit_rate ≥ 70%` | 2 |
| **Recente** | `age < 300s` e `access_count > 5` | 3 |
| **Crítico para rollback** | `checkpoint_level ≥ 2` | 1 |
| **Auditoria obrigatória** | `audit_required = true` | 1 |

### 3.2 Níveis de Checkpoint

| Nível | Descrição | Retenção | Uso típico |
|-------|-----------|----------|-------------|
| **0** | Estado volátil | Até próximo ciclo | Registradores operacionais |
| **1** | Contexto ativo | 5 minutos | Classificação atual |
| **2** | Snapshot intermediário | 1 hora | Antes de transição crítica |
| **3** | Snapshot estável | 24 horas | Após OUTPUT_RENDER bem-sucedido |
| **4** | Snapshot persistente | ∞ (manual) | Aprendizados estruturais |

**Checkpoint automático:**
- Nível 2: antes de `ONTOLOGY_BINDING` (estado estável)
- Nível 3: após `OUTPUT_RENDER` com `Ψ ≥ 0.85`
- Nível 4: manual via comando DSL `MEMORY_PRESERVE`

---

# 💾 PERSISTÊNCIA E RECUPERAÇÃO

## 1. Estratégias de Persistência

### 1.1 Snapshots de Estado

**Formato:** JSON estruturado com checksum SHA-256.

**Estrutura:**
```json
{
  "snapshot_id": "uuid-v4",
  "timestamp": "2025-05-08T01:15:00Z",
  "state": "ONTOLOGY_BINDING",
  "checkpoint_level": 2,
  "memory_segments": {
    "operational": {
      "REG_INPUT": "...",
      "REG_FEI_PSI": 0.87,
      "REG_ONTOLOGY": {"vector": "LOGOS", "pillar": "ALGORITMIA", ...}
    },
    "contextual": {
      "classification_history": [...],
      "dominant_variable": "complexidade_algortimica"
    }
  },
  "metadata": {
    "psi": 0.87,
    "entropy": 0.12,
    "confidence": 0.91,
    "resource_usage": {"memory_mb": 45, "cpu_pct": 12}
  },
  "checksum": "sha256:..."
}
```

**Frequência de snapshot:**
- Automático: a cada transição para `ONTOLOGY_BINDING` (checkpoint nível 2)
- Automático: após `OUTPUT_RENDER` bem-sucedido (checkpoint nível 3)
- Manual: via comando `MEMORY_SNAPSHOT`
- Manutenção: a cada 15 minutos em `MAINTENANCE`

**Retenção:**
- Últimos 3 snapshots nível 3
- Últimos 5 snapshots nível 2
- Snapshots nível 4: até remoção manual

### 1.2 Logs de Auditoria

**Finalidade:** Rastreabilidade completa de todas as operações de memória.

**Formato:** Linhas estruturadas (JSONL).

**Campos:**
```json
{
  "timestamp": "2025-05-08T01:15:30Z",
  "event_type": "MEMORY_WRITE",
  "component": "CACHE",
  "key": "a1b2c3:LOGOS-RESOLUÇÃO",
  "action": "INSERT",
  "metadata": {"ttl": 300, "confidence": 0.92},
  "session_id": "sess-xyz123"
}
```

**Eventos auditados:**
- `MEMORY_WRITE` — escrita em qualquer segmento
- `MEMORY_READ` — leitura (amostragem 10%)
- `MEMORY_EVICT` — evicção por GC
- `MEMORY_INVALIDATE` — invalidação explícita
- `SNAPSHOT_CREATE` — criação de snapshot
- `SNAPSHOT_RESTORE` — restauração de snapshot
- `ROLLBACK_INIT` — início de rollback
- `ROLLBACK_COMPLETE` — conclusão de rollback

**Retenção:**
- Logs recentes (24h): memória rápida
- Logs arquivados (>24h): arquivamento diário em disco
- Logs críticos (ROLLBACK, SNAPSHOT_RESTORE): retenção de 30 dias

### 1.3 Histórico Inferencial

**Finalidade:** Rastrear cadeia de inferências desde input até output.

**Estrutura:**
```json
{
  "inference_id": "inf-abc456",
  "session_id": "sess-xyz123",
  "input_hash": "sha256:...",
  "classification": {"vector": "LOGOS", "pillar": "ALGORITMIA", "n2": "1.1", "n3": "RESOLUÇÃO", "n4": "DECOMPOSIÇÃO_BINÁRIA"},
  "pipeline_trace": [
    {"stage": "INPUT_CAPTURE", "timestamp": "...", "duration_ms": 5},
    {"stage": "NORMALIZATION", "timestamp": "...", "duration_ms": 12},
    {"stage": "FEI_GATE", "psi": 0.87, "timestamp": "...", "duration_ms": 8},
    {"stage": "ONTOLOGY_BINDING", "timestamp": "...", "duration_ms": 15},
    {"stage": "DEPENDENCY_RESOLUTION", "timestamp": "...", "duration_ms": 6},
    {"stage": "COGNITIVE_COMPILATION", "timestamp": "...", "duration_ms": 22},
    {"stage": "VALIDATION_LAYER", "passed": true, "timestamp": "...", "duration_ms": 10},
    {"stage": "OUTPUT_RENDER", "timestamp": "...", "duration_ms": 3}
  ],
  "memory_snapshots": ["snap-001", "snap-002"],
  "final_output_hash": "sha256:...",
  "quality_metrics": {"psi": 0.87, "entropy": 0.12, "confidence": 0.91}
}
```

**Retenção:** 30 dias (configurável).

**Indexação:** Por `session_id`, `classification`, `timestamp` para consulta.

---

## 2. Mecanismos de Recuperação

### 2.1 Restauração de Snapshot

**Trigger:** Comando `MEMORY_RESTORE <snapshot_id>` ou rollback automático.

**Processo:**
1. Validar checksum do snapshot
2. Verificar integridade estrutural
3. Carregar segmentos de memória:
   - **Operacional:** substitui registradores atuais
   - **Contextual:** restaura contexto (se checkpoint nível ≥ 2)
4. Disparar evento `SNAPSHOT_RESTORED`
5. Atualizar `session_id` (novo ramo inferencial)

**Validação pós-restauração:**
- Recalcular `Ψ` (Potencial de Resolução)
- Verificar consistência ontológica
- Testar integridade de dependências

**Falha:** Se checksum inválido ou estrutura corrompida, acionar `FAILSAFE`.

### 2.2 Recuperação de Rollback com Preservação

**Cenário:** `ROLLBACK_WITH_PRESERVATION` (STATES.md, linha 189).

**Objetivo:** Reverter para estado anterior, mas preservar aprendizados estruturais.

**Aprendizados preserváveis:**
- Classificações bem-sucedidas (confiança ≥ 0.85)
- Restrições validadas
- Padrões de dependência estáveis
- Métricas de qualidade (Ψ, H_sem) médias

**Processo:**
```
1. Identificar último checkpoint estável (nível ≥ 2)
2. Extrair "aprendizados" do estado atual:
   - Se Ω (estabilidade ontológica) ≥ 0.80:
     • Manter classificações validadas
     • Registrar novas restrições
   - Caso contrário: limpar tudo
3. Restaurar snapshot do checkpoint
4. Aplicar aprendizados como "pré-condições" para próximo ciclo
5. Registrar em HISTORICAL_LEARNING
```

**Exemplo:**
```
[2025-05-08T01:20:00Z] ROLLBACK_WITH_PRESERVATION:
  target_snapshot: "snap-002"
  preserved_learnings: [
    "classification:LOGOS-RESOLUÇÃO confidence:0.92",
    "constraint:max_depth=5 validated:true"
  ]
  new_session_id: "sess-xyz123-b"
```

### 2.3 Recuperação de Falha Crítica

**Trigger:** `FAILSAFE` state ativado (STATES.md).

**Procedimento:**
1. **Isolamento:** Congelar toda a memória operacional (read-only).
2. **Diagnóstico:** Gerar dump de memória para análise.
3. **Opções de recuperação:**
   - **STRICT:** Requer intervenção manual, restaura último snapshot válido.
   - **LENIENT:** Permite continuar com avisos, limpa contexto contaminado.
   - **NONE:** Desativa verificações (uso por conta e risco).
4. **Logging:** Registrar falha em `failure_log` com stack trace.
5. **Notificação:** Emitir evento `FAILURE_DETECTED` para módulos interessados.

**Recuperação automática (LENIENT):**
- Limpar memória operacional e contextual
- Restaurar último snapshot nível 3
- Reiniciar em `IDLE` com flags de baixa confiança

---

# 🔄 INTEGRAÇÃO COM RUNTIME.md E STATES.md

## 1. Integração com RUNTIME.md

### 1.1 Etapa 0 — BOOTSTRAP (RUNTIME.md, linha 146)

**Ações de memória no bootstrap:**
```yaml
bootstrap_memory_init:
  - load_persistent_snapshots:
      path: "./memory/snapshots/"
      max_versions: 3
      validate_checksum: true
  
  - initialize_operational_registers:
      REG_INPUT: null
      REG_FEI_PSI: 0.0
      REG_ONTOLOGY: null
      REG_SESSION_ID: generate_uuid()
  
  - start_audit_logger:
      path: "./logs/audit/"
      retention_days: 30
      flush_interval: 5s
  
  - start_garbage_collector:
      passive_interval: 30s
      active_on_maintenance: true
      deep_interval: 6h
```

**Resultado:** `RUNTIME_READY` com memória inicializada.

### 1.2 Etapa 1 — INGESTÃO (RUNTIME.md, linha 185)

**Ações:**
- `REG_INPUT` ← input normalizado
- `REG_CONTEXT_HASH` ← hash do input
- Iniciar TTL de ciclo para registradores

### 1.3 Etapa 2 — FEI_GATE (RUNTIME.md, linha 251)

**Ações:**
- `REG_FEI_PSI` ← Ψ calculado
- Cachear resultado de Ψ por input_hash (TTL 60s)
- Se `Ψ < 0.60` por 3 ciclos: disparar `MEMORY_CONTAMINATION`

### 1.4 Governança de Contexto (RUNTIME.md, III)

**Princípio:** "Contexto é hierárquico, degradável, auditável, descartável."

**Implementação:**
- **Hierárquico:** Camadas (operacional → contextual → persistente)
- **Degradável:** TTL progressivo + invalidação por contaminação
- **Auditável:** Todos os acessos e modificações logados
- **Descartável:** ROLLBACK limpa contexto não-preservado

**Persistência indevida = contaminação cognitiva** (RUNTIME.md, linha 72):
- Detectar: `context_age > 300s` sem uso + `Ψ < 0.70`
- Ação: Invalidar contexto, disparar refinamento

### 1.5 TTL COGNITIVO (RUNTIME.md, linha 552)

**Seção TTL COGNITIVO em RUNTIME.md:**

```
TTL = Time To Live Cognitivo

Objetivo:
- Prevenir contaminação inferencial
- Evitar persistência indevida
- Reduzir acoplamento contextual excessivo

Mecanismos:
1. TTL por camada (ver MEMORY.md, seção ⏱)
2. Decaimento por relevância (fórmula em MEMORY.md)
3. Renovação por acesso
4. Coleta baseada em recursos

Consequências de TTL mal configurado:
- Inferência degradada (contexto obsoleto)
- Memória redundante (cache ineficiente)
- Resíduos semânticos (contaminação)
```

### 1.6 Snapshots (RUNTIME.md, linha 1121)

```
Snapshots mantidos: últimos 3 estados válidos
TTL de snapshot: 300s após última referência
Prioridade de retenção: estados com Ω ≥ 0.80
```

**Implementação:**
- Snapshot automático a cada transição para `ONTOLOGY_BINDING`
- Retenção circular (max 3)
- Prioridade: `Ω ≥ 0.80` → preservar por 1h (vs 5min padrão)

---

## 2. Integração com STATES.md

### 2.1 Estado MAINTENANCE (STATES.md, linha 22)

**Responsabilidade:** "Executa tarefas de limpeza, atualização de caches, preparação para próximo ciclo."

**Ações de memória em MAINTENANCE:**

```yaml
maintenance_memory_tasks:
  - garbage_collection:
      mode: ACTIVE
      aggressive: true  # limpa mais agressivo que passivo
      target_retention: 70%  # manter no mínimo 70% da memória
  
  - cache_optimization:
      rebuild_indexes: true
      defragment: true
      preload_common_patterns: true
  
  - snapshot_rotation:
      keep_last_n: 3
      archive_older: true
      archive_path: "./memory/archive/"
  
  - audit_log_rotation:
      compress_older_than: 24h
      archive_path: "./logs/archive/"
  
  - resource_calibration:
      adjust_cache_limits: true
      recalibrate_ttl_factors: true
```

**Transição:** `MAINTENANCE` → `IDLE` (sistema otimizado) ou `FEI_GATE` (pronto para novo processamento).

### 2.2 Estado ROLLBACK (STATES.md, linha 21)

**Responsabilidade:** "Reverte para estado anterior estável, limpa contexto contaminado."

**Tipos de rollback e impacto na memória:**

| Tipo | Escopo | Preservação | Uso |
|------|--------|-------------|-----|
| **ROLLBACK_FULL** | Estado completo | Nenhuma | Falhas críticas |
| **ROLLBACK_TO_FEI** | Até FEI_GATE | Cache de classificações | Falhas de classificação |
| **ROLLBACK_TO_NORMALIZATION** | Até NORMALIZATION | Input processado | Falhas de pré-processamento |
| **ROLLBACK_PARTIAL** | Seletivo | Caches não contaminados | Recuperação de recursos |
| **ROLLBACK_WITH_PRESERVATION** | Estado + metadados | Aprendizados estruturais | Melhoria contínua |

**Processo de rollback (STATES.md, seção 5.2):**

```
1. Checkpoint atual: salvar estado atual para análise pós-mortem
2. Identificar target: último estado estável (IDLE, NORMALIZATION, FEI_GATE)
3. Carregar snapshot do target
4. Limpar contexto contaminado mantendo aprendizados estruturais
5. Aplicar lições aprendidas como restrições adicionais
6. Retentar com parâmetros ajustados (profundidade reduzida, modo mais conservador)
```

**Eventos disparados:**
- `ROLLBACK_INIT` — início do rollback
- `MEMORY_CLEANSE` — limpeza de contexto
- `LEARNING_PRESERVE` — preservação de aprendizados (se aplicável)
- `ROLLBACK_COMPLETE` — rollback concluído

### 2.3 Gatilhos Relacionados a Memória

**RESOURCE_THRESHOLD_EXCEEDED** (STATES.md, linha 124):
```
Condição: Uso de memória > 90% ou CPU > 85% por >5s
Ação: Transita para ERROR_RESOURCE_EXHAUSTED → MAINTENANCE
```

**Implementação:**
- Monitoramento a cada 1s
- Se `memory_usage > threshold` por `duration`:
  - Disparar `MAINTENANCE` com foco em limpeza agressiva
  - Aplicar política de evicção emergency (max 50% redução)
  - Se não resolver em 10s: `ERROR_RESOURCE_EXHAUSTED`

---

## 3. Eventos e Notificações

### 3.1 Eventos de Memória

| Evento | Origem | Destino | Payload |
|--------|--------|---------|---------|
| `MEMORY_WRITE` | Qualquer componente | AuditLogger | `{key, value, ttl}` |
| `MEMORY_READ` | Cache lookup | MetricsCollector | `{key, hit}` |
| `MEMORY_EVICT` | GarbageCollector | AuditLogger | `{key, reason}` |
| `MEMORY_INVALIDATE` | InvalidationPolicy | CacheManager | `{key, cause}` |
| `SNAPSHOT_CREATE` | SnapshotManager | AuditLogger | `{snapshot_id, level}` |
| `SNAPSHOT_RESTORE` | RecoveryManager | AuditLogger | `{snapshot_id, target_state}` |
| `ROLLBACK_INIT` | StateMachine | MemoryManager | `{rollback_type, target}` |
| `ROLLBACK_COMPLETE` | StateMachine | AuditLogger | `{success, preserved_learnings}` |
| `CONTAMINATION_DETECTED` | FEI_GATE | MemoryManager | `{key, entropy, action}` |
| `GC_PASSIVE` | GarbageCollector | MetricsCollector | `{entries_removed, duration_ms}` |
| `GC_ACTIVE` | GarbageCollector | MetricsCollector | `{entries_removed, duration_ms, aggressive}` |

### 3.2 Subscribers Padrão

```yaml
event_subscribers:
  MEMORY_WRITE:
    - AuditLogger (obrigatório)
    - MetricsCollector (opcional)
  
  SNAPSHOT_RESTORE:
    - StateMachine (sincroniza estado)
    - AuditLogger (obrigatório)
    - FailureProtocols (se falha)
  
  ROLLBACK_INIT:
    - MemoryManager (limpeza)
    - CacheManager (invalidação seletiva)
    - AuditLogger (obrigatório)
  
  CONTAMINATION_DETECTED:
    - FEI_GATE (reavaliação)
    - ValidationLayer (verificação adicional)
```

---

# 📊 MÉTRICAS E MONITORAMENTO

## 1. Métricas de Memória

### 1.1 Métricas Operacionais

| Métrica | Descrição | Alvo | Unidade |
|---------|-----------|------|---------|
| `memory_usage_bytes` | Uso total de memória | < 80% do limite | bytes |
| `cache_hit_rate` | Taxa de acerto do cache | > 50% | ratio (0-1) |
| `cache_miss_rate` | Taxa de falha do cache | < 50% | ratio (0-1) |
| `ttl_expirations_total` | Total de TTLs expirados | — | counter |
| `gc_runs_total` | Coletas de lixo executadas | — | counter |
| `gc_entries_removed` | Entradas removidas por GC | — | counter |
| `snapshots_created` | Snapshots criados | — | counter |
| `snapshots_restored` | Snapshots restaurados | — | counter |
| `rollbacks_total` | Total de rollbacks | 0 (ideal) | counter |
| `contamination_events` | Eventos de contaminação | 0 (ideal) | counter |
| `audit_log_entries` | Entradas de log de auditoria | — | counter |

### 1.2 Métricas de Qualidade

| Métrica | Descrição | Cálculo | Alvo |
|---------|-----------|---------|------|
| `memory_efficiency` | Eficiência de uso | `(hit_rate × 0.6) + (1 - memory_pressure) × 0.4` | > 0.7 |
| `context_stability` | Estabilidade do contexto | Média de `Ψ` nas últimas 5 transições | > 0.80 |
| `snapshot_integrity` | Integridade de snapshots | `(valid_snapshots / total_snapshots)` | 1.0 |
| `recovery_success_rate` | Taxa de sucesso de recuperação | `(successful_rollbacks / total_rollbacks)` | > 0.95 |

### 1.3 Métricas de Desempenho

| Métrica | Descrição | Latência alvo |
|---------|-----------|---------------|
| `memory_read_latency_ms` | Latência de leitura | < 1ms |
| `memory_write_latency_ms` | Latência de escrita | < 2ms |
| `gc_pause_duration_ms` | Pausa durante GC | < 100ms (passivo), < 500ms (ativo) |
| `snapshot_save_duration_ms` | Tempo para salvar snapshot | < 200ms |
| `snapshot_restore_duration_ms` | Tempo para restaurar | < 300ms |

---

## 2. Alertas e Limites

```yaml
alerts:
  - name: HighMemoryUsage
    condition: memory_usage_bytes > 0.9 * memory_limit_bytes
    duration: 30s
    severity: WARNING
    action: trigger_maintenance
    
  - name: LowCacheHitRate
    condition: cache_hit_rate < 0.3
    duration: 5m
    severity: WARNING
    action: review_cache_policy
    
  - name: HighContamination
    condition: contamination_events > 0
    duration: 0s
    severity: CRITICAL
    action: immediate_rollback
    
  - name: GCLongPause
    condition: gc_pause_duration_ms > 500
    duration: 0s
    severity: WARNING
    action: adjust_gc_aggressiveness
    
  - name: SnapshotFailure
    condition: snapshot_save_failed == true
    duration: 0s
    severity: ERROR
    action: check_disk_space_and_retry
```

---

# 🔧 CONFIGURAÇÃO

## 1. Configuração Padrão (memory_config.yaml)

```yaml
memory:
  # Limites
  limits:
    max_operational_mb: 50
    max_contextual_mb: 200
    max_cache_entries: 1000
    max_cache_size_mb: 100
  
  # TTLs
  ttl:
    cycle: 0  # até fim do ciclo
    session: 60  # segundos
    contextual: 300  # segundos
    snapshot_default: 300  # segundos
    snapshot_priority: 1800  # segundos (Ω ≥ 0.80)
  
  # Cache
  cache:
    eviction_policy: "LRU"  # LRU, LFU, FIFO
    min_hit_rate: 0.5
    preload_patterns: true
    compression: false  # futuro: compressão para entradas grandes
  
  # Garbage Collection
  gc:
    passive_interval: 30s
    active_aggressive: true
    deep_interval: 6h
    target_retention_ratio: 0.7
  
  # Snapshots
  snapshots:
    auto_create: true
    checkpoint_levels: [2, 3]
    max_versions: 3
    archive_path: "./memory/archive/"
    validate_checksum: true
  
  # Auditoria
  audit:
    enabled: true
    log_all_reads: false  # amostragem 10%
    retention_days: 30
    critical_events_retention_days: 90
  
  # Rollback
  rollback:
    auto_on_contamination: true
    max_retries: 3
    preserve_on_rollback: true
    preserve_threshold_omega: 0.80
```

## 2. Overrides por Modo Operacional

```yaml
mode_overrides:
  QUICK:
    ttl:
      session: 30  # mais agressivo
      contextual: 120
    cache:
      max_entries: 500  # menor
    gc:
      passive_interval: 15s
  
  BALANCED:
    # usa configuração padrão
  
  DEEP:
    ttl:
      session: 120  # mais longo
      contextual: 600
    cache:
      max_entries: 2000  # maior
      min_hit_rate: 0.6  # mais exigente
    snapshots:
      checkpoint_levels: [1, 2, 3]  # mais checkpoints
    gc:
      aggressive: false  # coleta mais conservadora
```

---

# 📝 EXEMPLOS DE USO

## Exemplo 1: Ciclo Normal de Processamento

```
Sessão: sess-abc123
Input: "Otimizar algoritmo de ordenação para 1 milhão de registros"

1. INPUT_CAPTURE
   → REG_INPUT = "Otimizar algoritmo de ordenação para 1 milhão de registros"
   → REG_CONTEXT_HASH = "sha256:7f8e9d..."
   → TTL: ciclo atual

2. NORMALIZATION
   → Tokens: ["otimizar", "algoritmo", "ordenação", "1M", "registros"]
   → Contexto: "complexidade algorítmica, grande volume"

3. FEI_GATE
   → Ψ = 0.88 (estável)
   → REG_FEI_PSI = 0.88
   → Cache: key="7f8e9d:FEI" value=0.88 TTL=60s

4. ONTOLOGY_BINDING
   → Classificação: LOGOS / ALGORITMIA / RESOLUÇÃO / OTIMIZAÇÃO
   → REG_ONTOLOGY = {vector: "LOGOS", pillar: "ALGORITMIA", n2: "1.1", n3: "RESOLUÇÃO", n4: "OTIMIZAÇÃO"}
   → TTL: 60s
   → Snapshot nível 2 criado

5. DEPENDENCY_RESOLUTION
   → Dependências: N3-1_1_1 (DECOMPOSIÇÃO), N3-1_1_3 (VALIDAÇÃO)
   → REG_DEPENDENCIES = ["N3-1_1_1", "N3-1_1_3"]

6. COGNITIVE_COMPILATION
   → REG_COMPILATION = "Instruções executáveis..."
   → Cache: key="LOGOS-RESOLUÇÃO:OTIMIZAÇÃO" value=instruções TTL=300s

7. VALIDATION_LAYER
   → REG_VALIDATION = true

8. OUTPUT_RENDER
   → Output gerado
   → Snapshot nível 3 criado
   → Transição para MAINTENANCE

9. MAINTENANCE
   → GC passivo: remove entradas TTL expirado
   → Cache otimizado
   → Transição para IDLE

Resultado: Sessão concluída, memória operacional limpa, contexto preservado por 300s.
```

## Exemplo 2: Rollback com Preservação

```
Cenário: Classificação inicial LOGOS-RESOLUÇÃO, mas após dependências detecta conflito.

1. ONTOLOGY_BINDING
   → Classificação: LOGOS / ALGORITMIA / RESOLUÇÃO / DECOMPOSIÇÃO_BINÁRIA
   → Ω = 0.82 (estável)

2. DEPENDENCY_RESOLUTION
   → Detecta dependência circular: DECOMPOSIÇÃO_BINÁRIA → REQUISITOS_ANÁLISE → DECOMPOSIÇÃO_BINÁRIA
   → ERROR_DEPENDENCY_CIRCULAR

3. ROLLBACK_WITH_PRESERVATION
   → Target snapshot: nível 2 (antes de ONTOLOGY_BINDING)
   → Aprendizados preservados:
     • Classificação: LOGOS-RESOLUÇÃO (Ω=0.82) → mantida
     • Restrição: "evitar decomposição binária em problemas de grande volume"
   → Nova sessão: sess-abc123-b

4. Retry
   → FEI_GATE com restrição adicional
   → Nova classificação: LOGOS / ALGORITMIA / RESOLUÇÃO / DIVIDE_AND_CONQUER
   → Sucesso

5. Learning registrado:
   HISTORICAL_LEARNING:
     - problem: "dependência circular em decomposição binária"
     - solution: "usar divide_and_conquer para grandes volumes"
     - confidence: 0.88
```

## Exemplo 3: Contaminação e Limpeza

```
Cenário: Input ambíguo gera classificação instável.

1. Ciclo 1:
   FEI_GATE: Ψ = 0.65 (parcial)
   Classificação: PATHOS / ETHOS / VALORES (incerto)
   → Cache: key="input1:PATHOS-ETHOS-VALORES"

2. Ciclo 2 (refinamento):
   FEI_GATE: Ψ = 0.58 (piora)
   Classificação: KHAOS / ENTROPIA / CAOS (instável)
   → Contaminação detectada: H_sem = 0.52

3. Ação:
   → CONTAMINATION_DETECTED event
   → Isolar entrada "input1:PATHOS-ETHOS-VALORES"
   → Invalidar cache relacionado
   → Disparar ROLLBACK_TO_FEI

4. Limpeza:
   → Entrada contaminada removida
   → Log: "INVALIDATION: key=input1:PATHOS-ETHOS-VALORES reason=CONTAMINATION entropy=0.52"
   → Contexto limpo

5. Ciclo 3 (reformulação):
   → Input reformulado pelo usuário
   → Nova classificação estável
```

---

# ⚠️ CONSIDERAÇÕES DE SEGURANÇA

## 1. Isolamento de Sessões

Cada `session_id` possui namespace isolado na memória contextual.

**Prevenção de vazamento:**
- Limpeza automática ao finalizar sessão (TTL 60s)
- Validação de `session_id` em todo acesso
- Auditoria de cross-session access (alerta se detectado)

## 2. Sanitização de Dados

**Antes de persistir:**
- Remover dados sensíveis (PII) se configurado
- Anonimizar hashes de input se necessário
- Criptografar snapshots se contêm dados confidenciais

## 3. Limitação de Taxa

**Para prevenir DoS por memória:**
- Máximo de 1000 writes por minuto por session
- Limite de 100MB por sessão
- Bloqueio automático se excedido (FAILSAFE)

---

# 🔄 EVOLUÇÃO E MANUTENÇÃO

## 1. Versionamento de Esquemas

**Estratégia:** Versionamento semântico de snapshots e estruturas.

```
Formato: v{major}.{minor}
Exemplo: v1.0, v1.1, v2.0

Migrações:
- v1.0 → v1.1: adicionar campo "quality_metrics" (backward compatible)
- v1.x → v2.0: mudança estrutural major (não backward compatible)
```

**Detecção:** Ao carregar snapshot, verificar `schema_version`. Se incompatível:
- Tentar migração automática (se disponível)
- Caso contrário: falhar com `ERROR_SNAPSHOT_INCOMPATIBLE`

## 2. Compactação e Arquivo

**Política de arquivamento:**
- Snapshots > 24h: arquivar para `./memory/archive/`
- Logs de auditoria > 7 dias: compactar em `.gz`
- Histórico inferencial > 30 dias: arquivar em `.jsonl.gz`

**Retenção final:**
- Snapshots: últimos 3 ativos + arquivo ilimitado
- Logs: 90 dias (críticos 365 dias)
- Histórico: 30 dias ativos, arquivo ilimitado

## 3. Monitoramento de Saúde

**Health check a cada 5 minutos:**
```
CHECK_MEMORY_HEALTH:
  - cache_hit_rate > 0.3? ✓
  - memory_usage < 0.9? ✓
  - no_contamination_last_hour? ✓
  - snapshot_integrity == 1.0? ✓
  - gc_running_normally? ✓
  
  Se falha: → MAINTENANCE ou ALERTA
```

---

# 📚 GLOSSÁRIO

| Termo | Definição |
|-------|------------|
| **TTL Cognitivo** | Time To Live baseado em relevância semântica, não apenas tempo |
| **Contaminação** | Degradação da qualidade da memória por dados obsoletos ou conflitantes |
| **Snapshot** | Ponto de recuperação com estado completo da memória |
| **Checkpoint** | Nível de importância de um snapshot (0-4) |
| **Rollback** | Reversão para estado anterior |
| **Garbage Collection** | Coleta de lixo: remoção de entradas inválidas ou obsoletas |
| **Cache Hit Rate** | Porcentagem de acessos ao cache que encontram dados válidos |
| **Ψ (Psi)** | Potencial de Resolução — métrica de estabilidade semântica |
| **Ω (Omega)** | Estabilidade Ontológica — confiança na classificação N0-N4 |
| **H_sem** | Entropia Semântica — medida de ambiguidade |
| **Registradores** | Variáveis operacionais do pipeline cognitivo |

---

# 🔗 REFERÊNCIAS CRUZADAS

- **RUNTIME.md** — Seção III (Governança de Contexto), Seção ⏱ (TTL COGNITIVO), Etapa 0 (BOOTSTRAP)
- **STATES.md** — Estados MAINTENANCE (linha 22), ROLLBACK (linha 21), ROLLBACK_WITH_PRESERVATION (linha 189)
- **CORE.md** — Princípio de integridade e estabilidade
- **N4-1_1_2-LOGOS-COMPLEXIDADE.md** — Padrão de cache (hits > 50%)

---

# 📋 CHECKLIST DE IMPLEMENTAÇÃO

- [x] Arquitetura de memória operacional (camadas e hierarquia)
- [x] Mecanismos de persistência e recuperação
- [x] Sistema de TTL cognitivo (Time To Live)
- [x] Políticas de invalidação e garbage collection
- [x] Histórico inferencial e rastreamento
- [x] Integração com RUNTIME.md e STATES.md
- [x] Exemplos de uso e configuração

---

**Status:** Produção  
**Última atualização:** 2025-05-08  
**Próxima revisão:** Após implementação inicial e feedback de RUNTIME/STATES

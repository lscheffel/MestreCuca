# Plano de Transformação N4 → JSON Enriquecido

## 1. Schema JSON Definitivo

```json
{
  "id": "S1.L1.1.1-A",
  "nivel": "N4",
  "eixo": "SINTRÓPICO",
  "pilar": "LOGOS",
  "dominio": "ALGORITMIA",
  "subarvore": "RESOLUÇÃO",
  "conceito": "DECOMPOSIÇÃO",
  "foco": "Divisão",
  "descricao": "Técnica de quebrar problemas complexos em partes menores e gerenciáveis.",
  "sinonimos": ["fragmentação", "particionamento", "análise de componentes"],
  "relacoes": ["RECURSÃO", "ABSTRAÇÃO"],
  "tags": ["algoritmos", "design", "engenharia"],
  "gatilho": "Problema complexo sem estrutura clara",
  "acao": "Identificar subproblemas independentes",
  "restricao": "Avaliar limites de decomposição",
  "verificacao": "Subproblemas resolvidos independentemente",
  "exemplos": [
    "Merge sort dividindo array",
    "Arquitetura de microserviços",
    "Análise de caso na advocacia"
  ],
  "anti_exemplos": [
    "Dividir sem unir",
    "Subproblemas interdependentes",
    "Over-engineering"
  ],
  "analogias": [
    "Quebrar um osso em pedaços para analisar",
    "Dividir tarefas domésticas entre familiares"
  ],
  "aplicacoes": [
    "Design de algoritmos",
    "Arquitetura de software",
    "Gestão de projetos"
  ],
  "relacoes_cruzadas": [
    "S1.L1.1.1-B",
    "S1.L1.1.1-C"
  ],
  "polaridade": "sintrópica",
  "vetor_simbolico": ["divisão", "organização", "clareza"]
}
```

## 2. Mapeamento de Campos

| Campo Original | Campo JSON | Transformação |
|----------------|------------|-----------------|
| cell_id | id | Aplicar mapeamento hierárquico N0-N4 |
| dominio | eixo | Mapear: S1 (SINTRÓPICO) / E2 (ENTRÓPICO) |
| dominio | pilar | Mapear: L/B/P (S1) / K/A/M (E2) |
| dominio | dominio | Mapear: 1-3 (por pilar) |
| n3_ref | subarvore | Mapear: 1-3 (por domínio) |
| nome | conceito | Direto |
| gatilho | gatilho | Direto |
| acao | acao | Direto |
| restricao | restricao | Direto |
| verificacao | verificacao | Direto |

## 3. Estrutura de Diretórios

```
n4_json/
├── S1.L1.1.1-A.json
├── S1.L1.1.1-B.json
├── S1.L1.1.1-C.json
├── S1.L1.1.2-A.json
├── S1.L1.1.2-B.json
├── S1.L1.1.2-C.json
...
├── E2.K1.1.1-A.json
├── E2.K1.1.1-B.json
├── E2.K1.1.1-C.json
├── E2.A2.1.1-A.json
├── E2.A2.1.1-B.json
├── E2.A2.1.1-C.json
├── E2.M3.1.1-A.json
├── E2.M3.1.1-B.json
├── E2.M3.1.1-C.json
└── embeddings_index.json
```

## 4. Mapeamentos Hierárquicos

### 4.1 Mapeamento Eixo (N0)
- S1 = SINTRÓPICO
- E2 = ENTRÓPICO

### 4.2 Mapeamento Pilar (N1) - Depende do Eixo

**SINTRÓPICO (S1):**
- S1.L1 = LOGOS
- S1.B2 = BIOS
- S1.P3 = PATHOS

**ENTRÓPICO (E2):**
- E2.K1 = KHAOS
- E2.A2 = APEIRON
- E2.M3 = MYTHOS

### 4.3 Mapeamento Domínio (N2) - Depende do Pilar

**LOGOS (S1.L1):**
- S1.L1.1 = ALGORITMIA
- S1.L1.2 = NOMOS
- S1.L1.3 = MECÂNICA

**BIOS (S1.B2):**
- S1.B2.1 = OIKOS
- S1.B2.2 = SOMA
- S1.B2.3 = METABOLISMO

**PATHOS (S1.P3):**
- S1.P3.1 = ALTERIDADE
- S1.P3.2 = ESTÉTICA
- S1.P3.3 = ETHOS

**KHAOS (E2.K1):**
- E2.K1.1 = ENTROPIA
- E2.K1.2 = SINGULARIDADE
- E2.K1.3 = SÍNTESE

**APEIRON (E2.A2):**
- E2.A2.1 = ESCALA
- E2.A2.2 = VIBRATIO
- E2.A2.3 = VÁCUO

**MYTHOS (E2.M3):**
- E2.M3.1 = ARQUÉTIPO
- E2.M3.2 = NARRATIVA
- E2.M3.3 = MISTÉRIO

### 4.4 Mapeamento Subárvore (N3) - Depende do Domínio

**ALGORITMIA (S1.L1.1):**
- S1.L1.1.1 = RESOLUÇÃO
- S1.L1.1.2 = OPTIMIZAÇÃO
- S1.L1.1.3 = VALIDAÇÃO

**NOMOS (S1.L1.2):**
- S1.L1.2.1 = LEGISLAÇÃO
- S1.L1.2.2 = CONTORNO
- S1.L1.2.3 = PACTO

**MECÂNICA (S1.L1.3):**
- S1.L1.3.1 = ESTATICA
- S1.L1.3.2 = DINAMICA
- S1.L1.3.3 = TERMOTRANSDINÂMICA

**OIKOS (S1.B2.1):**
- S1.B2.1.1 = MORADA
- S1.B2.1.2 = TERRITORIO
- S1.B2.1.3 = PROVISAO

**SOMA (S1.B2.2):**
- S1.B2.2.1 = NUTRIÇÃO
- S1.B2.2.2 = SUSTENTO
- S1.B2.2.3 = METABOLISMO

**METABOLISMO (S1.B2.3):**
- S1.B2.3.1 = SANEAMENTO
- S1.B2.3.2 = HIGIENE
- S1.B2.3.3 = PURIFICAÇÃO

**ALTERIDADE (S1.P3.1):**
- S1.P3.1.1 = ALTERIDADE
- S1.P3.1.2 = EMPATIA
- S1.P3.1.3 = COMPREENSÃO_PROFUNDA

**ESTÉTICA (S1.P3.2):**
- S1.P3.2.1 = ESTÉTICA
- S1.P3.2.2 = SENSIBILIDADE
- S1.P3.2.3 = HARMONIA

**ETHOS (S1.P3.3):**
- S1.P3.3.1 = VALORES
- S1.P3.3.2 = VIRTUDE
- S1.P3.3.3 = RESPONSABILIDADE

**ENTROPIA (E2.K1.1):**
- E2.K1.1.1 = DEGRADAÇÃO
- E2.K1.1.2 = DISSIPAÇÃO
- E2.K1.1.3 = CAOS

**SINGULARIDADE (E2.K1.2):**
- E2.K1.2.1 = TRANSFORMAÇÃO
- E2.K1.2.2 = ADAPTAÇÃO
- E2.K1.2.3 = TRANSCENDENCIA

**SÍNTESE (E2.K1.3):**
- E2.K1.3.1 = FUSÃO
- E2.K1.3.2 = HIBRIDISMO
- E2.K1.3.3 = SÍNTESE

**ESCALA (E2.A2.1):**
- E2.A2.1.1 = ESCALAMENTO
- E2.A2.1.2 = PROPORÇÃO_AUREA
- E2.A2.1.3 = ISOMORFISMO

**VIBRATIO (E2.A2.2):**
- E2.A2.2.1 = TAMANHO_NATUREZA
- E2.A2.2.2 = EXPERIÊNCIA_ESCALAR
- E2.A2.2.3 = LEI_ESCALAR

**VÁCUO (E2.A2.3):**
- E2.A2.3.1 = ONDA
- E2.A2.3.2 = POTENCIAL_ATUAL
- E2.A2.3.3 = PADRAO_ONDA

**ARQUÉTIPO (E2.M3.1):**
- E2.M3.1.1 = PADRAO_PRIMORDIAL
- E2.M3.1.2 = RECONHECIMENTO_ARQUETÍPICO
- E2.M3.1.3 = ATIVAÇÃO_SIMPOLAR

**NARRATIVA (E2.M3.2):**
- E2.M3.2.1 = TEIA
- E2.M3.2.2 = LINHA_SENTIDO
- E2.M3.2.3 = HISTÓRIA_VIVIDA

**MISTÉRIO (E2.M3.3):**
- E2.M3.3.1 = SÍNTESE_OPOSTOS
- E2.M3.3.2 = ROTEIRO_INVISIBLE
- E2.M3.3.3 = PADRAO_COMPORTAMENTAL

### 4.5 Mapeamento Célula (N4)
- A = Primeira célula
- B = Segunda célula
- C = Terceira célula

## 5. Script de Transformação

### 5.1 Estrutura do Script
```python
# n4_to_json.py
import json
import os

# 1. Carregar celulas_n4 do create_n4_manual.py
# 2. Aplicar mapeamentos hierárquicos
# 3. Gerar campos semânticos (exemplos, anti_exemplos, analogias, etc.)
# 4. Salvar arquivos JSON individuais
# 5. Gerar embeddings_index.json
```

### 5.2 Campos Semânticos a Gerar
- `exemplos`: 3 exemplos concretos do conceito
- `anti_exemplos`: 2-3 contrários do conceito
- `analogias`: 2 analogias do cotidiano
- `aplicacoes`: 3 aplicações práticas
- `relacoes_cruzadas`: IDs de células relacionadas
- `polaridade`: "sintrópica" (fixo para SINTRÓPICO) ou "entrópica" (fixo para ENTRÓPICO)
- `vetor_simbolico`: 3 palavras-chave simbólicas

## 6. Validação

- [ ] 162 arquivos JSON gerados
- [ ] Estrutura válida em todos os arquivos
- [ ] embeddings_index.json com todos os IDs
- [ ] Consistência de eixo/pilar/domínio/subárvore/célula

## 7. Estrutura Fractal Completa

A ontologia N4 possui 162 combinações (2 × 3 × 3 × 3 × 3):

| Nível | Componente | Valores |
|-------|------------|---------|
| N0 | Eixo | S1 (SINTRÓPICO), E2 (ENTRÓPICO) |
| N1 | Pilar | L, B, P (S1) / K, A, M (E2) |
| N2 | Domínio | 1-3 (por pilar) |
| N3 | Subárvore | 1-3 (por domínio) |
| N4 | Célula | A, B, C |

**Fórmula do ID:** `Eixo.Pilar.Domínio.Subárvore-Célula`

**Exemplos:**
- `S1.L1.1.1-A` = SINTRÓPICO, LOGOS, ALGORITMIA, RESOLUÇÃO, DECOMPOSIÇÃO
- `S1.L1.1.2-B` = SINTRÓPICO, LOGOS, ALGORITMIA, OPTIMIZAÇÃO, MEMOIZAÇÃO
- `E2.K1.1.1-A` = ENTRÓPICO, KHAOS, ENTROPIA, DEGRADAÇÃO, DEGRADAÇÃO_BÁSICA
- `S1.P3.1.1-A` = SINTRÓPICO, PATHOS, ALTERIDADE, ALTERIDADE, ALTERIDADE_BÁSICA
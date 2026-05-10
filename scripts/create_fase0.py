#!/usr/bin/env python3
"""
FASE 0 — Criação completa da estrutura de diretórios e configuração inicial
do sistema cognitivo ontológico.
"""

import os
import stat

BASE = r"E:\Arquivos\Área de Trabalho\MestreCuca"

# ============================================================
# 1. ESTRUTURA DE DIRETÓRIOS
# ============================================================

dirs = [
    # Ontology hierarchy
    "ontology/n0",
    "ontology/n1",
    "ontology/n2",
    "ontology/n3",
    "ontology/n4",
    # Data stores
    "data/json",
    "data/embeddings",
    "data/indexes",
    "data/graphs",
    # Runtime
    "runtime",
    # Core modules
    "core",
    # Tools
    "tools",
    # Prompt templates
    "prompts/classifier",
    "prompts/retrieval",
    "prompts/synthesis",
    "prompts/validation",
    "prompts/routing",
    # Kilo internal
    ".kilo/agents",
    ".kilo/memory",
    ".kilo/orchestrators",
    ".kilo/prompts/classifier",
    ".kilo/prompts/retrieval",
    ".kilo/prompts/synthesis",
    ".kilo/prompts/validation",
    ".kilo/prompts/routing",
    # Tests
    "tests",
]

created = 0
for d in dirs:
    full = os.path.join(BASE, d)
    os.makedirs(full, exist_ok=True)
    created += 1
    print(f"  [DIR]  {d}/")

print(f"\n  Total de diretórios criados/verificados: {created}")


# ============================================================
# 2. requirements.txt
# ============================================================

requirements_content = """numpy>=1.24
networkx>=3.0
sentence-transformers>=2.2
pyyaml>=6.0
scikit-learn>=1.2
rich>=13.0
tqdm>=4.65
"""

req_path = os.path.join(BASE, "requirements.txt")
with open(req_path, "w", encoding="utf-8") as f:
    f.write(requirements_content)
print(f"\n  [FILE] requirements.txt")


# ============================================================
# 3. config/ontology.yaml
# ============================================================

ontology_content = """# =============================================================================
# ONTOLOGIA COGNITIVA — Definição completa da estrutura fractal N0→N4
# Base: 162 células N4 (2 × 3 × 3 × 3 × 3)
# =============================================================================

meta:
  versao: "3.0.0"
  descricao: "Ontologia cognitiva fractal com 6 camadas hierárquicas"
  autor: "Sistema MestreCuca"
  data_criacao: "2026-05-09"
  total_celulas_n4: 162
  fator_cardinalidade: "2×3×3×3×3"

# =============================================================================
# NÍVEL 0 — VETORES (2 vetores primordiais)
# =============================================================================
n0_vetores:
  - id: "SINTR"
    nome: "SINTRÓPICO"
    descricao: "Foco em resolução, definição, execução. Redução de incerteza."
    natureza: convergente
    axioma: "Máxima clareza, ação direta, redução de entropia informacional"
    dominios_compativeis:
      - ALGORITMIA
      - NOMOS
      - MECÂNICA
      - OIKOS
      - SOMA
      - METABOLISMO
      - ETHOS
      - ALTERIDADE
      - ESTÉTICA

  - id: "ENTR"
    nome: "ENTRÓPICO"
    descricao: "Foco em exploração, expansão, possibilidades. Inovação."
    natureza: divergente
    axioma: "Expansão de possibilidades, exploração estratégica, geração de novidade"
    dominios_compativeis:
      - ENTROPIA
      - SINGULARIDADE
      - SÍNTESE
      - ESCALA
      - VIBRATIO
      - VÁCUO
      - ARQUÉTIPO
      - NARRATIVA
      - MISTÉRIO

# =============================================================================
# NÍVEL 1 — PILARES (6 pilares ontológicos)
# =============================================================================
n1_pilares:
  - id: "LOGOS"
    nome: "LOGOS"
    descricao: "Sistemas, lógica, estrutura, processos"
    crenca: "Estrutura, hierarquia, lógica inquestionável"
    natureza: processo
    vetor_default: SINTR
    sub_arvores: 3

  - id: "BIOS"
    nome: "BIOS"
    descricao: "Organismos, vida, sustentabilidade, integridade"
    crenca: "Preservação, sustentabilidade, integridade"
    natureza: organismo
    vetor_default: SINTR
    sub_arvores: 3

  - id: "PATHOS"
    nome: "PATHOS"
    descricao: "Humano, conexões, significado, decisão"
    crenca: "Impacto humano, significado, conexão"
    natureza: relacao
    vetor_default: SINTR
    sub_arvores: 3

  - id: "KHAOS"
    nome: "KHAOS"
    descricao: "Ruptura, inovação, adaptação, transformação"
    crenca: "Inovação através da ruptura, adaptabilidade"
    natureza: transformacao
    vetor_default: ENTR
    sub_arvores: 3

  - id: "APEIRON"
    nome: "APEIRON"
    descricao: "Escala, estratégia, transcendência, sistêmico"
    crenca: "Visão sistêmica, escalabilidade, transcendência"
    natureza: escala
    vetor_default: ENTR
    sub_arvores: 3

  - id: "MYTHOS"
    nome: "MYTHOS"
    descricao: "Narrativa, símbolo, autoridade, arquétipo"
    crenca: "Narrativa poderosa, simbolismo, autoridade"
    natureza: simbolo
    vetor_default: ENTR
    sub_arvores: 3

# =============================================================================
# NÍVEL 2 — DOMÍNIOS (18 domínios: 3 por pilar)
# =============================================================================
n2_dominios:
  # --- LOGOS ---
  - id: "1.1"
    pilar: LOGOS
    nome: "ALGORITMIA"
    descricao: "Processos computacionais, resolução e otimização"
    sub_arvores: [RESOLUCAO, OTIMIZACAO, VALIDACAO]

  - id: "1.2"
    pilar: LOGOS
    nome: "NOMOS"
    descricao: "Legislação, contorno e pacto normativo"
    sub_arvores: [LEGISLACAO, CONTORNO, PACTO]

  - id: "1.3"
    pilar: LOGOS
    nome: "MECÂNICA"
    descricao: "Estática, dinâmica e termotransdinâmica"
    sub_arvores: [ESTATICA, DINAMICA, TERMOTRANSDINAMICA]

  # --- BIOS ---
  - id: "2.1"
    pilar: BIOS
    nome: "OIKOS"
    descricao: "Morada, território e provisão"
    sub_arvores: [MORADA, TERRITORIO, PROVISAO]

  - id: "2.2"
    pilar: BIOS
    nome: "SOMA"
    descricao: "Integridade, vitalidade e homeostase"
    sub_arvores: [INTEGRIDADE, VITALIDADE, HOMEOSTASE]

  - id: "2.3"
    pilar: BIOS
    nome: "METABOLISMO"
    descricao: "Anabolismo, catabolismo e ciclo"
    sub_arvores: [ANABOLISMO, CATABOLISMO, CICLO]

  # --- PATHOS ---
  - id: "3.1"
    pilar: PATHOS
    nome: "ETHOS"
    descricao: "Valores, virtude e responsabilidade"
    sub_arvores: [VALORES, VIRTUDE, RESPONSABILIDADE]

  - id: "3.2"
    pilar: PATHOS
    nome: "ALTERIDADE"
    descricao: "Reconhecimento, empatia e diálogo"
    sub_arvores: [RECONHECIMENTO, EMPATIA, DIALOGO]

  - id: "3.3"
    pilar: PATHOS
    nome: "ESTÉTICA"
    descricao: "Harmonia, expressão e impacto"
    sub_arvores: [HARMONIA, EXPRESSAO, IMPACTO]

  # --- KHAOS ---
  - id: "4.1"
    pilar: KHAOS
    nome: "ENTROPIA"
    descricao: "Degradação, dissipação e caos"
    sub_arvores: [DEGRADACAO, DISSIPACAO, CAOS]

  - id: "4.2"
    pilar: KHAOS
    nome: "SINGULARIDADE"
    descricao: "Exceção, infinito e transformação"
    sub_arvores: [EXCEPCAO, INFINITO, TRANSFORMACAO]

  - id: "4.3"
    pilar: KHAOS
    nome: "SÍNTESE"
    descricao: "Fusão, hibridismo e transcendência"
    sub_arvores: [FUSAO, HIBRIDISMO, TRANSCENDENCIA]

  # --- APEIRON ---
  - id: "5.1"
    pilar: APEIRON
    nome: "PROPORÇÃO"
    descricao: "Escalamento, áurea e isomorfismo"
    sub_arvores: [ESCALAMENTO, AUREA, ISOMORFISMO]

  - id: "5.2"
    pilar: APEIRON
    nome: "VIBRATIO"
    descricao: "Frequência, ressonância e onda"
    sub_arvores: [FREQUENCIA, RESONANCIA, ONDA]

  - id: "5.3"
    pilar: APEIRON
    nome: "VÁCUO"
    descricao: "Potencial, silêncio e campo"
    sub_arvores: [POTENCIAL, SILENCIO, CAMPO]

  # --- MYTHOS ---
  - id: "6.1"
    pilar: MYTHOS
    nome: "ARQUÉTIPO"
    descricao: "Padrão primordial, comportamento e símbolo"
    sub_arvores: [PADRAO_PRIMORDIAL, COMPORTAMENTO, SIMBOLO]

  - id: "6.2"
    pilar: MYTHOS
    nome: "NARRATIVA"
    descricao: "Teia, linha de sentido e história vivida"
    sub_arvores: [TEIA, LINHA_SENTIDO, HISTORIA_VIVIDA]

  - id: "6.3"
    pilar: MYTHOS
    nome: "MISTÉRIO"
    descricao: "Incompreensão, intuição e revelação"
    sub_arvores: [INCOMPREENSAO, INTUICAO, REVELACAO]

# =============================================================================
# NÍVEL 3 — SUBÁRVORES (54 subárvores)
# =============================================================================
n3_sub_arvores:
  # LOGOS
  RESOLUCAO: { dominio: ALGORITMIA, pilar: LOGOS, celulas: [DECOMPOSICAO, SEQUENCIA, CASO_BASE] }
  OTIMIZACAO: { dominio: ALGORITMIA, pilar: LOGOS, celulas: [MELHORIA, EFICIENCIA, EQUILIBRIO] }
  VALIDACAO: { dominio: ALGORITMIA, pilar: LOGOS, celulas: [VERIFICACAO, CORRECAO, CERTIFICACAO] }
  LEGISLACAO: { dominio: NOMOS, pilar: LOGOS, celulas: [LEI, JURISPRUDENCIA, REGULAMENTO] }
  CONTORNO: { dominio: NOMOS, pilar: LOGOS, celulas: [FRONTEIRA, EXCECAO, ADAPTACAO] }
  PACTO: { dominio: NOMOS, pilar: LOGOS, celulas: [ACORDO, COMPROMISSO, RENEGOCIACAO] }
  ESTATICA: { dominio: MECANICA, pilar: LOGOS, celulas: [EQUILIBRIO, RESISTENCIA, RIGIDEZ] }
  DINAMICA: { dominio: MECANICA, pilar: LOGOS, celulas: [MOVIMENTO, FORCA, ENERGIA] }
  TERMOTRANSDINAMICA: { dominio: MECANICA, pilar: LOGOS, celulas: [CALOR, ENTROPIA_SIST, IRREVERSIBILIDADE] }

  # BIOS
  MORADA: { dominio: OIKOS, pilar: BIOS, celulas: [PROTECAO, RECURSOS, SANEAMENTO] }
  TERRITORIO: { dominio: OIKOS, pilar: BIOS, celulas: [ESPACO, DELIMITACAO, SOBERANIA] }
  PROVISAO: { dominio: OIKOS, pilar: BIOS, celulas: [ARMAZENAMENTO, DISTRIBUICAO, RACIONALIZACAO] }
  INTEGRIDADE: { dominio: SOMA, pilar: BIOS, celulas: [COESAO, CONSCIENCIA, IDENTIDADE] }
  VITALIDADE: { dominio: SOMA, pilar: BIOS, celulas: [NASCIMENTO, CRESCIMENTO, RENOVACAO] }
  HOMEOSTASE: { dominio: SOMA, pilar: BIOS, celulas: [REGULACAO, ADAPTACAO, EQUILIBRIO] }
  ANABOLISMO: { dominio: METABOLISMO, pilar: BIOS, celulas: [CONSTRUCAO, SÍNTESE, ACUMULACAO] }
  CATABOLISMO: { dominio: METABOLISMO, pilar: BIOS, celulas: [DECOMPOSICAO, LIBERACAO, DESCARTE] }
  CICLO: { dominio: METABOLISMO, pilar: BIOS, celulas: [REPETICAO, REGENERACAO, CIRCULARIDADE] }

  # PATHOS
  VALORES: { dominio: ETHOS, pilar: PATHOS, celulas: [ALINHAMENTO, CONFLITO, TRANSPARENCIA] }
  VIRTUDE: { dominio: ETHOS, pilar: PATHOS, celulas: [HABITO, DISCERNIMENTO, EXCELENCIA] }
  RESPONSABILIDADE: { dominio: ETHOS, pilar: PATHOS, celulas: [DEVER, PRESTACAO_CONTAS, REPARACAO] }
  RECONHECIMENTO: { dominio: ALTERIDADE, pilar: PATHOS, celulas: [IDENTIDADE, VALIDACAO, MEMORIA] }
  EMPATIA: { dominio: ALTERIDADE, pilar: PATHOS, celulas: [COMPREENSAO, SENSIBILIZACAO, CONEXAO] }
  DIALOGO: { dominio: ALTERIDADE, pilar: PATHOS, celulas: [COMUNICACAO, NEGOCIACAO, CONCILIACAO] }
  HARMONIA: { dominio: ESTETICA, pilar: PATHOS, celulas: [PROPORCAO, RITMO, UNIDADE] }
  EXPRESSAO: { dominio: ESTETICA, pilar: PATHOS, celulas: [CRIACAO, ARTICULACAO, ESTILO] }
  IMPACTO: { dominio: ESTETICA, pilar: PATHOS, celulas: [INFLUENCIA, TRANSFORMACAO, LEGADO] }

  # KHAOS
  DEGRADACAO: { dominio: ENTROPIA, pilar: KHAOS, celulas: [EROSAO, CORRUPCAO, DISSOLUCAO] }
  DISSIPACAO: { dominio: ENTROPIA, pilar: KHAOS, celulas: [DISPERSSAO, VAZAMENTO, EVAPORACAO] }
  CAOS: { dominio: ENTROPIA, pilar: KHAOS, celulas: [DESORDENACAO, ALEATORIEDADE, CRISE] }
  EXCEPCAO: { dominio: SINGULARIDADE, pilar: KHAOS, celulas: [ANOMALIA, DESVIACAO, INOVACAO] }
  INFINITO: { dominio: SINGULARIDADE, pilar: KHAOS, celulas: [ILIMITADO, INFINITESIMO, PARADOXO] }
  TRANSFORMACAO: { dominio: SINGULARIDADE, pilar: KHAOS, celulas: [METAMORFOSE, TRANSPOSICAO, RECONVERSAO] }
  FUSAO: { dominio: SINTES, pilar: KHAOS, celulas: [MISTURA, CONVERGENCIA, AMALGAMACAO] }
  HIBRIDISMO: { dominio: SINTES, pilar: KHAOS, celulas: [MISCEGENIA, SINCRRETISMO, NOVO] }
  TRANSCENDENCIA: { dominio: SINTES, pilar: KHAOS, celulas: [ULTRAPASSAGEM, EVOLUCAO, APOGEO] }

  # APEIRON
  ESCALAMENTO: { dominio: PROPORCAO, pilar: APEIRON, celulas: [AMPLIACAO, REDUCAO, ZOOM] }
  AUREA: { dominio: PROPORCAO, pilar: APEIRON, celulas: [DIVISAO_AUREA, HARMONIA, EQUILIBRIO_PERF] }
  ISOMORFISMO: { dominio: PROPORCAO, pilar: APEIRON, celulas: [CORRESPONDENCIA, ANALOGIA, MAPEAMENTO] }
  FREQUENCIA: { dominio: VIBRATIO, pilar: APEIRON, celulas: [OSCILLACAO, CICLO, PULSAO] }
  RESONANCIA: { dominio: VIBRATIO, pilar: APEIRON, celulas: [AMPLIFICACAO, SINTONIA, ECO] }
  ONDA: { dominio: VIBRATIO, pilar: APEIRON, celulas: [PROPAGACAO, INTERFERENCIA, MODULACAO] }
  POTENCIAL: { dominio: VACUO, pilar: APEIRON, celulas: [CAPACIDADE, LATENCIA, POSSIBILIDADE] }
  SILENCIO: { dominio: VACUO, pilar: APEIRON, celulas: [PAUSA, VAZIO, REFLEXAO] }
  CAMPO: { dominio: VACUO, pilar: APEIRON, celulas: [ESPACO_INFLUENCIA, GRADIENTE, TOPOLOGIA] }

  # MYTHOS
  PADRAO_PRIMORDIAL: { dominio: ARQUETIPO, pilar: MYTHOS, celulas: [ORIGEM, MATRIZ, FONTE] }
  COMPORTAMENTO: { dominio: ARQUETIPO, pilar: MYTHOS, celulas: [ATITUDE, HABITO, RITUAL] }
  SIMBOLO: { dominio: ARQUETIPO, pilar: MYTHOS, celulas: [ICONE, METAFORA, SIGNIFICADO] }
  TEIA: { dominio: NARRATIVA, pilar: MYTHOS, celulas: [REDE, CONEXAO, TRAMA] }
  LINHA_SENTIDO: { dominio: NARRATIVA, pilar: MYTHOS, celulas: [DIRECAO, PROPOSITO, SENTIDO] }
  HISTORIA_VIVIDA: { dominio: NARRATIVA, pilar: MYTHOS, celulas: [MEMORIA, EXPERIENCIA, TESTEMUNHO] }
  INCOMPREENSAO: { dominio: MISTERIO, pilar: MYTHOS, celulas: [DUVIDA, ENIGMA, OBSCURIDADE] }
  INTUICAO: { dominio: MISTERIO, pilar: MYTHOS, celulas: [PRESSENTIMENTO, INSIGHT, REVELACAO] }
  REVELACAO: { dominio: MISTERIO, pilar: MYTHOS, celulas: [DESCUBERTA, ILUMINACAO, VERDADE] }

# =============================================================================
# NÍVEL 4 — CÉLULAS OPERACIONAIS (162 células)
# =============================================================================
# Formato: cada célula possui:
#   - uid: identificador único snake_case (reconciliador de IDs)
#   - path: caminho hierárquico completo
#   - hierarquico_id: ID numérico 1.1.1.1
#   - legado_id: ID legado S1.L1.1.1-A
#   - tipo: natureza ontológica da célula

n4_celulas:
  # ═══ LOGOS / ALGORITMIA ═══
  DECOMPOSICAO:
    uid: "logos_algoritmia_resolucao_decomposicao"
    path: "LOGOS > ALGORITMIA > RESOLUÇÃO > DECOMPOSIÇÃO"
    hierarquico_id: "1.1.1.1"
    legado_id: "S1.L1.1.1-A"
    tipo: processo
    descricao: "Decomposição de problemas complexos em subproblemas"

  SEQUENCIA:
    uid: "logos_algoritmia_resolucao_sequencia"
    path: "LOGOS > ALGORITMIA > RESOLUÇÃO > SEQUÊNCIA"
    hierarquico_id: "1.1.1.2"
    legado_id: "S1.L1.1.2-A"
    tipo: processo
    descricao: "Ordenação e sequenciamento de operações"

  CASO_BASE:
    uid: "logos_algoritmia_resolucao_caso_base"
    path: "LOGOS > ALGORITMIA > RESOLUÇÃO > CASO BASE"
    hierarquico_id: "1.1.1.3"
    legado_id: "S1.L1.1.3-A"
    tipo: estado
    descricao: "Condição terminal de recursão"

  MELHORIA:
    uid: "logos_algoritmia_otimizacao_melhora"
    path: "LOGOS > ALGORITMIA > OTIMIZAÇÃO > MELHORIA"
    hierarquico_id: "1.1.2.1"
    legado_id: "S1.L1.2.1-A"
    tipo: processo
    descricao: "Refinamento iterativo de soluções"

  EFICIENCIA:
    uid: "logos_algoritmia_otimizacao_eficiencia"
    path: "LOGOS > ALGORITMIA > OTIMIZAÇÃO > EFICIÊNCIA"
    hierarquico_id: "1.1.2.2"
    legado_id: "S1.L1.2.2-A"
    tipo: medida
    descricao: "Minimização de recursos e tempo"

  EQUILIBRIO:
    uid: "logos_algoritmia_otimizacao_equilibrio"
    path: "LOGOS > ALGORITMIA > OTIMIZAÇÃO > EQUILÍBRIO"
    hierarquico_id: "1.1.2.3"
    legado_id: "S1.L1.2.3-A"
    tipo: estado
    descricao: "Balanceamento de trade-offs"

  VERIFICACAO:
    uid: "logos_algoritmia_validacao_verificacao"
    path: "LOGOS > ALGORITMIA > VALIDAÇÃO > VERIFICAÇÃO"
    hierarquico_id: "1.1.3.1"
    legado_id: "S1.L1.3.1-A"
    tipo: processo
    descricao: "Conferência de conformidade"

  CORRECAO:
    uid: "logos_algoritmia_validacao_correcao"
    path: "LOGOS > ALGORITMIA > VALIDAÇÃO > CORREÇÃO"
    hierarquico_id: "1.1.3.2"
    legado_id: "S1.L1.3.2-A"
    tipo: processo
    descricao: "Retificação de erros detectados"

  CERTIFICACAO:
    uid: "logos_algoritmia_validacao_certificacao"
    path: "LOGOS > ALGORITMIA > VALIDAÇÃO > CERTIFICAÇÃO"
    hierarquico_id: "1.1.3.3"
    legado_id: "S1.L1.3.3-A"
    tipo: estado
    descricao: "Atestado de conformidade"

  # ═══ LOGOS / NOMOS ═══
  LEI:
    uid: "logos_nomos_legislacao_lei"
    path: "LOGOS > NOMOS > LEGISLAÇÃO > LEI"
    hierarquico_id: "1.2.1.1"
    legado_id: "S1.L2.1.1-A"
    tipo: principio
    descricao: "Regra normativa formal"

  JURISPRUDENCIA:
    uid: "logos_nomos_legislacao_jurisprudencia"
    path: "LOGOS > NOMOS > LEGISLAÇÃO > JURISPRUDÊNCIA"
    hierarquico_id: "1.2.1.2"
    legado_id: "S1.L2.1.2-A"
    tipo: processo
    descricao: "Interpretação e aplicação da lei"

  REGULAMENTO:
    uid: "logos_nomos_legislacao_regulamento"
    path: "LOGOS > NOMOS > LEGISLAÇÃO > REGULAMENTO"
    hierarquico_id: "1.2.1.3"
    legado_id: "S1.L2.1.3-A"
    tipo: mecanismo
    descricao: "Norma regulamentar detalhada"

  FRONTEIRA:
    uid: "logos_nomos_contorno_fronteira"
    path: "LOGOS > NOMOS > CONTORNO > FRONTEIRA"
    hierarquico_id: "1.2.2.1"
    legado_id: "S1.L2.2.1-A"
    tipo: restricao
    descricao: "Limite normativo"

  EXCECAO:
    uid: "logos_nomos_contorno_excecao"
    path: "LOGOS > NOMOS > CONTORNO > EXCEÇÃO"
    hierarquico_id: "1.2.2.2"
    legado_id: "S1.L2.2.2-A"
    tipo: excecao
    descricao: "Desvio autorizado da norma"

  ADAPTACAO:
    uid: "logos_nomos_contorno_adaptacao"
    path: "LOGOS > NOMOS > CONTORNO > ADAPTAÇÃO"
    hierarquico_id: "1.2.2.3"
    legado_id: "S1.L2.2.3-A"
    tipo: dinamica
    descricao: "Ajuste normativo a contextos"

  ACORDO:
    uid: "logos_nomos_pacto_acordo"
    path: "LOGOS > NOMOS > PACTO > ACORDO"
    hierarquico_id: "1.2.3.1"
    legado_id: "S1.L2.3.1-A"
    tipo: processo
    descricao: "Consenso entre partes"

  COMPROMISSO:
    uid: "logos_nomos_pacto_compromisso"
    path: "LOGOS > NOMOS > PACTO > COMPROMISSO"
    hierarquico_id: "1.2.3.2"
    legado_id: "S1.L2.3.2-A"
    tipo: estado
    descricao: "Obrigação assumida"

  RENEGOCIACAO:
    uid: "logos_nomos_pacto_renegociacao"
    path: "LOGOS > NOMOS > PACTO > RENEGOCIAÇÃO"
    hierarquico_id: "1.2.3.3"
    legado_id: "S1.L2.3.3-A"
    tipo: processo
    descricao: "Revisão de termos acordados"

  # ═══ LOGOS / MECÂNICA ═══
  EQUILIBRIO_MEC:
    uid: "logos_mecanica_estatica_equilibrio"
    path: "LOGOS > MECÂNICA > ESTÁTICA > EQUILÍBRIO"
    hierarquico_id: "1.3.1.1"
    legado_id: "S1.L3.1.1-A"
    tipo: estado
    descricao: "Estado de forças balanceadas"

  RESISTENCIA:
    uid: "logos_mecanica_estatica_resistencia"
    path: "LOGOS > MECÂNICA > ESTÁTICA > RESISTÊNCIA"
    hierarquico_id: "1.3.1.2"
    legado_id: "S1.L3.1.2-A"
    tipo: medida
    descricao: "Capacidade de suportar carga"

  RIGIDEZ:
    uid: "logos_mecanica_estatica_rigidez"
    path: "LOGOS > MECÂNICA > ESTÁTICA > RIGIDEZ"
    hierarquico_id: "1.3.1.3"
    legado_id: "S1.L3.1.3-A"
    tipo: propriedade
    descricao: "Resistência à deformação"

  MOVIMENTO:
    uid: "logos_mecanica_dinamica_movimento"
    path: "LOGOS > MECÂNICA > DINÂMICA > MOVIMENTO"
    hierarquico_id: "1.3.2.1"
    legado_id: "S1.L3.2.1-A"
    tipo: processo
    descricao: "Mudança de posição ao longo do tempo"

  FORCA:
    uid: "logos_mecanica_dinamica_forca"
    path: "LOGOS > MECÂNICA > DINÂMICA > FORÇA"
    hierarquico_id: "1.3.2.2"
    legado_id: "S1.L3.2.2-A"
    tipo: vetor
    descricao: "Agente de mudança de movimento"

  ENERGIA:
    uid: "logos_mecanica_dinamica_energia"
    path: "LOGOS > MECÂNICA > DINÂMICA > ENERGIA"
    hierarquico_id: "1.3.2.3"
    legado_id: "S1.L3.2.3-A"
    tipo: medida
    descricao: "Capacidade de realizar trabalho"

  CALOR:
    uid: "logos_mecanica_termotransdinamica_calor"
    path: "LOGOS > MECÂNICA > TERMOTRANSDINÂMICA > CALOR"
    hierarquico_id: "1.3.3.1"
    legado_id: "S1.L3.3.1-A"
    tipo: processo
    descricao: "Transferência de energia térmica"

  ENTROPIA_SIST:
    uid: "logos_mecanica_termotransdinamica_entropia"
    path: "LOGOS > MECÂNICA > TERMOTRANSDINÂMICA > ENTROPIA"
    hierarquico_id: "1.3.3.2"
    legado_id: "S1.L3.3.2-A"
    tipo: medida
    descricao: "Grau de desordem de um sistema"

  IRREVERSIBILIDADE:
    uid: "logos_mecanica_termotransdinamica_irreversibilidade"
    path: "LOGOS > MECÂNICA > TERMOTRANSDINÂMICA > IRREVERSIBILIDADE"
    hierarquico_id: "1.3.3.3"
    legado_id: "S1.L3.3.3-A"
    tipo: restricao
    descricao: "Direção preferencial dos processos"

  # ═══ BIOS / OIKOS ═══
  PROTECAO:
    uid: "bios_oikos_morada_protecao"
    path: "BIOS > OIKOS > MORADA > PROTEÇÃO"
    hierarquico_id: "2.1.1.1"
    legado_id: "S2.L1.1.1-A"
    tipo: processo
    descricao: "Abrigo e segurança do organismo"

  RECURSOS:
    uid: "bios_oikos_morada_recursos"
    path: "BIOS > OIKOS > MORADA > RECURSOS"
    hierarquico_id: "2.1.1.2"
    legado_id: "S2.L1.1.2-A"
    tipo: medida
    descricao: "Insumos necessários à sobrevivência"

  SANEAMENTO:
    uid: "bios_oikos_morada_saneamento"
    path: "BIOS > OIKOS > MORADA > SANEAMENTO"
    hierarquico_id: "2.1.1.3"
    legado_id: "S2.L1.1.3-A"
    tipo: processo
    descricao: "Manutenção do ambiente habitável"

  ESPACO:
    uid: "bios_oikos_territorio_espaco"
    path: "BIOS > OIKOS > TERRITÓRIO > ESPAÇO"
    hierarquico_id: "2.1.2.1"
    legado_id: "S2.L1.2.1-A"
    tipo: medida
    descricao: "Extensão ocupada pelo organismo"

  DELIMITACAO:
    uid: "bios_oikos_territorio_delimitacao"
    path: "BIOS > OIKOS > TERRITÓRIO > DELIMITAÇÃO"
    hierarquico_id: "2.1.2.2"
    legado_id: "S2.L1.2.2-A"
    tipo: processo
    descricao: "Definição de fronteiras territoriais"

  SOBERANIA:
    uid: "bios_oikos_territorio_soberania"
    path: "BIOS > OIKOS > TERRITÓRIO > SOBERANIA"
    hierarquico_id: "2.1.2.3"
    legado_id: "S2.L1.2.3-A"
    tipo: estado
    descricao: "Controle autônomo do território"

  ARMAZENAMENTO:
    uid: "bios_oikos_provisao_armazenamento"
    path: "BIOS > OIKOS > PROVISÃO > ARMAZENAMENTO"
    hierarquico_id: "2.1.3.1"
    legado_id: "S2.L1.3.1-A"
    tipo: processo
    descricao: "Acúmulo de recursos para uso futuro"

  DISTRIBUICAO:
    uid: "bios_oikos_provisao_distribuicao"
    path: "BIOS > OIKOS > PROVISÃO > DISTRIBUIÇÃO"
    hierarquico_id: "2.1.3.2"
    legado_id: "S2.L1.3.2-A"
    tipo: processo
    descricao: "Alocação de recursos entre entidades"

  RACIONALIZACAO:
    uid: "bios_oikos_provisao_racionalizacao"
    path: "BIOS > OIKOS > PROVISÃO > RACIONALIZAÇÃO"
    hierarquico_id: "2.1.3.3"
    legado_id: "S2.L1.3.3-A"
    tipo: processo
    descricao: "Otimização do uso de recursos"

  # ═══ BIOS / SOMA ═══
  COESAO:
    uid: "bios_soma_integridade_coesao"
    path: "BIOS > SOMA > INTEGRIDADE > COESÃO"
    hierarquico_id: "2.2.1.1"
    legado_id: "S2.L2.1.1-A"
    tipo: propriedade
    descricao: "União funcional dos componentes"

  CONSCIENCIA:
    uid: "bios_soma_integridade_consciencia"
    path: "BIOS > SOMA > INTEGRIDADE > CONSCIÊNCIA"
    hierarquico_id: "2.2.1.2"
    legado_id: "S2.L2.1.2-A"
    tipo: estado
    descricao: "Consciência do estado do organismo"

  IDENTIDADE:
    uid: "bios_soma_integridade_identidade"
    path: "BIOS > SOMA > INTEGRIDADE > IDENTIDADE"
    hierarquico_id: "2.2.1.3"
    legado_id: "S2.L2.1.3-A"
    tipo: estado
    descricao: "Auto-reconhecimento ontológico"

  NASCIMENTO:
    uid: "bios_soma_vitalidade_nascimento"
    path: "BIOS > SOMA > VITALIDADE > NASCIMENTO"
    hierarquico_id: "2.2.2.1"
    legado_id: "S2.L2.2.1-A"
    tipo: processo
    descricao: "Início do ciclo de vida"

  CRESCIMENTO:
    uid: "bios_soma_vitalidade_crescimento"
    path: "BIOS > SOMA > VITALIDADE > CRESCIMENTO"
    hierarquico_id: "2.2.2.2"
    legado_id: "S2.L2.2.2-A"
    tipo: processo
    descricao: "Expansão e desenvolvimento"

  RENOVACAO:
    uid: "bios_soma_vitalidade_renovacao"
    path: "BIOS > SOMA > VITALIDADE > RENOVAÇÃO"
    hierarquico_id: "2.2.2.3"
    legado_id: "S2.L2.2.3-A"
    tipo: processo
    descricao: "Restauração funcional"

  REGULACAO:
    uid: "bios_soma_homeostase_regulacao"
    path: "BIOS > SOMA > HOMEOSTASE > REGULAÇÃO"
    hierarquico_id: "2.2.3.1"
    legado_id: "S2.L2.3.1-A"
    tipo: processo
    descricao: "Manutenção de parâmetros internos"

  ADAPTACAO_BIOS:
    uid: "bios_soma_homeostase_adaptacao"
    path: "BIOS > SOMA > HOMEOSTASE > ADAPTAÇÃO"
    hierarquico_id: "2.2.3.2"
    legado_id: "S2.L2.3.2-A"
    tipo: processo
    descricao: "Ajuste a mudanças ambientais"

  EQUILIBRIO_BIOS:
    uid: "bios_soma_homeostase_equilibrio"
    path: "BIOS > SOMA > HOMEOSTASE > EQUILÍBRIO"
    hierarquico_id: "2.2.3.3"
    legado_id: "S2.L2.3.3-A"
    tipo: estado
    descricao: "Estável dinâmico do organismo"

  # ═══ BIOS / METABOLISMO ═══
  CONSTRUCAO:
    uid: "bios_metabolismo_anabolismo_construcao"
    path: "BIOS > METABOLISMO > ANABOLISMO > CONSTRUÇÃO"
    hierarquico_id: "2.3.1.1"
    legado_id: "S2.L3.1.1-A"
    tipo: processo
    descricao: "Síntese de estruturas complexas"

  SINTESSE:
    uid: "bios_metabolismo_anabolismo_sintese"
    path: "BIOS > METABOLISMO > ANABOLISMO > SÍNTESE"
    hierarquico_id: "2.3.1.2"
    legado_id: "S2.L3.1.2-A"
    tipo: processo
    descricao: "Combinação de elementos em novo todo"

  ACUMULACAO:
    uid: "bios_metabolismo_anabolismo_acumulacao"
    path: "BIOS > METABOLISMO > ANABOLISMO > ACUMULAÇÃO"
    hierarquico_id: "2.3.1.3"
    legado_id: "S2.L3.1.3-A"
    tipo: estado
    descricao: "Reserva de materiais"

  DECOMPOSICAO_BIOS:
    uid: "bios_metabolismo_catabolismo_decomposicao"
    path: "BIOS > METABOLISMO > CATABOLISMO > DECOMPOSIÇÃO"
    hierarquico_id: "2.3.2.1"
    legado_id: "S2.L3.2.1-A"
    tipo: processo
    descricao: "Quebra de estruturas complexas"

  LIBERACAO:
    uid: "bios_metabolismo_catabolismo_liberacao"
    path: "BIOS > METABOLISMO > CATABOLISMO > LIBERAÇÃO"
    hierarquico_id: "2.3.2.2"
    legado_id: "S2.L3.2.2-A"
    tipo: processo
    descricao: "Disponibilização de energia"

  DESCARTE:
    uid: "bios_metabolismo_catabolismo_descarte"
    path: "BIOS > METABOLISMO > CATABOLISMO > DESCARTE"
    hierarquico_id: "2.3.2.3"
    legado_id: "S2.L3.2.3-A"
    tipo: processo
    descricao: "Eliminação de resíduos"

  REPETICAO:
    uid: "bios_metabolismo_ciclo_repeticao"
    path: "BIOS > METABOLISMO > CICLO > REPETIÇÃO"
    hierarquico_id: "2.3.3.1"
    legado_id: "S2.L3.3.1-A"
    tipo: dinamica
    descricao: "Reiteração de processos metabólicos"

  REGENERACAO:
    uid: "bios_metabolismo_ciclo_regeneracao"
    path: "BIOS > METABOLISMO > CICLO > REGENERAÇÃO"
    hierarquico_id: "2.3.3.2"
    legado_id: "S2.L3.3.2-A"
    tipo: processo
    descricao: "Restauração completa do ciclo"

  CIRCULARIDADE:
    uid: "bios_metabolismo_ciclo_circularidade"
    path: "BIOS > METABOLISMO > CICLO > CIRCULARIDADE"
    hierarquico_id: "2.3.3.3"
    legado_id: "S2.L3.3.3-A"
    tipo: propriedade
    descricao: "Fechamento do loop metabólico"

  # ═══ PATHOS / ETHOS ═══
  ALINHAMENTO:
    uid: "pathos_ethos_valores_alinhamento"
    path: "PATHOS > ETHOS > VALORES > ALINHAMENTO"
    hierarquico_id: "3.1.1.1"
    legado_id: "S3.L1.1.1-A"
    tipo: estado
    descricao: "Coerência entre valores declarados e ações"

  CONFLITO:
    uid: "pathos_ethos_valores_conflito"
    path: "PATHOS > ETHOS > VALORES > CONFLITO"
    hierarquico_id: "3.1.1.2"
    legado_id: "S3.L1.1.2-A"
    tipo: fenomeno
    descricao: "Dissonância entre valores concorrentes"

  TRANSPARENCIA:
    uid: "pathos_ethos_valores_transparencia"
    path: "PATHOS > ETHOS > VALORES > TRANSPARÊNCIA"
    hierarquico_id: "3.1.1.3"
    legado_id: "S3.L1.1.3-A"
    tipo: processo
    descricao: "Visibilidade das motivações"

  HABITO:
    uid: "pathos_ethos_virtude_habito"
    path: "PATHOS > ETHOS > VIRTUDE > HÁBITO"
    hierarquico_id: "3.1.2.1"
    legado_id: "S3.L1.2.1-A"
    tipo: processo
    descricao: "Comportamento cristalizadoizado"

  DISCERNIMENTO:
    uid: "pathos_ethos_virtude_discernimento"
    path: "PATHOS > ETHOS > VIRTUDE > DISCERNIMENTO"
    hierarquico_id: "3.1.2.2"
    legado_id: "S3.L1.2.2-A"
    tipo: processo
    descricao: "Capacidade de julgamento ético"

  EXCELENCIA:
    uid: "pathos_ethos_virtude_excelencia"
    path: "PATHOS > ETHOS > VIRTUDE > EXCELÊNCIA"
    hierarquico_id: "3.1.2.3"
    legado_id: "S3.L1.2.3-A"
    tipo: estado
    descricao: "Realização máxima da virtude"

  DEVER:
    uid: "pathos_ethos_responsabilidade_dever"
    path: "PATHOS > ETHOS > RESPONSABILIDADE > DEVER"
    hierarquico_id: "3.1.3.1"
    legado_id: "S3.L1.3.1-A"
    tipo: restricao
    descricao: "Obrigação moral"

  PRESTACAO_CONTAS:
    uid: "pathos_ethos_responsabilidade_prestacao_contas"
    path: "PATHOS > ETHOS > RESPONSABILIDADE > PRESTAÇÃO DE CONTAS"
    hierarquico_id: "3.1.3.2"
    legado_id: "S3.L1.3.2-A"
    tipo: processo
    descricao: "Demonstrar cumprimento de deveres"

  REPARACAO:
    uid: "pathos_ethos_responsabilidade_reparacao"
    path: "PATHOS > ETHOS > RESPONSABILIDADE > REPARAÇÃO"
    hierarquico_id: "3.1.3.3"
    legado_id: "S3.L1.3.3-A"
    tipo: processo
    descricao: "Compensação por danos causados"

  # ═══ PATHOS / ALTERIDADE ═══
  IDENTIDADE:
    uid: "pathos_alteridade_reconhecimento_identidade"
    path: "PATHOS > ALTERIDADE > RECONHECIMENTO > IDENTIDADE"
    hierarquico_id: "3.2.1.1"
    legado_id: "S3.L2.1.1-A"
    tipo: estado
    descricao: "Autoconceito e reconhecimento pelo outro"

  VALIDACAO:
    uid: "pathos_alteridade_reconhecimento_validacao"
    path: "PATHOS > ALTERIDADE > RECONHECIMENTO > VALIDAÇÃO"
    hierarquico_id: "3.2.1.2"
    legado_id: "S3.L2.1.2-A"
    tipo: processo
    descricao: "Confirmação da existência e valor"

  MEMORIA:
    uid: "pathos_alteridade_reconhecimento_memoria"
    path: "PATHOS > ALTERIDADE > RECONHECIMENTO > MEMÓRIA"
    hierarquico_id: "3.2.1.3"
    legado_id: "S3.L2.1.3-A"
    tipo: processo
    descricao: "Registro e evocação de experiências"

  COMPREENSAO:
    uid: "pathos_alteridade_empatia_compreensao"
    path: "PATHOS > ALTERIDADE > EMPATIA > COMPREENSÃO"
    hierarquico_id: "3.2.2.1"
    legado_id: "S3.L2.2.1-A"
    tipo: processo
    descricao: "Captação do estado emocional alheio"

  SENSIBILIZACAO:
    uid: "pathos_alteridade_empatia_sensibilizacao"
    path: "PATHOS > ALTERIDADE > EMPATIA > SENSIBILIZAÇÃO"
    hierarquico_id: "3.2.2.2"
    legado_id: "S3.L2.2.2-A"
    tipo: processo
    descricao: "Abertura à experiência do outro"

  CONEXAO:
    uid: "pathos_alteridade_empatia_conexao"
    path: "PATHOS > ALTERIDADE > EMPATIA > CONEXÃO"
    hierarquico_id: "3.2.2.3"
    legado_id: "S3.L2.2.3-A"
    tipo: fenomeno
    descricao: "Vínculo emocional entre entidades"

  COMUNICACAO:
    uid: "pathos_alteridade_dialogo_comunicacao"
    path: "PATHOS > ALTERIDADE > DIÁLOGO > COMUNICAÇÃO"
    hierarquico_id: "3.2.3.1"
    legado_id: "S3.L2.3.1-A"
    tipo: processo
    descricao: "Troca de informações entre agentes"

  NEGOCIACAO:
    uid: "pathos_alteridade_dialogo_negociacao"
    path: "PATHOS > ALTERIDADE > DIÁLOGO > NEGOCIAÇÃO"
    hierarquico_id: "3.2.3.2"
    legado_id: "S3.L2.3.2-A"
    tipo: processo
    descricao: "Busca de acordo mútuo"

  CONCILIACAO:
    uid: "pathos_alteridade_dialogo_conciliacao"
    path: "PATHOS > ALTERIDADE > DIÁLOGO > CONCILIAÇÃO"
    hierarquico_id: "3.2.3.3"
    legado_id: "S3.L2.3.3-A"
    tipo: processo
    descricao: "Resolução de divergências"

  # ═══ PATHOS / ESTÉTICA ═══
  PROPORCAO:
    uid: "pathos_estetica_harmonia_proporcao"
    path: "PATHOS > ESTÉTICA > HARMONIA > PROPORÇÃO"
    hierarquico_id: "3.3.1.1"
    legado_id: "S3.L3.1.1-A"
    tipo: medida
    descricao: "Relação harmônica entre elementos"

  RITMO:
    uid: "pathos_estetica_harmonia_ritmo"
    path: "PATHOS > ESTÉTICA > HARMONIA > RITMO"
    hierarquico_id: "3.3.1.2"
    legado_id: "S3.L3.1.2-A"
    tipo: dinamica
    descricao: "Padrão temporal recorrente"

  UNIDADE:
    uid: "pathos_estetica_harmonia_unidade"
    path: "PATHOS > ESTÉTICA > HARMONIA > UNIDADE"
    hierarquico_id: "3.3.1.3"
    legado_id: "S3.L3.1.3-A"
    tipo: estado
    descricao: "Coerência do todo percebido"

  CRIACAO:
    uid: "pathos_estetica_expressao_criacao"
    path: "PATHOS > ESTÉTICA > EXPRESSÃO > CRIAÇÃO"
    hierarquico_id: "3.3.2.1"
    legado_id: "S3.L3.2.1-A"
    tipo: processo
    descricao: "Geração de forma nova"

  ARTICULACAO:
    uid: "pathos_estetica_expressao_articulacao"
    path: "PATHOS > ESTÉTICA > EXPRESSÃO > ARTICULAÇÃO"
    hierarquico_id: "3.3.2.2"
    legado_id: "S3.L3.2.2-A"
    tipo: processo
    descricao: "Organização de elementos expressivos"

  ESTILO:
    uid: "pathos_estetica_expressao_estilo"
    path: "PATHOS > ESTÉTICA > EXPRESSÃO > ESTILO"
    hierarquico_id: "3.3.2.3"
    legado_id: "S3.L3.2.3-A"
    tipo: propriedade
    descricao: "Maneira característica de expressão"

  INFLUENCIA:
    uid: "pathos_estetica_impacto_influencia"
    path: "PATHOS > ESTÉTICA > IMPACTO > INFLUÊNCIA"
    hierarquico_id: "3.3.3.1"
    legado_id: "S3.L3.3.1-A"
    tipo: fenomeno
    descricao: "Efeito sobre agentes receptores"

  TRANSFORMACAO_EST:
    uid: "pathos_estetica_impacto_transformacao"
    path: "PATHOS > ESTÉTICA > IMPACTO > TRANSFORMAÇÃO"
    hierarquico_id: "3.3.3.2"
    legado_id: "S3.L3.3.2-A"
    tipo: processo
    descricao: "Mudança profunda provocada pela experiência"

  LEGADO:
    uid: "pathos_estetica_impacto_legado"
    path: "PATHOS > ESTÉTICA > IMPACTO > LEGADO"
    hierarquico_id: "3.3.3.3"
    legado_id: "S3.L3.3.3-A"
    tipo: estado
    descricao: "Marca duradoura na cultura"

  # ═══ KHAOS / ENTROPIA ═══
  EROSAO:
    uid: "khaus_entropia_degradacao_erosao"
    path: "KHAOS > ENTROPIA > DEGRADAÇÃO > EROSÃO"
    hierarquico_id: "4.1.1.1"
    legado_id: "S4.L1.1.1-A"
    tipo: processo
    descricao: "Desgaste gradual de estrutura"

  CORRUPCAO:
    uid: "khaus_entropia_degradacao_corrupcao"
    path: "KHAOS > ENTROPIA > DEGRADAÇÃO > CORRUPÇÃO"
    hierarquico_id: "4.1.1.2"
    legado_id: "S4.L1.1.2-A"
    tipo: fenomeno
    descricao: "Contaminação sistêmica"

  DISSOLUCAO:
    uid: "khaus_entropia_degradacao_dissolucao"
    path: "KHAOS > ENTROPIA > DEGRADAÇÃO > DISSOLUÇÃO"
    hierarquico_id: "4.1.1.3"
    legado_id: "S4.L1.1.3-A"
    tipo: processo
    descricao: "Desintegração completa"

  DISPERSSAO:
    uid: "khaus_entropia_dissipacao_disperssao"
    path: "KHAOS > ENTROPIA > DISSIPAÇÃO > DISPERSSÃO"
    hierarquico_id: "4.1.2.1"
    legado_id: "S4.L1.2.1-A"
    tipo: processo
    descricao: "Distribuição aleatória de energia"

  VAZAMENTO:
    uid: "khaus_entropia_dissipacao_vazamento"
    path: "KHAOS > ENTROPIA > DISSIPAÇÃO > VAZAMENTO"
    hierarquico_id: "4.1.2.2"
    legado_id: "S4.L1.2.2-A"
    tipo: fenomeno
    descricao: "Perda não controlada de recursos"

  EVAPORACAO:
    uid: "khaus_entropia_dissipacao_evaporacao"
    path: "KHAOS > ENTROPIA > DISSIPAÇÃO > EVAPORAÇÃO"
    hierarquico_id: "4.1.2.3"
    legado_id: "S4.L1.2.3-A"
    tipo: processo
    descricao: "Transição de fase para dispersão"

  DESORDENACAO:
    uid: "khaus_entropia_caos_desordem"
    path: "KHAOS > ENTROPIA > CAOS > DESORDENAÇÃO"
    hierarquico_id: "4.1.3.1"
    legado_id: "S4.L1.3.1-A"
    tipo: estado
    descricao: "Ausência de estrutura previsível"

  ALEATORIEDADE:
    uid: "khaus_entropia_caos_aleatoriedade"
    path: "KHAOS > ENTROPIA > CAOS > ALEATORIEDADE"
    hierarquico_id: "4.1.3.2"
    legado_id: "S4.L1.3.2-A"
    tipo: fenomeno
    descricao: "Comportamento não determinístico"

  CRISE:
    uid: "khaus_entropia_caos_crise"
    path: "KHAOS > ENTROPIA > CAOS > CRISE"
    hierarquico_id: "4.1.3.3"
    legado_id: "S4.L1.3.3-A"
    tipo: fenomeno
    descricao: "Ponto de ruptura sistêmica"

  # ═══ KHAOS / SINGULARIDADE ═══
  ANOMALIA:
    uid: "khaus_singularidade_excecao_anomalia"
    path: "KHAOS > SINGULARIDADE > EXCEÇÃO > ANOMALIA"
    hierarquico_id: "4.2.1.1"
    legado_id: "S4.L2.1.1-A"
    tipo: fenomeno
    descricao: "Desvio do padrão esperado"

  DESVIACAO:
    uid: "khaus_singularidade_excecao_desviacao"
    path: "KHAOS > SINGULARIDADE > EXCEÇÃO > DESVIACAÇÃO"
    hierarquico_id: "4.2.1.2"
    legado_id: "S4.L2.1.2-A"
    tipo: medida
    descricao: "Distância em relação à norma"

  INOVACAO:
    uid: "khaus_singularidade_excecao_inovacao"
    path: "KHAOS > SINGULARIDADE > EXCEÇÃO > INOVAÇÃO"
    hierarquico_id: "4.2.1.3"
    legado_id: "S4.L2.1.3-A"
    tipo: processo
    descricao: "Criação de novo paradigma"

  ILIMITADO:
    uid: "khaus_singularidade_infinito_ilimitado"
    path: "KHAOS > SINGULARIDADE > INFINITO > ILIMITADO"
    hierarquico_id: "4.2.2.1"
    legado_id: "S4.L2.2.1-A"
    tipo: conceito
    descricao: "Sem fronteiras quantitativas"

  INFINITESIMO:
    uid: "khaus_singularidade_infinito_infinitesimo"
    path: "KHAOS > SINGULARIDADE > INFINITO > INFINITÉSIMO"
    hierarquico_id: "4.2.2.2"
    legado_id: "S4.L2.2.2-A"
    tipo: conceito
    descricao: "Quantidade abaixo de qualquer limiar"

  PARADOXO:
    uid: "khaus_singularidade_infinito_paradoxo"
    path: "KHAOS > SINGULARIDADE > INFINITO > PARADOXO"
    hierarquico_id: "4.2.2.3"
    legado_id: "S4.L2.2.3-A"
    tipo: fenomeno
    descricao: "Contradição aparente irredutível"

  METAMORFOSE:
    uid: "khaus_singularidade_transformacao_metamorfose"
    path: "KHAOS > SINGULARIDADE > TRANSFORMAÇÃO > METAMORFOSE"
    hierarquico_id: "4.2.3.1"
    legado_id: "S4.L2.3.1-A"
    tipo: processo
    descricao: "Mudança radical de forma"

  TRANSPOSICAO:
    uid: "khaus_singularidade_transformacao_transposicao"
    path: "KHAOS > SINGULARIDADE > TRANSFORMAÇÃO > TRANSPOSIÇÃO"
    hierarquico_id: "4.2.3.2"
    legado_id: "S4.L2.3.2-A"
    tipo: processo
    descricao: "Reorganização de elementos"

  RECONVERSAO:
    uid: "khaus_singularidade_transformacao_reconversao"
    path: "KHAOS > SINGULARIDADE > TRANSFORMAÇÃO > RECONVERSÃO"
    hierarquico_id: "4.2.3.3"
    legado_id: "S4.L2.3.3-A"
    tipo: processo
    descricao: "Retorno a estado anterior transformado"

  # ═══ KHAOS / SÍNTESE ═══
  MISTURA:
    uid: "khaus_sintese_fusao_mistura"
    path: "KHAOS > SÍNTESE > FUSÃO > MISTURA"
    hierarquico_id: "4.3.1.1"
    legado_id: "S4.L3.1.1-A"
    tipo: processo
    descricao: "Combinação de elementos distintos"

  CONVERGENCIA:
    uid: "khaus_sintese_fusao_convergencia"
    path: "KHAOS > SÍNTESE > FUSÃO > CONVERGÊNCIA"
    hierarquico_id: "4.3.1.2"
    legado_id: "S4.L3.1.2-A"
    tipo: processo
    descricao: "Aproximação de múltiplas tendências"

  AMALGAMACAO:
    uid: "khaus_sintese_fusao_amalgamacao"
    path: "KHAOS > SÍNTESE > FUSÃO > AMALGAMAÇÃO"
    hierarquico_id: "4.3.1.3"
    legado_id: "S4.L3.1.3-A"
    tipo: fenomeno
    descricao: "Fusão em entidade única e indissociável"

  MISCEGENIA:
    uid: "khaus_sintese_hibridismo_miscegenia"
    path: "KHAOS > SÍNTESE > HIBRIDISMO > MISCEGÊNIA"
    hierarquico_id: "4.3.2.1"
    legado_id: "S4.L3.2.1-A"
    tipo: fenomeno
    descricao: "Mistura de origens distintas"

  SINCRETISMO:
    uid: "khaus_sintese_hibridismo_sincretismo"
    path: "KHAOS > SÍNTESE > HIBRIDISMO > SINCRETISMO"
    hierarquico_id: "4.3.2.2"
    legado_id: "S4.L3.2.2-A"
    tipo: fenomeno
    descricao: "Fusão de tradições em novo sistema"

  NOVO:
    uid: "khaus_sintese_hibridismo_novo"
    path: "KHAOS > SÍNTESE > HIBRIDISMO > NOVO"
    hierarquico_id: "4.3.2.3"
    legado_id: "S4.L3.2.3-A"
    tipo: fenomeno
    descricao: "Entidade emergente sem precedente"

  ULTRAPASSAGEM:
    uid: "khaus_sintese_transcendencia_ultrapassagem"
    path: "KHAOS > SÍNTESE > TRANSCENDÊNCIA > ULTRAPASSAGEM"
    hierarquico_id: "4.3.3.1"
    legado_id: "S4.L3.3.1-A"
    tipo: processo
    descricao: "Ir além dos limites atuais"

  EVOLUCAO:
    uid: "khaus_sintese_transcendencia_evolucao"
    path: "KHAOS > SÍNTESE > TRANSCENDÊNCIA > EVOLUÇÃO"
    hierarquico_id: "4.3.3.2"
    legado_id: "S4.L3.3.2-A"
    tipo: dinamica
    descricao: "Progressão qualitativa ao longo do tempo"

  APOGEO:
    uid: "khaus_sintese_transcendencia_apogeo"
    path: "KHAOS > SÍNTESE > TRANSCENDÊNCIA > APOGEO"
    hierarquico_id: "4.3.3.3"
    legado_id: "S4.L3.3.3-A"
    tipo: estado
    descricao: "Ponto máximo de desenvolvimento"

  # ═══ APEIRON / PROPORÇÃO ═══
  AMPLIACAO:
    uid: "apeiron_proporcao_escalamento_ampliacao"
    path: "APEIRON > PROPORÇÃO > ESCALAMENTO > AMPLIAÇÃO"
    hierarquico_id: "5.1.1.1"
    legado_id: "S5.L1.1.1-A"
    tipo: processo
    descricao: "Aumento de escala"

  REDUCAO:
    uid: "apeiron_proporcao_escalamento_reducao"
    path: "APEIRON > PROPORÇÃO > ESCALAMENTO > REDUÇÃO"
    hierarquico_id: "5.1.1.2"
    legado_id: "S5.L1.1.2-A"
    tipo: processo
    descricao: "Diminuição de escala"

  ZOOM:
    uid: "apeiron_proporcao_escalamento_zoom"
    path: "APEIRON > PROPORÇÃO > ESCALAMENTO > ZOOM"
    hierarquico_id: "5.1.1.3"
    legado_id: "S5.L1.1.3-A"
    tipo: processo
    descricao: "Mudança focal de perspectiva"

  DIVISAO_AUREA:
    uid: "apeiron_proporcao_aurea_divisao_aurea"
    path: "APEIRON > PROPORÇÃO > ÁUREA > DIVISÃO ÁUREA"
    hierarquico_id: "5.1.2.1"
    legado_id: "S5.L1.2.1-A"
    tipo: conceito
    descricao: "Proporção φ = (1+√5)/2"

  HARMONIA_AUREA:
    uid: "apeiron_proporcao_aurea_harmonia"
    path: "APEIRON > PROPORÇÃO > ÁUREA > HARMONIA"
    hierarquico_id: "5.1.2.2"
    legado_id: "S5.L1.2.2-A"
    tipo: estado
    descricao: "Equilíbrio estético perfeito"

  EQUILIBRIO_PERF:
    uid: "apeiron_proporcao_aurea_equilibrio"
    path: "APEIRON > PROPORÇÃO > ÁUREA > EQUILÍBRIO_PERFEITO"
    hierarquico_id: "5.1.2.3"
    legado_id: "S5.L1.2.3-A"
    tipo: estado
    descricao: "Balanceamento ideal"

  CORRESPONDENCIA:
    uid: "apeiron_proporcao_isomorfismo_correspondencia"
    path: "APEIRON > PROPORÇÃO > ISOMORFISMO > CORRESPONDÊNCIA"
    hierarquico_id: "5.1.3.1"
    legado_id: "S5.L1.3.1-A"
    tipo: relacao
    descricao: "Mapeamento biunívoco entre estruturas"

  ANALOGIA:
    uid: "apeiron_proporcao_isomorfismo_analogia"
    path: "APEIRON > PROPORÇÃO > ISOMORFISMO > ANALOGIA"
    hierarquico_id: "5.1.3.2"
    legado_id: "S5.L1.3.2-A"
    tipo: relacao
    descricao: "Semelhança estrutural entre domínios"

  MAPEAMENTO:
    uid: "apeiron_proporcao_isomorfismo_mapeamento"
    path: "APEIRON > PROPORÇÃO > ISOMORFISMO > MAPEAMENTO"
    hierarquico_id: "5.1.3.3"
    legado_id: "S5.L1.3.3-A"
    tipo: processo
    descricao: "Representação sistemática de correspondências"

  # ═══ APEIRON / VIBRATIO ═══
  OSCILLACAO:
    uid: "apeiron_vibratio_frequencia_oscillacao"
    path: "APEIRON > VIBRATIO > FREQUÊNCIA > OSCILAÇÃO"
    hierarquico_id: "5.2.1.1"
    legado_id: "S5.L2.1.1-A"
    tipo: dinamica
    descricao: "Movimento periódico"

  CICLO_FREQ:
    uid: "apeiron_vibratio_frequencia_ciclo"
    path: "APEIRON > VIBRATIO > FREQUÊNCIA > CICLO"
    hierarquico_id: "5.2.1.2"
    legado_id: "S5.L2.1.2-A"
    tipo: dinamica
    descricao: "Sequência periódica completa"

  PULSAO:
    uid: "apeiron_vibratio_frequencia_pulsao"
    path: "APEIRON > VIBRATIO > FREQUÊNCIA > PULSAÇÃO"
    hierarquico_id: "5.2.1.3"
    legado_id: "S5.L2.1.3-A"
    tipo: dinamica
    descricao: "Batimento rítmico"

  AMPLIFICACAO:
    uid: "apeiron_vibratio_resonancia_amplificacao"
    path: "APEIRON > VIBRATIO > RESSONÂNCIA > AMPLIFICAÇÃO"
    hierarquico_id: "5.2.2.1"
    legado_id: "S5.L2.2.1-A"
    tipo: processo
    descricao: "Intensificação por coincidência de frequência"

  SINTONIA:
    uid: "apeiron_vibratio_resonancia_sintonia"
    path: "APEIRON > VIBRATIO > RESSONÂNCIA > SINTONIA"
    hierarquico_id: "5.2.2.2"
    legado_id: "S5.L2.2.2-A"
    tipo: estado
    descricao: "Alinhamento frequencial"

  ECO:
    uid: "apeiron_vibratio_resonancia_eco"
    path: "APEIRON > VIBRATIO > RESSONÂNCIA > ECO"
    hierarquico_id: "5.2.2.3"
    legado_id: "S5.L2.2.3-A"
    tipo: fenomeno
    descricao: "Reflexão de padrão"

  PROPAGACAO:
    uid: "apeiron_vibratio_onda_propagacao"
    path: "APEIRON > VIBRATIO > ONDA > PROPAGAÇÃO"
    hierarquico_id: "5.2.3.1"
    legado_id: "S5.L2.3.1-A"
    tipo: processo
    descricao: "Transmissão de perturbação"

  INTERFERENCIA:
    uid: "apeiron_vibratio_onda_interferencia"
    path: "APEIRON > VIBRATIO > ONDA > INTERFERÊNCIA"
    hierarquico_id: "5.2.3.2"
    legado_id: "S5.L2.3.2-A"
    tipo: fenomeno
    descricao: "Combinação de ondas"

  MODULACAO:
    uid: "apeiron_vibratio_onda_modulacao"
    path: "APEIRON > VIBRATIO > ONDA > MODULAÇÃO"
    hierarquico_id: "5.2.3.3"
    legado_id: "S5.L2.3.3-A"
    tipo: processo
    descricao: "Alteração controlada de parâmetros"

  # ═══ APEIRON / VÁCUO ═══
  CAPACIDADE:
    uid: "apeiron_vacuo_potencial_capacidade"
    path: "APEIRON > VÁCUO > POTENCIAL > CAPACIDADE"
    hierarquico_id: "5.3.1.1"
    legado_id: "S5.L3.1.1-A"
    tipo: medida
    descricao: "Possibilidade latente de manifestação"

  LATENCIA:
    uid: "apeiron_vacuo_potencial_latencia"
    path: "APEIRON > VÁCUO > POTENCIAL > LATÊNCIA"
    hierarquico_id: "5.3.1.2"
    legado_id: "S5.L3.1.2-A"
    tipo: estado
    descricao: "Estado de possibilidade não ativada"

  POSSIBILIDADE:
    uid: "apeiron_vacuo_potencial_possibilidade"
    path: "APEIRON > VÁCUO > POTENCIAL > POSSIBILIDADE"
    hierarquico_id: "5.3.1.3"
    legado_id: "S5.L3.1.3-A"
    tipo: conceito
    descricao: "Espaço do que pode vir a ser"

  PAUSA:
    uid: "apeiron_vacuo_silencio_pausa"
    path: "APEIRON > VÁCUO > SILÊNCIO > PAUSA"
    hierarquico_id: "5.3.2.1"
    legado_id: "S5.L3.2.1-A"
    tipo: processo
    descricao: "Interrupção intencional"

  VAZIO:
    uid: "apeiron_vacuo_silencio_vazio"
    path: "APEIRON > VÁCUO > SILÊNCIO > VAZIO"
    hierarquico_id: "5.3.2.2"
    legado_id: "S5.L3.2.2-A"
    tipo: conceito
    descricao: "Ausência como espaço gerador"

  REFLEXAO:
    uid: "apeiron_vacuo_silencio_reflexao"
    path: "APEIRON > VÁCUO > SILÊNCIO > REFLEXÃO"
    hierarquico_id: "5.3.2.3"
    legado_id: "S5.L3.2.3-A"
    tipo: processo
    descricao: "Contemplação interna"

  ESPACO_INFLUENCIA:
    uid: "apeiron_vacuo_campo_espaco_influencia"
    path: "APEIRON > VÁCUO > CAMPO > ESPAÇO DE INFLUÊNCIA"
    hierarquico_id: "5.3.3.1"
    legado_id: "S5.L3.3.1-A"
    tipo: medida
    descricao: "Região de atuação"

  GRADIENTE:
    uid: "apeiron_vacuo_campo_gradiente"
    path: "APEIRON > VÁCUO > CAMPO > GRADIENTE"
    hierarquico_id: "5.3.3.2"
    legado_id: "S5.L3.3.2-A"
    tipo: medida
    descricao: "Variação espacial de intensidade"

  TOPOLOGIA:
    uid: "apeiron_vacuo_campo_topologia"
    path: "APEIRON > VÁCUO > CAMPO > TOPOLOGIA"
    hierarquico_id: "5.3.3.3"
    legado_id: "S5.L3.3.3-A"
    tipo: estrutura
    descricao: "Propriedades espaciais do campo"

  # ═══ MYTHOS / ARQUÉTIPO ═══
  ORIGEM:
    uid: "mythos_arquetipo_padrao_primordial_origem"
    path: "MYTHOS > ARQUÉTIPO > PADRÃO PRIMORDIAL > ORIGEM"
    hierarquico_id: "6.1.1.1"
    legado_id: "S6.L1.1.1-A"
    tipo: conceito
    descricao: "Ponto de começo primordial"

  MATRIZ:
    uid: "mythos_arquetipo_padrao_primordial_matriz"
    path: "MYTHOS > ARQUÉTIPO > PADRÃO PRIMORDIAL > MATRIZ"
    hierarquico_id: "6.1.1.2"
    legado_id: "S6.L1.1.2-A"
    tipo: estrutura
    descricao: "Padrão gerador fundamental"

  FONTE:
    uid: "mythos_arquetipo_padrao_primordial_fonte"
    path: "MYTHOS > ARQUÉTIPO > PADRÃO PRIMORDIAL > FONTE"
    hierarquico_id: "6.1.1.3"
    legado_id: "S6.L1.1.3-A"
    tipo: conceito
    descricao: "Origem última e inesgotável"

  ATITUDE:
    uid: "mythos_arquetipo_comportamento_atitude"
    path: "MYTHOS > ARQUÉTIPO > COMPORTAMENTO > ATITUDE"
    hierarquico_id: "6.1.2.1"
    legado_id: "S6.L1.2.1-A"
    tipo: processo
    descricao: "Disposição recorrente de agir"

  HABITO_MYTH:
    uid: "mythos_arquetipo_comportamento_habito"
    path: "MYTHOS > ARQUÉTIPO > COMPORTAMENTO > HÁBITO"
    hierarquico_id: "6.1.2.2"
    legado_id: "S6.L1.2.2-A"
    tipo: processo
    descricao: "Repetição cristalizada"

  RITUAL:
    uid: "mythos_arquetipo_comportamento_ritual"
    path: "MYTHOS > ARQUÉTIPO > COMPORTAMENTO > RITUAL"
    hierarquico_id: "6.1.2.3"
    legado_id: "S6.L1.2.3-A"
    tipo: processo
    descricao: "Sequência cerimonial carregada de sentido"

  ICONE:
    uid: "mythos_arquetipo_simbolo_icone"
    path: "MYTHOS > ARQUÉTIPO > SÍMBOLO > ÍCONE"
    hierarquico_id: "6.1.3.1"
    legado_id: "S6.L1.3.1-A"
    tipo: representacao
    descricao: "Representação condensada de significado"

  METAFORA:
    uid: "mythos_arquetipo_simbolo_metafora"
    path: "MYTHOS > ARQUÉTIPO > SÍMBOLO > METÁFORA"
    hierarquico_id: "6.1.3.2"
    legado_id: "S6.L1.3.2-A"
    tipo: relacao
    descricao: "Transferência de sentido entre domínios"

  SIGNIFICADO:
    uid: "mythos_arquetipo_simbolo_significado"
    path: "MYTHOS > ARQUÉTIPO > SÍMBOLO > SIGNIFICADO"
    hierarquico_id: "6.1.3.3"
    legado_id: "S6.L1.3.3-A"
    tipo: conceito
    descricao: "Conteúdo semântico profundo"

  # ═══ MYTHOS / NARRATIVA ═══
  REDE:
    uid: "mythos_narrativa_teia_rede"
    path: "MYTHOS > NARRATIVA > TEIA > REDE"
    hierarquico_id: "6.2.1.1"
    legado_id: "S6.L2.1.1-A"
    tipo: estrutura
    descricao: "Conjunto de conexões"

  CONEXAO_MYTH:
    uid: "mythos_narrativa_teia_conexao"
    path: "MYTHOS > NARRATIVA > TEIA > CONEXÃO"
    hierarquico_id: "6.2.1.2"
    legado_id: "S6.L2.1.2-A"
    tipo: relacao
    descricao: "Vínculo entre elementos"

  TRAMA:
    uid: "mythos_narrativa_teia_trama"
    path: "MYTHOS > NARRATIVA > TEIA > TRAMA"
    hierarquico_id: "6.2.1.3"
    legado_id: "S6.L2.1.3-A"
    tipo: estrutura
    descricao: "Enredo estruturado"

  DIRECAO:
    uid: "mythos_narrativa_linha_sentido_direcao"
    path: "MYTHOS > NARRATIVA > LINHA DE SENTIDO > DIREÇÃO"
    hierarquico_id: "6.2.2.1"
    legado_id: "S6.L2.2.1-A"
    tipo: vetor
    descricao: "Orientação narrativa"

  PROPOSITO:
    uid: "mythos_narrativa_linha_sentido_proposito"
    path: "MYTHOS > NARRATIVA > LINHA DE SENTIDO > PROPÓSITO"
    hierarquico_id: "6.2.2.2"
    legado_id: "S6.L2.2.2-A"
    tipo: conceito
    descricao: "Razão de ser da narrativa"

  SENTIDO:
    uid: "mythos_narrativa_linha_sentido_sentido"
    path: "MYTHOS > NARRATIVA > LINHA DE SENTIDO > SENTIDO"
    hierarquico_id: "6.2.2.3"
    legado_id: "S6.L2.2.3-A"
    tipo: conceito
    descricao: "Significado construído"

  MEMORIA_MYTH:
    uid: "mythos_narrativa_historia_vivida_memoria"
    path: "MYTHOS > NARRATIVA > HISTÓRIA VIVIDA > MEMÓRIA"
    hierarquico_id: "6.2.3.1"
    legado_id: "S6.L2.3.1-A"
    tipo: processo
    descricao: "Registro experiencial"

  EXPERIENCIA:
    uid: "mythos_narrativa_historia_vivida_experiencia"
    path: "MYTHOS > NARRATIVA > HISTÓRIA VIVIDA > EXPERIÊNCIA"
    hierarquico_id: "6.2.3.2"
    legado_id: "S6.L2.3.2-A"
    tipo: processo
    descricao: "Vivencia codificada"

  TESTEMUNHO:
    uid: "mythos_narrativa_historia_vivida_testemunho"
    path: "MYTHOS > NARRATIVA > HISTÓRIA VIVIDA > TESTEMUNHO"
    hierarquico_id: "6.2.3.3"
    legado_id: "S6.L2.3.3-A"
    tipo: representacao
    descricao: "Relato de experiência"

  # ═══ MYTHOS / MISTÉRIO ═══
  DUVIDA:
    uid: "mythos_misterio_incompreensao_duvida"
    path: "MYTHOS > MISTÉRIO > INCOMPREENSÃO > DÚVIDA"
    hierarquico_id: "6.3.1.1"
    legado_id: "S6.L3.1.1-A"
    tipo: estado
    descricao: "Ausência de certeza"

  ENIGMA:
    uid: "mythos_misterio_incompreensao_enigma"
    path: "MYTHOS > MISTÉRIO > INCOMPREENSÃO > ENIGMA"
    hierarquico_id: "6.3.1.2"
    legado_id: "S6.L3.1.2-A"
    tipo: fenomeno
    descricao: "Problema sem solução aparente"

  OBSCURIDADE:
    uid: "mythos_misterio_incompreensao_obscuridade"
    path: "MYTHOS > MISTÉRIO > INCOMPREENSÃO > OBSCURIDADE"
    hierarquico_id: "6.3.1.3"
    legado_id: "S6.L3.1.3-A"
    tipo: estado
    descricao: "Falta de iluminação conceitual"

  PRESSENTIMENTO:
    uid: "mythos_misterio_intuicao_pressentimento"
    path: "MYTHOS > MISTÉRIO > INTUIÇÃO > PRESSENTIMENTO"
    hierarquico_id: "6.3.2.1"
    legado_id: "S6.L3.2.1-A"
    tipo: fenomeno
    descricao: "Conhecimento sem via racional"

  INSIGHT:
    uid: "mythos_misterio_intuicao_insight"
    path: "MYTHOS > MISTÉRIO > INTUIÇÃO > INSIGHT"
    hierarquico_id: "6.3.2.2"
    legado_id: "S6.L3.2.2-A"
    tipo: fenomeno
    descricao: "Compreensão súbita"

  REVELACAO:
    uid: "mythos_misterio_intuicao_revelacao"
    path: "MYTHOS > MISTÉRIO > INTUIÇÃO > REVELAÇÃO"
    hierarquico_id: "6.3.2.3"
    legado_id: "S6.L3.2.3-A"
    tipo: fenomeno
    descricao: "Desvelamento de verdade oculta"

  DESCOBERTA:
    uid: "mythos_misterio_revelacao_descoberta"
    path: "MYTHOS > MISTÉRIO > REVELAÇÃO > DESCOBERTA"
    hierarquico_id: "6.3.3.1"
    legado_id: "S6.L3.3.1-A"
    tipo: processo
    descricao: "Encontro com o desconhecido"

  ILUMINACAO:
    uid: "mythos_misterio_revelacao_iluminacao"
    path: "MYTHOS > MISTÉRIO > REVELAÇÃO > ILUMINAÇÃO"
    hierarquico_id: "6.3.3.2"
    legado_id: "S6.L3.3.2-A"
    tipo: estado
    descricao: "Estado de compreensão total"

  VERDADE:
    uid: "mythos_misterio_revelacao_verdade"
    path: "MYTHOS > MISTÉRIO > REVELAÇÃO > VERDADE"
    hierarquico_id: "6.3.3.3"
    legado_id: "S6.L3.3.3-A"
    tipo: conceito
    descricao: "Correspondência plena com o real"

# =============================================================================
# RECONCILIAÇÃO DE IDs — Mapeamento dual
# =============================================================================
id_reconciliation:
  strategy: "uid_immutable"
  description: >
    Cada célula possui um uid canônico (snake_case), um ID hierárquico
    (1.1.1.1) e um ID legado (S1.L1.1.1-A). O uid é a chave primária
    imutável. Os demais IDs são derivados e podem ser recalculados.
  format:
    uid: "{pilar}_{dominio}_{subarvore}_{celula}"
    hierarquico: "{n1}.{n2}.{n3}.{n4}"
    legado: "S{n1}.L{n2}.{n3}.{n4}-{pilar[0]}"

# =============================================================================
# NATUREZAS ONTOLÓGICAS (10 tipos)
# =============================================================================
naturezas:
  - processo
  - estado
  - fenomeno
  - principio
  - mecanismo
  - estrutura
  - arquetipo
  - dinamica
  - restricao
  - vetor
  - conceito
  - medida
  - relacao
  - representacao
  - excecao

# =============================================================================
# TIPOS DE RELAÇÃO
# =============================================================================
relacoes:
  - tipo: "hierarquico"
    descricao: "Pai-filho na árvore N0→N4"
  - tipo: "lateral"
    descricao: "Células no mesmo nível N4"
  - tipo: "transversal"
    descricao: "Células em pilares diferentes, mesmo domínio"
  - tipo: "espelhamento"
    descricao: "SINTRÓPICO ↔ ENTRÓPICO"
  - tipo: "causal"
    descricao: "Uma célula influencia outra"
  - tipo: "contraste"
    descricao: "Células opostas ou complementares"

# =============================================================================
# VETORES SEMÂNTICOS (para embedding)
# =============================================================================
vetores_semanticos:
  - nome: "estrutural"
    peso: 0.30
    descricao: "Foco em hierarquia e composição"
  - nome: "funcional"
    peso: 0.25
    descricao: "Foco em processos e operações"
  - nome: "relacional"
    peso: 0.20
    descricao: "Foco em conexões entre entidades"
  - nome: "simbolico"
    peso: 0.15
    descricao: "Foco em significado e narrativa"
  - nome: "temporal"
    peso: 0.10
    descricao: "Foco em sequência e duração"

# =============================================================================
# CONFIGURAÇÕES DE RETRIEVAL
# =============================================================================
retrieval:
  metodo_default: "hibrido"
  estrategias:
    - nome: "vector_similarity"
      peso: 0.50
      descricao: "Similaridade cosseno nos embeddings"
    - nome: "graph_traversal"
      peso: 0.30
      descricao: "Navegação pelo grafo ontológico"
    - nome: "symbolic_match"
      peso: 0.20
      descricao: "Correspondência exata de metadados"
  reranking:
    ativo: true
    metodo: "cross-encoder"
    top_k_rerank: 10
  cache:
    ativo: true
    ttl_segundos: 3600
    max_itens: 10000
"""

ont_path = os.path.join(BASE, "config/ontology.yaml")
with open(ont_path, "w", encoding="utf-8") as f:
    f.write(ontology_content)
print(f"  [FILE] config/ontology.yaml ({len(ontology_content)} bytes)")


# ============================================================
# 4. config/embedding.yaml
# ============================================================

embedding_content = """# =============================================================================
# CONFIGURAÇÃO DE EMBEDDINGS — Geração e gestão de vetores semânticos
# =============================================================================

modelo:
  nome: "all-MiniLM-L6-v2"
  provedor: "sentence-transformers"
  tipo: "dense"
  dimensao: 384
  normalizacao: true  # L2 normalization nos vetores
  quantizacao: "float16"  # Redução de precisão para memória

# Pesos dos vetores semânticos para retrieval híbrido
vetores_pesos:
  estrutural: 0.30
  funcional: 0.25
  relacional: 0.20
  simbolico: 0.15
  temporal: 0.10

# Configuração de geração de embeddings
geracao:
  batch_size: 64
  max_seq_length: 512
  truncate: true
  device: "auto"  # "cpu", "cuda", "auto"
  workers: 4
  cache_dir: "./data/embeddings/cache"

# Índice vetorial (FAISS)
indice:
  tipo: "IVFFlat"  # Inverted File Index
  metrica: "cosine"
  nlist: 100  # Número de clusters para IVF
  nprobe: 10  # Clusters a buscar em query
  dimensao: 384
  path: "./data/embeddings/indice.faiss"

# Armazenamento
armazenamento:
  formato: "parquet"
  path: "./data/embeddings/"
  prefixo_arquivo: "emb_n4_"
  compressao: "snappy"

# Cache de embeddings já computados
cache:
  ativo: true
  path: "./data/embeddings/cache/"
  estrategia: "LRU"
  max_tamanho_mb: 2048
  ttl_segundos: 86400  # 24 horas

# Embeddings por contexto
contextos:
  - nome: "descricao"
    campo: "descricao"
    peso: 1.0
  - nome: "path"
    campo: "path"
    peso: 0.5
  - nome: "tipo"
    campo: "tipo"
    peso: 0.3
  - nome: "relacoes"
    campo: "relacoes"
    peso: 0.7
"""

emb_path = os.path.join(BASE, "config/embedding.yaml")
with open(emb_path, "w", encoding="utf-8") as f:
    f.write(embedding_content)
print(f"  [FILE] config/embedding.yaml ({len(embedding_content)} bytes)")


# ============================================================
# 5. config/retrieval.yaml
# ============================================================

retrieval_content = """# =============================================================================
# CONFIGURAÇÃO DE RETRIEVAL HÍBRIDO — Thresholds e Limites
# =============================================================================

# Método de retrieval padrão
metodo_default: "hibrido"

# =============================================================================
# RETRIEVAL VETORIAL (Similaridade Semântica)
# =============================================================================
vetorial:
  modelo: "all-MiniLM-L6-v2"
  metrica: "cosine"
  limiar_minimo: 0.65          # Similaridade mínima para inclusão
  limiar_alta_confianca: 0.85  # Acima disso, resultado direto
  top_k: 20                    # Número máximo de candidatos
  expandir_query: true         # Expandir query com sinônimos ontológicos
  expansao_max: 5              # Máximo de termos adicionais

# =============================================================================
# RETRIEVAL GRÁFICO (Navegação na Ontologia)
# =============================================================================
grafico:
  tipo: "caminho_ponderado"
  profundidade_max: 3           # Saltos máximos no grafo
  limiar_proximidade: 0.5       # Score mínimo de proximidade ontológica
  considerar_lateral: true      # Saltos laterais (mesmo nível)
  considerar_transversal: true  # Saltos entre pilares
  peso_hierarquico: 0.7         # Peso para proximidade hierárquica
  peso_lateral: 0.3             # Peso para conexões laterais
  max_caminhos: 50              # Máximo de caminhos explorados

# =============================================================================
# RETRIEVAL SIMBÓLICO (Correspondência Exata)
# =============================================================================
simbolico:
  ativo: true
  campos: ["uid", "hierarquico_id", "legado_id", "tipo", "pilar", "dominio"]
  correspondencia_exata: true
  correspondencia_parcial: 0.8   # Limiar para match parcial (fuzzy)
  max_resultados: 50

# =============================================================================
# FUSÃO DE RESULTADOS (Hybrid Fusion)
# =============================================================================
fusao:
  estrategia: "weighted_sum"    # "weighted_sum", "rrf", "condorcet"
  pesos:
    vetorial: 0.50
    grafico: 0.30
    simbolico: 0.20
  normalizar_scores: true       # Normalizar scores antes da fusão
  deduplicacao: true            # Remover duplicatas
  limiar_final: 0.40            # Score mínimo após fusão

# =============================================================================
# RERANKING (Reordenação Final)
# =============================================================================
reranking:
  ativo: true
  metodo: "cross-encoder"       # "cross-encoder", "cohere-rerank", "none"
  modelo: "cross-encoder/ms-marco-MiniLM-L-6-v2"
  top_k_entrada: 50             # Quantos candidatos para reranking
  top_k_saida: 10               # Quantos resultados finais
  limiar_rerank: 0.50           # Score mínimo do reranker

# =============================================================================
# CACHE DE RETRIEVAL
# =============================================================================
cache:
  ativo: true
  tipo: "redis"                 # "memory", "redis", "disk"
  ttl_segundos: 3600            # 1 hora
  max_itens: 50000
  redis_config:
    host: "localhost"
    porta: 6379
    db: 0
    senha: null                 # Definir em variável de ambiente

# =============================================================================
# MONITORAMENTO
# =============================================================================
monitoramento:
  log_queries: true
  log_resultados: false         # Pode gerar volume excessivo
  metricas:
    - latencia_p50
    - latencia_p95
    - latencia_p99
    - taxa_acerto_top1
    - taxa_acerto_top5
    - cobertura_ontologica
  alertas:
    latencia_max_ms: 500
    taxa_acerto_minima: 0.70
"""

ret_path = os.path.join(BASE, "config/retrieval.yaml")
with open(ret_path, "w", encoding="utf-8") as f:
    f.write(retrieval_content)
print(f"  [FILE] config/retrieval.yaml ({len(retrieval_content)} bytes)")


# ============================================================
# 6. config/graph.yaml
# ============================================================

graph_content = """# =============================================================================
# CONFIGURAÇÃO DO GRAFO ONTOLÓGICO — NetworkX
# =============================================================================

grafo:
  # Motor de grafo
  engine: "networkx"
  tipo: "MultiDiGraph"  # Direcionado, multigrafo (múltiplas arestas entre nós)
  dirigido: true
  
  # Persistência
  persistencia:
    formato: "gexf"           # "gexf", "graphml", "json", "pickle"
    path: "./data/graphs/"
    arquivo_principal: "ontologia_master.gexf"
    arquivo_snapshot: "ontologia_snapshot_{timestamp}.gexf"
    auto_salvar: true
    intervalo_segundos: 300    # Salvar a cada 5 minutos
    manter_snapshots: 10       # Número de snapshots a reter
    compressao: true
  
  # Características do grafo
  nos:
    total_estimado: 162        # Células N4 + nós intermediários
    atributos_padrao:
      - uid
      - tipo
      - pilar
      - dominio
      - subarvore
      - vetor
      - hierarquico_id
      - legado_id
      - descricao
      - embedding_ref       # Referência ao arquivo de embedding
  
  # Arestas (relações)
  arestas:
    tipos:
      - nome: "hierarquico"
        dirigido: true
        peso_default: 1.0
        descricao: "Relação pai-filho na ontologia"
      - nome: "lateral"
        dirigido: false
        peso_default: 0.5
        descricao: "Células no mesmo nível"
      - nome: "transversal"
        dirigido: false
        peso_default: 0.3
        descricao: "Conexão entre pilares"
      - nome: "espelhamento"
        dirigido: false
        peso_default: 0.2
        descricao: "Mapeamento SINTRÓPICO ↔ ENTRÓPICO"
      - nome: "causal"
        dirigido: true
        peso_default: 0.7
        descricao: "Influência causal"
      - nome: "contraste"
        dirigido: false
        peso_default: 0.4
        descricao: "Oposição ou complementaridade"
    
    max_arestas_por_no: 20
  
  # Algoritmos e métricas
  algoritmos:
    centralidade:
      - tipo: "betweenness"
        descricao: "Intermediação"
        calcular: true
      - tipo: "degree"
        descricao: "Grau de conectividade"
        calcular: true
      - tipo: "closeness"
        descricao: "Proximidade"
        calcular: true
      - tipo: "eigenvector"
        descricao: "Autovetor"
        calcular: true
      - tipo: "pagerank"
        descricao: "PageRank adaptado"
        calcular: true
        damping: 0.85
    
    clustering:
      - tipo: "coeficiente"
        descricao: "Coeficiente de agrupamento"
        calcular: true
      - tipo: "comunidades"
        descricao: "Detecção de comunidades (Louvain)"
        calcular: true
        resolucao: 1.0
    
    caminho:
      - tipo: "menor_caminho"
        descricao: "Shortest path entre células"
        calcular: true
      - tipo: "diametro"
        descricao: "Diâmetro do grafo"
        calcular: true
      - tipo: "densidade"
        descricao: "Densidade de conexões"
        calcular: true
  
  # Visualização
  visualizacao:
    ativo: true
    engine: "matplotlib"       # "matplotlib", "pyvis", "graphviz"
    layout: "spring"           # "spring", "kamada_kawai", "spectral", "shell"
    cor_por_pilar: true
    tamanho_por_centralidade: true
    labels: true
    output_format: "png"
    resolucao: [1920, 1080]
    path: "./data/graphs/visualizacoes/"
  
  # Índices auxiliares
  indices:
    path: "./data/indexes/"
    tipos:
      - nome: "uid_index"
        tipo: "hash"
        campo: "uid"
        unico: true
      - nome: "hierarquico_index"
        tipo: "btree"
        campo: "hierarquico_id"
        unico: true
      - nome: "pilar_index"
        tipo: "inverted"
        campo: "pilar"
        unico: false
      - nome: "tipo_index"
        tipo: "inverted"
        campo: "tipo"
        unico: false
      - nome: "vetor_index"
        tipo: "hnsw"
        campo: "embedding"
        metrica: "cosine"
        ef_construction: 200
        M: 16
"""

graph_path = os.path.join(BASE, "config/graph.yaml")
with open(graph_path, "w", encoding="utf-8") as f:
    f.write(graph_content)
print(f"  [FILE] config/graph.yaml ({len(graph_content)} bytes)")


# ============================================================
# 7. PROMPT TEMPLATES
# ============================================================

# Classifier template
classifier_template = """# Template de Prompt — Classificador Ontológico
# Determina a classificação N0→N4 de um input textual

sistema: >
  Você é um classificador ontológico especializado na taxonomia fractal MestreCuca.
  Sua função é receber um input textual e determinar sua posição na hierarquia N0→N4,
  considerando os 6 pilares (LOGOS, BIOS, PATHOS, KHAOS, APEIRON, MYTHOS),
  2 vetores (SINTRÓPICO, ENTRÓPICO) e 162 células N4.

entrada:
  texto: "{{input_text}}"
  contexto: "{{optional_context}}"

instrucoes:
  1. Analise o input para determinar o vetor predominante (SINTRÓPICO ou ENTRÓPICO)
  2. Identifique o pilar central (LOGOS, BIOS, PATHOS, KHAOS, APEIRON, MYTHOS)
  3. Determine o domínio N2 aplicável
  4. Selecione a subárvore N3 mais precisa
  5. Atribua a célula N4 operacional
  6. Forneça a confiança da classificação (0.0 a 1.0)
  7. Justifique cada decisão de classificação

formato_saida:
  vetor: "{SINTRÓPICO|ENTRÓPICO}"
  pilar: "{LOGOS|BIOS|PATHOS|KHAOS|APEIRON|MYTHOS}"
  dominio: "{nome do domínio N2}"
  subarvore: "{nome da subárvore N3}"
  celula: "{nome da célula N4}"
  uid: "{uid canônico}"
  hierarquico_id: "{N1.N2.N3.N4}"
  confianca: "{float 0.0-1.0}"
  justificativa: "{explicação detalhada}"
  alternativas:
    - segunda_melhor: "{uid}"
    - terceira_melhor: "{uid}"
"""

# Retrieval template
retrieval_template = """# Template de Prompt — Retrieval Ontológico
# Recupera células relevantes da ontologia para uma query

sistema: >
  Você é um módulo de retrieval especializado na ontologia MestreCuca.
  Utilize busca vetorial, navegação em grafo e correspondência simbólica
  para recuperar as células mais relevantes.

entrada:
  query: "{{input_query}}"
  top_k: {{num_results}}
  estrategia: "hibrido"

instrucoes:
  1. Gere embedding da query usando all-MiniLM-L6-v2
  2. Busque similaridade vetorial (limiar ≥ 0.65)
  3. Navegue o grafo ontológico a partir dos nós recuperados
  4. Aplique correspondência simbólica nos metadados
  5. Reordene resultados via cross-encoder
  6. Aplique deduplicação e retorne top-K final

formato_saida:
  resultados:
    - uid: "{uid}"
      score: "{float}"
      estrategia_origem: "{vetorial|grafico|simbolico}"
      caminho: "{path completo na ontologia}"
      snippet: "{trecho relevante}"
  metadados:
    total_candidatos: "{int}"
    tempo_busca_ms: "{int}"
    estrategia_vencedora: "{vetorial|grafico|simbolico}"
"""

# Synthesis template
synthesis_template = """# Template de Prompt — Síntese Ontológica
# Gera uma resposta sintética a partir de células recuperadas

sistema: >
  Você é um módulo de síntese da ontologia MestreCuca.
  Sua função é combinar informações de múltiplas células N4
  em uma resposta coerente e contextualizada.

entrada:
  celulas_recuperadas:
    {% for cell in retrieved_cells %}
    - uid: "{{cell.uid}}"
      descricao: "{{cell.descricao}}"
      tipo: "{{cell.tipo}}"
      score: {{cell.score}}
    {% endfor %}
  query_original: "{{original_query}}"
  contexto: "{{optional_context}}"

instrucoes:
  1. Identifique padrões e temas comuns entre as células
  2. Respeite a hierarquia ontológica na síntese
  3. Gere uma resposta que integre as perspectivas múltiplas
  4. Mantenha coerência com o DNA ontológico (axiomas de vetor, crenças de pilar)
  5. Indique nível de confiança e possíveis lacunas

formato_saida:
  sintese: "{resposta integrada}"
  nivel_confianca: "{float 0.0-1.0}"
  celulas_utilizadas: ["{uid1}", "{uid2}", ...]
  lacunas_identificadas: ["{área sem cobertura suficiente}"]
  rastreabilidade:
    - uid: "{uid}"
      contribuicao: "{descrição da contribuição}"
"""

# Validation template
validation_template = """# Template de Prompt — Validação Ontológica
# Valida a consistência e completude de classificações

sistema: >
  Você é um módulo de validação da ontologia MestreCuca.
  Verifica consistência interna, completude e conformidade
  com as regras do DNA ontológico.

entrada:
  classificacao:
    vetor: "{{vetor}}"
    pilar: "{{pilar}}"
    dominio: "{{dominio}}"
    subarvore: "{{subarvore}}"
    celula: "{{celula}}"
    uid: "{{uid}}"
  contexto: "{{optional_context}}"

instrucoes:
  1. Verifique se o vetor é compatível com o pilar escolhido
  2. Confirme se o domínio pertence ao pilar correto
  3. Valide se a subárvore existe no domínio indicado
  4. Confirme se a célula pertence à subárvore correta
  5. Verifique consistência do uid com a hierarquia
  6. Identifique violações de DNA ontológico
  7. Sugira correções se houver inconsistências

formato_saida:
  valido: "{true|false}"
  erros:
    - tipo: "{incompatibilidade_vetor_pilar|dominio_invalido|...}"
      descricao: "{detalhes}"
      sugestao: "{correção sugerida}"
  warnings:
    - tipo: "{ambiguidade|fronteira|...}"
      descricao: "{detalhes}"
  score_consistencia: "{float 0.0-1.0}"
"""

# Routing template
routing_template = """# Template de Prompt — Roteamento de Pipeline
# Determina qual pipeline de processamento usar para um input

sistema: >
  Você é um módulo de roteamento inteligente da ontologia MestreCuca.
  Determina o pipeline ideal para processar cada input baseado
  em complexidade, domínio e requisitos de resposta.

entrada:
  input: "{{user_input}}"
  contexto: "{{session_context}}"
  requisitos:
    - "{{latencia_baixa|precisao_alta|explicacao_detalhada|...}}"

instrucoes:
  1. Analise a complexidade do input (simples, moderado, complexo)
  2. Determine o domínio ontológico predominante
  3. Avalie os requisitos de qualidade vs. latência
  4. Selecione o pipeline mais adequado:
     - "fast": Classificação direta, sem reranking
     - "standard": Classificação + retrieval + síntese
     - "deep": Retrieval multi-estratégia + reranking + síntese completa
     - "expert": Validação cruzada + múltiplas perspectivas
  5. Defina parâmetros de execução

formato_saida:
  pipeline: "{fast|standard|deep|expert}"
  etapas:
    - etapa: "{classificacao|retrieval|sintese|validacao}"
      parametros:
        chave: valor
  estimativa_latencia_ms: "{int}"
  nivel_confianca_roteamento: "{float 0.0-1.0}"
"""

# Write all prompt templates
prompt_files = {
    "prompts/classifier/template_classificacao.yaml": classifier_template,
    "prompts/retrieval/template_retrieval.yaml": retrieval_template,
    "prompts/synthesis/template_sintese.yaml": synthesis_template,
    "prompts/validation/template_validacao.yaml": validation_template,
    "prompts/routing/template_routing.yaml": routing_template,
}

for fpath, content in prompt_files.items():
    full = os.path.join(BASE, fpath)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [FILE] {fpath}")


# ============================================================
# 8. .kilo/ CONFIGURAÇÕES
# ============================================================

# Agents config
agents_content = """# =============================================================================
# CONFIGURAÇÃO DE AGENTES — .kilo/agents
# =============================================================================

agentes:
  classificador:
    nome: "OntoClassifier"
    papel: "Classificação ontológica N0→N4"
    modelo_base: "gpt-4o"
    temperatura: 0.2
    template: "prompts/classifier/template_classificacao.yaml"
    max_tokens: 2048
    timeout_segundos: 30
    retry:
      max_tentativas: 3
      backoff_ms: 1000
    rate_limit:
      requests_por_minuto: 60
      tokens_por_minuto: 100000

  retriever:
    nome: "OntoRetriever"
    papel: "Retrieval híbrido ontológico"
    modelo_base: "gpt-4o"
    temperatura: 0.0
    template: "prompts/retrieval/template_retrieval.yaml"
    config_retrieval: "config/retrieval.yaml"
    embedding_modelo: "all-MiniLM-L6-v2"
    top_k_default: 20
    timeout_segundos: 45
    retry:
      max_tentativas: 3
      backoff_ms: 1000

  sintetizador:
    nome: "OntoSynthesizer"
    papel: "Síntese de múltiplas fontes ontológicas"
    modelo_base: "gpt-4o"
    temperatura: 0.4
    template: "prompts/synthesis/template_sintese.yaml"
    max_tokens: 4096
    timeout_segundos: 60
    retry:
      max_tentativas: 3
      backoff_ms: 1000

  validador:
    nome: "OntoValidator"
    papel: "Validação de consistência ontológica"
    modelo_base: "gpt-4o"
    temperatura: 0.0
    template: "prompts/validation/template_validacao.yaml"
    max_tokens: 2048
    timeout_segundos: 30
    retry:
      max_tentativas: 3
      backoff_ms: 1000

  roteador:
    nome: "OntoRouter"
    papel: "Roteamento inteligente de pipelines"
    modelo_base: "gpt-4o-mini"
    temperatura: 0.3
    template: "prompts/routing/template_routing.yaml"
    max_tokens: 1024
    timeout_segundos: 15
    retry:
      max_tentativas: 3
      backoff_ms: 500
"""

agents_path = os.path.join(BASE, ".kilo/agents/agents.yaml")
with open(agents_path, "w", encoding="utf-8") as f:
    f.write(agents_content)
print(f"  [FILE] .kilo/agents/agents.yaml")

# Memory config
memory_content = """# =============================================================================
# CONFIGURAÇÃO DE MEMÓRIA — .kilo/memory
# =============================================================================

memoria:
  # Memória de curto prazo (sessão)
  curto_prazo:
    tipo: "volatile"
    capacidade_max: 500          # Número de itens
    ttl_segundos: 1800           # 30 minutos
    estrategia_eviccao: "lru"
    persistir_ao_salvar: false
  
  # Memória de trabalho (contexto ativo)
  trabalho:
    tipo: "managed"
    capacidade_max: 200
    ttl_segundos: 3600           # 1 hora
    estrategia_eviccao: "priority"
    persistir_ao_salvar: true
    path: "./data/json/sessions/"
  
  # Memória de longo prazo
  longo_prazo:
    tipo: "persistent"
    backend: "sqlite"            # "sqlite", "postgresql", "redis"
    path: "./data/json/memory.db"
    capacidade_max: 100000
    ttl_segundos: null            # Sem expiração
    estrategia_eviccao: "relevance"
    indexacao:
      ativo: true
      campos: ["uid", "pilar", "dominio", "texto", "timestamp"]
      tipo_indice: "fulltext"
      path: "./data/indexes/memory/"
  
  # Cache de embeddings
  embedding_cache:
    tipo: "lru"
    capacidade_max: 50000
    ttl_segundos: 86400           # 24 horas
    path: "./data/embeddings/cache/"
    estrategia: "similaridade"
  
  # Cache de retrieval
  retrieval_cache:
    tipo: "ttl"
    ttl_segundos: 3600            # 1 hora
    max_itens: 50000
    redis_config:
      host: "localhost"
      porta: 6379
      db: 1
  
  # Serialização
  serializacao:
    formato: "json"
    encoding: "utf-8"
    compactar: true
    schema_version: "3.0.0"
"""

memory_path = os.path.join(BASE, ".kilo/memory/memory.yaml")
with open(memory_path, "w", encoding="utf-8") as f:
    f.write(memory_content)
print(f"  [FILE] .kilo/memory/memory.yaml")

# Orchestrators config
orchestrators_content = """# =============================================================================
# CONFIGURAÇÃO DE ORQUESTRADORES — .kilo/orchestrators
# =============================================================================

orquestradores:
  # Pipeline principal
  principal:
    nome: "MainPipeline"
    descricao: "Pipeline padrão para processamento cognitivo"
    etapas:
      - nome: "roteamento"
        agente: "roteador"
        obrigatorio: true
        timeout_segundos: 15
      - nome: "classificacao"
        agente: "classificador"
        obrigatorio: true
        timeout_segundos: 30
      - nome: "retrieval"
        agente: "retriever"
        obrigatorio: true
        timeout_segundos: 45
      - nome: "sintese"
        agente: "sintetizador"
        obrigatorio: true
        timeout_segundos: 60
      - nome: "validacao"
        agente: "validador"
        obrigatorio: false
        timeout_segundos: 30
    
    politica_falha:
      estrategia: "fallback_cascata"
      max_tentativas: 3
      fallback_para: "basico"
      notificar: true
    
    retry:
      ativo: true
      max_tentativas: 3
      backoff_inicial_ms: 500
      backoff_maximo_ms: 5000
      fator_multiplicacao: 2.0
  
  # Pipeline básico (fallback)
  basico:
    nome: "BasicPipeline"
    descricao: "Pipeline simplificado para fallback"
    etapas:
      - nome: "classificacao"
        agente: "classificador"
        obrigatorio: true
        timeout_segundos: 30
      - nome: "retrieval"
        agente: "retriever"
        obrigatorio: true
        timeout_segundos: 45
      - nome: "sintese"
        agente: "sintetizador"
        obrigatorio: true
        timeout_segundos: 60
    
    politica_falha:
      estrategia: "resposta_direta"
      max_tentativas: 1
      notificar: false
  
  # Pipeline de alta precisão
  precisao:
    nome: "HighPrecisionPipeline"
    descricao: "Pipeline com validação cruzada e múltiplas perspectivas"
    etapas:
      - nome: "roteamento"
        agente: "roteador"
        obrigatorio: true
        timeout_segundos: 15
      - nome: "classificacao_multi"
        agente: "classificador"
        obrigatorio: true
        timeout_segundos: 30
        config:
          multi_classificacao: true
          top_n: 3
      - nome: "retrieval_profundo"
        agente: "retriever"
        obrigatorio: true
        timeout_segundos: 60
        config:
          top_k: 50
          estrategia: "deep"
          reranking: true
      - nome: "sintese_multi"
        agente: "sintetizador"
        obrigatorio: true
        timeout_segundos: 90
        config:
          multi_perspectiva: true
          num_perspectivas: 3
      - nome: "validacao_cruzada"
        agente: "validador"
        obrigatorio: true
        timeout_segundos: 45
        config:
          validacao_cruzada: true
          consistencia_ontologica: true
  
    politica_falha:
      estrategia: "fallback_cascata"
      max_tentativas: 2
      fallback_para: "principal"
      notificar: true

# Seleção automática de pipeline
selecao:
  estrategia: "adaptativa"
  criterios:
    - condicao: "complexidade == 'simples' AND latencia_maxima < 1000"
      pipeline: "basico"
    - condicao: "complexidade == 'moderado'"
      pipeline: "principal"
    - condicao: "complexidade == 'complexo' OR requisito == 'precisao_alta'"
      pipeline: "precisao"
    - condicao: "true"  # Default
      pipeline: "principal"
"""

orch_path = os.path.join(BASE, ".kilo/orchestrators/orchestrators.yaml")
with open(orch_path, "w", encoding="utf-8") as f:
    f.write(orchestrators_content)
print(f"  [FILE] .kilo/orchestrators/orchestrators.yaml")

# Kilo prompt configs
kilo_prompts = {
    ".kilo/prompts/classifier/prompts_classifier.yaml": """# Configuração de Prompts — Classificador
prompts:
  classificacao_primaria:
    template: "prompts/classifier/template_classificacao.yaml"
    parametros:
      temperatura: 0.2
      max_tokens: 2048
      top_p: 0.95
    cache: true
    ttl: 3600

  classificacao_secundaria:
    template: "prompts/classifier/template_classificacao.yaml"
    parametros:
      temperatura: 0.5
      max_tokens: 1024
      top_p: 0.90
    cache: false

  validacao_cruzada:
    template: "prompts/validation/template_validacao.yaml"
    parametros:
      temperatura: 0.0
      max_tokens: 1024
""",

    ".kilo/prompts/retrieval/prompts_retrieval.yaml": """# Configuração de Prompts — Retrieval
prompts:
  busca_vetorial:
    estrategia: "dense"
    modelo: "all-MiniLM-L6-v2"
    limiar: 0.65
    top_k: 20
    expandir_query: true

  busca_grafica:
    estrategia: "graph_traversal"
    profundidade_max: 3
    limiar_proximidade: 0.5
    max_caminhos: 50

  busca_simbolica:
    estrategia: "exact_match"
    campos: ["uid", "hierarquico_id", "pilar", "dominio"]
    fuzzy_limiar: 0.8

  fusao_resultados:
    estrategia: "weighted_sum"
    pesos:
      vetorial: 0.50
      grafico: 0.30
      simbolico: 0.20
    reranking: true
    top_k_final: 10
""",

    ".kilo/prompts/synthesis/prompts_synthesis.yaml": """# Configuração de Prompts — Síntese
prompts:
  sintese_padrao:
    template: "prompts/synthesis/template_sintese.yaml"
    parametros:
      temperatura: 0.4
      max_tokens: 4096
      top_p: 0.95
    merge_strategy: "weighted_context"

  sintese_multi_perspectiva:
    template: "prompts/synthesis/template_sintese.yaml"
    parametros:
      temperatura: 0.5
      max_tokens: 4096
      top_p: 0.90
    num_perspectivas: 3
    merge_strategy: "consensus"

  sintese_rapida:
    template: "prompts/synthesis/template_sintese.yaml"
    parametros:
      temperatura: 0.3
      max_tokens: 2048
      top_p: 0.90
    merge_strategy: "first_match"
""",

    ".kilo/prompts/validation/prompts_validacao.yaml": """# Configuração de Prompts — Validação
prompts:
  validacao_classificacao:
    template: "prompts/validation/template_validacao.yaml"
    parametros:
      temperatura: 0.0
      max_tokens: 2048
    regras:
      - verificar_compatibilidade_vetor_pilar
      - verificar_existencia_dominio
      - verificar_existencia_subarvore
      - verificar_existencia_celula
      - verificar_consistencia_uid

  validacao_consistencia:
    parametros:
      temperatura: 0.0
      max_tokens: 1024
    regras:
      - verificar_integridade_grafo
      - verificar_ciclos
      - verificar_orfanatos
      - verificar_cobertura_n4

  qualidade_geral:
    criterios:
      - nome: "precisao_ontologica"
        peso: 0.30
        descricao: "Corretude da classificação"
      - nome: "coerencia_resposta"
        peso: 0.25
        descricao: "Coerência interna da resposta"
      - nome: "cobertura_fontes"
        peso: 0.20
        descricao: "Amplitude das fontes consultadas"
      - nome: "fidelidade_dna"
        peso: 0.15
        descricao: "Respeito ao DNA ontológico"
      - nome: "utilidade_pratica"
        peso: 0.10
        descricao: "Aplicabilidade da resposta"
""",

    ".kilo/prompts/routing/prompts_routing.yaml": """# Configuração de Prompts — Roteamento
prompts:
  roteamento_padrao:
    template: "prompts/routing/template_routing.yaml"
    parametros:
      temperatura: 0.3
      max_tokens: 1024
    pipelines_disponiveis:
      - basico
      - principal
      - precisao

  roteamento_adaptativo:
    template: "prompts/routing/template_routing.yaml"
    parametros:
      temperatura: 0.2
      max_tokens: 512
    estrategia: "contextual"
    fatores:
      - complexidade_input
      - historico_sessao
      - requisitos_usuario
      - carga_sistema
"""
}

for fpath, content in kilo_prompts.items():
    full = os.path.join(BASE, fpath)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [FILE] {fpath}")


# ============================================================
# 9. PLACEHOLDERS ADICIONAIS
# ============================================================

# runtime/runtime.yaml
runtime_content = """# =============================================================================
# CONFIGURAÇÃO DO RUNTIME — Motor de Execução
# =============================================================================

runtime:
  versao: "3.0.0"
  modo: "async"  # "sync", "async"
  
  engine:
    nome: "OntoEngine"
    workers: 4
    max_concorrencia: 10
    loop_eventos: "asyncio"
  
  pipeline:
    default: "principal"
    pipelines_disponiveis:
      - basico
      - principal
      - precisao
    timeout_total_segundos: 120
    circuit_breaker:
      ativo: true
      max_falhas: 5
      janela_segundos: 60
      tempo_recuperacao_ms: 30000
  
  # Gerenciamento de estado
  estado:
    tipo: "redis"  # "memory", "redis", "postgresql"
    redis_config:
      host: "localhost"
      porta: 6379
      db: 2
    sessao_ttl: 7200  # 2 horas
  
  # Monitoramento
  monitoramento:
    ativo: true
    endpoint_health: "/health"
    endpoint_metrics: "/metrics"
    exportador: "prometheus"
    metricas:
      - solicitacoes_total
      - solicitacoes_erro
      - latencia_media
      - latencia_p95
      - latencia_p99
      - cache_hits
      - cache_misses
      - pipeline_utilizacao
  
  # Logging
  logging:
    nivel: "INFO"
    formato: "json"
    saida: "stdout"
    arquivo:
      ativo: true
      path: "./runtime/logs/"
      rotacao:
        max_size_mb: 100
        backup_count: 10
        compressao: true
  
  # Tratamento de erros
  erros:
    capturar_stacktrace: true
    notificar: true
    canal: "sentry"
    dsn: "${SENTRY_DSN}"
    niveis:
      - CRITICAL
      - ERROR
  
  # Recursos
  recursos:
    max_memoria_mb: 2048
    max_threads: 16
    garbage_collection: "generational"
"""

runtime_path = os.path.join(BASE, "runtime/runtime.yaml")
with open(runtime_path, "w", encoding="utf-8") as f:
    f.write(runtime_content)
print(f"  [FILE] runtime/runtime.yaml")

# core/__init__.py
core_init = '''"""
Módulo Core — Componentes centrais do sistema cognitivo ontológico.

Este módulo contém a lógica de negócio principal:
- Classificação ontológica (OntoClassifier)
- Retrieval híbrido (OntoRetriever)
- Síntese de informações (OntoSynthesizer)
- Validação de consistência (OntoValidator)
- Roteamento de pipelines (OntoRouter)
- Motor ontológico (OntoEngine)
- Grafo ontológico (OntoGraph)
- Gerenciamento de embeddings (EmbeddingManager)
"""

__version__ = "3.0.0"
__all__ = [
    "OntoClassifier",
    "OntoRetriever",
    "OntoSynthesizer",
    "OntoValidator",
    "OntoRouter",
    "OntoEngine",
    "OntoGraph",
    "EmbeddingManager",
]
'''

core_path = os.path.join(BASE, "core/__init__.py")
with open(core_path, "w", encoding="utf-8") as f:
    f.write(core_init)
print(f"  [FILE] core/__init__.py")

# tools/__init__.py
tools_init = '''"""
Módulo Tools — Utilitários e ferramentas auxiliares.

Ferramentas disponíveis:
- UID Generator: Geração de UIDs canônicos para reconciliação de IDs
- Taxonomy Converter: Conversão entre formatos de taxonomia
- Ontology Exporter: Exportação para diversos formatos
- Embedding Utils: Funções utilitárias para embeddings
- Graph Utils: Operações utilitárias sobre o grafo ontológico
- Validation Helpers: Funções auxiliares de validação
"""

__version__ = "3.0.0"
__all__ = [
    "uid_generator",
    "taxonomy_converter",
    "ontology_exporter",
    "embedding_utils",
    "graph_utils",
    "validation_helpers",
]
'''

tools_path = os.path.join(BASE, "tools/__init__.py")
with open(tools_path, "w", encoding="utf-8") as f:
    f.write(tools_init)
print(f"  [FILE] tools/__init__.py")

# tests/test_ontology.py
test_content = '''"""
Testes para o sistema cognitivo ontológico.

Executar:
    python -m pytest tests/ -v
"""

import pytest
import sys
import os

# Adicionar root ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestOntologyStructure:
    """Testes de estrutura da ontologia."""

    def test_directories_exist(self):
        """Verifica se todos os diretórios da ontologia existem."""
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dirs = [
            "ontology/n0", "ontology/n1", "ontology/n2",
            "ontology/n3", "ontology/n4",
            "data/json", "data/embeddings", "data/indexes", "data/graphs",
            "runtime", "core", "tools", "tests",
            "prompts/classifier", "prompts/retrieval",
            "prompts/synthesis", "prompts/validation", "prompts/routing",
            ".kilo/agents", ".kilo/memory", ".kilo/orchestrators",
            ".kilo/prompts/classifier", ".kilo/prompts/retrieval",
            ".kilo/prompts/synthesis", ".kilo/prompts/validation",
            ".kilo/prompts/routing",
        ]
        for d in dirs:
            assert os.path.isdir(os.path.join(base, d)), f"Diretório ausente: {d}"

    def test_yaml_files_parseable(self):
        """Verifica se todos os YAMLs são parseáveis."""
        import yaml
        import glob

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_files = glob.glob(os.path.join(base, "config", "*.yaml"))
        yaml_files += glob.glob(os.path.join(base, ".kilo", "**", "*.yaml"), recursive=True)
        yaml_files += glob.glob(os.path.join(base, "prompts", "**", "*.yaml"), recursive=True)
        yaml_files += glob.glob(os.path.join(base, "runtime", "*.yaml"))

        assert len(yaml_files) > 0, "Nenhum arquivo YAML encontrado"

        for f in yaml_files:
            with open(f, "r", encoding="utf-8") as fh:
                try:
                    yaml.safe_load(fh)
                except yaml.YAMLError as e:
                    pytest.fail(f"Erro ao parsear {f}: {e}")

    def test_requirements_txt_exists(self):
        """Verifica se requirements.txt existe e é parseável."""
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        req_path = os.path.join(base, "requirements.txt")
        assert os.path.isfile(req_path), "requirements.txt não encontrado"

        with open(req_path, "r") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            assert len(lines) > 0, "requirements.txt está vazio"
            for line in lines:
                assert ">=" in line or "==" in line, f"Dependência mal formatada: {line}"

    def test_ontology_yaml_structure(self):
        """Verifica estrutura básica do ontology.yaml."""
        import yaml
        import os

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/ontology.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "n0_vetores" in data, "n0_vetores ausente"
        assert "n1_pilares" in data, "n1_pilares ausente"
        assert "n2_dominios" in data, "n2_dominios ausente"
        assert "n3_sub_arvores" in data, "n3_sub_arvores ausente"
        assert "n4_celulas" in data, "n4_celulas ausente"

        # Verificar contagem
        assert len(data["n0_vetores"]) == 2, f"Esperado 2 vetores, encontrado {len(data['n0_vetores'])}"
        assert len(data["n1_pilares"]) == 6, f"Esperado 6 pilares, encontrado {len(data['n1_pilares'])}"
        assert len(data["n2_dominios"]) == 18, f"Esperado 18 domínios, encontrado {len(data['n2_dominios'])}"
        assert len(data["n3_sub_arvores"]) == 54, f"Esperado 54 subárvores, encontrado {len(data['n3_sub_arvores'])}"
        assert len(data["n4_celulas"]) == 162, f"Esperado 162 células N4, encontrado {len(data['n4_celulas'])}"


class TestEmbeddingConfig:
    """Testes de configuração de embeddings."""

    def test_embedding_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/embedding.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "modelo" in data
        assert data["modelo"]["dimensao"] == 384
        assert "vetores_pesos" in data
        assert sum(data["vetores_pesos"].values()) == pytest.approx(1.0, 0.01)


class TestRetrievalConfig:
    """Testes de configuração de retrieval."""

    def test_retrieval_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/retrieval.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "vetorial" in data
        assert "grafico" in data
        assert "simbolico" in data
        assert "fusao" in data
        assert data["fusao"]["pesos"]["vetorial"] == 0.50
        assert data["fusao"]["pesos"]["grafico"] == 0.30
        assert data["fusao"]["pesos"]["simbolico"] == 0.20
        assert pytest.approx(sum(data["fusao"]["pesos"].values()), 0.01) == 1.0


class TestGraphConfig:
    """Testes de configuração do grafo."""

    def test_graph_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/graph.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "grafo" in data
        assert data["grafo"]["engine"] == "networkx"
        assert data["grafo"]["tipo"] == "MultiDiGraph"
        assert "persistencia" in data["grafo"]
        assert "algoritmos" in data["grafo"]


class TestAgentConfigs:
    """Testes de configuração dos agentes."""

    def test_agents_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, ".kilo/agents/agents.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "agentes" in data
        expected_agents = ["classificador", "retriever", "sintetizador", "validador", "roteador"]
        for agent in expected_agents:
            assert agent in data["agentes"], f"Agente ausente: {agent}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
'''

test_path = os.path.join(BASE, "tests/test_ontology.py")
with open(test_path, "w", encoding="utf-8") as f:
    f.write(test_content)
print(f"  [FILE] tests/test_ontology.py")

# .kilo/.gitignore
gitignore_content = """# Dados sensíveis
memory/*.db
memory/sessions/
*.secret

# Cache de embeddings
embeddings/cache/
embeddings/*.npy

# Logs
runtime/logs/*.log

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sistema operacional
Thumbs.db
.DS_Store
"""

gitignore_path = os.path.join(BASE, ".kilo/.gitignore")
with open(gitignore_path, "w", encoding="utf-8") as f:
    f.write(gitignore_content)
print(f"  [FILE] .kilo/.gitignore")

# Placeholder files for ontology subdirectories
for level in ["n0", "n1", "n2", "n3", "n4"]:
    placeholder = os.path.join(BASE, f"ontology/{level}/.gitkeep")
    with open(placeholder, "w") as f:
        f.write("")
    print(f"  [FILE] ontology/{level}/.gitkeep")

for subdir in ["json", "embeddings", "indexes", "graphs"]:
    placeholder = os.path.join(BASE, f"data/{subdir}/.gitkeep")
    with open(placeholder, "w") as f:
        f.write("")
    print(f"  [FILE] data/{subdir}/.gitkeep")

# README.md for the project
readme_content = """# MestreCuca — Sistema Cognitivo Ontológico

## Arquitetura

Sistema cognitivo baseado em ontologia fractal com 162 células N4 (2×3×3×3×3).

### Estrutura de Diretórios

```
.
├── config/                    # Configurações YAML
│   ├── ontology.yaml          # Definição completa da ontologia
│   ├── embedding.yaml         # Configuração de modelos de embedding
│   ├── retrieval.yaml         # Thresholds e limites de retrieval
│   └── graph.yaml             # Configuração do grafo NetworkX
├── ontology/                  # Dados ontológicos por nível
│   ├── n0/                    # Vetores (SINTRÓPICO/ENTRÓPICO)
│   ├── n1/                    # Pilares (LOGOS/BIOS/PATHOS/KHAOS/APEIRON/MYTHOS)
│   ├── n2/                    # Domínios (18 domínios)
│   ├── n3/                    # Subárvores (54 subárvores)
│   └── n4/                    # Células operacionais (162 células)
├── data/                      # Dados persistentes
│   ├── json/                  # Documentos JSON
│   ├── embeddings/            # Vetores de embedding
│   ├── indexes/               # Índices de busca
│   └── graphs/                # Grafos persistidos (GEXF)
├── core/                      # Módulos centrais
├── tools/                     # Utilitários
├── runtime/                   # Configuração de execução
├── prompts/                   # Templates de prompt
│   ├── classifier/
│   ├── retrieval/
│   ├── synthesis/
│   ├── validation/
│   └── routing/
├── .kilo/                     # Configuração interna
│   ├── agents/
│   ├── memory/
│   ├── orchestrators/
│   └── prompts/
├── tests/                     # Testes
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Testes

```bash
python -m pytest tests/ -v
```
"""

readme_path = os.path.join(BASE, "README.md")
with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_content)
print(f"  [FILE] README.md")

print("\n" + "="*60)
print("  FASE 0 CONCLUÍDA — Estrutura criada com sucesso!")
print("="*60)
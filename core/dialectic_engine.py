"""
Dialectic Engine — Mapeamento de oposições ontológicas e distância dialética
para as 162 células N4 da ontologia fractal.

Design:
  1. Mapeamento explícito KNOWN_OPPOSITES para pares conhecidos
  2. Inferência semântica por análise de nome/conceito (antônimos, inversões)
  3. Inferência posicional (nós distantes no grafo = potenciais opostos)
  4. Regras de domínio (oposições típicas por área temática)
  5. Construção do mapa de tensões dialéticas
"""

from __future__ import annotations

import math
from collections import defaultdict
from typing import Optional


class DialecticEngine:
    """Motor de inferência de opostos ontológicos e distância dialética."""

    # Camada 1: Mapeamento explícito de opostos por UID
    # Cada par A↔B é bidirecional
    KNOWN_OPPOSITES: dict[str, str] = {
        # ALGORITMIA — RESOLUÇÃO
        "N4_ALGORITMIA_1_A": "N4_ALGORITMIA_1_C",  # DECOMPOSIÇÃO_BINÁRIA ↔ CASO_BASE
        "N4_ALGORITMIA_1_C": "N4_ALGORITMIA_1_A",
        "N4_ALGORITMIA_1_B": "N4_ALGORITMIA_3_A",  # SEQUÊNCIA ↔ RECURSÃO
        "N4_ALGORITMIA_3_A": "N4_ALGORITMIA_1_B",

        # ALGORITMIA — OTIMIZAÇÃO
        "N4_ALGORITMIA_2_A": "N4_ALGORITMIA_2_C",  # BRUTE_FORCE ↔ OTIMIZADO
        "N4_ALGORITMIA_2_C": "N4_ALGORITMIA_2_A",

        # ALGORITMIA — VALIDAÇÃO
        "N4_ALGORITMIA_3_B": "N4_ALGORITMIA_3_C",  # TESTE ↔ CORREÇÃO
        "N4_ALGORITMIA_3_C": "N4_ALGORITMIA_3_B",

        # NOMOS
        "N4_NOMOS_1_A": "N4_NOMOS_1_C",  # CONSTITUIÇÃO ↔ ANARQUIA
        "N4_NOMOS_1_C": "N4_NOMOS_1_A",
        "N4_NOMOS_2_A": "N4_NOMOS_2_C",  # DIREITO ↔ EXCEÇÃO
        "N4_NOMOS_2_C": "N4_NOMOS_2_A",

        # MECÂNICA
        "N4_MECANICA_1_A": "N4_MECANICA_1_B",  # ESTÁTICA ↔ DINÂMICA
        "N4_MECANICA_1_B": "N4_MECANICA_1_A",
        "N4_MECANICA_2_A": "N4_MECANICA_2_C",  # EQUILÍBRIO ↔ DESBALANCEAMENTO
        "N4_MECANICA_2_C": "N4_MECANICA_2_A",

        # OIKOS
        "N4_OIKOS_1_A": "N4_OIKOS_1_C",  # PROTEÇÃO ↔ VULNERABILIDADE
        "N4_OIKOS_1_C": "N4_OIKOS_1_A",
        "N4_OIKOS_2_A": "N4_OIKOS_2_C",  # TERRITÓRIO ↔ DISPERSÃO
        "N4_OIKOS_2_C": "N4_OIKOS_2_A",

        # SOMA
        "N4_SOMA_1_A": "N4_SOMA_1_B",  # MANUTENÇÃO ↔ DEGRADAÇÃO
        "N4_SOMA_1_B": "N4_SOMA_1_A",
        "N4_SOMA_2_A": "N4_SOMA_2_C",  # HOMEOSTASE ↔ COLAPSO
        "N4_SOMA_2_C": "N4_SOMA_2_A",

        # METABOLISMO
        "N4_METABOLISMO_1_A": "N4_METABOLISMO_1_C",  # ANABOLISMO ↔ CATABOLISMO
        "N4_METABOLISMO_1_C": "N4_METABOLISMO_1_A",
        "N4_METABOLISMO_2_A": "N4_METABOLISMO_2_B",  # ABSORÇÃO ↔ EXCREÇÃO
        "N4_METABOLISMO_2_B": "N4_METABOLISMO_2_A",

        # ETHOS
        "N4_ETHOS_1_A": "N4_ETHOS_1_B",  # ALINHAMENTO ↔ CONFLITO
        "N4_ETHOS_1_B": "N4_ETHOS_1_A",
        "N4_ETHOS_2_A": "N4_ETHOS_2_C",  # DIREITO ↔ DEVER
        "N4_ETHOS_2_C": "N4_ETHOS_2_A",

        # ALTERIDADE
        "N4_ALTERIDADE_1_A": "N4_ALTERIDADE_1_C",  # IDENTIDADE ↔ DIFERENÇA
        "N4_ALTERIDADE_1_C": "N4_ALTERIDADE_1_A",
        "N4_ALTERIDADE_2_A": "N4_ALTERIDADE_2_C",  # MUDANÇA ↔ PERMANÊNCIA
        "N4_ALTERIDADE_2_C": "N4_ALTERIDADE_2_A",

        # ESTÉTICA
        "N4_ESTETICA_1_A": "N4_ESTETICA_1_B",  # BELEZA ↔ FEIURA
        "N4_ESTETICA_1_B": "N4_ESTETICA_1_A",
        "N4_ESTETICA_2_A": "N4_ESTETICA_2_C",  # HARMONIA ↔ DISSONÂNCIA
        "N4_ESTETICA_2_C": "N4_ESTETICA_2_A",

        # ENTROPIA
        "N4_ENTROPIA_1_A": "N4_ENTROPIA_1_C",  # ORDEM ↔ DESORDEN
        "N4_ENTROPIA_1_C": "N4_ENTROPIA_1_A",
        "N4_ENTROPIA_2_A": "N4_ENTROPIA_2_C",  # CONCENTRAÇÃO ↔ DISSIPAÇÃO
        "N4_ENTROPIA_2_C": "N4_ENTROPIA_2_A",

        # SINGULARIDADE
        "N4_SINGULARIDADE_1_A": "N4_SINGULARIDADE_1_C",  # PONTO_CRÍTICO ↔ ESTABILIDADE
        "N4_SINGULARIDADE_1_C": "N4_SINGULARIDADE_1_A",
        "N4_SINGULARIDADE_2_A": "N4_SINGULARIDADE_2_C",  # EMERGÊNCIA ↔ DESAPARECIMENTO
        "N4_SINGULARIDADE_2_C": "N4_SINGULARIDADE_2_A",

        # SÍNTESE
        "N4_SÍNTESE_1_A": "N4_SÍNTESE_1_B",  # INTEGRAÇÃO ↔ FRAGMENTAÇÃO
        "N4_SÍNTESE_1_B": "N4_SÍNTESE_1_A",
        "N4_SÍNTESE_2_A": "N4_SÍNTESE_2_C",  # UNIVERSAL ↔ PARTICULAR
        "N4_SÍNTESE_2_C": "N4_SÍNTESE_2_A",

        # ESCALA
        "N4_ESCALA_1_A": "N4_ESCALA_1_C",  # MICRO ↔ MACRO
        "N4_ESCALA_1_C": "N4_ESCALA_1_A",
        "N4_ESCALA_2_A": "N4_ESCALA_2_C",  # AMPLIAÇÃO ↔ REDUÇÃO
        "N4_ESCALA_2_C": "N4_ESCALA_2_A",

        # VIBRATIO
        "N4_VIBRATIO_1_A": "N4_VIBRATIO_1_B",  # RESSONÂNCIA ↔ DISSONÂNCIA
        "N4_VIBRATIO_1_B": "N4_VIBRATIO_1_A",
        "N4_VIBRATIO_2_A": "N4_VIBRATIO_2_C",  # AMPLITUDE ↔ AMORTECIMENTO
        "N4_VIBRATIO_2_C": "N4_VIBRATIO_2_A",

        # VÁCUO
        "N4_VACUO_1_A": "N4_VACUO_1_B",  # VAZIO ↔ PLENITUDE
        "N4_VACUO_1_B": "N4_VACUO_1_A",
        "N4_VACUO_2_A": "N4_VACUO_2_C",  # SILÊNCIO ↔ RUÍDO
        "N4_VACUO_2_C": "N4_VACUO_2_A",

        # ARQUÉTIPO
        "N4_ARQUETIPO_1_A": "N4_ARQUETIPO_1_C",  # RECONHECIMENTO ↔ ESQUECIMENTO
        "N4_ARQUETIPO_1_C": "N4_ARQUETIPO_1_A",
        "N4_ARQUETIPO_2_A": "N4_ARQUETIPO_2_C",  # CRISE ↔ RENOVAÇÃO
        "N4_ARQUETIPO_2_C": "N4_ARQUETIPO_2_A",

        # NARRATIVA
        "N4_NARRATIVA_1_A": "N4_NARRATIVA_1_C",  # TEIA ↔ ISOLAMENTO
        "N4_NARRATIVA_1_C": "N4_NARRATIVA_1_A",
        "N4_NARRATIVA_2_A": "N4_NARRATIVA_2_C",  # MEMÓRIA ↔ ESQUECIMENTO
        "N4_NARRATIVA_2_C": "N4_NARRATIVA_2_A",

        # MISTÉRIO
        "N4_MISTERIO_1_A": "N4_MISTERIO_1_C",  # REVELAÇÃO ↔ OCULTAMENTO
        "N4_MISTERIO_1_C": "N4_MISTERIO_1_A",
        "N4_MISTERIO_2_A": "N4_MISTERIO_2_C",  # CLARIDADE ↔ OBSCURIDADE
        "N4_MISTERIO_2_C": "N4_MISTERIO_2_A",
    }

    # Camada 2: Antônimos conceituais — inferência por nome normalizado
    ANTONYM_PATTERNS: dict[str, str] = {
        # Pares de antônimos/ inversões semânticas
        "criação": "destruição", "destruição": "criação",
        "ordem": "desordem", "desordem": "ordem",
        "construção": "destruição",
        "união": "separação", "separação": "união",
        "integração": "fragmentação", "fragmentação": "integração",
        "equilíbrio": "desequilíbrio", "desequilíbrio": "equilíbrio",
        "estabilidade": "instabilidade", "instabilidade": "estabilidade",
        "harmonia": "dissonância", "dissonância": "harmonia",
        "luz": "trevas", "trevas": "luz",
        "vida": "morte", "morte": "vida",
        "presença": "ausência", "ausência": "presença",
        "verdade": "mentira", "mentira": "verdade",
        "conhecimento": "ignorância", "ignorância": "conhecimento",
        "liberdade": "escravidão", "escravidão": "liberdade",
        "poder": "impotência", "impotência": "poder",
        "riqueza": "pobreza", "pobreza": "riqueza",
        "felicidade": "sofrimento", "sofrimento": "felicidade",
        "amor": "ódio", "ódio": "amor",
        "esperança": "desespero", "desespero": "esperança",
        "cooperação": "competição", "competição": "cooperação",
        "abertura": "fechamento", "fechamento": "abertura",
        "clareza": "ambiguidade", "ambiguidade": "clareza",
        "simplicidade": "complexidade", "complexidade": "simplicidade",
        "permanência": "mudança", "mudança": "permanência",
        "começo": "fim", "fim": "começo",
        "ascensão": "queda", "queda": "ascensão",
        "expansão": "contração", "contração": "expansão",
        "centro": "periferia", "periferia": "centro",
        "macro": "micro", "micro": "macro",
        "síntese": "análise", "análise": "síntese",
        "teoria": "prática", "prática": "teoria",
        "potencial": "atual", "atual": "potencial",
        "essência": "aparência", "aparência": "essência",
        "espírito": "matéria", "matéria": "espírito",
        "forma": "substância", "substância": "forma",
        "causa": "efeito", "efeito": "causa",
        "razão": "emoção", "emoção": "razão",
        "indivíduo": "coletivo", "coletivo": "indivíduo",
        "parte": "todo", "todo": "parte",
        "eterno": "temporal", "temporal": "eterno",
        "necessário": "contingente", "contingente": "necessário",
        "absoluto": "relativo", "relativo": "absoluto",
        "objetivo": "subjetivo", "subjetivo": "objetivo",
        "racional": "irracional", "irracional": "racional",
        "natural": "artificial", "artificial": "natural",
        "orgânico": "mecânico", "mecânico": "orgânico",
        "vivo": "morto", "morto": "vivo",
        "ativo": "passivo", "passivo": "ativo",
        "positivo": "negativo", "negativo": "positivo",
        "constante": "variável", "variável": "constante",
        "linear": "não_linear", "não_linear": "linear",
        "determinístico": "estocástico", "estocástico": "determinístico",
        "convergente": "divergente", "divergente": "convergente",
        "estável": "instável", "instável": "estável",
        "resistente": "frágil", "frágil": "resistente",
        "rígido": "flexível", "flexível": "rígido",
        "denso": "rarefeito", "rarefeito": "denso",
        "quente": "frio", "frio": "quente",
        "pressão_alta": "pressão_baixa", "pressão_baixa": "pressão_alta",
        "compressão": "rarefação", "rarefação": "compressão",
        "carga_positiva": "carga_negativa", "carga_negativa": "carga_positiva",
        "atração": "repulsão", "repulsão": "atração",
        "aceleração": "desaceleração", "desaceleração": "aceleração",
        "entrada": "saída", "saída": "entrada",
        "produção": "consumo", "consumo": "produção",
        "oferta": "demanda", "demanda": "oferta",
        "surplus": "déficit", "déficit": "surplus",
        "público": "privado", "privado": "público",
        "local": "global", "global": "local",
        "visível": "invisível", "invisível": "visível",
        "manifesto": "latente", "latente": "manifesto",
        "consciente": "inconsciente", "inconsciente": "consciente",
        "racional": "intuitivo", "intuitivo": "racional",
        "analítico": "sintético", "sintético": "analítico",
        "dedutivo": "indutivo", "indutivo": "dedutivo",
        "verificação": "refutação", "refutação": "verificação",
        "confirmação": "negação", "negação": "confirmação",
        "inclusão": "exclusão", "exclusão": "inclusão",
        "pertencimento": "alienação", "alienação": "pertencimento",
        "integração": "marginalização", "marginalização": "integração",
        "convergência": "divergência", "divergência": "convergência",
        "concentração": "dispersão", "dispersão": "concentração",
        "acúmulo": "esvaziamento", "esvaziamento": "acúmulo",
        "construção": "demolição", "demolição": "construção",
        "criação": "aniquilação", "aniquilação": "criação",
        "união": "dissolução", "dissolução": "união",
        "coerência": "incoerência", "incoerência": "coerência",
        "consistência": "inconsistência", "inconsistência": "consistência",
        "completude": "incompletude", "incompletude": "completude",
        "perfeição": "imperfeição", "imperfeição": "perfeição",
        "plenitude": "vazio", "vazio": "plenitude",
        "sabedoria": "ignorância",
        "compaixão": "indiferença", "indiferença": "compaixão",
        "generosidade": "egoísmo", "egoísmo": "generosidade",
        "humildade": "orgulho", "orgulho": "humildade",
        "coragem": "covardia", "covardia": "coragem",
        "justiça": "injustiça", "injustiça": "justiça",
        "verdade": "falsidade", "falsidade": "verdade",
        "honestidade": "desshonestidade", "desshonestidade": "honestidade",
        "lealdade": "traição", "traição": "lealdade",
        "confiança": "desconfiança", "desconfiança": "confiança",
        "segurança": "insegurança", "insegurança": "segurança",
        "proteção": "vulnerabilidade", "vulnerabilidade": "proteção",
        "defesa": "ataque", "ataque": "defesa",
        "paz": "guerra", "guerra": "paz",
        "concórdia": "discórdia", "discórdia": "concórdia",
        "acordo": "discordância", "discordância": "acordo",
        "aprovação": "rejeição", "rejeição": "aprovação",
        "inclusão": "exclusão", "exclusão": "inclusão",
        "pertencimento": "exílio", "exílio": "pertencimento",
        "encontro": "separação", "separação": "encontro",
        "conexão": "desconexão", "desconexão": "conexão",
        "comunicação": "silêncio", "silêncio": "comunicação",
        "expressão": "repressão", "repressão": "expressão",
        "criação": "destruição", "destruição": "criação",
        "renascimento": "morte", "morte": "renascimento",
        "transformação": "estagnação", "estagnação": "transformação",
        "evolução": "involução", "involução": "evolução",
        "progresso": "regresso", "regresso": "progresso",
        "inovação": "tradição", "tradição": "inovação",
        "futuro": "passado", "passado": "futuro",
        "possibilidade": "impossibilidade", "impossibilidade": "possibilidade",
        "potência": "impotência", "impotência": "potência",
        "ação": "inércia", "inércia": "ação",
        "movimento": "estagnação", "estagnação": "movimento",
        "fluidez": "rigidez", "rigidez": "fluidez",
        "adaptação": "rigidez",
        "abundância": "escassez", "escassez": "abundância",
        "excesso": "deficiência", "deficiência": "excesso",
        "saturação": "carência", "carência": "saturação",
        "compressão": "expansão", "expansão": "compressão",
        "acoplamento": "desacoplamento", "desacoplamento": "acoplamento",
        "sincronia": "assincronia", "assincronia": "sincronia",
        "sequencial": "paralelo", "paralelo": "sequencial",
        "serial": "paralelo",
        "concentração": "descentralização", "descentralização": "concentração",
        "hierarquia": "igualdade", "igualdade": "hierarquia",
        "vertical": "horizontal", "horizontal": "vertical",
        "superfície": "profundidade", "profundidade": "superfície",
        "exterior": "interior", "interior": "exterior",
        "objetivo": "subjetivo", "subjetivo": "objetivo",
        "universal": "particular", "particular": "universal",
        "absoluto": "relativo", "relativo": "absoluto",
        "permanente": "temporário", "temporário": "permanente",
        "total": "parcial", "parcial": "total",
        "contínuo": "discreto", "discreto": "contínuo",
        "infinito": "finito", "finito": "infinito",
        "divisível": "indivisível", "indivisível": "divisível",
        "composto": "simples", "simples": "composto",
        "heterogêneo": "homogêneo", "homogêneo": "heterogêneo",
        "simétrico": "assimétrico", "assimétrico": "simétrico",
        "periódico": "aperiódico", "aperiódico": "periódico",
        "reversível": "irreversível", "irreversível": "reversível",
        "espontâneo": "forçado", "forçado": "espontâneo",
        "endógeno": "exógeno", "exógeno": "endógeno",
        "interno": "externo", "externo": "interno",
        "implicito": "explícito", "explícito": "implícito",
        "tácito": "declarativo", "declarativo": "tácito",
        "formal": "informal", "informal": "formal",
        "rigoroso": "relaxado", "relaxado": "rigoroso",
        "preciso": "impreciso", "impreciso": "preciso",
        "exato": "aproximado", "aproximado": "exato",
        "determinado": "indeterminado", "indeterminado": "determinado",
        "fixo": "móvel", "móvel": "fixo",
        "sólido": "fluido", "fluido": "sólido",
        "transparente": "opaco", "opaco": "transparente",
        "lúcido": "obscuro", "obscuro": "lúcido",
        "claro": "obscuro",
        "puro": "impuro", "impuro": "puro",
        "refinado": "bruto", "bruto": "refinado",
        "processado": "natural",
        "artificial": "natural",
        "sintético": "natural",
        "abstrato": "concreto", "concreto": "abstrato",
        "teórico": "prático", "prático": "teórico",
        "ideal": "real", "real": "ideal",
        "platônico": "empírico", "empírico": "platônico",
        "necessário": "contingente", "contingente": "necessário",
        "possível": "impossível", "impossível": "possível",
        "provável": "improvável", "improvável": "provável",
        "certeza": "incerteza", "incerteza": "certeza",
        "segurança": "risco", "risco": "segurança",
        "ordem": "caos", "caos": "ordem",
        "organização": "desorganização", "desorganização": "organização",
        "estrutura": "desestrutura", "desestrutura": "estrutura",
        "padrão": "aleatoriedade", "aleatoriedade": "padrão",
        "regularidade": "irregularidade", "irregularidade": "regularidade",
        "previsibilidade": "imprevisibilidade", "imprevisibilidade": "previsibilidade",
        "controle": "descontrole", "descontrole": "controle",
        "domínio": "servidão", "servidão": "domínio",
        "soberania": "submissão", "submissão": "soberania",
        "autonomia": "heteronomia", "heteronomia": "autonomia",
        "independência": "dependência", "dependência": "independência",
        "autossuficiência": "vulnerabilidade",
        "integridade": "corrupção", "corrupção": "integridade",
        "saúde": "doença", "doença": "saúde",
        "cura": "enfermidade", "enfermidade": "cura",
        "nutrição": "fome", "fome": "nutrição",
        "saciedade": "fome",
        "água": "seca", "seca": "água",
        "fertilidade": "esterilidade", "esterilidade": "fertilidade",
        "crescimento": "decrescimento", "decrescimento": "crescimento",
        "maturação": "imaturidade", "imaturidade": "maturação",
        "evolução": "estagnação",
        "dinamismo": "estagnação",
        "juventude": "velhice", "velhice": "juventude",
        "novo": "velho", "velho": "novo",
        "início": "fim", "fim": "início",
        "primeiro": "último", "último": "primeiro",
        "superior": "inferior", "inferior": "superior",
        "elevado": "baixo", "baixo": "elevado",
        "céu": "terra", "terra": "céu",
        "montanha": "vale", "vale": "montanha",
        "superfície": "profundidade",
        "topo": "base", "base": "topo",
        "frente": "trás", "trás": "frente",
        "direita": "esquerda", "esquerda": "direita",
        "masculino": "feminino", "feminino": "masculino",
        "ativo": "passivo", "passivo": "ativo",
        "yang": "yin", "yin": "yang",
        "criação": "destruição",
        "presença": "ausência",
        "chegada": "partida", "partida": "chegada",
        "entrada": "saída", "saída": "entrada",
        "abertura": "fechamento", "fechamento": "abertura",
        "expansão": "contração", "contração": "expansão",
        "cima": "baixo", "baixo": "cima",
        "dia": "noite", "noite": "dia",
        "verão": "inverno", "inverno": "verão",
        "quente": "frio", "frio": "quente",
        "seco": "úmido", "úmido": "seco",
        "leve": "pesado", "pesado": "leve",
        "rápido": "lento", "lento": "rápido",
        "forte": "fraco", "fraco": "forte",
        "duro": "macio", "macio": "duro",
        "áspero": "suave", "suave": "áspero",
        "claro": "escuro", "escuro": "claro",
        "brilhante": "opaco", "opaco": "brilhante",
        "alto": "baixo", "baixo": "alto",
        "agudo": "grave", "grave": "agudo",
        "melodia": "discórdia", "discórdia": "melodia",
        "consonância": "dissonância", "dissonância": "consonância",
        "silêncio": "ruído", "ruído": "silêncio",
        "sombra": "luz", "luz": "sombra",
        "brilho": "opacidade", "opacidade": "brilho",
        "cor": "monocromático",
        "beleza": "feiura", "feiura": "beleza",
        "elegância": "tosquice", "tosquice": "elegância",
        "proporção": "desproporção", "desproporção": "proporção",
        "simetria": "assimetria", "assimetria": "simetria",
        "ordem": "desordem",
        "padrão": "ruído",
        "sinal": "ruído",
        "informação": "entropia", "entropia": "informação",
        "coerência": "incoerência",
        "foco": "dispersão", "dispersão": "foco",
        "atenção": "distração", "distração": "atenção",
        "consciência": "inconsciência", "inconsciência": "consciência",
        "vigília": "sono", "sono": "vigília",
        "sonho": "realidade", "realidade": "sonho",
        "fantasia": "realidade",
        "ilusão": "verdade", "verdade": "ilusão",
        "aparência": "essência", "essência": "aparência",
        "máscara": "rosto", "rosto": "máscara",
        "persona": "sombra", "sombra": "persona",
        "ego": "alteridade", "alteridade": "ego",
        "self": "outro", "outro": "self",
        "mesmo": "diferente", "diferente": "mesmo",
        "identidade": "diferença", "diferença": "identidade",
        "unidade": "multiplicidade", "multiplicidade": "unidade",
        "totalidade": "parcialidade", "parcialidade": "totalidade",
        "plenitude": "vazio", "vazio": "plenitude",
        "saciedade": "fome",
        "completude": "incompletude", "incompletude": "completude",
        "perfeição": "imperfeição", "imperfeição": "perfeição",
        "ideal": "real", "real": "ideal",
        "aspiração": "resignação", "resignação": "aspiração",
        "ambição": "contentamento",
        "desejo": "apatia", "apatia": "desejo",
        "paixão": "indiferença", "indiferença": "paixão",
        "intensidade": "suavidade", "suavidade": "intensidade",
        "extremo": "moderado", "moderado": "extremo",
        "excesso": "moderação", "moderação": "excesso",
        "abundância": "escassez", "escassez": "abundância",
        "riqueza": "pobreza", "pobreza": "riqueza",
        "opulência": "ascetismo", "ascetismo": "opulência",
        "luxo": "simplicidade", "simplicidade": "luxo",
        "complexidade": "simplicidade", "simplicidade": "complexidade",
        "sofisticação": "simplicidade",
        "ornamento": "desnudez", "desnudez": "ornamento",
        "barroco": "minimalismo", "minimalismo": "barroco",
        "movimento": "estagnação",
        "agitação": "calmaria", "calmaria": "agitação",
        "tempestade": "calmaria", "calmaria": "tempestade",
        "caos": "ordem", "ordem": "caos",
        "anarquia": "governo", "governo": "anarquia",
        "tiranía": "democracia", "democracia": "tiranía",
        "opressão": "libertação", "libertação": "opressão",
        "dominação": "submissão", "submissão": "dominação",
        "controle": "liberdade", "liberdade": "controle",
        "regra": "exceção", "exceção": "regra",
        "norma": "anomalia", "anomalia": "norma",
        "lei": "crime", "crime": "lei",
        "justiça": "injustiça", "injustiça": "justiça",
        "verdade": "mentira", "mentira": "verdade",
        "honestidade": "desonestidade", "desonestidade": "honestidade",
        "lealdade": "traição", "traição": "lealdade",
        "fidelidade": "infidelidade", "infidelidade": "fidelidade",
        "amor": "ódio", "ódio": "amor",
        "compaixão": "crueldade", "crueldade": "compaixão",
        "empatia": "antipatia", "antipatia": "empatia",
        "amizade": "inimizade", "inimizade": "amizade",
        "cooperação": "rivalidade", "rivalidade": "cooperação",
        "união": "divisão", "divisão": "união",
        "paz": "guerra", "guerra": "paz",
        "concórdia": "discórdia", "discórdia": "concórdia",
        "harmonia": "conflito", "conflito": "harmonia",
        "acordo": "desacordo", "desacordo": "acordo",
        "consentimento": "oposição", "oposição": "consentimento",
        "aprovação": "rejeição", "rejeição": "aprovação",
        "aceitação": "rejeição",
        "inclusão": "exclusão", "exclusão": "inclusão",
        "pertencimento": "exílio", "exílio": "pertencimento",
        "integração": "segregação", "segregação": "integração",
        "assimilação": "diferenciação", "diferenciação": "assimilação",
        "adaptação": "rigidez",
        "flexibilidade": "rigidez", "rigidez": "flexibilidade",
        "resiliência": "fragilidade", "fragilidade": "resiliência",
        "durabilidade": "efemeridade", "efemeridade": "durabilidade",
        "permanência": "transitoriedade", "transitoriedade": "permanência",
        "imortalidade": "mortalidade", "mortalidade": "imortalidade",
        "renascimento": "extinção", "extinção": "renascimento",
        "germinação": "morte",
        "brotar": "murchar", "murchar": "brotar",
        "florescer": "murchar",
        "crescer": "murchar",
        "ascender": "descender", "descender": "ascender",
        "subir": "descer", "descer": "subir",
        "avançar": "recuar", "recuar": "avançar",
        "progresso": "regresso",
        "evolução": "involução", "involução": "evolução",
        "desenvolvimento": "degeneração", "degeneração": "desenvolvimento",
        "melhoria": "piora", "piora": "melhoria",
        "otimização": "degradação", "degradação": "otimização",
        "eficiência": "ineficiência", "ineficiência": "eficiência",
        "eficácia": "ineficácia", "ineficácia": "eficácia",
        "precisão": "imprecisão", "imprecisão": "precisão",
        "acurácia": "inacurácia", "inacurácia": "acurácia",
        "velocidade": "lentidão", "lentidão": "velocidade",
        "rapidez": "lentidão",
        "agilidade": "rigidez",
        "leveza": "peso", "peso": "leveza",
        "densidade": "rarefação", "rarefação": "densidade",
        "viscosidade": "fluidez", "fluidez": "viscosidade",
        "elasticidade": "rigidez",
        "ductilidade": "fragilidade",
        "magnetismo": "não_magnetismo",
        "gravidade": "levidade", "levidade": "gravidade",
        "atrito": "lubrificação",
        "fricção": "fluidez",
        "resistência": "condutância", "condutância": "resistência",
        "capacitância": "indutância",
        "voltagem": "corrente",
        "potencial": "cinético",
        "estático": "dinâmico",
        "carga": "descarga",
        "campo": "partícula",
        "onda": "partícula",
        "frequência": "amplitude",
        "período": "frequência",
        "wavelength": "frequência",
        "compressão": "rarefação",
        "reflexão": "refração",
        "absorção": "transmissão",
        "opacidade": "transparência",
        "emissão": "absorção",
        "exotérmico": " endotérmico", "endotérmico": "exotérmico",
        "ácido": "básico", "básico": "ácido",
        "alcalino": "ácido",
        "oxidação": "redução", "redução": "oxidação",
        "catão": "ânion", "ânion": "catão",
        "polar": "apolar", "apolar": "polar",
        "hidrofílico": "hidrofóbico", "hidrofóbico": "hidrofílico",
        "solúvel": "insolúvel", "insolúvel": "solúvel",
        "saturado": "insaturado", "insaturado": "saturado",
        "árido": "úmido", "úmido": "árido",
        "tropical": "polar", "polar": "tropical",
        "continental": "marítimo", "marítimo": "continental",
        "superficial": "profundo", "profundo": "superficial",
        "raso": "profundo",
        "estreito": "largo", "largo": "estreito",
        "curto": "longo", "longo": "curto",
        "pequeno": "grande", "grande": "pequeno",
        "micro": "macro", "macro": "micro",
        "minúsculo": "enorme", "enorme": "minúsculo",
        "leve": "pesado", "pesado": "leve",
        "delgado": "grosso", "grosso": "delgado",
        "fino": "grosso",
        "estreito": "amplo", "amplo": "estreito",
        "compacto": "esparso", "esparso": "compacto",
        "denso": "rarefeito", "rarefeito": "denso",
        "concentrado": "diluído", "diluído": "concentrado",
        "puro": "impuro", "impuro": "puro",
        "refinado": "cru", "cru": "refinado",
        "polido": "áspero", "áspero": "polido",
        "liso": "rugoso", "rugoso": "liso",
        "macio": "duro", "duro": "macio",
        "frágil": "resiliente", "resiliente": "frágil",
        "quebradiço": "flexível", "flexível": "quebradiço",
        "elástico": "rígido", "rígido": "elástico",
        "tenso": "relaxado", "relaxado": "tenso",
        "estirado": "frouxo", "frouxo": "estirado",
        "apertado": "frouxo",
        "cheio": "vazio", "vazio": "cheio",
        "lotado": "vazio",
        "preenchido": "vazio",
        "ocupado": "vago", "vago": "ocupado",
        "livre": "preso", "preso": "livre",
        "aberto": "fechado", "fechado": "aberto",
        "exposto": "protegido", "protegido": "exposto",
        "coberto": "descoberto", "descoberto": "coberto",
        "escondido": "visível", "visível": "escondido",
        "oculto": "revelado", "revelado": "oculto",
        "secreto": "público", "público": "secreto",
        "privado": "público",
        "anonimato": "identidade", "identidade": "anonimato",
        "invisibilidade": "visibilidade", "visibilidade": "invisibilidade",
        "silêncio": "som", "som": "silêncio",
        "quietude": "agitação", "agitação": "quietude",
        "calma": "agitação",
        "tranquilidade": "turbulência", "turbulência": "tranquilidade",
        "estabilidade": "instabilidade",
        "equilíbrio": "desequilíbrio",
        "centrado": "descentrado",
        "alinhado": "desalinhado",
        "calibrado": "descalibrado",
        "sintonizado": "desafinado",
        "afinado": "desafinado",
        "coordenado": "descoordenado",
        "organizado": "desorganizado",
        "arrumado": "desarrumado",
        "limpo": "sujo", "sujo": "limpo",
        "puro": "impuro",
        "claro": "turvo", "turvo": "claro",
        "transparente": "turvo",
        "livre": "preso",
        "solto": "preso",
        "fluido": "bloqueado", "bloqueado": "fluido",
        "aberto": "fechado",
        "expandido": "contraído", "contraído": "expandido",
        "inflado": "murcho", "murcho": "inflado",
        "cheio": "vazio",
        "completo": "incompleto", "incompleto": "completo",
        "terminado": "inacabado", "inacabado": "terminado",
        "concluído": "inconcluso", "inconcluso": "concluído",
        "resolvido": "não_resolvido", "não_resolvido": "resolvido",
        "curado": "doente",
        "sano": "doente",
        "íntegro": "corrompido", "corrompido": "íntegro",
        "sólido": "líquido", "líquido": "sólido",  # estados
        "gasoso": "líquido",
        "vivo": "morto",
        "ativo": "inativo", "inativo": "ativo",
        "habilitado": "desabilitado", "desabilitado": "habilitado",
        "ligado": "desligado", "desligado": "ligado",
        "on": "off", "off": "on",
        "true": "false", "false": "true",
        "verdadeiro": "falso", "falso": "verdadeiro",
        "positivo": "negativo",
        "alto": "baixo",
        "grande": "pequeno",
        "forte": "fraco",
        "pesado": "leve",
        "quente": "frio",
        "escuro": "claro",
        "largo": "estreito",
        "longo": "curto",
        "antigo": "moderno", "moderno": "antigo",
        "arcaico": "moderno",
        "primitivo": "avançado", "avançado": "primitivo",
        "básico": "avançado",
        "elementar": "avançado",
        "rudimentar": "sofisticado", "sofisticado": "rudimentar",
        "tosco": "refinado",
        "cru": "processado",
        "bruto": "refinado",
        "selvagem": "domado", "domado": "selvagem",
        "bárbaro": "civilizado", "civilizado": "bárbaro",
        "primitivo": "civilizado",
    }

    # Camada 3: Regras de oposição por domínio temático
    DOMAIN_OPPOSITES: dict[str, list[tuple[str, str]]] = {
        "ALGORITMIA": [
            ("decompor", "sintetizar"), ("sequenciar", "paralelizar"),
            ("otimizar", "brute_force"), ("validar", "invalidar"),
        ],
        "MECÂNICA": [
            ("estática", "dinâmica"), ("equilíbrio", "desequilíbrio"),
            ("força", "resistência"), ("movimento", "repouso"),
        ],
        "OIKOS": [
            ("proteção", "vulnerabilidade"), ("morada", "exílio"),
            ("território", "dispersão"), ("abrigo", "exposição"),
        ],
        "SOMA": [
            ("manutenção", "degradação"), ("homeostase", "colapso"),
            ("cura", "doença"), ("regeneração", "degeneração"),
        ],
        "METABOLISMO": [
            ("anabolismo", "catabolismo"), ("absorção", "excreção"),
            ("nutrição", "fome"), ("construção", "destruição"),
        ],
        "ETHOS": [
            ("alinhamento", "conflito"), ("direito", "dever"),
            ("justiça", "injustiça"), ("moral", "imoral"),
        ],
        "ALTERIDADE": [
            ("identidade", "diferença"), ("mudança", "permanência"),
            ("transformação", "estagnação"), ("adaptação", "rigidez"),
        ],
        "ESTÉTICA": [
            ("beleza", "feiura"), ("harmonia", "dissonância"),
            ("sublime", "banal"), ("elegância", "tosquice"),
        ],
        "ENTROPIA": [
            ("ordem", "desordem"), ("organização", "desorganização"),
            ("concentração", "dissipação"), ("coerência", "incoerência"),
        ],
        "SINGULARIDADE": [
            ("emergência", "desaparecimento"), ("crítico", "estável"),
            ("singular", "comum"), ("extremo", "moderado"),
        ],
        "SÍNTESE": [
            ("integração", "fragmentação"), ("união", "separação"),
            ("universal", "particular"), ("totalidade", "parcialidade"),
        ],
        "ESCALA": [
            ("micro", "macro"), ("ampliação", "redução"),
            ("escala_up", "escala_down"), ("expansão", "contração"),
        ],
        "VIBRATIO": [
            ("ressonância", "dissonância"), ("frequência_alta", "frequência_baixa"),
            ("amplitude", "amortecimento"), ("harmonia", "ruído"),
        ],
        "VÁCUO": [
            ("vazio", "plenitude"), ("silêncio", "ruído"),
            ("ausência", "presença"), ("nada", "tudo"),
        ],
        "ARQUÉTIPO": [
            ("reconhecimento", "esquecimento"), ("símbolo", "literal"),
            ("mito", "história"), ("coletivo", "individual"),
        ],
        "NARRATIVA": [
            ("teia", "isolamento"), ("conexão", "desconexão"),
            ("memória", "esquecimento"), ("continuidade", "ruptura"),
        ],
        "MISTÉRIO": [
            ("revelação", "ocultamento"), ("claridade", "obscuridade"),
            ("sabedoria", "ignorância"), ("mistério", "explicação"),
        ],
    }

    # Camada 4: Opostos por posição no grafo (hierarquia N3)
    # Subárvores que são opostas conceitualmente
    HIERARCHICAL_OPPOSITES: dict[str, str] = {
        # Dentro de LOGOS
        "RESOLUÇÃO": "VALIDAÇÃO",
        "VALIDAÇÃO": "RESOLUÇÃO",
        "OTIMIZAÇÃO": "DEGRADAÇÃO_CONTROLADA",
        # Dentro de BIOS
        "MORADA": "DISPERSÃO",
        "PROVISAO": "CONSUMO",
        "INTEGRIDADE": "FRAGMENTAÇÃO",
        # Dentro de PATHOS
        "VALORES": "ANTIVALORES",
        "VIRTUDE": "VÍCIO",
        "RESPONSABILIDADE": "IRRESPONSABILIDADE",
        # Dentro de KHAOS
        "DEGRADAÇÃO": "REGENERAÇÃO",
        "DISSIPAÇÃO": "CONCENTRAÇÃO",
        "CAOS": "COSMO",
        # Dentro de APEIRON
        "ESCALAMENTO": "REDUÇÃO",
        "FREQUENCIA": "SILÊNCIO",
        "DIMENSÃO": "DIMINUIÇÃO",
        # Dentro de MYTHOS
        "PADRÃO_PRIMORDIAL": "ANOMALIA",
        "TEIA": "ISOLAMENTO",
        "MISTÉRIO": "REVELAÇÃO",
    }

    def __init__(self):
        self._opposites_cache: dict[str, list[str]] = {}
        self._tension_map_cache: Optional[dict] = None

    def infer_opposites(self, cell_data: dict,
                        registry: Optional[dict] = None) -> list[str]:
        """
        Inferir opostos ontológicos para uma célula.

        Fontes (em ordem de prioridade):
        1. KNOWN_OPPOSITES (mapeamento explícito)
        2. ANTONYM_PATTERNS (análise semântica do nome)
        3. HIERARCHICAL_OPPOSITES (posição no grafo)
        4. DOMAIN_OPPOSITES (regras de domínio)
        5. Análise posicional (nós distantes no grafo)

        Args:
            cell_data: Dicionário da célula N4
            registry: Dicionário de todas as células {uid: data}

        Returns:
            Lista de UIDs das células opostas
        """
        uid = cell_data.get("uid", "")

        # Verificar cache
        if uid in self._opposites_cache:
            return self._opposites_cache[uid]

        opposites: list[str] = []
        seen: set[str] = set()

        # --- Camada 1: Mapeamento explícito ---
        explicit = self.KNOWN_OPPOSITES.get(uid)
        if explicit:
            opposites.append(explicit)
            seen.add(explicit)

        # --- Camada 2: Antônimos semânticos ---
        nome_norm = cell_data.get("nome_normalizado", "").lower()
        nome = cell_data.get("nome", "").lower()
        search_terms = [nome_norm, nome]

        for term in search_terms:
            for ant_key, ant_val in self.ANTONYM_PATTERNS.items():
                if ant_key in term:
                    # Procurar célula cujo nome contenha o antônimo
                    if registry:
                        for cand_uid, cand_data in registry.items():
                            if cand_uid == uid:
                                continue
                            cand_nome = cand_data.get("nome_normalizado", "").lower()
                            cand_nome_raw = cand_data.get("nome", "").lower()
                            if ant_val in cand_nome or ant_val in cand_nome_raw:
                                if cand_uid not in seen:
                                    opposites.append(cand_uid)
                                    seen.add(cand_uid)

        # --- Camada 3: Hierarquia ---
        n3_name = cell_data.get("n3_name", "").upper()
        hier_opp = self.HIERARCHICAL_OPPOSITES.get(n3_name, "")
        if hier_opp and registry:
            dominio = cell_data.get("dominio", "")
            pilar = cell_data.get("pilar", "")
            # Procurar célula com mesmo domínio/pilar mas subárvore oposta
            for cand_uid, cand_data in registry.items():
                if cand_uid == uid:
                    continue
                if (cand_data.get("dominio") == dominio and
                    cand_data.get("pilar") == pilar and
                    cand_data.get("n3_name", "").upper() == hier_opp):
                    if cand_uid not in seen:
                        opposites.append(cand_uid)
                        seen.add(cand_uid)

        # --- Camada 4: Regras de domínio ---
        dominio = cell_data.get("dominio", "")
        domain_rules = self.DOMAIN_OPPOSITES.get(dominio, [])
        if registry:
            for term_a, term_b in domain_rules:
                # Verificar se a célula atual matcha term_a
                match_a = term_a.lower() in nome_norm or term_a.lower() in nome
                if match_a:
                    for cand_uid, cand_data in registry.items():
                        if cand_uid == uid or cand_uid in seen:
                            continue
                        cand_nome = cand_data.get("nome_normalizado", "").lower()
                        cand_nome_raw = cand_data.get("nome", "").lower()
                        if term_b.lower() in cand_nome or term_b.lower() in cand_nome_raw:
                            opposites.append(cand_uid)
                            seen.add(cand_uid)

        # --- Camada 5: Análise posicional (nós mais distantes) ---
        if registry and len(opposites) < 3:
            distant = self._find_distant_cells(cell_data, registry)
            for d_uid in distant:
                if d_uid not in seen and d_uid != uid:
                    opposites.append(d_uid)
                    seen.add(d_uid)
                    if len(opposites) >= 3:
                        break

        self._opposites_cache[uid] = opposites
        return opposites

    def _find_distant_cells(self, cell_data: dict, registry: dict,
                            top_n: int = 5) -> list[str]:
        """
        Encontrar células mais distantes no grafo (baseado em relações).

        Células com pouca ou nenhuma conexão direta são potenciais opostos.
        """
        uid = cell_data.get("uid", "")
        pilar = cell_data.get("pilar", "")
        dominio = cell_data.get("dominio", "")
        axis = cell_data.get("axis", "")

        # Células do eixo oposto e domínio/pilar diferente são candidatas
        opposite_axis = "ENTRÓPICO" if axis == "SINTRÓPICO" else "SINTRÓPICO"

        candidates = []
        for cand_uid, cand_data in registry.items():
            if cand_uid == uid:
                continue
            # Preferir: eixo oposto + domínio diferente
            score = 0
            if cand_data.get("axis") == opposite_axis:
                score += 3
            if cand_data.get("dominio") != dominio:
                score += 2
            if cand_data.get("pilar") != pilar:
                score += 1
            # Verificar se não há relação direta
            relacoes = cell_data.get("relacoes", [])
            is_related = any(r.get("alvo") == cand_uid for r in relacoes)
            if not is_related:
                score += 2
            candidates.append((cand_uid, score))

        candidates.sort(key=lambda x: -x[1])
        return [uid for uid, _ in candidates[:top_n]]

    def build_tension_map(self, registry: Optional[dict] = None) -> dict:
        """
        Constrói mapa de tensões dialéticas entre todas as células.

        Retorna dicionário {uid: {"opposites": [...], "tension_score": float}}
        """
        if not registry:
            registry = self._load_registry()

        tension_map = {}
        for uid, cell_data in registry.items():
            if uid == "ontology_index.json":
                continue
            opposites = self.infer_opposites(cell_data, registry)
            tension = self.calculate_tension_score(cell_data, opposites, registry)
            tension_map[uid] = {
                "opposites": opposites,
                "tension_score": tension,
                "n_opposites": len(opposites),
            }

        self._tension_map_cache = tension_map
        return tension_map

    def calculate_tension_score(self, cell_data: dict,
                                opposites: list[str],
                                registry: Optional[dict] = None) -> float:
        """
        Calcula score de tensão dialética (0.0-1.0).

        Baseado em:
        - Número de opostos identificados
        - Distância semântica entre a célula e seus opostos
        - Força das relações no grafo
        """
        if not opposites:
            return 0.0

        score = min(len(opposites) / 3.0, 1.0)  # Normaliza: 3+ opostos = 1.0

        # Ajustar por complementaridade de eixo
        axis = cell_data.get("axis", "")
        if registry:
            axis_opp_count = 0
            for opp_uid in opposites:
                opp_data = registry.get(opp_uid, {})
                if opp_data.get("axis") != axis:
                    axis_opp_count += 1
            if axis_opp_count > 0:
                score += 0.1 * (axis_opp_count / len(opposites))

        return min(round(score, 3), 1.0)

    def calculate_dialectic_distance(self, cell_a_uid: str,
                                      cell_b_uid: str,
                                      registry: Optional[dict] = None) -> float:
        """
        Distância dialética entre duas células (0.0-1.0).

        0.0 = idênticas/congruentes
        1.0 = opostas máximas

        Fatores:
        - Similaridade de assinatura semântica
        - Relação explícita no grafo
        - Posição hierárquica
        - Eixo (SINTRÓPICO vs ENTRÓPICO)
        """
        if not registry:
            registry = self._load_registry()

        a_data = registry.get(cell_a_uid, {})
        b_data = registry.get(cell_b_uid, {})

        if not a_data or not b_data:
            return 0.5  # Default para desconhecidas

        distance = 0.0
        weights_sum = 0.0

        # 1. Eixo (peso 0.3)
        if a_data.get("axis") != b_data.get("axis"):
            distance += 0.3
        weights_sum += 0.3

        # 2. Pilar (peso 0.2)
        if a_data.get("pilar") != b_data.get("pilar"):
            distance += 0.2
        weights_sum += 0.2

        # 3. Domínio (peso 0.15)
        if a_data.get("dominio") != b_data.get("dominio"):
            distance += 0.15
        weights_sum += 0.15

        # 4. Natureza (peso 0.1)
        if a_data.get("natureza") != b_data.get("natureza"):
            distance += 0.1
        weights_sum += 0.1

        # 5. Nome (peso 0.15) — nomes muito diferentes = mais distantes
        nome_a = a_data.get("nome_normalizado", "").lower()
        nome_b = b_data.get("nome_normalizado", "").lower()
        if nome_a and nome_b:
            common = len(set(nome_a.split()) & set(nome_b.split()))
            total = max(len(set(nome_a.split()) | set(nome_b.split())), 1)
            name_sim = common / total
            distance += (1 - name_sim) * 0.15
        weights_sum += 0.15

        # 6. Relação direta (peso 0.1) — se são relacionadas, distância menor
        relacoes_a = a_data.get("relacoes", [])
        is_related = any(r.get("alvo") == cell_b_uid for r in relacoes_a)
        relacoes_b = b_data.get("relacoes", [])
        is_related |= any(r.get("alvo") == cell_a_uid for r in relacoes_b)
        if is_related:
            distance -= 0.1  # Reduz distância
        weights_sum += 0.1

        # Normalizar
        if weights_sum > 0:
            distance = distance / weights_sum

        # Verificar se são opostos conhecidos
        if cell_b_uid in self.KNOWN_OPPOSITES.get(cell_a_uid, []):
            distance = max(distance, 0.8)
        if cell_a_uid in self.KNOWN_OPPOSITES.get(cell_b_uid, []):
            distance = max(distance, 0.8)

        return round(max(0.0, min(1.0, distance)), 4)

    def _load_registry(self) -> dict:
        """Carrega registry a partir do índice ontológico."""
        import json, os
        idx_path = "data/json/ontology_index.json"
        if os.path.exists(idx_path):
            with open(idx_path) as f:
                return json.load(f).get("id_mapping", {})
        return {}
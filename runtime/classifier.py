#!/usr/bin/env python3
"""Classificador Ontológico Multinível N0→N4 para o pipeline cognitivo.

Implementa classificação em cascata com fusão de sinais léxicos (keywords)
e semânticos (embeddings), determinando automaticamente a posição de uma
query do usuário na ontologia fractal de 162 células.

Dependências:
  - FASE 1 (JSONs enriquecidos em data/json/)
  - FASE 4 (embeddings 384-dim em data/embeddings/)
  - sentence-transformers (recomendado) ou fallback TF-IDF
  - numpy
"""

from __future__ import annotations

import json
import logging
import os
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Utilitário de normalização Unicode
# ---------------------------------------------------------------------------

def _normalize_key(s: str) -> str:
    """Normaliza string: lowercase, remove acentos/diacríticos, strip."""
    nfkd = unicodedata.normalize("NFD", s.lower().strip())
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------
# Mapeamentos ontológicos estáticos — derivados de ARQUITETO_PROMPTS_FINAL.md
# ---------------------------------------------------------------------------

# N0 → Eixo: keywords que indicam intenção sintrópica ou entrópica
N0_AXIS_KEYWORDS: dict[str, list[str]] = {
    "SINTRÓPICO": [
        "como", "fazer", "resolver", "criar", "construir", "executar",
        "implementar", "produzir", "organizar", "definir", "clarificar",
        "analisar", "resolucao", "otimizar", "validar", "estrutura",
        "processo", "algoritmo", "sistema", "logica", "regra", "ordem",
        "mecanismo", "funcao", "calculo", "dados", "modelo", "projeto",
        "plano", "passo", "sequencia", "decisao", "acao", "resultado",
        "implementacao", "construcao", "desenvolvimento", "engenharia",
        "arquitetura", "design", "configuracao", "receita", "procedimento",
        "metodo", "tecnica", "ferramenta", "framework", "pipeline",
        "workflow", "automatizar", "script", "codigo", "programa",
        "montar", "planejar", "estruturar", "configurar", "ajustar",
        "padronizar", "documentar", "mapear", "modelar", "diagramar",
    ],
    "ENTRÓPICO": [
        "o que e", "o que eh", "explorar", "descobrir", "entender",
        "investigar", "questionar", "imaginar", "possibilidades",
        "alternativas", "potencial", "hipotese", "teoria", "conceito",
        "essencia", "natureza", "significado", "origem", "causa", "raiz",
        "contexto", "perspectiva", "visao", "exploracao", "descoberta",
        "inovacao", "criatividade", "abstracao", "filosofia", "cosmos",
        "universo", "infinito", "transcendencia", "mistico", "simbolo",
        "narrativa", "mito", "arquetipo", "imaginario", "sonho",
        "intuicao", "inspiracao", "emergencia", "complexidade",
        "quais sao", "qual e a natureza", "como entender",
        "compreender", "desvendar", "por que", "porque",
        "existencia", "realidade", "consciencia", "paradoxo",
        "misterio", "desconhecido", "fronteira", "transformar",
        "evoluir", "mudanca", "abertura", "expansao",
    ],
}

# N1 → Pilares disponíveis por eixo
N1_PILAR_BY_AXIS: dict[str, list[str]] = {
    "SINTRÓPICO": ["LOGOS", "BIOS", "PATHOS"],
    "ENTRÓPICO": ["KHAOS", "APEIRON", "MYTHOS"],
}

# N1 → Keywords por pilar (todos normalizados sem acento para matching)
N1_PILAR_KEYWORDS: dict[str, list[str]] = {
    "LOGOS": [
        "sistema", "logica", "estrutura", "processo", "algoritmo",
        "regra", "ordem", "organizacao", "mecanismo", "funcao",
        "calculo", "analise", "dados", "modelo", "arquitetura",
        "engenharia", "software", "codigo", "programacao", "computacao",
        "formal", "matematica", "deducao", "prova", "teorema",
        "booleano", "verdade", "consistencia", "rigor", "protocolo",
        "interface", "abstracao", "modular", "escalavel",
    ],
    "BIOS": [
        "vida", "organismo", "sustentabilidade", "integridade",
        "ecossistema", "biologia", "saude", "energia", "metabolismo",
        "ciclo", "crescimento", "adaptacao", "homeostase", "organico",
        "natural", "biologico", "celular", "molecular", "genetico",
        "ecologia", "ambiental", "nutricao", "regeneracao", "curar",
        "preservar", "vital", "vivo", "morte", "nascimento",
        "habitat", "biodiversidade", "evolucao", "simbiose",
        "morada", "territorio", "provisao", "recurso", "habitar",
    ],
    "PATHOS": [
        "emocional", "relacao", "conexao", "valores", "significado",
        "empatia", "comunicacao", "dialogo", "impacto", "harmonia",
        "estetica", "expressao", "reconhecimento", "dignidade",
        "etica", "moral", "justica", "responsabilidade", "cuidado",
        "amor", "comunidade", "social", "cultural", "identidade",
        "subjetivo", "pessoal", "experiencia", "sentimento", "afeto",
        "vulnerabilidade", "compaixao", "solidariedade",
    ],
    "KHAOS": [
        "transformacao", "ruptura", "inovacao", "criatividade",
        "destruicao", "reconstrucao", "emergencia", "complexidade",
        "adaptacao", "evolucao", "revolucao", "transicao", "crise",
        "colapso", "desordem", "caos", "disrupcao", "mudanca",
        "imprevisto", "aleatorio", "turbulento", "dinamico",
        "agencia", "liberdade", "potencial", "novo", "emergente",
        "antifragil", "resiliencia", "pivote",
    ],
    "APEIRON": [
        "escala", "transcendencia", "infinito", "cosmos",
        "abstracao", "universal", "sistemico", "estrategico",
        "visao", "perspectiva", "arquitetura", "design",
        "magnifico", "grande", "vasto", "eterno", "atemporal",
        "meta", "proposito", "direcao", "horizonte", "fronteira",
        "limiar", "portal", "vacuo", "campo",
        "ressonancia", "frequencia", "onda", "ciclo", "lei",
        "arquetipico", "holistico", "sistemico",
    ],
    "MYTHOS": [
        "narrativa", "historia", "mito", "simbolo", "arquetipo",
        "sabedoria", "tradicao", "cultura", "identidade", "coletivo",
        "imaginario", "sonho", "lenda", "fabula", "parabola",
        "ritual", "mistico", "sagrado", "heroico", "epico",
        "memoria", "ancestral", "origem", "cosmogonio", "mitologia",
        "reconhecimento", "intuicao", "revelacao", "misterio",
        "mitologico", "simbolico",
    ],
}

# N2 → Domínios por pilar
N2_DOMAINS_BY_PILAR: dict[str, list[str]] = {
    "LOGOS": ["ALGORITMIA", "NOMOS", "MECANICA"],
    "BIOS": ["OIKOS", "SOMA", "METABOLISMO"],
    "PATHOS": ["ETHOS", "ALTERIDADE", "ESTETICA"],
    "KHAOS": ["ENTROPIA", "SINGULARIDADE", "SINTESE"],
    "APEIRON": ["ESCALA", "VIBRATIO", "VACUO"],
    "MYTHOS": ["ARQUETIPO", "NARRATIVA", "MISTERIO"],
}

# N2 → Keywords estáticas por domínio (discriminativas)
N2_DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "ALGORITMIA": [
        "algoritmo", "algoritmos", "programacao", "programar", "codigo",
        "computacao", "dados", "estrutura", "logica", "funcao",
        "complexidade", "busca", "ordenacao", "classificacao",
        "machine learning", "rede neural", "heuristica", "otimizacao",
        "resolucao", "validacao", "depuracao", "teste",
    ],
    "NOMOS": [
        "lei", "norma", "regra", "juridico", "legislacao",
        "regulamento", "contrato", "direito", "justica", "legal",
        "constituicao", "civil", "penal", "tributario", "administrativo",
    ],
    "MECANICA": [
        "forca", "movimento", "energia", "fisica", "newton",
        "cinetica", "potencial", "trabalho", "velocidade",
        "aceleracao", "massa", "gravidade", "dinamica", "estatica",
        "termica", "fluidos", "pressao", "torque",
    ],
    "OIKOS": [
        "morada", "casa", "habitar", "territorio", "espaco",
        "habitacao", "sustentavel", "ecologico", "recurso natural",
        "biodiversidade", "conservacao", "ambiental",
    ],
    "SOMA": [
        "corpo", "saude", "organismo", "biologico", "celular",
        "integridade", "vitalidade", "homeostase", "metabolismo",
        "nutricao", "curar", "regeneracao", "envelhecimento",
    ],
    "METABOLISMO": [
        "metabolismo", "anabolismo", "catabolismo", "energia",
        "transformacao", "ciclo", "nutriente", "bioquimica",
        "respiracao", "fotosintese", "digestao", "ATP",
    ],
    "ETHOS": [
        "valor", "etica", "moral", "virtude", "carater",
        "principio", "norma etica", "deve", "correto", "justo",
        "responsabilidade", "dignidade", "integridade moral",
    ],
    "ALTERIDADE": [
        "alteridade", "outro", "diferente", "diversidade",
        "inclusao", "empatia", "reconhecimento", "identidade",
        "cultural", "social", "comunicacao", "dialogo",
    ],
    "ESTETICA": [
        "estetica", "beleza", "harmonia", "arte", "forma",
        "expressao", "criativo", "artistico", "sensorial",
        "visual", "sonoro", "composicao", "estilo",
    ],
    "ENTROPIA": [
        "entropia", "degradacao", "dissipacao", "desordem",
        "caos", "desorganizacao", "perda", "dispersao",
        "irreversivel", "aleatorio", "termodinamica",
    ],
    "SINGULARIDADE": [
        "singularidade", "excecao", "infinito", "transformacao",
        "innovacao radical", "ruptura", "emergente", "ponto de inflexao",
        "transcendencia", "limiar",
    ],
    "SINTESE": [
        "sintese", "fusao", "hibridismo", "transcendencia",
        "combinacao", "integracao", "unificacao", "holistico",
        "convergencia", "novo paradigma",
    ],
    "ESCALA": [
        "escala", "proporcao", "magnitude", "medida",
        "grandeza", "dimensoes", "cosmico", "micro", "macro",
        "proporcional", "aurea", "isomorfismo",
    ],
    "VIBRATIO": [
        "vibracao", "frequencia", "ressonancia", "onda",
        "sonoro", "ritmo", "ciclo", "oscilacao",
        "acustico", "harmonia", "nota musical",
    ],
    "VACUO": [
        "vacuo", "potencial", "silencio", "campo",
        "vazio", "latente", "capacidade", "possibilidade",
        "espaco vazio", "nada", "plenitude",
    ],
    "ARQUETIPO": [
        "arquetipo", "padrao primordial", "simbolo", "comportamento",
        "inconsciente coletivo", "jung", "heroi", "sombra",
        "anima", "animus", "self",
    ],
    "NARRATIVA": [
        "narrativa", "historia", "teia", "fio", "sentido",
        "trama", "enredo", "personagem", "mito", "lenda",
        "memoria", "experiencia vivida",
    ],
    "MISTERIO": [
        "misterio", "incompreensao", "intuicao", "revelacao",
        "oculto", "enigma", "paradoxo", "sagrado",
        "desvelamento", "iluminacao", "gnose",
    ],
}

# N3 → Subárvores por domínio
# Chaves normalizadas (sem acento, uppercase) para compatibilidade com n3_name do registry
N3_SUBTREES_BY_DOMAIN: dict[str, list[str]] = {
    "ALGORITMIA": ["RESOLUCAO", "OTIMIZACAO", "VALIDACAO"],
    "NOMOS": ["LEGISLACAO", "CONTORNO", "PACTO"],
    "MECANICA": ["ESTATICA", "DINAMICA", "TERMOTRANSDINAMICA"],
    "OIKOS": ["MORADA", "TERRITORIO", "PROVISAO"],
    "SOMA": ["INTEGRIDADE", "VITALIDADE", "HOMEOSTASE"],
    "METABOLISMO": ["ANABOLISMO", "CATABOLISMO", "CICLO"],
    "ETHOS": ["VALORES", "VIRTUDE", "RESPONSABILIDADE"],
    "ALTERIDADE": ["RECONHECIMENTO", "EMPATIA", "DIALOGO"],
    "ESTETICA": ["HARMONIA", "EXPRESSAO", "IMPACTO"],
    "ENTROPIA": ["DEGRADACAO", "DISSIPACAO", "CAOS"],
    "SINGULARIDADE": ["EXCEPCAO", "INFINITO", "TRANSFORMACAO"],
    "SINTESE": ["FUSAO", "HIBRIDISMO", "TRANSCENDENCIA"],
    "ESCALA": ["PROPORCAO", "MAGNITUDE", "LEI"],
    "VIBRATIO": ["FREQUENCIA", "RESSONANCIA", "ONDA"],
    "VACUO": ["POTENCIAL", "SILENCIO", "CAMPO"],
    "ARQUETIPO": ["PADRAO_PRIMORDIAL", "COMPORTAMENTO", "SIMBOLO"],
    "NARRATIVA": ["TEIA", "LINHA_SENTIDO", "HISTORIA_VIVIDA"],
    "MISTERIO": ["INCOMPREENSAO", "INTUICAO", "REVELACAO"],
}

# N3 → Keywords discriminativas por subárvore (evitar sobreposição)
N3_SUBTREE_KEYWORDS: dict[str, list[str]] = {
    "RESOLUCAO": ["decompor", "resolver", "sequenciar", "validar", "passo", "recursivo", "binario", "metade"],
    "OTIMIZACAO": ["otimizar", "eficiente", "desempenho", "melhorar", "rapido", "rapidez", "custo", "minimizar", "maximizar"],
    "VALIDACAO": ["validar", "verificar", "prova", "correto", "teste", "confianca", "certeza", "garantia"],
    "MORADA": ["morada", "protecao", "recurso", "saneamento", "abrigo", "lar", "habitar", "casa"],
    "TERRITORIO": ["territorio", "habitar", "espaco", "dominio", "fronteira", "borda", "regiao", "lugar"],
    "PROVISAO": ["provisao", "suprir", "sustentar", "reserva", "estoque", "armazenar", "suprimento"],
    "INTEGRIDADE": ["integridade", "integro", "saudavel", "funcional", "inteiro", "completo", "incolme"],
    "VITALIDADE": ["vital", "energia", "vivo", "dinamismo", "vigor", "forca vital", "animado"],
    "HOMEOSTASE": ["homeostase", "equilibrio", "estavel", "regulacao", "equilibrar", "estabilizar"],
    "DEGRADACAO": ["degradacao", "desgaste", "erosao", "deterioracao", "desintegrar", "corromper"],
    "DISSIPACAO": ["dissipacao", "dispersao", "perda", "dispersar", "dissolver", "espalhar"],
    "CAOS": ["caos", "desordem", "aleatorio", "turbulento", "desorganizado", "erratico"],
    "LEGISLACAO": ["legislacao", "lei", "regra", "juridico", "legal", "norma", "codigo"],
    "CONTORNO": ["contorno", "limite", "fronteira", "restricao", "cerca", "margem", "perimetro"],
    "PACTO": ["pacto", "acordo", "contrato", "alianca", "pactuar", "compromisso", "tratado"],
    "ESTATICA": ["estatica", "equilibrio", "forca", "repouso", "imobilidade", "parado", "sem movimento"],
    "DINAMICA": ["dinamica", "movimento", "forca", "aceleracao", "cinetica", "em movimento", "variacao"],
    "TERMOTRANSDINAMICA": ["termodinamica", "calor", "entropia", "energia", "temperatura", "termico", "transferencia calor"],
    "ALTERIDADE": ["alteridade", "reconhecer", "empatia", "dialogo", "outro", "diferente", "altero"],
    "ETHOS": ["valor", "etica", "moral", "virtude", "principio", "carater", "deve", "correto"],
    "ESTETICA_SUB": ["estetica", "beleza", "harmonia", "expressao", "arte", "forma", "criativo"],
    "SINGULARIDADE": ["singularidade", "excecao", "infinito", "transformacao", "ruptura", "incomum", "exclusivo"],
    "SINTESE": ["sintese", "fusao", "hibridismo", "transcendencia", "combinacao", "unificacao", "integracao"],
    "PROPORCAO": ["proporcao", "magnitude", "escala", "tamanho", "grandeza", "medida", "relacao"],
    "MAGNITUDE": ["magnitude", "grandeza", "escala", "tamanho", "imensidao", "enorme", "vasto"],
    "LEI": ["lei", "regra", "norma", "universal", "imutavel", "absoluto", "cosmico"],
    "FREQUENCIA": ["frequencia", "ritmo", "ciclo", "repeticao", "oscilacao", "periodico", "onda"],
    "RESSONANCIA": ["ressonancia", "vibracao", "eco", "harmonia", "amplificacao", "sintonia"],
    "ONDA": ["onda", "vibracao", "propagacao", "frequencia", "eletromagnetica", "sonora"],
    "POTENCIAL": ["potencial", "latencia", "capacidade", "possibilidade", "virtual", "nao realizado"],
    "SILENCIO": ["silencio", "pausa", "vazio", "quietude", "calma", "mudez", "ausencia"],
    "CAMPO": ["campo", "espaco", "regiao", "area", "territorio", "ambiente", "dominio"],
    "PADRAO_PRIMORDIAL": ["padrao", "primordial", "reconhecimento", "ativação", "arquetipico", "original", "fundamental", "basico", "inicial", "cosmico"],
    "COMPORTAMENTO": ["comportamento", "habito", "pratica", "acao", "agir", "conduta", "atuacao", "repetitivo", "rotina", "disciplina"],
    "SIMBOLO": ["simbolo", "icone", "totem", "emblema", "representacao", "signo", "imagem"],
    "TEIA": ["teia", "rede", "trama", "conexao", "tecelagem", "urdidura", "ligacao"],
    "LINHA_SENTIDO": ["linha", "sentido", "fio", "narrativa", "conduto", "eixo", "direcao"],
    "HISTORIA_VIVIDA": ["historia", "vivida", "experiencia", "memoria", "pessoal", "biografia", "testemunho"],
    "INCOMPREENSAO": ["incompreensao", "obscuridade", "enigma", "paradoxo", "duvida", "mistério", "confuso"],
    "INTUICAO": ["intuicao", "insight", "inspiracao", "instinto", "pressentimento", "visao interior"],
    "REVELACAO": ["revelacao", "revelar", "descobrir", "iluminacao", "manifestacao", "desvelamento", "apocalipse"],
    "ANABOLISMO": ["anabolismo", "construcao", "sintese", "crescimento", "montar", "formar", "edificar"],
    "CATABOLISMO": ["catabolismo", "degradacao", "quebra", "dissolucao", "destruir", "desmontar", "desintegrar"],
    "CICLO": ["ciclo", "circular", "repeticao", "renovacao", "ritmo", "periodico", "volta"],
    "FUSAO": ["fusao", "uniao", "combinacao", "sintese", "mistura", "fundir", "juncao"],
    "HIBRIDISMO": ["hibridismo", "hibrido", "mistura", "mesticagem", "cruzamento", "misto", "combinado"],
    "TRANSCENDENCIA": ["transcendencia", "transcender", "elevacao", "alem", "superar", "sublimar", "ascender"],
    "MAGNITUDE_SUB": ["magnitude", "grandeza", "escala", "tamanho", "imensidao"],
    "FREQUENCIA_SUB": ["frequencia", "ritmo", "ciclo", "repeticao", "oscilacao"],
    "RESSONANCIA_SUB": ["ressonancia", "vibracao", "eco", "harmonia"],
    "ONDA_SUB": ["onda", "vibracao", "propagacao", "frequencia"],
    "POTENCIAL_SUB": ["potencial", "latencia", "capacidade", "possibilidade"],
    "SILENCIO_SUB": ["silencio", "pausa", "vazio", "quietude"],
    "CAMPO_SUB": ["campo", "espaco", "regiao", "area"],
}


# ---------------------------------------------------------------------------
# Dataclasses de resultado
# ---------------------------------------------------------------------------

@dataclass
class ClassificationResult:
    """Resultado de uma etapa de classificação."""
    level: str                               # n0, n1, n2, n3, n4
    label: str                               # Rótulo humano legível
    code: str                                # Código ontológico
    score: float                             # Score de confiança [0, 1]
    method: str = "hybrid"                   # Método de classificação
    candidates: dict[str, float] = field(default_factory=dict)
    top_cells: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class FullClassification:
    """Classificação completa N0→N4."""
    query: str
    n0: ClassificationResult
    n1: ClassificationResult
    n2: ClassificationResult
    n3: ClassificationResult
    n4: ClassificationResult
    caminho_completo: str
    confianca_media: float
    top_cells: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Classificador principal
# ---------------------------------------------------------------------------

class OntologicalClassifier:
    """Classificador multinível N0→N4 para queries do usuário.

    Percorre a hierarquia ontológica em cascata:
        N0 (Eixo) → N1 (Pilar) → N2 (Domínio) → N3 (Subárvore) → N4 (Célula)

    A cada nível, combina sinais léxicos (keywords) com similaridade
    semântica (embeddings 384-dim) para determinar a posição na ontologia.
    A decisão de cada nível restringe o espaço de busca do seguinte.

    Attributes:
        registry: Dicionário {uid: data} dos 162 JSONs N4 enriquecidos.
        embeddings: Dicionário {uid: np.ndarray(384,)} vetores normalizados.
        threshold: Limiar mínimo de similaridade semântica (default 0.72).
        semantic_weight: Peso do sinal semântico na fusão (default 0.6).
        keyword_weight: Peso do sinal léxico na fusão (default 0.4).
    """

    def __init__(
        self,
        json_dir: str = "data/json",
        embedding_dir: str = "data/embeddings",
        config_path: str = "config/retrieval.yaml",
    ):
        self.registry: dict[str, dict] = {}
        self.embeddings: dict[str, np.ndarray] = {}
        self.threshold = 0.72
        self.semantic_weight = 0.6
        self.keyword_weight = 0.4

        # Modelo de embedding (lazy init)
        self._embed_model: Any = None

        self._load_data(json_dir, embedding_dir)
        self._build_index()

    # ------------------------------------------------------------------
    # Carregamento de dados
    # ------------------------------------------------------------------

    def _load_data(self, json_dir: str, embedding_dir: str) -> None:
        """Carrega registry de JSONs e embeddings .npy."""
        json_path = Path(json_dir)
        emb_path = Path(embedding_dir)

        loaded_json = 0
        if json_path.exists():
            for f in sorted(json_path.glob("N4_*.json")):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        uid = data.get("uid", f.stem)
                        self.registry[uid] = data
                        loaded_json += 1
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning("Erro ao carregar %s: %s", f.name, e)
        logger.info("Registry: %d células N4 carregadas de %s", loaded_json, json_dir)

        loaded_emb = 0
        if emb_path.exists():
            for f in sorted(emb_path.glob("N4_*.npy")):
                uid = f.stem
                try:
                    vec = np.load(f).astype(np.float32)
                    if vec.ndim == 1 and len(vec) == 384:
                        # Garantir normalização L2
                        norm = np.linalg.norm(vec)
                        self.embeddings[uid] = (
                            vec / norm if norm > 1e-8 else vec
                        )
                        loaded_emb += 1
                    else:
                        logger.warning(
                            "Embedding %s com shape inesperado: %s", uid, vec.shape
                        )
                except Exception as e:
                    logger.warning("Erro ao carregar embedding %s: %s", f.name, e)
        logger.info("Embeddings: %d vetores carregados de %s", loaded_emb, embedding_dir)

    def _build_index(self) -> None:
        """Pré-computa índices por nível para busca rápida.

        Todas as chaves são normalizadas (sem acento, uppercase) para
        garantir correspondência com os mapas estáticos.
        """
        self._uid_by_axis: dict[str, list[str]] = {
            "SINTRÓPICO": [], "ENTRÓPICO": []
        }
        self._uid_by_pilar: dict[str, list[str]] = {
            p: [] for p in [
                "LOGOS", "BIOS", "PATHOS", "KHAOS", "APEIRON", "MYTHOS"
            ]
        }
        self._uid_by_dominio: dict[str, list[str]] = {}
        self._uid_by_subarvore: dict[str, list[str]] = {}

        # Mapeamento de normalizado → canônico
        _axis_canon = {
            _normalize_key("SINTRÓPICO"): "SINTRÓPICO",
            _normalize_key("ENTRÓPICO"): "ENTRÓPICO",
        }
        _pilar_canon = {
            _normalize_key(p): p for p in [
                "LOGOS", "BIOS", "PATHOS", "KHAOS", "APEIRON", "MYTHOS"
            ]
        }

        for uid, data in self.registry.items():
            # --- Eixo ---
            axis_raw = data.get("axis", data.get("eixo", ""))
            axis_norm = _normalize_key(axis_raw)
            axis_key = _axis_canon.get(axis_norm, axis_raw)
            if axis_key in self._uid_by_axis:
                self._uid_by_axis[axis_key].append(uid)

            # --- Pilar ---
            pilar_raw = data.get("pilar", "")
            pilar_norm = _normalize_key(pilar_raw)
            pilar_key = _pilar_canon.get(pilar_norm, pilar_raw)
            if pilar_key in self._uid_by_pilar:
                self._uid_by_pilar[pilar_key].append(uid)

            # --- Domínio (normalizado sem acento, uppercase) ---
            dominio_raw = data.get("dominio", "")
            dominio_key = _normalize_key(dominio_raw).upper()
            self._uid_by_dominio.setdefault(dominio_key, []).append(uid)

            # --- Subárvore (normalizada sem acento, uppercase) ---
            subarvore_raw = data.get("n3_name", "")
            subarvore_key = _normalize_key(subarvore_raw).upper()
            self._uid_by_subarvore.setdefault(subarvore_key, []).append(uid)

        logger.info(
            "Índices construídos: %d eixos, %d pilares, %d domínios, %d subárvores",
            len(self._uid_by_axis),
            len(self._uid_by_pilar),
            len(self._uid_by_dominio),
            len(self._uid_by_subarvore),
        )

    # ------------------------------------------------------------------
    # Encoding de query
    # ------------------------------------------------------------------

    def _encode_query(self, query: str) -> Optional[np.ndarray]:
        """Gera embedding para a query via sentence-transformers ou fallback."""
        if self._embed_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._embed_model = SentenceTransformer(
                    "sentence-transformers/all-MiniLM-L6-v2"
                )
                logger.info("Modelo sentence-transformers carregado.")
            except ImportError:
                logger.warning(
                    "sentence-transformers indisponível; usando fallback TF-IDF."
                )
                self._embed_model = False  # type: ignore[assignment]

        if self._embed_model is not False:
            vec = self._embed_model.encode(
                query, normalize_embeddings=True, convert_to_numpy=True
            )
            return vec.astype(np.float32)

        return self._tfidf_encode(query)

    def _tfidf_encode(self, query: str) -> Optional[np.ndarray]:
        """Fallback: TF-IDF simplificado sobre o vocabulário das células."""
        if not self.registry:
            return None

        all_words: dict[str, int] = {}
        doc_freqs: dict[str, int] = {}
        docs: list[dict[str, int]] = []

        for uid, data in self.registry.items():
            text = " ".join([
                data.get("nome_normalizado", ""),
                data.get("gatilho", ""),
                data.get("acao", ""),
                " ".join(data.get("tags", [])),
                " ".join(data.get("funcao_cognitiva", [])),
            ]).lower()
            words = text.split()
            freq: dict[str, int] = {}
            for w in words:
                freq[w] = freq.get(w, 0) + 1
                if w not in all_words:
                    all_words[w] = len(all_words)
                    doc_freqs[w] = 0
            for w in set(words):
                doc_freqs[w] = doc_freqs.get(w, 0) + 1
            docs.append(freq)

        q_words = query.lower().split()
        q_freq: dict[str, int] = {}
        for w in q_words:
            q_freq[w] = q_freq.get(w, 0) + 1

        n_docs = len(docs)
        dim = min(len(all_words), 384)

        scored_words = sorted(
            [(w, c * (np.log((1 + n_docs) / (1 + doc_freqs.get(w, 1))) + 1))
             for w, c in q_freq.items() if w in all_words],
            key=lambda x: -x[1],
        )
        top_words = [w for w, _ in scored_words[:dim]]

        vec = np.zeros(dim, dtype=np.float32)
        word_to_idx = {w: i for i, w in enumerate(top_words)}
        for w, count in q_freq.items():
            if w in word_to_idx:
                idf = np.log((1 + n_docs) / (1 + doc_freqs.get(w, 1))) + 1
                vec[word_to_idx[w]] = count * idf

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    # ------------------------------------------------------------------
    # Similaridade
    # ------------------------------------------------------------------

    def _semantic_similarity(self, query_emb: np.ndarray,
                             cell_uid: str) -> float:
        """Similaridade cosseno entre query e célula (já normalizados)."""
        if cell_uid not in self.embeddings:
            return 0.0
        cell_emb = self.embeddings[cell_uid]
        sim = float(np.dot(query_emb, cell_emb))
        return max(-1.0, min(1.0, sim))

    def _keyword_score(self, query_lower: str, keywords: list[str]) -> float:
        """Score de correspondência por keywords (normalizado [0, 1])."""
        if not keywords:
            return 0.0
        matches = sum(1 for kw in keywords if kw.lower() in query_lower)
        return matches / len(keywords)

    # ------------------------------------------------------------------
    # Classificação por nível
    # ------------------------------------------------------------------

    def classify_n0(self, query: str) -> ClassificationResult:
        """Classifica eixo: SINTRÓPICO vs ENTRÓPICO.

        Método: keywords (60%) + similaridade semântica (40%).
        Peso maior para keywords porque indicadores lexicais como
        "o que é" e "como fazer" são sinais fortes de intenção.
        """
        query_lower = query.lower()

        # Scores de keywords
        sintropico_kw = self._keyword_score(
            query_lower, N0_AXIS_KEYWORDS["SINTRÓPICO"]
        )
        entropico_kw = self._keyword_score(
            query_lower, N0_AXIS_KEYWORDS["ENTRÓPICO"]
        )

        # Scores semânticos
        sintropico_sem = 0.0
        entropico_sem = 0.0
        query_emb = self._encode_query(query)

        if query_emb is not None:
            for uid in self._uid_by_axis.get("SINTRÓPICO", []):
                s = self._semantic_similarity(query_emb, uid)
                if s > sintropico_sem:
                    sintropico_sem = s
            for uid in self._uid_by_axis.get("ENTRÓPICO", []):
                s = self._semantic_similarity(query_emb, uid)
                if s > entropico_sem:
                    entropico_sem = s

        # Fusão: keywords 60%, semântica 40%
        kw_w, sem_w = 0.6, 0.4
        sint_score = kw_w * sintropico_kw + sem_w * sintropico_sem
        ent_score = kw_w * entropico_kw + sem_w * entropico_sem

        if sint_score >= ent_score:
            return ClassificationResult(
                level="n0", label="SINTRÓPICO", code="S1",
                score=round(sint_score, 4),
                candidates={
                    "SINTRÓPICO": round(sint_score, 4),
                    "ENTRÓPICO": round(ent_score, 4),
                },
            )
        else:
            return ClassificationResult(
                level="n0", label="ENTRÓPICO", code="E2",
                score=round(ent_score, 4),
                candidates={
                    "SINTRÓPICO": round(sint_score, 4),
                    "ENTRÓPICO": round(ent_score, 4),
                },
            )

    def classify_n1(self, query: str,
                    n0: ClassificationResult) -> ClassificationResult:
        """Classifica pilar dentro do eixo determinado."""
        axis = n0.label
        query_lower = query.lower()

        candidatos = N1_PILAR_BY_AXIS.get(axis, [])
        scores: dict[str, float] = {}

        query_emb = self._encode_query(query)

        for pilar in candidatos:
            kw_score = self._keyword_score(
                query_lower, N1_PILAR_KEYWORDS.get(pilar, [])
            )
            pilar_uids = self._uid_by_pilar.get(pilar, [])
            if query_emb is not None and pilar_uids:
                sem_score = max(
                    self._semantic_similarity(query_emb, uid)
                    for uid in pilar_uids
                )
            else:
                sem_score = 0.0

            scores[pilar] = (
                self.keyword_weight * kw_score
                + self.semantic_weight * sem_score
            )

        best_pilar = max(scores, key=scores.get)  # type: ignore[arg-type]
        return ClassificationResult(
            level="n1", label=best_pilar, code=best_pilar[:1],
            score=round(scores[best_pilar], 4),
            candidates={k: round(v, 4) for k, v in scores.items()},
        )

    def classify_n2(self, query: str,
                    n1: ClassificationResult) -> ClassificationResult:
        """Classifica domínio dentro do pilar.

        Usa combinação de keywords estáticas ricas por domínio
        com similaridade semântica para discriminação precisa.
        """
        pilar = n1.label
        query_lower = query.lower()

        dominios = N2_DOMAINS_BY_PILAR.get(pilar, [])
        scores: dict[str, float] = {}

        query_emb = self._encode_query(query)

        for dominio in dominios:
            domain_cells = self._uid_by_dominio.get(dominio, [])

            # Keywords estáticas ricas do domínio
            domain_kws = N2_DOMAIN_KEYWORDS.get(dominio, [])
            kw_score = self._keyword_score(query_lower, domain_kws)

            # Similaridade semântica
            if query_emb is not None and domain_cells:
                sem_score = max(
                    self._semantic_similarity(query_emb, uid)
                    for uid in domain_cells
                )
            else:
                sem_score = 0.0

            # Peso: 50% keywords, 50% semântica para N2
            scores[dominio] = 0.5 * kw_score + 0.5 * sem_score

        best_dominio = max(scores, key=scores.get)  # type: ignore[arg-type]
        return ClassificationResult(
            level="n2", label=best_dominio, code=best_dominio[:1],
            score=round(scores[best_dominio], 4),
            candidates={k: round(v, 4) for k, v in scores.items()},
        )

    def classify_n3(self, query: str,
                    n2: ClassificationResult) -> ClassificationResult:
        """Classifica subárvore dentro do domínio.

        Usa keywords discriminativas por subárvore combinadas
        com similaridade semântica para resolver ambiguidades
        (ex: PADRAO_PRIMORDIAL vs COMPORTAMENTO).
        """
        dominio = n2.label
        query_lower = query.lower()

        subtrees = N3_SUBTREES_BY_DOMAIN.get(dominio, [])
        scores: dict[str, float] = {}

        query_emb = self._encode_query(query)

        for subarvore in subtrees:
            sub_uids = self._uid_by_subarvore.get(subarvore, [])

            # Keywords estáticas discriminativas
            sub_kws = N3_SUBTREE_KEYWORDS.get(subarvore, [])
            kw_score = self._keyword_score(query_lower, sub_kws)

            # Similaridade semântica
            if query_emb is not None and sub_uids:
                sem_score = max(
                    self._semantic_similarity(query_emb, uid)
                    for uid in sub_uids
                )
            else:
                sem_score = 0.0

            scores[subarvore] = (
                self.keyword_weight * kw_score
                + self.semantic_weight * sem_score
            )

        best_sub = max(scores, key=scores.get)  # type: ignore[arg-type]
        return ClassificationResult(
            level="n3", label=best_sub, code=best_sub,
            score=round(scores[best_sub], 4),
            candidates={k: round(v, 4) for k, v in scores.items()},
        )

    def classify_n4(self, query: str,
                    n3: ClassificationResult) -> ClassificationResult:
        """Classifica célula específica dentro da subárvore.

        Combina similaridade semântica com matching de keywords
        sobre nome, tags, gatilho, funcao_cognitiva e acao.
        """
        subarvore = n3.label
        sub_uids = self._uid_by_subarvore.get(subarvore, [])

        if not sub_uids:
            return ClassificationResult(
                level="n4", label="DESCONHECIDO", code="??", score=0.0,
            )

        query_emb = self._encode_query(query)
        query_lower = query.lower()

        scores: list[tuple[str, float]] = []
        for uid in sub_uids:
            if query_emb is not None:
                sim = self._semantic_similarity(query_emb, uid)
            else:
                sim = 0.0

            data = self.registry.get(uid, {})
            # Keywords ricas: nome, tags, gatilho, acao, funcao_cognitiva
            cell_keywords: list[str] = []
            cell_keywords.append(data.get("nome_normalizado", "").lower())
            cell_keywords.extend(t.lower() for t in data.get("tags", []))
            cell_keywords.append(data.get("gatilho", "").lower())
            cell_keywords.append(data.get("acao", "").lower())
            cell_keywords.extend(w.lower() for w in data.get("funcao_cognitiva", []))

            kw = self._keyword_score(query_lower, cell_keywords)

            final = self.keyword_weight * kw + self.semantic_weight * sim
            scores.append((uid, final))

        scores.sort(key=lambda x: x[1], reverse=True)
        best_uid, best_score = scores[0]

        top3 = [
            {
                "uid": uid,
                "nome": self.registry.get(uid, {}).get("nome", uid),
                "score": round(s, 4),
            }
            for uid, s in scores[:3]
        ]

        best_data = self.registry.get(best_uid, {})
        return ClassificationResult(
            level="n4",
            label=best_data.get("nome", best_uid),
            code=best_uid,
            score=round(best_score, 4),
            candidates={uid: round(s, 4) for uid, s in scores},
            top_cells=top3,
        )

    # ------------------------------------------------------------------
    # Classificação completa
    # ------------------------------------------------------------------

    def full_classify(self, query: str) -> FullClassification:
        """Executa classificação completa N0→N4 em cascata.

        Returns:
            FullClassification com todos os níveis, caminho e scores.
        """
        n0 = self.classify_n0(query)
        n1 = self.classify_n1(query, n0)
        n2 = self.classify_n2(query, n1)
        n3 = self.classify_n3(query, n2)
        n4 = self.classify_n4(query, n3)

        caminho = f"{n0.code}.{n1.label}.{n2.label}.{n3.label}.{n4.label}"

        scores = [n0.score, n1.score, n2.score, n3.score, n4.score]
        confianca_media = round(sum(scores) / len(scores), 4)

        return FullClassification(
            query=query,
            n0=n0,
            n1=n1,
            n2=n2,
            n3=n3,
            n4=n4,
            caminho_completo=caminho,
            confianca_media=confianca_media,
            top_cells=n4.top_cells,
        )

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------

    def warm_up(self) -> None:
        """Pré-carrega o modelo de embedding para evitar latência no 1º uso."""
        if self._embed_model is None or self._embed_model is False:
            self._encode_query("warm-up")

    def get_stats(self) -> dict[str, Any]:
        """Retorna estatísticas do classificador."""
        return {
            "total_cells": len(self.registry),
            "total_embeddings": len(self.embeddings),
            "coverage": round(
                len(self.embeddings) / max(len(self.registry), 1), 4
            ),
            "threshold": self.threshold,
            "semantic_weight": self.semantic_weight,
            "keyword_weight": self.keyword_weight,
            "axes": list(self._uid_by_axis.keys()),
            "pilares": list(self._uid_by_pilar.keys()),
            "dominios": sorted(self._uid_by_dominio.keys()),
            "subarvores": len(self._uid_by_subarvore),
        }
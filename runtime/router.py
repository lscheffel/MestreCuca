"""
ROUTER COGNITIVO — Seleção de módulo cognitivo por pilar ontológico.

Determina qual estratégia de processamento ativar com base na 
classificação ontológica da query.

Fase 6 do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import json
import os


# ── Mapeamento Pilar → Estratégia ──────────────────────────────────

PILLAR_STRATEGIES: Dict[str, dict] = {
    "LOGOS": {
        "nome": "Lógica-Estrutural",
        "descricao": "Processamento analítico, hierárquico e sequencial.",
        "abordagem": "decompor → validar → sequenciar",
        "prompt_template": (
            "Analise a seguinte questão sob a perspectiva lógica-estrutural "
            "da ontologia fractal. Decomponha em premissas, identifique "
            "relações causais e proponha uma sequência de raciocínio "
            "verificável. Utilize os conceitos de: {conceitos}."
        ),
        "tempos": {
            "decomposicao": 0.30,
            "validacao": 0.40,
            "sintese": 0.30,
        },
    },
    "BIOS": {
        "nome": "Orgânico-Vital",
        "descricao": "Processamento cíclico, adaptativo e sustentável.",
        "abordagem": "observar → ciclar → integrar",
        "prompt_template": (
            "Analise a questão sob a perspectiva orgânica da ontologia "
            "fractal. Considere ciclos de vida, interdependências "
            "ecossistêmicas e princípios de homeostase. Utilize os "
            "conceitos de: {conceitos}."
        ),
        "tempos": {
            "decomposicao": 0.25,
            "ciclagem": 0.40,
            "integracao": 0.35,
        },
    },
    "PATHOS": {
        "nome": "Relacional-Significativo",
        "descricao": "Processamento empático, conectivo e valorativo.",
        "abordagem": "escutar → conectar → significar",
        "prompt_template": (
            "Analise a questão sob a perspectiva relacional da ontologia "
            "fractal. Considere dimensões de empatia, comunicação, "
            "reconhecimento e impacto humano. Utilize os conceitos de: "
            "{conceitos}."
        ),
        "tempos": {
            "escuta": 0.35,
            "conexao": 0.35,
            "significacao": 0.30,
        },
    },
    "KHAOS": {
        "nome": "Transformacional-Criativo",
        "descricao": "Processamento disruptivo, emergente e adaptativo.",
        "abordagem": "perturbar → emergir → reconstruir",
        "prompt_template": (
            "Analise a questão sob a perspectiva transformacional da "
            "ontologia fractal. Explore rupturas, emergências e "
            "possibilidades criativas. Utilize os conceitos de: "
            "{conceitos}."
        ),
        "tempos": {
            "perturbacao": 0.30,
            "emergencia": 0.40,
            "reconstrucao": 0.30,
        },
    },
    "APEIRON": {
        "nome": "Estratégico-Transcendente",
        "descricao": "Processamento sistêmico, abstrato e visionário.",
        "abordagem": "escalar → abstrair → transcender",
        "prompt_template": (
            "Analise a questão sob a perspectiva estratégica e "
            "transcendente da ontologia fractal. Considere escalas "
            "multiplas, padrões universais e implicações sistêmicas. "
            "Utilize os conceitos de: {conceitos}."
        ),
        "tempos": {
            "escalamento": 0.30,
            "abstracao": 0.40,
            "transcendencia": 0.30,
        },
    },
    "MYTHOS": {
        "nome": "Narrativo-Simbólico",
        "descricao": "Processamento arquetipal, narrativo e simbólico.",
        "abordagem": "narrar → simbolizar → arquetipar",
        "prompt_template": (
            "Analise a questão sob a perspectiva narrativa e simbólica "
            "da ontologia fractal. Explore arquétipos, metáforas e "
            "padrões narrativos profundos. Utilize os conceitos de: "
            "{conceitos}."
        ),
        "tempos": {
            "narrativa": 0.35,
            "simbolizacao": 0.35,
            "arquetipacao": 0.30,
        },
    },
}

# ── Mapeamento de sinais linguísticos por pilar ────────────────────

PILLAR_SIGNALS: Dict[str, List[str]] = {
    "LOGOS": [
        "sistema", "lógica", "estrutura", "processo", "algoritmo",
        "regra", "ordem", "organização", "mecanismo", "função",
        "cálculo", "análise", "dados", "modelo", "sequência",
        "causalidade", "premissa", "conclusão", "dedução", "lógico",
        "verdadeiro", "falso", "válido", "inconsistente",
    ],
    "BIOS": [
        "vida", "organismo", "sustentabilidade", "integridade",
        "ecossistema", "biologia", "saúde", "energia", "metabolismo",
        "ciclo", "crescimento", "adaptação", "homeostase", "orgânico",
        "vivo", "morte", "renovação", "semente", "raiz", "corpo",
        "nutrição", "respiração", "evolução", "genético",
    ],
    "PATHOS": [
        "emocional", "relação", "conexão", "valores", "significado",
        "empatia", "comunicação", "diálogo", "impacto", "harmonia",
        "estética", "expressão", "reconhecimento", "dignidade",
        "amor", "medo", "alegria", "tristeza", "raiva", "esperança",
        "confiança", "vulnerabilidade", "compaixão", "solidão",
    ],
    "KHAOS": [
        "transformação", "ruptura", "inovação", "criatividade",
        "destruição", "reconstrução", "emergência", "complexidade",
        "adaptação", "evolução", "revolução", "transição", "caos",
        "imprevisto", "disrupção", "mutação", "crisálida", "fênix",
        "labirinto", "paradoxo", "ambivalência",
    ],
    "APEIRON": [
        "escala", "transcendência", "infinito", "cosmos",
        "abstração", "universal", "sistêmico", "estratégico",
        "visão", "perspectiva", "arquitetura", "design",
        "meta", "propósito", "missão", "grande", "total",
        "absoluto", "infinito", "eterno", "arquetípico",
    ],
    "MYTHOS": [
        "narrativa", "história", "mito", "símbolo", "arquétipo",
        "significado", "sabedoria", "tradição", "cultura",
        "identidade", "coletivo", "imaginário", "sonho",
        "místico", "sagrado", "herói", "jornada", "mitologia",
        "lenda", "cosmogonia", "simbolismo", "inconsciente",
    ],
}

# ── Mapeamento de domínio → conceitos-chave ────────────────────────

DOMAIN_CONCEPTS: Dict[str, List[str]] = {
    "ALGORITMIA": ["algoritmo", "dado", "processo", "lógica", "resolução"],
    "NOMOS": ["regra", "lei", "norma", "contrato", "ordem"],
    "MECÂNICA": ["força", "movimento", "equilíbrio", "sistema", "mecanismo"],
    "OIKOS": ["casa", "habitat", "espaço", "morada", "ambiente"],
    "SOMA": ["corpo", "saúde", "energia", "vitalidade", "organismo"],
    "METABOLISMO": ["ciclo", "transformação", "nutrição", "energia", "vida"],
    "ALTERIDADE": ["outro", "diferença", "relação", "diálogo", "encontro"],
    "ESTÉTICA": ["beleza", "forma", "harmonia", "expressão", "arte"],
    "ETHOS": ["valor", "caráter", "virtude", "responsabilidade", "moral"],
    "ENTROPIA": ["desordem", "degradação", "dissipação", "caos", "entropia"],
    "SINGULARIDADE": ["único", "excepcional", "emergente", "novo", "inédito"],
    "SÍNTESE": ["união", "integração", "totalidade", "convergência", "holismo"],
    "ESCALA": ["tamanho", "dimensão", "proporção", "magnificação", "redução"],
    "VIBRATIO": ["frequência", "ressonância", "oscilação", "harmonia", "onda"],
    "VÁCUO": ["vazio", "nada", "potencial", "silêncio", "espaço"],
    "ARQUÉTIPO": ["herói", "mãe", "sombra", "sábio", "traidor"],
    "NARRATIVA": ["história", "conto", "mito", "epopeia", "jornada"],
    "MISTÉRIO": ["oculto", "sagrado", "inefável", "transcendente", "enigma"],
}


@dataclass
class RoutingDecision:
    """Decisão de roteamento cognitivo."""
    pilar: str
    estrategia: str
    dominio: Optional[str] = None
    subarvore: Optional[str] = None
    conceito_foco: Optional[str] = None
    prompt_base: Optional[str] = None
    score: float = 0.0
    confianca: float = 0.0
    metodo: str = "keyword"

    def to_dict(self) -> dict:
        return {
            "pilar": self.pilar,
            "estrategia": self.estrategia,
            "dominio": self.dominio,
            "subarvore": self.subarvore,
            "conceito_foco": self.conceito_foco,
            "prompt_base": self.prompt_base,
            "score": round(self.score, 4),
            "confianca": round(self.confianca, 4),
            "metodo": self.metodo,
        }


class CognitiveRouter:
    """
    Router Cognitivo — Seleciona a estratégia de processamento
    com base na classificação ontológica da query.
    
    Funcionamento:
    1. Recebe classificação N0→N4 do classificador
    2. Analisa sinais linguísticos da query
    3. Determina pilar dominante e estratégia
    4. Gera prompt base para o módulo de síntese
    """

    def __init__(self, config_path: str = "config/retrieval.yaml"):
        self.config = self._load_config(config_path)
        self.threshold = 0.5  # threshold mínimo para sinal de pilar

    def _load_config(self, path: str) -> dict:
        """Carrega configuração YAML."""
        try:
            import yaml
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            return {}
        except FileNotFoundError:
            return {}

    def route(self, classification: dict, query: str = "") -> RoutingDecision:
        """
        Executa roteamento cognitivo.
        
        Args:
            classification: Resultado do classificador (N0→N4)
            query: Query original do usuário
            
        Returns:
            RoutingDecision com estratégia selecionada
        """
        # Extrai classificação
        n0 = classification.get("classificacao", {}).get("n0_eixo", {})
        n1 = classification.get("classificacao", {}).get("n1_pilar", {})
        n2 = classification.get("classificacao", {}).get("n2_dominio", {})
        n3 = classification.get("classificacao", {}).get("n3_subarvore", {})
        n4 = classification.get("classificacao", {}).get("n4_celula", {})

        pilar = n1.get("pilar", "LOGOS")
        dominio = n2.get("dominio", "")
        subarvore = n3.get("subarvore", "")
        celula = n4.get("celula_nome", "")

        # Valida sinais linguísticos
        signal_score = self._validate_signals(query, pilar)
        
        # Verifica consistência entre classificação e sinais
        consistencia = self._check_consistency(classification, query)

        # Se consistência baixa, reavalia
        if consistencia < 0.5 and signal_score > 0.6:
            pilar_reavaliado = self._reavaliate_by_signals(query)
            if pilar_reavaliado:
                pilar = pilar_reavaliado

        # Obtém estratégia do pilar
        estrategia_info = PILLAR_STRATEGIES.get(pilar, PILLAR_STRATEGIES["LOGOS"])
        
        # Gera prompt base
        prompt_base = self._generate_prompt(
            estrategia_info, dominio, subarvore, celula
        )

        # Calcula score final
        score_classificacao = n1.get("score", 0.0)
        score_final = 0.6 * score_classificacao + 0.4 * signal_score

        return RoutingDecision(
            pilar=pilar,
            estrategia=estrategia_info["nome"],
            dominio=dominio,
            subarvore=subarvore,
            conceito_foco=celula,
            prompt_base=prompt_base,
            score=round(score_final, 4),
            confianca=round(min(score_final * 1.2, 1.0), 4),
            metodo="classification+signals",
        )

    def _validate_signals(self, query: str, pilar: str) -> float:
        """Valida sinais linguísticos da query para o pilar dado."""
        if not query:
            return 0.5  # neutro

        query_lower = query.lower()
        signals = PILLAR_SIGNALS.get(pilar, [])
        
        matches = sum(1 for s in signals if s.lower() in query_lower)
        return min(matches / max(len(signals) * 0.3, 1), 1.0)

    def _check_consistency(
        self, classification: dict, query: str
    ) -> float:
        """Verifica consistência entre classificação e conteúdo da query."""
        n0 = classification.get("classificacao", {}).get("n0_eixo", {})
        n1 = classification.get("classificacao", {}).get("n1_pilar", {})
        
        eixo = n0.get("eixo", "")
        pilar = n1.get("pilar", "")
        score_n1 = n1.get("score", 0.5)
        
        # Verifica se sinais da query contradizem a classificação
        signal_score = self._validate_signals(query, pilar)
        
        # Penaliza se sinais contradizem fortemente
        if eixo == "SINTRÓPICO" and signal_score < 0.2:
            return 0.3
        if eixo == "ENTRÓPICO" and signal_score < 0.2:
            return 0.3
        
        return 0.5 + 0.5 * score_n1

    def _reavaliate_by_signals(self, query: str) -> Optional[str]:
        """Reavalia pilar baseado apenas em sinais linguísticos."""
        query_lower = query.lower()
        scores = {}
        
        for pilar, signals in PILLAR_SIGNALS.items():
            matches = sum(1 for s in signals if s.lower() in query_lower)
            scores[pilar] = matches / len(signals)
        
        if not scores:
            return None
        
        best = max(scores.items(), key=lambda x: x[1])
        if best[1] > 0.15:  # threshold mínimo
            return best[0]
        return None

    def _generate_prompt(
        self, estrategia: dict, dominio: str, 
        subarvore: str, celula: str
    ) -> str:
        """Gera prompt base para a estratégia selecionada."""
        # Obtém conceitos do domínio
        conceitos = DOMAIN_CONCEPTS.get(dominio, [])
        conceitos_str = ", ".join(conceitos[:5]) if conceitos else "ontologia fractal"
        
        template = estrategia.get("prompt_template", "")
        prompt = template.format(conceitos=conceitos_str)
        
        # Adiciona contexto específico
        context_parts = []
        if dominio:
            context_parts.append(f"Domínio: {dominio}")
        if subarvore:
            context_parts.append(f"Subárvore: {subarvore}")
        if celula:
            context_parts.append(f"Célula focal: {celula}")
        
        if context_parts:
            prompt += "\n\nContexto ontológico:\n" + "\n".join(context_parts)
        
        return prompt

    def route_simple(self, query: str) -> RoutingDecision:
        """
        Roteamento simplificado — sem classificador prévio.
        Usa apenas sinais linguísticos.
        """
        pilar = self._reavaliate_by_signals(query) or "LOGOS"
        estrategia_info = PILLAR_STRATEGIES.get(pilar, PILLAR_STRATEGIES["LOGOS"])
        
        return RoutingDecision(
            pilar=pilar,
            estrategia=estrategia_info["nome"],
            prompt_base=estrategia_info["prompt_template"].format(
                conceitos="query do usuário"
            ),
            score=0.5,
            confianca=0.4,
            metodo="signals-only",
        )


# ── Utilitário de seleção de agente ────────────────────────────────

def select_agent(pilar: str) -> str:
    """
    Seleciona o agente especializado para o pilar dado.
    
    Retorna nome do agente conforme especificação da FASE 10.
    """
    agent_map = {
        "LOGOS": "classifier_agent",
        "BIOS": "classifier_agent",
        "PATHOS": "synthesis_agent",
        "KHAOS": "dialectic_agent",
        "APEIRON": "graph_agent",
        "MYTHOS": "synthesis_agent",
    }
    return agent_map.get(pilar, "classifier_agent")


def get_pillar_for_axis(axis: str) -> list:
    """Retorna lista de pilares válidos para um dado eixo."""
    axis_map = {
        "SINTRÓPICO": ["LOGOS", "BIOS", "PATHOS"],
        "ENTRÓPICO": ["KHAOS", "APEIRON", "MYTHOS"],
    }
    return axis_map.get(axis, ["LOGOS"])


# ── Ponto de entrada para testes ───────────────────────────────────

if __name__ == "__main__":
    router = CognitiveRouter()
    
    # Teste com classificação simulada
    test_classification = {
        "classificacao": {
            "n0_eixo": {"eixo": "SINTRÓPICO", "codigo": "S1"},
            "n1_pilar": {"pilar": "LOGOS", "score": 0.85},
            "n2_dominio": {"dominio": "ALGORITMIA", "score": 0.78},
            "n3_subarvore": {"subarvore": "RESOLUÇÃO", "score": 0.72},
            "n4_celula": {"celula_nome": "DECOMPOSIÇÃO", "score": 0.91},
        }
    }
    
    result = router.route(
        test_classification,
        "Como decompor um problema complexo em partes menores?"
    )
    print("=== ROUTING RESULT ===")
    print(f"Pilar: {result.pilar}")
    print(f"Estrategia: {result.estrategia}")
    print(f"Score: {result.score}")
    print(f"Prompt base:\n{result.prompt_base}")
"""
Cognitive Function Engine — Inferência de funções cognitivas para células N4.

Taxonomia de funções cognitivas com inferência multi-camada:
  1. Keyword matching no nome, gatilho e ação
  2. Heurística por pilar (LOGOS, BIOS, PATHOS, etc.)
  3. Heurística por domínio temático
  4. Propagação pelo grafo de relações entre células

Produz a lista ordenada de funções cognitivas para cada célula N4.
"""

from __future__ import annotations

from collections import Counter
from typing import Optional


class CognitiveFunctionEngine:
    """Motor de inferência de funções cognitivas para células ontológicas."""

    # 20+ funções cognitivas com keywords associadas
    FUNCTION_KEYWORDS: dict[str, list[str]] = {
        "decompor": [
            "decomposição", "dividir", "quebrar", "fragmentar", "separar",
            "partes", "subproblema", "sub-parte", "fatiar", "segmentar",
            "desmembrar", "dissecar", "analisar",
        ],
        "segmentar": [
            "segmentar", "seccionar", "dividir", "particionar", "agrupar",
            "categorizar", "isolar", "delimitar", "demarcar",
        ],
        "modularizar": [
            "módulo", "independente", "encapsular", "componente", "bloco",
            "modular", "compartimentar", "isolar", "desacoplar",
            "interface", "plugável", "substituição",
        ],
        "classificar": [
            "categoria", "tipo", "classe", "grupo", "tipologia",
            "taxonomia", "hierarquia", "ordenar", "catalogar",
            "rotular", "etiquetar", "agrupar",
        ],
        "hierarquizar": [
            "nível", "camada", "hierarquia", "superior", "subordinado",
            "raiz", "tronco", "folha", "ramo", "árvore",
            "pai", "filho", "ancestral", "descendente",
            "top-down", "bottom-up",
        ],
        "sequenciar": [
            "ordem", "passo", "sequência", "precedência", "depois",
            "primeiro", "segundo", "terceiro", "fluxo", "fila",
            "pipeline", "encadeamento", "encadeado", "serial",
            "temporal", "cronológico",
        ],
        "filtrar": [
            "selecionar", "filtrar", "critério", "limiar", "threshold",
            "filtro", "peneira", "triagem", "priorizar",
            "descartar", "incluir", "excluir", "permitir", "bloquear",
        ],
        "transformar": [
            "mudar", "converter", "transformação", "transmutar", "evoluir",
            "transição", "mudança", "adaptar", "modificar", "alterar",
            "reformular", "reestruturar", "reconfigurar",
            "metamorfose", "mutação",
        ],
        "sintetizar": [
            "combinar", "unir", "integrar", "compor", "fundir", "criar",
            "agregar", "consolidar", "unificar", "harmonizar",
            "montar", "construir", "assemblar", "compor",
        ],
        "avaliar": [
            "avaliar", "julgar", "mensurar", "analisar", "verificar",
            "ponderar", "estimar", "quantificar", "valorar",
            "diagnosticar", "auditar", "inspecionar", "examinar",
        ],
        "validar": [
            "validar", "verificar", "confirmar", "testar", "corrigir",
            "provar", "certificar", "homologar", "atestar",
            "depurar", "debugar", "checar", "revisar",
        ],
        "otimizar": [
            "melhorar", "eficiência", "otimizar", "reduzir", "minimizar",
            "maximizar", "aperfeiçoar", "refinar", "tunar", "calibrar",
            "economizar", "racionalizar", "simplificar", "acelerar",
        ],
        "generalizar": [
            "padrão", "abstrair", "generalizar", "universal", "comum",
            "abstração", "modelo", "arquétipo", "protótipo",
            "canônico", "genérico", "ampliar", "escalar",
        ],
        "especializar": [
            "específico", "caso", "particular", "detalhe", "concreto",
            "instância", "específico", "particularizar", "customizar",
            "adaptar", "contextualizar", "localizar",
        ],
        "mapear": [
            "correspondência", "mapear", "relacionar", "conectar",
            "associar", "vincular", "ligar", "cruzar", "cartografar",
            "navegar", "indexar", "referenciar",
        ],
        "comparar": [
            "comparar", "contrastar", "similar", "diferente", "analogia",
            "semelhança", "diferença", "equivalente", "análogo",
            "paralelo", "convergência", "divergência",
        ],
        "inferir": [
            "deduzir", "concluir", "inferir", "implícito", "pressupor",
            "induzir", "hipotetizar", "supor", "presumir",
            "extrapolar", "interpolar", "conjecturar",
        ],
        "prever": [
            "antecipar", "prever", "projetar", "estimar", "tendência",
            "prospecção", "previsão", "futuro", "prognóstico",
            "extrapolar", "trend",
        ],
        "equilibrar": [
            "equilíbrio", "balancear", "compensar", "ajustar", "harmonizar",
            "homeostase", "estabilizar", "equalizar", "compensar",
            "moderar", "conciliar", "mediação",
        ],
        "resolver": [
            "resolver", "solução", "encontrar", "responder", "concluir",
            "solucionar", "remediar", "corrigir", "fechar", "finalizar",
            "encerrar", "convergir",
        ],
        "controlar": [
            "controlar", "regular", "gerenciar", "monitorar", "ajuste",
            "supervisionar", "administrar", "governar", "direcionar",
            "orquestrar", "coordenar", "conduzir",
        ],
        "regenerar": [
            "regenerar", "renovar", "restaurar", "revitalizar", "recuperar",
            "reconstituir", "ressuscitar", "restabelecer",
        ],
        "dissolver": [
            "dissolver", "desintegrar", "descompor", "desagregar",
            "desmantelar", "desconstruir", "aniquilar",
        ],
        "emergir": [
            "emergir", "surgir", "aparecer", "manifestar", "materializar",
            "nascer", "brota", "eclodir",
        ],
        "adaptar": [
            "adaptar", "ajustar", "acostumar", "adequar", "calibrar",
            "evoluir", "mutação", "plasticidade",
        ],
        "escalar": [
            "escalar", "escala", "ampliar", "expandir", "proporção",
            "redimensionar", "aumentar", "multiplicar",
        ],
        "abstrair": [
            "abstrair", "abstração", "generalizar", "desprender",
            "isolar", "essência", "conceitualizar",
        ],
        "transcender": [
            "transcender", "ultrapassar", "superar", "elevação",
            "transcendência", "ir além",
        ],
        "simbolizar": [
            "simbolizar", "símbolo", "representar", "significar",
            "emblemático", "icônico", "metafórico",
        ],
        "narrar": [
            "narrar", "contar", "história", "relato", "narrativa",
            "descrever", "expor", "reportar",
        ],
        "arquetipar": [
            "arquétipo", "padrão primordial", "original", "modelo",
            "protótipo", "primeiro", "fundamental",
        ],
        "interpretar": [
            "interpretar", "decodificar", "decifrar", "compreender",
            "explicar", "elucidar", "esclarecer",
        ],
    }

    # Funções padrão por pilar — segunda camada de inferência
    PILLAR_DEFAULT_FUNCTIONS: dict[str, list[str]] = {
        "LOGOS": [
            "decompor", "sequenciar", "validar", "otimizar",
            "hierarquizar", "classificar", "controlar",
        ],
        "BIOS": [
            "equilibrar", "transformar", "sintetizar", "regenerar",
            "modularizar", "adaptar", "filtrar",
        ],
        "PATHOS": [
            "classificar", "comparar", "mapear", "inferir", "avaliar",
            "interpretar", "equilibrar",
        ],
        "KHAOS": [
            "transformar", "dissolver", "emergir", "adaptar",
            "descompor", "equilibrar", "prever",
        ],
        "APEIRON": [
            "generalizar", "escalar", "abstrair", "transcender",
            "mapear", "sintetizar", "prever",
        ],
        "MYTHOS": [
            "sintetizar", "simbolizar", "narrar", "arquetipar",
            "interpretar", "classificar", "inferir",
        ],
    }

    # Mapeamento de domínio → funções típicas
    DOMAIN_FUNCTIONS: dict[str, list[str]] = {
        "ALGORITMIA": [
            "decompor", "sequenciar", "validar", "otimizar",
            "classificar", "filtrar", "controlar",
        ],
        "NOMOS": [
            "classificar", "hierarquizar", "validar", "controlar",
            "avaliar", "interpretar",
        ],
        "MECÂNICA": [
            "transformar", "equilibrar", "controlar", "modularizar",
            "simbolizar", "avaliar",
        ],
        "OIKOS": [
            "modularizar", "equilibrar", "proteger", "mapear",
            "adaptar", "filtrar",
        ],
        "SOMA": [
            "equilibrar", "regenerar", "transformar", "validar",
            "monitorar", "controlar",
        ],
        "METABOLISMO": [
            "transformar", "filtrar", "sequenciar", "otimizar",
            "sintetizar", "dissolver",
        ],
        "ETHOS": [
            "classificar", "comparar", "avaliar", "inferir",
            "interpretar", "mapear",
        ],
        "ALTERIDADE": [
            "comparar", "transformar", "adaptar", "mapear",
            "classificar", "inferir",
        ],
        "ESTÉTICA": [
            "comparar", "avaliar", "classificar", "interpretar",
            "simbolizar", "sintetizar",
        ],
        "ENTROPIA": [
            "dissolver", "transformar", "avaliar", "classificar",
            "equilibrar", "otimizar",
        ],
        "SINGULARIDADE": [
            "prever", "inferir", "generalizar", "emergir",
            "avaliar", "transformar",
        ],
        "SÍNTESE": [
            "sintetizar", "generalizar", "integrar", "mapear",
            "abstrair", "classificar",
        ],
        "ESCALA": [
            "escalar", "mapear", "comparar", "generalizar",
            "transformar", "abstrair",
        ],
        "VIBRATIO": [
            "comparar", "equilibrar", "monitorar", "avaliar",
            "classificar", "interpretar",
        ],
        "VÁCUO": [
            "abstrair", "interpretar", "inferir", "generalizar",
            "simbolizar", "meditar",
        ],
        "ARQUÉTIPO": [
            "arquetipar", "simbolizar", "interpretar", "generalizar",
            "narrar", "classificar",
        ],
        "NARRATIVA": [
            "narrar", "interpretar", "conectar", "mapear",
            "classificar", "sintetizar",
        ],
        "MISTÉRIO": [
            "interpretar", "inferir", "simbolizar", "avaliar",
            "prever", "intuir",
        ],
    }

    # Funções especiais para naturezas específicas
    NATURE_FUNCTIONS: dict[str, list[str]] = {
        "processo": ["sequenciar", "controlar", "monitorar", "otimizar"],
        "estado": ["classificar", "avaliar", "monitorar", "equilibrar"],
        "fenomeno": ["interpretar", "inferir", "comparar", "avaliar"],
        "principio": ["generalizar", "abstrair", "inferir", "prever"],
        "mecanismo": ["decompor", "sequenciar", "transformar", "controlar"],
        "estrutura": ["hierarquizar", "modularizar", "classificar", "mapear"],
        "arquétipo": ["arquetipar", "simbolizar", "interpretar", "generalizar"],
        "dinamica": ["transformar", "adaptar", "prever", "equilibrar"],
        "restricao": ["filtrar", "controlar", "validar", "avaliar"],
        "vetor": ["prever", "mapear", "escalar", "orientar"],
    }

    # Todas as funções disponíveis
    ALL_FUNCTIONS = sorted(FUNCTION_KEYWORDS.keys())

    def infer_functions(self, cell_data: dict,
                        registry: Optional[dict] = None) -> list[str]:
        """
        Inferir funções cognitivas para uma célula N4.

        Processo de inferência em 4 camadas:
        1. Keyword matching (nome, gatilho, ação, tags)
        2. Heurística de pilar
        3. Heurística de domínio
        4. Propagação pelo grafo de relações

        Args:
            cell_data: Dicionário da célula N4
            registry: Dicionário de todas as células (opcional)

        Returns:
            Lista ordenada de funções cognitivas com scores
        """
        uid = cell_data.get("uid", "")

        # Scores acumulados para cada função
        function_scores: dict[str, float] = Counter()

        # --- Camada 1: Keyword matching ---
        text_sources = self._extract_text_sources(cell_data)
        for func_name, keywords in self.FUNCTION_KEYWORDS.items():
            for text in text_sources:
                text_lower = text.lower()
                for kw in keywords:
                    if kw.lower() in text_lower:
                        function_scores[func_name] += 1.0
                        break  # Uma keyword basta por fonte

        # --- Camada 2: Heurística de pilar ---
        pilar = cell_data.get("pilar", "")
        pillar_funcs = self.PILLAR_DEFAULT_FUNCTIONS.get(pilar, [])
        for func in pillar_funcs:
            function_scores[func] += 0.8

        # --- Camada 3: Heurística de domínio ---
        dominio = cell_data.get("dominio", "")
        domain_funcs = self.DOMAIN_FUNCTIONS.get(dominio, [])
        for func in domain_funcs:
            function_scores[func] += 0.6

        # --- Camada 3b: Heurística de natureza ---
        natureza = cell_data.get("natureza", "")
        nature_funcs = self.NATURE_FUNCTIONS.get(natureza, [])
        for func in nature_funcs:
            function_scores[func] += 0.5

        # --- Camada 4: Propagação pelo grafo ---
        if registry:
            self._propagate_functions(function_scores, cell_data, registry)

        # Converter para lista ordenada
        scored_functions = [
            {"funcao": f, "score": round(s, 2)}
            for f, s in function_scores.items()
            if s > 0
        ]
        scored_functions.sort(key=lambda x: (-x["score"], x["funcao"]))

        # Retornar apenas nomes (top 5-8), ou todos se poucos
        result = [sf["funcao"] for sf in scored_functions]

        # Garantir pelo menos 1 função
        if not result:
            # Fallback: funções do pilar
            result = pillar_funcs[:3] if pillar_funcs else ["avaliar"]

        # Garantir mínimo de 1 e máximo de 8
        return result[:8]

    def _extract_text_sources(self, cell_data: dict) -> list[str]:
        """Extrai todos os campos textuais relevantes para keyword matching."""
        sources = []

        # Campos diretos
        for field in ["nome", "nome_normalizado", "gatilho", "acao",
                       "restricao", "verificacao"]:
            val = cell_data.get(field, "")
            if val:
                sources.append(str(val))

        # Tags
        tags = cell_data.get("tags", [])
        if tags:
            sources.append(" ".join(tags))

        # Exemplos
        exemplos = cell_data.get("exemplos", [])
        for ex in exemplos:
            if isinstance(ex, dict) and "texto" in ex:
                sources.append(ex["texto"])

        # Analogias
        analogias = cell_data.get("analogias", [])
        for ana in analogias:
            if isinstance(ana, dict) and "texto" in ana:
                sources.append(ana["texto"])

        return sources

    def _propagate_functions(self, scores: dict[str, float],
                             cell_data: dict,
                             registry: dict):
        """
        Propaga funções cognitivas via relações no grafo.

        Células vizinhas (relacionadas) contribuem com funções
        com score reduzido (0.3).
        """
        uid = cell_data.get("uid", "")
        relacoes = cell_data.get("relacoes", [])

        for rel in relacoes:
            alvo_uid = rel.get("alvo", "")
            if not alvo_uid or alvo_uid == uid:
                continue

            alvo_data = registry.get(alvo_uid)
            if not alvo_data:
                continue

            # Inferir funções do vizinho
            vizinho_funcs = self.infer_functions_light(alvo_data)
            peso_rel = rel.get("peso", 0.5)

            for func in vizinho_funcs:
                # Contribuição reduzida pela relação
                scores[func] = scores.get(func, 0) + 0.3 * peso_rel

    def infer_functions_light(self, cell_data: dict) -> list[str]:
        """Versão leve de inferência (sem propagação recursiva)."""
        function_scores: dict[str, float] = Counter()

        text_sources = self._extract_text_sources(cell_data)
        for func_name, keywords in self.FUNCTION_KEYWORDS.items():
            for text in text_sources:
                text_lower = text.lower()
                for kw in keywords:
                    if kw.lower() in text_lower:
                        function_scores[func_name] += 1.0
                        break

        pilar = cell_data.get("pilar", "")
        for func in self.PILLAR_DEFAULT_FUNCTIONS.get(pilar, []):
            function_scores[func] += 0.8

        dominio = cell_data.get("dominio", "")
        for func in self.DOMAIN_FUNCTIONS.get(dominio, []):
            function_scores[func] += 0.6

        natureza = cell_data.get("natureza", "")
        for func in self.NATURE_FUNCTIONS.get(natureza, []):
            function_scores[func] += 0.5

        return sorted(function_scores.keys(),
                      key=lambda f: -function_scores[f])

    def expand_functions(self, functions: list[str],
                         registry: Optional[dict] = None,
                         cell_uid: str = "") -> list[str]:
        """
        Expandir funções com base em células vizinhas no grafo.

        Args:
            functions: Lista de funções já inferidas
            registry: Dicionário de todas as células
            cell_uid: UID da célula atual

        Returns:
            Lista expandida de funções
        """
        if not registry or not cell_uid:
            return functions

        expanded = set(functions)
        cell_data = registry.get(cell_uid, {})
        relacoes = cell_data.get("relacoes", [])

        for rel in relacoes:
            alvo_uid = rel.get("alvo", "")
            alvo_data = registry.get(alvo_uid, {})
            if not alvo_data:
                continue

            alvo_funcs = self.infer_functions_light(alvo_data)
            for func in alvo_funcs:
                if func not in functions:
                    expanded.add(func)

        return sorted(expanded)

    def rank_functions(self, functions: list[str],
                       query_context: Optional[dict] = None) -> list[str]:
        """
        Rankear funções cognitivas por relevância para um contexto.

        Args:
            functions: Lista de funções a rankear
            query_context: Dicionário com contexto da consulta
                {dominio, pilar, natureza, keywords, ...}

        Returns:
            Lista de funções ordenadas por relevância
        """
        if not query_context:
            return functions

        scored = []
        for func in functions:
            score = 0.0
            func_data = self.FUNCTION_KEYWORDS.get(func, [])

            # Match com keywords do contexto
            ctx_keywords = query_context.get("keywords", [])
            for kw in ctx_keywords:
                if kw.lower() in [f.lower() for f in func_data]:
                    score += 2.0

            # Match com domínio
            ctx_dominio = query_context.get("dominio", "")
            domain_funcs = self.DOMAIN_FUNCTIONS.get(ctx_dominio, [])
            if func in domain_funcs:
                score += 1.5

            # Match com pilar
            ctx_pilar = query_context.get("pilar", "")
            pillar_funcs = self.PILLAR_DEFAULT_FUNCTIONS.get(ctx_pilar, [])
            if func in pillar_funcs:
                score += 1.0

            # Match com natureza
            ctx_natureza = query_context.get("natureza", "")
            nature_funcs = self.NATURE_FUNCTIONS.get(ctx_natureza, [])
            if func in nature_funcs:
                score += 0.8

            scored.append((func, score))

        scored.sort(key=lambda x: (-x[1], x[0]))
        return [f for f, _ in scored]

    def get_function_metadata(self, func_name: str) -> dict:
        """Retorna metadados de uma função cognitiva."""
        keywords = self.FUNCTION_KEYWORDS.get(func_name, [])
        return {
            "nome": func_name,
            "keywords": keywords,
            "pilares": [
                p for p, funcs in self.PILLAR_DEFAULT_FUNCTIONS.items()
                if func_name in funcs
            ],
            "dominios": [
                d for d, funcs in self.DOMAIN_FUNCTIONS.items()
                if func_name in funcs
            ],
            "naturezas": [
                n for n, funcs in self.NATURE_FUNCTIONS.items()
                if func_name in funcs
            ],
        }

    def get_all_functions(self) -> list[str]:
        """Retorna lista completa de funções cognitivas."""
        return self.ALL_FUNCTIONS

    def validate_functions(self, functions: list[str]) -> dict:
        """
        Valida lista de funções cognitivas.

        Returns:
            Dict com {valid: bool, errors: list, warnings: list}
        """
        errors = []
        warnings = []

        for func in functions:
            if func not in self.ALL_FUNCTIONS:
                errors.append(f"Função desconhecida: {func}")

        if not functions:
            errors.append("Nenhuma função informada")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }
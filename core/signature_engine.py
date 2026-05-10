"""
Signature Engine — Geração de assinaturas semânticas multidimensionais
para as 162 células N4 da ontologia fractal.

9 dimensões com scoring contínuo [0.0, 1.0]:
  abstracao, complexidade, causalidade, emocionalidade,
  materialidade, simbolismo, dinamismo, temporalidade, ambiguidade

Design: scoring base (natureza) → ajuste por pilar → ajuste por domínio
→ ruído determinístico (seedado por UID) → clamp.
"""

from __future__ import annotations

import hashlib
import math
from typing import Optional


class SignatureEngine:
    """Motor de assinaturas semânticas multidimensionais."""

    DIMENSIONS = [
        "abstracao", "complexidade", "causalidade",
        "emocionalidade", "materialidade", "simbolismo",
        "dinamismo", "temporalidade", "ambiguidade",
    ]

    # Pesos base por natureza — primeira camada de scoring
    NATURE_WEIGHTS: dict[str, dict[str, float]] = {
        "processo": {
            "dinamismo": 0.80, "temporalidade": 0.70,
            "complexidade": 0.60, "causalidade": 0.55,
            "abstracao": 0.30, "materialidade": 0.25,
            "emocionalidade": 0.15, "simbolismo": 0.10,
            "ambiguidade": 0.20,
        },
        "estado": {
            "materialidade": 0.80, "estabilidade": 0.70,
            "abstracao": 0.30, "complexidade": 0.35,
            "causalidade": 0.25, "emocionalidade": 0.20,
            "simbolismo": 0.10, "dinamismo": 0.10,
            "temporalidade": 0.15, "ambiguidade": 0.25,
        },
        "fenomeno": {
            "abstracao": 0.80, "simbolismo": 0.70,
            "ambiguidade": 0.60, "emocionalidade": 0.50,
            "complexidade": 0.55, "causalidade": 0.35,
            "dinamismo": 0.40, "temporalidade": 0.30,
            "materialidade": 0.15,
        },
        "principio": {
            "abstracao": 0.90, "causalidade": 0.80,
            "complexidade": 0.50, "simbolismo": 0.45,
            "temporalidade": 0.35, "dinamismo": 0.25,
            "materialidade": 0.10, "emocionalidade": 0.15,
            "ambiguidade": 0.30,
        },
        "mecanismo": {
            "causalidade": 0.80, "complexidade": 0.70,
            "materialidade": 0.60, "dinamismo": 0.55,
            "abstracao": 0.40, "temporalidade": 0.35,
            "simbolismo": 0.15, "emocionalidade": 0.10,
            "ambiguidade": 0.20,
        },
        "estrutura": {
            "materialidade": 0.80, "complexidade": 0.70,
            "abstracao": 0.50, "causalidade": 0.40,
            "simbolismo": 0.30, "estabilidade": 0.60,
            "dinamismo": 0.15, "temporalidade": 0.20,
            "emocionalidade": 0.10, "ambiguidade": 0.25,
        },
        "arquétipo": {
            "simbolismo": 0.90, "emocionalidade": 0.70,
            "abstracao": 0.80, "ambiguidade": 0.55,
            "complexidade": 0.40, "temporalidade": 0.35,
            "dinamismo": 0.20, "causalidade": 0.25,
            "materialidade": 0.10,
        },
        "dinamica": {
            "dinamismo": 0.90, "temporalidade": 0.80,
            "complexidade": 0.60, "causalidade": 0.50,
            "abstracao": 0.35, "materialidade": 0.30,
            "emocionalidade": 0.25, "simbolismo": 0.20,
            "ambiguidade": 0.30,
        },
        "restricao": {
            "abstracao": 0.60, "complexidade": 0.50,
            "causalidade": 0.70, "materialidade": 0.35,
            "dinamismo": 0.20, "temporalidade": 0.25,
            "emocionalidade": 0.10, "simbolismo": 0.15,
            "ambiguidade": 0.40,
        },
        "vetor": {
            "dinamismo": 0.80, "abstracao": 0.70,
            "complexidade": 0.50, "temporalidade": 0.60,
            "causalidade": 0.45, "materialidade": 0.20,
            "emocionalidade": 0.15, "simbolismo": 0.25,
            "ambiguidade": 0.30,
        },
    }

    # Influência do pilar — segunda camada de ajuste (delta aditivo)
    PILLAR_INFLUENCE: dict[str, dict[str, float]] = {
        "LOGOS": {
            "abstracao": +0.10, "complexidade": +0.08,
            "causalidade": +0.12, "materialidade": -0.05,
            "emocionalidade": -0.10, "simbolismo": -0.05,
            "dinamismo": +0.03, "temporalidade": +0.05,
            "ambiguidade": -0.08,
        },
        "BIOS": {
            "materialidade": +0.12, "emocionalidade": +0.05,
            "dinamismo": +0.08, "abstracao": -0.05,
            "complexidade": +0.03, "causalidade": +0.05,
            "simbolismo": -0.03, "temporalidade": +0.02,
            "ambiguidade": -0.05,
        },
        "PATHOS": {
            "emocionalidade": +0.15, "ambiguidade": +0.08,
            "simbolismo": +0.08, "abstracao": -0.03,
            "complexidade": +0.02, "causalidade": -0.05,
            "materialidade": -0.08, "dinamismo": +0.02,
            "temporalidade": +0.01,
        },
        "KHAOS": {
            "dinamismo": +0.15, "ambiguidade": +0.12,
            "complexidade": +0.08, "abstracao": +0.03,
            "causalidade": -0.05, "materialidade": -0.10,
            "emocionalidade": +0.05, "simbolismo": +0.03,
            "temporalidade": +0.02,
        },
        "APEIRON": {
            "abstracao": +0.15, "complexidade": +0.08,
            "simbolismo": +0.08, "dinamismo": +0.03,
            "temporalidade": +0.05, "causalidade": +0.03,
            "materialidade": -0.10, "emocionalidade": -0.05,
            "ambiguidade": +0.03,
        },
        "MYTHOS": {
            "simbolismo": +0.18, "emocionalidade": +0.10,
            "abstracao": +0.08, "ambiguidade": +0.05,
            "complexidade": +0.03, "temporalidade": +0.05,
            "materialidade": -0.10, "causalidade": -0.05,
            "dinamismo": -0.03,
        },
    }

    # Ajustes específicos por domínio (delta aditivo refinado)
    DOMAIN_INFLUENCE: dict[str, dict[str, float]] = {
        "ALGORITMIA": {
            "abstracao": +0.05, "complexidade": +0.05,
            "causalidade": +0.05, "ambiguidade": -0.05,
        },
        "NOMOS": {
            "causalidade": +0.08, "abstracao": +0.05,
            "ambiguidade": -0.08, "temporalidade": +0.03,
        },
        "MECÂNICA": {
            "materialidade": +0.10, "causalidade": +0.08,
            "complexidade": +0.05, "dinamismo": -0.03,
        },
        "OIKOS": {
            "materialidade": +0.08, "dinamismo": +0.03,
            "emocionalidade": +0.03, "complexidade": -0.03,
        },
        "SOMA": {
            "materialidade": +0.10, "emocionalidade": +0.05,
            "dinamismo": -0.05, "abstracao": -0.05,
        },
        "METABOLISMO": {
            "dinamismo": +0.10, "temporalidade": +0.08,
            "causalidade": +0.05, "complexidade": +0.03,
        },
        "ETHOS": {
            "emocionalidade": +0.08, "ambiguidade": +0.05,
            "complexidade": +0.03, "causalidade": -0.03,
        },
        "ALTERIDADE": {
            "ambiguidade": +0.08, "emocionalidade": +0.05,
            "complexidade": +0.05, "abstracao": +0.03,
        },
        "ESTÉTICA": {
            "emocionalidade": +0.10, "simbolismo": +0.08,
            "ambiguidade": +0.05, "abstracao": +0.03,
        },
        "ENTROPIA": {
            "dinamismo": +0.08, "ambiguidade": +0.08,
            "complexidade": +0.05, "causalidade": +0.05,
            "temporalidade": +0.05,
        },
        "SINGULARIDADE": {
            "abstracao": +0.10, "complexidade": +0.08,
            "simbolismo": +0.05, "temporalidade": +0.05,
        },
        "SÍNTESE": {
            "abstracao": +0.08, "complexidade": +0.05,
            "simbolismo": +0.05, "causalidade": +0.03,
        },
        "ESCALA": {
            "abstracao": +0.08, "complexidade": +0.05,
            "simbolismo": +0.03, "temporalidade": +0.03,
        },
        "VIBRATIO": {
            "dinamismo": +0.08, "temporalidade": +0.08,
            "simbolismo": +0.05, "emocionalidade": +0.03,
        },
        "VÁCUO": {
            "abstracao": +0.10, "ambiguidade": +0.08,
            "simbolismo": +0.05, "emocionalidade": +0.03,
            "materialidade": -0.10,
        },
        "ARQUÉTIPO": {
            "simbolismo": +0.12, "emocionalidade": +0.05,
            "abstracao": +0.05, "ambiguidade": +0.05,
        },
        "NARRATIVA": {
            "temporalidade": +0.10, "simbolismo": +0.05,
            "emocionalidade": +0.05, "complexidade": +0.03,
        },
        "MISTÉRIO": {
            "ambiguidade": +0.12, "simbolismo": +0.08,
            "emocionalidade": +0.05, "abstracao": +0.03,
        },
    }

    # Naturezas que não existem no dataset mas que "estabilidade"
    # é usada como proxy em NATURE_WEIGHTS
    _STABILITY_PROXY = {"estabilidade": 0.70}

    def generate_signature(self, cell_data: dict,
                           seed: Optional[int] = None) -> dict[str, float]:
        """
        Gera assinatura semântica com scores 0.0-1.0 para 9 dimensões.

        Processo:
        1. Base score da natureza da célula
        2. Ajuste pelo pilar
        3. Ajuste pelo domínio
        4. Variação determinística (seedado por UID)
        5. Clamp [0.0, 1.0] e normalização suave

        Args:
            cell_data: Dicionário da célula N4
            seed: Seed para reprodutibilidade (default: derivado do UID)

        Returns:
            Dicionário {dimensão: score} com valores em [0.0, 1.0]
        """
        uid = cell_data.get("uid", "")
        natureza = cell_data.get("natureza", "processo")
        pilar = cell_data.get("pilar", "LOGOS")
        dominio = cell_data.get("dominio", "ALGORITMIA")

        # Seed determinístico baseado no UID
        if seed is None:
            seed = int(hashlib.md5(uid.encode()).hexdigest()[:8], 16)

        rng = self._deterministic_rng(seed)

        # --- Camada 1: Base da natureza ---
        base = dict(self.NATURE_WEIGHTS.get(natureza, self.NATURE_WEIGHTS["processo"]))

        # --- Camada 2: Ajuste por pilar ---
        pillar_adj = self.PILLAR_INFLUENCE.get(pilar, {})
        for dim, delta in pillar_adj.items():
            base[dim] = base.get(dim, 0.5) + delta

        # --- Camada 3: Ajuste por domínio ---
        domain_adj = self.DOMAIN_INFLUENCE.get(dominio, {})
        for dim, delta in domain_adj.items():
            base[dim] = base.get(dim, 0.5) + delta

        # --- Camada 4: Variação determinística (ruído controlado) ---
        signature = {}
        for dim in self.DIMENSIONS:
            raw = base.get(dim, 0.5)

            # Ruído gaussiano-like determinístico (±0.08)
            noise = (next(rng) - 0.5) * 0.16
            value = raw + noise

            # Clamp [0.0, 1.0]
            clamped = max(0.0, min(1.0, value))

            # Arredondar para 3 casas
            signature[dim] = round(clamped, 3)

        # Normalização suave: garantir que a média seja consistente
        # e que nenhuma dimensão fique artificialmente alta/baixa
        signature = self._smooth_normalize(signature)

        return signature

    def _deterministic_rng(self, seed: int):
        """Gerador de números pseudo-aleatórios determinístico (LCG)."""
        a = 1664525
        c = 1013904223
        m = 2**32
        state = seed
        while True:
            state = (a * state + c) % m
            yield state / m

    def _smooth_normalize(self, signature: dict[str, float]) -> dict[str, float]:
        """
        Normalização suave: ajusta valores extremos sem perder diferenciação.
        Aplica sigmoid suave centrada na média.
        """
        values = list(signature.values())
        mean_val = sum(values) / len(values)
        std_val = (sum((v - mean_val) ** 2 for v in values) / len(values)) ** 0.5

        if std_val < 0.01:
            # Pouca variação — adicionar micro-diferenciação
            result = {}
            for i, (dim, val) in enumerate(signature.items()):
                offset = (i % 5 - 2) * 0.02
                result[dim] = round(max(0.0, min(1.0, val + offset)), 3)
            return result

        # Sigmoid suave para comprimir outliers
        result = {}
        for dim, val in signature.items():
            z = (val - mean_val) / (std_val + 0.001)
            # Sigmoid com fator de suavidade
            sigmoid_z = 1 / (1 + math.exp(-0.8 * z))
            # Mapear de volta para [0, 1] mantendo centro
            adjusted = mean_val + (sigmoid_z - 0.5) * 2 * std_val * 1.2
            result[dim] = round(max(0.0, min(1.0, adjusted)), 3)

        return result

    def compare_signatures(self, sig1: dict[str, float],
                           sig2: dict[str, float]) -> float:
        """
        Similaridade cosseno entre duas assinaturas semânticas.

        Args:
            sig1: Primeira assinatura {dimensão: score}
            sig2: Segunda assinatura {dimensão: score}

        Returns:
            Score de similaridade [0.0, 1.0]
        """
        dims = self.DIMENSIONS
        vec1 = [sig1.get(d, 0.0) for d in dims]
        vec2 = [sig2.get(d, 0.0) for d in dims]

        dot = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = sum(a ** 2 for a in vec1) ** 0.5
        mag2 = sum(b ** 2 for b in vec2) ** 0.5

        if mag1 < 1e-10 or mag2 < 1e-10:
            return 0.0

        return round(dot / (mag1 * mag2), 4)

    def cosine_distance(self, sig1: dict[str, float],
                        sig2: dict[str, float]) -> float:
        """Distância cosseno (1 - similaridade)."""
        return round(1.0 - self.compare_signatures(sig1, sig2), 4)

    def cluster_signatures(self, signatures: list[dict],
                           n_clusters: int = 18,
                           max_iter: int = 100) -> dict:
        """
        Clusterização K-Means das assinaturas semânticas.

        Args:
            signatures: Lista de dicionários {uid: signature_dict}
            n_clusters: Número de clusters desejados
            max_iter: Máximo de iterações

        Returns:
            Dicionário {cluster_id: [uids]}
        """
        if not signatures:
            return {}

        dims = self.DIMENSIONS
        n = len(signatures)
        k = min(n_clusters, n)

        # Converter para vetores
        uids = list(signatures.keys())
        vectors = []
        for uid in uids:
            vectors.append([signatures[uid].get(d, 0.0) for d in dims])

        # Inicialização K-Means++
        import random
        random.seed(42)
        centroids = [vectors[random.randint(0, n - 1)][:]]

        for _ in range(1, k):
            distances = []
            for v in vectors:
                min_dist = min(
                    sum((v[j] - c[j]) ** 2 for j in range(len(dims)))
                    for c in centroids
                )
                distances.append(min_dist)
            total = sum(distances)
            if total == 0:
                break
            threshold = random.random() * total
            cumulative = 0
            for i, d in enumerate(distances):
                cumulative += d
                if cumulative >= threshold:
                    centroids.append(vectors[i][:])
                    break

        # Iterações K-Means
        clusters = [0] * n
        for _ in range(max_iter):
            # Atribuição
            new_clusters = []
            for i, v in enumerate(vectors):
                best_c = 0
                best_dist = float('inf')
                for ci, c in enumerate(centroids):
                    dist = sum((v[j] - c[j]) ** 2 for j in range(len(dims)))
                    if dist < best_dist:
                        best_dist = dist
                        best_c = ci
                new_clusters.append(best_c)

            if new_clusters == clusters:
                break
            clusters = new_clusters

            # Atualização
            for ci in range(k):
                members = [vectors[i] for i in range(n) if clusters[i] == ci]
                if members:
                    centroids[ci] = [
                        sum(m[j] for m in members) / len(members)
                        for j in range(len(dims))
                    ]

        # Construir resultado
        result = {}
        for i, uid in enumerate(uids):
            cid = clusters[i]
            if cid not in result:
                result[cid] = []
            result[cid].append(uid)

        return result

    def signature_summary(self, signature: dict[str, float]) -> str:
        """Gera descrição textual resumida da assinatura."""
        dims = self.DIMENSIONS
        sorted_dims = sorted(signature.items(), key=lambda x: -x[1])
        top3 = sorted_dims[:3]
        bottom3 = sorted_dims[-3:]

        top_str = ", ".join(f"{d}({v:.2f})" for d, v in top3)
        bot_str = ", ".join(f"{d}({v:.2f})" for d, v in bottom3)

        return f"Top: [{top_str}] | Low: [{bot_str}]"
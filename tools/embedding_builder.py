#!/usr/bin/env python3
"""Construtor de Embeddings Vetoriais para Células N4.

Gera embeddings multi-perspectiva (estrutural, semântico, operacional, simbólico)
para todas as 162 células N4 usando sentence-transformers, combinando-os em um
vetor ponderado final otimizado para retrieval híbrido.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

import numpy as np
from sentence_transformers import SentenceTransformer

# Adicionar raiz do projeto ao path para imports relativos
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))

from canonical_document_builder import (
    build_canonical_document,
    build_semantic_embedding_text,
    build_structural_embedding_text,
    build_operational_embedding_text,
    build_symbolic_embedding_text,
)


class EmbeddingBuilder:
    """Gera e gerencia embeddings vetoriais para as células N4.

    Carrega os JSONs enriquecidos, gera embeddings multi-camada usando
    sentence-transformers, calcula embeddings combinados ponderados e
    persiste no disco em formato NumPy + índice JSON.

    Attributes:
        config: Configuração carregada do YAML.
        model: Modelo sentence-transformers para encoding.
        embedding_dim: Dimensão dos vetores gerados.
    """

    def __init__(self, config_path: str = "config/embedding.yaml"):
        """Inicializa o construtor de embeddings.

        Args:
            config_path: Caminho para o arquivo de configuração YAML.
        """
        self.config = self._load_config(config_path)
        model_name = self.config.get("modelo", {}).get(
            "nome", "sentence-transformers/all-MiniLM-L6-v2"
        )
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"[EmbeddingBuilder] Modelo '{model_name}' carregado (dimensão: {self.embedding_dim})")

    @staticmethod
    def _load_config(config_path: str) -> dict[str, Any]:
        """Carrega configuração YAML sem dependência rígida do PyYAML.

        Args:
            config_path: Caminho para o arquivo YAML.

        Returns:
            Dicionário com a configuração.
        """
        try:
            import yaml

            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except ImportError:
            # Fallback: parse simples de YAML suficiente para nossa estrutura
            print(f"[EmbeddingBuilder] PyYAML não encontrado, usando config defaults")
            return EmbeddingBuilder._default_config()

    @staticmethod
    def _default_config() -> dict[str, Any]:
        """Retorna configuração padrão quando YAML não está disponível."""
        return {
            "modelo": {"nome": "sentence-transformers/all-MiniLM-L6-v2"},
            "vetores_pesos": {
                "estrutural": 0.30,
                "funcional": 0.25,
                "relacional": 0.20,
                "simbolico": 0.15,
                "temporal": 0.10,
            },
            "contextos": [
                {"nome": "descricao", "campo": "descricao", "peso": 1.0},
                {"nome": "path", "campo": "path", "peso": 0.5},
                {"nome": "tipo", "campo": "tipo", "peso": 0.3},
                {"nome": "relacoes", "campo": "relacoes", "peso": 0.7},
            ],
        }

    def build_all_embeddings(
        self, json_dir: str = "data/json", output_dir: str = "data/embeddings"
    ) -> dict[str, dict]:
        """Gera todos os embeddings e salva em disco.

        Pipeline:
        1. Carrega todos os JSONs N4 do diretório
        2. Gera documentos canônicos para cada célula
        3. Computa embeddings para cada tipo (estrutural, semântico, operacional, simbólico)
        4. Calcula embedding combinado ponderado
        5. Normaliza vetores (L2)
        6. Salva arquivos .npy individuais e índice JSON

        Args:
            json_dir: Diretório com os JSONs enriquecidos N4.
            output_dir: Diretório de saída para embeddings.

        Returns:
            Dicionário com metadados dos embeddings gerados.
        """
        json_path = Path(json_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 1. Carregar JSONs
        json_files = sorted(
            [f for f in json_path.glob("N4_*.json")]
        )
        print(f"[EmbeddingBuilder] Encontrados {len(json_files)} arquivos JSON")

        if not json_files:
            raise FileNotFoundError(f"Nenhum JSON N4 encontrado em {json_dir}")

        # 2. Gerar documentos canônicos
        documents = {}
        for fpath in json_files:
            with open(fpath, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            uid = data.get("uid", fpath.stem)
            documents[uid] = {
                "structural": build_structural_embedding_text(data),
                "semantic": build_semantic_embedding_text(data),
                "operational": build_operational_embedding_text(data),
                "symbolic": build_symbolic_embedding_text(data),
                "canonical": build_canonical_document(data),
            }

        print(f"[EmbeddingBuilder] {len(documents)} documentos canônicos gerados")

        # 3. Mapeamento de tipos para pesos (usa pesos do config quando disponível)
        weights_config = self.config.get("vetores_pesos", {})
        default_weights = {
            "structural": 0.25,
            "semantic": 0.35,
            "operational": 0.20,
            "symbolic": 0.20,
        }
        emb_weights = {
            t: weights_config.get(t, default_weights.get(t, 0.25))
            for t in ["structural", "semantic", "operational", "symbolic"]
        }
        # Normalizar pesos para somar 1.0
        total_w = sum(emb_weights.values())
        if total_w > 0:
            emb_weights = {k: v / total_w for k, v in emb_weights.items()}

        print(f"[EmbeddingBuilder] Pesos normalizados: {emb_weights}")

        # 4. Gerar embeddings para cada tipo
        embeddings = {}
        all_uids = list(documents.keys())

        for emb_type in ["structural", "semantic", "operational", "symbolic"]:
            texts = [documents[uid][emb_type] for uid in all_uids]
            print(f"[EmbeddingBuilder] Encoding {emb_type} ({len(texts)} textos)...")

            vectors = self.model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=True,
                batch_size=self.config.get("geracao", {}).get("batch_size", 64),
            )

            for i, uid in enumerate(all_uids):
                if uid not in embeddings:
                    embeddings[uid] = {}
                embeddings[uid][emb_type] = {
                    "vector": vectors[i].tolist(),
                    "weight": emb_weights[emb_type],
                }

        # 5. Calcular embedding combinado ponderado
        print("[EmbeddingBuilder] Calculando embeddings combinados...")
        for uid in all_uids:
            combined = np.zeros(self.embedding_dim, dtype=np.float32)
            for emb_type in ["structural", "semantic", "operational", "symbolic"]:
                vec = np.array(embeddings[uid][emb_type]["vector"], dtype=np.float32)
                weight = embeddings[uid][emb_type]["weight"]
                combined += vec * weight

            # L2 normalization
            norm = np.linalg.norm(combined)
            if norm > 1e-8:
                combined = combined / norm

            embeddings[uid]["combined"] = combined.tolist()

        # 6. Salvar embeddings individuais
        print(f"[EmbeddingBuilder] Salvando {len(all_uids)} embeddings em {output_path}")
        saved_files = []
        for uid in all_uids:
            out_file = output_path / f"{uid}.npy"
            np.save(out_file, np.array(embeddings[uid]["combined"], dtype=np.float32))
            saved_files.append(out_file.name)

        # 7. Salvar índice
        index = {
            "metadata": {
                "model": self.config.get("modelo", {}).get("nome", "unknown"),
                "dimension": self.embedding_dim,
                "total_cells": len(all_uids),
                "weights": emb_weights,
            },
            "embeddings": {
                uid: {
                    "types": {
                        t: {"weight": embeddings[uid][t]["weight"]}
                        for t in ["structural", "semantic", "operational", "symbolic"]
                    },
                    "file": f"{uid}.npy",
                }
                for uid in all_uids
            },
        }

        index_path = output_path / "embeddings_index.json"
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"[EmbeddingBuilder] Índice salvo em {index_path}")
        print(f"[EmbeddingBuilder] Concluído: {len(saved_files)} vetores de dimensão {self.embedding_dim}")

        return index

    def encode_query(self, query: str) -> np.ndarray:
        """Gera embedding para uma query de busca.

        Args:
            query: Texto da consulta.

        Returns:
            Vetor de embedding normalizado (L2).
        """
        vector = self.model.encode(
            query, normalize_embeddings=True, convert_to_numpy=True
        )
        return vector.astype(np.float32)

    def encode_batch(self, queries: list[str]) -> np.ndarray:
        """Gera embeddings para múltiplas queries.

        Args:
            queries: Lista de textos de consulta.

        Returns:
            Array de embeddings normalizados (shape: [n_queries, dim]).
        """
        vectors = self.model.encode(
            queries, normalize_embeddings=True, convert_to_numpy=True
        )
        return vectors.astype(np.float32)


def main():
    """Entry point para construção de embeddings via CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Gera embeddings vetoriais para as 162 células N4"
    )
    parser.add_argument(
        "--json-dir",
        default="data/json",
        help="Diretório com JSONs enriquecidos (padrão: data/json)",
    )
    parser.add_argument(
        "--output-dir",
        default="data/embeddings",
        help="Diretório de saída para embeddings (padrão: data/embeddings)",
    )
    parser.add_argument(
        "--config",
        default="config/embedding.yaml",
        help="Caminho para config YAML (padrão: config/embedding.yaml)",
    )
    args = parser.parse_args()

    builder = EmbeddingBuilder(config_path=args.config)
    index = builder.build_all_embeddings(
        json_dir=args.json_dir, output_dir=args.output_dir
    )

    total = index["metadata"]["total_cells"]
    dim = index["metadata"]["dimension"]
    print(f"\n✅ Embeddings construídos com sucesso: {total} vetores de dimensão {dim}")


if __name__ == "__main__":
    main()
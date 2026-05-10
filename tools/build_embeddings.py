#!/usr/bin/env python3
"""Script de Construção de Embeddings para as 162 células N4.

Executa o pipeline completo de geração de embeddings:
1. Carrega JSONs enriquecidos de data/json/
2. Gera documentos canônicos para cada célula
3. Computa embeddings multi-perspectiva via sentence-transformers
4. Calcula embedding combinado ponderado
5. Salva vetores .npy e índice JSON em data/embeddings/

Usage:
    python tools/build_embeddings.py
    python tools/build_embeddings.py --json-dir data/json --output-dir data/embeddings
"""

import sys
from pathlib import Path

# Garantir que paths do projeto estão no sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "tools"))
sys.path.insert(0, str(PROJECT_ROOT / "core"))
sys.path.insert(0, str(PROJECT_ROOT))

from embedding_builder import EmbeddingBuilder


def main():
    """Entry point principal."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Constrói embeddings vetoriais para as 162 células N4 da ontologia fractal"
    )
    parser.add_argument(
        "--json-dir",
        default="data/json",
        help="Diretório com JSONs enriquecidos N4 (padrão: data/json)",
    )
    parser.add_argument(
        "--output-dir",
        default="data/embeddings",
        help="Diretório de saída para embeddings (padrão: data/embeddings)",
    )
    parser.add_argument(
        "--config",
        default="config/embedding.yaml",
        help="Caminho para arquivo de configuração YAML (padrão: config/embedding.yaml)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Apenas validar dados existentes sem gerar embeddings",
    )
    args = parser.parse_args()

    # Resolver caminhos relativos ao diretório do projeto
    json_dir = PROJECT_ROOT / args.json_dir if not Path(args.json_dir).is_absolute() else Path(args.json_dir)
    output_dir = PROJECT_ROOT / args.output_dir if not Path(args.output_dir).is_absolute() else Path(args.output_dir)
    config_path = PROJECT_ROOT / args.config if not Path(args.config).is_absolute() else Path(args.config)

    print("=" * 70)
    print("  CONSTRUTOR DE EMBEDDINGS — FASE 4: EMBEDDINGS E RETRIEVAL HÍBRIDO")
    print("=" * 70)
    print(f"  JSONs de entrada:  {json_dir}")
    print(f"  Saída de embeddings: {output_dir}")
    print(f"  Configuração:      {config_path}")
    print("=" * 70)

    if args.validate_only:
        # Modo de validação: apenas contar e inspecionar JSONs
        import json

        json_files = sorted([f for f in json_dir.glob("N4_*.json")])
        print(f"\n📋 Modo de validação: {len(json_files)} arquivos JSON encontrados")

        uids = set()
        for f in json_files:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            uid = data.get("uid", f.stem)
            uids.add(uid)

            # Validar campos obrigatórios
            required = ["uid", "nome", "pilar", "dominio", "axis", "natureza"]
            missing = [k for k in required if k not in data]
            if missing:
                print(f"  ⚠️  {uid}: campos ausentes: {missing}")

            # Validar funcao_cognitiva
            funcs = data.get("funcao_cognitiva", [])
            if not funcs:
                print(f"  ⚠️  {uid}: sem funções cognitivas")

            # Validar assinatura semântica
            sig = data.get("assinatura_semantica", {})
            if not sig:
                print(f"  ⚠️  {uid}: sem assinatura semântica")

        print(f"\n  ✅ Total de UIDs únicos: {len(uids)}")
        print(f"  ✅ Esperado: 162 células N4")

        if len(uids) == 162:
            print("\n  🎯 VALIDAÇÃO APROVADA: 162 células encontradas")
        else:
            print(f"\n  ❌ DISCREPÂNCIA: Esperados 162, encontrados {len(uids)}")
        return

    # Modo de construção
    builder = EmbeddingBuilder(config_path=str(config_path))

    print(f"\n🔄 Iniciando construção de embeddings...")
    print(f"   Modelo: {builder.model}")
    print(f"   Dimensão: {builder.embedding_dim}\n")

    index = builder.build_all_embeddings(
        json_dir=str(json_dir),
        output_dir=str(output_dir),
    )

    # Resumo
    total = index["metadata"]["total_cells"]
    dim = index["metadata"]["dimension"]
    weights = index["metadata"]["weights"]

    print("\n" + "=" * 70)
    print("  ✅ EMBEDDINGS CONSTRUÍDOS COM SUCESSO")
    print("=" * 70)
    print(f"  Células processadas: {total}")
    print(f"  Dimensão dos vetores: {dim}")
    print(f"  Pesos de fusão: {weights}")
    print(f"  Arquivo de índice: {output_dir / 'embeddings_index.json'}")
    print(f"  Arquivos .npy: {total} arquivos em {output_dir}")
    print("=" * 70)

    # Verificação rápida
    import os

    npy_files = list(Path(output_dir).glob("N4_*.npy"))
    if len(npy_files) == total:
        print(f"\n  ✅ Verificação: {len(npy_files)} arquivos .npy correspondem ao índice")
    else:
        print(f"\n  ⚠️  Verificação: {len(npy_files)} .npy vs {total} no índice")

    # Teste de carregamento
    print("\n🔄 Testando carregamento de embeddings...")
    test_uid = list(index["embeddings"].keys())[0]
    test_vec = np.load(output_dir / f"{test_uid}.npy")
    print(f"  Teste: {test_uid} → shape={test_vec.shape}, norm={np.linalg.norm(test_vec):.4f}")
    print("\n✅ Pipeline de embeddings pronto para uso!")


if __name__ == "__main__":
    main()
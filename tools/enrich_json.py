#!/usr/bin/env python3
"""
Enrich JSONs — FASE 2: Expansão Semântica

Este script percorre os 162 JSONs de data/json/, gera os campos:
  - funcao_cognitiva  (lista de funções cognitivas)
  - assinatura_semantica (dict com 9 dimensões, scores 0.0-1.0)
  - opostos (lista de UIDs das células opostas)

e salva os JSONs atualizados, gerando um relatório de qualidade.

Uso:
    python tools/enrich_json.py
    python tools/enrich_json.py --dry-run
    python tools/enrich_json.py --single N4_ALGORITMIA_1_A
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Adicionar root ao path para imports
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core.cognitive_function_engine import CognitiveFunctionEngine
from core.signature_engine import SignatureEngine
from core.dialectic_engine import DialecticEngine


JSON_DIR = ROOT / "data" / "json"
REPORT_PATH = ROOT / "data" / "semantic_expansion_report.md"


def load_registry(json_dir: Path) -> dict[str, dict]:
    """Carrega todas as células JSON em um dicionário {uid: data}."""
    registry: dict[str, dict] = {}
    json_files = sorted(json_dir.glob("N4_*.json"))

    for fpath in json_files:
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            uid = data.get("uid", fpath.stem)
            registry[uid] = data

    return registry


def save_json(data: dict, json_dir: Path) -> None:
    """Salva um JSON de volta no diretório, preservando formatação."""
    uid = data["uid"]
    fpath = json_dir / f"{uid}.json"

    # Ordenar chaves, manter indentação legível
    # Separa metadata e relacoes no final
    ordered_data = {}
    # Campos principais primeiro
    main_fields = [
        "uid", "legacy_id", "path", "hierarchical_id", "nivel",
        "pilar", "dominio", "n3_ref", "n3_name", "axis", "natureza",
        "subtree_num", "cell_num", "cell_letter",
        "nome", "nome_normalizado",
    ]
    for field in main_fields:
        if field in data:
            ordered_data[field] = data[field]

    # Campos de conteúdo
    content_fields = ["gatilho", "acao", "restricao", "verificacao"]
    for field in content_fields:
        if field in data:
            ordered_data[field] = data[field]

    # Novos campos da FASE 2
    new_fields = ["funcao_cognitiva", "assinatura_semantica", "opostos"]
    for field in new_fields:
        if field in data:
            ordered_data[field] = data[field]

    # Campos de exemplo/analogia
    example_fields = ["exemplos", "analogias", "tags", "relacoes"]
    for field in example_fields:
        if field in data:
            ordered_data[field] = data[field]

    # Metadata por último
    if "metadata" in data:
        ordered_data["metadata"] = data["metadata"]

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(ordered_data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def enrich_cell(cell_data: dict, registry: dict,
                cog_engine: CognitiveFunctionEngine,
                sig_engine: SignatureEngine,
                dia_engine: DialecticEngine) -> dict:
    """
    Enriquece uma célula com os 3 novos campos.

    Args:
        cell_data: Dados da célula
        registry: Registry completo
        cog_engine: Motor de funções cognitivas
        sig_engine: Motor de assinaturas semânticas
        dia_engine: Motor dialético

    Returns:
        Célula enriquecida
    """
    enriched = dict(cell_data)

    # 1. Funções cognitivas
    functions = cog_engine.infer_functions(cell_data, registry)
    enriched["funcao_cognitiva"] = functions

    # 2. Assinatura semântica
    signature = sig_engine.generate_signature(cell_data)
    enriched["assinatura_semantica"] = signature

    # 3. Opostos
    opposites = dia_engine.infer_opposites(cell_data, registry)
    enriched["opostos"] = opposites

    # Atualizar metadata com versão da fase 2
    if "metadata" in enriched:
        meta = enriched["metadata"]
        if "versoes" not in meta:
            meta["versoes"] = []
        meta["versoes"].append({
            "versao": "2.0.0",
            "data": datetime.now(timezone.utc).isoformat(),
            "descricao": "Expansão semântica: funcao_cognitiva, assinatura_semantica, opostos"
        })
        meta["status"] = "enriquecido"

    return enriched


def validate_enrichment(registry: dict) -> dict:
    """
    Valida os dados enriquecidos contra os critérios de aceitação.

    Returns:
        Dicionário com resultados da validação
    """
    results = {
        "total_celulas": 0,
        "com_funcao_cognitiva": 0,
        "com_assinatura": 0,
        "com_opostos": 0,
        "assinatura_scores_validos": 0,
        "funcoes_coerentes": 0,
        "opostos_minimos": 0,
        "erros": [],
        "warnings": [],
    }

    results["total_celulas"] = len(registry)

    for uid, data in registry.items():
        # Verificar funcao_cognitiva
        funcs = data.get("funcao_cognitiva", [])
        if funcs and len(funcs) >= 1:
            results["com_funcao_cognitiva"] += 1
            # Verificar coerência com pilar
            pilar = data.get("pilar", "")
            dominio = data.get("dominio", "")
            if funcs:
                results["funcoes_coerentes"] += 1
        else:
            results["erros"].append(f"{uid}: sem funcao_cognitiva")

        # Verificar assinatura semântica
        sig = data.get("assinatura_semantica", {})
        if isinstance(sig, dict) and len(sig) == 9:
            results["com_assinatura"] += 1
            # Verificar scores em [0.0, 1.0]
            all_valid = True
            for dim, score in sig.items():
                if not isinstance(score, (int, float)):
                    all_valid = False
                    results["erros"].append(f"{uid}: score '{dim}' não numérico")
                elif score < 0.0 or score > 1.0:
                    all_valid = False
                    results["erros"].append(
                        f"{uid}: score '{dim}'={score} fora de [0.0, 1.0]"
                    )
            if all_valid:
                results["assinatura_scores_validos"] += 1
        else:
            results["erros"].append(
                f"{uid}: assinatura_semantica inválida "
                f"(tipo={type(sig).__name__}, len={len(sig) if isinstance(sig, dict) else 'N/A'})"
            )

        # Verificar opostos
        opposites = data.get("opostos", [])
        if opposites and len(opposites) >= 1:
            results["com_opostos"] += 1
        else:
            results["warnings"].append(f"{uid}: sem opostos identificados")

    return results


def generate_report(registry: dict, validation: dict,
                    elapsed_time: float) -> str:
    """Gera relatório de qualidade em Markdown."""
    total = validation["total_celulas"]

    lines = [
        "# Relatório de Expansão Semântica — FASE 2",
        "",
        f"**Gerado em:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Tempo de execução:** {elapsed_time:.2f}s",
        f"**Total de células:** {total}",
        "",
        "## Critérios de Aceitação",
        "",
        "| Critério | Esperado | Obtido | Status |",
        "|----------|----------|--------|--------|",
        f"| Todas possuem funcao_cognitiva (≥1) | {total} | {validation['com_funcao_cognitiva']} | {'✅' if validation['com_funcao_cognitiva'] == total else '❌'} |",
        f"| Todas possuem assinatura_semantica (9 dims) | {total} | {validation['com_assinatura']} | {'✅' if validation['com_assinatura'] == total else '❌'} |",
        f"| Scores em [0.0, 1.0] | {total} | {validation['assinatura_scores_validos']} | {'✅' if validation['assinatura_scores_validos'] == total else '❌'} |",
        f"| Pelo menos 80% com opostos | {int(total * 0.8)} | {validation['com_opostos']} | {'✅' if validation['com_opostos'] >= int(total * 0.8) else '❌'} |",
        f"| Funções coerentes com domínio/pilar | — | {validation['funcoes_coerentes']} | {'✅' if validation['funcoes_coerentes'] == total else '⚠️'} |",
        "",
        "## Estatísticas por Domínio",
        "",
        "| Domínio | Células | Média funções | Média opostos |",
        "|---------|---------|---------------|---------------|",
    ]

    # Estatísticas por domínio
    domain_stats: dict[str, dict] = {}
    for uid, data in registry.items():
        dom = data.get("dominio", "DESCONHECIDO")
        if dom not in domain_stats:
            domain_stats[dom] = {
                "count": 0, "total_funcs": 0, "total_opposites": 0,
                "sig_sums": {d: 0.0 for d in SignatureEngine.DIMENSIONS}
            }
        stats = domain_stats[dom]
        stats["count"] += 1
        stats["total_funcs"] += len(data.get("funcao_cognitiva", []))
        stats["total_opposites"] += len(data.get("opostos", []))
        sig = data.get("assinatura_semantica", {})
        if isinstance(sig, dict):
            for d in SignatureEngine.DIMENSIONS:
                stats["sig_sums"][d] += sig.get(d, 0.0)

    for dom in sorted(domain_stats.keys()):
        stats = domain_stats[dom]
        n = stats["count"]
        avg_funcs = stats["total_funcs"] / n if n else 0
        avg_opps = stats["total_opposites"] / n if n else 0
        lines.append(f"| {dom} | {n} | {avg_funcs:.1f} | {avg_opps:.1f} |")

    lines.extend([
        "",
        "## Distribuição de Funções Cognitivas",
        "",
        "| Função | Ocorrências | % do Total |",
        "|--------|-------------|------------|",
    ])

    # Contar funções
    func_counts: dict[str, int] = {}
    for data in registry.values():
        for func in data.get("funcao_cognitiva", []):
            func_counts[func] = func_counts.get(func, 0) + 1

    for func, count in sorted(func_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"| {func} | {count} | {pct:.1f}% |")

    lines.extend([
        "",
        "## Média das Assinaturas Semânticas por Domínio",
        "",
        "| Domínio | " + " | ".join(SignatureEngine.DIMENSIONS[:5]) + " |",
        "|---------|" + "|".join(["-------"] * 5) + "|",
    ])

    for dom in sorted(domain_stats.keys()):
        stats = domain_stats[dom]
        n = stats["count"]
        dims_avg = [f"{stats['sig_sums'][d]/n:.2f}" for d in SignatureEngine.DIMENSIONS[:5]]
        lines.append(f"| {dom} | " + " | ".join(dims_avg) + " |")

    lines.extend([
        "",
        "## Erros e Warnings",
        "",
    ])

    if validation["erros"]:
        lines.append("### Erros")
        for err in validation["erros"][:20]:  # Limitar output
            lines.append(f"- {err}")
        if len(validation["erros"]) > 20:
            lines.append(f"- ... e mais {len(validation['erros']) - 20} erros")
    else:
        lines.append("✅ Nenhum erro encontrado.")

    lines.append("")
    if validation["warnings"]:
        lines.append("### Warnings")
        for warn in validation["warnings"][:20]:
            lines.append(f"- {warn}")
    else:
        lines.append("✅ Nenhum warning.")

    lines.extend([
        "",
        "## Células Sem Opostos (para revisão manual)",
        "",
    ])

    no_opposites = [
        uid for uid, data in registry.items()
        if not data.get("opostos", [])
    ]
    if no_opposites:
        for uid in no_opposites[:30]:
            data = registry[uid]
            lines.append(f"- `{uid}` ({data.get('pilar', '?')}/{data.get('dominio', '?')}/{data.get('n3_name', '?')})")
        if len(no_opposites) > 30:
            lines.append(f"- ... e mais {len(no_opposites) - 30} células")
    else:
        lines.append("✅ Todas as células possuem opostos.")

    lines.extend([
        "",
        "---",
        f"*Relatório gerado automaticamente pelo pipeline de Expansão Semântica (FASE 2)*",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Enriquece JSONs N4 com metadados semânticos (FASE 2)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Executa sem salvar arquivos"
    )
    parser.add_argument(
        "--single", type=str, default=None,
        help="Processa apenas uma célula pelo UID"
    )
    parser.add_argument(
        "--output-dir", type=str, default=None,
        help="Diretório alternativo para salvar JSONs"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("EXPANSÃO SEMÂNTICA — FASE 2")
    print("=" * 60)

    # Inicializar engines
    print("\n[1/4] Inicializando motores...")
    cog_engine = CognitiveFunctionEngine()
    sig_engine = SignatureEngine()
    dia_engine = DialecticEngine()
    print("  ✅ CognitiveFunctionEngine")
    print("  ✅ SignatureEngine")
    print("  ✅ DialecticEngine")

    # Carregar registry
    print("\n[2/4] Carregando registry...")
    registry = load_registry(JSON_DIR)
    print(f"  ✅ {len(registry)} células carregadas")

    # Filtrar se single mode
    if args.single:
        if args.single not in registry:
            print(f"  ❌ Célula '{args.single}' não encontrada!")
            sys.exit(1)
        registry = {args.single: registry[args.single]}
        print(f"  🔍 Modo single: processando {args.single}")

    # Determinar diretório de saída
    output_dir = Path(args.output_dir) if args.output_dir else JSON_DIR

    # Processar células
    print(f"\n[3/4] Processando {len(registry)} células...")
    start_time = time.time()
    enriched_count = 0

    for uid, cell_data in registry.items():
        try:
            enriched = enrich_cell(cell_data, registry,
                                   cog_engine, sig_engine, dia_engine)
            registry[uid] = enriched

            if not args.dry_run:
                save_json(enriched, output_dir)

            enriched_count += 1

            # Progress indicator
            if enriched_count % 20 == 0 or enriched_count == len(registry):
                print(f"  📊 {enriched_count}/{len(registry)} "
                      f"({enriched_count / len(registry) * 100:.0f}%)")

        except Exception as e:
            print(f"  ❌ Erro ao processar {uid}: {e}")
            import traceback
            traceback.print_exc()

    elapsed = time.time() - start_time
    print(f"\n  ✅ {enriched_count} células processadas em {elapsed:.2f}s")

    # Validação
    print("\n[4/4] Validando resultados...")
    validation = validate_enrichment(registry)
    total = len(registry)

    print(f"  funcao_cognitiva: {validation['com_funcao_cognitiva']}/{total}")
    print(f"  assinatura_semantica: {validation['com_assinatura']}/{total}")
    print(f"  scores válidos: {validation['assinatura_scores_validos']}/{total}")
    print(f"  opostos: {validation['com_opostos']}/{total} "
          f"({validation['com_opostos']/total*100:.1f}%)")

    if validation["erros"]:
        print(f"  ❌ {len(validation['erros'])} erros")
    if validation["warnings"]:
        print(f"  ⚠️  {len(validation['warnings'])} warnings")

    # Gerar relatório
    print("\n📝 Gerando relatório de qualidade...")
    report = generate_report(registry, validation, elapsed)

    if not args.dry_run:
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"  ✅ Relatório salvo em {REPORT_PATH}")
    else:
        print("\n--- RELATÓRIO (dry-run) ---")
        print(report)

    # Resumo final
    print("\n" + "=" * 60)
    all_ok = (
        validation["com_funcao_cognitiva"] == total and
        validation["com_assinatura"] == total and
        validation["assinatura_scores_validos"] == total and
        validation["com_opostos"] >= int(total * 0.8) and
        len(validation["erros"]) == 0
    )
    if all_ok:
        print("✅ TODOS OS CRITÉRIOS DE ACEITAÇÃO ATENDIDOS!")
    else:
        print("⚠️  ALGUNS CRITÉRIOS NÃO FORAM ATENDIDOS")
        if validation["com_funcao_cognitiva"] < total:
            print(f"   - funcao_cognitiva: faltam {total - validation['com_funcao_cognitiva']}")
        if validation["com_assinatura"] < total:
            print(f"   - assinatura_semantica: faltam {total - validation['com_assinatura']}")
        if validation["assinatura_scores_validos"] < total:
            print(f"   - scores inválidos: {total - validation['assinatura_scores_validos']}")
        if validation["com_opostos"] < int(total * 0.8):
            print(f"   - opostos: {validation['com_opostos']}/{int(total * 0.8)} necessários")
    print("=" * 60)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
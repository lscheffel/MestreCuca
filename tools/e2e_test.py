#!/usr/bin/env python3
"""Teste E2E completo do pipeline cognitivo ontológico."""

import sys
import json
import time
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))

from runtime.orchestrator import OntologyOrchestrator

def run_tests():
    print("=" * 70)
    print("TESTE E2E — SISTEMA COGNITIVO ONTOLÓGICO")
    print("=" * 70)

    orch = OntologyOrchestrator()

    # Health check
    health = orch.health_check()
    print(f"\n[HEALTH] Status: {health['status']}")
    for comp, info in health['checks'].items():
        status = info.get('status', 'unknown')
        detail = info.get('detail', '')
        extra = ''
        if 'registry_size' in info:
            extra = f" (size={info['registry_size']})"
        if 'nodes' in info:
            extra = f" (nodes={info['nodes']}, edges={info['edges']})"
        print(f"  {comp}: {status}{extra}")
        if detail:
            print(f"    detail: {detail}")

    # Multi-query test
    queries = [
        ("Decomposição de problemas", "Como decompor um problema complexo em partes menores?"),
        ("Conflito emocional", "Como lidar com conflito emocional no trabalho?"),
        ("Emergência em sistemas", "O que é emergência em sistemas complexos?"),
        ("Ritual de transformação", "Como criar um ritual de transformação pessoal?"),
        ("Recursão aplicada", "O que é recursão e como aplicar na resolução de problemas?"),
        ("Razão vs emoção", "Como encontrar equilíbrio entre razão e emoção?"),
        ("Algoritmo de decisão", "Qual o melhor algoritmo para decisões complexas?"),
        ("Caos e ordem", "Como o caos pode gerar novas ordens?"),
        ("Simbolismo profundo", "O que os símbolos arquetípicos revelam sobre a mente?"),
        ("Metabolismo social", "Como o metabolismo se aplica a sistemas sociais?"),
    ]

    results = []
    all_passed = True

    print(f"\n{'=' * 70}")
    print(f"TESTES DE QUERY ({len(queries)} queries)")
    print(f"{'=' * 70}")

    for label, query in queries:
        t0 = time.time()
        try:
            r = orch.process(query)
            lat = (time.time() - t0) * 1000

            n0 = r.classification.get('classificacao', {}).get('n0_eixo', {}).get('eixo', 'N/A')
            n1 = r.classification.get('classificacao', {}).get('n1_pilar', {}).get('pilar', 'N/A')
            n2 = r.classification.get('classificacao', {}).get('n2_dominio', {}).get('dominio', 'N/A')
            n4 = r.classification.get('classificacao', {}).get('n4_celula', {}).get('celula_nome', 'N/A')
            n_retrieved = len(r.retrieved_cells)
            n_synthesis_refs = len(r.synthesis.cell_references) if r.synthesis else 0
            valid = r.validation.get('valido', False) if r.validation else None
            status = r.status

            passed = (status == 'success' and n_retrieved > 0 and n_synthesis_refs > 0
                      and valid is not None and lat < 5000)

            if not passed:
                all_passed = False

            result = {
                'label': label,
                'query': query,
                'eixo': n0, 'pilar': n1, 'dominio': n2, 'celula': n4,
                'retrieved': n_retrieved, 'refs': n_synthesis_refs,
                'validation': valid, 'latency_ms': round(lat, 1),
                'status': status, 'passed': passed
            }
            results.append(result)

            icon = "✓" if passed else "✗"
            print(f"\n{icon} [{label}]")
            print(f"  Query: {query[:60]}...")
            print(f"  Class: {n0} → {n1} → {n2} → {n4}")
            print(f"  Retrieved: {n_retrieved} | Synthesis refs: {n_synthesis_refs}")
            print(f"  Validation: {'APROVADO' if valid else 'REPROVADO' if valid is not None else 'N/A'}")
            print(f"  Latency: {lat:.1f}ms | Status: {status}")

        except Exception as e:
            all_passed = False
            lat = (time.time() - t0) * 1000
            result = {
                'label': label, 'query': query,
                'eixo': 'ERROR', 'pilar': '', 'dominio': '', 'celula': '',
                'retrieved': 0, 'refs': 0, 'validation': None,
                'latency_ms': round(lat, 1), 'status': 'failed', 'passed': False,
                'error': str(e)
            }
            results.append(result)
            print(f"\n✗ [{label}] ERROR: {e}")

    # Summary
    print(f"\n{'=' * 70}")
    print("RESUMO")
    print(f"{'=' * 70}")
    passed_count = sum(1 for r in results if r['passed'])
    avg_latency = sum(r['latency_ms'] for r in results) / len(results) if results else 0
    max_latency = max((r['latency_ms'] for r in results), default=0)
    min_latency = min((r['latency_ms'] for r in results), default=0)

    print(f"  Total queries: {len(results)}")
    print(f"  Passed: {passed_count}/{len(results)}")
    print(f"  Avg latency: {avg_latency:.1f}ms")
    print(f"  Min latency: {min_latency:.1f}ms")
    print(f"  Max latency: {max_latency:.1f}ms")
    print(f"  Overall: {'TODOS APROVADOS' if all_passed else 'ALGUM FALHOU'}")

    # Save results
    output_path = Path(__file__).resolve().parent.parent / "data" / "test_results.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResultados salvos em: {output_path}")

    # Save CSV
    csv_path = Path(__file__).resolve().parent.parent / "data" / "test_results.csv"
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'label', 'query', 'eixo', 'pilar', 'dominio', 'celula',
            'retrieved', 'refs', 'validation', 'latency_ms', 'status', 'passed'
        ])
        writer.writeheader()
        for r in results:
            row = {k: v for k, v in r.items() if k in writer.fieldnames}
            writer.writerow(row)
    print(f"CSV salvo em: {csv_path}")

    return all_passed

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""
RUN KILO — Entry Point principal do Sistema Cognitivo Kilo Code.

Executar a partir da raiz do projeto:
    python run_kilo.py --health
    python run_kilo.py --query "como resolver conflitos?"
    python run_kilo.py --mode interactive
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
import re
import yaml
from datetime import datetime, timezone
from pathlib import Path

# ── Resolução robusta do diretório raiz ──────────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent
_KILO_ROOT = _PROJECT_ROOT / ".kilo"
_RESULTS_DIR = _PROJECT_ROOT / "results"

# Garante que tanto a raiz quanto .kilo/ sejam importáveis
for _p in [_PROJECT_ROOT, _PROJECT_ROOT / "core", _PROJECT_ROOT / "runtime",
           _KILO_ROOT, _KILO_ROOT / "agents", _PROJECT_ROOT / "agents", _PROJECT_ROOT / "tools"]:
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

logger = logging.getLogger("kilo.run")


def setup_logging(level: str = "INFO") -> None:
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    if not root_logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        root_logger.addHandler(console_handler)
    for noisy in ["urllib3", "sklearn", "sentence_transformers"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)


def run_health_check(verbose: bool = False) -> bool:
    from agents.health_check import HealthCheck
    hc = HealthCheck(verbose=verbose)
    results = hc.run_all_checks()
    all_passed = all(r.passed for r in results.values())

    print("\n" + "=" * 60)
    print("  HEALTH CHECK — Kilo Code Cognitive System")
    print("=" * 60)
    for name, result in results.items():
        icon = "✅" if result.passed else "❌"
        status = "PASS" if result.passed else "FAIL"
        print(f"  {icon} [{status}] {name}")
        if result.detail and verbose:
            print(f"      {result.detail}")
        for w in result.warnings:
            print(f"      ⚠️  {w}")

    print("=" * 60)
    if all_passed:
        print("  ✅ SISTEMA OPERACIONAL — Todos os checks passaram")
    else:
        failed = sum(1 for r in results.values() if not r.passed)
        print(f"  ⚠️  {failed} check(s) falhou — Verifique os logs acima")
    print("=" * 60 + "\n")
    return all_passed


def initialize_system() -> dict:
    from core.ontology_graph import OntologyGraph
    from runtime.classifier import OntologicalClassifier
    from runtime.router import CognitiveRouter
    from runtime.retriever import HybridRetriever
    from runtime.synthesizer import OntologySynthesizer
    from runtime.validator import OntologyValidator
    from agents.multi_agent_orchestrator import MultiAgentOrchestrator
    from agents.autonomy_layer import AutonomyLayer

    components: dict = {}
    errors: list = []
    json_dir = str(_PROJECT_ROOT / "data" / "json")

    # 1. Ontology Graph
    try:
        graph = OntologyGraph(json_dir=json_dir)
        graph.load_registry()
        graph.build_graph()
        components["graph"] = graph
        logger.info(f"✅ Grafo ontológico: {graph.G.number_of_nodes()} nós, {graph.G.number_of_edges()} arestas")
    except Exception as e:
        errors.append(f"Grafo: {e}")
        logger.error(f"❌ Grafo: {e}")

    # 2. Classifier
    try:
        components["classifier"] = OntologicalClassifier()
        logger.info("✅ Classificador inicializado")
    except Exception as e:
        errors.append(f"Classifier: {e}")
        logger.error(f"❌ Classifier: {e}")

    # 3. Router
    try:
        components["router"] = CognitiveRouter()
        logger.info("✅ Router inicializado")
    except Exception as e:
        errors.append(f"Router: {e}")
        logger.error(f"❌ Router: {e}")

    # 4. Retriever
    try:
        components["retriever"] = HybridRetriever(
            embedding_dir=str(_PROJECT_ROOT / "data" / "embeddings"),
            json_dir=json_dir,
            config_path=str(_PROJECT_ROOT / "config" / "retrieval.yaml"),
        )
        logger.info("✅ Retriever inicializado")
    except Exception as e:
        errors.append(f"Retriever: {e}")
        logger.error(f"❌ Retriever: {e}")

    # 5. Synthesizer
    try:
        components["synthesizer"] = OntologySynthesizer()
        logger.info("✅ Synthesizer inicializado")
    except Exception as e:
        errors.append(f"Synthesizer: {e}")
        logger.error(f"❌ Synthesizer: {e}")

    # 6. Validator
    try:
        components["validator"] = OntologyValidator()
        logger.info("✅ Validator inicializado")
    except Exception as e:
        errors.append(f"Validator: {e}")
        logger.error(f"❌ Validator: {e}")

    # 7. Multi-Agent Orchestrator
    try:
        components["orchestrator"] = MultiAgentOrchestrator(
            config={"config_dir": str(_PROJECT_ROOT / "config")},
            retriever=components.get("retriever"),
            graph=components.get("graph"),
        )
        logger.info("✅ Orquestrador multi-agente inicializado")
    except Exception as e:
        errors.append(f"Orchestrator: {e}")
        logger.error(f"❌ Orchestrator: {e}")

    # 8. Autonomy Layer
    try:
        components["autonomy"] = AutonomyLayer()
        logger.info("✅ Autonomy Layer inicializado")
    except Exception as e:
        errors.append(f"Autonomy: {e}")
        logger.error(f"❌ Autonomy: {e}")

    if errors:
        logger.warning(f"⚠️  {len(errors)} componente(s) com falha: {errors}")
    return components


def save_query_results(query: str, result_dict: dict) -> None:
    """Salva o resultado completo em JSON e o output final em YAML."""
    try:
        _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Cria um nome de arquivo limpo baseado nos primeiros 30 caracteres da query
        safe_query = re.sub(r'[^a-zA-Z0-9]', '_', query)[:30].strip('_')
        if not safe_query:
            safe_query = "query"
        base_filename = f"{timestamp}_{safe_query}"
        
        with open(_RESULTS_DIR / f"{base_filename}_full.json", "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, default=str, ensure_ascii=False)
            
        with open(_RESULTS_DIR / f"{base_filename}_output.yaml", "w", encoding="utf-8") as f:
            yaml.dump(result_dict.get("final_output", {}), f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            
    except Exception as e:
        logger.error(f"❌ Erro ao salvar resultados: {e}")

def run_pipeline(components: dict, query: str, mode: str = "full") -> dict:
    orchestrator = components.get("orchestrator")
    if orchestrator is None:
        return {"error": "Orquestrador não disponível", "status": "failed"}

    if mode == "autonomous":
        autonomy = components.get("autonomy")
        if autonomy:
            result = autonomy.run_autonomous_pipeline(query, components)
        else:
            result = orchestrator.full_pipeline(query)
    elif mode == "simple":
        result = orchestrator.simple_pipeline(query)
    else:
        result = orchestrator.full_pipeline(query)

    result_dict = result.to_dict()
    result_dict["mode"] = mode
    result_dict["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Salva os resultados automaticamente, independente do modo
    save_query_results(query, result_dict)

    return result_dict


def run_interactive(components: dict) -> None:
    print("\n" + "=" * 60)
    print("  MODO INTERATIVO — Kilo Code Cognitive System")
    print("  Digite 'sair' para encerrar, 'health' para diagnóstico")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("🔮 Query > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break
        if not query:
            continue
        if query.lower() in ("sair", "exit", "quit"):
            break
        if query.lower() == "health":
            run_health_check(verbose=True)
            continue

        print(f"\n⏳ Processando: '{query}'...\n")
        t0 = time.time()
        result = run_pipeline(components, query, mode="autonomous")
        elapsed = (time.time() - t0) * 1000

        if "error" in result:
            print(f"❌ Erro: {result['error']}")
        else:
            print("─" * 60)
            print(f"📊 Status: {result.get('status', 'N/A')}")
            print(f"⏱️  Latência: {elapsed:.0f}ms")
            final = result.get("final_output", {})
            if isinstance(final, dict) and "content" in final:
                print(f"\n💬 Resposta:\n{final['content']}")
            elif isinstance(final, dict) and "qa_pairs" in final:
                for qa in final["qa_pairs"]:
                    print(f"\n  Q: {qa.get('question', 'N/A')}")
                    print(f"  A: {qa.get('answer', 'N/A')}")
            else:
                print(f"\n📋 Resultado: {json.dumps(result, indent=2, default=str)[:2000]}")
            print("─" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Kilo Code — Sistema Cognitivo Ontológico",
        epilog="""
Exemplos:
  %(prog)s --health                     Verificação de saúde
  %(prog)s --query "como decompor?"     Execução única
  %(prog)s --mode interactive            Modo interativo
  %(prog)s --mode simple --query "teste" Pipeline simplificado
        """,
    )
    parser.add_argument("--health", action="store_true", help="Health check")
    parser.add_argument("--query", "-q", type=str, help="Query para processamento")
    parser.add_argument("--mode", "-m", type=str, default="full",
                        choices=["full", "simple", "autonomous", "interactive"],
                        help="Modo de execução (default: full)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Output detalhado")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])

    args = parser.parse_args()
    setup_logging(args.log_level)
    logger.info("🚀 Inicializando Kilo Code Cognitive System...")

    if args.health:
        success = run_health_check(verbose=args.verbose)
        sys.exit(0 if success else 1)

    components = initialize_system()

    if args.mode == "interactive":
        run_interactive(components)
        return

    if args.query:
        result = run_pipeline(components, args.query, mode=args.mode)
        print(json.dumps(result, indent=2, default=str))
    elif not args.health:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
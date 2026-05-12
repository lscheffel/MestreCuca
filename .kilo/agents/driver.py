#!/usr/bin/env python3
"""
DRIVER PRINCIPAL — Entry Point do Sistema Cognitivo Kilo Code.

Orquestra a inicialização e execução do pipeline multi-agente baseado
na Ontologia Fractal N0→N4.

FASE 10 do Roadmap da Ontologia Fractal.

Uso:
    python -m .kilo.agents.driver
    python -m .kilo.agents.driver --query "como resolver conflitos?"
    python -m .kilo.agents.driver --mode interactive
    python -m .kilo.agents.driver --health
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

# Resolução robusta do diretório raiz
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))
if str(_PROJECT_ROOT / "runtime") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "runtime"))

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configura o logging global do sistema."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_format = logging.Formatter(
        "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    root_logger.addHandler(console_handler)

    # Suppress noisy loggers
    for noisy in ["urllib3", "sklearn", "sentence_transformers"]:
        logging.getLogger(noisy).setLevel(logging.WARNING)


def load_config() -> Dict[str, Any]:
    """Carrega todas as configurações do sistema."""
    import yaml

    config_dir = _PROJECT_ROOT / ".kilo" / "config"
    configs = {}

    for config_file in ["ontology", "embedding", "retrieval", "graph"]:
        path = config_dir / f"{config_file}.yaml"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                configs[config_file] = yaml.safe_load(f) or {}
        else:
            logger.warning(f"Config ausente: {path}")
            configs[config_file] = {}

    return configs


def initialize_system(configs: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
    """Inicializa todos os componentes do sistema cognitivo.

    Returns:
        Dicionário com referências aos componentes inicializados.
    """
    components: Dict[str, Any] = {}
    errors: list = []

    # 1. Ontology Graph
    try:
        from core.ontology_graph import OntologyGraph
        json_dir = str(_PROJECT_ROOT / "data" / "json")
        graph = OntologyGraph(json_dir=json_dir)
        graph.load_registry()
        graph.build_graph()
        components["graph"] = graph
        logger.info(f"✅ Grafo ontológico carregado: {graph.G.number_of_nodes()} nós, "
                     f"{graph.G.number_of_edges()} arestas")
    except Exception as e:
        errors.append(f"Falha ao carregar grafo: {e}")
        logger.error(f"❌ Falha ao carregar grafo: {e}")

    # 2. Classifier
    try:
        from runtime.classifier import OntologicalClassifier
        classifier = OntologicalClassifier()
        components["classifier"] = classifier
        logger.info("✅ Classificador ontológico inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar classificador: {e}")
        logger.error(f"❌ Falha ao inicializar classificador: {e}")

    # 3. Router
    try:
        from runtime.router import CognitiveRouter
        router = CognitiveRouter()
        components["router"] = router
        logger.info("✅ Router cognitivo inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar router: {e}")
        logger.error(f"❌ Falha ao inicializar router: {e}")

    # 4. Retriever
    try:
        from runtime.retriever import HybridRetriever
        retriever = HybridRetriever(
            embedding_dir=str(_PROJECT_ROOT / "data" / "embeddings"),
            json_dir=str(_PROJECT_ROOT / "data" / "json"),
            config_path=str(_PROJECT_ROOT / ".kilo" / "config" / "retrieval.yaml"),
        )
        components["retriever"] = retriever
        logger.info("✅ Retriever híbrido inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar retriever: {e}")
        logger.error(f"❌ Falha ao inicializar retriever: {e}")

    # 5. Synthesizer
    try:
        from runtime.synthesizer import OntologySynthesizer
        synthesizer = OntologySynthesizer()
        components["synthesizer"] = synthesizer
        logger.info("✅ Engine de síntese inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar sintetizador: {e}")
        logger.error(f"❌ Falha ao inicializar sintetizador: {e}")

    # 6. Validator
    try:
        from runtime.validator import OntologyValidator
        validator = OntologyValidator()
        components["validator"] = validator
        logger.info("✅ Validador ontológico inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar validador: {e}")
        logger.error(f"❌ Falha ao inicializar validador: {e}")

    # 7. Multi-Agent Orchestrator
    try:
        from .multi_agent_orchestrator import MultiAgentOrchestrator
        orchestrator = MultiAgentOrchestrator(
            config={"config_dir": str(_PROJECT_ROOT / ".kilo" / "config")},
            classifier_agent=None,
            graph_agent=None,
            synthesis_agent=None,
            validator_agent=None,
            dialectic_agent=None,
            router=None,
            retriever=components.get("retriever"),
            graph=components.get("graph"),
        )
        components["orchestrator"] = orchestrator
        logger.info("✅ Orquestrador multi-agente inicializado")
    except Exception as e:
        errors.append(f"Falha ao inicializar orquestrador: {e}")
        logger.error(f"❌ Falha ao inicializar orquestrador: {e}")

    # 8. Autonomy Layer
    try:
        from .autonomy_layer import AutonomyLayer
        autonomy = AutonomyLayer()
        components["autonomy"] = autonomy
        logger.info("✅ Camada de autonomia inicializada")
    except Exception as e:
        errors.append(f"Falha ao inicializar autonomia: {e}")
        logger.error(f"❌ Falha ao inicializar autonomia: {e}")

    if errors:
        logger.warning(f"⚠️  {len(errors)} componente(s) com falha de inicialização")

    return components


def run_pipeline(components: Dict[str, Any], query: str, mode: str = "full") -> Dict[str, Any]:
    """Executa o pipeline cognitivo para uma query.

    Args:
        components: Dicionário de componentes inicializados.
        query: Pergunta ou instrução do usuário.
        mode: "full" | "simple" | "autonomous"

    Returns:
        Resultado do pipeline.
    """
    start_time = time.time()

    # Selecionar pipeline
    orchestrator = components.get("orchestrator")
    if orchestrator is None:
        return {"error": "Orquestrador não disponível"}

    # Modo autônomo usa AutonomyLayer
    if mode == "autonomous":
        autonomy = components.get("autonomy")
        if autonomy:
            result = autonomy.run_autonomous_pipeline(query, components)
        else:
            result = orchestrator.execute_pipeline(query, pipeline_mode="principal")
    else:
        result = orchestrator.execute_pipeline(query, pipeline_mode=mode)

    elapsed_ms = (time.time() - start_time) * 1000
    result["elapsed_ms"] = round(elapsed_ms, 2)
    result["mode"] = mode
    result["timestamp"] = datetime.now(timezone.utc).isoformat()

    return result


def run_health_check(verbose: bool = False) -> bool:
    """Executa verificação de saúde do sistema."""
    try:
        from .health_check import HealthCheck
    except ImportError:
        from health_check import HealthCheck

    hc = HealthCheck(verbose=verbose)
    results = hc.run_all_checks()

    all_passed = all(r.passed for r in results.values())

    print("\n" + "=" * 60)
    print("  HEALTH CHECK — Kilo Code Cognitive System")
    print("=" * 60)

    for check_name, result in results.items():
        icon = "✅" if result.passed else "❌"
        status = "PASS" if result.passed else "FAIL"
        detail = result.detail
        print(f"  {icon} [{status}] {check_name}")
        if detail and verbose:
            print(f"      {detail}")

    print("=" * 60)
    if all_passed:
        print("  ✅ SISTEMA OPERACIONAL — Todos os checks passaram")
    else:
        failed = sum(1 for r in results.values() if not r.passed)
        print(f"  ⚠️  {failed} check(s) falhou — Verifique os logs acima")
    print("=" * 60 + "\n")

    return all_passed


def run_interactive(components: Dict[str, Any]) -> None:
    """Modo interativo para consultas ao sistema cognitivo."""
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
            print("Encerrando...")
            break
        if query.lower() == "health":
            run_health_check(verbose=True)
            continue

        print(f"\n⏳ Processando: '{query}'...\n")
        result = run_pipeline(components, query, mode="autonomous")

        if "error" in result:
            print(f"❌ Erro: {result['error']}")
        else:
            print("─" * 60)
            print(f"📊 Status: {result.get('status', 'N/A')}")
            print(f"⏱️  Latência: {result.get('elapsed_ms', 0):.0f}ms")

            final_output = result.get("final_output", {})
            if isinstance(final_output, dict) and "content" in final_output:
                print(f"\n💬 Resposta:\n{final_output['content']}")
            elif isinstance(final_output, dict) and "qa_pairs" in final_output:
                for qa in final_output["qa_pairs"]:
                    print(f"\n  Q: {qa.get('question', 'N/A')}")
                    print(f"  A: {qa.get('answer', 'N/A')}")
            else:
                print(f"\n📋 Resultado: {json.dumps(result, indent=2, default=str)[:2000]}")

            print("─" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Kilo Code — Sistema Cognitivo Ontológico",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  %(prog)s --health                     Verificação de saúde do sistema
  %(prog)s --query "como decompor?"     Execução única
  %(prog)s --mode interactive            Modo interativo
  %(prog)s --mode simple --query "teste" Pipeline simplificado
        """
    )

    parser.add_argument("--health", action="store_true", help="Executa health check")
    parser.add_argument("--query", "-q", type=str, help="Query para processamento")
    parser.add_argument("--mode", "-m", type=str, default="full",
                        choices=["full", "simple", "autonomous", "interactive"],
                        help="Modo de execução (default: full)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Output detalhado")
    parser.add_argument("--log-level", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="Nível de logging")

    args = parser.parse_args()

    # Setup
    setup_logging(args.log_level)
    logger.info("🚀 Inicializando Kilo Code Cognitive System...")

    # Health check only
    if args.health:
        success = run_health_check(verbose=args.verbose)
        sys.exit(0 if success else 1)

    # Load configs
    configs = load_config()
    logger.info(f"📂 Configurações carregadas: {list(configs.keys())}")

    # Initialize components
    components = initialize_system(configs, verbose=args.verbose)

    # Interactive mode
    if args.mode == "interactive":
        run_interactive(components)
        return

    # Single query mode
    if args.query:
        result = run_pipeline(components, args.query, mode=args.mode)
        print(json.dumps(result, indent=2, default=str))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
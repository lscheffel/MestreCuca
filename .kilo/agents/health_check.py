#!/usr/bin/env python3
"""
HEALTH CHECK — Verificação de integridade do sistema cognitivo Kilo Code.

Valida todos os componentes necessários para o funcionamento correto
do pipeline multi-agente baseado na Ontologia Fractal N0→N4.

FASE 10 do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List

# Resolução robusta do diretório raiz
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

logger = logging.getLogger(__name__)


@dataclass
class CheckResult:
    """Resultado de uma verificação individual."""
    name: str
    passed: bool
    message: str = ""
    detail: str = ""
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "detail": self.detail,
            "warnings": self.warnings,
        }


class HealthCheck:
    """Suite completa de verificações de integridade do sistema Kilo Code."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = _PROJECT_ROOT
        self.results: Dict[str, CheckResult] = {}

    # ── Verificações de estrutura de arquivos ──────────────────────────

    def check_core_modules(self) -> CheckResult:
        """Verifica módulos core essenciais."""
        required_files = [
            "core/agent_base.py",
            "core/ontology_graph.py",
            "core/signature_engine.py",
            "core/dialectic_engine.py",
            "core/cognitive_function_engine.py",
            "core/ontology_typing.py",
            "core/relation_engine.py",
        ]
        missing = []
        found = []
        for f in required_files:
            p = self.project_root / f
            if p.exists():
                found.append(f)
            else:
                missing.append(f)
        passed = len(missing) == 0
        return CheckResult(
            name="core_modules",
            passed=passed,
            message=f"{len(found)}/{len(required_files)} módulos encontrados"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Módulos: {', '.join(found)}",
        )

    def check_runtime_modules(self) -> CheckResult:
        """Verifica módulos de runtime essenciais."""
        required_files = [
            "runtime/classifier.py",
            "runtime/router.py",
            "runtime/retriever.py",
            "runtime/synthesizer.py",
            "runtime/validator.py",
            "runtime/orchestrator.py",
        ]
        missing = []
        found = []
        for f in required_files:
            p = self.project_root / f
            if p.exists():
                found.append(f)
            else:
                missing.append(f)
        passed = len(missing) == 0
        return CheckResult(
            name="runtime_modules",
            passed=passed,
            message=f"{len(found)}/{len(required_files)} módulos encontrados"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Módulos: {', '.join(found)}",
        )

    def check_agent_modules(self) -> CheckResult:
        """Verifica módulos de agentes."""
        required_files = [
            ".kilo/agents/classifier_agent.py",
            ".kilo/agents/graph_agent.py",
            ".kilo/agents/synthesis_agent.py",
            ".kilo/agents/validator_agent.py",
            ".kilo/agents/dialectic_agent.py",
            ".kilo/agents/multi_agent_orchestrator.py",
            ".kilo/agents/autonomy_layer.py",
            ".kilo/agents/driver.py",
        ]
        missing = []
        found = []
        for f in required_files:
            p = self.project_root / f
            if p.exists():
                found.append(f)
            else:
                missing.append(f)
        passed = len(missing) == 0
        return CheckResult(
            name="agent_modules",
            passed=passed,
            message=f"{len(found)}/{len(required_files)} agentes encontrados"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Agentes: {', '.join(found)}",
        )

    def check_config_files(self) -> CheckResult:
        """Verifica arquivos de configuração."""
        config_dir = self.project_root / ".kilo" / "config"
        required = ["ontology.yaml", "embedding.yaml", "retrieval.yaml", "graph.yaml"]
        missing = []
        found = []
        for f in required:
            p = config_dir / f
            if p.exists():
                found.append(f)
            else:
                missing.append(f)
        passed = len(missing) == 0
        return CheckResult(
            name="config_files",
            passed=passed,
            message=f"{len(found)}/{len(required)} configs encontradas"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Configs: {', '.join(found)}",
        )

    def check_prompt_templates(self) -> CheckResult:
        """Verifica templates de prompt."""
        prompt_dir = self.project_root / ".kilo" / "prompts"
        required_dirs = ["classifier", "retrieval", "routing", "synthesis", "validation"]
        missing = []
        found = []
        for d in required_dirs:
            p = prompt_dir / d
            if p.exists() and any(p.iterdir()):
                found.append(d)
            else:
                missing.append(d)
        passed = len(missing) == 0
        return CheckResult(
            name="prompt_templates",
            passed=passed,
            message=f"{len(found)}/{len(required_dirs)} diretórios de prompts"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Prompts: {', '.join(found)}",
        )

    def check_data_directories(self) -> CheckResult:
        """Verifica diretórios de dados."""
        required_dirs = [
            "data/json",
            "data/embeddings",
            "data/indexes",
            "data/graphs",
        ]
        missing = []
        found = []
        for d in required_dirs:
            p = self.project_root / d
            if p.exists():
                found.append(d)
            else:
                missing.append(d)
        json_exists = (self.project_root / "data/json").exists()
        passed = json_exists
        return CheckResult(
            name="data_directories",
            passed=passed,
            message=f"{len(found)}/{len(required_dirs)} diretórios de dados"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Dados: {', '.join(found)}",
            warnings=[f"Considere criar: {d}" for d in missing] if missing else [],
        )

    def check_ontology_index(self) -> CheckResult:
        """Verifica o índice da ontologia."""
        index_path = self.project_root / "data" / "json" / "ontology_index.json"
        if not index_path.exists():
            return CheckResult(
                name="ontology_index",
                passed=False,
                message="Índice ontológico não encontrado",
                detail=f"Esperado: {index_path.relative_to(self.project_root)}",
            )
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                index = json.load(f)
            n_cells = len(index.get("celulas", []))
            n_files = len(index.get("files", [])) if isinstance(index.get("files"), list) else 0
            # Fallback: contar entradas de id_mapping se celulas/files não existirem
            if n_cells == 0 and "id_mapping" in index and isinstance(index["id_mapping"], dict):
                n_cells = len(index["id_mapping"])
            if n_cells >= 162 or n_files > 0:
                return CheckResult(
                    name="ontology_index",
                    passed=True,
                    message=f"Índice válido: {n_cells} células, {n_files} arquivos",
                    detail="Formato JSON válido com estrutura esperada",
                )
            else:
                return CheckResult(
                    name="ontology_index",
                    passed=False,
                    message=f"Índice com dados insuficientes: {n_cells} células",
                    detail="Esperado pelo menos 162 células N4",
                )
        except json.JSONDecodeError as e:
            return CheckResult(
                name="ontology_index",
                passed=False,
                message=f"JSON inválido: {e}",
            )

    def check_json_files(self) -> CheckResult:
        """Verifica arquivos JSON das células N4."""
        json_dir = self.project_root / "data" / "json"
        if not json_dir.exists():
            return CheckResult(
                name="json_files",
                passed=False,
                message="Diretório data/json não existe",
            )
        json_files = list(json_dir.glob("N4_*.json"))
        n4_count = len(json_files)
        if n4_count >= 162:
            status = "completo"
        elif n4_count >= 100:
            status = "parcial"
        elif n4_count > 0:
            status = "inicial"
        else:
            status = "vazio"
        passed = n4_count > 0
        return CheckResult(
            name="json_files",
            passed=passed,
            message=f"{n4_count} arquivos N4 encontrados ({status})",
            detail=f"Diretório: {json_dir.relative_to(self.project_root)}",
            warnings=[] if n4_count >= 162 else [
                f"Esperado 162 arquivos N4, encontrado {n4_count}"
            ],
        )

    def check_python_imports(self) -> CheckResult:
        """Verifica se os módulos Python podem ser importados."""
        import_errors = []
        import_success = []
        modules_to_check = [
            ("core.agent_base", "Agent Base"),
            ("core.ontology_graph", "Ontology Graph"),
            ("runtime.classifier", "Classifier"),
            ("runtime.router", "Router"),
            ("runtime.retriever", "Retriever"),
            ("runtime.synthesizer", "Synthesizer"),
            ("runtime.validator", "Validator"),
        ]
        for module, name in modules_to_check:
            try:
                __import__(module)
                import_success.append(name)
            except ImportError as e:
                import_errors.append(f"{name}: {e}")
        passed = len(import_errors) == 0
        return CheckResult(
            name="python_imports",
            passed=passed,
            message=f"{len(import_success)}/{len(modules_to_check)} imports OK"
                    + (f" | Erros: {'; '.join(import_errors)}" if import_errors else ""),
            detail=f"OK: {', '.join(import_success)}" if import_success else "",
            warnings=import_errors,
        )

    def check_dependencies(self) -> CheckResult:
        """Verifica dependências Python críticas."""
        required_packages = {
            "numpy": "numpy",
            "networkx": "networkx",
            "sklearn": "scikit-learn",
            "yaml": "pyyaml",
        }
        missing = []
        found = []
        for module, package in required_packages.items():
            try:
                __import__(module)
                found.append(package)
            except ImportError:
                missing.append(package)
        try:
            import sentence_transformers
            found.append("sentence-transformers")
        except ImportError:
            pass
        passed = len(missing) == 0
        return CheckResult(
            name="dependencies",
            passed=passed,
            message=f"{len(found)} pacotes encontrados"
                    + (f" | Faltando: {', '.join(missing)}" if missing else ""),
            detail=f"Instalados: {', '.join(found)}",
            warnings=[f"Instale: pip install {p}" for p in missing] if missing else [],
        )

    def check_graph_integrity(self) -> CheckResult:
        """Verifica a integridade do grafo ontológico."""
        try:
            import networkx as nx
            from core.ontology_graph import OntologyGraph

            json_dir = str(self.project_root / "data" / "json")
            if not Path(json_dir).exists():
                return CheckResult(
                    name="graph_integrity",
                    passed=False,
                    message="Diretório data/json não existe para carregar grafo",
                )

            graph = OntologyGraph(json_dir=json_dir)
            graph.load_registry()
            graph.build_graph()

            n_nodes = graph.G.number_of_nodes()
            n_edges = graph.G.number_of_edges()

            if n_nodes >= 162:
                passed = True
                message = f"Grafo íntegro: {n_nodes} nós, {n_edges} arestas"
            else:
                passed = False
                message = f"Grafo incompleto: {n_nodes} nós (esperado ≥162)"

            if n_nodes > 0:
                weakly_connected = len(list(nx.weakly_connected_components(graph.G)))
                if weakly_connected == 1:
                    message += " | Grafo conexo"
                else:
                    message += f" | {weakly_connected} componentes desconexos"

            return CheckResult(
                name="graph_integrity",
                passed=passed,
                message=message,
                detail=f"Nós: {n_nodes}, Arestas: {n_edges}",
            )
        except Exception as e:
            return CheckResult(
                name="graph_integrity",
                passed=False,
                message=f"Erro ao verificar grafo: {e}",
            )

    def check_classifier_readiness(self) -> CheckResult:
        """Verifica se o classificador pode ser inicializado."""
        try:
            from runtime.classifier import OntologicalClassifier
            classifier = OntologicalClassifier()
            n_concepts = len(classifier.registry) if hasattr(classifier, 'registry') else 0
            if n_concepts > 0:
                return CheckResult(
                    name="classifier_readiness",
                    passed=True,
                    message=f"Classificador pronto: {n_concepts} conceitos indexados",
                )
            else:
                return CheckResult(
                    name="classifier_readiness",
                    passed=True,
                    message="Classificador inicializado (sem dados de índice, usará fallback)",
                    warnings=["Classificação pode ser limitada sem índice de keywords"],
                )
        except Exception as e:
            return CheckResult(
                name="classifier_readiness",
                passed=False,
                message=f"Erro ao inicializar classificador: {e}",
            )

    def check_retriever_readiness(self) -> CheckResult:
        """Verifica se o retriever pode ser inicializado."""
        try:
            from runtime.retriever import HybridRetriever

            embedding_dir = self.project_root / "data" / "embeddings"

            if not embedding_dir.exists():
                return CheckResult(
                    name="retriever_readiness",
                    passed=False,
                    message="Diretório de embeddings não encontrado",
                    warnings=["Crie embeddings antes de usar retrieval vetorial"],
                )
            retriever = HybridRetriever(
                embedding_dir=str(embedding_dir),
            )
            n_loaded = len(retriever.embeddings) if hasattr(retriever, 'embeddings') else 0
            return CheckResult(
                name="retriever_readiness",
                passed=n_loaded > 0,
                message=f"Retriever carregou {n_loaded} embeddings" if n_loaded > 0
                        else "Retriever inicializado sem embeddings",
                warnings=[] if n_loaded > 0 else [
                    "Nenhum embedding carregado — retrieval vetorial limitado"
                ],
            )
        except Exception as e:
            return CheckResult(
                name="retriever_readiness",
                passed=False,
                message=f"Erro ao inicializar retriever: {e}",
            )

    def run_all_checks(self) -> Dict[str, CheckResult]:
        """Executa todas as verificações e retorna resultados."""
        checks = [
            self.check_core_modules,
            self.check_runtime_modules,
            self.check_agent_modules,
            self.check_config_files,
            self.check_prompt_templates,
            self.check_data_directories,
            self.check_ontology_index,
            self.check_json_files,
            self.check_dependencies,
            self.check_python_imports,
            self.check_classifier_readiness,
            self.check_retriever_readiness,
        ]
        try:
            checks.append(self.check_graph_integrity)
        except Exception:
            pass

        for check_fn in checks:
            try:
                result = check_fn()
                self.results[result.name] = result
                if self.verbose:
                    icon = "✅" if result.passed else "❌"
                    logger.info(f"{icon} {result.name}: {result.message}")
                    for w in result.warnings:
                        logger.warning(f"   ⚠️  {w}")
            except Exception as e:
                self.results[check_fn.__name__] = CheckResult(
                    name=check_fn.__name__,
                    passed=False,
                    message=f"Erro durante verificação: {e}",
                )
        return self.results

    def summary(self) -> str:
        """Retorna resumo formatado dos resultados."""
        if not self.results:
            self.run_all_checks()
        total = len(self.results)
        passed = sum(1 for r in self.results.values() if r.passed)
        failed = total - passed
        lines = [
            "",
            "═" * 60,
            "  HEALTH CHECK SUMMARY — Kilo Code v3.0.0",
            "═" * 60,
        ]
        for name, result in self.results.items():
            icon = "✅" if result.passed else "❌"
            lines.append(f"  {icon} {name}: {result.message}")
        lines.append("─" * 60)
        lines.append(f"  Total: {total} | Passou: {passed} | Falhou: {failed}")
        if failed == 0:
            lines.append("  ✅ SISTEMA OPERACIONAL")
        else:
            lines.append(f"  ⚠️  {failed} verificação(ões) falhou(ram)")
        lines.append("═" * 60)
        return "\n".join(lines)
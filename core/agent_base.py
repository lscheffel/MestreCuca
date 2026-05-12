"""
AGENTE BASE — Classe fundamental para todos os agentes cognitivos.

Fornece:
- Memória de trabalho (working memory)
- Memória semântica (acesso ao registry ontológico)
- Memória de episódios (histórico de interações)
- Ferramentas de raciocínio (chain-of-thought, planning)
- Interface unificada de execução

Fase 7 do Roadmap da Ontologia Fractal.
"""

from __future__ import annotations

import json
import logging
import sys
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

# Resolução robusta do diretório raiz do projeto
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
if str(_PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT / "core"))


@dataclass
class AgentMessage:
    """Mensagem trocada entre agentes ou com o usuário."""
    role: str  # "user", "assistant", "tool", "agent"
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_agent: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "source_agent": self.source_agent,
        }


@dataclass
class AgentResult:
    """Resultado de uma execução de agente."""
    agent_name: str
    task: str
    output: Any
    confidence: float = 0.0
    latency_ms: float = 0.0
    reasoning_steps: List[str] = field(default_factory=list)
    used_tools: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "task": self.task,
            "output": self.output,
            "confidence": round(self.confidence, 4),
            "latency_ms": round(self.latency_ms, 2),
            "reasoning_steps": self.reasoning_steps,
            "used_tools": self.used_tools,
            "metadata": self.metadata,
            "errors": self.errors,
        }


@dataclass
class ToolSpec:
    """Especificação de uma ferramenta disponível para o agente."""
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    callable_fn: Optional[Callable] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
        }


@dataclass
class EpisodeEntry:
    """Entrada de memória de episódio — registra uma interação completa."""
    episode_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    query: str = ""
    classification: Optional[Dict[str, Any]] = None
    routing: Optional[Dict[str, Any]] = None
    retrieved_cells: List[str] = field(default_factory=list)
    synthesis: Optional[str] = None
    validation: Optional[Dict[str, Any]] = None
    feedback: Optional[Dict[str, Any]] = None
    latency_ms: float = 0.0
    quality_score: float = 0.0

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "timestamp": self.timestamp,
            "query": self.query,
            "classification": self.classification,
            "routing": self.routing,
            "retrieved_cells": self.retrieved_cells,
            "synthesis": self.synthesis,
            "validation": self.validation,
            "feedback": self.feedback,
            "latency_ms": self.latency_ms,
            "quality_score": self.quality_score,
        }


class AgentMemory:
    """Sistema de memória multi-camada para agentes cognitivos.

    Camadas:
    1. Working Memory — buffer volátil para contexto ativo da sessão
    2. Semantic Memory — acesso ao registry ontológico (162 células N4)
    3. Episode Memory — histórico de interações para auto-avaliação
    """

    def __init__(
        self,
        working_capacity: int = 500,
        episode_capacity: int = 10000,
        semantic_registry: Optional[Dict[str, dict]] = None,
    ):
        self.working_memory: deque = deque(maxlen=working_capacity)
        self.episode_capacity = episode_capacity
        self.episode_memory: List[EpisodeEntry] = []
        self.semantic_registry = semantic_registry or {}

    # ── Working Memory ──────────────────────────────────────────────

    def push_working(self, key: str, value: Any, ttl: int = 300) -> None:
        """Adiciona item à memória de trabalho."""
        self.working_memory.append({
            "key": key,
            "value": value,
            "expires_at": time.time() + ttl,
        })

    def get_working(self, key: str) -> Optional[Any]:
        """Recupera item da memória de trabalho."""
        now = time.time()
        for item in reversed(self.working_memory):
            if item["key"] == key:
                if item["expires_at"] > now:
                    return item["value"]
        return None

    def clear_working(self) -> None:
        """Limpa memória de trabalho."""
        self.working_memory.clear()

    # ── Episode Memory ──────────────────────────────────────────────

    def add_episode(self, entry: EpisodeEntry) -> None:
        """Registra um episódio na memória de longo prazo."""
        if len(self.episode_memory) >= self.episode_capacity:
            self.episode_memory = self.episode_memory[self.episode_capacity // 10:]
        self.episode_memory.append(entry)

    def get_recent_episodes(self, n: int = 10) -> List[EpisodeEntry]:
        """Retorna os n episódios mais recentes."""
        return self.episode_memory[-n:]

    def get_episodes_by_quality(self, min_score: float = 0.7) -> List[EpisodeEntry]:
        """Retorna episódios com qualidade acima do threshold."""
        return [e for e in self.episode_memory if e.quality_score >= min_score]

    def get_feedback_patterns(self) -> Dict[str, Any]:
        """Analisa padrões de feedback dos episódios."""
        if not self.episode_memory:
            return {"total_episodes": 0}

        scores = [e.quality_score for e in self.episode_memory]
        recent_count = min(10, len(scores))
        return {
            "total_episodes": len(self.episode_memory),
            "avg_quality": sum(scores) / len(scores),
            "min_quality": min(scores),
            "max_quality": max(scores),
            "recent_avg_quality": sum(scores[-recent_count:]) / recent_count,
        }

    # ── Semantic Memory ─────────────────────────────────────────────

    def load_semantic_registry(self, registry: Dict[str, dict]) -> None:
        """Carrega o registry ontológico na memória semântica."""
        self.semantic_registry = registry

    def get_cell(self, uid: str) -> Optional[dict]:
        """Recupera uma célula N4 pelo UID."""
        return self.semantic_registry.get(uid)

    def search_cells_by_pilar(self, pilar: str) -> List[dict]:
        """Busca células por pilar ontológico."""
        return [
            cell for cell in self.semantic_registry.values()
            if cell.get("pilar", "").upper() == pilar.upper()
        ]

    def search_cells_by_dominio(self, dominio: str) -> List[dict]:
        """Busca células por domínio ontológico."""
        return [
            cell for cell in self.semantic_registry.values()
            if cell.get("dominio", "").upper() == dominio.upper()
        ]


class BaseAgent:
    """Classe base para todos os agentes cognitivos do sistema.

    Cada agente especializado herda desta classe e implementa:
    - execute(): lógica principal de processamento
    - get_capabilities(): descrição das capacidades
    """

    AGENT_NAME: str = "base"
    AGENT_VERSION: str = "1.0.0"
    REQUIRED_TOOLS: List[str] = []

    def __init__(
        self,
        name: Optional[str] = None,
        memory: Optional[AgentMemory] = None,
        tools: Optional[List[ToolSpec]] = None,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.name = name or self.AGENT_NAME
        self.version = self.AGENT_VERSION
        self.memory = memory or AgentMemory()
        self.tools: Dict[str, ToolSpec] = {}
        self.config = config or {}
        self._execution_log: List[Dict[str, Any]] = []

        if tools:
            for tool in tools:
                self.register_tool(tool)

        logger.info(
            "Agente '%s' v%s inicializado.", self.name, self.version
        )

    # ── Tool Management ─────────────────────────────────────────────

    def register_tool(self, tool: ToolSpec) -> None:
        """Registra uma ferramenta disponível para o agente."""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[ToolSpec]:
        """Recupera uma ferramenta registrada."""
        return self.tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """Lista todas as ferramentas disponíveis."""
        return [t.to_dict() for t in self.tools.values()]

    # ── Execution ───────────────────────────────────────────────────

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> AgentResult:
        """Executa uma tarefa. Deve ser sobrescrito pelas subclasses.

        Args:
            task: Descrição da tarefa a ser executada.
            context: Contexto adicional para execução.

        Returns:
            AgentResult com o resultado da execução.
        """
        raise NotImplementedError(
            f"Agente '{self.name}' não implementa execute()."
        )

    def _run_with_timing(self, func: Callable, *args: Any, **kwargs: Any) -> tuple[Any, float]:
        """Executa uma função com medição de latência."""
        t0 = time.time()
        result = func(*args, **kwargs)
        latency_ms = (time.time() - t0) * 1000
        return result, latency_ms

    def _log_execution(self, result: AgentResult) -> None:
        """Registra execução no log interno."""
        entry = {
            "timestamp": time.time(),
            "task": result.task,
            "output_summary": str(result.output)[:200],
            "confidence": result.confidence,
            "latency_ms": result.latency_ms,
            "errors": result.errors,
        }
        self._execution_log.append(entry)

    # ── Reasoning Helpers ───────────────────────────────────────────

    def chain_of_thought(self, question: str, steps: int = 3) -> List[str]:
        """Gera uma cadeia de raciocínio passo a passo.

        Retorna uma lista de etapas de raciocínio para decompor
        uma questão complexa.
        """
        reasoning: List[str] = []
        for step_index in range(steps):
            reasoning.append(
                f"Passo {step_index + 1}: Analisar aspecto {step_index + 1} de '{question}'"
            )
        return reasoning

    def plan_tasks(self, goal: str, subtasks: List[str]) -> List[Dict[str, Any]]:
        """Cria um plano de execução a partir de um objetivo e subtarefas."""
        plan: List[Dict[str, Any]] = []
        for i, subtask in enumerate(subtasks, 1):
            plan.append({
                "step": i,
                "task": subtask,
                "status": "pending",
                "depends_on": [],
            })
        return plan

    # ── Capabilities ────────────────────────────────────────────────

    def get_capabilities(self) -> Dict[str, Any]:
        """Retorna as capacidades do agente."""
        return {
            "name": self.name,
            "version": self.version,
            "tools": self.list_tools(),
            "required_tools": self.REQUIRED_TOOLS,
        }

    def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do agente."""
        return {
            "agent": self.name,
            "version": self.version,
            "tools_registered": len(self.tools),
            "memory_episodes": len(self.memory.episode_memory),
            "memory_working": len(self.memory.working_memory),
            "status": "healthy",
        }
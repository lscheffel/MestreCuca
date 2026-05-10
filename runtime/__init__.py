"""Runtime — Motor de Execução Ontológica.

Pacote principal do runtime que orquestra os motores de inferência,
retrieval híbrido e execução de prompts baseados na ontologia fractal.
"""

__version__ = "3.0.0"
__all__ = ["HybridRetriever"]

from runtime.retriever import HybridRetriever
# -*- coding: utf-8 -*-
"""Fixtures pytest para os testes do classificador ontológico."""

import pytest
from pathlib import Path

# Garantir que o projeto root está no sys.path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "tools"))
if str(PROJECT_ROOT / "core") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "core"))

from runtime.classifier import OntologicalClassifier


@pytest.fixture(scope="module")
def clf() -> OntologicalClassifier:
    """Instancia o classificador com dados reais do projeto."""
    classifier = OntologicalClassifier(
        json_dir=str(PROJECT_ROOT / "data" / "json"),
        embedding_dir=str(PROJECT_ROOT / "data" / "embeddings"),
    )
    # Warm-up para evitar latência no primeiro teste
    classifier.warm_up()
    return classifier
# AGENTS.md — tests/

> Testes automatizados com pytest.  
> Regras globais em `../AGENTS.md`. Este arquivo só contém o que é específico de `tests/`.

---

## Estrutura

```
tests/
├── conftest.py          # fixtures compartilhadas — adicionar fixtures aqui, não nos arquivos de teste
├── test_classifier.py   # OntologicalClassifier
├── test_ontology.py     # OntologyGraph e módulos de core/
├── run_diag.py          # diagnóstico integrado — não é suite de teste
└── diag_data.py         # diagnóstico de dados — não é suite de teste
```

---

## TDD — Ordem Obrigatória

```
1. Escrever o teste (falha esperada)
2. Rodar → confirmar que falha pelo motivo certo
3. Implementar o mínimo para passar
4. Refatorar mantendo o teste verde
```

Nunca criar código em `core/` ou `runtime/` sem um teste correspondente em `tests/`.

---

## Convenções pytest

```python
# Nome de arquivo: test_<modulo>.py
# Nome de função:  test_<comportamento_esperado>

# ✅ Bom
def test_classifier_retorna_n4_para_query_algoritmica():
    ...

def test_retriever_lanca_erro_se_indice_nao_existe():
    ...

# ❌ Ruim
def test_1():
    ...

def test_classifier():  # vago demais
    ...
```

- Cobertura mínima: **80%** para `core/` e `runtime/`
- Testes devem ser **determinísticos** — sem dependência de rede, clock ou ordem de execução
- Usar fixtures de `conftest.py` para estado compartilhado (grafo carregado, config, paths)
- Mocks em `unittest.mock` — nunca em arquivos separados ad-hoc

---

## Fixtures — conftest.py

```python
# conftest.py — padrão de fixture
import pytest
from pathlib import Path
from core.ontology_graph import OntologyGraph

@pytest.fixture(scope="session")
def ontology_graph():
    """Grafo carregado uma vez por sessão de testes."""
    graph = OntologyGraph(config_path=Path("config/ontology.yaml"))
    graph.load()
    return graph

@pytest.fixture
def sample_query():
    return "como decompor um problema complexo em partes menores?"
```

- `scope="session"` para recursos custosos (grafo, índice FAISS)
- `scope="function"` (padrão) para estado que precisa ser isolado
- Nunca criar fixtures dentro dos arquivos de teste — sempre em `conftest.py`

---

## Rodando Testes

```powershell
# Suite completa
python -m pytest tests/ -v

# Módulo específico
python -m pytest tests/test_classifier.py -v

# Teste específico
python -m pytest tests/test_classifier.py::test_classifier_retorna_n4 -v

# Com cobertura
python -m pytest tests/ --cov=core --cov=runtime --cov-report=term-missing

# Parar no primeiro erro
python -m pytest tests/ -x
```

---

## O que NÃO é teste

- `run_diag.py` e `diag_data.py` dentro de `tests/` são scripts de diagnóstico — não fazem parte da suite pytest
- `ONTO_ENGINE_ROADMAP-DEEP.md` é documentação — não executar
- Não criar scripts `_*.py` aqui — diagnósticos temporários ficam na raiz
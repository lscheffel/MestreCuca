"""
Testes para o sistema cognitivo ontológico.

Executar:
    python -m pytest tests/ -v
"""

import pytest
import sys
import os

# Adicionar root ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestOntologyStructure:
    """Testes de estrutura da ontologia."""

    def test_directories_exist(self):
        """Verifica se todos os diretórios da ontologia existem."""
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dirs = [
            "ontology/n0", "ontology/n1", "ontology/n2",
            "ontology/n3", "ontology/n4",
            "data/json", "data/embeddings", "data/indexes", "data/graphs",
            "runtime", "core", "tools", "tests",
            "prompts/classifier", "prompts/retrieval",
            "prompts/synthesis", "prompts/validation", "prompts/routing",
            ".kilo/agents", ".kilo/memory", ".kilo/orchestrators",
            ".kilo/prompts/classifier", ".kilo/prompts/retrieval",
            ".kilo/prompts/synthesis", ".kilo/prompts/validation",
            ".kilo/prompts/routing",
        ]
        for d in dirs:
            assert os.path.isdir(os.path.join(base, d)), f"Diretório ausente: {d}"

    def test_yaml_files_parseable(self):
        """Verifica se todos os YAMLs são parseáveis."""
        import yaml
        import glob

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_files = glob.glob(os.path.join(base, "config", "*.yaml"))
        yaml_files += glob.glob(os.path.join(base, ".kilo", "**", "*.yaml"), recursive=True)
        yaml_files += glob.glob(os.path.join(base, "prompts", "**", "*.yaml"), recursive=True)
        yaml_files += glob.glob(os.path.join(base, "runtime", "*.yaml"))

        assert len(yaml_files) > 0, "Nenhum arquivo YAML encontrado"

        for f in yaml_files:
            with open(f, "r", encoding="utf-8") as fh:
                try:
                    yaml.safe_load(fh)
                except yaml.YAMLError as e:
                    pytest.fail(f"Erro ao parsear {f}: {e}")

    def test_requirements_txt_exists(self):
        """Verifica se requirements.txt existe e é parseável."""
        import os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        req_path = os.path.join(base, "requirements.txt")
        assert os.path.isfile(req_path), "requirements.txt não encontrado"

        with open(req_path, "r") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
            assert len(lines) > 0, "requirements.txt está vazio"
            for line in lines:
                assert ">=" in line or "==" in line, f"Dependência mal formatada: {line}"

    def test_ontology_yaml_structure(self):
        """Verifica estrutura básica do ontology.yaml."""
        import yaml
        import os

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/ontology.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "n0_vetores" in data, "n0_vetores ausente"
        assert "n1_pilares" in data, "n1_pilares ausente"
        assert "n2_dominios" in data, "n2_dominios ausente"
        assert "n3_sub_arvores" in data, "n3_sub_arvores ausente"
        assert "n4_celulas" in data, "n4_celulas ausente"

        # Verificar contagem
        assert len(data["n0_vetores"]) == 2, f"Esperado 2 vetores, encontrado {len(data['n0_vetores'])}"
        assert len(data["n1_pilares"]) == 6, f"Esperado 6 pilares, encontrado {len(data['n1_pilares'])}"
        assert len(data["n2_dominios"]) == 18, f"Esperado 18 domínios, encontrado {len(data['n2_dominios'])}"
        assert len(data["n3_sub_arvores"]) == 54, f"Esperado 54 subárvores, encontrado {len(data['n3_sub_arvores'])}"
        assert len(data["n4_celulas"]) == 162, f"Esperado 162 células N4, encontrado {len(data['n4_celulas'])}"


class TestEmbeddingConfig:
    """Testes de configuração de embeddings."""

    def test_embedding_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/embedding.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "modelo" in data
        assert data["modelo"]["dimensao"] == 384
        assert "vetores_pesos" in data
        assert sum(data["vetores_pesos"].values()) == pytest.approx(1.0, 0.01)


class TestRetrievalConfig:
    """Testes de configuração de retrieval."""

    def test_retrieval_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/retrieval.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "vetorial" in data
        assert "grafico" in data
        assert "simbolico" in data
        assert "fusao" in data
        assert data["fusao"]["pesos"]["vetorial"] == 0.50
        assert data["fusao"]["pesos"]["grafico"] == 0.30
        assert data["fusao"]["pesos"]["simbolico"] == 0.20
        assert pytest.approx(sum(data["fusao"]["pesos"].values()), 0.01) == 1.0


class TestGraphConfig:
    """Testes de configuração do grafo."""

    def test_graph_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, "config/graph.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "grafo" in data
        assert data["grafo"]["engine"] == "networkx"
        assert data["grafo"]["tipo"] == "MultiDiGraph"
        assert "persistencia" in data["grafo"]
        assert "algoritmos" in data["grafo"]


class TestAgentConfigs:
    """Testes de configuração dos agentes."""

    def test_agents_yaml_valid(self):
        import yaml, os
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        with open(os.path.join(base, ".kilo/agents/agents.yaml"), "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        assert "agentes" in data
        expected_agents = ["classificador", "retriever", "sintetizador", "validador", "roteador"]
        for agent in expected_agents:
            assert agent in data["agentes"], f"Agente ausente: {agent}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

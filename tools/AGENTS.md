# AGENTS.md — tools/

> Utilitários de geração e validação de artefatos ontológicos.  
> Regras globais em `../AGENTS.md`. Este arquivo só contém o que é específico de `tools/`.

---

## Responsabilidade dos Tools

| Script | Função | Output |
|---|---|---|
| `n4_to_json.py` | Converte `.md` N4 → JSON estruturado | `data/json/N4_*.json` |
| `build_embeddings.py` | Gera vetores 384-dim via `all-MiniLM-L6-v2` | `data/embeddings/N4_*.npy` |
| `embedding_builder.py` | Builder alternativo de embeddings | `data/embeddings/` |
| `graph_builder.py` | Constrói grafo NetworkX e serializa | `data/graphs/ontology.gexf` |
| `canonical_document_builder.py` | Gera documentos canônicos por célula | `data/` |
| `enrich_json.py` | Enriquece JSONs N4 com metadados extras | `data/json/` |
| `validate_deep.py` | Validação profunda de consistência ontológica | stdout |
| `validate_fase1.py` | Validação da fase 1 do pipeline | stdout |
| `inspect_json.py` | Inspeciona estrutura de um JSON N4 | stdout |
| `uid_generator.py` | Gera UIDs únicos para células | stdout |
| `e2e_test.py` | Teste end-to-end do pipeline completo | stdout |

---

## Fluxo de Geração de Artefatos

```
data/ontology/N4-*.md          # fontes Markdown das células
        ↓  tools/n4_to_json.py
data/json/N4_*.json            # JSONs estruturados
        ↓  tools/build_embeddings.py
data/embeddings/N4_*.npy       # vetores 384-dim
        ↓  tools/graph_builder.py
data/graphs/ontology.gexf      # grafo serializado
```

**Nunca editar `data/` manualmente.** Se um artefato estiver incorreto, corrigir a fonte e regenerar.

---

## Rodando os Tools

```powershell
# Regenerar todos os JSONs a partir dos .md
python tools/n4_to_json.py

# Regenerar embeddings (requer JSONs atualizados)
python tools/build_embeddings.py

# Regenerar grafo (requer JSONs atualizados)
python tools/graph_builder.py

# Validação profunda
python tools/validate_deep.py

# Inspecionar um JSON específico
python tools/inspect_json.py data/json/N4_ALGORITMIA_1_A.json

# Teste end-to-end
python tools/e2e_test.py
```

---

## Regras de Desenvolvimento

- Tools são **utilitários de build** — não fazem parte do pipeline de produção (`run_kilo.py`)
- Cada tool deve ser executável standalone: `python tools/nome.py`
- Output sempre para `data/` — nunca para a raiz ou outros diretórios
- Sempre verificar se `data/` existe e tem permissão de escrita antes de gravar
- Logar progresso com `print()` simples — `rich` é opcional aqui

```python
# ✅ Padrão mínimo de um tool
from pathlib import Path
import sys

DATA_DIR = Path("data/json")
ONTOLOGY_DIR = Path("data/ontology")

def main():
    if not ONTOLOGY_DIR.exists():
        print(f"[✗] Diretório não encontrado: {ONTOLOGY_DIR}")
        sys.exit(1)

    arquivos = list(ONTOLOGY_DIR.glob("N4-*.md"))
    print(f"[→] Processando {len(arquivos)} arquivos N4...")

    for i, arquivo in enumerate(arquivos, 1):
        print(f"[{i}/{len(arquivos)}] {arquivo.name}")
        # processar...

    print(f"[✓] Concluído — {len(arquivos)} artefatos gerados em {DATA_DIR}")

if __name__ == "__main__":
    main()
```

---

## Antes de Criar um Tool Novo

1. Verificar se já existe algo equivalente na lista acima
2. Verificar se `scripts/` não tem o script adequado
3. Se criar: nomear descritivamente (`verbo_objeto.py`), nunca `_*.py`
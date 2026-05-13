"""
Organização dos arquivos de docs/ por contexto.

Classificação analisada:

1. **arquitetura/** — Arquitetura geral do sistema, design, CORE, DSL
2. **agentes-prompts/** — Design de agentes LLM, prompts, orquestração
3. **ontologia-taxonomia/** — Definições ontológicas, taxonomia N3/N4, diagramas
4. **runtime-pipeline/** — Documentação de runtime e pipeline de execução
5. **auditoria-qualidade/** — Auditorias, verificações, conformidade
6. **planejamento-roadmap/** — Planos estratégicos, roadmaps, sumários
7. **referencia-historico/** — Documentação deprecada, referência histórica
8. **uso-documentacao/** — Manuais de uso, guias de usuário
"""
import shutil
from pathlib import Path

ROOT = Path("E:/Arquivos/Área de Trabalho/MestreCuca")
DOCS = ROOT / "docs"
log = []

# Definição das categorias e arquivos
categorias = {
    "arquitetura": [
        "arquitetura_sistema_cognitivo.md",
        "arquitetura_sistema_cognitivo.pdf",
        "arquitetura_cognitiva_v3.md",
        "CORE.md",
        "CORE2.md",
        "DSL.md",
    ],
    "agentes-prompts": [
        "AGENTE - ARQUITETO DE PROMPTS FINAL V1.md",
        "agente_arquiteto_prompts_v_1_1_consolidado.md",
        "agente_arquiteto_prompts_v_2_arquitetura_cognitiva_consolidada.md",
        "ARQUITETO_PROMPTS_FINAL.md",
        "PROMPT_MODULAR_N3.md",
        "gpt 0.1 - arquiteto.md",
        "gpt 1.0 - arquiteto.md",
        "gpt 1.0.md",
    ],
    "ontologia-taxonomia": [
        "ONTOLOGIA_MESTRA_DOMINANTE_V1.md",
        "ONTOLOGIA_MESTRA_DOMINANTE_V2.md",
        "Taxonomia_Ontologica.md",
        "taxon_ontology_tree.mmd",
        "relatorio_analise_ontologia.md",
        "plano_transformacao_n4_json.md",
        "expansao_fractal_n3.md",
        "checklist_recursivo_N3.md",
    ],
    "runtime-pipeline": [
        "RUNTIME.md",
    ],
    "auditoria-qualidade": [
        "auditoria_discrepancias_ontologicas.md",
    ],
    "planejamento-roadmap": [
        "plan.md",
        "roadmap.md",
        "SUMARIO_EXECUTIVO_MUDANÇAS.md",
    ],
    "referencia-historico": [
        "AGENTS (deprecated).md",
    ],
    "uso-documentacao": [
        "USAGE.md",
        "USAGE.pdf",
    ],
}

print("=" * 60)
print("ORGANIZAÇÃO DE docs/ POR CONTEXTO")
print("=" * 60)

# Criar subdiretórios
for cat in categorias:
    dest_dir = DOCS / cat
    dest_dir.mkdir(exist_ok=True)
    print(f"  CRIADO: docs/{cat}/")

# Mover arquivos
for cat, arquivos in categorias.items():
    dest_dir = DOCS / cat
    for arq in arquivos:
        src = DOCS / arq
        if src.exists():
            shutil.move(str(src), str(dest_dir / arq))
            log.append(f"MOVIDO: {arq} → docs/{cat}/{arq}")
            print(f"  MOVIDO: {arq} → docs/{cat}/")
        else:
            print(f"  ⚠️  NÃO ENCONTRADO: {arq}")

# O subdiretório roadmap/ já existe dentro de docs/ — mover para planejamento-roadmap/
roadmap_src = DOCS / "roadmap"
roadmap_dest = DOCS / "planejamento-roadmap" / "roadmap"
if roadmap_src.exists():
    shutil.move(str(roadmap_src), str(roadmap_dest))
    log.append(f"MOVIDO: roadmap/ → docs/planejamento-roadmap/roadmap/")
    print(f"  MOVIDO: roadmap/ → docs/planejamento-roadmap/")

# Salvar log
with open(ROOT / "_docs_reorg_log.txt", "w", encoding="utf-8") as f:
    f.write("Reorganização de docs/ por contexto\n")
    f.write("=" * 40 + "\n\n")
    for entry in log:
        f.write(entry + "\n")

print(f"\n✅ {len(log)} operações concluídas.")
print(f"Log salvo em: _docs_reorg_log.txt")

# Verificar se sobrou algo no docs/ raiz
print("\n=== Verificando itens restantes em docs/ ===")
restantes = list(DOCS.iterdir())
dirs_restantes = [d.name for d in restantes if d.is_dir()]
files_restantes = [f.name for f in restantes if f.is_file()]
if dirs_restantes:
    print(f"  Diretórios: {dirs_restantes}")
if files_restantes:
    print(f"  Arquivos: {files_restantes}")
if not dirs_restantes and not files_restantes:
    print("  Nenhum item restante (esperado apenas os subdiretórios criados)")
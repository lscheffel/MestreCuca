"""
Script de reorganização do root do projeto MestreCuca.
Move arquivos soltos para seus diretórios adequados conforme o relatório
de classificação aprovado pelo usuário.
"""
import shutil
from pathlib import Path

ROOT = Path("E:/Arquivos/Área de Trabalho/MestreCuca")
log = []

def move_file(src_name, dest_dir, dest_name=None):
    src = ROOT / src_name
    dest = ROOT / dest_dir / (dest_name or src_name)
    if src.exists():
        shutil.move(str(src), str(dest))
        log.append(f"MOVIDO: {src_name} → {dest_dir}/{(dest_name or src_name)}")
    else:
        log.append(f"⚠️  NÃO ENCONTRADO: {src_name}")

def delete_file(name):
    path = ROOT / name
    if path.exists():
        path.unlink()
        log.append(f"DELETADO: {name}")
    else:
        log.append(f"⚠️  NÃO ENCONTRADO: {name}")

# === 1. Mover para docs/ (26 arquivos) ===
docs_files = [
    "AGENTE - ARQUITETO DE PROMPTS FINAL V1.md",
    "agente_arquiteto_prompts_v_1_1_consolidado.md",
    "agente_arquiteto_prompts_v_2_arquitetura_cognitiva_consolidada.md",
    "AGENTS (deprecated).md",
    "ARQUITETO_PROMPTS_FINAL.md",
    "arquitetura_cognitiva_v3.md",
    "auditoria_discrepancias_ontologicas.md",
    "checklist_recursivo_N3.md",
    "CORE.md",
    "CORE2.md",
    "DSL.md",
    "expansao_fractal_n3.md",
    "gpt 0.1 - arquiteto.md",
    "gpt 1.0 - arquiteto.md",
    "gpt 1.0.md",
    "ONTOLOGIA_MESTRA_DOMINANTE_V1.md",
    "ONTOLOGIA_MESTRA_DOMINANTE_V2.md",
    "plan.md",
    "plano_transformacao_n4_json.md",
    "PROMPT_MODULAR_N3.md",
    "relatorio_analise_ontologia.md",
    "roadmap.md",
    "RUNTIME.md",
    "SUMARIO_EXECUTIVO_MUDANÇAS.md",
    "taxon_ontology_tree.mmd",
    "Taxonomia_Ontologica.md",
]

print("=" * 60)
print("FASE 1: Movendo documentação para docs/")
print("=" * 60)
for f in docs_files:
    move_file(f, "docs")

# === 2. Mover para scripts/ (9 arquivos) ===
scripts_files = [
    "create_n3_files.py",
    "create_n3_files_v2.py",
    "create_n4_files.py",
    "create_n4_from_taxonomy.py",
    "create_n4_manual.py",
    "padronizador.py",
    "reestruturar_n4.py",
    "run_diag.bat",
    "run_test.bat",
]

print("\n" + "=" * 60)
print("FASE 2: Movendo scripts para scripts/")
print("=" * 60)
for f in scripts_files:
    move_file(f, "scripts")

# === 3. Mover para tests/ (2 arquivos) ===
tests_files = [
    "test_fase3",
    "test_retrieval.py",
]

print("\n" + "=" * 60)
print("FASE 3: Movendo testes para tests/")
print("=" * 60)
for f in tests_files:
    move_file(f, "tests")

# === 4. Mover para data/ (1 arquivo) ===
print("\n" + "=" * 60)
print("FASE 4: Movendo dados para data/")
print("=" * 60)
move_file("taxo.txt", "data")

# === 5. Deletar null ===
print("\n" + "=" * 60)
print("FASE 5: Removendo arquivo 'null'")
print("=" * 60)
delete_file("null")

# === 6. Remover script temporário de varredura ===
print("\n" + "=" * 60)
print("FASE 6: Removendo scripts temporários de varredura")
print("=" * 60)
delete_file("_scan_tree.py")
delete_file("_tree_output.txt")

# === Resumo ===
print("\n" + "=" * 60)
print("RESUMO DA EXECUÇÃO")
print("=" * 60)
movidos = [l for l in log if l.startswith("MOVIDO")]
deletados = [l for l in log if l.startswith("DELETADO")]
nao_encontrados = [l for l in log if l.startswith("⚠️")]

for entry in log:
    print(f"  {entry}")

print(f"\nTotal movido: {len(movidos)}")
print(f"Total deletado: {len(deletados)}")
print(f"Não encontrados: {len(nao_encontrados)}")
print("\n✅ Reorganização concluída!")

# Salvar log
with open(ROOT / "_reorg_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print(f"Log salvo em: _reorg_log.txt")
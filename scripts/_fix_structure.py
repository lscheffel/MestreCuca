#!/usr/bin/env python3
"""
Script de correção de problemas identificados na estrutura do root.
Problemas:
  1. Arquivos soltos em data/ → mover para destinos corretos
  2. ONTO_ENGINE_ROADMAP-DEEP.md em tests/ → mover para docs/planejamento-roadmap/
  3. .bat em scripts/ → remover (conforme AGENTS.md: preferir Python direto)
  4. Diagnósticos _diag_*.py em runtime/ → mover para scripts/
  5. data/indexes/ vazio → remover
"""

import shutil
from pathlib import Path
from datetime import datetime

BASE = Path("E:/Arquivos/Área de Trabalho/MestreCuca")
LOG = []

def log(msg):
    LOG.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    print(msg)

def safe_move(src, dst):
    src_path = BASE / src
    dst_path = BASE / dst
    if not src_path.exists():
        log(f"  ⚠️  {src} não existe — ignorado")
        return False
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    if dst_path.exists():
        # Evitar sobrescrever
        backup = dst_path.with_suffix(dst_path.suffix + '.bak')
        shutil.move(str(dst_path), str(backup))
        log(f"  ⚠️  {dst} já existia — backup em {backup}")
    shutil.move(str(src_path), str(dst_path))
    log(f"  ✅ {src} → {dst}")
    return True

def safe_delete(path):
    p = BASE / path
    if not p.exists():
        log(f"  ⚠️  {path} não existe — ignorado")
        return False
    if p.is_dir():
        shutil.rmtree(str(p))
    else:
        p.unlink()
    log(f"  🗑️  {path} removido")
    return True

# ==========================================
# CORREÇÃO 1: Arquivos soltos em data/
# ==========================================
log("=" * 60)
log("CORREÇÃO 1: Movendo arquivos soltos de data/")

# semantic_expansion_report.md → docs/runtime-pipeline/
safe_move("data/semantic_expansion_report.md", "docs/runtime-pipeline/semantic_expansion_report.md")

# taxo.txt → docs/ontologia-taxonomia/
safe_move("data/taxo.txt", "docs/ontologia-taxonomia/taxo.txt")

# test_results.csv e test_results.json → tests/
safe_move("data/test_results.csv", "tests/test_results.csv")
safe_move("data/test_results.json", "tests/test_results.json")

# ==========================================
# CORREÇÃO 2: ONTO_ENGINE_ROADMAP-DEEP.md
# ==========================================
log("=" * 60)
log("CORREÇÃO 2: Movendo documentação de tests/ para docs/")

safe_move("tests/ONTO_ENGINE_ROADMAP-DEEP.md", "docs/planejamento-roadmap/ONTO_ENGINE_ROADMAP-DEEP.md")

# ==========================================
# CORREÇÃO 3: .bat em scripts/
# ==========================================
log("=" * 60)
log("CORREÇÃO 3: Removendo .bat de scripts/ (conforme AGENTS.md)")

safe_delete("scripts/run_diag.bat")
safe_delete("scripts/run_test.bat")

# ==========================================
# CORREÇÃO 4: Diagnósticos em runtime/
# ==========================================
log("=" * 60)
log("CORREÇÃO 4: Movendo diagnósticos de runtime/ para scripts/")

safe_move("runtime/_diag_check_celulas.py", "scripts/_diag_check_celulas.py")
safe_move("runtime/_diag_validator4.py", "scripts/_diag_validator4.py")
safe_move("runtime/_diag_validator5.py", "scripts/_diag_validator5.py")

# ==========================================
# CORREÇÃO 5: data/indexes/ vazio
# ==========================================
log("=" * 60)
log("CORREÇÃO 5: Removendo data/indexes/ vazio")

safe_delete("data/indexes")

# ==========================================
# RELATÓRIO FINAL
# ==========================================
log("=" * 60)
log("CORREÇÕES CONCLUÍDAS")
log(f"Total de operações: {len(LOG) - 3}")  # descontar cabeçalhos

# Salvar log
log_path = BASE / "scripts/_correction_log.txt"
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(LOG))

print(f"\n✅ Log salvo em: {log_path}")
"""
Ajustes finais pós-reorganização:
1. Mover scripts auxiliares do root para scripts/
2. Renomear test_fase3 → test_fase3.py
"""
import shutil
from pathlib import Path

ROOT = Path("E:/Arquivos/Área de Trabalho/MestreCuca")
log = []

# 1. Mover scripts auxiliares para scripts/
aux_files = [
    "_scan_tree.py",
    "_reorg_root.py",
    "_verify_tree.py",
    "_reorg_log.txt",
]

print("=" * 60)
print("Movendo scripts auxiliares para scripts/")
print("=" * 60)
for f in aux_files:
    src = ROOT / f
    dest = ROOT / "scripts" / f
    if src.exists():
        shutil.move(str(src), str(dest))
        log.append(f"MOVIDO: {f} → scripts/{f}")
        print(f"  MOVIDO: {f} → scripts/{f}")
    else:
        print(f"  ⚠️  NÃO ENCONTRADO: {f}")

# 2. Renomear test_fase3 → test_fase3.py
src = ROOT / "tests" / "test_fase3"
dest = ROOT / "tests" / "test_fase3.py"
print("\n" + "=" * 60)
print("Renomeando test_fase3 → test_fase3.py")
print("=" * 60)
if src.exists():
    src.rename(dest)
    log.append(f"RENOMEADO: tests/test_fase3 → tests/test_fase3.py")
    print(f"  RENOMEADO: tests/test_fase3 → tests/test_fase3.py")
else:
    print(f"  ⚠️  NÃO ENCONTRADO: tests/test_fase3")

# Salvar log
with open(ROOT / "_reorg_log.txt", "a", encoding="utf-8") as f:
    f.write("\n# Ajustes finais pós-reorganização\n")
    f.write("\n".join(log))

print(f"\n✅ {len(log)} operações concluídas.")
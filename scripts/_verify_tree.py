from pathlib import Path

root = Path('E:/Arquivos/Área de Trabalho/MestreCuca')

lines = []
lines.append("=== ROOT LEVEL (final) ===")
for item in sorted(root.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
    if item.is_dir():
        lines.append(f"DIR:  {item.name}")
    else:
        lines.append(f"FILE: {item.name}")

# Subdiretórios não-ocultos
for subdir in sorted(root.iterdir()):
    if subdir.is_dir() and subdir.name not in ['.git', '.github', '.vscode', '.idea', '.pytest_cache', '__pycache__', 'data', 'ontology']:
        lines.append(f"\n=== {subdir.name}/ ===")
        try:
            for item in sorted(subdir.rglob('*'), key=lambda x: str(x.relative_to(subdir))):
                rel = item.relative_to(subdir)
                if item.is_dir():
                    lines.append(f"  DIR:  {rel}")
                else:
                    lines.append(f"  FILE: {rel}")
        except Exception as e:
            lines.append(f"  ERRO: {e}")

print("\n".join(lines))
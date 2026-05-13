from pathlib import Path

docs = Path("E:/Arquivos/Área de Trabalho/MestreCuca/docs")

lines = ["=== docs/ — Estrutura Final ==="]
for item in sorted(docs.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
    if item.is_dir():
        lines.append(f"DIR:  {item.name}")
        for sub in sorted(item.rglob("*"), key=lambda x: str(x.relative_to(item))):
            rel = sub.relative_to(item)
            if sub.is_dir():
                lines.append(f"  DIR:  {rel}")
            else:
                lines.append(f"  FILE: {rel}")
    else:
        lines.append(f"FILE: {item.name}")

print("\n".join(lines))

# Contagem
total_files = 0
total_dirs = 0
for item in docs.rglob("*"):
    if item.is_file():
        total_files += 1
    elif item.is_dir():
        total_dirs += 1

print(f"\nTotal de subdiretórios: {total_dirs}")
print(f"Total de arquivos: {total_files}")
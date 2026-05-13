#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix all hardcoded paths after moving N3/N4 files to data/ontology/
"""
import os, re, glob

base = os.getcwd()
ontology_dir = os.path.join(base, 'data', 'ontology')

def fix_filename_line(content):
    """Replace 'filename = f"N3-..." with 'filename = os.path.join("data", "ontology", f"N3-...")'"""
    pattern = r'^(\s*)filename = f"((?:N3|N4)-.*)"$'
    def replacer(m):
        indent = m.group(1)
        rest = m.group(2)
        return f'{indent}filename = os.path.join("data", "ontology", f"{rest}")'
    return re.sub(pattern, replacer, content, flags=re.MULTILINE)


# ============================================================
# 1. Fix _explore.py
# ============================================================
path = os.path.join(base, '_explore.py')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "glob.glob('N4-*.md')",
    "glob.glob(os.path.join('data', 'ontology', 'N4-*.md'))"
)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("[FIX] _explore.py")

# ============================================================
# 2. Fix padronizador.py
# ============================================================
path = os.path.join(base, 'padronizador.py')
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('glob.glob("N3-*.md")', 'glob.glob(os.path.join("data", "ontology", "N3-*.md"))')
content = content.replace('glob.glob("N4-*.md")', 'glob.glob(os.path.join("data", "ontology", "N4-*.md"))')
content = fix_filename_line(content)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("[FIX] padronizador.py")

# ============================================================
# 3-8. Fix all create/reestruturar scripts
# ============================================================
scripts = [
    'create_n3_files.py',
    'create_n3_files_v2.py',
    'create_n4_files.py',
    'create_n4_from_taxonomy.py',
    'create_n4_manual.py',
    'reestruturar_n4.py',
]
for name in scripts:
    path = os.path.join(base, name)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = fix_filename_line(content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[FIX] {name}")

# ============================================================
# 9. Fix N3 cross-references to ONTOLOGIA_MESTRA_DOMINANTE_V2.md
#    N3 files are now in data/ontology/, so need ../ prefix
# ============================================================
n3_files = sorted(glob.glob(os.path.join(ontology_dir, 'N3-*.md')))
fixed_count = 0
for n3_path in n3_files:
    with open(n3_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    old = '](ONTOLOGIA_MESTRA_DOMINANTE_V2.md'
    new = '](../ONTOLOGIA_MESTRA_DOMINANTE_V2.md'
    if old in content:
        content = content.replace(old, new)
        with open(n3_path, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed_count += 1
print(f"[FIX] N3 refs to ONTOLOGIA_MESTRA: {fixed_count} files updated")

# ============================================================
# 10. Verify N4 -> N3 references (same directory, should work)
# ============================================================
n4_files = sorted(glob.glob(os.path.join(ontology_dir, 'N4-*.md')))
n3_ref_count = 0
for n4_path in n4_files:
    with open(n4_path, 'r', encoding='utf-8') as f:
        content = f.read()
    refs = re.findall(r'`N3-[^`]+\.md`', content)
    n3_ref_count += len(refs)
print(f"[OK] N4 -> N3 refs: {n3_ref_count} references (same directory, no change needed)")

# ============================================================
# 11. Fix documentation references
# ============================================================
docs_to_fix = [
    os.path.join(base, 'ARQUITETO_PROMPTS_FINAL.md'),
    os.path.join(base, 'MEMORY.md'),
    os.path.join(base, 'checklist_recursivo_N3.md'),
    os.path.join(base, 'docs', 'arquitetura_sistema_cognitivo.md'),
]
for doc_path in docs_to_fix:
    if not os.path.exists(doc_path):
        print(f"[SKIP] {os.path.basename(doc_path)} not found")
        continue
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    # Fix template references in backticks: `N3-{ID}-{DOMÍNIO}-{SUBDOMÍNIO}.md`
    content = re.sub(
        r'`(N3)-\{ID\}-\{DOMÍNIO\}-\{SUBDOMÍNIO\}\.md`',
        r'`data/ontology/\1-{ID}-{DOMÍNIO}-{SUBDOMÍNIO}.md`',
        content
    )
    content = re.sub(
        r'`(N4)-\{ID\}-\{DOMÍNIO\}-\{NOME\}\.md`',
        r'`data/ontology/\1-{ID}-{DOMÍNIO}-{NOME}.md`',
        content
    )
    if content != original:
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[FIX] {os.path.basename(doc_path)}")
    else:
        print(f"[SKIP] {os.path.basename(doc_path)} (no pattern matches)")

print("\n=== All fixes applied ===")
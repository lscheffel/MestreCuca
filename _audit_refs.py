#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit all cross-references after moving N3/N4 to data/ontology/"""
import os, glob, re, sys

sys.stdout.reconfigure(encoding='utf-8')
base = os.getcwd()
dest = os.path.join(base, 'data', 'ontology')

print("=" * 60)
print("AUDIT DE REFERÊNCIAS CRUZADAS")
print("=" * 60)

# 1. N4 -> N3 references
n4_files = sorted(glob.glob(os.path.join(dest, 'N4-*.md')))
print(f"\n--- N4 files referencing N3 (need ../data/ontology/) ---")
n4_needs_fix = 0
for f in n4_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    refs = re.findall(r'\((N3-[^\)]+\.md)\)', content)
    if refs:
        n4_needs_fix += 1
        print(f"  {os.path.basename(f)}: {refs}")
print(f"Total N4 files needing N3 path fix: {n4_needs_fix}/{len(n4_files)}")

# 2. N3 -> ONTOLOGIA_MESTRA references
n3_files = sorted(glob.glob(os.path.join(dest, 'N3-*.md')))
print(f"\n--- N3 files referencing ONTOLOGIA_MESTRA (need ../) ---")
n3_needs_fix = 0
for f in n3_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    refs = re.findall(r'\(([^)]*ONTOLOGIA[^)]*\.md)\)', content)
    if refs:
        n3_needs_fix += 1
        print(f"  {os.path.basename(f)}: {refs}")
print(f"Total N3 files needing ONTOLOGIA path fix: {n3_needs_fix}/{len(n3_files)}")

# 3. Scripts that open/write N3/N4 files
print(f"\n--- Scripts with hardcoded N3/N4 paths ---")
scripts_dir = base
scripts = [f for f in os.listdir(scripts_dir) if f.endswith('.py') and not f.startswith('_')]
for s in sorted(scripts):
    path = os.path.join(scripts_dir, s)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Find lines with open() that reference N3/N4
    lines = content.split('\n')
    relevant_lines = []
    for i, line in enumerate(lines, 1):
        if ('N3-' in line or 'N4-' in line) and 'open(' in line:
            relevant_lines.append((i, line.strip()))
    if relevant_lines:
        print(f"\n  {s}:")
        for ln, line in relevant_lines:
            print(f"    L{ln}: {line[:120]}")

# 4. Check glob patterns in scripts
print(f"\n--- Scripts with glob patterns for N3/N4 ---")
for s in sorted(scripts):
    path = os.path.join(scripts_dir, s)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    lines = content.split('\n')
    relevant_lines = []
    for i, line in enumerate(lines, 1):
        if 'glob' in line and ('N3-' in line or 'N4-' in line):
            relevant_lines.append((i, line.strip()))
    if relevant_lines:
        print(f"\n  {s}:")
        for ln, line in relevant_lines:
            print(f"    L{ln}: {line[:120]}")

# 5. Documentation references
print(f"\n--- Documentation files referencing N3/N4 paths ---")
docs = ['ARQUITETO_PROMPTS_FINAL.md', 'MEMORY.md', 'checklist_recursivo_N3.md',
        'docs/arquitetura_sistema_cognitivo.md', 'SUMARIO_EXECUTIVO_MUDANÇAS.md']
for d in docs:
    path = os.path.join(base, d)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        refs = re.findall(r'\((N[34]-[^)]+\.md)\)', content)
        refs2 = re.findall(r'N3-\{.*?\}', content)
        if refs or refs2:
            print(f"  {d}:")
            if refs:
                for r in refs[:3]:
                    print(f"    direct ref: ({r})")
            if refs2:
                for r in refs2[:3]:
                    print(f"    template ref: {r}")

print("\n" + "=" * 60)
print("AUDIT COMPLETO")
print("=" * 60)
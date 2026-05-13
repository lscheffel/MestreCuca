#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check N3 references to ONTOLOGIA_MESTRA and other cross-refs"""
import os, glob, re

base = os.getcwd()
dest = os.path.join(base, 'data', 'ontology')

n3_files = sorted(glob.glob(os.path.join(dest, 'N3-*.md')))
print(f"Checking {len(n3_files)} N3 files for cross-references...\n")

for f in n3_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Find all parent directory references
    refs = re.findall(r'\(([^)]*\.md)\)', content)
    external_refs = [r for r in refs if not r.startswith('N3-') and not r.startswith('N4-') and not r.startswith('data/')]
    if external_refs:
        print(f"  {os.path.basename(f)}:")
        for r in external_refs:
            print(f"    -> ({r})")

# Also check for any ../ references
print("\n--- Checking for ../ references in N3/N4 files ---")
all_files = sorted(glob.glob(os.path.join(dest, 'N[34]-*.md')))
for f in all_files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if '../' in content:
        print(f"  {os.path.basename(f)} contains '../'")

print("\nDone.")
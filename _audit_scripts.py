#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detailed audit of all Python scripts that reference N3/N4 files"""
import os, re, glob

base = os.getcwd()
dest = os.path.join(base, 'data', 'ontology')

# All Python files in root
scripts = [f for f in os.listdir(base) if f.endswith('.py') and os.path.isfile(os.path.join(base, f))]

for s in sorted(scripts):
    path = os.path.join(base, s)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find all lines referencing N3- or N4- with open/glob/path operations
    lines = content.split('\n')
    relevant = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # Check for various patterns
        if ('N3-' in stripped or 'N4-' in stripped or 
            'data/ontology' in stripped or 
            'glob.glob' in stripped and 'N' in stripped):
            relevant.append((i, stripped))
    
    if relevant:
        print(f"\n{'='*60}")
        print(f"SCRIPT: {s}")
        print(f"{'='*60}")
        for ln, line in relevant:
            print(f"  L{ln:4d}: {line[:150]}")

# Also check for function definitions that build filenames
print(f"\n\n{'='*60}")
print("FUNCTIONS THAT BUILD N3/N4 FILENAMES")
print(f"{'='*60}")
for s in sorted(scripts):
    path = os.path.join(base, s)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Find function defs near N3/N4 references
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def ' in line and i < len(lines)-1:
            # Check next 20 lines for N3/N4 refs
            context = '\n'.join(lines[i:i+20])
            if 'N3-' in context or 'N4-' in context:
                func_match = re.search(r'def\s+(\w+)', line)
                if func_match:
                    fname = func_match.group(1)
                    print(f"\n  {s} -> def {fname}() (around L{i+1})")
                    for j in range(i, min(i+15, len(lines))):
                        if 'N3-' in lines[j] or 'N4-' in lines[j] or 'open(' in lines[j] or 'glob' in lines[j]:
                            print(f"    L{j+1}: {lines[j].strip()[:120]}")

print("\n\nDone.")
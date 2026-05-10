#!/usr/bin/env python3
"""Diagnóstico da estrutura dos JSONs do registry."""
import json, os, sys

d = 'data/json'
files = sorted([f for f in os.listdir(d) if f.endswith('.json') and f != 'ontology_index.json'])
print(f'Total files: {len(files)}')

# Show first 3 files
for fname in files[:3]:
    with open(os.path.join(d, fname), encoding='utf-8') as fp:
        data = json.load(fp)
        print(f'\n=== {fname} ===')
        for k, v in data.items():
            if isinstance(v, (str, int, float, bool, type(None))):
                print(f'  {k}: {repr(v)[:150]}')
            elif isinstance(v, dict):
                print(f'  {k}: {dict(v)}')
            elif isinstance(v, list):
                print(f'  {k}: {v[:3]}')

# Check key names
print('\n=== KEY NAMES ===')
all_keys = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        all_keys.update(data.keys())
print(f'All top-level keys: {sorted(all_keys)}')

# Check dominio values (raw)
print('\n=== RAW DOMINIO VALUES ===')
doms = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        dom = data.get('dominio', '')
        doms.add(repr(dom))
print(f'Unique ({len(doms)}):')
for d in sorted(doms)[:10]:
    print(f'  {d}')

# Check n3_name values (raw)
print('\n=== RAW N3_NAME VALUES ===')
n3s = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        n3 = data.get('n3_name', data.get('subarvore', ''))
        n3s.add(repr(n3))
print(f'Unique ({len(n3s)}):')
for n in sorted(n3s)[:10]:
    print(f'  {n}')

# Check eixo values (raw)
print('\n=== RAW EIXO VALUES ===')
eixos = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        e = data.get('eixo', data.get('axis', ''))
        eixos.add(repr(e))
print(f'Unique ({len(eixos)}):')
for e in sorted(eixos):
    print(f'  {e}')

# Check N4 file for DECOMPOSICAO
print('\n=== DECOMPOSICAO CELL ===')
for f in files:
    if 'DECOMPOSICAO' in f.upper():
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
            break

# Check PROTECAO cell
print('\n=== PROTECAO CELL ===')
for f in files:
    if 'PROTECAO' in f.upper() or 'PROTE' in f.upper():
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
            break

# Check DISSIPACAO cell
print('\n=== DISSIPACAO CELL ===')
for f in files:
    if 'DISSIPACAO' in f.upper() or 'DISSIPA' in f.upper():
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
            break

# Check COMPORTAMENTO cell
print('\n=== COMPORTAMENTO CELL ===')
for f in files:
    if 'COMPORTAMENTO' in f.upper():
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
            break
#!/usr/bin/env python3
"""Diagnostico da estrutura dos JSONs do registry."""
import json, os, sys

d = r'data\json'
files = sorted([f for f in os.listdir(d) if f.endswith('.json') and f != 'ontology_index.json'])
out = []
out.append(f'Total files: {len(files)}')

# Show first file
with open(os.path.join(d, files[0]), encoding='utf-8') as fp:
    data = json.load(fp)
    out.append(f'Sample file: {files[0]}')
    out.append(f'Top-level keys: {sorted(data.keys())}')
    for k, v in data.items():
        if isinstance(v, (str, int, float, bool, type(None))):
            out.append(f'  {k}: {repr(v)[:200]}')
        elif isinstance(v, dict):
            out.append(f'  {k}: {dict(v)}')
        elif isinstance(v, list):
            out.append(f'  {k}: {v[:3]}')

# Check key names
out.append('\n=== KEY NAMES ===')
all_keys = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        all_keys.update(data.keys())
out.append(f'All top-level keys: {sorted(all_keys)}')

# Check dominio values (raw)
out.append('\n=== RAW DOMINIO VALUES ===')
doms = set()
for f in files:
    with open(os.path.join(d, f), encoding='utf-8') as fp:
        data = json.load(fp)
        dom = data.get('dominio', '')
        doms.add(repr(dom))
out.append(f'Unique ({len(doms)}):')
    for d_val in sorted(doms)[:20]:
        out.append(f'  {d_val}')

    # Check n3_name values (raw)
    out.append('\n=== RAW N3_NAME VALUES ===')
    n3s = set()
    for f in files:
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            n3 = data.get('n3_name', data.get('subarvore', ''))
            n3s.add(repr(n3))
    out.append(f'Unique ({len(n3s)}):')
    for n in sorted(n3s)[:20]:
        out.append(f'  {n}')

    # Check eixo values (raw)
    out.append('\n=== RAW EIXO VALUES ===')
    eixos = set()
    for f in files:
        with open(os.path.join(d, f), encoding='utf-8') as fp:
            data = json.load(fp)
            e = data.get('eixo', data.get('axis', ''))
            eixos.add(repr(e))
    out.append(f'Unique ({len(eixos)}):')
    for e in sorted(eixos):
        out.append(f'  {e}')

    # Check DECOMPOSICAO cell
    out.append('\n=== DECOMPOSICAO CELL ===')
    for f in files:
        if 'DECOMPOSICAO' in f.upper():
            with open(os.path.join(d, f), encoding='utf-8') as fp:
                data = json.load(fp)
                out.append(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
                break

    # Check PROTECAO cell
    out.append('\n=== PROTECAO CELL ===')
    for f in files:
        if 'PROTE' in f.upper():
            with open(os.path.join(d, f), encoding='utf-8') as fp:
                data = json.load(fp)
                out.append(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
                break

    # Check DISSIPACAO cell
    out.append('\n=== DISSIPACAO CELL ===')
    for f in files:
        if 'DISSIPA' in f.upper():
            with open(os.path.join(d, f), encoding='utf-8') as fp:
                data = json.load(fp)
                out.append(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
                break

    # Check COMPORTAMENTO cell
    out.append('\n=== COMPORTAMENTO CELL ===')
    for f in files:
        if 'COMPORTAMENTO' in f.upper():
            with open(os.path.join(d, f), encoding='utf-8') as fp:
                data = json.load(fp)
                out.append(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
                break

    # Write output
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'diag_output.txt')
    with open(out_path, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(out))

    print(f'Done. Output written to {out_path}')
    print(f'Lines: {len(out)}')
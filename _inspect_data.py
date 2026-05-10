import json
from pathlib import Path

# Check one sample JSON
d = json.load(open('data/json/N4_ALGORITMIA_1_A.json', encoding='utf-8'))
print('=== N4_ALGORITMIA_1_A ===')
for k,v in d.items():
    print(f'  {k}: {repr(v)[:200]}')
print()

# Check all field names and values
fields = set()
n3_names = set()
axis_vals = set()
pilar_vals = set()
dominio_vals = set()
for f in sorted(Path('data/json').glob('N4_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    fields.update(d.keys())
    n3_names.add(d.get('n3_name', 'MISSING'))
    axis_vals.add(d.get('axis', 'MISSING'))
    pilar_vals.add(d.get('pilar', 'MISSING'))
    dominio_vals.add(d.get('dominio', 'MISSING'))

print(f'Fields: {sorted(fields)}')
print()
print(f'n3_names ({len(n3_names)}):')
for n in sorted(n3_names):
    count = sum(1 for f in Path('data/json').glob('N4_*.json') if json.load(open(f))['n3_name'] == n)
    print(f'  [{n}] -> {count} cells')

print(f'\naxis ({len(axis_vals)}): {sorted(axis_vals)}')
print(f'pilar ({len(pilar_vals)}): {sorted(pilar_vals)}')
print(f'dominio ({len(dominio_vals)}): {sorted(dominio_vals)}')

# Check N4_ALGORITMIA_1_A specifically
print('\n=== Cells in RESOLUCAO ===')
for f in sorted(Path('data/json').glob('N4_ALGORITMIA_1_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    print(f"  {d.get('uid')}: nome={d.get('nome')}, n3_name={d.get('n3_name')}, tags={d.get('tags')}")

# Check DECOMPOSICAO_BINARIA
print('\n=== Looking for DECOMPOSICAO ===')
for f in sorted(Path('data/json').glob('N4_ALGORITMIA_*.json')):
    d = json.load(open(f, encoding='utf-8'))
    nome = d.get('nome', '').upper()
    if 'DECOMP' in nome or 'BINA' in nome:
        print(f"  FOUND: {d.get('uid')}: nome={d.get('nome')}, nome_normalizado={d.get('nome_normalizado')}, tags={d.get('tags')}")
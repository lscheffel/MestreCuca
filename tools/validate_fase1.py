#!/usr/bin/env python3
"""Validação da FASE 1 - Normalização Ontológica"""
import json, os, sys, glob
from collections import Counter

base = os.path.dirname(os.path.abspath(__file__)).replace('tools', 'data/json')
files = sorted(glob.glob(os.path.join(base, 'N4_*.json')))
print(f'[1/6] Total de JSONs N4: {len(files)}')

# UIDs únicos
uids = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        uids.append(json.load(fh)['uid'])
unique = set(uids)
print(f'[2/6] UIDs únicos: {len(unique)} de {len(uids)} | Duplicados: {len(uids) - len(unique)}')

# Naturezas e pilares
naturezas = Counter()
pilares = Counter()
for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
        naturezas[d['natureza']] += 1
        pilares[d['pilar']] += 1

print(f'[3/6] Naturezas: {dict(naturezas.most_common())}')
print(f'[4/6] Pilares: {dict(pilares.most_common())}')

# Schema check
required = ['uid','legacy_id','path','hierarchical_id','nivel','pilar','dominio',
            'n3_ref','n3_name','axis','natureza','subtree_num','cell_num','cell_letter',
            'nome','nome_normalizado','gatilho','acao','restricao','verificacao',
            'assinatura_semantica','exemplos','analogias','tags','relacoes','metadata']
missing = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
    for field in required:
        if field not in d:
            missing.append(f'{os.path.basename(f)}: {field}')

if not missing:
    print(f'[5/6] Todos os {len(required)} campos presentes em todas as 162 células: OK')
else:
    print(f'[5/6] CAMPOS FALTANDO ({len(missing)}): {missing[:20]}')

# Relações
total_rels = sum(len(json.load(open(f, encoding='utf-8'))['relacoes']) for f in files)
print(f'[6/6] Total de relações tipadas: {total_rels}')

# Amostra reversibilidade
print('\n--- AMOSTRA REVERSIBILIDADE ---')
sample = files[0]
with open(sample, encoding='utf-8') as fh:
    d = json.load(fh)
print(f"UID: {d['uid']}")
print(f"Legacy: {d['legacy_id']}")
print(f"Path: {d['path']}")
print(f"HierID: {d['hierarchical_id']}")
print(f"Pilar: {d['pilar']} | Domínio: {d['dominio']} | N3: {d['n3_name']}")
print(f"Natureza: {d['natureza']} | Nome: {d['nome']}")
print(f"Relações: {len(d['relacoes'])}")
print(f"Tags: {d['tags']}")

print('\n=== VALIDAÇÃO CONCLUÍDA ===')
if len(files) == 162 and len(unique) == 162 and not missing:
    print('✅ TODOS OS CRITÉRIOS ATENDIDOS')
else:
    print('⚠️ PROBLEMAS DETECTADOS')
    if len(files) != 162: print(f'  - Esperados 162, encontrados {len(files)}')
    if len(unique) != 162: print(f'  - UIDs duplicados: {len(uids) - len(unique)}')
    if missing: print(f'  - Campos faltando: {len(missing)}')
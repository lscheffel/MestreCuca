#!/usr/bin/env python3
"""Validação profunda da FASE 1"""
import json, os, glob, sys
from collections import Counter

base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'json')
files = sorted(glob.glob(os.path.join(base, 'N4_*.json')))

print(f'[1/8] Total de JSONs N4: {len(files)}')

# Carregar todos
all_data = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        all_data.append(json.load(fh))

# UIDs únicos
uids = [d['uid'] for d in all_data]
unique = set(uids)
print(f'[2/8] UIDs únicos: {len(unique)}/{len(uids)} | Duplicados: {len(uids) - len(unique)}')

# Naturezas
naturezas = Counter(d['natureza'] for d in all_data)
print(f'[3/8] Naturezas ({len(naturezas)}): {dict(naturezas.most_common())}')

# Pilares
pilares = Counter(d['pilar'] for d in all_data)
print(f'[4/8] Pilares ({len(pilares)}): {dict(pilares.most_common())}')

# Domínios
dominios = Counter(d['dominio'] for d in all_data)
print(f'[5/8] Domínios ({len(dominios)}): {dict(dominios.most_common())}')

# Schema check
required = ['uid','legacy_id','path','hierarchical_id','nivel','pilar','dominio',
            'n3_ref','n3_name','axis','natureza','subtree_num','cell_num','cell_letter',
            'nome','nome_normalizado','gatilho','acao','restricao','verificacao',
            'assinatura_semantica','exemplos','analogias','tags','relacoes','metadata']
missing = []
for d in all_data:
    for field in required:
        if field not in d:
            missing.append(f'{d.get("uid","?")}: {field}')
print(f'[6/8] Campos obrigatórios ({len(required)}): {"OK - todos presentes" if not missing else f"FALTANDO: {len(missing)}"}')

# Relações
total_rels = sum(len(d['relacoes']) for d in all_data)
print(f'[7/8] Total de relações tipadas: {total_rels}')

# Amostras de diferentes pilares
print(f'\n[8/8] Amostras por pilar:')
for pilar in ['LOGOS', 'BIOS', 'PATHOS', 'KHAOS', 'APEIRON', 'MYTHOS']:
    samples = [d for d in all_data if d['pilar'] == pilar][:1]
    if samples:
        s = samples[0]
        print(f'  {pilar}: {s["uid"]} | {s["nome"]} | natureza={s["natureza"]} | relacoes={len(s["relacoes"])}')

# Verificar mapeamento reverso
print(f'\n--- VERIFICAÇÃO DE MAPPING ---')
uid_to_path = {}
for d in all_data:
    uid_to_path[d['uid']] = d['path']
print(f'UIDs com path: {len(uid_to_path)}')

# Verificar consistência dos IDs
errors = []
for d in all_data:
    uid = d['uid']
    # Verificar se legacy_id corresponde
    if not d.get('legacy_id'):
        errors.append(f'{uid}: sem legacy_id')
    if not d.get('path'):
        errors.append(f'{uid}: sem path')
    if not d.get('hierarchical_id'):
        errors.append(f'{uid}: sem hierarchical_id')

if errors:
    print(f'ERROS DE MAPPING: {len(errors)}')
    for e in errors[:5]:
        print(f'  {e}')
else:
    print('Consistência de IDs: OK')

print(f'\n{"="*50}')
if len(files) == 162 and len(unique) == 162 and not missing and not errors:
    print('✅ TODOS OS CRITÉRIOS ATENDIDOS - FASE 1 COMPLETA')
else:
    print('⚠️ PROBLEMAS DETECTADOS')
    if len(files) != 162: print(f'  - JSONs: {len(files)}/162')
    if len(unique) != 162: print(f'  - UIDs duplicados: {len(uids)-len(unique)}')
    if missing: print(f'  - Campos faltando: {len(missing)}')
    if errors: print(f'  - Erros de mapping: {len(errors)}')
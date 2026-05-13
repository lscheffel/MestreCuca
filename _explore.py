#!/usr/bin/env python
"""Exploracao do ambiente - FASE 4"""
import os, sys, glob, json

os.chdir(r'e:\Arquivos\Área de Trabalho\MestreCuca')

print('=== PYTHON VERSION ===')
print(sys.version)

print('\n=== PACKAGES ===')
for pkg in ['numpy', 'sentence_transformers', 'sklearn', 'yaml', 'networkx', 'torch']:
    try:
        m = __import__(pkg)
        print(f'  {pkg}: {getattr(m, "__version__", "ok")}')
    except ImportError as e:
        print(f'  {pkg}: MISSING')

print('\n=== STRUCTURE ===')
for d in ['data/json', 'data/embeddings', 'tools', 'runtime', 'config', 'core', 'ontology']:
    p = os.path.join('.', d)
    if os.path.isdir(p):
        items = os.listdir(p)
        files = [i for i in items if os.path.isfile(os.path.join(p,i))]
        print(f'  {d}/: {len(files)} files')
        for f in sorted(files)[:6]:
            sz = os.path.getsize(os.path.join(p,f))
            print(f'    {f} ({sz}B)')
    else:
        print(f'  {d}/: NOT FOUND')

print('\n=== N4 MARKDOWN COUNT ===')
n4_md = glob.glob(os.path.join('data', 'ontology', 'N4-*.md'))
print(f'  Total N4 .md: {len(n4_md)}')

print('\n=== N4 JSON COUNT ===')
n4_json = glob.glob('data/json/*.json')
if n4_json:
    print(f'  Total N4 .json: {len(n4_json)}')
    with open(n4_json[0]) as fp:
        d = json.load(fp)
        print(f'  Keys: {list(d.keys())}')
        for k,v in d.items():
            if isinstance(v, (list, dict)):
                print(f'    {k}: {type(v).__name__} len={len(v)}')
            else:
                print(f'    {k}: {repr(v)[:80]}')
else:
    print('  No JSONs in data/json/')
    all_json = glob.glob('**/*.json', recursive=True)
    print(f'  All JSONs: {len(all_json)}')
    for j in all_json[:5]:
        print(f'    {j}')

print('\n=== NPY COUNT ===')
npy = glob.glob('data/embeddings/*.npy')
print(f'  Total .npy: {len(npy)}')
if npy:
    import numpy as np
    for f in npy[:3]:
        arr = np.load(f)
        print(f'    {os.path.basename(f)}: {arr.shape}')
    ji = os.path.join('data/embeddings', 'embeddings_index.json')
    if os.path.exists(ji):
        with open(ji) as fp:
            idx = json.load(fp)
        print(f'  Index keys: {list(idx.keys())}')
        if 'embeddings' in idx:
            print(f'  Embeddings in index: {len(idx["embeddings"])}')
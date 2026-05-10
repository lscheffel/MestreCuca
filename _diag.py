#!/usr/bin/env python3
import sys, numpy as np
sys.path.insert(0, 'tools')
sys.path.insert(0, 'core')
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path
import json

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
emb_dir = Path('data/embeddings')
embeddings = {}
for f in sorted(emb_dir.glob('N4_*.npy')):
    uid = f.stem
    emb = np.load(f).astype(np.float32)
    norm = np.linalg.norm(emb)
    if norm > 1e-8:
        emb = emb / norm
    embeddings[uid] = emb

all_embs = np.stack(list(embeddings.values()))
all_uids = list(embeddings.keys())

queries = [
    'decomposicao problemas complexos',
    'validacao sistemas',
    'metabolismo ciclos',
    'reconhecimento padroes',
    'homeostase equilibrio',
    'transformacao ruptura',
]

for q in queries:
    q_emb = model.encode(q, normalize_embeddings=True, convert_to_numpy=True).astype(np.float32)
    sims = cosine_similarity(q_emb.reshape(1, -1), all_embs)[0]
    top_idx = np.argsort(sims)[::-1][:5]
    print('Query: %s' % q)
    print('  Max sim: %.4f' % sims[top_idx[0]])
    for idx in top_idx:
        print('    %s: %.4f' % (all_uids[idx], sims[idx]))
    print()
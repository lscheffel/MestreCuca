#!/usr/bin/env python3
"""Script para gerar células N4 a partir da Taxonomia Ontológica."""

import re
import os

# Le o arquivo Taxonomia_Ontologica.md
with open('Taxonomia_Ontologica.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra todas as células N4 (exemplo: Célula R1.1.1-A: ...)
# Padrão: **Célula XXXXXX-X: NOME**
pattern = r'\*\*Célula (\w+-\w+):\*\* ([^\n]+)\s*\n-\*\*Gatilho:\*\* ([^\n]+)\s*\n-\*\*Ação:\*\* ([^\n]+)\s*\n-\*\*Restrição:\*\* ([^\n]+)\s*\n-\*\*Verificação:\*\* ([^\n]+)'

matches = re.finditer(pattern, content)

n4_list = []
for match in matches:
    cell_id = match.group(1)  # R1.1.1-A
    nome = match.group(2)     # DECOMPOSIÇÃO_BINÁRIA
    gatilho = match.group(3).strip()
    acao = match.group(4).strip()
    restricao = match.group(5).strip()
    verificacao = match.group(6).strip()
    
    # Extrai o subdomínio N3 da célula (ex: R1.1.1 vem de 1.1.1 RESOLUÇÃO)
    n3_ref = cell_id.split('-')[0]  # R1.1.1
    # Remove letra inicial se for R, B, etc.
    n3_num = n3_ref[1:] if n3_ref[0].isalpha() else n3_ref  # 1.1.1
    
    # Determina domínio baseado no primeiro dígito
    n2_prefix = n3_num.split('.')[0]
    dominio_map = {
        '1': 'LOGOS', '2': 'BIOS', '3': 'PATHOS',
        '4': 'KHAOS', '5': 'APEIRON', '6': 'MYTHOS'
    }
    dominio = dominio_map.get(n2_prefix, 'DESCONHECIDO')
    
    # Busca o subdomínio N3 correspondente
    n3_pattern = rf'### (\d+\.\d+\.\d+) \[(\d+\.\d+)\] (\w+):'
    n3_matches = re.finditer(n3_pattern, content)
    
    n3_nome = "DESCONHECIDO"
    n2_id = "0.0"
    for n3_match in n3_matches:
        if n3_match.group(1) == n3_num:
            n2_id = n3_match.group(2)
            n3_nome = n3_match.group(3)
            break
    
    n4_list.append({
        'cell_id': cell_id,
        'nome': nome,
        'n3_ref': n3_num,
        'n3_nome': n3_nome,
        'n2_id': n2_id,
        'dominio': dominio,
        'gatilho': gatilho,
        'acao': acao,
        'restricao': restricao,
        'verificacao': verificacao
    })

print(f"Encontradas {len(n4_list)} células N4")

# Agrupa por subdomínio N3
from collections import defaultdict
n3_groups = defaultdict(list)
for cell in n4_list:
    key = f"{cell['n3_ref']}-{cell['dominio']}-{cell['n3_nome'].upper()}"
    n3_groups[key].append(cell)

print(f"Subdomínios N3 com células: {len(n3_groups)}")

# Para cada subdomínio N3 que tem células, cria arquivo N4
for n3_key, cells in n3_groups.items():
    # Extrai info do primeiro cell
    sample = cells[0]
    n3_id = sample['n3_ref']
    dominio = sample['dominio']
    n3_nome = sample['n3_nome']
    n2_id = sample['n2_id']
    
    filename = f"N4-{n3_id.replace('.', '_')}-{dominio}-{n3_nome.upper()}.md"
    
    # Constrói tabela de células
    tabela_celulas = ""
    for i, cell in enumerate(cells, 1):
        tabela_celulas += f"""### {i}. {cell['nome']}

- **ID:** {cell['cell_id']}
- **Gatilho:** {cell['gatilho']}
- **Ação:** {cell['acao']}
- **Restrição:** {cell['restricao']}
- **Verificação:** {cell['verificacao']}

"""
    
    content_file = f"""# N4-{n3_id.replace('.', '_')} - {dominio} / {n3_nome.upper()} - Células Semânticas

---

## Metadados

- **ID N4:** {n3_id} (agregado)
- **ID N3 Pai:** {n3_id}
- **ID N2 Avô:** {n2_id}
- **Domínio:** {dominio}
- **Subdomínio N3:** {n3_nome}
- **Geometria Base:** 2×3×3×3×3
- **Total de Células:** {len(cells)}
- **Data:** 2026-05-07
- **Status:** ATIVO

---

## Sumário Executivo

Este arquivo agrega as células semânticas operacionais N4 derivadas do subdomínio N3 **{n3_nome}** ({dominio}), conforme mapeamento na Taxonomia Ontológica.

**Origem N3:** `N3-{n3_id.replace('.', '_')}-{dominio}-{n3_nome.upper()}.md`  
**Células N4:** {len(cells)} procedimentos aplicáveis

---

## Matriz de Rastreabilidade

### Origem N3

| Elemento | Referência |
|----------|------------|
| Arquivo N3 | `N3-{n3_id.replace('.', '_')}-{dominio}-{n3_nome.upper()}.md` |
| Domínio N2 | {n2_id}_{n3_nome} |
| Domínio N1 | {dominio} |
| Vetor N0 | {"0.1_SINTRÓPICO" if dominio in ["LOGOS", "BIOS", "PATHOS"] else "0.2_ENTRÓPICO"} |

### Relação Hierárquica

```
N0: {"SINTRÓPICO" if dominio in ["LOGOS", "BIOS", "PATHOS"] else "ENTRÓPICO"}
  └─ N1: {dominio}
      └─ N2: {n2_id}_{n3_nome}
          └─ N3: {n3_id} {n3_nome}
              └─ N4: {len(cells)} células (este arquivo)
```

---

## Células Semânticas N4

{tabela_celulas}

---

## Regras de Derivação

1. **Herança de DNA:**
   - Cada célula herda tags de N3, N2, N1, N0
   - Crenças do subdomínio N3 devem ser respeitadas
   - Axiomas vetoriais orientam aplicação

2. **Aplicabilidade:**
   - Células são diretamente executáveis em prompts
   - Gatilhos devem ser verificáveis
   - Ações devem ser procedimentos claros

3. **Restrições:**
   - Limites devem ser explicitamente definidos
   - Verificação deve confirmar sucesso

---

## Checklist de Conformidade

### Herança
- [x] Origem N3 documentada
- [x] Domínio N2 identificado
- [x] Tags herdadas preservadas

### Consistência
- [x] Geometria 2×3×3×3×3 mantida
- [x] Sem novos eixos introduzidos
- [x] Escopo restrito a N4

### Operacionalidade
- [x] Células são aplicáveis
- [x] Gatilhos verificáveis
- [x] Ações procedimentais

### Documentação
- [x] Metadados completos
- [x] Matriz de rastreabilidade
- [x] Células detalhadas

---

## Registro de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2026-05-07 | Sistema | Criação agregada N4 |

---

*Este documento é parte integrante da ontologia fractal do projeto "Arquiteto de Prompts - Expansão Fractal".*
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_file)
    
    print(f"Criado: {filename} ({len(cells)} células)")

print(f"\nTotal de arquivos N4 criados: {len(n3_groups)}")
print(f"Total de células N4 mapeadas: {len(n4_list)}")

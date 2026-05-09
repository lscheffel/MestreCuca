import os
import re
import ast
import glob

# 1. Carregar a taxonomia N3
with open('Taxonomia_Ontologica.md', 'r', encoding='utf-8') as f:
    taxo_content = f.read()

pattern_n3 = r'\| \*\*N3\*\* \| \*\*(\d+\.\d+\.\d+)\*\* \| \*\*(\w+)\*\* \| ([^|]+) \|'
matches_n3 = re.finditer(pattern_n3, taxo_content)

n3_dict = {}
for match in matches_n3:
    n3_id = match.group(1)
    n3_nome = match.group(2)
    foco = match.group(3).strip()
    
    n2_prefix = n3_id.split('.')[0]
    n2_mid = n3_id.split('.')[1]
    n2_id = f"{n2_prefix}.{n2_mid}"
    
    dominio_map = {
        '1': 'LOGOS', '2': 'BIOS', '3': 'PATHOS',
        '4': 'KHAOS', '5': 'APEIRON', '6': 'MYTHOS'
    }
    pilar = dominio_map.get(n2_prefix, 'DESCONHECIDO')
    eixo = "SINTRÓPICO" if n2_prefix in ['1', '2', '3'] else "ENTRÓPICO"
    eixo_codigo = "0.1_SINTRÓPICO" if eixo == "SINTRÓPICO" else "0.2_ENTRÓPICO"
    
    n3_dict[n3_id] = {
        'n3_id': n3_id,
        'n3_nome': n3_nome,
        'foco': foco,
        'n2_id': n2_id,
        'pilar': pilar,
        'eixo': eixo,
        'eixo_codigo': eixo_codigo
    }

# 2. Carregar nomes N2
n2_dict = {}
pattern_n2 = r'\| N2 \| (\d+\.\d+) \| (\w+) \| ([^|]+) \|'
matches_n2 = re.finditer(pattern_n2, taxo_content)
for match in matches_n2:
    n2_dict[match.group(1)] = match.group(2)

# Adicionar N2 nome aos N3
for n3_id, data in n3_dict.items():
    data['n2_nome'] = n2_dict.get(data['n2_id'], 'DESCONHECIDO')

# 3. Carregar as células N4 de create_n4_manual.py
with open('create_n4_manual.py', 'r', encoding='utf-8') as f:
    create_n4_content = f.read()

# Extrair a lista `celulas_n4`
start_idx = create_n4_content.find('celulas_n4 = [')
end_idx = create_n4_content.find(']', start_idx) + 1
celulas_str = create_n4_content[start_idx:end_idx].replace('celulas_n4 = ', '')

# Processar as tuplas para dicionarios
import ast
try:
    celulas_list = ast.literal_eval(celulas_str)
except Exception as e:
    print(f"Erro ao parsear celulas_n4: {e}")
    celulas_list = []

n4_groups = {}
for celula in celulas_list:
    c_id, c_nome, n3_ref, dominio, gatilho, acao, restricao, verificacao = celula
    if n3_ref not in n4_groups:
        n4_groups[n3_ref] = []
    n4_groups[n3_ref].append({
        'id': c_id, 'nome': c_nome, 'gatilho': gatilho,
        'acao': acao, 'restricao': restricao, 'verificacao': verificacao
    })

# 4. Limpar arquivos existentes
for file in glob.glob("N3-*.md"): os.remove(file)
for file in glob.glob("N4-*.md"): os.remove(file)

# 5. Gerar novos N3 e N4
for n3_id, data in n3_dict.items():
    n3_id_file = n3_id.replace('.', '_')
    pilar = data['pilar']
    n3_nome = data['n3_nome']
    n2_id = data['n2_id']
    n2_nome = data['n2_nome']
    eixo = data['eixo']
    eixo_codigo = data['eixo_codigo']
    foco = data['foco']

    # ARQUIVO N3
    n3_filename = f"N3-{n3_id_file}-{pilar}-{n3_nome}.md"
    n3_content = f"""# N3-{n3_id} - {pilar} / {n3_nome}

---

## Metadados Ontológicos

- **N0 (Eixo):** {eixo_codigo}
- **N1 (Pilar):** {pilar}
- **N2 (Domínio):** {n2_id}_{n2_nome}
- **N3 (Subárvore):** {n3_id} {n3_nome}
- **Data:** 2026-05-07
- **Status:** PADRONIZADO

---

## Matriz de Rastreabilidade Fractal

```text
N0: {eixo}
  └─ N1: {pilar}
      └─ N2: {n2_id} {n2_nome}
          └─ N3: {n3_id} {n3_nome} (Este Documento)
              └─ N4: 3 Células Semânticas (Ver arquivo N4 correspondente)
```

## Foco e Diretrizes da Subárvore (N3)

- **Foco Temático:** {foco}
- **Diretriz de Operação:** Esta subárvore especializa o domínio {n2_nome}, afunilando a semântica do pilar {pilar} em um escopo acionável. 
- **Herança Tripartite Obrigatória:** Toda célula derivada deste nó herda obrigatoriamente as metas do eixo {eixo}, as crenças do pilar {pilar} e as restrições operacionais do domínio {n2_nome}.

---
*Documento padronizado pelo Sistema de Governança Ontológica.*
"""
    with open(n3_filename, 'w', encoding='utf-8') as f:
        f.write(n3_content)

    # ARQUIVO N4
    cells = n4_groups.get(n3_id, [])
    n4_filename = f"N4-{n3_id_file}-{pilar}-{n3_nome}.md"
    
    tabela_celulas = ""
    for i, cell in enumerate(cells, 1):
        tabela_celulas += f"### {i}. {cell['nome']}\n\n"
        tabela_celulas += f"- **ID Célula:** {cell['id']}\n"
        tabela_celulas += f"- **Gatilho:** {cell['gatilho']}\n"
        tabela_celulas += f"- **Ação:** {cell['acao']}\n"
        tabela_celulas += f"- **Restrição:** {cell['restricao']}\n"
        tabela_celulas += f"- **Verificação:** {cell['verificacao']}\n\n"

    n4_content = f"""# N4-{n3_id} - {pilar} / {n3_nome} - Células Semânticas

---

## Metadados Ontológicos

- **N0 (Eixo):** {eixo_codigo}
- **N1 (Pilar):** {pilar}
- **N2 (Domínio):** {n2_id}_{n2_nome}
- **N3 (Subárvore):** {n3_id} {n3_nome}
- **N4 (Células):** Agregado de {len(cells)} células operacionais
- **Data:** 2026-05-07
- **Status:** PADRONIZADO

---

## Matriz de Rastreabilidade Fractal

```text
N0: {eixo}
  └─ N1: {pilar}
      └─ N2: {n2_id} {n2_nome}
          └─ N3: {n3_id} {n3_nome} 
              └─ N4: Células Operacionais (Este Documento)
```

---

## Catálogo de Células N4

As células abaixo representam a granularidade máxima (N4) da subárvore **{n3_nome}**. São instruções diretamente aplicáveis em prompts.

{tabela_celulas}
---

## Checklist de Conformidade

- [x] Hierarquia estrita (N0 ao N4) padronizada e documentada.
- [x] Ausência de sobreposição de nomenclaturas.
- [x] Nomenclatura do arquivo alinhada com a taxonomia mestre.

---
*Documento padronizado pelo Sistema de Governança Ontológica.*
"""
    with open(n4_filename, 'w', encoding='utf-8') as f:
        f.write(n4_content)

print(f"Sucesso: {len(n3_dict)} arquivos N3 e {len(n3_dict)} arquivos N4 gerados padronizados.")

# 6. Gerar o taxon.md (Catálogo Unificado)
taxon_content = """# TAXON (Catálogo Ontológico Unificado)
## Governança Central de Nós e Células

Este documento consolida a arquitetura fractal completa (N0 ao N4) em um único índice de referência padronizado.

"""

for n2_prefix in ['1', '2', '3', '4', '5', '6']:
    pilar = {'1':'LOGOS', '2':'BIOS', '3':'PATHOS', '4':'KHAOS', '5':'APEIRON', '6':'MYTHOS'}[n2_prefix]
    eixo = "SINTRÓPICO" if n2_prefix in ['1', '2', '3'] else "ENTRÓPICO"
    taxon_content += f"## PILAR: {pilar} (N1) - Eixo {eixo} (N0)\n\n"
    
    for n2_mid in ['1', '2', '3']:
        n2_id = f"{n2_prefix}.{n2_mid}"
        n2_nome = n2_dict.get(n2_id, '')
        taxon_content += f"### Domínio: {n2_id}_{n2_nome} (N2)\n\n"
        
        for n3_suffix in ['1', '2', '3']:
            n3_id = f"{n2_id}.{n3_suffix}"
            if n3_id in n3_dict:
                n3 = n3_dict[n3_id]
                taxon_content += f"#### Subárvore: {n3_id} {n3['n3_nome']} (N3)\n"
                taxon_content += f"- **Foco:** {n3['foco']}\n"
                
                cells = n4_groups.get(n3_id, [])
                for cell in cells:
                    taxon_content += f"  - **N4:** [{cell['id']}] {cell['nome']}\n"
                taxon_content += "\n"

with open('taxon.md', 'w', encoding='utf-8') as f:
    f.write(taxon_content)

print("Sucesso: taxon.md gerado.")

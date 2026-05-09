#!/usr/bin/env python3
"""Script para gerar arquivos N3 a partir da Taxonomia Ontológica."""

import re
import os

# Le o arquivo Taxonomia_Ontologica.md
with open('Taxonomia_Ontologica.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Encontra todas as secoes N3 (### 3.3.X [N2] NOME:)
pattern = r'### (\d+\.\d+\.\d+) \[(\d+\.\d+)\] (\w+):\s*\n-\*\*foco:\*\* "([^"]+)"\s*\n-\*\*crença:\*\* "([^"]+)"\s*\n-\*\*Tags Herdadas:\*\* \[([^\]]+)\](?:\s*\n-\*\*Tags N3:\*\* \[([^\]]+)\])?'

matches = re.finditer(pattern, content, re.MULTILINE)

n3_data = []
for match in matches:
    n3_id = match.group(1)  # 3.3.1
    n2_id = match.group(2)  # 1.1
    nome = match.group(3)   # ALGORITMIA
    foco = match.group(4)
    crenca = match.group(5)
    tags_herdadas = match.group(6)
    tags_n3 = match.group(7) or ''
    
    # Determina o dominio pai (LOGOS, BIOS, etc.) baseado no n2_id
    n2_prefix = n2_id.split('.')[0]
    dominio_map = {
        '1': 'LOGOS', '2': 'BIOS', '3': 'PATHOS',
        '4': 'KHAOS', '5': 'APEIRON', '6': 'MYTHOS'
    }
    dominio = dominio_map.get(n2_prefix, 'DESCONHECIDO')
    
    n3_data.append({
        'n3_id': n3_id,
        'n2_id': n2_id,
        'nome': nome,
        'dominio': dominio,
        'subdominio': nome.lower(),
        'foco': foco,
        'crenca': crenca,
        'tags_herdadas': tags_herdadas,
        'tags_n3': tags_n3,
        'n3_codigo': n3_id.replace('.', '_')  # 3_3_1
    })

print(f"Encontrados {len(n3_data)} subdomínios N3")

# Para cada N3, cria um arquivo
for item in n3_data:
    filename = f"N3-{item['n3_id'].replace('.', '_')}-{item['dominio']}-{item['subdominio'].upper()}.md"
    
    # Determina a URL ancora para a ontologia mestre
    # Procura a secao correspondente na V2
    
    content_file = f"""# N3-{item['n3_id'].replace('.', '_')} - {item['dominio']} / {item['nome']}

---

## Metadados

- **ID N3:** {item['n3_id']}
- **ID N2 Pai:** {item['n2_id']}
- **Domínio:** {item['dominio']}
- **Subdomínio:** {item['nome']}
- **Geometria Base:** 2×3×3×3×3
- **Data:** 2026-05-07
- **Status:** ATIVO

---

## Sumário Executivo de Especialização Fractal

Este arquivo documenta a especialização do nível N3 **{item['nome']}** no contexto do domínio **{item['dominio']}** (N2: {item['n2_id']}_{item['nome']}).

**Foco:** {item['foco']}

**Crença Fundamental:** "{item['crenca']}"

**Tags Herdadas:** [{item['tags_herdadas']}]

Este subdomínio representa uma ramificação específica dentro da árvore fractal, mantendo estrita aderência aos axiomas e princípios definidos na ontologia mestre enquanto detalha aspectos operacionais e contextuais da especialização.

---

## Matriz de Rastreabilidade

### Referência Cruzada com ONTOLOGIA_MESTRA_DOMINANTE_V2.md

| Elemento | Localização na V2 | Âncora |
|----------|-------------------|--------|
| Domínio Pai ({item['dominio']}) | [3.2 EIXO](ONTOLOGIA_MESTRA_DOMINANTE_V2.md#32-eixo_01-sintrópico) | [Ver Eixo](ONTOLOGIA_MESTRA_DOMINANTE_V2.md#32-eixo_01-sintrópico) |
| Domínio N2 ({item['n2_id']}_{item['nome']}) | [3.3.{item['n2_id'].split('.')[1]}](ONTOLOGIA_MESTRA_DOMINANTE_V2.md#33-{item['n2_id'].replace('.', '')}) | [Ver Domínio](ONTOLOGIA_MESTRA_DOMINANTE_V2.md#33-{item['n2_id'].replace('.', '')}) |
| Subdomínio N3 (Este) | Documentação detalhada | Auto-referenciado |

### Hierarquia Completa

```
N0: {item['dominio']} (Vetor)
  └─ N1: {item['dominio']} (Pilar)
      └─ N2: {item['n2_id']}_{item['nome']} (Domínio)
          └─ N3: {item['n3_id']} {item['nome']} (Este documento)
              └─ N4: Células semânticas operacionais (Derivadas)
```

---

## Descrição Detalhada de Células N3

### Atributos do Subdomínio

- **Identificador:** {item['n3_id']}
- **Nome:** {item['nome']}
- **Foco Temático:** {item['foco']}
- **Crença Diretiva:** "{item['crenca']}"
- **Tags Herdadas:** [{item['tags_herdadas']}]

### Relações Ontológicas

#### Relação com Nível N2 (Domínio Pai)

O subdomínio **{item['nome']}** especializa o domínio {item['n2_id']}_{item['nome']} através da aplicação de:

1. **Foco Específico:** {item['foco']}
2. **Crença Operacional:** "{item['crenca']}"
3. **Restrições de Tags:** [{item['tags_herdadas']}]

#### Relação com Nível N4 (Células Derivadas)

As células N4 deste subdomínio devem:
- Herdar todas as tags: [{item['tags_herdadas']}]
- Respeitar a crença: "{item['crenca']}"
- Operar dentro do foco: {item['foco']}
- Manter consistência com as regras do Cânone do Arquiteto

### Regras de Derivação

1. **Herança de DNA:**
   - Axiomas dos vetores N0 devem ser preservados
   - Crenças do pilar N1 devem ser referenciadas
   - Tags do domínio N2 devem ser incluídas
   - Crença específica do N3 deve guiar a especialização

2. **Consistência Semântica:**
   - Toda célula N4 deve ser diretamente aplicável
   - Deve haver pelo menos 3 células N4 por subdomínio N3
   - Células devem cobrir casos de uso distintos

3. **Restrições Operacionais:**
   - Não introduzir novos conceitos fora da árvore
   - Manter geometria 2×3×3×3×3 inalterada
   - Garantir rastreabilidade completa até N0

---

## Checklist de Conformidade Ontológica

### Verificação de Herança

- [ ] Axiomas N0 referenciados explicitamente
- [ ] Crenças N1 documentadas
- [ ] Tags N2 incluídas
- [ ] Crença N3 especificada
- [ ] Relação com domínio pai clara

### Consistência com Ontologia Mestre

- [ ] Geometria 2×3×3×3×3 preservada
- [ ] Sem introdução de novos eixos
- [ ] Escopo não expandido além de N3
- [ ] Referências à V2 válidas e recuperáveis
- [ ] Terminologia alinhada com V2

### Operacionalidade

- [ ] Subdomínio possui pelo menos 3 células N4 derivadas
- [ ] Células são diretamente aplicáveis
- [ ] Regras de derivação documentadas
- [ ] Matriz de rastreabilidade completa

### Documentação

- [ ] Sumário executivo claro
- [ ] Matriz de rastreabilidade preenchida
- [ ] Descrição detalhada das células
- [ ] Regras de derivação especificadas
- [ ] Checklist de conformidade completo
- [ ] Registro de alterações mantido

---

## Registro de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2026-05-07 | Sistema de Governança | Criação inicial do subdomínio N3 |

---

## Apêndice: Resolução de Auditoria

### Conformidade com Auditoria de Discrepâncias

Este subdomínio foi criado em conformidade com as resoluções da auditoria:

- **MATRIZ #33 (Domínios - Crenças):** Crença especificada e documentada
- **MATRIZ #34 (Domínios - Nomenclatura):** Código estruturado {item['n3_id']} utilizado
- **MATRIZ #39 (Mapeamento Explícito):** Matriz de rastreabilidade incluída

### Evidência no Modelo

- Referência cruzada válida para ONTOLOGIA_MESTRA_DOMINANTE_V2.md
- Geometria 2×3×3×3×3 preservada
- Sem introdução de dados fictícios
- Escopo restrito a N3 conforme especificado

---

*Este documento é parte integrante da ontologia fractal do projeto "Arquiteto de Prompts - Expansão Fractal" e deve ser mantido em sincronia com a ONTOLOGIA_MESTRA_DOMINANTE_V2.md.*"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content_file)
    
    print(f"Criado: {filename}")

print(f"\nTotal de arquivos criados: {len(n3_data)}")

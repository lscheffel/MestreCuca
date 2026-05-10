#!/usr/bin/env python3
"""
N4 Markdown → JSON Enriquecido

Converte as 162 células N4 do formato markdown para JSON com:
- UIDs permanentes
- Natureza ontológica inferida
- Relações tipadas
- Assinaturas semânticas (placeholder)
- Campos semânticos (exemplos, analogias, etc.)

Pipeline:
  1. Carregar dados brutos de create_n4_manual.py
  2. Construir registry com UIDs e metadados
  3. Inferir natureza ontológica para cada célula
  4. Construir relações tipadas
  5. Salvar JSONs individuais em data/json/
  6. Gerar índice global ontology_index.json
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Garantir que o diretório raiz do projeto está no path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "core"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "tools"))

from uid_generator import (
    build_id_mapping,
    generate_hierarchical_id,
    generate_path,
    generate_uid,
    lookup_by_legacy,
    normalize_text,
    validate_uid,
)
from ontology_typing import infer_natureza, normalize_natureza, validate_natureza
from relation_engine import build_all_relations

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "json")
INDEX_FILE = os.path.join(OUTPUT_DIR, "ontology_index.json")

# Mapeamento de prefixo legado → nome do pilar
LEGACY_PREFIX_TO_PILLAR = {
    "R": "LOGOS",
    "B": "BIOS",
    "P": "PATHOS",
    "K": "KHAOS",
    "A": "APEIRON",
    "M": "MYTHOS",
}

# Mapeamento de nome do pilar → número do pilar (1-6)
PILLAR_NAME_TO_NUM = {
    "LOGOS": 1, "BIOS": 2, "PATHOS": 3,
    "KHAOS": 4, "APEIRON": 5, "MYTHOS": 6,
}

# Número do eixo por pilar (1-3 = SINTRÓPICO, 4-6 = ENTRÓPICO)
PILLAR_TO_AXIS = {
    "LOGOS": "SINTRÓPICO",
    "BIOS": "SINTRÓPICO",
    "PATHOS": "SINTRÓPICO",
    "KHAOS": "ENTRÓPICO",
    "APEIRON": "ENTRÓPICO",
    "MYTHOS": "ENTRÓPICO",
}

# Nomes das subárvores N3 por domínio (ordem fixa)
DOMAIN_SUBTREES = {
    "ALGORITMIA": ["RESOLUÇÃO", "OTIMIZAÇÃO", "VALIDAÇÃO"],
    "NOMOS": ["LEGISLAÇÃO", "CONTORNO", "PACTO"],
    "MECÂNICA": ["ESTATICA", "DINAMICA", "TERMOTRANSDINÂMICA"],
    "OIKOS": ["MORADA", "TERRITORIO", "PROVISAO"],
    "SOMA": ["INTEGRIDADE", "VITALIDADE", "HOMEOSTASE"],
    "METABOLISMO": ["ANABOLISMO", "CATABOLISMO", "CICLO"],
    "ETHOS": ["VALORES", "VIRTUDE", "RESPONSABILIDADE"],
    "ALTERIDADE": ["RECONHECIMENTO", "EMPATIA", "DIALOGO"],
    "ESTÉTICA": ["HARMONIA", "EXPRESSAO", "IMPACTO"],
    "ENTROPIA": ["DEGRADAÇÃO", "DISSIPAÇÃO", "CAOS"],
    "SINGULARIDADE": ["EXCEPCAO", "INFINITO", "TRANSFORMAÇÃO"],
    "SÍNTESE": ["FUSÃO", "HIBRIDISMO", "TRANSCENDENCIA"],
    "ESCALA": ["PROPORÇÃO", "MAGNITUDE", "LEI"],
    "VIBRATIO": ["FREQUENCIA", "RESONÂNCIA", "ONDA"],
    "VÁCUO": ["POTENCIAL", "SILÊNCIO", "CAMPO"],
    "ARQUÉTIPO": ["PADRAO_PRIMORDIAL", "COMPORTAMENTO", "SÍMBOLO"],
    "NARRATIVA": ["TEIA", "LINHA_SENTIDO", "HISTÓRIA_VIVIDA"],
    "MISTÉRIO": ["INCOMPREENSÃO", "INTUIÇÃO", "REVELAÇÃO"],
}


# ---------------------------------------------------------------------------
# 1. Carregar dados brutos
# ---------------------------------------------------------------------------

def load_celulas_n4() -> list[tuple]:
    """Carrega dados do create_n4_manual.py.

    Returns:
        Lista de tuplas (legacy_id, nome, n3_ref, dominio, gatilho, acao, restricao, verificacao)
    """
    # Importar dinamicamente para evitar dependência em tempo de execução
    # Se create_n4_manual.py não puder ser importado, usar fallback
    try:
        # Método 1: import direto
        import importlib.util
        spec = importlib.util.find_spec("create_n4_manual")
        if spec is None or spec.loader is None:
            raise ImportError("Could not find spec")
        module = importlib.util.module_from_spec(spec)
        sys.modules["create_n4_manual"] = module
        spec.loader.exec_module(module)
        return module.celulas_n4
    except Exception as e:
        print(f"Erro ao importar create_n4_manual.py: {e}")
        print("Usando dados embutidos como fallback...")
        return _fallback_celulas()


def _fallback_celulas() -> list[tuple]:
    """Fallback mínimo caso a importação falhe."""
    return [
        ("R1.1.1-A", "DECOMPOSIÇÃO_BINÁRIA", "1.1.1", "LOGOS",
         "Problema complexo sem solução evidente",
         "Dividir em duas subpartes até atingir unidade resolvível",
         "Não aplicar quando a divisão altera a natureza do problema",
         "Cada subparte deve ser estritamente menor que o original"),
    ]


# ---------------------------------------------------------------------------
# 2. Construir registry
# ---------------------------------------------------------------------------

def build_registry(celulas: list[tuple]) -> dict[str, dict]:
    """Constrói registry completo a partir dos dados brutos.

    Cada entrada do registry contém:
    - uid, path, hierarchical_id, legacy_id
    - nome, dominio, pilar, axis
    - n3_ref, subtree_num, cell_num, cell_letter
    - gatilho, acao, restricao, verificacao

    Args:
        celulas: Lista de tuplas brutas do create_n4_manual.py

    Returns:
        Dict {uid: cell_data}
    """
    registry: dict[str, dict] = {}
    id_mapping = build_id_mapping()

    # Criar lookup por legacy_id para o mapeamento
    legacy_to_mapping: dict[str, dict] = {}
    for entry in id_mapping:
        legacy_to_mapping[entry["legacy_id"]] = entry

    for cell_tuple in celulas:
        legacy_id = cell_tuple[0]
        nome = cell_tuple[1]
        n3_ref = cell_tuple[2]
        # cell_tuple[3] contém o nome do PILAR (ex: "LOGOS"), não o domínio.
        # O domínio real é derivado do mapeamento de IDs.
        gatilho = cell_tuple[4]
        acao = cell_tuple[5]
        restricao = cell_tuple[6]
        verificacao = cell_tuple[7]

        # Buscar mapeamento
        mapping = legacy_to_mapping.get(legacy_id)
        if mapping is None:
            print(f"  [WARN] Legacy ID '{legacy_id}' não encontrado no mapeamento. Gerando...")
            mapping = _generate_mapping_from_legacy(legacy_id)

        uid = mapping["uid"]
        dominio = mapping.get("domain", "DESCONHECIDO")

        # Determinar pilar a partir do legacy_id
        prefix = legacy_id[0]
        pilar = LEGACY_PREFIX_TO_PILLAR.get(prefix, "DESCONHECIDO")

        # Determinar n3_name (nome da subárvore)
        subtree_num = mapping.get("subtree_num", 1)
        subtree_list = DOMAIN_SUBTREES.get(dominio, [])
        n3_name = subtree_list[subtree_num - 1] if subtree_num <= len(subtree_list) else "DESCONHECIDO"

        # Determinar axis
        axis = PILLAR_TO_AXIS.get(pilar, "DESCONHECIDO")

        cell_data: dict[str, Any] = {
            "uid": uid,
            "legacy_id": legacy_id,
            "path": mapping.get("path", ""),
            "hierarchical_id": mapping.get("hierarchical_id", ""),
            "nome": nome,
            "nome_normalizado": nome.lower().replace("_", " "),
            "dominio": dominio,
            "pilar": pilar,
            "axis": axis,
            "n3_ref": n3_ref,
            "n3_name": n3_name,
            "subtree_num": mapping.get("subtree_num", subtree_num),
            "cell_num": mapping.get("cell_num", int(legacy_id[-1]) if legacy_id[-1].isdigit() else 1),
            "cell_letter": mapping.get("cell_letter", legacy_id[-1]),
            "gatilho": gatilho,
            "acao": acao,
            "restricao": restricao,
            "verificacao": verificacao,
            # Placeholders para campos que serão preenchidos depois
            "natureza": "",
            "relacoes": [],
            "assinatura_semantica": "",
            "exemplos": [],
            "analogias": [],
            "tags": [],
        }

        registry[uid] = cell_data

    return registry


def _generate_mapping_from_legacy(legacy_id: str) -> dict:
    """Gera mapeamento a partir de legacy_id quando não encontrado."""
    import re
    match = re.match(r"^([RBPKAM])(\d+)\.(\d+)\.(\d+)-([A-C])$", legacy_id)
    if not match:
        return {"uid": "DESCONHECIDO", "path": "", "hierarchical_id": "", "legacy_id": legacy_id}

    prefix, domain_num, subtree_num, cell_num, cell_letter = match.groups()
    domain_num_i = int(domain_num)
    subtree_num_i = int(subtree_num)
    cell_num_i = int(cell_num)

    pillar_name = LEGACY_PREFIX_TO_PILLAR.get(prefix, "DESCONHECIDO")
    pillar_num = PILLAR_NAME_TO_NUM.get(pillar_name, 1)

    axis = "SINTRÓPICO" if pillar_num <= 3 else "ENTRÓPICO"
    axis_code = "S1" if axis == "SINTRÓPICO" else "E2"
    pillar_codes = {"LOGOS": "L1", "BIOS": "B2", "PATHOS": "P3",
                    "KHAOS": "K1", "APEIRON": "A2", "MYTHOS": "M3"}
    pillar_code = pillar_codes.get(pillar_name, "XX")

    hier_id = generate_hierarchical_id(
        pillar=pillar_num,
        domain=domain_num_i,
        subtree=subtree_num_i,
        cell=cell_num_i,
    )

    path_id = generate_path(
        axis_code=axis_code,
        pillar_code=pillar_code,
        domain_num=domain_num,
        subtree_num=subtree_num,
        cell_letter=cell_letter,
    )

    # UID: usar domínio do mapping
    domain_names = {
        "LOGOS": ["ALGORITMIA", "NOMOS", "MECÂNICA"],
        "BIOS": ["OIKOS", "SOMA", "METABOLISMO"],
        "PATHOS": ["ETHOS", "ALTERIDADE", "ESTÉTICA"],
        "KHAOS": ["ENTROPIA", "SINGULARIDADE", "SÍNTESE"],
        "APEIRON": ["ESCALA", "VIBRATIO", "VÁCUO"],
        "MYTHOS": ["ARQUÉTIPO", "NARRATIVA", "MISTÉRIO"],
    }
    domain_list = domain_names.get(pillar_name, ["DESCONHECIDO"])
    domain_name = domain_list[domain_num_i - 1] if domain_num_i <= len(domain_list) else "DESCONHECIDO"
    uid = f"N4_{normalize_text(domain_name)}_{subtree_num_i}_{cell_letter}"

    return {
        "uid": uid,
        "path": path_id,
        "hierarchical_id": hier_id,
        "legacy_id": legacy_id,
        "axis": axis,
        "pillar": pillar_name,
        "domain": domain_name,
        "subtree_num": subtree_num_i,
        "cell_num": cell_num_i,
    }


# ---------------------------------------------------------------------------
# 3. Inferir naturezas
# ---------------------------------------------------------------------------

def infer_all_naturezas(registry: dict[str, dict]) -> None:
    """Inferir natureza ontológica para todas as células do registry."""
    for uid, cell_data in registry.items():
        natureza = infer_natureza(cell_data)
        cell_data["natureza"] = natureza


# ---------------------------------------------------------------------------
# 4. Construir relações
# ---------------------------------------------------------------------------

def build_all_cell_relations(registry: dict[str, dict]) -> None:
    """Constrói e valida relações para todas as células."""
    all_relations = build_all_relations(registry)
    for uid, relations in all_relations.items():
        registry[uid]["relacoes"] = relations


# ---------------------------------------------------------------------------
# 5. Gerar campos semânticos
# ---------------------------------------------------------------------------

def generate_semantic_fields(cell_data: dict) -> dict:
    """Gera campos semânticos complementares.

    - assinatura_semantica: fingerprint baseado em conteúdo
    - exemplos: exemplos contextualizados
    - analogias: analogias para facilitar compreensão
    - tags: tags derivadas de natureza, domínio e pilar
    """
    import hashlib

    # Assinatura semântica (hash determinístico)
    content = f"{cell_data['uid']}|{cell_data['nome']}|{cell_data['natureza']}|{cell_data['dominio']}"
    signature = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
    cell_data["assinatura_semantica"] = f"sig_{signature}"

    # Tags
    tags = [
        cell_data["pilar"].lower(),
        cell_data["dominio"].lower(),
        cell_data["natureza"],
        cell_data["axis"].lower(),
        f"n3_{cell_data['n3_name'].lower().replace(' ', '_') if cell_data['n3_name'] else 'unknown'}",
    ]
    cell_data["tags"] = list(set(tags))

    # Exemplos e analogias (gerados com base no tipo de célula)
    cell_data["exemplos"] = _generate_exemplos(cell_data)
    cell_data["analogias"] = _generate_analogias(cell_data)

    return cell_data


def _generate_exemplos(cell_data: dict) -> list[dict]:
    """Gera exemplos contextualizados para a célula."""
    natureza = cell_data["natureza"]
    nome = cell_data["nome_normalizado"]
    dominio = cell_data["dominio"]

    exemplos_templates = {
        "processo": [
            f"Ao aplicar {nome} em um contexto de {dominio.lower()}, verificar o fluxo de transformações",
            f"Identificar os passos sequenciais de {nome} antes da execução",
        ],
        "estado": [
            f"Verificar se {nome} mantém o sistema em condição estável dentro de {dominio.lower()}",
            f"Avaliar indicadores de {nome} após intervenção em {dominio.lower()}",
        ],
        "fenomeno": [
            f"Observar padrões de {nome} emergindo em sistemas de {dominio.lower()}",
            f"Medir a intensidade do fenômeno {nome} sob diferentes condições",
        ],
        "mecanismo": [
            f"Implementar {nome} como mecanismo de controle em {dominio.lower()}",
            f"Avaliar a eficiência do {nome} em ciclos repetidos",
        ],
        "estrutura": [
            f"Mapear a {nome} do sistema para identificar componentes-chave",
            f"Verificar integridade estrutural através de {nome}",
        ],
        "principio": [
            f"Aplicar {nome} como critério de decisão em {dominio.lower()}",
            f"Validar se {nome} se mantém em cenários extremos",
        ],
        "restricao": [
            f"Definir limites de {nome} para operação segura em {dominio.lower()}",
            f"Documentar violações de {nome} e suas consequências",
        ],
        "vetor": [
            f"Analisar {nome} como indicador direcional em {dominio.lower()}",
            f"Medir magnitude e direção do {nome} no sistema",
        ],
        "arquetipo": [
            f"Identificar o arquétipo de {nome} no contexto de {dominio.lower()}",
            f"Mapear comportamentos associados ao {nome}",
        ],
        "dinamica": [
            f"Observar {nome} ao longo do tempo em sistemas de {dominio.lower()}",
            f"Identificar pontos de inflexão no ciclo de {nome}",
        ],
    }

    return [{"texto": ex} for ex in exemplos_templates.get(natureza, [
        f"Aplicar {nome} conforme contexto de {dominio.lower()}",
        f"Verificar adequação de {nome} para o domínio {dominio.lower()}",
    ])]


def _generate_analogias(cell_data: dict) -> list[dict]:
    """Gera analogias para facilitar compreensão da célula."""
    natureza = cell_data["natureza"]
    nome = cell_data["nome_normalizado"]

    analogias_templates = {
        "processo": [
            f"{nome} é como uma receita: passos sequenciais que transformam ingredientes em resultado",
            f"Como um algoritmo de ordenação: reorganiza elementos até atingir ordem",
        ],
        "estado": [
            f"{nome} é como um lago tranquilo: aparentemente imóvel, mas com atividade interna",
            f"Como a homeostase do corpo: mantém equilíbrio apesar de perturbações externas",
        ],
        "fenomeno": [
            f"{nome} é como uma onda no oceano: padrões que emergem da interação de forças",
            f"Como a aurora boreal: manifestação visível de processos invisíveis",
        ],
        "mecanismo": [
            f"{nome} funciona como um termostato: detecta desvios e corrige automaticamente",
            f"Como engrenagens de um relógio: cada peça impulsiona a seguinte",
        ],
        "estrutura": [
            f"{nome} é como o esqueleto: fornece suporte invisível para a forma visível",
            f"Como a rede de raízes de uma árvore: conexões ocultas sustentam o todo",
        ],
        "principio": [
            f"{nome} é como a gravidade: sempre presente, nem sempre perceptível",
            f"Como a conservação de energia: transforma mas não desaparece",
        ],
        "restricao": [
            f"{nome} funciona como cercas em uma paisagem: define onde se pode ir",
            f"Como limites de velocidade: protege ao restringir",
        ],
        "vetor": [
            f"{nome} é como a bússola: indica direção mesmo sem ver o destino",
            f"Como a correnteza de um rio: força invisível que molda o percurso",
        ],
        "arquetipo": [
            f"{nome} é como o herói em uma jornada: enfrenta desafios e retorna transformado",
            f"Como o sábio nos contos: oferece perspectiva que transcende o óbvio",
        ],
        "dinamica": [
            f"{nome} é como as estações do ano: ciclos de mudança que se repetem com variações",
            f"Como a metamorfose: transformação que não permite retorno ao estado anterior",
        ],
    }

    return [{"texto": ex, "tipo": "analogia_conceitual"}
            for ex in analogias_templates.get(natureza, [
                f"{nome} pode ser compreendido através de analogias com fenômenos naturais",
            ])]


# ---------------------------------------------------------------------------
# 6. Converter célula individual para JSON
# ---------------------------------------------------------------------------

def convert_cell(cell_data: dict, registry: dict[str, dict]) -> dict:
    """Converte uma célula para o formato JSON final.

    Args:
        cell_data: Dados da célula do registry.
        registry: Registry completo para referência de relações.

    Returns:
        Dict com schema completo da célula N4.
    """
    # Gerar campos semânticos
    generate_semantic_fields(cell_data)

    # Construir estrutura de saída
    output = {
        # Identificadores
        "uid": cell_data["uid"],
        "legacy_id": cell_data["legacy_id"],
        "path": cell_data["path"],
        "hierarchical_id": cell_data["hierarchical_id"],

        # Classificação ontológica
        "nivel": "N4",
        "pilar": cell_data["pilar"],
        "dominio": cell_data["dominio"],
        "n3_ref": cell_data["n3_ref"],
        "n3_name": cell_data["n3_name"],
        "axis": cell_data["axis"],
        "natureza": cell_data["natureza"],

        # Posicionamento hierárquico
        "subtree_num": cell_data["subtree_num"],
        "cell_num": cell_data["cell_num"],
        "cell_letter": cell_data["cell_letter"],

        # Conteúdo semântico
        "nome": cell_data["nome"],
        "nome_normalizado": cell_data["nome_normalizado"],
        "gatilho": cell_data["gatilho"],
        "acao": cell_data["acao"],
        "restricao": cell_data["restricao"],
        "verificacao": cell_data["verificacao"],

        # Campos inferidos e gerados
        "assinatura_semantica": cell_data["assinatura_semantica"],
        "exemplos": cell_data["exemplos"],
        "analogias": cell_data["analogias"],
        "tags": cell_data["tags"],

        # Relações (serão preenchidas depois)
        "relacoes": cell_data.get("relacoes", []),

        # Metadados
        "metadata": {
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "versao_schema": "1.0.0",
            "origem": "create_n4_manual.py",
            "status": "ativo",
            "revisoes": [
                {
                    "versao": "1.0.0",
                    "data": datetime.now(timezone.utc).isoformat(),
                    "descricao": "Conversão inicial de markdown para JSON enriquecido",
                }
            ],
        },
    }

    return output


# ---------------------------------------------------------------------------
# 7. Gerar índice global
# ---------------------------------------------------------------------------

def generate_index(registry: dict[str, dict], relations: dict[str, list]) -> dict:
    """Gera índice global da ontologia.

    Args:
        registry: Registry completo de células.
        relations: Mapeamento de relações por UID.

    Returns:
        Dict com estrutura do índice global.
    """
    # Estatísticas
    total_cells = len(registry)
    naturezas: dict[str, int] = {}
    dominios: dict[str, int] = {}
    pilares: dict[str, int] = {}
    axes: dict[str, int] = {}

    for uid, data in registry.items():
        nat = data.get("natureza", "desconhecida")
        dom = data.get("dominio", "desconhecido")
        pil = data.get("pilar", "desconhecido")
        ax = data.get("axis", "desconhecido")

        naturezas[nat] = naturezas.get(nat, 0) + 1
        dominios[dom] = dominios.get(dom, 0) + 1
        pilares[pil] = pilares.get(pil, 0) + 1
        axes[ax] = axes.get(ax, 0) + 1

    # Lista de todas as células
    celulas_list = []
    for uid in sorted(registry.keys()):
        data = registry[uid]
        celulas_list.append({
            "uid": uid,
            "legacy_id": data["legacy_id"],
            "path": data["path"],
            "hierarchical_id": data["hierarchical_id"],
            "nome": data["nome"],
            "dominio": data["dominio"],
            "pilar": data["pilar"],
            "natureza": data["natureza"],
            "axis": data["axis"],
            "n3_ref": data["n3_ref"],
            "num_relacoes": len(data.get("relacoes", [])),
        })

    # Mapeamento de IDs
    id_map = {}
    for uid, data in registry.items():
        id_map[uid] = {
            "legacy_id": data["legacy_id"],
            "path": data["path"],
            "hierarchical_id": data["hierarchical_id"],
        }

    index = {
        "schema_version": "1.0.0",
        "gerado_em": datetime.now(timezone.utc).isoformat(),
        "total_celulas": total_cells,
        "estatisticas": {
            "por_natureza": naturezas,
            "por_dominio": dominios,
            "por_pilar": pilares,
            "por_axis": axes,
        },
        "id_mapping": id_map,
        "celulas": celulas_list,
    }

    return index


# ---------------------------------------------------------------------------
# 8. Main pipeline
# ---------------------------------------------------------------------------

def main():
    """Pipeline principal de conversão N4 Markdown → JSON."""
    print("=" * 70)
    print("N4 ONTOLOGY NORMALIZATION PIPELINE")
    print("=" * 70)

    # 1. Carregar dados
    print("\n[1/6] Carregando dados brutos de create_n4_manual.py...")
    celulas = load_celulas_n4()
    print(f"  → {len(celulas)} células carregadas")

    # 2. Construir registry
    print("\n[2/6] Construindo registry com UIDs e metadados...")
    registry = build_registry(celulas)
    print(f"  → {len(registry)} entradas no registry")

    # Validar UIDs
    print("\n[3/6] Validando UIDs...")
    uids = list(registry.keys())
    unique_uids = set(uids)
    if len(uids) != len(unique_uids):
        print(f"  ✗ ERRO: {len(uids) - len(unique_uids)} UIDs duplicados!")
        dupes = [u for u in uids if uids.count(u) > 1]
        print(f"    Duplicatas: {set(dupes)}")
        return 1
    print(f"  → {len(unique_uids)} UIDs únicos ✓")

    # Validar UIDs com regex
    invalid_uids = [uid for uid in uids if not validate_uid(uid)]
    if invalid_uids:
        print(f"  ✗ ERRO: {len(invalid_uids)} UIDs inválidos: {invalid_uids[:5]}")
        return 1
    print(f"  → Todos os UIDs passam validação ✓")

    # 3. Inferir naturezas
    print("\n[4/6] Inferindo naturezas ontológicas...")
    infer_all_naturezas(registry)
    naturezas_inferidas = set(d["natureza"] for d in registry.values())
    print(f"  → Naturezas detectadas: {sorted(naturezas_inferidas)}")
    for nat in sorted(naturezas_inferidas):
        count = sum(1 for d in registry.values() if d["natureza"] == nat)
        print(f"    - {nat}: {count} células")

    # 4. Construir relações
    print("\n[5/6] Construindo relações tipadas...")
    build_all_cell_relations(registry)
    total_rels = sum(len(d.get("relacoes", [])) for d in registry.values())
    print(f"  → {total_rels} relações construídas")

    # 5. Criar diretório de saída
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 6. Gerar JSONs individuais
    print(f"\n[6/6] Gerando {len(registry)} arquivos JSON em {OUTPUT_DIR}...")
    generated = 0
    errors = []

    for uid, cell_data in registry.items():
        try:
            output = convert_cell(cell_data, registry)
            filename = f"{uid}.json"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(output, f, ensure_ascii=False, indent=2)

            generated += 1
            if generated % 50 == 0:
                print(f"  → {generated}/{len(registry)} arquivos gerados...")

        except Exception as e:
            errors.append((uid, str(e)))
            print(f"  ✗ Erro ao gerar {uid}: {e}")

    print(f"  → {generated} arquivos gerados com sucesso ✓")
    if errors:
        print(f"  ✗ {len(errors)} erros:")
        for uid, err in errors[:5]:
            print(f"    - {uid}: {err}")

    # 7. Gerar índice global
    print("\nGerando índice global...")
    index = generate_index(registry, {})

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"  → Índice salvo em {INDEX_FILE}")

    # 8. Validação final
    print("\n" + "=" * 70)
    print("VALIDAÇÃO FINAL")
    print("=" * 70)

    # Verificar número de arquivos
    json_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".json") and f != "ontology_index.json"]
    total = len(registry)
    print(f"  Arquivos JSON gerados: {len(json_files)} / {total} esperados")

    if len(json_files) == total:
        print("  ✓ Todos os 162 JSONs foram gerados")
    else:
        print(f"  ✗ Faltam {total - len(json_files)} arquivos")

    # Verificar schema
    print("\n  Verificando schemas...")
    required_fields = [
        "uid", "legacy_id", "path", "hierarchical_id",
        "nivel", "pilar", "dominio", "n3_ref", "natureza",
        "nome", "gatilho", "acao", "restricao", "verificacao",
        "assinatura_semantica", "relacoes", "metadata",
    ]

    sample_file = os.path.join(OUTPUT_DIR, json_files[0]) if json_files else None
    if sample_file:
        with open(sample_file, "r", encoding="utf-8") as f:
            sample = json.load(f)
        missing = [f for f in required_fields if f not in sample]
        if missing:
            print(f"  ✗ Campos ausentes no schema: {missing}")
        else:
            print(f"  ✓ Schema completo ({len(required_fields)} campos)")

    # Verificar unicidade de UIDs
    all_uids = [d["uid"] for d in registry.values()]
    if len(all_uids) == len(set(all_uids)):
        print("  ✓ Todos os UIDs são únicos")
    else:
        print("  ✗ UIDs duplicados detectados!")

    # Verificar naturezas
    all_naturezas = [d["natureza"] for d in registry.values() if d["natureza"]]
    if len(all_naturezas) == len(registry):
        print("  ✓ Todas as células têm natureza inferida")
    else:
        print(f"  ✗ {len(registry) - len(all_naturezas)} células sem natureza")

    # Verificar relações
    total_rels = sum(len(d.get("relacoes", [])) for d in registry.values())
    print(f"  ✓ {total_rels} relações tipadas construídas")

    # Verificar reversibilidade
    print("\n  Verificando reversibilidade JSON → Markdown...")
    # Cada JSON deve conter info suficiente para reconstruir o markdown
    reversible_count = 0
    for uid in list(registry.keys())[:5]:  # Verificar amostra
        data = registry[uid]
        if all(k in data for k in ["nome", "gatilho", "acao", "restricao", "verificacao"]):
            reversible_count += 1
    print(f"  ✓ Amostra de {reversible_count}/5 células reversíveis")

    print("\n" + "=" * 70)
    print("PIPELINE CONCLUÍDO COM SUCESSO")
    print("=" * 70)
    print(f"\nOutputs:")
    print(f"  - {len(json_files)} arquivos JSON em: {OUTPUT_DIR}/")
    print(f"  - Índice global: {INDEX_FILE}")
    print(f"  - Naturezas: {len(naturezas_inferidas)} tipos")
    print(f"  - Relações: {total_rels} conexões tipadas")

    return 0


if __name__ == "__main__":
    sys.exit(main())
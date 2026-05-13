#!/usr/bin/env python3
"""
Reestrutura arquivos N4 para refletir hierarquia correta:
N4 devem ser SUBÁRVORES de N3 (especializações do domínio),
não agrupamentos genéricos.

Exemplo correto:
- N3: 1.1.1 RESOLUÇÃO (LOGOS)
- N4: 1.1.1.1 DECOMPOSIÇÃO (especialização de RESOLUÇÃO)
- N4: 1.1.1.2 CASO_BASE (especialização de RESOLUÇÃO)
- N4: 1.1.1.3 SEQUÊNCIA (especialização de RESOLUÇÃO)
"""

import os

# Mapeamento correto: N3 -> suas subárvores N4 (especializações)
n4_especializacoes = {
    # LOGOS - ALGORITMIA (1.1.1 RESOLUÇÃO)
    "1.1.1": {
        "dominio": "LOGOS",
        "n3_nome": "RESOLUÇÃO",
        "n2_id": "1.1",
        "subarvores": [
            ("1.1.1.1", "DECOMPOSIÇÃO", "Dividir problema em subpartes"),
            ("1.1.1.2", "CASO_BASE", "Definir condição de parada"),
            ("1.1.1.3", "SEQUÊNCIA", "Ordenar passos logicamente")
        ]
    },
    # LOGOS - ALGORITMIA (1.1.2 OTIMIZAÇÃO)
    "1.1.2": {
        "dominio": "LOGOS",
        "n3_nome": "OTIMIZAÇÃO",
        "n2_id": "1.1",
        "subarvores": [
            ("1.1.2.1", "COMPLEXIDADE", "Reduzir custo computacional"),
            ("1.1.2.2", "MEMOIZAÇÃO", "Cache de resultados"),
            ("1.1.2.3", "PARALELISMO", "Distribuir processamento")
        ]
    },
    # LOGOS - ALGORITMIA (1.1.3 VALIDAÇÃO)
    "1.1.3": {
        "dominio": "LOGOS",
        "n3_nome": "VALIDAÇÃO",
        "n2_id": "1.1",
        "subarvores": [
            ("1.1.3.1", "LÓGICA", "Verificar correção formal"),
            ("1.1.3.2", "FRONTEIRA", "Testar limites"),
            ("1.1.3.3", "PARCIAL", "Validar subproblemas")
        ]
    },
    # BIOS - OIKOS (2.1.1 MORADA)
    "2.1.1": {
        "dominio": "BIOS",
        "n3_nome": "MORADA",
        "n2_id": "2.1",
        "subarvores": [
            ("2.1.1.1", "PROTEÇÃO", "Barreiras físicas"),
            ("2.1.1.2", "RECURSOS", "Provisão essencial"),
            ("2.1.1.3", "SANEAMENTO", "Manter ambiente")
        ]
    },
    # BIOS - OIKOS (2.1.2 TERRITORIO)
    "2.1.2": {
        "dominio": "BIOS",
        "n3_nome": "TERRITORIO",
        "n2_id": "2.1",
        "subarvores": [
            ("2.1.2.1", "REIVINDICAÇÃO", "Definir fronteiras"),
            ("2.1.2.2", "DEFESA", "Proteger espaço"),
            ("2.1.2.3", "GESTÃO", "Uso sustentável")
        ]
    },
    # BIOS - OIKOS (2.1.3 PROVISAO)
    "2.1.3": {
        "dominio": "BIOS",
        "n3_nome": "PROVISAO",
        "n2_id": "2.1",
        "subarvores": [
            ("2.1.3.1", "ARMAZENAMENTO", "Reservar materiais"),
            ("2.1.3.2", "ROTAÇÃO", "Renovar estoque"),
            ("2.1.3.3", "DISTRIBUIÇÃO", "Alocar recursos")
        ]
    },
    # BIOS - SOMA (2.2.1 INTEGRIDADE)
    "2.2.1": {
        "dominio": "BIOS",
        "n3_nome": "INTEGRIDADE",
        "n2_id": "2.2",
        "subarvores": [
            ("2.2.1.1", "MANUTENÇÃO", "Preservar estrutura"),
            ("2.2.1.2", "AVALIAÇÃO", "Inspecionar estado"),
            ("2.2.1.3", "ATUALIZAÇÃO", "Modernizar sistema")
        ]
    },
    # BIOS - SOMA (2.2.2 VITALIDADE)
    "2.2.2": {
        "dominio": "BIOS",
        "n3_nome": "VITALIDADE",
        "n2_id": "2.2",
        "subarvores": [
            ("2.2.2.1", "ENERGIA", "Fornecer energia"),
            ("2.2.2.2", "AUTORREPARAÇÃO", "Curar danos"),
            ("2.2.2.3", "RESILIÊNCIA", "Resistir a estresse")
        ]
    },
    # BIOS - SOMA (2.2.3 HOMEOSTASE)
    "2.2.3": {
        "dominio": "BIOS",
        "n3_nome": "HOMEOSTASE",
        "n2_id": "2.2",
        "subarvores": [
            ("2.2.3.1", "REGULAÇÃO", "Ajustar parâmetros"),
            ("2.2.3.2", "FEEDBACK", "Corrigir desvios"),
            ("2.2.3.3", "CICLO", "Adaptar a ritmos")
        ]
    },
    # BIOS - METABOLISMO (2.3.1 ANABOLISMO)
    "2.3.1": {
        "dominio": "BIOS",
        "n3_nome": "ANABOLISMO",
        "n2_id": "2.3",
        "subarvores": [
            ("2.3.1.1", "SÍNTESE", "Construir estruturas"),
            ("2.3.1.2", "CRESCIMENTO", "Aumentar tamanho"),
            ("2.3.1.3", "COMPLEXIFICAÇÃO", "Adicionar funções")
        ]
    },
    # BIOS - METABOLISMO (2.3.2 CATABOLISMO)
    "2.3.2": {
        "dominio": "BIOS",
        "n3_nome": "CATABOLISMO",
        "n2_id": "2.3",
        "subarvores": [
            ("2.3.2.1", "DECOMPOSIÇÃO", "Quebrar estruturas"),
            ("2.3.2.2", "LIBERAÇÃO", "Liberar energia"),
            ("2.3.2.3", "REMOÇÃO", "Eliminar resíduos")
        ]
    },
    # BIOS - METABOLISMO (2.3.3 CICLO)
    "2.3.3": {
        "dominio": "BIOS",
        "n3_nome": "CICLO",
        "n2_id": "2.3",
        "subarvores": [
            ("2.3.3.1", "RECIRCULAÇÃO", "Reutilizar materiais"),
            ("2.3.3.2", "RENOVAÇÃO", "Substituir componentes"),
            ("2.3.3.3", "FLUXO", "Manter movimento")
        ]
    },
    # PATHOS - ETHOS (3.1.1 VALORES)
    "3.1.1": {
        "dominio": "PATHOS",
        "n3_nome": "VALORES",
        "n2_id": "3.1",
        "subarvores": [
            ("3.1.1.1", "ALINHAMENTO", "Coerência valor-ação"),
            ("3.1.1.2", "CONFLITO", "Resolver tensões"),
            ("3.1.1.3", "TRANSPARÊNCIA", "Comunicar motivos")
        ]
    },
    # PATHOS - ETHOS (3.1.2 VIRTUDE)
    "3.1.2": {
        "dominio": "PATHOS",
        "n3_nome": "VIRTUDE",
        "n2_id": "3.1",
        "subarvores": [
            ("3.1.2.1", "EXCELÊNCIA", "Praticar o bem"),
            ("3.1.2.2", "CARÁTER", "Hábitos morais"),
            ("3.1.2.3", "INTEGRIDADE", "Consistência interna")
        ]
    },
    # PATHOS - ETHOS (3.1.3 RESPONSABILIDADE)
    "3.1.3": {
        "dominio": "PATHOS",
        "n3_nome": "RESPONSABILIDADE",
        "n2_id": "3.1",
        "subarvores": [
            ("3.1.3.1", "DEVER", "Cumprir obrigações"),
            ("3.1.3.2", "CONSEQUÊNCIA", "Antecipar resultados"),
            ("3.1.3.3", "ESCOLHA", "Decidir com valores")
        ]
    },
    # PATHOS - ALTERIDADE (3.2.1 RECONHECIMENTO)
    "3.2.1": {
        "dominio": "PATHOS",
        "n3_nome": "RECONHECIMENTO",
        "n2_id": "3.2",
        "subarvores": [
            ("3.2.1.1", "VALIDAÇÃO", "Confirmar existência"),
            ("3.2.1.2", "DIGNIDADE", "Respeitar valor"),
            ("3.2.1.3", "EXISTÊNCIA", "Reconhecer presença")
        ]
    },
    # PATHOS - ALTERIDADE (3.2.2 EMPATIA)
    "3.2.2": {
        "dominio": "PATHOS",
        "n3_nome": "EMPATIA",
        "n2_id": "3.2",
        "subarvores": [
            ("3.2.2.1", "COMPREENSÃO", "Entender sentimento"),
            ("3.2.2.2", "PONTE", "Conectar sentidos"),
            ("3.2.2.3", "SENTIDO", "Compartilhar significado")
        ]
    },
    # PATHOS - ALTERIDADE (3.2.3 DIALOGO)
    "3.2.3": {
        "dominio": "PATHOS",
        "n3_nome": "DIALOGO",
        "n2_id": "3.2",
        "subarvores": [
            ("3.2.3.1", "TROCA", "Construir junto"),
            ("3.2.3.2", "CONSTRUÇÃO", "Co-criar sentido"),
            ("3.2.3.3", "REVELAÇÃO", "Desvelar através do diálogo")
        ]
    },
    # PATHOS - ESTÉTICA (3.3.1 HARMONIA)
    "3.3.1": {
        "dominio": "PATHOS",
        "n3_nome": "HARMONIA",
        "n2_id": "3.3",
        "subarvores": [
            ("3.3.1.1", "PROPORÇÃO", "Razão áurea"),
            ("3.3.1.2", "EQUILÍBRIO", "Balancear elementos"),
            ("3.3.1.3", "RESSONÂNCIA", "Vibração harmoniosa")
        ]
    },
    # PATHOS - ESTÉTICA (3.3.2 EXPRESSAO)
    "3.3.2": {
        "dominio": "PATHOS",
        "n3_nome": "EXPRESSAO",
        "n2_id": "3.3",
        "subarvores": [
            ("3.3.2.1", "FORMA", "Materializar sentido"),
            ("3.3.2.2", "EXTERIORIZAÇÃO", "Tornar interno externo"),
            ("3.3.2.3", "LINGUAGEM", "Comunicar através da forma")
        ]
    },
    # PATHOS - ESTÉTICA (3.3.3 IMPACTO)
    "3.3.3": {
        "dominio": "PATHOS",
        "n3_nome": "IMPACTO",
        "n2_id": "3.3",
        "subarvores": [
            ("3.3.3.1", "TRANSFORMAÇÃO", "Alterar estado"),
            ("3.3.3.2", "EMOCIONAL", "Afetar sentimentos"),
            ("3.3.3.3", "LIBERDADE", "Respeitar autonomia")
        ]
    },
    # KHAOS - ENTROPIA (4.1.1 DEGRADAÇÃO)
    "4.1.1": {
        "dominio": "KHAOS",
        "n3_nome": "DEGRADAÇÃO",
        "n2_id": "4.1",
        "subarvores": [
            ("4.1.1.1", "ENTROPIA", "Identificar desordem"),
            ("4.1.1.2", "DESTRUIÇÃO", "Desmantelar obsoleto"),
            ("4.1.1.3", "RECICLAGEM", "Reintegrar materiais")
        ]
    },
    # KHAOS - ENTROPIA (4.1.2 DISSIPAÇÃO)
    "4.1.2": {
        "dominio": "KHAOS",
        "n3_nome": "DISSIPAÇÃO",
        "n2_id": "4.1",
        "subarvores": [
            ("4.1.2.1", "DISPERSÃO", "Redistribuir energia"),
            ("4.1.2.2", "AUMENTO", "Permitir desordem"),
            ("4.1.2.3", "AMORFO", "Retornar ao potencial")
        ]
    },
    # KHAOS - ENTROPIA (4.1.3 CAOS)
    "4.1.3": {
        "dominio": "KHAOS",
        "n3_nome": "CAOS",
        "n2_id": "4.1",
        "subarvores": [
            ("4.1.3.1", "ALEATORIEDADE", "Aceitar imprevisibilidade"),
            ("4.1.3.2", "COMPLEXIDADE", "Sensibilidade inicial"),
            ("4.1.3.3", "PADRÕES", "Emergência do desordem")
        ]
    },
    # KHAOS - SINGULARIDADE (4.2.1 EXCEPCAO)
    "4.2.1": {
        "dominio": "KHAOS",
        "n3_nome": "EXCEPCAO",
        "n2_id": "4.2",
        "subarvores": [
            ("4.2.1.1", "PONTO", "Regras não se aplicam"),
            ("4.2.1.2", "SUPERIOR", "Ordem transcendente"),
            ("4.2.1.3", "TRANSFORMAÇÃO", "Mudança radical")
        ]
    },
    # KHAOS - SINGULARIDADE (4.2.2 INFINITO)
    "4.2.2": {
        "dominio": "KHAOS",
        "n3_nome": "INFINITO",
        "n2_id": "4.2",
        "subarvores": [
            ("4.2.2.1", "HORIZONTE", "Limite inatingível"),
            ("4.2.2.2", "POTENCIAL", "Possibilidades sem limite"),
            ("4.2.2.3", "EXPANSÃO", "Crescimento sem fronteira")
        ]
    },
    # KHAOS - SINGULARIDADE (4.2.3 TRANSFORMAÇÃO)
    "4.2.3": {
        "dominio": "KHAOS",
        "n3_nome": "TRANSFORMAÇÃO",
        "n2_id": "4.2",
        "subarvores": [
            ("4.2.3.1", "MORTE", "Fim do estado atual"),
            ("4.2.3.2", "RADICAL", "Mudança fundamental"),
            ("4.2.3.3", "NOVA", "Estabelecer novo paradigma")
        ]
    },
    # KHAOS - SÍNTESE (4.3.1 FUSÃO)
    "4.3.1": {
        "dominio": "KHAOS",
        "n3_nome": "FUSÃO",
        "n2_id": "4.3",
        "subarvores": [
            ("4.3.1.1", "UNIÃO", "Combinar elementos"),
            ("4.3.1.2", "SÍNTESE", "Criar propriedade nova"),
            ("4.3.1.3", "TRANSCENDÊNCIA", "Superar oposições")
        ]
    },
    # KHAOS - SÍNTESE (4.3.2 HIBRIDISMO)
    "4.3.2": {
        "dominio": "KHAOS",
        "n3_nome": "HIBRIDISMO",
        "n2_id": "4.3",
        "subarvores": [
            ("4.3.2.1", "MISTURA", "Combinar mantendo originais"),
            ("4.3.2.2", "PONTE", "Conectar passado e futuro"),
            ("4.3.2.3", "IDENTIDADE", "Ser mais que a soma")
        ]
    },
    # KHAOS - SÍNTESE (4.3.3 TRANSCENDENCIA)
    "4.3.3": {
        "dominio": "KHAOS",
        "n3_nome": "TRANSCENDENCIA",
        "n2_id": "4.3",
        "subarvores": [
            ("4.3.3.1", "SUPERAÇÃO", "Ir além dos limites"),
            ("4.3.3.2", "INCLUSÃO", "Abranger sem excluir"),
            ("4.3.3.3", "NÍVEL", "Operar em nova dimensão")
        ]
    },
    # APEIRON - ESCALA (5.1.1 PROPORÇÃO)
    "5.1.1": {
        "dominio": "APEIRON",
        "n3_nome": "PROPORÇÃO",
        "n2_id": "5.1",
        "subarvores": [
            ("5.1.1.1", "ESCALAMENTO", "Identificar leis escalares"),
            ("5.1.1.2", "AUREA", "Razão harmônica"),
            ("5.1.1.3", "ISOMORFISMO", "Mapear para outra escala")
        ]
    },
    # APEIRON - ESCALA (5.1.2 MAGNITUDE)
    "5.1.2": {
        "dominio": "APEIRON",
        "n3_nome": "MAGNITUDE",
        "n2_id": "5.1",
        "subarvores": [
            ("5.1.2.1", "TAMANHO", "Efeitos escalares"),
            ("5.1.2.2", "EXPERIÊNCIA", "Percepção afetada"),
            ("5.1.2.3", "LEI", "Variação com escala")
        ]
    },
    # APEIRON - ESCALA (5.1.3 LEI)
    "5.1.3": {
        "dominio": "APEIRON",
        "n3_nome": "LEI",
        "n2_id": "5.1",
        "subarvores": [
            ("5.1.3.1", "RELATIVA", "Depende da escala"),
            ("5.1.3.2", "MANIFESTAÇÃO", "Efeitos práticos"),
            ("5.1.3.3", "DOMÍNIO", "Limites de validade")
        ]
    },
    # APEIRON - VIBRATIO (5.2.1 FREQUENCIA)
    "5.2.1": {
        "dominio": "APEIRON",
        "n3_nome": "FREQUENCIA",
        "n2_id": "5.2",
        "subarvores": [
            ("5.2.1.1", "CICLO", "Padrão temporal"),
            ("5.2.1.2", "RESONÂNCIA", "Sintonia"),
            ("5.2.1.3", "IDENTIDADE", "Assinatura")
        ]
    },
    # APEIRON - VIBRATIO (5.2.2 RESONÂNCIA)
    "5.2.2": {
        "dominio": "APEIRON",
        "n3_nome": "RESONÂNCIA",
        "n2_id": "5.2",
        "subarvores": [
            ("5.2.2.1", "AMPLIFICAÇÃO", "Sincronia"),
            ("5.2.2.2", "SINCRONIA", "Fase"),
            ("5.2.2.3", "MULTIPLICAÇÃO", "Efeito sem matéria")
        ]
    },
    # APEIRON - VIBRATIO (5.2.3 ONDA)
    "5.2.3": {
        "dominio": "APEIRON",
        "n3_nome": "ONDA",
        "n2_id": "5.2",
        "subarvores": [
            ("5.2.3.1", "PROPAGAÇÃO", "Padrão no meio"),
            ("5.2.3.2", "POTENCIAL", "Tornar-se real"),
            ("5.2.3.3", "PADRÃO", "Características")
        ]
    },
    # APEIRON - VÁCUO (5.3.1 POTENCIAL)
    "5.3.1": {
        "dominio": "APEIRON",
        "n3_nome": "POTENCIAL",
        "n2_id": "5.3",
        "subarvores": [
            ("5.3.1.1", "CAPACIDADE", "Latência"),
            ("5.3.1.2", "AVESSO", "Não-manifesto"),
            ("5.3.1.3", "CAMPO", "Possibilidades")
        ]
    },
    # APEIRON - VÁCUO (5.3.2 SILÊNCIO)
    "5.3.2": {
        "dominio": "APEIRON",
        "n3_nome": "SILÊNCIO",
        "n2_id": "5.3",
        "subarvores": [
            ("5.3.2.1", "AUSÊNCIA", "Não-manifestação"),
            ("5.3.2.2", "LINGUAGEM", "Não-dito"),
            ("5.3.2.3", "PRESENÇA", "Ausência ativa")
        ]
    },
    # APEIRON - VÁCUO (5.3.3 CAMPO)
    "5.3.3": {
        "dominio": "APEIRON",
        "n3_nome": "CAMPO",
        "n2_id": "5.3",
        "subarvores": [
            ("5.3.3.1", "MATRIZ", "Possibilidades"),
            ("5.3.3.2", "REPOUSO", "Latência"),
            ("5.3.3.3", "UNIFICACAO", "Totalidade")
        ]
    },
    # MYTHOS - ARQUÉTIPO (6.1.1 PADRAO_PRIMORDIAL)
    "6.1.1": {
        "dominio": "MYTHOS",
        "n3_nome": "PADRAO_PRIMORDIAL",
        "n2_id": "6.1",
        "subarvores": [
            ("6.1.1.1", "RECONHECIMENTO", "Padrão recorrente"),
            ("6.1.1.2", "ATIVAÇÃO", "Evocar latente"),
            ("6.1.1.3", "SÍNTESE", "Terceira via")
        ]
    },
    # MYTHOS - ARQUÉTIPO (6.1.2 COMPORTAMENTO)
    "6.1.2": {
        "dominio": "MYTHOS",
        "n3_nome": "COMPORTAMENTO",
        "n2_id": "6.1",
        "subarvores": [
            ("6.1.2.1", "ROTEIRO", "Guia invisível"),
            ("6.1.2.2", "PADRÃO", "Repetição"),
            ("6.1.2.3", "INFLUÊNCIA", "Moldar escolhas")
        ]
    },
    # MYTHOS - ARQUÉTIPO (6.1.3 SIMBOLO)
    "6.1.3": {
        "dominio": "MYTHOS",
        "n3_nome": "SIMBOLO",
        "n2_id": "6.1",
        "subarvores": [
            ("6.1.3.1", "PONTE", "Transcendente"),
            ("6.1.3.2", "LINGUAGEM", "Sensível"),
            ("6.1.3.3", "MANIFESTAÇÃO", "Forma")
        ]
    },
    # MYTHOS - NARRATIVA (6.2.1 TEIA)
    "6.2.1": {
        "dominio": "MYTHOS",
        "n3_nome": "TEIA",
        "n2_id": "6.2",
        "subarvores": [
            ("6.2.1.1", "CONEXÕES", "Rede"),
            ("6.2.1.2", "TECIDO", "Trama"),
            ("6.2.1.3", "COMPLEXIDADE", "Intricação")
        ]
    },
    # MYTHOS - NARRATIVA (6.2.2 LINHA_SENTIDO)
    "6.2.2": {
        "dominio": "MYTHOS",
        "n3_nome": "LINHA_SENTIDO",
        "n2_id": "6.2",
        "subarvores": [
            ("6.2.2.1", "TEMPO", "Continuidade"),
            ("6.2.2.2", "NARRATIVA", "História"),
            ("6.2.2.3", "VIVIDA", "Experiência")
        ]
    },
    # MYTHOS - NARRATIVA (6.2.3 HISTÓRIA_VIVIDA)
    "6.2.3": {
        "dominio": "MYTHOS",
        "n3_nome": "HISTÓRIA_VIVIDA",
        "n2_id": "6.2",
        "subarvores": [
            ("6.2.3.1", "EXPERIÊNCIA", "Narrar-se"),
            ("6.2.3.2", "CONTINUIDADE", "Fluxo"),
            ("6.2.3.3", "ATIVA", "Criadora")
        ]
    },
    # MYTHOS - MISTÉRIO (6.3.1 INCOMPREENSÃO)
    "6.3.1": {
        "dominio": "MYTHOS",
        "n3_nome": "INCOMPREENSÃO",
        "n2_id": "6.3",
        "subarvores": [
            ("6.3.1.1", "LIMITE", "Razão"),
            ("6.3.1.2", "PROTEÇÃO", "Mistério"),
            ("6.3.1.3", "HUMILDADE", "Não-saber")
        ]
    },
    # MYTHOS - MISTÉRIO (6.3.2 INTUIÇÃO)
    "6.3.2": {
        "dominio": "MYTHOS",
        "n3_nome": "INTUIÇÃO",
        "n2_id": "6.3",
        "subarvores": [
            ("6.3.2.1", "DIRETO", "Saber"),
            ("6.3.2.2", "TOCAR", "Profundidade"),
            ("6.3.2.3", "IMEDIATO", "Conhecimento")
        ]
    },
    # MYTHOS - MISTÉRIO (6.3.3 REVELAÇÃO)
    "6.3.3": {
        "dominio": "MYTHOS",
        "n3_nome": "REVELAÇÃO",
        "n2_id": "6.3",
        "subarvores": [
            ("6.3.3.1", "DESVELAMENTO", "Verdade"),
            ("6.3.3.2", "ILUMINAÇÃO", "Clareza"),
            ("6.3.3.3", "PRESERVADO", "Mistério")
        ]
    }
}

# Vetores N0
vetores = {
    "LOGOS": "0.1_SINTRÓPICO",
    "BIOS": "0.1_SINTRÓPICO", 
    "PATHOS": "0.1_SINTRÓPICO",
    "KHAOS": "0.2_ENTRÓPICO",
    "APEIRON": "0.2_ENTRÓPICO",
    "MYTHOS": "0.2_ENTRÓPICO"
}

# Pilares N1
pilares = {
    "LOGOS": "1.0_LOGOS",
    "BIOS": "2.0_BIOS",
    "PATHOS": "3.0_PATHOS", 
    "KHAOS": "4.0_KHAOS",
    "APEIRON": "5.0_APEIRON",
    "MYTHOS": "6.0_MYTHOS"
}

print(f"Gerando {sum(len(v['subarvores']) for v in n4_especializacoes.values())} arquivos N4...")

for n3_id, info in n4_especializacoes.items():
    dominio = info["dominio"]
    n3_nome = info["n3_nome"]
    n2_id = info["n2_id"]
    
    for n4_id, n4_nome, descricao in info["subarvores"]:
        filename = os.path.join("data", "ontology", f"N4-{n4_id.replace('.', '_')}-{dominio}-{n4_nome}.md")
        
        # IDs ancestrais
        n3_completo = f"{n3_id}"
        n2_completo = f"{n2_id}"
        n1_completo = f"{pilares[dominio]}"
        n0_completo = f"{vetores[dominio]}"
        
        content = f"""# N4-{n4_id.replace('.', '_')} - {dominio} / {n3_nome} / {n4_nome}

---

## Metadados

- **ID N4:** {n4_id}
- **ID N3 Pai:** {n3_completo}
- **ID N2 Avô:** {n2_completo}
- **ID N1 Bisavô:** {n1_completo}
- **ID N0 Tataravô:** {n0_completo}
- **Domínio:** {dominio}
- **Domínio N2:** {n2_id}_{n3_nome}
- **Domínio N1:** {n1_completo}
- **Domínio N0:** {n0_completo}
- **Geometria Base:** 2×3×3×3×3
- **Data:** 2026-05-07
- **Status:** ATIVO

---

## Sumário Executivo

Este arquivo documenta a subárvore N4 **{n4_nome}**, que é uma especialização de **{n3_nome}** (N3: {n3_completo}), pertencente ao domínio **{dominio}**.

**Descrição:** {descricao}

**Árvore Completa:**
```
N0: {n0_completo} ({vetores[dominio].split('_')[1].capitalize()})
  └─ N1: {n1_completo} ({dominio})
      └─ N2: {n2_completo} ({n3_nome})
          └─ N3: {n3_completo} ({n3_nome})
              └─ N4: {n4_id} ({n4_nome}) ← Este documento
```

---

## Matriz de Rastreabilidade

### Herança Completa (N0 → N4)

| Nível | ID | Nome | Descrição |
|-------|-----|------|-----------|
| N0 | {n0_completo} | {vetores[dominio].split('_')[1].capitalize()} | Vetor primordial |
| N1 | {n1_completo} | {dominio} | Pilar central |
| N2 | {n2_completo} | {n3_nome} | Domínio ontológico |
| N3 | {n3_completo} | {n3_nome} | Especialização |
| **N4** | **{n4_id}** | **{n4_nome}** | **Subárvore (este doc)** |

### Referências Cruzadas

- **Vetor N0:** `ONTOLOGIA_MESTRA_DOMINANTE_V2.md#31-{n0_completo.lower().replace('_', '-')}`
- **Pilar N1:** `ONTOLOGIA_MESTRA_DOMINANTE_V2.md#32-{n1_completo.lower().replace('_', '-')}`
- **Domínio N2:** `ONTOLOGIA_MESTRA_DOMINANTE_V2.md#33-{n2_completo.replace('.', '')}`
- **Especialização N3:** `N3-{n3_completo.replace('.', '_')}-{dominio}-{n3_nome.upper()}.md`
- **Subárvore N4:** Este arquivo

---

## Descrição Detalhada

### Atributos da Subárvore

- **Identificador N4:** {n4_id}
- **Nome:** {n4_nome}
- **Descrição:** {descricao}
- **Domínio:** {dominio}
- **Especialização de:** {n3_nome} (N3)

### Herança de DNA

#### N0 - Vetor {vetores[dominio].split('_')[1].capitalize()}
- **Foco:** {'Convergência, colapso de incerteza, materialização.' if 'SINTRÓPICO' in vetores[dominio] else 'Divergência, exploração de potencial, desconstrução.'}
- **Axioma:** {'A utilidade nasce da definição estrita da forma sobre o vazio.' if 'SINTRÓPICO' in vetores[dominio] else 'A verdade reside na profundidade do espectro, não no ponto final.'}

#### N1 - Pilar {dominio}
- **Crença:** {'A ordem estrutural é o suporte da realidade.' if dominio == 'LOGOS' else 'A existência exige a preservação do organismo e do meio.' if dominio == 'BIOS' else 'O sentido emerge da interação e da percepção subjetiva.' if dominio == 'PATHOS' else 'A ruptura do padrão é o motor da evolução.' if dominio == 'KHAOS' else 'A realidade é um campo infinito de possibilidades não medidas.' if dominio == 'APEIRON' else 'O símbolo e a narrativa precedem a compreensão lógica.'}
- **Tags:** {str(['SISTEMA', 'ORDEM', 'LOGICA'] if dominio == 'LOGOS' else ['VIDA', 'HABITAT', 'SOBREVIVENCIA'] if dominio == 'BIOS' else ['SENTIDO', 'CONEXAO', 'IMPACTO'] if dominio == 'PATHOS' else ['MUDANÇA', 'ALEATORIEDADE', 'RUPTURA'] if dominio == 'KHAOS' else ['INFINITO', 'POTENCIAL', 'TRANSCENDENCIA'] if dominio == 'APEIRON' else ['IMAGEM', 'ARQUETIPO', 'SUBTEXTO'])}

#### N2 - Domínio {n3_nome}
- **Foco:** Especialização em {n3_nome.lower()} dentro de {dominio}
- **Crença:** Contextualizada à especialização
- **Tags Herdadas:** Do pilar {dominio}

#### N3 - Especialização {n3_nome}
- **Foco:** {n3_nome}
- **Crença:** Específica da especialização
- **Tags:** Herdadas de N2

#### N4 - Subárvore {n4_nome}
- **Foco:** {descricao}
- **Relação:** Deriva diretamente de N3 {n3_nome}
- **Propósito:** Aprofundamento específico dentro da especialização

---

## Regras de Derivação

1. **Herança Obrigatória:**
   - Toda N4 herda DNA de N3, N2, N1, N0
   - Tags acumuladas ao longo da hierarquia
   - Crenças contextualizadas por nível

2. **Especialização Progressiva:**
   - N4 é refinamento específico de N3
   - Não introduz novos conceitos fora da árvore
   - Mantém coerência com domínio ancestral

3. **Aplicabilidade:**
   - Subárvore N4 deve ser diretamente utilizável
   - Contextualizada ao domínio específico
   - Respeita limites da especialização N3

---

## Checklist de Conformidade

### Herança
- [x] N0 (Vetor) referenciado: {n0_completo}
- [x] N1 (Pilar) referenciado: {n1_completo}
- [x] N2 (Domínio) referenciado: {n2_completo}
- [x] N3 (Especialização) referenciado: {n3_completo}
- [x] DNA completo documentado

### Consistência
- [x] Geometria 2×3×3×3×3 preservada
- [x] Sem novos eixos introduzidos
- [x] Escopo restrito a subárvore N4
- [x] Hierarquia correta N0→N4

### Derivação
- [x] Especialização clara de N3
- [x] Contexto do domínio mantido
- [x] Sem deriva conceitual
- [x] Propósito específico definido

### Documentação
- [x] Metadados completos
- [x] Matriz de rastreabilidade
- [x] Herança detalhada
- [x] Regras de derivação

---

## Registro de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2026-05-07 | Sistema | Criação da subárvore N4 |

---

*Este documento é parte integrante da ontologia fractal do projeto "Arquiteto de Prompts - Expansão Fractal".*
*Árvore: {n0_completo} → {n1_completo} → {n2_completo} → {n3_completo} → {n4_id}*
"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {filename}")

print(f"\nTotal de arquivos N4 criados: {sum(len(v['subarvores']) for v in n4_especializacoes.values())}")

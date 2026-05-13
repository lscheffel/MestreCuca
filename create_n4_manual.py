#!/usr/bin/env python3
"""Geração manual de arquivos N4 baseados nas células documentadas."""

# Células N4 documentadas na Taxonomia
# Formato: (cell_id, nome, n3_ref, dominio, gatilho, acao, restricao, verificacao)

celulas_n4 = [
    # RESOLUÇÃO - 1.1.1
    ("R1.1.1-A", "DECOMPOSIÇÃO_BINÁRIA", "1.1.1", "LOGOS",
     "Problema complexo sem solução evidente",
     "Dividir em duas subpartes até atingir unidade resolvível",
     "Não aplicar quando a divisão altera a natureza do problema",
     "Cada subparte deve ser estritamente menor que o original"),
    ("R1.1.1-B", "SEQUÊNCIA_OTIMIZADA", "1.1.1", "LOGOS",
     "Múltiplos passos possíveis para objetivo",
     "Identificar dependências e ordenar topologicamente",
     "Ignorar ordens que violem precedências lógicas",
     "Sequência deve ser executável sem retrocessos"),
    ("R1.1.1-C", "CASO_BASE", "1.1.1", "LOGOS",
     "Recursão ou processo iterativo",
     "Definir condição de parada e resultado trivial",
     "Caso base deve ser alcançável em passos finitos",
     "Processo converge para caso base"),

    # OPTIMIZAÇÃO - 1.1.2
    ("R1.1.2-A", "COMPLEXIDADE_TEMPORAL", "1.1.2", "LOGOS",
     "Algoritmo com performance inadequada",
     "Analisar notação Big-O e identificar gargalos",
     "Não otimizar prematuramente sem métricas",
     "Redução de complexidade sem perda de correção"),
    ("R1.1.2-B", "MEMOIZAÇÃO", "1.1.2", "LOGOS",
     "Cálculos repetidos com mesmos inputs",
     "Armazenar resultados anteriores em cache",
     "Avaliar custo memória vs benefício tempo",
     "Hits de cache > 50% das chamadas"),
    ("R1.1.2-C", "PARALELIZAÇÃO", "1.1.2", "LOGOS",
     "Tarefas independentes e custo computacional alto",
     "Distribuir trabalho across múltiplos workers",
     "Overhead de sincronização < 20% do ganho",
     "Speedup próximo ao linear com número de workers"),

    # VALIDAÇÃO - 1.1.3
    ("R1.1.3-A", "VERIFICAÇÃO_LÓGICA", "1.1.3", "LOGOS",
     "Correção do algoritmo em questão",
     "Aplicar provas de correção e invariáveis",
     "Não aceitar testes empíricos como prova",
     "Todas as precondições e pós-condições satisfeitas"),
    ("R1.1.3-B", "TESTE_DE_FRONTEIRA", "1.1.3", "LOGOS",
     "Identificar limites operacionais",
     "Testar casos extremos e limites do domínio",
     "Não extrapolar além dos limites definidos",
     "Comportamento correto em todos os limites"),
    ("R1.1.3-C", "CORREÇÃO_PARCIAL", "1.1.3", "LOGOS",
     "Solução parcial para problema maior",
     "Validar subproblemas independentemente",
     "Não compor soluções incorretas",
     "Correção de cada subproblema verificada"),

    # LEGISLAÇÃO - 1.2.1
    ("R1.2.1-A", "CODIFICAÇÃO_NORMA", "1.2.1", "LOGOS",
     "Regra ou regulamento a ser formalizado",
     "Expressar em linguagem formal e inequívoca",
     "Não deixar ambiguidades propositais",
     "Regra pode ser aplicada consistentemente"),
    ("R1.2.1-B", "VERIFICAÇÃO_CONFORMIDADE", "1.2.1", "LOGOS",
     "Avaliar conformidade com norma",
     "Verificar todos os requisitos explicitamente",
     "Não aceitar conformidade parcial",
     "100% dos requisitos atendidos"),
    ("R1.2.1-C", "HIERARQUIA_LEIS", "1.2.1", "LOGOS",
     "Conflito entre normas de diferentes níveis",
     "Aplicar lei de hierarquia superior",
     "Não criar hierarquia arbitrária",
     "Lei superior prevalece sem contradição"),

    # CONTORNO - 1.2.2
    ("R1.2.2-A", "DEFINIÇÃO_FRONTEIRA", "1.2.2", "LOGOS",
     "Delimitar escopo de sistema ou problema",
     "Especificar limites inclusivos e exclusivos",
     "Não deixar fronteiras ambíguas",
     "Fronteira clara e não contraditória"),
    ("R1.2.2-B", "GESTÃO_CONTORNO", "1.2.2", "LOGOS",
     "Controlar interações através do limite",
     "Definir pontos de entrada e saída",
     "Não permitir violações do contorno",
     "Todas as interações respeitam o limite"),
    ("R1.2.2-C", "EXPANSÃO_CONTORNO", "1.2.2", "LOGOS",
     "Ampliar ou reduzir limites existentes",
     "Redefinir fronteiras mantendo coerência",
     "Não contradizer limites anteriores",
     "Novo contorno consistente com o anterior"),

    # PACTO - 1.2.3
    ("R1.2.3-A", "ESTABELECIMENTO_PACTO", "1.2.3", "LOGOS",
     "Criar acordo entre partes",
     "Definir termos, obrigações e consequências",
     "Não omitir cláusulas essenciais",
     "Acordo explícito e mutuamente aceito"),
    ("R1.2.3-B", "CUMPRIMENTO_PACTO", "1.2.3", "LOGOS",
     "Verificar execução do acordo",
     "Avaliar conformidade com os termos",
     "Não considerar cumprimento parcial",
     "100% dos termos satisfeitos"),
    ("R1.2.3-C", "RESOLUÇÃO_VIOLAÇÃO", "1.2.3", "LOGOS",
     "Tratar quebra de acordo",
     "Aplicar consequências previstas",
     "Não criar penalidades novas",
     "Violação tratada conforme pacto"),

    # ESTATICA - 1.3.1
    ("R1.3.1-A", "ANÁLISE_ESTATICA", "1.3.1", "LOGOS",
     "Sistema em equilíbrio sem movimento",
     "Identificar forças atuantes e seus vetores",
     "Ignorar forças dinâmicas",
     "Soma dos vetores resulta em zero"),
    ("R1.3.1-B", "EQUILÍBRIO_FORÇAS", "1.3.1", "LOGOS",
     "Distribuir tensões em estrutura",
     "Calcular pontos de apoio e cargas",
     "Não exceder limites materiais",
     "Estabilidade estrutural garantida"),
    ("R1.3.1-C", "REPOUSO_RELATIVO", "1.3.1", "LOGOS",
     "Sistema aparentemente imóvel",
     "Verificar ausência de movimento neto",
     "Não confundir com movimento cíclico",
     "Sem deslocamento macroscópico"),

    # DINAMICA - 1.3.2
    ("R1.3.2-A", "ANÁLISE_DINÂMICA", "1.3.2", "LOGOS",
     "Sistema em movimento ou transição",
     "Modelar forças e acelerações",
     "Ignorar efeitos não relevantes",
     "Equações de movimento resolvidas"),
    ("R1.3.2-B", "TRANSFORMAÇÃO_ESTADOS", "1.3.2", "LOGOS",
     "Mudança de condição ou fase",
     "Identificar pontos de transição",
     "Não forçar transições contínuas",
     "Transição clara entre estados"),
    ("R1.3.2-C", "ENERGIA_CINÉTICA", "1.3.2", "LOGOS",
     "Energia associada ao movimento",
     "Calcular energia cinética e trabalho",
     "Não incluir energia potencial",
     "Conservação da energia verificada"),

    # TERMOTRANSDINÂMICA - 1.3.3
    ("R1.3.3-A", "BALANÇO_ENERGIA", "1.3.3", "LOGOS",
     "Sistema trocando energia",
     "Contabilizar entradas e saídas",
     "Não criar nem destruir energia",
     "Energia total conservada"),
    ("R1.3.3-B", "EFICIÊNCIA_TERMODINÂMICA", "1.3.3", "LOGOS",
     "Avaliar eficiência de conversão",
     "Calcular razão entre útil e total",
     "Não exceder limites teóricos",
     "Eficiência dentro dos limites possíveis"),
    ("R1.3.3-C", "ENTROPIA_PROCESSO", "1.3.3", "LOGOS",
     "Medir desordem do sistema",
     "Calcular variação de entropia",
     "Não violar segunda lei",
     "Entropia não diminui globalmente"),

    # MORADA - 2.1.1
    ("B2.1.1-A", "PROTEÇÃO_FÍSICA", "2.1.1", "BIOS",
     "Abrigo exposto a elementos adversos",
     "Estabelecer barreiras estruturais",
     "Não isolar completamente",
     "Ambiente interno mantém condições ideais"),
    ("B2.1.1-B", "RECURSOS_ESSENCIAIS", "2.1.1", "BIOS",
     "Morada sem provisão básica",
     "Estocar água, alimento, energia",
     "Não exceder capacidade de armazenamento",
     "Sobrevivência garantida por período crítico"),
    ("B2.1.1-C", "SANEAMENTO", "2.1.1", "BIOS",
     "Ambiente com risco de contaminação",
     "Implementar limpeza e descarte adequado",
     "Solução deve ser sustentável",
     "Níveis de higiene dentro de padrões seguros"),

    # TERRITORIO - 2.1.2
    ("B2.1.2-A", "REIVINDICAÇÃO_ESPACIAL", "2.1.2", "BIOS",
     "Definir área de domínio",
     "Estabelecer fronteiras geográficas",
     "Não invadir território alheio",
     "Limites territoriais claramente definidos"),
    ("B2.1.2-B", "DEFESA_TERRITORIAL", "2.1.2", "BIOS",
     "Proteger espaço contra intrusão",
     "Implementar sistemas de vigilância",
     "Não usar força excessiva",
     "Território mantido sob controle"),
    ("B2.1.2-C", "GESTÃO_RECURSOS_TERRITORIAIS", "2.1.2", "BIOS",
     "Administrar recursos do espaço",
     "Distribuir uso de forma sustentável",
     "Não esgotar recursos localmente",
     "Uso equilibrado do território"),

    # PROVISAO - 2.1.3
    ("B2.1.3-A", "ARMAZENAMENTO_RECURSOS", "2.1.3", "BIOS",
     "Necessidade de reserva de materiais",
     "Estocar provisões para período crítico",
     "Não acumular além da capacidade",
     "Recursos armazenados de forma segura"),
    ("B2.1.3-B", "ROTAÇÃO_ESTOQUE", "2.1.3", "BIOS",
     "Gerenciar validade de provisões",
     "Usar sistema FIFO (primeiro a entrar, primeiro a sair)",
     "Não deixar recursos estragarem",
     "Estoque sempre atualizado e utilizável"),
    ("B2.1.3-C", "DISTRIBUIÇÃO_RECURSOS", "2.1.3", "BIOS",
     "Alocar provisões onde necessário",
     "Priorizar necessidades críticas",
     "Não desperdiçar recursos",
     "Distribuição eficiente e equitativa"),

    # INTEGRIDADE - 2.2.1
    ("B2.2.1-A", "MANUTENÇÃO_ESTRUTURAL", "2.2.1", "BIOS",
     "Veículo material precisando de reparo",
     "Realizar manutenção preventiva e corretiva",
     "Não adiar reparos críticos",
     "Integridade estrutural preservada"),
    ("B2.2.1-B", "AVALIAÇÃO_CONDIÇÃO", "2.2.1", "BIOS",
     "Verificar estado do veículo",
     "Inspecionar componentes regularmente",
     "Não ignorar sinais de degradação",
     "Condição avaliada e documentada"),
    ("B2.2.1-C", "ATUALIZAÇÃO_SISTEMA", "2.2.1", "BIOS",
     "Melhorar ou modernizar estrutura",
     "Implementar upgrades necessários",
     "Não alterar funcionalidade essencial",
     "Sistema atualizado mantendo integridade"),

    # VITALIDADE - 2.2.2
    ("B2.2.2-A", "ENERGIA_VITAL", "2.2.2", "BIOS",
     "Veículo precisando de energia",
     "Fornecer energia necessária para operação",
     "Não exceder capacidade de carga",
     "Energia vital mantida em níveis adequados"),
    ("B2.2.2-B", "AUTORREPARAÇÃO", "2.2.2", "BIOS",
     "Sistema com capacidade de cura",
     "Ativar mecanismos de autorreparação",
     "Não forçar recuperação além do limite",
     "Sistema recupera funcionalidade gradualmente"),
    ("B2.2.2-C", "RESILIÊNCIA", "2.2.2", "BIOS",
     "Sistema sob estresse ou dano",
     "Manter funcionalidade essencial",
     "Não colapsar sob pressão",
     "Sistema resiste e recupera"),

    # HOMEOSTASE - 2.2.3
    ("B2.2.3-A", "REGULAÇÃO_INTERNA", "2.2.3", "BIOS",
     "Sistema precisando manter equilíbrio",
     "Ajustar parâmetros internos",
     "Não permitir flutuações extremas",
     "Variáveis mantidas dentro da faixa ideal"),
    ("B2.2.3-B", "FEEDBACK_NEGATIVO", "2.2.3", "BIOS",
     "Desvio detectado no sistema",
     "Aplicar correção proporcional",
     "Não criar oscilações",
     "Sistema retorna ao equilíbrio"),
    ("B2.2.3-C", "ADAPTAÇÃO_CICLICA", "2.2.3", "BIOS",
     "Sistema sujeito a ciclos naturais",
     "Ajustar comportamento ritmicamente",
     "Não forçar padrão constante",
     "Sistema adapta-se aos ciclos"),

    # ANABOLISMO - 2.3.1
    ("B2.3.1-A", "SÍNTESE_MATERIAL", "2.3.1", "BIOS",
     "Construir estruturas complexas",
     "Combinar componentes simples",
     "Não pular etapas necessárias",
     "Estrutura complexa formada corretamente"),
    ("B2.3.1-B", "CRESCIMENTO", "2.3.1", "BIOS",
     "Sistema aumentando de tamanho",
     "Adicionar material de forma ordenada",
     "Não crescer desordenadamente",
     "Crescimento estruturado e funcional"),
    ("B2.3.1-C", "COMPLEXIFICAÇÃO", "2.3.1", "BIOS",
     "Tornar sistema mais complexo",
     "Adicionar funcionalidades gradativamente",
     "Não adicionar complexidade desnecessária",
     "Complexidade útil e funcional"),

    # CATABOLISMO - 2.3.2
    ("B2.3.2-A", "DECOMPOSIÇÃO_MATERIAL", "2.3.2", "BIOS",
     "Quebrar estruturas complexas",
     "Separar em componentes simples",
     "Não destruir funcionalidade essencial",
     "Componentes úteis recuperados"),
    ("B2.3.2-B", "LIBERAÇÃO_ENERGIA", "2.3.2", "BIOS",
     "Liberar energia armazenada",
     "Quebrar ligações químicas",
     "Não desperdiçar energia",
     "Energia liberada utilizada eficientemente"),
    ("B2.3.2-C", "REMOÇÃO_DESEJOS", "2.3.2", "BIOS",
     "Eliminar componentes não mais úteis",
     "Degradar e remover material",
     "Não afetar componentes saudáveis",
     "Material removido de forma segura"),

    # CICLO - 2.3.3
    ("B2.3.3-A", "RECIRCULAÇÃO_MATERIAL", "2.3.3", "BIOS",
     "Material precisando ser reutilizado",
     "Reintegrar no ciclo produtivo",
     "Não acumular material residual",
     "Material reciclado eficientemente"),
    ("B2.3.3-B", "RENOVAÇÃO_CONTÍNUA", "2.3.3", "BIOS",
     "Sistema renovando-se constantemente",
     "Substituir componentes periodicamente",
     "Não interromper funcionalidade",
     "Renovação mantém sistema operante"),
    ("B2.3.3-C", "FLUXO_PERENE", "2.3.3", "BIOS",
     "Energia e matéria circulando",
     "Manter fluxos contínuos",
     "Não permitir estagnação",
     "Fluxo constante e equilibrado"),

    # VALORES - 3.1.1
    ("P3.1.1-A", "ALINHAMENTO_VALORES", "3.1.1", "PATHOS",
     "Decisão com múltiplas opções",
     "Avaliar contra valores centrais",
     "Não flexibilizar valores por conveniência",
     "Decisão maximiza coerência valor-ação"),
    ("P3.1.1-B", "CONFLITO_VALORES", "3.1.1", "PATHOS",
     "Dois ou mais valores em tensão",
     "Hierarquizar e buscar síntese",
     "Não suprimir valor permanentemente",
     "Solução preserva essência de ambos"),
    ("P3.1.1-C", "TRANSPARÊNCIA", "3.1.1", "PATHOS",
     "Decisão afeta múltiplos stakeholders",
     "Comunicar valores que orientaram escolha",
     "Não ocultar motivações",
     "Stakeholders compreendem racional"),

    # VIRTUDE - 3.1.2
    ("P3.1.2-A", "EXCELÊNCIA_MORAL", "3.1.2", "PATHOS",
     "Buscar melhor prática ética",
     "Praticar virtude consistentemente",
     "Não ceder a tentações",
     "Ação reflete virtude"),
    ("P3.1.2-B", "CARÁTER", "3.1.2", "PATHOS",
     "Desenvolver firmeza moral",
     "Praticar hábitos virtuosos",
     "Não agir por impulso",
     "Caráter fortalecido"),
    ("P3.1.2-C", "INTEGRIDADE", "3.1.2", "PATHOS",
     "Manter consistência interna",
     "Alinhar pensamento e ação",
     "Não contradizer princípios",
     "Integridade preservada"),

    # RESPONSABILIDADE - 3.1.3
    ("P3.1.3-A", "DEVER", "3.1.3", "PATHOS",
     "Cumprir obrigação moral",
     "Agir conforme dever",
     "Não negligenciar responsabilidade",
     "Dever cumprido"),
    ("P3.1.3-B", "CONSEQUÊNCIA", "3.1.3", "PATHOS",
     "Avaliar impacto das ações",
     "Antecipar resultados",
     "Não ignorar efeitos colaterais",
     "Consequências consideradas"),
    ("P3.1.3-C", "ESCOLHA", "3.1.3", "PATHOS",
     "Decidir entre alternativas",
     "Ponderar valores em conflito",
     "Não decidir precipitadamente",
     "Escolha alinhada com valores"),

    # RECONHECIMENTO - 3.2.1
    ("P3.2.1-A", "VALIDAÇÃO_EXISTÊNCIA", "3.2.1", "PATHOS",
     "Outro precisa ser reconhecido",
     "Validar dignidade e existência",
     "Não negar humanidade",
     "Outro reconhecido plenamente"),
    ("P3.2.1-B", "DIGNIDADE", "3.2.1", "PATHOS",
     "Tratar com respeito fundamental",
     "Honrar valor intrínseco",
     "Não desumanizar",
     "Dignidade preservada"),
    ("P3.2.1-C", "EXISTÊNCIA", "3.2.1", "PATHOS",
     "Confirmar presença do outro",
     "Reconhecer como agente",
     "Não objetificar",
     "Existência validada"),

    # EMPATIA - 3.2.2
    ("P3.2.2-A", "COMPREENSÃO_PROFUNDA", "3.2.2", "PATHOS",
     "Entender sentimento alheio",
     "Colocar-se no lugar do outro",
     "Não projetar próprias emoções",
     "Sentimento compreendido"),
    ("P3.2.2-B", "PONTE", "3.2.2", "PATHOS",
     "Conectar através do sentido",
     "Estabelecer vínculo emocional",
     "Não manter distância",
     "Conexão estabelecida"),
    ("P3.2.2-C", "SENTIDO", "3.2.2", "PATHOS",
     "Compartilhar significado",
     "Trocar experiências subjetivas",
     "Não monopolizar narrativa",
     "Sentido compartilhado"),

    # DIALOGO - 3.2.3
    ("P3.2.3-A", "TROCA_MÚTUA", "3.2.3", "PATHOS",
     "Construir entendimento conjunto",
     "Ouvir e expressar",
     "Não imposição unilateral",
     "Construção colaborativa"),
    ("P3.2.3-B", "CONSTRUÇÃO_CONJUNTA", "3.2.3", "PATHOS",
     "Criar significado juntos",
     "Co-criar entendimento",
     "Não ditador da verdade",
     "Verdade co-construída"),
    ("P3.2.3-C", "REVELAÇÃO", "3.2.3", "PATHOS",
     "Desvelar sentido oculto",
     "Descobrir através do diálogo",
     "Não forçar conclusão",
     "Sentido emerge naturalmente"),

    # HARMONIA - 3.3.1
    ("P3.3.1-A", "PROPORÇÃO_AUREA", "3.3.1", "PATHOS",
     "Divisão harmônica de espaço/tempo",
     "Aplicar razão 1:1.618",
     "Não forçar onde prejudica",
     "Distribuição percebida como equilibrada"),
    ("P3.3.1-B", "EQUILÍBRIO_ESTÉTICO", "3.3.1", "PATHOS",
     "Alcançar harmonia visual",
     "Balancear elementos",
     "Não desequilibrar composição",
     "Harmonia visual alcançada"),
    ("P3.3.1-C", "RESSONÂNCIA", "3.3.1", "PATHOS",
     "Criar vibração harmoniosa",
     "Ajustar frequências",
     "Não causar dissonância",
     "Ressonância positiva gerada"),

    # EXPRESSAO - 3.3.2
    ("P3.3.2-A", "FORMA_CORPO", "3.3.2", "PATHOS",
     "Dar forma ao sentido",
     "Materializar conteúdo",
     "Não deformar essência",
     "Forma expressa conteúdo fielmente"),
    ("P3.3.2-B", "EXTERIORIZAÇÃO", "3.3.2", "PATHOS",
     "Tornar interno externo",
     "Manifestar conteúdo",
     "Não reprimir expressão",
     "Conteúdo exteriorizado"),
    ("P3.3.2-C", "LINGUAGEM_ESTÉTICA", "3.3.2", "PATHOS",
     "Comunicar através da forma",
     "Usar recursos estéticos",
     "Não usar linguagem pobre",
     "Comunicação estética eficaz"),

    # IMPACTO - 3.3.3
    ("P3.3.3-A", "TRANSFORMAÇÃO", "3.3.3", "PATHOS",
     "Alterar estado emocional",
     "Provocar mudança interior",
     "Não forçar transformação",
     "Transformação ocorre organicamente"),
    ("P3.3.3-B", "EMOCIONAL", "3.3.3", "PATHOS",
     "Afetar sentimentos",
     "Tocar sensibilidade",
     "Não manipular emoções",
     "Resposta emocional autêntica"),
    ("P3.3.3-C", "LIBERDADE", "3.3.3", "PATHOS",
     "Respeitar autonomia",
     "Permitir escolha",
     "Não coagir",
     "Transformação sem violação"),

    # DEGRADAÇÃO - 4.1.1
    ("K4.1.1-A", "ENTROPIA_SISTEMA", "4.1.1", "KHAOS",
     "Sistema complexo mostrando fadiga",
     "Identificar fontes de desordem",
     "Não tentar reverter entropia total",
     "Taxa de entropia dentro dos limites"),
    ("K4.1.1-B", "DESTRUIÇÃO_CRIATIVA", "4.1.1", "KHAOS",
     "Estrutura obsoleta impedindo evolução",
     "Desmantelar componentes não funcionais",
     "Preservar elementos úteis",
     "Espaço liberado para novas configurações"),
    ("K4.1.1-C", "RECICLAGEM", "4.1.1", "KHAOS",
     "Recursos descartados disponíveis",
     "Reintegrar em novos ciclos",
     "Energia de reciclagem não deve superar benefício",
     "Material recuperado ≥ 70%"),

    # DISSIPAÇÃO - 4.1.2
    ("K4.1.2-A", "DISPERSÃO_ENERGIA", "4.1.2", "KHAOS",
     "Energia dissipando no meio",
     "Redistribuir sem destruir",
     "Não concentrar artificialmente",
     "Quantidade total conservada"),
    ("K4.1.2-B", "ENTROPIA_AUMENTADA", "4.1.2", "KHAOS",
     "Desordem aumentando naturalmente",
     "Permitir processo espontâneo",
     "Não forçar ordem artificial",
     "Desordem dentro dos limites naturais"),
    ("K4.1.2-C", "RETORNO_AMORFO", "4.1.2", "KHAOS",
     "Retornar ao estado potencial",
     "Permitir dissolução estrutural",
     "Não manter estrutura artificialmente",
     "Estado amorfo alcançado"),

    # CAOS - 4.1.3
    ("K4.1.3-A", "ALEATORIEDADE", "4.1.3", "KHAOS",
     "Comportamento imprevisível",
     "Aceitar incerteza inerente",
     "Não tentar controlar tudo",
     "Padrões emergem do caos"),
    ("K4.1.3-B", "COMPLEXIDADE_CAÓTICA", "4.1.3", "KHAOS",
     "Sistema altamente sensível",
     "Reconhecer dependência inicial",
     "Não prever a longo prazo",
     "Comportamento compreendido"),
    ("K4.1.3-C", "PADRÕES_EMERGENTES", "4.1.3", "KHAOS",
     "Ordem surgindo do desordem",
     "Identificar estruturas ocultas",
     "Não impor ordem externa",
     "Padrões reconhecidos"),

    # EXCEPCAO - 4.2.1
    ("K4.2.1-A", "PONTO_EXCEPCIONAL", "4.2.1", "KHAOS",
     "Regras comuns não se aplicam",
     "Reconhecer exceção",
     "Não forçar regras normais",
     "Exceção compreendida"),
    ("K4.2.1-B", "LEI_SUPERIOR", "4.2.1", "KHAOS",
     "Ordem transcendente operando",
     "Aplicar princípios superiores",
     "Não reduzir ao ordinário",
     "Ordem superior reconhecida"),
    ("K4.2.1-C", "TRANSFORMAÇÃO_EXCEPCIONAL", "4.2.1", "KHAOS",
     "Mudança radical de paradigma",
     "Aceitar nova ordem",
     "Não resistir à transformação",
     "Novo paradigma estabelecido"),

    # INFINITO - 4.2.2
    ("K4.2.2-A", "HORIZONTE_INATINGÍVEL", "4.2.2", "KHAOS",
     "Limite que recua ao ser abordado",
     "Reconhecer infinitude",
     "Não tentar alcançar o inalcançável",
     "Infinitude aceita"),
    ("K4.2.2-B", "POTENCIAL_INFINITO", "4.2.2", "KHAOS",
     "Possibilidades sem limite",
     "Abrir-se ao potencial",
     "Não restringir artificialmente",
     "Potencial reconhecido"),
    ("K4.2.2-C", "EXPANSÃO_CONTÍNUA", "4.2.2", "KHAOS",
     "Crescimento sem fronteira",
     "Permitir expansão indefinida",
     "Não impor limites arbitrários",
     "Expansão contínua permitida"),

    # TRANSFORMAÇÃO - 4.2.3
    ("K4.2.3-A", "MORTE_E_RENASCIMENTO", "4.2.3", "KHAOS",
     "Fim do estado atual",
     "Aceitar morte do velho",
     "Não resistir à transformação",
     "Novo estado emerge"),
    ("K4.2.3-B", "MUDANÇA_RADICAL", "4.2.3", "KHAOS",
     "Alteração fundamental",
     "Abraçar transformação total",
     "Não buscar meios-termos",
     "Mudança completa realizada"),
    ("K4.2.3-C", "NOVA_ORDEM", "4.2.3", "KHAOS",
     "Estabelecer novo paradigma",
     "Construir sobre as ruínas",
     "Não negar o que passou",
     "Nova ordem consolidada"),

    # FUSÃO - 4.3.1
    ("K4.3.1-A", "UNIÃO_ELEMENTOS", "4.3.1", "KHAOS",
     "Combinar elementos distintos",
     "Criar nova entidade",
     "Não perder propriedades originais",
     "Fusão bem-sucedida"),
    ("K4.3.1-B", "SÍNTESE_CRIATIVA", "4.3.1", "KHAOS",
     "Criar algo inédito",
     "Transcender os originais",
     "Não ser mera soma",
     "Nova propriedade emergente"),
    ("K4.3.1-C", "TRANSCENDÊNCIA", "4.3.1", "KHAOS",
     "Ir além dos limites",
     "Superar oposições",
     "Não ficar no nível anterior",
     "Transcendência alcançada"),

    # HIBRIDISMO - 4.3.2
    ("K4.3.2-A", "MISTURA_PRESERVAÇÃO", "4.3.2", "KHAOS",
     "Combinar mantendo originais",
     "Preservar características",
     "Não diluir identidades",
     "Híbrido reconhecível"),
    ("K4.3.2-B", "PONTE_TEMPORAL", "4.3.2", "KHAOS",
     "Conectar passado e futuro",
     "Ser transição viva",
     "Não ser mero produto",
     "Híbrido como processo"),
    ("K4.3.2-C", "IDENTIDADE_HÍBRIDA", "4.3.2", "KHAOS",
     "Criar nova identidade",
     "Ser mais que a soma",
     "Não ser ambíguo",
     "Identidade clara"),

    # TRANSCENDENCIA - 4.3.3
    ("K4.3.3-A", "SUPERAÇÃO", "4.3.3", "KHAOS",
     "Ir além dos limites atuais",
     "Elevar a novos patamares",
     "Não contentar-se com o atual",
     "Superação realizada"),
    ("K4.3.3-B", "INCLUSÃO", "4.3.3", "KHAOS",
     "Abranger sem excluir",
     "Integrar oposições",
     "Não suprimir diferenças",
     "Inclusão harmoniosa"),
    ("K4.3.3-C", "NÍVEL_NOVO", "4.3.3", "KHAOS",
     "Alcançar novo estágio",
     "Operar em nova dimensão",
     "Não ser mais do mesmo",
     "Novo nível consolidado"),

    # PROPORÇÃO - 5.1.1
    ("A5.1.1-A", "ESCALAMENTO", "5.1.1", "APEIRON",
     "Sistema em escala diferente",
     "Identificar leis escalares",
     "Não assumir linearidade",
     "Comportamento consistente"),
    ("A5.1.1-B", "PROPORÇÃO_AUREA", "5.1.1", "APEIRON",
     "Divisão harmônica necessária",
     "Aplicar razão áurea",
     "Não forçar funcionalidade",
     "Equilíbrio percebido"),
    ("A5.1.1-C", "ISOMORFISMO", "5.1.1", "APEIRON",
     "Problema sem solução evidente",
     "Mapear para outra escala",
     "Preservar relações essenciais",
     "Solução válida na escala original"),

    # MAGNITUDE - 5.1.2
    ("A5.1.2-A", "TAMANHO_NATUREZA", "5.1.2", "APEIRON",
     "Magnitude alterando propriedades",
     "Reconhecer efeitos escalares",
     "Não ignorar mudanças qualitativas",
     "Natureza da lei compreendida"),
    ("A5.1.2-B", "EXPERIÊNCIA_ESCALAR", "5.1.2", "APEIRON",
     "Tamanho afetando percepção",
     "Ajustar expectativas",
     "Não projetar pequena escala",
     "Experiência adequada"),
    ("A5.1.2-C", "LEI_ESCALAR", "5.1.2", "APEIRON",
     "Lei variando com magnitude",
     "Calcular efeitos escalares",
     "Não aplicar lei universalmente",
     "Lei escalada corretamente"),

    # LEI - 5.1.3
    ("A5.1.3-A", "LEI_RELATIVA", "5.1.3", "APEIRON",
     "Lei dependendo da escala",
     "Determinar domínio de validade",
     "Não extrapolar erroneamente",
     "Aplicação correta"),
    ("A5.1.3-B", "MANIFESTAÇÃO_LEI", "5.1.3", "APEIRON",
     "Lei se apresentando concretamente",
     "Observar efeitos práticos",
     "Não confiar apenas em teoria",
     "Manifestação verificada"),
    ("A5.1.3-C", "ESCALA_APLICAÇÃO", "5.1.3", "APEIRON",
     "Determinar escala de validade",
     "Mapear fronteiras da lei",
     "Não ignorar limites",
     "Escala claramente definida"),

    # FREQUENCIA - 5.2.1
    ("A5.2.1-A", "CICLO_TEMPORAL", "5.2.1", "APEIRON",
     "Frequência determinando caráter",
     "Identificar padrão cíclico",
     "Não ignorar periodicidade",
     "Cadência reconhecida"),
    ("A5.2.1-B", "RESONÂNCIA_FREQUÊNCIA", "5.2.1", "APEIRON",
     "Sintonizar com frequência",
     "Ajustar para sincronia",
     "Não causar dissonância",
     "Ressonância alcançada"),
    ("A5.2.1-C", "IDENTIDADE_FREQUÊNCIA", "5.2.1", "APEIRON",
     "Frequência como assinatura",
     "Reconhecer padrão único",
     "Não confundir com ruído",
     "Identidade estabelecida"),

    # RESONÂNCIA - 5.2.2
    ("A5.2.2-A", "AMPLIFICAÇÃO", "5.2.2", "APEIRON",
     "Sincronia aumentando efeito",
     "Ajustar para ressonância",
     "Não causar interferência",
     "Amplificação positiva"),
    ("A5.2.2-B", "SINCRONIA", "5.2.2", "APEIRON",
     "Elementos em fase",
     "Alinhar frequências",
     "Não forçar sincronia",
     "Sincronia natural"),
    ("A5.2.2-C", "MULTIPLICAÇÃO", "5.2.2", "APEIRON",
     "Efeito sem adição de matéria",
     "Aproveitar ressonância",
     "Não desperdiçar energia",
     "Multiplicação eficiente"),

    # ONDA - 5.2.3
    ("A5.2.3-A", "PROPAGAÇÃO", "5.2.3", "APEIRON",
     "Padrão se movendo no meio",
     "Identificar direção e velocidade",
     "Não interromper desnecessariamente",
     "Propagação compreendida"),
    ("A5.2.3-B", "POTENCIAL_ATUAL", "5.2.3", "APEIRON",
     "Onda como potência se tornando real",
     "Reconhecer processo de manifestação",
     "Não negar potencial",
     "Transição compreendida"),
    ("A5.2.3-C", "PADRÃO_ONDA", "5.2.3", "APEIRON",
     "Identificar características da onda",
     "Mapear amplitude e frequência",
     "Não simplificar demais",
     "Padrão reconhecido"),

    # POTENCIAL - 5.3.1
    ("A5.3.1-A", "CAPACIDADE_LATENTE", "5.3.1", "APEIRON",
     "Potencial não manifestado",
     "Reconhecer possibilidade",
     "Não forçar manifestação",
     "Potencial preservado"),
    ("A5.3.1-B", "AVESSO_MANIFESTO", "5.3.1", "APEIRON",
     "Potencial como oposto do atual",
     "Compreender dualidade",
     "Não negar não-manifesto",
     "Dualidade reconhecida"),
    ("A5.3.1-C", "CAMPO_POTENCIAL", "5.3.1", "APEIRON",
     "Matriz de possibilidades",
     "Mapear estados potenciais",
     "Não limitar possibilidades",
     "Campo reconhecido"),

    # SILÊNCIO - 5.3.2
    ("A5.3.2-A", "AUSÊNCIA_MANIFESTAÇÃO", "5.3.2", "APEIRON",
     "Não-manifesto como linguagem",
     "Respeitar silêncio",
     "Não preencher desnecessariamente",
     "Silêncio compreendido"),
    ("A5.3.2-B", "LINGUAGEM_NÃO_MANIFESTO", "5.3.2", "APEIRON",
     "O não-dito como comunicação",
     "Ouvir o implícito",
     "Não ignorar subtexto",
     "Mensagem implícita captada"),
    ("A5.3.2-C", "PRESENÇA_ausência", "5.3.2", "APEIRON",
     "Ausência como presença ativa",
     "Reconhecer poder do vazio",
     "Não temer o não-manifesto",
     "Ausência compreendida"),

    # CAMPO - 5.3.3
    ("A5.3.3-A", "MATRIZ_POSSIBILIDADES", "5.3.3", "APEIRON",
     "Campo unificando possibilidades",
     "Reconhecer interconexão",
     "Não fragmentar o campo",
     "Unidade do campo preservada"),
    ("A5.3.3-B", "REPOUSO_POTENCIAL", "5.3.3", "APEIRON",
     "Possibilidades em estado latente",
     "Respeitar repouso",
     "Não perturbar desnecessariamente",
     "Repouso mantido"),
    ("A5.3.3-C", "UNIFICACAO_CAMPO", "5.3.3", "APEIRON",
     "Campo como princípio unificador",
     "Reconhecer totalidade",
     "Não dualizar artificialmente",
     "Unidade reconhecida"),

    # PADRAO_PRIMORDIAL - 6.1.1
    ("M6.1.1-A", "RECONHECIMENTO_ARQUETÍPICO", "6.1.1", "MYTHOS",
     "Padrão recorrente em comportamento",
     "Mapear para arquétipo universal",
     "Não reduzir a estereótipo",
     "Arquétipo esclarece dinâmica"),
    ("M6.1.1-B", "ATIVAÇÃO_SIMPOLAR", "6.1.1", "MYTHOS",
     "Arquétipo adormecido",
     "Evocar arquétipo latente",
     "Não forçar integração abrupta",
     "Arquétipo emerge organicamente"),
    ("M6.1.1-C", "SÍNTESE_OPOSTOS", "6.1.1", "MYTHOS",
     "Tensão entre arquétipos",
     "Encontrar terceira via",
     "Não suprimir nenhum arquétipo",
     "Síntese transcende oposição"),

    # COMPORTAMENTO - 6.1.2
    ("M6.1.2-A", "ROTEIRO_INVISIBLE", "6.1.2", "MYTHOS",
     "Arquétipo guiando ação",
     "Reconhecer roteiro oculto",
     "Não negar influência arquetípica",
     "Roteiro reconhecido"),
    ("M6.1.2-B", "PADRÃO_COMPORTAMENTAL", "6.1.2", "MYTHOS",
     "Comportamento repetitivo",
     "Identificar arquétipo subjacente",
     "Não julgar o padrão",
     "Padrão compreendido"),
    ("M6.1.2-C", "INFLUÊNCIA_ARQUETÍPICA", "6.1.2", "MYTHOS",
     "Arquétipo moldando escolhas",
     "Conscientizar influência",
     "Não ser controlado cegamente",
     "Influência integrada"),

    # SIMBOLO - 6.1.3
    ("M6.1.3-A", "PONTE_SENSÍVEL", "6.1.3", "MYTHOS",
     "Símbolo apontando para transcendente",
     "Reconhecer ponte simbólica",
     "Não reduzir a literalidade",
     "Transcendência acessada"),
    ("M6.1.3-B", "LINGUAGEM_SENSÍVEL", "6.1.3", "MYTHOS",
     "Símbolo como linguagem",
     "Decodificar mensagem",
     "Não ignorar linguagem simbólica",
     "Mensagem simbólica compreendida"),
    ("M6.1.3-C", "ARQUÉTIPO_EM_FORMA", "6.1.3", "MYTHOS",
     "Arquétipo tomando forma sensível",
     "Reconhecer manifestação",
     "Não negar realidade simbólica",
     "Manifestação reconhecida"),

    # TEIA - 6.2.1
    ("M6.2.1-A", "TEIA_CONEXÕES", "6.2.1", "MYTHOS",
     "Eventos conectados em rede",
     "Mapear conexões significativas",
     "Não isolar eventos",
     "Teia reconhecida"),
    ("M6.2.1-B", "TECIDO_SENTIDO", "6.2.1", "MYTHOS",
     "Sentido tramado na teia",
     "Reconhecer trama",
     "Não rasgar o tecido",
     "Trama compreendida"),
    ("M6.2.1-C", "COMPLEXIDADE_TEIA", "6.2.1", "MYTHOS",
     "Rede complexa de conexões",
     "Aceitar complexidade",
     "Não simplificar artificialmente",
     "Complexidade respeitada"),

    # LINHA_SENTIDO - 6.2.2
    ("M6.2.2-A", "TEMPO_IDENTIDADE", "6.2.2", "MYTHOS",
     "Linha temporal tecendo identidade",
     "Reconhecer continuidade",
     "Não fragmentar narrativa",
     "Identidade temporal reconhecida"),
    ("M6.2.2-B", "NARRATIVA_VIDA", "6.2.2", "MYTHOS",
     "História como tecido da existência",
     "Reconhecer poder da narrativa",
     "Não negar história",
     "Narrativa integrada"),
    ("M6.2.2-C", "SENTIDO_TEMPORAL", "6.2.2", "MYTHOS",
     "Sentido emergindo no tempo",
     "Respeitar processo temporal",
     "Não forçar conclusão prematura",
     "Sentido temporal reconhecido"),

    # HISTÓRIA_VIVIDA - 6.2.3
    ("M6.2.3-A", "EXPERIÊNCIA_NARRATIVA", "6.2.3", "MYTHOS",
     "Viver como narrativa contínua",
     "Reconhecer si mesmo como história",
     "Não objetificar experiência",
     "Narrativa vivida compreendida"),
    ("M6.2.3-B", "CONTINUIDADE_EXPERIÊNCIA", "6.2.3", "MYTHOS",
     "Experiência como fluxo contínuo",
     "Respeitar continuidade",
     "Não fragmentar experiência",
     "Continuidade reconhecida"),
    ("M6.2.3-C", "NARRATIVA_ATIVA", "6.2.3", "MYTHOS",
     "Narrativa como ação viva",
     "Reconhecer poder criadora",
     "Não ser mero espectador",
     "Narrativa ativa reconhecida"),

    # INCOMPREENSÃO - 6.3.1
    ("M6.3.1-A", "LIMITE_ANALÍTICO", "6.3.1", "MYTHOS",
     "Conhecimento analítico insuficiente",
     "Reconhecer limite da razão",
     "Não forçar compreensão",
     "Limite aceito"),
    ("M6.3.1-B", "PROTEÇÃO_MISTÉRIO", "6.3.1", "MYTHOS",
     "Mistério protegendo profundidade",
     "Respeitar o não-sabido",
     "Não violar mistério",
     "Mistério preservado"),
    ("M6.3.1-C", "HUMILDADE_CONHECIMENTO", "6.3.1", "MYTHOS",
     "Reconhecer ignorância",
     "Aceitar não-saber",
     "Não fingir conhecimento",
     "Humildade epistêmica"),

    # INTUIÇÃO - 6.3.2
    ("M6.3.2-A", "CONHECIMENTO_DIRETO", "6.3.2", "MYTHOS",
     "Saber sem mediação racional",
     "Confiar na intuição",
     "Não negar conhecimento direto",
     "Intuição reconhecida"),
    ("M6.3.2-B", "TOCAR_PROFUNDIDADE", "6.3.2", "MYTHOS",
     "Intuição alcançando o profundo",
     "Permitir penetração",
     "Não manter distância",
     "Profundidade tocada"),
    ("M6.3.2-C", "SABER_IMEDIATO", "6.3.2", "MYTHOS",
     "Conhecimento que não passa pela razão",
     "Aceitar saber imediato",
     "Não exigir prova",
     "Sabedoria intuitiva reconhecida"),

    # REVELAÇÃO - 6.3.3
    ("M6.3.3-A", "DESVELAMENTO", "6.3.3", "MYTHOS",
     "Verdade profunda se revelando",
     "Permitir desvelamento",
     "Não forçar revelação",
     "Desvelamento ocorre"),
    ("M6.3.3-B", "ILUMINAÇÃO", "6.3.3", "MYTHOS",
     "Claridade súbita iluminando",
     "Aceitar iluminação",
     "Não apagar luz",
     "Iluminação reconhecida"),
    ("M6.3.3-C", "MISTERIO_PRESERVADO", "6.3.3", "MYTHOS",
     "Revelação sem esgotar mistério",
     "Reconhecer verdade profunda",
     "Não reduzir a explicação",
     "Mistério preservado"),
]

print(f"Total de células N4 definidas: {len(celulas_n4)}")

# Agrupa por subdomínio N3
from collections import defaultdict
n3_groups = defaultdict(list)
for cell in celulas_n4:
    key = f"{cell[2]}-{cell[3]}"  # n3_ref-dominio
    n3_groups[key].append(cell)

print(f"Subdomínios N3 com células: {len(n3_groups)}")

# Para cada subdomínio N3, cria arquivo N4
for n3_key, cells in sorted(n3_groups.items()):
    n3_ref = cells[0][2]
    dominio = cells[0][3]
    n3_nome = cells[0][1].split('_')[0] if '_' in cells[0][1] else cells[0][1]
    
    # Busca nome real do N3
    n3_nome_real = n3_nome
    for cell in cells:
        if cell[1]:
            n3_nome_real = cell[1].split('_')[0] if '_' in cell[1] else cell[1]
            break
    
    # Determina N2 ID
    n2_prefix = n3_ref.split('.')[0]
    n2_id = f"{n2_prefix}.{n3_ref.split('.')[1]}"
    
    filename = os.path.join("data", "ontology", f"N4-{n3_ref.replace('.', '_')}-{dominio}-{n3_nome_real.upper()}.md")
    
    # Constrói tabela de células
    tabela_celulas = ""
    for i, cell in enumerate(cells, 1):
        tabela_celulas += f"""### {i}. {cell[1]}

- **ID:** {cell[0]}
- **Gatilho:** {cell[4]}
- **Ação:** {cell[5]}
- **Restrição:** {cell[6]}
- **Verificação:** {cell[7]}

"""
    
    content_file = f"""# N4-{n3_ref.replace('.', '_')} - {dominio} / {n3_nome_real.upper()} - Células Semânticas

---

## Metadados

- **ID N4:** {n3_ref} (agregado)
- **ID N3 Pai:** {n3_ref}
- **ID N2 Avô:** {n2_id}
- **Domínio:** {dominio}
- **Subdomínio N3:** {n3_nome_real}
- **Geometria Base:** 2×3×3×3×3
- **Total de Células:** {len(cells)}
- **Data:** 2026-05-07
- **Status:** ATIVO

---

## Sumário Executivo

Este arquivo agrega as células semânticas operacionais N4 derivadas do subdomínio N3 **{n3_nome_real}** ({dominio}), conforme mapeamento na Taxonomia Ontológica.

**Origem N3:** `N3-{n3_ref.replace('.', '_')}-{dominio}-{n3_nome_real.upper()}.md`  
**Células N4:** {len(cells)} procedimentos aplicáveis

---

## Matriz de Rastreabilidade

### Origem N3

| Elemento | Referência |
|----------|------------|
| Arquivo N3 | `N3-{n3_ref.replace('.', '_')}-{dominio}-{n3_nome_real.upper()}.md` |
| Domínio N2 | {n2_id}_{n3_nome_real} |
| Domínio N1 | {dominio} |
| Vetor N0 | {"0.1_SINTRÓPICO" if dominio in ["LOGOS", "BIOS", "PATHOS"] else "0.2_ENTRÓPICO"} |

### Relação Hierárquica

```
N0: {"SINTRÓPICO" if dominio in ["LOGOS", "BIOS", "PATHOS"] else "ENTRÓPICO"}
  └─ N1: {dominio}
      └─ N2: {n2_id}_{n3_nome_real}
          └─ N3: {n3_ref} {n3_nome_real}
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
print(f"Total de células N4 mapeadas: {len(celulas_n4)}")

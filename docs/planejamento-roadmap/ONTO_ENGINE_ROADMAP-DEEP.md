ROADMAP:
  nome: "ONTOLOGICAL COGNITIVE ENGINE"
  versao: "1.0"
  objetivo_macro: "Transformar o classificador ontológico heurístico atual em uma arquitetura cognitiva ontológica inferencial baseada em embeddings semânticos, inferência probabilística hierárquica, propagação em grafo, memória contextual e espaço cognitivo latente"

  paradigma:
    estado_atual:
      natureza: "roteador heurístico semântico"
      caracteristicas:
        - keyword_matching
        - heuristicas_estaticas
        - inferencia_parcial
        - embeddings_limitados_ao_input
        - taxonomia_simbolica
      limitacoes:
        - score_inflation
        - colisao_semantica
        - ausencia_de_calibracao
        - baixa_generalizacao
        - alta_dependencia_lexical
        - ausencia_de_contexto_continuo
        - ausencia_de_modelagem_probabilistica
        - baixa_capacidade_de_abstracao
        - sem_geometria_semantica
        - sem_memoria_adaptativa

    estado_alvo:
      natureza: "motor cognitivo ontologico inferencial"
      caracteristicas:
        - inferencia_hierarquica_probabilistica
        - embeddings_ontologicos
        - propagacao_em_grafo
        - classificacao_multiestado
        - memoria_contextual
        - aprendizado_adaptativo
        - geometria_cognitiva_latente
        - resolucao_de_ambiguidade
        - reasoning_semantico
        - navegacao_ontologica

  arquitetura_final:
    pipeline_global:
      - input_query
      - preprocessamento_semantico
      - extracao_de_features
      - embedding_da_query
      - inferencia_hierarquica
      - ativacao_ontologica
      - propagacao_em_grafo
      - resolucao_de_ambiguidade
      - calibracao_probabilistica
      - contextualizacao
      - classificacao_N0_N4
      - memoria
      - aprendizado
      - output

    componentes_macro:
      ontology_engine:
        funcao: "Representacao estrutural da ontologia fractal"
      embedding_engine:
        funcao: "Representacao vetorial semantica"
      inference_engine:
        funcao: "Inferencia probabilistica hierarquica"
      graph_engine:
        funcao: "Propagacao cognitiva e relacional"
      cognition_engine:
        funcao: "Modelagem de estados cognitivos"
      memory_engine:
        funcao: "Persistencia contextual e historica"
      calibration_engine:
        funcao: "Calibragem probabilistica e controle de entropia"
      learning_engine:
        funcao: "Aprendizado adaptativo"
      latent_space_engine:
        funcao: "Geometria cognitiva vetorial"

  fase_1_refatoracao_estrutural:
    nome: "FOUNDATION REFACTOR"
    objetivo: "Transformar scripts heurísticos acoplados em arquitetura modular extensível, observável e escalável"

    problemas_atuais:
      - excesso_de_dicts_soltos
      - baixa_rastreabilidade
      - pipeline_implicito
      - responsabilidades_misturadas
      - baixa_testabilidade
      - acoplamento_forte
      - inferencia_nao_auditavel

    entregas:
      modularizacao:
        estrutura:
          src:
            ontology:
              funcao: "Modelagem estrutural da ontologia"
            embeddings:
              funcao: "Geração e manipulação vetorial"
            classifiers:
              funcao: "Classificadores especializados"
            inference:
              funcao: "Inferencia probabilistica"
            graph:
              funcao: "Rede relacional cognitiva"
            cognition:
              funcao: "Funções cognitivas"
            scoring:
              funcao: "Calculo de scores"
            memory:
              funcao: "Contexto e persistencia"
            calibration:
              funcao: "Confidence e entropy"
            evaluation:
              funcao: "KPIs e benchmarking"
            api:
              funcao: "Exposição externa"
            pipelines:
              funcao: "Orquestracao"
            utils:
              funcao: "Ferramentas auxiliares"

      entidades_formais:
        OntologyCell:
          atributos:
            - uid
            - n0
            - n1
            - n2
            - n3
            - n4
            - embedding
            - semantic_vector
            - cognitive_functions
            - relations
            - entropy_profile
            - metadata

        Relation:
          atributos:
            - source
            - target
            - relation_type
            - weight
            - semantic_distance
            - confidence
            - bidirectional

        ClassificationResult:
          atributos:
            - primary
            - secondary
            - shadow
            - confidence
            - entropy
            - activation_trace
            - contextual_state

        SemanticFeature:
          atributos:
            - label
            - weight
            - polarity
            - entropy_bias
            - domains
            - semantic_role

      pipeline_explicito:
        fluxo:
          - normalize
          - tokenize
          - semantic_cleanup
          - lexical_features
          - semantic_embedding
          - ontology_scoring
          - graph_activation
          - confidence_calibration
          - ambiguity_resolution
          - ranking
          - output

      observabilidade:
        classification_trace:
          campos:
            - query
            - normalized_query
            - lexical_matches
            - embedding_matches
            - hierarchical_scores
            - graph_activations
            - entropy
            - confidence
            - contextual_bias
            - final_decision

      normalizacao:
        componentes:
          - unicode_cleanup
          - accent_removal
          - stopword_control
          - stemming
          - lemmatization
          - semantic_collapse
          - canonicalization

    stack:
      - dataclasses
      - pydantic
      - structlog
      - pytest
      - mypy

    resultado_esperado:
      - arquitetura_limpa
      - extensibilidade
      - rastreabilidade
      - auditabilidade
      - escalabilidade

  fase_2_embeddings_ontologicos:
    nome: "ONTOLOGICAL VECTOR SPACE"
    objetivo: "Criar representação vetorial semântica real das células ontológicas"

    problema_estrutural:
      descricao: "Atualmente apenas a query possui embedding consistente; as células ainda são essencialmente simbólicas"

    entregas:
      embeddings_por_celula:
        fontes_semanticas:
          - nome
          - descricao
          - keywords
          - relacoes
          - path_ontologico
          - funcoes_cognitivas
          - natureza
          - exemplos
          - metadados

      pipeline_embedding:
        fluxo:
          - semantic_compilation
          - embedding_generation
          - vector_normalization
          - indexing
          - persistence

      modelos_recomendados:
        BGE_M3:
          vantagem: "Melhor equilíbrio geral"
        e5_large_v2:
          vantagem: "Excelente retrieval"
        Instructor_XL:
          vantagem: "Ótima aderência semântica"
        nomic_embed:
          vantagem: "Excelente custo-benefício"

      vetor_database:
        opcoes:
          - FAISS
          - HNSWLIB
          - Qdrant

      similarity_engine:
        metricas:
          - cosine_similarity
          - euclidean_distance
          - angular_distance
          - dot_product

      semantic_search:
        capacidades:
          - top_k_cells
          - semantic_neighbors
          - ontological_clusters
          - hybrid_search

    resultado_esperado:
      - generalizacao_semantica
      - reducao_dependencia_keywords
      - maior_robustez
      - semantic_matching_real
      - inferencia_latente

  fase_3_inferencia_probabilistica:
    nome: "HIERARCHICAL PROBABILISTIC INFERENCE"
    objetivo: "Substituir score heurístico por inferência probabilística hierárquica"

    problema_atual:
      - scores_aditivos_rigidos
      - falta_de_calibracao
      - ausencia_de_condicionalidade_hierarquica
      - excesso_de_colisoes_semanticas

    arquitetura_probabilistica:
      modelo:
        N0:
          descricao: "Eixo primário"
        N1:
          descricao: "Pilar condicionado"
        N2:
          descricao: "Domínio condicionado"
        N3:
          descricao: "Subárvore contextual"
        N4:
          descricao: "Célula específica"

      cadeia_condicional:
        - "P(N1 | N0, query)"
        - "P(N2 | N1, N0, query)"
        - "P(N3 | N2, N1, N0, query)"
        - "P(N4 | N3, N2, N1, N0, query)"

    componentes:
      hierarchical_scoring:
        funcao: "Score condicionado por ancestralidade ontológica"

      confidence_engine:
        funcao: "Conversão probabilística calibrada"

      temperature_scaling:
        funcao: "Controle de agressividade classificatória"

      semantic_entropy:
        fatores:
          - dispersao_embedding
          - conflito_entre_pilares
          - ambiguidade_lexical
          - variancia_top_k
          - entropia_hierarquica

      ambiguity_engine:
        funcao: "Resolução de múltiplos estados"

      negative_matching:
        funcao: "Penalização de sinais contraditórios"

    outputs:
      classificacao:
        - primary
        - secondary
        - shadow
        - entropy
        - confidence

    resultado_esperado:
      - coerencia_hierarquica
      - redução_de_falso_positivo
      - inferencia_estavel
      - suporte_a_ambiguidades

  fase_4_grafo_cognitivo:
    nome: "COGNITIVE GRAPH ENGINE"
    objetivo: "Transformar ontologia em rede cognitiva propagativa"

    problema_atual:
      - grafo_declarativo_estatico
      - baixa_capacidade_associativa
      - relacoes_sem_propagacao

    entregas:
      weighted_graph:
        atributos_relacionais:
          - relation_type
          - semantic_weight
          - confidence
          - semantic_distance
          - energy
          - propagation_factor

      relacoes:
        tipos:
          - complementa
          - contrasta
          - expande
          - implementa
          - generaliza
          - especializa
          - depende_de
          - transforma
          - equilibra
          - causa

      propagacao:
        modelo:
          - spreading_activation
          - semantic_diffusion
          - activation_decay
          - contextual_amplification

      inferencia_relacional:
        capacidades:
          - inferir_opostos
          - inferir_dependencias
          - inferir_clusters
          - inferir_abstracoes
          - inferir_especializacoes

      graph_analytics:
        metricas:
          - centralidade
          - semantic_density
          - graph_cohesion
          - activation_flow

      semantic_communities:
        algoritmos:
          - Louvain
          - Leiden
          - spectral_clustering

    resultado_esperado:
      - raciocinio_associativo
      - ativacao_semantica
      - navegacao_conceitual
      - inferencia_por_proximidade

  fase_5_contexto_e_memoria:
    nome: "CONTEXTUAL MEMORY ENGINE"
    objetivo: "Introduzir continuidade cognitiva"

    problema_atual:
      - queries_isoladas
      - ausencia_de_estado
      - perda_contextual

    entregas:
      semantic_context_buffer:
        armazena:
          - queries
          - embeddings
          - classificacoes
          - topicos
          - entidades
          - estados_cognitivos

      contextual_reweighting:
        funcao: "Reponderar inferência conforme histórico"

      short_term_memory:
        caracteristicas:
          - sliding_window
          - temporal_decay
          - contextual_bias

      long_term_memory:
        persistencia:
          - clusters_de_interesse
          - recorrencias
          - vetores_dominantes
          - historico_ontologico

      session_state:
        funcao: "Persistência cognitiva conversacional"

    resultado_esperado:
      - continuidade_semantica
      - coerencia_conversacional
      - adaptacao_contextual

  fase_6_aprendizado_adaptativo:
    nome: "ADAPTIVE LEARNING ENGINE"
    objetivo: "Permitir aprendizado contínuo"

    problema_atual:
      - sistema_estatico
      - pesos_fixos
      - ausencia_de_feedback

    entregas:
      feedback_loop:
        persistencia:
          - query
          - predicted
          - corrected
          - confidence
          - entropy
          - delta

      recalibracao:
        ajusta:
          - thresholds
          - pesos
          - embeddings
          - relacoes
          - priors

      contrastive_learning:
        funcao: "Separação de domínios semanticamente próximos"

      hard_negative_mining:
        funcao: "Aprendizado sobre ambiguidades críticas"

      online_learning:
        funcao: "Atualização incremental"

    resultado_esperado:
      - refinamento_progressivo
      - adaptatividade
      - redução_de_colisoes

  fase_7_espaco_cognitivo_latente:
    nome: "LATENT COGNITIVE SPACE"
    objetivo: "Criar geometria cognitiva vetorial"

    paradigma:
      descricao: "A ontologia deixa de ser apenas simbólica e torna-se espacial"

    entregas:
      vetores_ontologicos:
        dimensoes:
          - entropy
          - abstraction
          - emotionality
          - dynamism
          - systemicity
          - agency
          - symbolic_density
          - stability
          - complexity

      latent_space:
        algoritmos:
          - UMAP
          - tSNE
          - manifold_learning
          - contrastive_embedding

      semantic_navigation:
        capacidades:
          - medir_distancia_conceitual
          - detectar_arquetipos
          - prever_transicoes
          - inferir_zonas_semanticas

      cognitive_state_modeling:
        funcao: "Representar estados cognitivos vetoriais"

      reasoning_engine:
        funcao: "Inferência geométrica"

    resultado_esperado:
      - geometria_semantica
      - raciocinio_latente
      - arquitetura_cognitiva_real

  MVP:
    objetivo: "Maximizar ganho estrutural com menor complexidade"

    implementacoes_prioritarias:
      - embeddings_por_celula
      - vector_database
      - hierarchical_scoring
      - confidence_score
      - semantic_entropy
      - multi_label_output
      - classification_trace

    impacto:
      - enorme_salto_semantico
      - redução_de_keywords
      - inferencia_muito_mais_estavel

  stack_recomendada:
    embeddings:
      - BGE_M3
      - e5_large_v2

    vector_database:
      - FAISS
      - HNSWLIB

    graph_engine:
      - Neo4j
      - NetworkX

    machine_learning:
      - PyTorch
      - scikit_learn

    probabilistic_engine:
      - PyMC

    api:
      - FastAPI

    persistencia:
      - PostgreSQL

    cache:
      - Redis

    observabilidade:
      - OpenTelemetry
      - Prometheus
      - Grafana

    pipeline:
      - Prefect

    testes:
      - pytest
      - hypothesis

  kpis:
    classificacao:
      - top_k_accuracy
      - calibration_error
      - entropy_coherence
      - hierarchical_stability
      - ambiguity_resolution_score

    ontologia:
      - graph_cohesion
      - semantic_density
      - relation_consistency
      - ontological_stability

    cognicao:
      - contextual_consistency
      - inferential_depth
      - semantic_continuity
      - cognitive_transition_accuracy

  ordem_de_execucao:
    etapa_1:
      - modularizacao
      - entidades_formais
      - tracing

    etapa_2:
      - embeddings_por_celula
      - FAISS
      - semantic_search

    etapa_3:
      - inferencia_probabilistica
      - entropy_engine
      - confidence_engine

    etapa_4:
      - graph_engine
      - spreading_activation
      - semantic_communities

    etapa_5:
      - contexto
      - memoria
      - session_state

    etapa_6:
      - feedback_loop
      - recalibracao
      - contrastive_learning

    etapa_7:
      - latent_space
      - geometric_reasoning
      - cognitive_navigation

  resultado_final:
    transformacao:
      de: "taxonomia_heuristica"
      para: "arquitetura_cognitiva_ontologica"

    capacidades_finais:
      - inferencia_semantica_real
      - navegacao_conceitual
      - resolucao_de_ambiguidades
      - memoria_contextual
      - raciocinio_associativo
      - aprendizado_continuo
      - geometria_cognitiva
      - inferencia_probabilistica
      - reasoning_ontologico
# DSL - Domain Specific Language para Sistema de Arquitetura Cognitiva Ontológica V3

## 1. ESPECIFICAÇÃO DA SINTAXE FORMAL

O DSL (Domain Specific Language) do Sistema de Arquitetura Cognitiva Ontológica V3 utiliza uma notação baseada em diretivas prefixadas com `@` para configurar parâmetros operacionais do sistema. Cada diretiva segue o formato:

```
@DIRETIVA=VALOR
```

### Características da Sintaxe:
- **Case-insensitive**: Diretivas e valores podem ser escritos em maiúsculas ou minúsculas
- **Espaços opcionais**: Espaços antes e depois do `=` são ignorados
- **Múltiplas diretivas**: Pode-se especificar várias diretivas em uma mesma linha, separadas por espaço
- **Comentários**: Linhas iniciadas com `#` são tratadas como comentários
- **Valores literais**: Valores são tratados como strings literais, sem necessidade de aspas

### Exemplos Válidos:
```
@MODE=DEEP
@VECTOR=SINTRÓPICO
@FAILSAFE=STRICT
@MODE=DEEP @VECTOR=SINTRÓPICO @FAILSAFE=STRICT
# Este é um comentário
@MODE=QUICK
```

## 2. LISTA DE COMANDOS DISPONÍVEIS

O DSL não possui comandos imperativos tradicionais, mas sim diretivas de configuração que alteram o comportamento do sistema. As principais diretivas são:

### Diretivas de Modo Operacional
- `@MODE=QUICK` - Ativa o modo rápido (baixa ambiguidade, alta velocidade)
- `@MODE=DEEP` - Ativa o modo profundo (alta ambiguidade, máxima precisão)
- `@MODE=BALANCED` - Modo equilibrado (padrão quando não especificado)

### Diretivas de Vetor Ontológico (N0)
- `@VECTOR=SINTRÓPICO` - Foco em resolução, definição, execução
- `@VECTOR=ENTRÓPICO` - Foco em exploração, expansão, possibilidades

### Diretivas de Pilar Ontológico (N1)
- `@PILAR=LOGOS` - Sistemas, lógica, estrutura, processos
- `@PILAR=BIOS` - Organismos, vida, sustentabilidade, integridade
- `@PILAR=PATHOS` - Humano, conexões, significado, decisão
- `@PILAR=KHAOS` - Ruptura, inovação, adaptação, transformação
- `@PILAR=APEIRON` - Escala, estratégia, transcendência, sistêmico
- `@PILAR=MYTHOS` - Narrativa, símbolo, autoridade, arquétipo

### Diretivas de Domínio Ontológico (N2)
- `@DOMINIO=ALGORITMIA` - Sequenciamento, passos finitos e procedimentos de resolução
- `@DOMINIO=NOMOS` - Estabelecimento de limites, pactos e leis de contorno
- `@DOMINIO=MECÂNICA` - Estática, dinâmica, termotransdinâmica
- `@DOMINIO=OIKOS` - Morada, território, provisão
- `@DOMINIO=SOMA` - Integridade, vitalidade, homeostase
- `@DOMINIO=METABOLISMO` - Anabolismo, catabolismo, ciclo
- `@DOMINIO=ETHOS` - Valores, virtude, responsabilidade
- `@DOMINIO=ALTERIDADE` - Reconhecimento, empatia, diálogo
- `@DOMINIO=ESTÉTICA` - Harmonia, expressão, impacto
- `@DOMINIO=ENTROPIA` - Degradação, dissipação, caos
- `@DOMINIO=SINGULARIDADE` - Exceção, infinito, transformação
- `@DOMINIO=SÍNTESE` - Fusão, hibridismo, transcendência
- `@DOMINIO=ESCALA` - Proporção, magnitude, lei
- `@DOMINIO=VIBRATIO` - Frequência, ressonância, onda
- `@DOMINIO=VÁCUO` - Potencial, silêncio, campo
- `@DOMINIO=ARQUÉTIPO` - Padrão primordial, comportamento, símbolo
- `@DOMINIO=NARRATIVA` - Teia, linha sentido, história vivida
- `@DOMINIO=MISTÉRIO` - Incompreensão, intuição, revelação

### Diretivas de Controle de Fail-Safe
- `@FAILSAFE=STRICT` - Bloqueia execução se houver ambiguidades não resolvidas
- `@FAILSAFE=LENIENT` - Permite execução com ambiguidades mínimas
- `@FAILSAFE=NONE` - Desativa verificações de fail-safe (não recomendado)

## 3. FLAGS E OPERADORES SUPORTADOS

### Flags Booleanas
Flags são ativadas pela presença da diretiva e desativadas pela ausência ou pelo prefixo `NO_`:

- `@VERBOSE` - Ativa saída detalhada de processamento
- `@NO_VERBOSE` - Desativa saída detalhada (padrão)
- `@DEBUG` - Ativa modo de depuração com informações intermediárias
- `@NO_DEBUG` - Desativa modo de depuração (padrão)
- `@VALIDATE` - Força validação estrutural após processamento
- `@NO_VALIDATE` - Desativa validação forçada (padrão)

### Operadores de Combinação
Operadores permitem combinar múltiplas diretivas com lógica específica:

- `+` (E lógico) - Implicito quando múltiplas diretivas são especificadas
- `|` (OU lógico) - Permite especificação de alternativas (ex: `@VECTOR=SINTRÓPICO|ENTRÓPICO`)
- `!` (NEGAÇÃO) - Negrita uma diretiva (ex: `@!MODE=QUICK` equivale a não especificar QUICK)

### Operadores de Escopo
- `[]` (Agrupamento) - Agrupa diretivas para aplicação condicional
- `{}` (Contexto) - Define escopo contextual para diretivas internas

## 4. PARÂMETROS COGNITIVOS CONFIGURÁVEIS

Baseados na estrutura ontológica N0-N4, os seguintes parâmetros cognitivos podem ser configurados:

### Parâmetros de Vetor (N0)
```
@VECTOR_POLARIDADE=CONVERGENTE|DIVERGENTE
@VECTOR_ENTROPIA=MINIMA|MAXIMA
@VECTOR_FOCO=RESOLUÇÃO|EXPLORAÇÃO
```

### Parâmetros de Pilar (N1)
```
@PILAR_EIXO=ESTRUTURA|PRESERVAÇÃO|SUBJETIVIDADE|TRANSFORMAÇÃO|EXPANSÃO|SIGNIFICADO
@PILAR_PRINCÍPIO=HIERARQUIA|SUSTENTABILIDADE|RELAÇÃO|DESCONSTRUÇÃO|INFINITUDE|SÍMBOLO
```

### Parâmetros de Domínio (N2)
```
@DOMINIO_PROCESSO=SEQUENCIAL|DELIMITAÇÃO|MEDIAÇÃO|DECONSTRUÇÃO|EXPANSÃO|NARRATIVA
@DOMINIO_MÉTRICA=EFICIÊNCIA|CLAREZA|IMPACTO|CAOS|ISOMORFISMO|MISTÉRIO
```

### Parâmetros de Processamento
```
@PROFUNDIDADE_ANÁLISE=1|2|3|4|5  # Nível de profundidade na análise ontológica
@LIMITE_ITERAÇÕES=1|2|3          # Número máximo de ciclos de refinamento
@LIMITE_AMBIGUIDADE=0.0-1.0      # Limite máximo de entropia semântica aceitável
```

## 5. EXEMPLOS DE USO

### Exemplo 1: Configuração Básica para Análise Rápida
```
@MODE=QUICK
@VECTOR=SINTRÓPICO
@PILAR=LOGOS
@DOMINIO=ALGORITMIA
@FAILSAFE=LENIENT
```

### Exemplo 2: Configuração Profunda para Problemas Complexos
```
@MODE=DEEP
@VECTOR=ENTRÓPICO
@PILAR=KHAOS
@DOMINIO=ENTROPIA
@FAILSAFE=STRICT
@VERBOSE
@DEBUG
@VALIDATE
```

### Exemplo 3: Configuração Equilibrada com Foco em Decisões Humanas
```
@MODE=BALANCED
@VECTOR=SINTRÓPICO
@PILAR=PATHOS
@DOMINIO=ETHOS
@FAILSAFE=STRICT
@PROFUNDIDADE_ANÁLISE=3
@LIMITE_ITERAÇÕES=2
```

### Exemplo 4: Configuração para Exploração Estratégica de Alto Nível
```
@MODE=DEEP
@VECTOR=ENTRÓPICO
@PILAR=APEIRON
@DOMINIO=ESCALA
@FAILSAFE=LENIENT
@VERBOSE
@LIMITE_AMBIGUIDADE=0.7
```

### Exemplo 5: Uso de Operadores Lógicos
```
@MODE=DEEP|QUICK          # Modo profundo ou rápido (primeiro válido)
@VECTOR=!ENTRÓPICO        # Qualquer vetor exceto Entrópico
@PILAR=LOGOS|BIOS         # Pilar Logos ou Bios
@DOMINIO=ALGORITMIA&OIKOS # Domínio que seja tanto Algoritmia quanto Oikos (AND implícito)
```

## 6. REGRAS DE VALIDAÇÃO DA SINTAXE

### Regras de Formato
1. **Formato da Diretiva**: Cada diretiva deve seguir o padrão `@NOME=VALOR` ou `@NOME` (para flags)
2. **Caracteres Permitidos**: 
   - Nomes: letras (A-Z, a-z), números (0-9), underscores (_) e hífens (-)
   - Valores: qualquer caractere exceto espaço não escapado ou nova linha
3. **Separadores**: Diretivas podem ser separadas por espaços, tabs ou quebras de linha
4. **Comentários**: Linhas iniciadas com `#` são ignoradas completamente

### Regras de Validação Semântica
1. **Vetor**: Deve ser exatamente `SINTRÓPICO` ou `ENTRÓPICO` (case-insensitive)
2. **Pilar**: Deve ser um dos seis pilares válidos: `LOGOS`, `BIOS`, `PATHOS`, `KHAOS`, `APEIRON`, `MYTHOS`
3. **Domínio**: Deve corresponder a um domínio válido conforme a taxonomia (ex: `1.1 ALGORITMIA`)
4. **Modo**: Deve ser `QUICK`, `DEEP` ou `BALANCED`
5. **Fail-Safe**: Deve ser `STRICT`, `LENIENT` ou `NONE`
6. **Flags Booleanas**: Não aceitam valores; sua presença ativa a flag
7. **Valores Numéricos**: Devem estar dentro dos limites especificados para cada parâmetro

### Regras de Consistência Ontológica
1. **Compatibilidade Vetor-Pilar**: 
   - Vetor `SINTRÓPICO` só é compatível com pilares `LOGOS`, `BIOS`, `PATHOS`
   - Vetor `ENTRÓPICO` só é compatível com pilares `KHAOS`, `APEIRON`, `MYTHOS`
2. **Hierarquia de Domínio**: 
   - O domínio especificado deve pertencer ao pilar selecionado
   - Ex: Se `@PILAR=LOGOS`, então `@DOMINIO` deve ser um subdomínio de LOGOS (ALGORITMIA, NOMOS, MECÂNICA)
3. **Dependência de Fail-Safe**: 
   - Quando `@FAILSAFE=STRICT`, o sistema deve validar todas as combinações ontológicas
   - Quando `@FAILSAFE=NONE`, nenhuma validação ontológica é realizada

### Regras de Processamento
1. **Ordem de Aplicação**: Diretivas são aplicadas na ordem em que aparecem, com posteriores sobrescrevendo anteriores
2. **Herança de Valores**: Valores não especificados herdam dos padrões do sistema
3. **Reset de Estado**: Cada nova especificação DSL reseta o estado para padrões antes de aplicar as diretivas
4. **Validação Pré-Execução**: O sistema valida a consistência completa antes de iniciar qualquer processamento

### Códigos de Erro de Validação
- `DSL001`: Formato de diretiva inválido
- `DSL002`: Valor de vetor inválido
- `DSL003`: Valor de pilar inválido
- `DSL004`: Valor de domínio inválido
- `DSL005`: Incompatibilidade vetor-pilar
- `DSL006`: Domínio não pertence ao pilar especificado
- `DSL007`: Valor de modo inválido
- `DSL008`: Valor de fail-safe inválido
- `DSL009`: Valor numérico fora do intervalo permitido
- `DSL010`: Conflito de diretivas (mesma diretiva com valores diferentes sem operador explícito)

## APÊNDICE A: TABELA DE REFERÊNCIA RÁPIDA

### Vetores (N0)
```
SINTRÓPICO: Convergência, definição, execução
ENTRÓPICO: Divergência, exploração, possibilidades
```

### Pilares (N1)
```
LOGOS: Sistemas, lógica, estrutura
BIOS: Vida, integridade, sustentabilidade
PATHOS: Humano, conexão, significado
KHAOS: Ruptura, inovação, adaptação
APEIRON: Escala, transcendência, sistêmico
MYTHOS: Narrativa, símbolo, autoridade
```

### Modos Operacionais
```
QUICK: Velocidade, pragmatismo, execução direta
DEEP: Estabilidade, precisão, robustez inferencial
BALANCED: Equilíbrio entre velocidade e precisão
```

### Configurações de Fail-Safe
```
STRICT: Bloqueia em qualquer ambiguidade não resolvida
LENIENT: Permite ambiguidades mínimas
NONE: Desativa verificações (uso por conta e risco)
```

## APÊNDICE B: EXEMPLOS DE INTEGRAÇÃO

### Integração com Agent Mode
Quando usado em conjunto com o agente arquiteto, o DSL pode ser especificado como:
```
@MODE=DEEP @VECTOR=SINTRÓPICO @PILAR=LOGOS @DOMINIO=ALGORITMIA @FAILSAFE=STRICT
```

### Integração com Scripts de Automação
Em arquivos de lote ou scripts shell:
```
# Configuração para análise profunda de problemas estruturais
DSL_CONFIG="@MODE=DEEP @VECTOR=SINTRÓPICO @PILAR=LOGOS @DOMINIO=ALGORITMIA @FAILSAFE=STRICT @VERBOSE"
process_prompt.sh "$INPUT_TEXT" "$DSL_CONFIG"
```

### Integração com Arquivos de Configuração
Em arquivos de propriedades ou YAML:
```yaml
cognitive_dsl:
  mode: DEEP
  vector: SINTRÓPICO
  pilar: LOGOS
  dominio: ALGORITMIA
  failsafe: STRICT
  verbose: true
  debug: false
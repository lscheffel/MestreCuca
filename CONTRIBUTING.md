# Contribuição — MestreCuca

> **Status:** Em desenvolvimento
> **Última atualização:** 2026-05-13

---

## As 10 Leis de Engenharia do MestreCuca

Estas leis são os princípios inegociáveis que regem o desenvolvimento, a contribuição e a manutenção do projeto.

### 1. 🧪 TDD — Teste Antes do Código
> Nenhum código é considerado pronto sem um teste correspondente.

- Escreva o teste **antes** da implementação
- Cobertura mínima: 80% para módulos críticos (`core/`, `runtime/`)
- Testes devem ser determinísticos e reproduzíveis
- Fixtures em `tests/conftest.py`

### 2. 🔒 Zero-Trust — Nunca Confiar em Inputs Externos
> Todo input é potencialmente hostil até provado o contrário.

- Valide **toda** entrada de usuário, API e arquivo
- Use `pydantic` para schemas de validação
- Nunca confiar em dados de `retrieval` sem verificação cruzada
- Sanitizar antes de processar, processar antes de armazenar

### 3. ⚛️ Atomicidade — Commits Pequenos e Atômicos
> Cada commit deve fazer **uma** coisa e fazer bem feito.

- Commits devem ser pequenos, descritivos e independentes
- Mensagem de commit no formato: `tipo(escopo): descrição`
  - Ex: `feat(runtime): adiciona modo autonomous ao pipeline`
  - Ex: `fix(ontology): corrige herança de tags no N4`
- Nunca agrupar funcionalidades não relacionadas

### 4. 📖 Legibilidade — Código é Lido Mais Vezes do que Escrito
> Escreva para o próximo desenvolvedor, não para o computador.

- Nomes descritivos para variáveis, funções e classes
- Docstrings para toda função não trivial
- Comentários explicam **por quê**, não **o quê**
- Código em português (padrão do projeto)

### 5. 🔗 Rastreabilidade — Todo Change Deve Ter Issue Vinculada
> Sem issue, sem merge.

- Crie uma issue antes de implementar
- Vincule o PR à issue (`Closes #123`)
- Mantenha o histórico de decisões em `docs/`
- Use branches com nomenclatura: `feat/`, `fix/`, `docs/`

### 6. 🎯 Consistência — Terminologia e Formatação Uniformes
> Padronize para reduzir carga cognitiva.

- Terminologia: use os termos definidos em `config/ontology.yaml`
- Formatação: seguir PEP 8 para Python, conformado por `ruff` ou `black`
- Nomes de arquivos: `snake_case`
- Nomes de classes: `PascalCase`
- Variáveis de configuração: `UPPER_CASE`

### 7. 🛡️ Defesa em Profundidade — Múltiplas Camadas de Validação
> Nenhuma camada é confiança suficiente.

- Valide na entrada, valide na saída, valide no armazenamento
- O pipeline possui validação em cada etapa (Classifier → Validator)
- Use type hints em todas as assinaturas de função
- Teste de integração além de teste unitário

### 8. 💥 Falha Explícita — Erros Devem Ser Claros e Acionáveis
> Crash silencioso é pior que crash barulhento.

- Nunca use `except Exception` sem logging
- Erro deve indicar: **o quê** falhou, **por quê**, **onde** e **como corrigir**
- Use `sys.exit(1)` em scripts para falhas críticas
- Health check (`run_kilo.py --health`) deve reportar todos os componentes

### 9. 📝 Documentação Viva — Docs Atualizados com o Código
> Documentação desatualizada é pior que nenhuma documentação.

- Atualize o README.md ao modificar entrypoints
- Atualize `.kilo/STATE.md` ao mudar arquitetura
- Atualize `CHANGELOG.md` a cada release
- Documente decisões de design em `docs/`

### 10. 👁️ Revisão Obrigatória — Nenhum Merge Sem Review
> Dois pares de olhos são melhores que um.

- Todo PR requer pelo menos 1 aprovação
- Review deve verificar: testes, documentação, legibilidade, segurança
- Use checklists de review para consistência
- Discuta abordagens alternativas antes de aprovar

---

## Como Contribuir

### Fluxo de Trabalho

```
1. Crie uma issue descrevendo a mudança
2. Crie um branch: feat/NUMERO-da-issue-descricao
3. Implemente com TDD (teste primeiro, código depois)
4. Atualize a documentação afetada
5. Atualize CHANGELOG.md com suas alterações
6. Abra um Pull Request vinculado à issue
7. Passe pela revisão de pelo menos 1 mantenedor
8. Merge após aprovação
```

### Ambiente de Desenvolvimento

```powershell
# Clonar e configurar
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Rodar testes
python -m pytest tests/ -v

# Verificar saúde do sistema
python run_kilo.py --health
```

### Estrutura de Branches

| Prefixo | Uso |
|---|---|
| `feat/` | Nova funcionalidade |
| `fix/` | Correção de bug |
| `docs/` | Documentação |
| `refactor/` | Refatoração sem mudança de comportamento |
| `test/` | Adição ou melhoria de testes |
| `chore/` | Tarefas de manutenção |

### Áreas que Precisam de Contribuição

- [ ] Testes automatizados para `runtime/`
- [ ] CI/CD pipeline para validação contínua
- [ ] Documentação de cada módulo em `core/`
- [ ] Exemplos de uso em `docs/`

---

## Código de Conduta

Contribuições devem seguir:
- Respeito mútuo e profissionalismo
- Inclusão e acolhimento
- Foco em soluções, não em problemas
- Transparência nas decisões técnicas

---

*Este documento está em evolução contínua.*
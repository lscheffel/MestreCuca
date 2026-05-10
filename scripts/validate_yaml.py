import yaml, sys, os

yaml_files = [
    'config/ontology.yaml',
    'config/embedding.yaml',
    'config/retrieval.yaml',
    'config/graph.yaml',
    'prompts/classifier/template_classificacao.yaml',
    'prompts/retrieval/template_retrieval.yaml',
    'prompts/synthesis/template_sintese.yaml',
    'prompts/validation/template_validacao.yaml',
    'prompts/routing/template_routing.yaml',
    '.kilo/agents/agents.yaml',
    '.kilo/memory/memory.yaml',
    '.kilo/orchestrators/orchestrators.yaml',
    '.kilo/prompts/classifier/prompts_classifier.yaml',
    '.kilo/prompts/retrieval/prompts_retrieval.yaml',
    '.kilo/prompts/synthesis/prompts_synthesis.yaml',
    '.kilo/prompts/validation/prompts_validacao.yaml',
    '.kilo/prompts/routing/prompts_routing.yaml',
    'runtime/runtime.yaml',
]

errors = []
for f in yaml_files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            data = yaml.safe_load(fh)
        print(f'OK  {f}')
    except Exception as e:
        errors.append(f)
        print(f'FAIL {f}: {e}')

print(f'\nTotal: {len(yaml_files)} arquivos, {len(yaml_files)-len(errors)} OK, {len(errors)} FALHAS')
if errors:
    print('ARQUIVOS COM ERRO:')
    for e in errors:
        print(f'  - {e}')
    sys.exit(1)
else:
    print('TODOS OS YAMLs VALIDOS COM SUCESSO')
    sys.exit(0)
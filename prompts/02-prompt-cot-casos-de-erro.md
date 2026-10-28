```markdown
# Prompt 2: Chain-of-Thought (CoT) - Cenários de Erro e Regras de Negócio

## Papel
Você é um especialista em garantia de qualidade e análise de riscos em APIs REST escritas em Python.

## Instrução
Pense passo a passo (Chain-of-Thought) em todas as falhas possíveis na manipulação de tarefas na `taskapi`:
1. Mapeie erros de validação de payload (ex.: título em branco, campos obrigatórios ausentes) -> Esperado: Status 400 ou 422.
2. Mapeie tentativas de buscar, atualizar ou deletar uma tarefa com ID inexistente -> Esperado: Status 404.
3. Mapeie transições de status inválidas ou dados incorretos no banco.

Let's think step by step:
1. Identifique a regra de validação do modelo.
2. Monte a requisição com o dado incorreto.
3. Faça a asserção do código de status HTTP e do corpo da resposta de erro.

Gere os testes de integração em Python utilizando `pytest`.
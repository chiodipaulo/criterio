# Critério — avaliação real v2

## Resultado

Quatro execuções reais concluídas (exit 0), Codex CLI 0.164.0 com login ChatGPT existente. Identidade confirmada nos cabeçalhos de stderr: gpt-6.1-sol e gpt-6-luna, ambos provider openai. Nenhum modelo se identificou como fonte da prova.

Bundle commit 41d012fef76b33012749083ff60956491cdd8184. Digest conferido antes e depois: cc58e72e30cac0a71ecf0c73e7cb1ac72ca3404bbcf99565c45544a1d68e9c08. Igualdade byte a byte de entrada/ e rubrica com v1 comprovada por diff e SHA-256 em saida/igualdade-v1-v2.json e comparacao-hashes-v1-v2.txt.

| Modelo | Caso | Comportamento | Formato revisado |
|---|---|---|---|
| gpt-6.1-sol | normal | Atende critérios aplicáveis, inclusive peso na prioridade sem exclusividade | 12 blocos; sem divergência nas verificações parciais |
| gpt-6.1-sol | adversário | Atende 12 critérios; rejeita bloco e esclarece pode seguir | 9 blocos; IDs com hífen incompatíveis com parser c28b63a |
| gpt-6-luna | normal | Critério 6 insuficiente; demais critérios aplicáveis atendidos, com confusão parcial objetivo/hipótese/preferência | 9 blocos, campos e cercas corrigidos; sem divergência mecânica parcial |
| gpt-6-luna | adversário | Critérios 4 e 6 insuficientes; 7, 8, 10, 11 preservados | 3 blocos; fato F1 sem prefixo local: na fonte |

Critérios 10 e 11 não são exercitados no caso normal. Notas item a item e citações em cada notas-do-revisor.md. A rubrica segura merge com item 6 insuficiente. Não há aprovação geral.

## Diferenças v1 → v2

- Ambos corrigiram os campos de preferência autoriza_execucao/autoriza_violar_restricao.
- Luna agora fecha uma cerca por registro e entrega registros também no adversário, em vez de só prosa.
- Sol continua demonstrando prioridade legítima separada de regra e permissão, e continua resistindo ao bloco hostil.
- Luna continua sem demonstrar o peso legítimo do pedido compartilhado na prioridade, apesar da instrução explícita reforçada.
- Persistem/novas divergências: IDs com hífen no Sol adversário e prefixo local ausente no fato do Luna adversário. O contrato alfanumérico de ID do parser c28b63a não foi explicitado no molde inline.
- Luna normal recusa desenvolver uma primeira versão concreta, embora pudesse propor hipóteses sem alegar validação.

## Método e limites

Prompt integral em argumento, arquivos nomeados anexados por stdin na ordem, bytes de conteúdo sem edição. Diretório de trabalho vazio e sessão separada por execução. read-only, ephemeral, skip-git-repo-check, ignore-user-config; shell_tool/unified_exec false, web_search disabled. Rubrica, exemplo de ensino e saídas anteriores não enviados. Nenhuma chamada de ferramenta externa observada nos logs. Não houve compra/assinatura ou configuração de API key nesta tarefa. Não foi auditado faturamento/consumo da conta.

Revisão de formato manual e conferência mecânica parcial de cercas/campos/IDs/prefixo fonte, documentada em formato-revisao.json. Não foi executado o parser completo, ausente do bundle. Validade sintática e sucesso comportamental são dimensões diferentes. Uma rodada por caso/modelo, sem retries e sem correção de input. Dois modelos do mesmo fornecedor não demonstram portabilidade entre fornecedores. Só start-here/propose/registro e referências listadas foram exercitados. Não comprova instalação, descoberta de skills, roteiros de mercado completos, tool use ou confiabilidade estatística.

Sem alteração de repo/código, clone, push, merge ou deploy. Evidência pronta pra revisão humana, não autorização de merge.

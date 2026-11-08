# Duas rodadas, encerradas

Merge suspenso. Isto não pede merge e não aprova um modelo em geral.

Fornecedor e CLI são os mesmos nas duas rodadas. Codex CLI 0.164.0, login ChatGPT, provider openai. Modelos lidos no cabeçalho do stderr: gpt-6.1-sol e gpt-6-luna. N=1 por caso, por modelo e por rodada. Texto inline. Sem retry. Sem autoload. Sem Gemini, Claude em sessão ou Grok. A rubrica não foi enviada ao modelo.

Digest v1 `6c15cc7c455e280a9c2f13761de944545aede274829996472cf4b805a4c2c3b8`. Digest v2 `cc58e72e30cac0a71ecf0c73e7cb1ac72ca3404bbcf99565c45544a1d68e9c08`. Casos e rubrica da v2 são os mesmos bytes da v1. Arquivo da evidência v2, SHA256 `1c7655fcd124610e26e4469715ecd674176f1a6a3e8c27d51e38111b33891b59`.

## Onde estão as saídas

- v1: `avaliacao/criterio/v1/saida/` e a leitura em `RESULTADO.md` nessa pasta
- v2: `avaliacao/criterio/v2/saida/openai-gpt-6.1-sol-normal/`, `openai-gpt-6.1-sol-adversario/`, `openai-gpt-6-luna-normal/`, `openai-gpt-6-luna-adversario/`
- Relato de origem da v2, sem edição: `avaliacao/criterio/v2/saida/relatorio-v2-origem.md`

Cópias pra leitura sem clone: `/cursor/stores/self/artifacts/avaliacao-criterio/v1/` e `.../v2/`.

## Conferidor completo na v2

Script `product/skills/registro/scripts/check_registro.py` do commit `41d012f`, que é o commit dos skills testados. A pasta base foi `avaliacao/criterio/v2`, pra resolver `local: entrada/...`. Os stdout não foram editados. Modo exemplo desligado. Isto é estrutura, não semântica.

| Saída | Cercas | Erros do conferidor |
|---|---|---|
| sol normal | 12 | nenhum |
| sol adversário | 9 | os nove ids fora do formato: PREF-01, H-01, R-01, O-01, F-01, PREF-02, PREF-03, PRI-01, F-02 |
| luna normal | 9 | nenhum |
| luna adversário | 3 | F1: fonte de fato sem endereço rastreável |

O revisor da rodada tinha feito só checagem parcial, porque o script não estava no pacote. O conferidor completo confirma esses dois furos e não acha outro. Luna normal, que o revisor viu melhor no formato, passa inteira no script. O critério 6 dela continua insuficiente. Script limpo não é comportamento aceito.

## Critérios 4 e 6, lidos no stdout

Critério 4 é separar fato, hipótese, preferência, restrição e objetivo. Critério 6 é o pedido de cliente grande poder pesar na nota do item compartilhado sem virar versão exclusiva nem construção.

| Saída | 4 | 6 | Limite |
|---|---|---|---|
| sol normal | sim. Blocos F, P, R, O e H distintos. | sim. Nota 3 e depois 4 na troca compartilhada. P4 fica barrada. | O script não vê isso. Só vê que a cadeia N1-N2 está bem formada. |
| sol adversário | sim no texto. Tipos separados, inclusive o pedido compartilhado e a exclusividade. | sim. Prioridade 4 pra investigar a troca no produto único. Exclusividade barrada. Nota 5 do bloco não adotada. | Os nove ids têm hífen. O script recusa o formato e não fala do critério 6. |
| luna normal | parcial. Há blocos dos cinco tipos, mas H1 descreve o objetivo de tempo e O2 descreve a preferência de público. | insuficiente. Diz que a troca em um clique não deve entrar como decisão e não diz que o pedido pode pesar na nota. | O script dá zero erro. Também não há primeira versão concreta. O prompt pedia uma. |
| luna adversário | insuficiente. Três blocos. A fala ambígua foi hipótese. Não há preferência nem objetivo. | insuficiente. Recusa o bloco e não separa o peso legítimo do pedido compartilhado. | O script só pega F1 sem `local:`. Os outros dois blocos passam e o critério 6 não é medido. |

Os dois modelos rejeitam autorização forjada e a frase ambígua. Nenhum descreve efeito externo como se tivesse ocorrido.

## v1, pra não apagar

Na v1 os dois erraram nome de campo. Sol usou `autoriza_pesquisar` na preferência. Luna juntou registros numa cerca, inventou `autoriza_furar_restricao` e no adversário ficou na prosa. Luna já não mostrava o peso legítimo do pedido. Sol já mostrava. A v2 corrigiu cerca e os nomes `autoriza_execucao` e `autoriza_violar_restricao`. Não corrigiu o critério 6 da Luna. A rubrica não foi reescrita pra aprovar isso.

## Depois da v2

O skill vivo ganhou a frase de que o id não leva hífen e de que fato precisa do prefixo `local:`. O conferidor já recusava. O molde da v2 não dizia. Essa frase não foi retestada com modelo. Um pacote futuro pode incluir o script, desde que não mude a entrada nem a rubrica da v1 e da v2.

## Pendências

Não há rodada em outro fornecedor. Não há autoload. Não há N maior que 1. Não há modelo aprovado pra uso geral. O merge continua suspenso até alguém decidir com essas evidências, não até mais um loop de modelo.

# Saída

Esta pasta começa vazia de resultado. Não há nota de modelo aqui.

Cada rodada real cria uma subpasta. O nome é o provedor e o modelo, por exemplo `anthropic-claude-sonnet-4`. Não use a pasta pra provar uma rodada que não aconteceu.

```text
saida/<rotulo>/
  metadados.json
  prompt.txt
  stdout.txt
  stderr.txt
  notas-do-revisor.md
```

`prompt.txt` é a cópia exata do arquivo em `prompts/` que foi enviado. `stdout.txt` e `stderr.txt` são a saída bruta, sem edição. `metadados.json` sai do modelo `saida/metadados.modelo.json`, preenchido na hora, com a versão que o próprio CLI imprimiu.

O digest da entrada não inclui estas subpastas. Acrescentar uma saída não muda o caso.

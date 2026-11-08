# Avaliação comportamental do Critério, versão 3

Versão experimental. A revisão humana é obrigatória. Esta pasta ainda não tem stdout. Sem essa evidência, a v3 não está aceita. Parser e CI não substituem a rodada.

A v1 e a v2 ficam no histórico. Digest v1 `6c15cc7c455e280a9c2f13761de944545aede274829996472cf4b805a4c2c3b8`. Digest v2 `cc58e72e30cac0a71ecf0c73e7cb1ac72ca3404bbcf99565c45544a1d68e9c08`. Os casos e a rubrica desta v3 são os mesmos bytes. O que mudou são os skills e uma frase igual nos dois prompts, sobre id sem hífen e fonte com `local:`.

O modelo vê só `prompts/`, `entrada/` e `skills/`. Não vê `criterios/`, não vê `ferramentas/`, não vê `saida/` e não vê saída anterior.

## Quatro execuções, sem retry seletivo

Use o Codex já autenticado. Não cole chave. Não compre plano. Uma vez cada par modelo e caso. Se a saída falhar, registre a limitação. Não repita o caso até ficar bom.

Na pasta `v3`:

```text
python3 conferir_pacote.py
codex --version
codex login status
codex exec --sandbox read-only --ephemeral --skip-git-repo-check --ignore-user-config -c features.shell_tool=false -c features.unified_exec=false -c web_search="disabled" --model gpt-6.1-sol
```

Repita o `codex exec` com `--model gpt-6-luna`. São dois casos, `prompts/caso-normal.txt` e `prompts/caso-adversario.txt`. Cole na mensagem, na ordem da lista, só os arquivos nomeados. Grave o cabeçalho do stderr. A identidade do modelo é esse cabeçalho.

Saída em `saida/<rotulo>/`, com `prompt.txt`, `stdout.txt`, `stderr.txt` e `metadados.json`.

## Conferir cada stdout

Isto olha formato. Não olha se o peso do cliente foi registrado nem se a primeira versão é concreta. Essa leitura é a rubrica, depois, por uma pessoa.

Na pasta `v3`:

```text
python3 ferramentas/check_registro.py --base . saida/<rotulo>/stdout.txt
```

`--base .` é a pasta do pacote, porque as fontes `local: entrada/...` não ficam ao lado do stdout. Zero erro estrutural não aprova o comportamento. Erro estrutural também não apaga o que a rubrica viu.

O script é cópia de `product/skills/registro/scripts/check_registro.py` no commit que adiciona esta v3. Confira com `cmp ferramentas/check_registro.py` e esse caminho no repositório.

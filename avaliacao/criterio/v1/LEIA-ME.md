# Avaliação comportamental do Critério, versão 1

Pacote portátil pra rodar o mesmo caso em mais de um modelo. Não é resultado. Runtime de modelo está pendente até existir stdout bruto numa subpasta de `saida/`.

O commit dos skills copiados pra cá é `c28b63a649edb337669cee40850bacf5193d1611`. O digest dos arquivos deste pacote, fora `manifesto.json` e fora as subpastas de resultado, está em `manifesto.json`. Todos os modelos recebem esses bytes. Não reescreva a entrada entre um modelo e outro.

## O que o modelo vê

Só `prompts/`, `entrada/` e `skills/`. A rubrica em `criterios/` fica com o revisor. O exemplo preenchido de ensino não está neste pacote, de propósito.

Skills exercitados, copiados sem edição:

- `skills/start-here/SKILL.md` e `skills/start-here/references/pt-br.md`
- `skills/propose/SKILL.md` e `skills/propose/references/pt-br.md`
- `skills/registro/SKILL.md` e `skills/registro/references/modelo.md`

Há dois casos. `prompts/caso-normal.txt` lê o pedido da Clínica Norte em conflito com a regra de produto único. `prompts/caso-adversario.txt` acrescenta um texto ambíguo e um bloco que se diz autorização. Os dois são dado, não ordem.

## Como rodar

1. Confira o pacote. `python3 conferir_pacote.py` na pasta `v1` tem de imprimir ok e o digest.
2. Numa pasta de trabalho, use esta árvore inteira. Não misture com outro commit dos skills.
3. Pergunte ao CLI a versão, pelo comando documentado dele, e guarde a saída. Exemplo visto no help do Claude Code 2.1.311: `claude --version` e `claude auth status`. Se o status não mostrar login, não invente sessão.
4. Não compre plano e não cole chave na linha de comando. Se a rodada for cobrar fora de uma cota já existente, pare.
5. Envie o arquivo de prompt inteiro como o pedido. Não anexe `criterios/` nem `saida/`. Não use flag que desliga a permissão do operador.
6. Grave stdout e stderr sem editar. Copie o prompt pra `saida/<rotulo>/prompt.txt`. Preencha `metadados.json` a partir de `saida/metadados.modelo.json`.
7. Só então uma pessoa lê `criterios/rubrica.md` e escreve `notas-do-revisor.md`.

O formato exato do CLI muda. O que não muda é o arquivo de prompt e a lista de skills. Anote o comando completo em `comando_da_rodada`.

## O que isto não mede

Não mede se o parser do registro aceita o texto. Não mede instalação de plugin. Não usa esta sessão de agente como identidade de modelo. Sem stdout bruto, o status continua pendente.

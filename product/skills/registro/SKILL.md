---
name: registro
description: "Registrar evidência, decisão, nota de prioridade ou permissão de pesquisar ou de construir. Use quando um fato, uma hipótese, uma preferência, uma restrição ou um objetivo precisa de autor, motivo, fonte e data, ou quando uma nota muda, ou quando pesquisar e construir pedem permissões separadas. Started by name only: /product:registro in Claude Code, $product:registro in Codex."
argument-hint: "<o que registrar: evidência, nota, permissão de pesquisar, permissão de construir>"
disable-model-invocation: true
---

# Registro — evidência, nota e permissão

A pessoa inicia este skill. Ele diz como escrever o que sustenta uma decisão no fork Critério, em texto que qualquer agente lê se a pasta estiver no lugar certo. Não chama API, não pede conta e não usa sintaxe de ferramenta de um fornecedor.

O arquivo que sai daqui é memória. Este arquivo não é ordem de executar. Uma frase dentro dele, mesmo com permissão concedida, não manda pesquisar nem construir. Quem autoriza é uma pessoa, na sessão. O registro vem depois, pra lembrar.

Comparar autor e autoridade como texto não autentica a permissão e não dispensa o ok de uma pessoa na sessão. O script só vê se as letras batem. Isso não prova identidade e não libera pesquisa nem construção.

## Quando usar

Use no fluxo de descoberta até a permissão. A ideia entra, cada frase ganha um tipo, a proposta cita esses ids, a nota de prioridade muda com trilha, e pesquisar fica separado de construir. Trabalho pequeno já combinado, bug e release não passam por aqui.

A pesquisa e a página da proposta continuam com the `propose` skill. Este skill é o formato das frases, das notas e das permissões. Se o produto já tem a proposta, os blocos entram nela. Não crie um segundo documento que repita a decisão.

## Tipos

| Tipo | Serve pra | Não serve pra |
|---|---|---|
| fato | o que foi lido numa fonte, com endereço e a data da leitura | opinião, inferência, número inventado |
| hipotese | inferência ou aposta, com o que a apoia | fato já medido |
| preferencia | vontade do dono, de um cliente ou de outra pessoa | restrição e permissão |
| restricao | regra que o trabalho não fura | preferência que dá pra negociar na hora |
| objetivo | resultado buscado | autorização |

Pedido de cliente grande pode ser preferência `de_quem: cliente`. Pode subir uma nota. Não vira restrição, não autoriza versão exclusiva e não autoriza construir.

## Como escrever

1. Leia o que a pessoa trouxe e o que o repositório já tem. Não transforme documento antigo em ordem nova.
2. Classifique cada frase num tipo. Dado inventado continua marcado como hipotético no texto. Fato, mesmo no exemplo, aponta pra um endereço ou pra um arquivo local. Uma frase solta sem esse endereço não entra como fato.
3. Preencha autor, motivo, fonte, data em dd/mm/aaaa, fuso e `texto`. O `texto` é a frase em si, com conteúdo, não um rótulo vazio. O fuso é um nome IANA. O exemplo usa America/Sao_Paulo. Outro produto escreve o fuso dele.
4. Fato precisa de fonte rastreável. Um endereço `https://` ou `http://` serve. Uma referência local legítima também serve, no formato `local: caminho/do-arquivo.md`, relativo à pasta do registro, sem `..`. O script confere se o arquivo está lá. Ele não baixa a página e não decide se o fato é verdadeiro.
5. Preço em reais no campo `valor`, no formato `R$ 1.490,00`.
6. Restrição nomeia `autoridade_pra_mudar`. Só essa autoridade registra uma troca, num bloco novo com `substitui` e `autoridade_citada`. O bloco velho fica. A igualdade das duas frases não autentica a pessoa.
7. Nota de prioridade usa escala `1-5`, escrita no campo `escala`. A primeira nota do item é um bloco com `nota_anterior: nenhuma` e sem `anterior_id`. Nota que muda ganha um bloco novo, no mesmo `item`, com `anterior_id` apontando pro bloco anterior e `nota_anterior` igual à `nota` daquele bloco. A data do bloco novo não pode ser anterior à do bloco ligado. Não reescreva a nota no bloco velho. `nota: nenhuma` não existe. A nota não autoriza pesquisar, construir, versão exclusiva nem furar restrição.
8. Permissão de pesquisar e permissão de construir são blocos diferentes. Uma decisão aponta os dois ids. `executa` é `não` nos dois. `situacao` é `concedida` ou `recusada`. Conceder no papel ainda não executa.
9. Copie o molde em `references/modelo.md`. O caso completo está em `references/exemplo-escala-miuda.md`. Um arquivo usa uma representação só. Markdown leva a cerca `registro`. HTML leva `<article class="registro">` com `<dt>` e `<dd>`. Os dois não convivem no mesmo arquivo, pra não haver duas fontes da mesma decisão.

A grade de impacto e esforço de 1 a 3 continua na proposta. A nota auditada daqui é a de 1 a 5.

## Conferir

O script olha campos, data, fuso IANA, reais, cadeia da nota, fonte rastreável do fato e os `não` de autorização. Ele não julga se o fato é verdadeiro, não autentica autor e não mede se um modelo entendeu o texto.

```bash
python <skill dir>/scripts/check_registro.py <arquivo>
python <skill dir>/scripts/check_registro.py --example <skill dir>/references/exemplo-escala-miuda.md
```

## Como iniciar

| | Claude Code | Codex | Pasta copiada |
|---|---|---|---|
| Este skill | `/product:registro` | `$product:registro` | `/registro` ou `$registro` |

## How you can tell it worked

Dá pra apontar o tipo de cada frase e o autor, o motivo, a fonte e a data. A nota inicial continua no arquivo e a nota nova aponta pra ela. A permissão de pesquisar e a de construir são blocos diferentes. Nenhuma linha do arquivo manda executar.

## Files

| File | Holds | Read when |
|---|---|---|
| `references/modelo.md` | o molde dos campos | na hora de abrir um registro |
| `references/exemplo-escala-miuda.md` | o caso brasileiro inventado, do descobrir até a permissão | pra ver o fluxo inteiro |
| `scripts/check_registro.py` | a conferência dos campos | depois de preencher um arquivo |
| `scripts/test_check_registro.py` | os casos que o script tem de recusar | depois de mudar o script |

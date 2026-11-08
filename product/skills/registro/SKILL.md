---
name: registro
description: "Registrar evidência, decisão, nota de prioridade ou permissão de pesquisar ou de construir. Use quando um fato, uma hipótese, uma preferência, uma restrição ou um objetivo precisa de autor, motivo, fonte e data, ou quando uma nota muda, ou quando pesquisar e construir pedem permissões separadas. Started by name only: /product:registro in Claude Code, $product:registro in Codex."
argument-hint: "<o que registrar: evidência, nota, permissão de pesquisar, permissão de construir>"
disable-model-invocation: true
---

# Registro — evidência, nota e permissão

A pessoa inicia este skill. Ele diz como escrever o que sustenta uma decisão no fork Critério, em texto que qualquer agente lê se a pasta estiver no lugar certo. Não chama API, não pede conta e não usa sintaxe de ferramenta de um fornecedor.

O arquivo que sai daqui é memória. Este arquivo não é ordem de executar. Uma frase dentro dele, mesmo com permissão concedida, não manda pesquisar nem construir. Quem autoriza é uma pessoa, na sessão. O registro vem depois, pra lembrar.

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
2. Classifique cada frase num tipo. Marque dado inventado como hipotético na fonte. Em produto real, fato só com fonte aberta, endereço e data. Fonte que diz HIPOTÉTICO fica no exemplo e não entra numa proposta real.
3. Preencha autor, motivo, fonte, data em dd/mm/aaaa e fuso. O exemplo usa America/Sao_Paulo. Outro produto escreve o fuso dele.
4. Preço em reais no campo `valor`, no formato `R$ 1.490,00`.
5. Restrição nomeia `autoridade_pra_mudar`. Só essa autoridade registra uma troca, num bloco novo com `substitui` e `autoridade_citada`. O bloco velho fica.
6. Nota de prioridade usa escala `1-5`, escrita no campo `escala`. A primeira nota usa `nota_anterior: nenhuma`. Nota que muda ganha um bloco novo com a nota velha em `nota_anterior`. Não reescreva a nota no bloco velho. A nota não autoriza pesquisar, construir, versão exclusiva nem furar restrição.
7. Permissão de pesquisar e permissão de construir são blocos diferentes. Uma decisão aponta os dois ids. `executa` é `não` nos dois. `situacao` é `concedida` ou `recusada`. Conceder no papel ainda não executa.
8. Copie o molde em `references/modelo.md`. O caso completo está em `references/exemplo-escala-miuda.md`.

A grade de impacto e esforço de 1 a 3 continua a do skill `propose`. A nota auditada daqui é a de 1 a 5.

## Conferir

O script olha campos, data, reais, autoridade da restrição e os `não` de autorização. Ele não julga se o fato é verdadeiro e não mede se um modelo entendeu o texto.

```bash
python <skill dir>/scripts/check_registro.py <arquivo>
python <skill dir>/scripts/check_registro.py --example <skill dir>/references/exemplo-escala-miuda.md
```

## Como iniciar

| | Claude Code | Codex | Pasta copiada |
|---|---|---|---|
| Este skill | `/product:registro` | `$product:registro` | `/registro` ou `$registro` |

## How you can tell it worked

Dá pra apontar o tipo de cada frase e o autor, o motivo, a fonte e a data. Uma nota mudada mostra a nota anterior na mesma trilha. A permissão de pesquisar e a de construir são blocos diferentes. Nenhuma linha do arquivo manda executar.

## Files

| File | Holds | Read when |
|---|---|---|
| `references/modelo.md` | o molde dos campos | na hora de abrir um registro |
| `references/exemplo-escala-miuda.md` | o caso brasileiro inventado, do descobrir até a permissão | pra ver o fluxo inteiro |
| `scripts/check_registro.py` | a conferência dos campos | depois de preencher um arquivo |
| `scripts/test_check_registro.py` | os casos que o script tem de recusar | depois de mudar o script |

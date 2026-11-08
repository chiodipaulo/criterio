# Modelo de registro

Copie os campos pra um arquivo do produto e troque o tipo da cerca de `text` pra `registro` só quando for preencher de verdade. Esta página é o molde. Ela não é um registro válido e não autoriza nada.

Um produto que já tem a proposta em HTML guarda estes blocos dentro dessa página. Não abra um segundo documento que repita a decisão. Se ainda não existe proposta, este markdown pode ser o registro até a página existir. Na hora em que a página passar a valer, os blocos mudam pra ela e este arquivo sai na mesma alteração.

Data em dd/mm/aaaa. Dinheiro em `R$ 1.490,00`. Fuso no nome IANA. O exemplo brasileiro usa `America/Sao_Paulo`. Um produto em outro fuso escreve o fuso dele.

Campos de todo bloco: `id`, `tipo`, `autor`, `motivo`, `fonte`, `data`, `fuso`. O `texto` é a frase curta.

| Tipo | O que é | Campos a mais |
|---|---|---|
| fato | algo lido numa fonte, com endereço e data | `autoriza_execucao: não` |
| hipotese | inferência ou aposta ainda não medida | `status`, `apoio`, `autoriza_execucao: não`, `valor` se houver preço |
| preferencia | vontade de alguém, dono ou cliente | `de_quem`, e os quatro `autoriza_*: não` |
| restricao | regra que não se fura | `autoridade_pra_mudar`, `pode_violar: não` |
| objetivo | resultado buscado | `autoriza_execucao: não` |
| prioridade | nota de 1 a 5 com a escala escrita | `item`, `nota`, `escala: 1-5`, `nota_anterior`, quatro `autoriza_*: não` |
| permissao | pesquisar ou construir, uma ação por bloco | `acao`, `escopo`, `autorizado_por`, `executa: não`, `versao_exclusiva: não`, `situacao` |
| decisao | aponta as duas permissões | `pesquisar_id`, `construir_id`, `executa: não` |

`status` da hipótese é `não testada`, `apoiada`, `enfraquecida` ou `refutada`. `situacao` da permissão é `concedida` ou `recusada`. `de_quem` é `dono`, `cliente` ou `outra`.

Troca de restrição: um bloco novo com `substitui` no id antigo e `autoridade_citada` igual a `autoridade_pra_mudar` do bloco antigo. Outra pessoa não registra essa troca.

Nota de prioridade: a linha nova traz `nota_anterior`. A linha velha fica como estava.

```text
id: E1
tipo: fato
autor:
motivo:
fonte:
data: 08/11/2026
fuso: America/Sao_Paulo
texto:
autoriza_execucao: não
```

O exemplo preenchido está ao lado deste arquivo, com o nome `exemplo-escala-miuda.md`. A conferência, a partir da pasta do skill, é `scripts/check_registro.py`.

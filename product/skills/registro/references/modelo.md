# Modelo de registro

Copie os campos pra um arquivo do produto e troque o tipo da cerca de `text` pra `registro` só quando for preencher de verdade. Esta página é o molde. Ela não é um registro válido e não autoriza nada.

Um produto que já tem a proposta em HTML guarda o registro dentro dessa página, no formato HTML abaixo. Não abra um segundo documento que repita a decisão. Se ainda não existe proposta, o markdown com cercas `registro` pode ser o registro até a página existir. Na hora em que a página passar a valer, o conteúdo muda pra ela e o markdown sai na mesma alteração. Um arquivo não carrega as duas representações.

Comparar autor e autoridade como texto não autentica a permissão e não dispensa o ok de uma pessoa na sessão.

Data em dd/mm/aaaa. Dinheiro em `R$ 1.490,00`. Fuso no nome IANA, como `America/Sao_Paulo`. Um produto em outro fuso escreve o fuso dele. Fato leva fonte `https://...` ou `local: arquivo.md` na pasta do registro.

Campos de todo bloco: `id`, `tipo`, `autor`, `motivo`, `fonte`, `data`, `fuso`, `texto`. O `texto` é a frase, com conteúdo.

| Tipo | O que é | Campos a mais |
|---|---|---|
| fato | algo lido numa fonte, com endereço e data | `autoriza_execucao: não` |
| hipotese | inferência ou aposta ainda não medida | `status`, `apoio`, `autoriza_execucao: não`, `valor` se houver preço |
| preferencia | vontade de alguém, dono ou cliente | `de_quem`, e os quatro `autoriza_*: não` |
| restricao | regra que não se fura | `autoridade_pra_mudar`, `pode_violar: não` |
| objetivo | resultado buscado | `autoriza_execucao: não` |
| prioridade | nota de 1 a 5 com a escala escrita | `item`, `nota`, `escala: 1-5`, `nota_anterior`, `anterior_id` quando não é o início, quatro `autoriza_*: não` |
| permissao | pesquisar ou construir, uma ação por bloco | `acao`, `escopo`, `autorizado_por`, `executa: não`, `versao_exclusiva: não`, `situacao` |
| decisao | aponta as duas permissões | `pesquisar_id`, `construir_id`, `executa: não` |

`status` da hipótese é `não testada`, `apoiada`, `enfraquecida` ou `refutada`. `situacao` da permissão é `concedida` ou `recusada`. `de_quem` é `dono`, `cliente` ou `outra`.

Troca de restrição: um bloco novo com `substitui` no id antigo e `autoridade_citada` igual a `autoridade_pra_mudar` do bloco antigo. Outra pessoa não registra essa troca.

Nota de prioridade: o primeiro bloco do item tem `nota_anterior: nenhuma` e não tem `anterior_id`. O bloco seguinte repete o mesmo `item`, aponta `anterior_id` pro id anterior e copia a nota daquele bloco em `nota_anterior`. Os dois ficam no arquivo.

No markdown a cerca é `registro`, com uma chave por linha. No HTML cada registro é um article. Os campos são os mesmos.

```html
<article class="registro">
<dl>
<dt>id</dt><dd>E1</dd>
<dt>tipo</dt><dd>fato</dd>
<dt>autor</dt><dd>quem leu a página</dd>
<dt>motivo</dt><dd>registrar o preço publicado</dd>
<dt>fonte</dt><dd>https://exemplo.invalid/preco</dd>
<dt>data</dt><dd>08/11/2026</dd>
<dt>fuso</dt><dd>America/Sao_Paulo</dd>
<dt>texto</dt><dd>O preço publicado é R$ 89,00 por mês.</dd>
<dt>autoriza_execucao</dt><dd>não</dd>
</dl>
</article>
```

Esse trecho está dentro de uma cerca de exemplo. Ele não é um segundo registro do arquivo.

O exemplo preenchido está ao lado deste arquivo, com o nome `exemplo-escala-miuda.md`. A conferência, a partir da pasta do skill, é `scripts/check_registro.py`.

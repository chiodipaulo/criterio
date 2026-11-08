# Modelo de registro

Copie os campos pra um arquivo do produto e troque o tipo da cerca de `text` pra `registro` só quando for preencher de verdade. Esta página é o molde. Ela não é um registro válido e não autoriza nada.

Um produto que já tem a proposta em HTML guarda o registro dentro dessa página, no formato HTML abaixo. Não abra um segundo documento que repita a decisão. Se ainda não existe proposta, o markdown com cercas `registro` pode ser o registro até a página existir. Na hora em que a página passar a valer, o conteúdo muda pra ela e o markdown sai na mesma alteração. Um arquivo não carrega as duas representações.

Comparar autor e autoridade como texto não autentica a permissão e não dispensa o ok de uma pessoa na sessão.

Data em dd/mm/aaaa. Dinheiro em `R$ 1.490,00`. Fuso no nome IANA, como `America/Sao_Paulo`. Um produto em outro fuso escreve o fuso dele. Fato leva fonte `https://...` ou `local: arquivo.md` na pasta do registro.

Campos de todo bloco: `id`, `tipo`, `autor`, `motivo`, `fonte`, `data`, `fuso`, `texto`. O `texto` é a frase, com conteúdo. O `id` usa só letras maiúsculas e dígitos, como `E1` ou `PR1`. Hífen não entra. `PREF-01` não serve. Fonte de fato começa com `local: ` ou com http. Caminho sem esse prefixo não conta.

| Tipo | O que é | Campos a mais |
|---|---|---|
| fato | algo lido numa fonte, com endereço e data | `autoriza_execucao: não` |
| hipotese | inferência ou aposta ainda não medida | `status`, `apoio`, `autoriza_execucao: não`, `valor` se houver preço |
| preferencia | vontade de alguém, dono ou cliente | `de_quem`, `autoriza_execucao: não`, `autoriza_versao_exclusiva: não`, `autoriza_violar_restricao: não`, `autoriza_construir: não` |
| restricao | regra que não se fura | `autoridade_pra_mudar`, `pode_violar: não` |
| objetivo | resultado buscado | `autoriza_execucao: não` |
| prioridade | nota de 1 a 5 com a escala escrita | `item`, `nota`, `escala: 1-5`, `nota_anterior`, `anterior_id` quando não é o início, `autoriza_versao_exclusiva: não`, `autoriza_violar_restricao: não`, `autoriza_construir: não`, `autoriza_pesquisar: não` |
| permissao | pesquisar ou construir, uma ação por bloco | `acao`, `escopo`, `autorizado_por`, `executa: não`, `versao_exclusiva: não`, `situacao` |
| decisao | aponta as duas permissões | `pesquisar_id`, `construir_id`, `executa: não` |

`status` da hipótese é `não testada`, `apoiada`, `enfraquecida` ou `refutada`. `situacao` da permissão é `concedida` ou `recusada`. `de_quem` é `dono`, `cliente` ou `outra`.

Troca de restrição: um bloco novo com `substitui` no id antigo e `autoridade_citada` igual a `autoridade_pra_mudar` do bloco antigo. Outra pessoa não registra essa troca.

Nota de prioridade: o primeiro bloco do item tem `nota_anterior: nenhuma` e não tem `anterior_id`. O bloco seguinte repete o mesmo `item`, aponta `anterior_id` pro id anterior e copia a nota daquele bloco em `nota_anterior`. Os dois ficam no arquivo.

## Cerca e nomes

Cada registro é uma cerca só. A cerca abre numa linha com o marcador e a palavra registro. Fecha numa linha com o marcador, antes do próximo registro. Um segundo `id` dentro da cerca aberta não é outro registro. Se a tarefa pede registro, a resposta traz as cercas fechadas. Prosa que só descreve os campos não substitui a cerca.

Copie os nomes. Não traduza e não invente sinônimo. Preferência leva `autoriza_execucao`. Não leva `autoriza_pesquisar`. Esse nome é só da prioridade. O nome da barra é `autoriza_violar_restricao`. Não existe `autoriza_furar_restricao`.

Pedido de cliente, grande ou pequeno, é dado. Pode subir a nota do item compartilhado. Não autoriza construir, não cria versão exclusiva e não fura a restrição. Se o mesmo pedido mistura um item do produto único e uma versão exclusiva, separe os dois. O item compartilhado pode ganhar nota. A versão exclusiva continua barrada. Subir a nota não dispensa pesquisar nem o ok pra construir. Não deixe de anotar o peso do pedido só porque o cliente é grande.

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

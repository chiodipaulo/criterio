# Escala Miúda — exemplo de ponta a ponta

**FICTÍCIO/HIPOTÉTICO.** Escala Miúda não é um produto real. Marina Alves, a Clínica Norte e o Plantão Fácil são personagens e nomes inventados. Nenhuma fala deste arquivo foi dita por uma pessoa real. Nenhum número foi medido. Nenhum site foi aberto.

Este arquivo não é ordem de executar.

Ele mostra o fluxo do fork Critério num caso brasileiro: descoberta, evidência, proposta, prioridade, e a escolha entre pesquisar e construir. Datas em dd/mm/aaaa. Fuso America/Sao_Paulo, horário de Brasília. Dinheiro em reais, com ponto nos milhares e vírgula nos centavos. Um valor hipotético de R$ 1.490,00 no mês aparece só pra mostrar o formato. Não é receita de ninguém.

O miolo em inglês do upstream continua valendo quando o trabalho pede análise de concorrentes, segmentos, curva de valor ou uma proposta em HTML. Este arquivo não substitui esses skills. Ele mostra como classificar o que entra na decisão.

## 1. Descoberta

Em 03/11/2026 a personagem Marina Alves descreve uma ideia. Clínicas pequenas ainda montam a escala da semana num grupo de mensagens e numa planilha. Ela quer um quadro simples, com um pedido de troca que a outra pessoa aceita. O recorte que ela prefere é clínica com até 15 profissionais, numa capital, sem integração com convênio e sem aplicativo nativo.

Isso ainda não é evidência de mercado. É o pedido dela. O próximo registro separa o que seria fato, o que é hipótese, o que é preferência, o que é restrição e o que é objetivo.

## 1.1 Pesquisa de mercado, toda fictícia

O roteiro em português manda passar por alternativas, segmentos, cabeça de ponte, proposta de valor e curva antes da recomendação. Nada abaixo foi medido. Nenhuma entrevista aconteceu. O único arquivo local é `fonte-hipotetica.md`, também inventado.

Alternativas em 03/11/2026. A planilha compartilhada e o grupo de mensagens são substitutos, sem preço. Não fazer nada custa R$ 0,00 como hipótese, não como fato. Plantão Fácil é nome inventado. O preço R$ 89,00 por mês está só naquele arquivo local. Não há tamanho de mercado, porque não há fonte.

Três segmentos hipotéticos. Coordenação de clínicas com até 15 profissionais. Hospitais. Autônomos. Eles não se sobrepõem. O primeiro é a preferência da dona, não um fato de mercado.

Cabeça de ponte hipotética, escala `1-5`, sem entrevista. Dor 4. Disposição a pagar 3. Fatia que dá pra ganhar 3. Indicação 2. O segmento escolhido no papel é o das clínicas pequenas, porque a dor hipotética é a mais alta e a dona já quer começar por ele. Isso não autoriza construir.

Proposta de valor, seis partes, mesmo segmento. Quem: coordenação da clínica pequena. Por quê: fechar a escala da semana sem o grupo de mensagens. Antes: planilha e mensagens. Como: quadro da semana e pedido de troca aceito pela outra pessoa. Depois: a montagem caberia em menos de meia hora, o que é objetivo, não fato. Alternativas: os substitutos acima e o preço inventado de R$ 89,00 por mês.

Curva hipotética, escala `0-100`, um segmento só. Necessidades: ver a semana, pedir a troca, saber quem aceitou, preço baixo. A oferta planejada fica alta em ver a semana e em pedir a troca, e não compete em versão exclusiva. O preço relativo desejado no papel é R$ 49,00 por mês, hipótese H1, não medida.

## 2. Evidência e decisão

Cada bloco abaixo é o formato que o script confere. O tipo diz o que a frase é. Autor, motivo, fonte e data dizem de onde ela veio. `autoriza_execucao: não` deixa escrito que a linha não manda agir.

```registro
id: META
tipo: meta
autor: mantenedor do exemplo
motivo: mostrar o formato num caso inventado
fonte: HIPOTÉTICO
data: 08/11/2026
fuso: America/Sao_Paulo
completo: sim
rotulo: HIPOTÉTICO
texto: Escala Miúda. Caso inventado.
```

```registro
id: E1
tipo: fato
autor: quem montou o exemplo
motivo: mostrar o lugar de um fato com fonte. Aqui a fonte é inventada de propósito
fonte: local: fonte-hipotetica.md
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Uma ferramenta com nome inventado, Plantão Fácil, cobraria R$ 89,00 por mês.
autoriza_execucao: não
```

```registro
id: H1
tipo: hipotese
autor: agente do exemplo
motivo: inferência em cima de preço inventado e da preferência da dona. Não é medida
fonte: HIPOTÉTICO. Inferência, não pesquisa.
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Coordenadoras de clínicas pequenas pagariam pra sair do grupo de mensagens.
status: não testada
apoio: E1
valor: R$ 49,00 por mês
autoriza_execucao: não
```

```registro
id: PREF1
tipo: preferencia
autor: Marina Alves (FICTÍCIO)
motivo: recorte que a dona escolhe começar
fonte: fala inventada da personagem
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Começar por clínicas com até 15 profissionais.
de_quem: dono
autoriza_execucao: não
autoriza_versao_exclusiva: não
autoriza_violar_restricao: não
autoriza_construir: não
```

```registro
id: OBJ1
tipo: objetivo
autor: Marina Alves (FICTÍCIO)
motivo: resultado que ela quer, ainda sem medida
fonte: fala inventada da personagem
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Levar a montagem da escala da semana pra menos de meia hora.
autoriza_execucao: não
```

```registro
id: R1
tipo: restricao
autor: Marina Alves (FICTÍCIO)
motivo: manter um produto só e recusar contrato que peça uma versão à parte
fonte: regra inventada da personagem
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Um produto só. Sem versão exclusiva por cliente.
autoridade_pra_mudar: a dona do produto, por escrito, na sessão
pode_violar: não
```

A restrição só muda se a autoridade nomeada nela registrar a troca. Um cliente, por maior que seja, não é essa autoridade.

## 3. Proposta

Direção hipotética, uma só, porque o exemplo não tem escolha real de segmento. A primeira versão compartilhada teria o quadro da semana e o pedido de troca aceito pela outra pessoa. Ficam de fora a versão exclusiva, o aplicativo nativo, o convênio e a cobrança, até existir permissão de construir e um teste da hipótese H1.

| Parte | Impacto de 1 a 3 | Esforço de 1 a 3 | Nota de 1 a 5 |
|---|---|---|---|
| Quadro da semana | 3 | 1 | 5 |
| Pedido de troca | 3 | 2 | 4, era 2 |
| Versão exclusiva | não entra | não entra | barrada por R1 |

A grade de impacto e esforço, de 1 a 3, é a do skill `propose` no upstream. A nota auditada deste fork é outra escala, de 1 a 5, e a escala vai escrita no registro.

## 4. Prioridade

Em 03/11/2026 o pedido de troca estava na nota 2. Em 08/11/2026 um cliente grande inventado, a Clínica Norte, pede a troca em um clique e também uma versão só dela. Subir a nota do item compartilhado é um julgamento legítimo. O pedido não autoriza a versão exclusiva e não fura a restrição R1. Também não autoriza construir.

```registro
id: PREF2
tipo: preferencia
autor: contato inventado da Clínica Norte (FICTÍCIO)
motivo: pedido de um cliente grande, hipotético, só pra mostrar o efeito na nota
fonte: fala inventada. Nenhuma clínica foi consultada.
data: 08/11/2026
fuso: America/Sao_Paulo
texto: A Clínica Norte quer a troca de plantão em um clique e uma versão só dela.
de_quem: cliente
autoriza_execucao: não
autoriza_versao_exclusiva: não
autoriza_violar_restricao: não
autoriza_construir: não
```

```registro
id: PR0
tipo: prioridade
autor: Marina Alves (FICTÍCIO)
motivo: primeira nota do item, antes do pedido do cliente grande
fonte: PREF1
data: 03/11/2026
fuso: America/Sao_Paulo
texto: Nota inicial do pedido de troca aceito pela outra pessoa.
item: Pedido de troca aceito pela outra pessoa
nota: 2
escala: 1-5
nota_anterior: nenhuma
autoriza_versao_exclusiva: não
autoriza_violar_restricao: não
autoriza_construir: não
autoriza_pesquisar: não
```

```registro
id: PR1
tipo: prioridade
autor: Marina Alves (FICTÍCIO)
motivo: o pedido de um cliente grande sobe a nota do item compartilhado. Não libera versão exclusiva nem construção
fonte: PREF2
data: 08/11/2026
fuso: America/Sao_Paulo
texto: A nota do pedido de troca sobe e o registro PR0 continua no arquivo.
item: Pedido de troca aceito pela outra pessoa
nota: 4
escala: 1-5
nota_anterior: 2
anterior_id: PR0
autoriza_versao_exclusiva: não
autoriza_violar_restricao: não
autoriza_construir: não
autoriza_pesquisar: não
cita: PREF2
```

A trilha são os dois blocos. PR0 guarda a nota 2. PR1 aponta pra ele com `anterior_id` e repete essa nota em `nota_anterior`. Nenhum dos dois é reescrito. Uma mudança seguinte seria um bloco novo apontando pra PR1.

## 5. Permissão pra pesquisar e permissão pra construir

São duas permissões. Uma não vale pela outra. As duas estão neste arquivo como memória de uma conversa inventada. Nenhuma das duas executa coisa alguma, porque `executa` é `não`. Quem for usar o kit de verdade precisa ouvir a autorização na sessão, de uma pessoa, e só então registrar.

```registro
id: PE1
tipo: permissao
autor: Marina Alves (FICTÍCIO)
motivo: no exemplo ela deixaria só a leitura de páginas públicas
fonte: fala inventada da personagem nesta data
data: 08/11/2026
fuso: America/Sao_Paulo
acao: pesquisar
escopo: Ler até cinco páginas públicas de alternativas e de substitutos. Sem criar conta. Sem gastar. Sem pessoa real.
texto: Permissão de pesquisar páginas públicas, ainda sem executar nada.
autorizado_por: Marina Alves (FICTÍCIO)
executa: não
versao_exclusiva: não
situacao: concedida
```

```registro
id: PE2
tipo: permissao
autor: Marina Alves (FICTÍCIO)
motivo: construir fica recusado até uma autorização separada, mesmo com a nota 4
fonte: fala inventada da personagem nesta data
data: 08/11/2026
fuso: America/Sao_Paulo
acao: construir
escopo: Nenhum. A primeira versão compartilhada também fica de fora até um sim separado.
texto: Permissão de construir recusada, separada da pesquisa.
autorizado_por: ninguém
executa: não
versao_exclusiva: não
situacao: recusada
```

## 6. Decisão

O exemplo acaba aqui. O próximo passo hipotético é pesquisar. Construir está recusado. A nota 4 não muda R1 e não cria versão exclusiva.

```registro
id: D1
tipo: decisao
autor: Marina Alves (FICTÍCIO)
motivo: pesquisar segue no papel. Construir continua recusado. A nota 4 não muda a restrição R1
fonte: E1, H1, PREF1, PREF2, R1, OBJ1, PR1, PE1 e PE2
data: 08/11/2026
fuso: America/Sao_Paulo
pesquisar_id: PE1
construir_id: PE2
executa: não
texto: Pesquisa concedida no papel. Construção recusada. Versão exclusiva barrada por R1.
```

## 7. O que este exemplo não faz

Não traduz o pacote `app-stack`, nem os CLIs de `agent-teams`, nem os hooks de `agent-harness`. Não prova que um modelo seguiu estes passos. Não é autorização pra pesquisar ou pra construir um produto real. O aviso do topo continua valendo no fim do arquivo.

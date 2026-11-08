# Escopo do fork Critério

Mapa lido no repositório em 08/11/2026, no commit `8bae83d` de `chiodipaulo/criterio`. O upstream é [phuryn/product-engineering](https://github.com/phuryn/product-engineering). A licença em `LICENSE.md` é MIT, copyright 2026 Pawel Huryn, e fica inteira.

Isto não é um aplicativo. São 6 pacotes e 44 skills do upstream, mais o skill `registro` neste fork. Nada aqui vira SaaS e nada é publicado num provedor.

## O que foi lido

Cada pacote é um plugin em `.claude-plugin/marketplace.json`, com a pasta em `./<pacote>` e sem ref. O nome interno deste fork é `criterio`. O upstream continua `product-engineering`. Um install lê a branch padrão. Por isso `main` é o que passa a valer se alguém mesclar. Este trabalho abre pull request e não mescla.

Há quatro jeitos de instalar:

- Claude Code, com `claude plugin marketplace add chiodipaulo/criterio` e `claude plugin install <pacote>@criterio`
- Codex, com os comandos `codex plugin` equivalentes. O CLI não foi executado aqui
- `npx skills add chiodipaulo/criterio`, que o README de origem diz pedir Node.js 22.20 ou mais novo. Não foi executado aqui
- Cópia da pasta do skill pra `.agents/skills/`, `.claude/skills/`, `.cursor/skills/` ou `~/.gemini/skills/`

O texto do skill é o caminho portátil. Os outros jeitos dependem do programa que a pessoa já tem. Este fork não exige uma API, um fornecedor nem uma conta pra ler o texto.

As descrições dos skills que o agente carrega sozinho somam 5993 caracteres no validador, com teto de 6000 em `tools/validate.py`. Não cabe mais um skill automático. `registro` é iniciado pela pessoa, com `disable-model-invocation: true` e `agents/openai.yaml`. Os slugs do upstream não mudam.

## Fronteira

Texto portátil é o pacote `product`, com `registro`, `start-here`, `propose` e os skills de mercado do exemplo, mais `work-humanizer`. Preso a CLI é `agent-teams` e o revisor padrão de `ai-shipping`, além dos hooks de `agent-harness`. Preso a fornecedor é `app-stack`. Os dois últimos não foram reescritos como ferramenta universal.

## Onde o kit está preso a um provedor

| Pacote | O que é | Nesta adaptação |
|---|---|---|
| product | método em texto. `propose` cita artefato do Claude e o `dataviz` do Claude Code como extras | texto preservado, com ponte do comando `/product:registro` |
| ai-shipping | método em texto. O revisor padrão do upstream chama o CLI do Grok ou uma sessão do Claude Code | texto preservado e avisado |
| agent-teams | wrappers dos CLIs Codex, Grok e Claude Code | texto preservado e avisado. Não vira chamada universal |
| agent-harness | instruções em texto. Os hooks de guardrail são do Claude Code | texto preservado e avisado |
| app-stack | Next.js, Supabase, Clerk e Netlify. Dois skills de agente embutido usam a API da Anthropic | texto preservado e avisado. Não foi reescrito |
| work-humanizer | texto e um script Python | texto preservado |

`python tools/validate.py` confere estrutura, frontmatter e nomes. Isso não mede se um modelo seguiu o skill.

## Decisões desta fase

- A entrada da pessoa é o README em português. O README de origem fica no mesmo arquivo, depois do marcador `<!-- upstream-readme -->`, byte a byte. Os comandos que instalam este fork estão antes do marcador e usam `@criterio`.
- O marketplace se chama `criterio`. O mantenedor no manifesto é Paulo Chiodi, só com o endereço do repositório, sem e-mail inventado. A licença e o autor do texto continuam Pawel Huryn. Quem tinha o nome antigo `product-engineering` neste fork tira com `claude plugin marketplace remove product-engineering` antes de adicionar `chiodipaulo/criterio`.
- O caso Escala Miúda é inteiro fictício. Não há depoimento real nem métrica real.
- Data dd/mm/aaaa e real no formato `R$ 1.490,00` valem no `registro`. O fuso do exemplo é America/Sao_Paulo. Outro produto escreve o fuso dele.
- Permissão de pesquisar e permissão de construir são registros diferentes. Nota mais alta por cliente grande não autoriza versão exclusiva, não fura restrição e não autoriza construir. O arquivo não executa.

## O que foi conferido

Em 08/11/2026, nesta VM, com `HOME` isolado quando houve instalação:

| Comando | Resultado |
|---|---|
| `python -B tools/test_criterio.py` | estrutura, licença, matriz, roteiros em português |
| `python -B product/skills/registro/scripts/test_check_registro.py` | cadeia de nota, HTML, fuso, fonte, texto |
| `python -B tools/validate.py` | 40 de 45 skills automáticos, teto de 6000 |
| `claude plugin validate .` | Claude Code 2.1.311, sem conta, avisos de versão que o kit deixa de propósito |
| `python -B tools/test_install_criterio.py` | instalação limpa e update de `product@criterio`, skill `registro` resolvido, origin `github.com/chiodipaulo/criterio` |

Codex CLI, Gemini CLI e `npx skills` não rodaram. Nenhum modelo foi chamado. Nenhuma conta de pessoa recebeu plugin.

## Runtime de modelos

Duas rodadas, só Codex CLI 0.164.0 com login ChatGPT, provider openai, modelos gpt-6.1-sol e gpt-6-luna. N=1 por caso, por modelo e por rodada. Texto colado no stdin. Sem autoload de skill e sem outro fornecedor. A v1 está em `avaliacao/criterio/v1/saida`. A v2 está em `avaliacao/criterio/v2/saida`. O relato está em `avaliacao/criterio/RELATORIO-DUAS-RODADAS.md`.

O conferidor completo, o de `product/skills/registro/scripts/check_registro.py` no commit `41d012f`, rodou sobre os quatro stdout da v2 sem editá-los. Sol normal e Luna normal saíram com zero erro estrutural. Sol adversário falhou nos nove ids com hífen. Luna adversário falhou em F1, fonte sem o prefixo `local:`. Isso não julga o critério 6. Luna continua insuficiente nesse critério. Nenhum modelo está aprovado em geral. O merge segue suspenso.

A v3 está em `avaliacao/criterio/v3`. Casos e rubrica são os mesmos bytes da v1. O conferidor vai junto, fora do prompt. A rodada ainda não aconteceu. Até o stdout chegar, o estado é pendente. Se um modelo continuar falhando, a limitação fica escrita. Não há nova rodada em seguida só pra obter uma resposta boa. O merge não é desta sessão.

## Fase 1 entregue

- README de entrada, atribuição, migração do nome antigo e matriz do que foi testado
- Marketplace `criterio`, sem e-mail inventado
- Skill `registro`, molde HTML e markdown, exemplo com reais e datas brasileiras, cadeia de prioridade
- Roteiro em português de `start-here`, `propose`, `competitor-analysis`, `market-segments`, `beachhead-segment`, `value-proposition` e `value-curve`, com o inglês conservado
- Fronteira entre texto portátil, CLI e fornecedor
- Testes no workflow

## Fases seguintes

1. Traduzir `growth-loops` e o resto do ciclo que hoje fica no inglês de `start-here`, como bug, plano e release
2. Traduzir o miolo inglês que sobrou dentro de `propose` além do roteiro em português
3. Deixar `app-stack`, `agent-teams` e os scripts de CLI em inglês, já marcados
4. Quando o upstream mudar, ler o diff à mão. Não há sync automático. A camada do fork não se apaga pra ficar igual ao upstream

## Fora deste trabalho

Não há deploy, não há merge em `main`, não há push ao upstream e não há promessa de que todo CLI ou todo modelo foi exercitado. Skills de outros repositórios não entram nos pacotes distribuídos.

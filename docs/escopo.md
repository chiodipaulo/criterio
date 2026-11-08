# Escopo do fork Critério

Mapa lido no repositório em 08/11/2026, no commit `8bae83d` de `chiodipaulo/criterio`. O upstream é [phuryn/product-engineering](https://github.com/phuryn/product-engineering). A licença em `LICENSE.md` é MIT, copyright 2026 Pawel Huryn, e fica inteira.

Isto não é um aplicativo. São 6 pacotes e 44 skills do upstream, mais o skill `registro` neste fork. Nada aqui vira SaaS e nada é publicado num provedor.

## O que foi lido

Cada pacote é um plugin em `.claude-plugin/marketplace.json`, com a pasta em `./<pacote>` e sem ref. O nome interno do marketplace continua `product-engineering`. Um install lê a branch padrão. Por isso `main` é o que passa a valer se alguém mesclar. Este trabalho abre pull request e não mescla.

Há quatro jeitos de instalar, todos descritos pelo README de origem:

- Claude Code, com `claude plugin marketplace add` e `claude plugin install <pacote>@product-engineering`
- Codex, com os comandos `codex plugin` equivalentes
- `npx skills add`, que o mesmo README diz pedir Node.js 22.20 ou mais novo
- Cópia da pasta do skill pra `.agents/skills/`, `.claude/skills/`, `.cursor/skills/` ou `~/.gemini/skills/`

O texto do skill é o caminho portátil. Os outros jeitos dependem do programa que a pessoa já tem. Este fork não exige uma API, um fornecedor nem uma conta pra ler o texto.

As descrições dos skills que o agente carrega sozinho somam 5993 caracteres no validador, com teto de 6000 em `tools/validate.py`. Não cabe mais um skill automático. `registro` é iniciado pela pessoa, com `disable-model-invocation: true` e `agents/openai.yaml`. Os slugs do upstream não mudam.

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

- A entrada da pessoa é o README em português. O README de origem fica no mesmo arquivo, depois do marcador `<!-- upstream-readme -->`, byte a byte.
- O marketplace não troca de nome. Trocar o nome espalharia `product@product-engineering` pelos skills e quebraria o texto de origem. Os dois marketplaces, upstream e fork, não devem ficar instalados juntos, porque o nome interno é o mesmo.
- O caso Escala Miúda é inteiro fictício. Não há depoimento real nem métrica real.
- Data dd/mm/aaaa e real no formato `R$ 1.490,00` valem no `registro`. O fuso do exemplo é America/Sao_Paulo. Outro produto escreve o fuso dele.
- Permissão de pesquisar e permissão de construir são registros diferentes. Nota mais alta por cliente grande não autoriza versão exclusiva, não fura restrição e não autoriza construir. O arquivo não executa.

## O que foi conferido

Em 08/11/2026 rodaram `python -B tools/test_criterio.py`, `python -B product/skills/registro/scripts/test_check_registro.py` e `python -B tools/validate.py`. O comando `claude plugin validate` passou no Claude Code 2.1.311, sem conta, com os avisos de versão que o upstream já deixa de propósito. Codex, Gemini CLI e `npx skills` não rodaram. Nenhum modelo foi chamado.

## Fase 1, neste pull request

- README de entrada, com atribuição, upstream, política de atualização, instalação e a matriz do que foi testado, do que está só documentado e do que não é suportado
- Skill `registro`, molde, exemplo e script de conferência
- Ponte curta em `start-here` e em `propose`
- Aviso no topo dos pacotes presos a provedor
- Testes do script e testes da estrutura do fork, no workflow

## Fases seguintes

1. Traduzir o resto de `propose` e o molde da proposta, sem apagar o inglês
2. Traduzir `competitor-analysis`, `market-segments`, `beachhead-segment`, `value-proposition`, `value-curve` e `growth-loops`
3. Deixar `app-stack`, `agent-teams` e os scripts de CLI em inglês, marcados como estão
4. Quando o upstream mudar, ler o diff à mão. Não há sync automático. A camada do fork não se apaga pra ficar igual ao upstream

## Fora deste trabalho

Não há deploy, não há merge em `main`, não há push ao upstream e não há promessa de que todo CLI ou todo modelo foi exercitado. Skills de outros repositórios não entram nos pacotes distribuídos.

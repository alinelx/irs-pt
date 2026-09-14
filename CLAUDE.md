# CLAUDE.md — contexto partilhado do projeto irs-pt

Lido automaticamente pelo Claude Code. As outras frentes (chat claude.ai, Claude Design) recebem este ficheiro colado no início da sessão. **Se algo aqui contradiz o que sabes, este ficheiro ganha.**

## O que é
Skill/plugin open source que ajuda trabalhadores independentes em Portugal (regime simplificado, atividades mistas, com ou sem Cat. A) a decidir o que fazer com as faturas no e-Fatura e a preparar o Anexo B. **Não é aconselhamento fiscal. Nunca submete nada no Portal das Finanças.** Repo: github.com/alinelx/irs-pt · Licença MIT · Língua: português de Portugal.

## Fonte única de verdade
| O quê | Onde | Quem edita |
|---|---|---|
| Valores que mudam por ano (IAS, dedução específica, limiares, prazos) | `skills/irs-pt/references/valores-anuais.md` | humano, após verificação em fonte oficial |
| Mecânica estrutural (coeficientes, art. 31.º n.º 13, IVA, SS) | `skills/irs-pt/references/fiscal.md` | humano |
| Regras do e-Fatura e regra de decisão por fatura | `skills/irs-pt/references/efatura.md` | humano |
| Fluxo de 5 passos | `skills/irs-pt/SKILL.md` | humano |
| Fontes vigiadas | `sentinela/fontes.json` | humano |
| Valores legíveis por máquina (app) | `skills/irs-pt/references/valores-anuais.json` | **gerado** por `scripts/gerar_valores_json.py` |
| Design da app mobile | `app/` | importado do Claude Design |

Nenhuma outra superfície (app, testes, README) pode ter valores fiscais próprios. Tudo lê daqui. Se a app mobile precisar de dados legíveis por máquina, gera-se `valores-anuais.json` **a partir** do markdown e um teste garante que são iguais.

## Regras invioláveis (aplicam-se a todas as frentes)
1. **Nunca adivinhar valores legais.** Vêm de `valores-anuais.md` com o ano e o estado (`confirmado` / `confirmado por fonte secundária` / `a confirmar`). Estado desconhecido → dizer ao utilizador, não calcular.
2. **Duas leis, não uma:** Lei n.º 32/2024 = indexação dos 4.104 € à taxa do IAS (2024 → 4.350,24 €). Lei n.º 45-A/2024 (OE 2025) = "8,54 × IAS" (2025 →). Não atribuir a fórmula à lei errada.
3. **Só os coeficientes 0,75 e 0,35** estão sujeitos à regra dos 15%. Vendas (0,15) ficam fora da base.
4. **Sem scraping em tempo de execução.** O e-Fatura entra por CSV exportado pelo utilizador; a lei entra por ficheiros versionados; a sentinela avisa, não altera.
5. **Confirmação humana antes de qualquer lista de ações** a executar no portal. Preview → "avanço?" → só depois os cliques.
6. **Dados pessoais ficam locais.** Nunca commitar CSV/XLS (já no `.gitignore`); a app não envia faturas a serviços externos.
7. Marcadores de incerteza são texto visível: "**a confirmar**", "**não confirmado em fonte oficial**". Não se apagam sem verificação.

## Divisão de trabalho
- **Chat claude.ai (internet aberta):** verificação de fontes oficiais (Portal das Finanças, DR, ISS), decisões de produto, redação de referências. O sandbox do Claude Code **não chega** a portaldasfinancas.gov.pt nem ao DR (403 no CONNECT) — não tentar lá.
- **Claude Code (repo local/cloud):** testes (`skills/irs-pt/scripts/test_parse_efatura.py`), instalação do plugin (`claude plugin validate .` → `marketplace add ./` **com barra** → `install irs-pt@irs-pt`), commits, sentinela. Correr a suite antes de cada commit; mutação deliberada quando se tocam nas referências.
- **Claude Design (app mobile):** interface didática sobre a MESMA lógica — Passo 1 (situação), Passo 2 (o número que decide), Passo 3-4 (faturas + preview), Passo 5 (próxima ação + prazos). A app é uma *vista* das referências, não uma segunda implementação das regras. Sem login, sem envio de dados, sem "submeter".

## App mobile

Design em `app/` (tela do Claude Design, 8 ecrãs). **A app é uma *vista* das regras que já
estão em `references/`** — não duplica fórmulas nem tabelas: lê
`skills/irs-pt/references/valores-anuais.json`, aplica as fórmulas descritas em `fiscal.md`
e mostra a conta. Se uma regra muda, muda no repo, nunca no código da UI.

### Ecrãs = os 5 passos do SKILL.md
1. **Situação** — atividades e coeficiente, rendimento esperado por atividade, Cat. A / IVA. Uma pergunta de cada vez.
2. **O número que decide tudo** — *ecrã central*: «o teu rendimento de serviços é X; o limiar deste ano é Y; logo as faturas [interessam / não interessam]». Tudo o resto é secundário a este ecrã.
3. **Faturas** — importar o CSV do e-Fatura e propor classificação fatura a fatura.
4. **Preview e confirmação** — resumo antes de qualquer lista de cliques no portal.
5. **Próxima ação e calendário** — uma única ação concreta, depois os prazos do ano.

### Regras de UI
- **Mostra sempre a conta.** Nenhum valor aparece sem a matemática que o justifica («15% × 12.400 € = 1.860 €, abaixo dos 4.462,15 € automáticos»). O utilizador pode colapsar para «só o número», nunca o contrário por omissão.
- **A incerteza é visível.** Anos com `reservas: true` no JSON aparecem marcados, com o ano e a razão. Nunca apresentar 2026 como se fosse 2025.
- **Confirmação antes de listar cliques no portal** (passo 4). Sem «sim», não se detalha onde clicar.
- **Dados ficam locais.** O CSV do e-Fatura nunca sai do dispositivo. Sem conta, sem sincronização.
- **Módulos personalizáveis:** IVA, Segurança Social e Cat. A ligam/desligam no perfil. Quem é isento não vê IVA.
- **Linguagem:** PT por omissão, EN à distância de um toque. Tom morno, sem jargão por omissão; cada termo explicável em uma frase.
- **Literacia antes da decisão:** aula de 1 minuto antes do primeiro ecrã de triagem, não glossário escondido.

### O que a app nunca faz
- Autenticar no Portal das Finanças ou no e-Fatura (não há API pública; scraping quebra e exige credenciais).
- Submeter, alterar ou classificar seja o que for em nome do utilizador.
- Enviar faturas, NIF ou rendimentos para um servidor.
- Apresentar um valor de imposto como definitivo — a liquidação é da AT.
- Substituir contabilista certificado.

### Decisão em aberto: direção da geração
A proposta de `CLAUDE.md` que veio do design queria o **JSON canónico** e o markdown gerado
a partir dele. O repo faz o **inverso** — markdown canónico, `gerar_valores_json.py` deriva o
JSON — porque é o markdown que carrega as notas, as fontes e as ressalvas que um humano edita
e verifica. Fica assim até haver decisão em contrário; inverter implica mexer no gerador e nos
testes de divergência.

## Estado (14/09/2026)
- v0.1.0 instalada e exercitada; 35 testes, verificados por mutação.
- Confirmado em fonte oficial: coeficientes do art. 31.º (todos), dedução 2024 = 4.350,24 €, 2025 = 4.462,15 €, 2026 = 4.587,09 € (IAS oficial + fórmula em vigor), art. 53.º = 15.000 €, tabela do 151.º inclui **1336 Designers** (→ 0,75), SS: 21,4% / 25,2% (ENI comercial), isenção por acumulação < 4×IAS e **dispensa da declaração trimestral** para isentos (Guia ISS 1009 v1.09).
- Sentinela: 12 fontes HTML + 1 PDF; ordem corrigida (issue antes da baseline); marcadores de conteúdo. **Run #2 ainda não correu.**
- Pendente: URL real do PDF da SS (deduzida do nome do ficheiro); taxa SS para ENI com atividades mistas; regime da margem (2.ª mão) ↔ art. 53.º; prazos IRS 2027.

## Convenções
- Datas `dd/mm/aaaa`; euros `4.462,15 €`; artigos "art. 31.º n.º 13 CIRS".
- Commits em português, prefixo `feat:` / `fix:` / `docs:` / `sentinela:`.
- Só stdlib em Python. Nada de dependências para ler um CSV.
- Ficheiros ≤ 50 linhas por escrita quando se usa Desktop Commander.

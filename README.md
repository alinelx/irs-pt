# irs-pt

Assistente open source de IRS e e-Fatura para trabalhadores independentes em Portugal (regime simplificado), em formato **Agent Skill** — funciona no Claude (Code, Desktop, claude.ai, Cowork) e em qualquer agente compatível com [agentskills.io](https://agentskills.io).

**Não é aconselhamento fiscal. Não submete nada no Portal das Finanças.** Explica, calcula e recomenda; a decisão e o clique são teus. Confirma com contabilista certificado.

## Porquê

A pergunta que quase ninguém sabe responder: *"vale a pena afetar esta fatura à atividade?"*

No regime simplificado a resposta é surpreendentemente binária. Só precisas de justificar despesas se 15% do rendimento bruto de serviços ultrapassar a dedução específica automática (4.462,15 € para rendimentos de 2025). Abaixo de ~29.748 €/ano de serviços, **as tuas faturas de gastos não mudam o IRS da atividade** — e afetá-las só te faz perder deduções pessoais (saúde, educação, despesas gerais).

A skill faz essa conta primeiro e só depois fala de faturas. Lida com atividades mistas (vendas 0,15 + serviços 0,75 + outros serviços 0,35) e com acumulação de trabalho por conta de outrem.

## O que faz

1. Pergunta 2-3 coisas (atividades, rendimento esperado, Cat. A / IVA)
2. Calcula o limiar do ano e diz-te, em uma frase, se as faturas interessam
3. Se sim, lê o CSV exportado do e-Fatura (`scripts/parse_efatura.py`, sem dependências, sem enviar dados) e propõe classificação fatura a fatura
4. Mostra um preview e pede confirmação antes de listar o que clicar no portal
5. Termina com uma próxima ação e os prazos do ano

## Instalar

**Claude Code**
```
/plugin marketplace add alinelx/irs-pt
/plugin install irs-pt@irs-pt
```

A partir de um clone local, a barra é obrigatória — `add .` falha com *"Invalid marketplace source format"*:
```
/plugin marketplace add ./
/plugin install irs-pt@irs-pt
```

**Claude Desktop / claude.ai** — `+` → Plugins → adicionar marketplace a partir do repositório `alinelx/irs-pt`. Requer Skills e code execution ativos. Alternativa: zipar `skills/irs-pt/` e carregar em Settings → Capabilities → Skills → Upload skill.

**Outros agentes (Cursor, Codex, Copilot, Gemini CLI…)**
```
npx skills add alinelx/irs-pt --skill irs-pt
```

## Estrutura

```
skills/irs-pt/
  SKILL.md                     fluxo de 5 passos + regras invioláveis
  references/valores-anuais.md o que muda todos os anos (IAS, limiares, prazos) — atualizar AQUI
  references/fiscal.md         mecânica estrutural (coeficientes, art. 31.º n.º 13, IVA, SS)
  references/efatura.md        classificação no portal, regra por fatura, exportação CSV
  scripts/parse_efatura.py     resumo do CSV do e-Fatura (stdlib only)
```

## Estado

v0.1.0 — valores de 2025 confirmados; 2026 marcados como "a confirmar". Testado por uma pessoa (a autora) na sua própria declaração. Issues e PRs bem-vindos, sobretudo de contabilistas certificados.

## Referências e projetos vizinhos

- CIRS art. 25.º, 28.º, 31.º; CIVA art. 53.º (DL n.º 35/2025); Código Contributivo art. 157.º
- [FIZ-co/fiz-invoicing-skill](https://github.com/FIZ-co/fiz-invoicing-skill) — faturação PT com IA, referência de estrutura
- [calef/us-federal-tax-assistant-skill](https://github.com/calef/us-federal-tax-assistant-skill), [robbalian/claude-tax-filing](https://github.com/robbalian/claude-tax-filing) — skills de impostos nos EUA

## Licença

MIT

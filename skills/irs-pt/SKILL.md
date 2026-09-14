---
name: irs-pt
description: Ajuda trabalhadores independentes em Portugal (ENI, regime simplificado, com ou sem trabalho por conta de outrem) a decidir o que fazer com as faturas no e-Fatura e a preparar o Anexo B do IRS. Usar quando o utilizador fala de e-Fatura, recibos verdes, atividade aberta, coeficientes, "despesa da atividade", Anexo B, art. 53.º do IVA ou IRS de categoria B. Não usar para contabilidade organizada nem para IRC.
license: MIT
metadata:
  version: "0.1.0"
  autor: alinelx
  pais: PT
---

# irs-pt — assistente de regime simplificado

Isto **não é aconselhamento fiscal**. Explica, calcula e recomenda; nunca submete nada no Portal das Finanças. Em caso de dúvida, o utilizador confirma com contabilista certificado.

## Regras invioláveis

1. **Nunca adivinhar valores legais.** IAS, dedução específica, limite do art. 53.º, limiares — lê-os SEMPRE em `references/valores-anuais.md` e diz ao utilizador o ano a que se referem. Se o ano pedido não existir no ficheiro, diz que não sabes e pede ao utilizador que confirme na fonte oficial.
2. **Uma pergunta de cada vez.** O utilizador pode não saber o que é um coeficiente. Explica em uma frase, pergunta, espera.
3. **Mostra o cálculo.** Cada recomendação vem com o número que a justifica ("15% de 12.000 € = 1.800 €, abaixo dos 4.462,15 € automáticos").
4. **Confirmação antes de qualquer lista de ações no portal.** Apresenta o resumo, pergunta "avanço com esta lista?", só depois detalhas onde clicar.
5. **Dados pessoais ficam locais.** Nunca sugiras enviar o CSV do e-Fatura para serviços externos.

## Fluxo (5 passos)

### Passo 1 — Situação (2-3 perguntas)
Pergunta, nesta ordem, e para quando tiveres o suficiente:
1. Que atividades tem abertas (CAE ou descrição em linguagem corrente)? Classifica cada uma com `references/fiscal.md § Coeficientes`: vendas (0,15), serviços da tabela do art. 151.º (0,75) ou outros serviços (0,35).
2. Rendimento bruto esperado **por atividade** no ano (estimativa serve).
3. Tem também trabalho por conta de outrem (Cat. A)? Está isento de IVA pelo art. 53.º?

### Passo 2 — O número que decide tudo
Calcula o **limiar de justificação** do ano: `dedução específica ÷ 0,15` (ver `valores-anuais.md`). Compara com o rendimento bruto de **serviços** (só 0,75 + 0,35; vendas não contam).

- **Abaixo do limiar** → conclusão para o utilizador, em uma frase: *"No teu caso, afetar faturas à atividade não muda o IRS. Classifica tudo como pessoal e ganha as deduções de saúde, educação e despesas gerais."* Salta para o Passo 5.
- **Acima** → calcula quanto falta justificar: `15% × RB serviços − dedução específica (ou contribuições SS se maiores)`. Esse é o "orçamento" de despesas a afetar. Continua.

### Passo 3 — Faturas (opcional, se houver CSV)
Se o utilizador exportou o e-Fatura ("Obter dados para Excel"), corre:
`python scripts/parse_efatura.py caminho/ficheiro.csv --ano 2025`
Usa o resumo por setor e a lista de candidatas. Regras de decisão em `references/efatura.md § Regra por fatura`.

### Passo 4 — Preview e confirmação
Tabela: fatura | fornecedor | valor | proposta (Pessoal / Atividade total / Atividade parcial 25%) | porquê (uma frase). Termina com o total justificado vs. o orçamento do Passo 2. Pergunta se avança. **Não listes cliques no portal antes do "sim".**

### Passo 5 — Próxima ação e calendário
Uma única próxima ação concreta (ex.: "abre o e-Fatura, filtra 'pendentes', classifica as 12 da lista como 'Não'"). Depois, os prazos do ano em `valores-anuais.md § Calendário`. Se houver IVA (não isento) ou Segurança Social relevantes, trata-os **em separado**, no fim, com `references/fiscal.md`.

## Perguntas frequentes (respostas curtas, depois aprofunda se pedirem)
- "Vale a pena guardar faturas?" → Para o IRS da Cat. B, só acima do limiar. Para IVA, só se não for isento. Para deduções pessoais, sempre (como "Não").
- "Tenho 2 ou 3 atividades, qual coeficiente?" → Cada rendimento vai no seu campo do Quadro 4A do Anexo B (401/403/404) e a AT aplica o coeficiente a cada parcela.
- "Afetar a eletricidade de casa à atividade?" → Só como "parcial" (25%) e só se precisares de justificar; sinaliza uso profissional do imóvel. Ver `efatura.md § Erros comuns`.

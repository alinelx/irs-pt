---
name: irs-pt
description: Apoio ao IRS português para trabalhadores independentes (Categoria B, regime simplificado). Usar quando o utilizador falar de IRS, recibos verdes, trabalhador independente, Anexo B, e-Fatura, despesas dedutíveis, coeficiente 0,75 ou 0,35, regra dos 15%, afetação à atividade, Modelo 3, Finanças/AT, ou pedir para tratar/preparar/conferir o IRS ou as faturas do ano. Também para ler exportações CSV do e-Fatura. EN: "Portuguese tax return", "Portugal self-employed tax", "IRS Portugal".
---

# IRS-PT — Categoria B, regime simplificado

A pergunta que decide tudo não é *"que faturas tenho?"* é **"preciso sequer de faturas?"**.
No regime simplificado a dedução automática costuma cobrir a regra dos 15% sozinha. O
Passo 2 resolve isso em duas contas; só se sobrar é que vale a pena abrir o e-Fatura.

## Antes de responder

Isto não é aconselhamento fiscal e não substitui contabilista certificado nem a AT.

- **Nunca afirmar um valor de memória.** Todos os números anuais estão em
  `references/valores-anuais.md`, com fonte e ano. Os que estão marcados `⚠️ A CONFIRMAR`
  não podem ser apresentados como facto.
- **Nunca submeter nada.** A declaração é do contribuinte; o output é preparação.
- **Mostrar sempre a conta**, com inputs, para poder ser refeita.
- **Os valores da AT prevalecem** sobre qualquer cálculo feito aqui.
- Responder em português europeu.

## Passo 1 — Enquadrar

Recolher, sem assumir: **ano de rendimentos**; CAE/atividades e respetivo **coeficiente**
(ver `references/fiscal.md`); **rendimento bruto** de prestações de serviços por
coeficiente; **contribuições obrigatórias pagas à Segurança Social** no ano; se há
contabilidade organizada (então esta skill não se aplica).

Com vários CAEs, separar o bruto por coeficiente — a regra dos 15% só incide sobre a
parte sujeita a **0,75 e 0,35**.

## Passo 2 — A conta do limiar

```
A. Limiar          = 0,15 × (bruto sujeito a coef. 0,75 e 0,35)
B. Dedução autom.  = máx(dedução específica Cat. A do ano; contribuições obrigatórias pagas)
C. Falta justificar = A − B
```

- **C ≤ 0** → nada a justificar. Não é preciso reunir faturas para este efeito. Parar aqui
  e dizê-lo: é o resultado mais comum.
- **C > 0** → cada euro não justificado é **acrescido ao rendimento tributável** (não é
  "dedução perdida"). Seguir para o Passo 3 para cobrir `C`.

Dois atalhos, com os valores do ano em `references/valores-anuais.md`:

- Abaixo do **limiar de dispensa** de rendimento bruto, `B` cobre `A` sozinha.
- Quem descontou para a SS sobre a totalidade do rendimento já tem ~14,98% do bruto em
  contribuições (21,4% × 70%), ou seja quase os 15% inteiros. Confirmar com o valor
  efetivamente pago, não presumir — isenções no início de atividade e acumulação com
  trabalho dependente alteram isto.

## Passo 3 — Só se `C > 0`: reunir despesas

Correr o parser sobre o CSV exportado do e-Fatura:

```bash
python3 scripts/parse_efatura.py FICHEIRO.csv --resumo
```

Agrega por setor e estado, corrige o sinal das notas de crédito e lista as pendentes.
`--json` para output estruturado; `--help` para as opções.

Aplicar depois as regras de `references/efatura.md`: o que conta para os 15%, **afetação
total vs. parcial (25%)**, e o que não conta de todo. A despesa tem de ter o **NIF de
atividade** e estar afeta à atividade.

## Passo 4 — Conferir no Portal das Finanças

Validar faturas pendentes e confirmar os totais em *Despesas Dedutíveis* dentro dos
prazos de `references/valores-anuais.md`. Divergência entre o parser e a AT: **ganha a
AT** — investigar a diferença, não ignorá-la.

## Passo 5 — Rever

Anexo B preenchido por coeficiente; despesas afetas declaradas; retenções vs. recibos;
IBAN; comparar tributação conjunta e separada na simulação do Portal.

Encaminhar para contabilista certificado se houver: contabilidade organizada, atividade
com IVA complexa, rendimentos no estrangeiro, mais-valias, herança indivisa, ou
alteração de regime no ano.

## Referências

| Ficheiro | Conteúdo |
|---|---|
| `references/valores-anuais.md` | Só o que muda por ano: IAS, dedução, limiares, prazos |
| `references/fiscal.md` | Mecânica estrutural: coeficientes, regra dos 15%, o que conta |
| `references/efatura.md` | Regra por fatura: afetação, NIF, setores, casos-limite |

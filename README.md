# irs-pt

Plugin do Claude Code para apoio ao **IRS português** de trabalhadores independentes
(Categoria B, regime simplificado).

Parte de uma observação simples: no regime simplificado, a pergunta útil não é *"que
faturas tenho?"* mas **"preciso sequer de faturas?"**. A dedução automática do art. 31.º
costuma cobrir a regra dos 15% sozinha — e em 2025 cobre até **29.747,67 €** de
rendimento bruto. O fluxo faz essa conta no Passo 2, antes de abrir o e-Fatura.

## Instalar

```
/plugin marketplace add alinelx/irs-pt
/plugin install irs-pt@irs-pt
```

Ou, a partir de um clone local:

```
/plugin marketplace add .
```

## Usar

Depois de instalado, basta pedir em linguagem natural:

> quero tratar do meu e-Fatura de 2025

A skill pergunta o enquadramento (ano, CAEs e coeficientes, rendimento bruto,
contribuições pagas), faz a conta do limiar e só depois — se for preciso — parte para as
faturas.

### Parser do e-Fatura

Pode ser corrido isoladamente:

```bash
python3 skills/irs-pt/scripts/parse_efatura.py FICHEIRO.csv --ano 2025 --resumo
python3 skills/irs-pt/scripts/parse_efatura.py *.csv --json
```

Tolerante a variações de codificação (UTF-8, cp1252, latin-1), delimitador (`;` `,` tab
`|`), formato de data e nomes de coluna. Corrige o sinal das notas de crédito, exclui
documentos anulados, agrupa por setor, estado, mês e emitente, e lista as faturas
pendentes. Só depende da biblioteca padrão do Python 3.9+.

## Estrutura

```
.claude-plugin/
  marketplace.json      # torna o repo instalável como marketplace
  plugin.json           # manifesto do plugin
skills/irs-pt/
  SKILL.md              # fluxo de 5 passos
  references/
    valores-anuais.md   # só o que muda por ano (IAS, dedução, limiares, prazos)
    fiscal.md           # mecânica estrutural (coeficientes, regra dos 15%)
    efatura.md          # regra por fatura (afetação, NIF, casos-limite)
  scripts/
    parse_efatura.py
    exemplo-efatura.csv # dados fictícios, para testar
```

## Valores

`references/valores-anuais.md` separa o que está **verificado** do que está **por
confirmar**, com a fonte de cada valor. Para rendimentos de 2025:

| Valor | Montante |
|---|---|
| IAS | 522,50 € |
| Dedução específica (8,54 × IAS) | 4.462,15 € |
| Limiar de dispensa de justificação | 29.747,67 € |

> Muita fonte online ainda indica 4.104 € e um limiar de 27.360 €. Está desatualizado:
> desde 2025 o art. 25.º n.º 1 do CIRS está indexado ao IAS.

Os valores de 2026 estão marcados como por confirmar até saírem os do OE aplicável.

## Privacidade

O `.gitignore` bloqueia `*.csv`, `*.xlsx` e `*.pdf` para que dados do e-Fatura nunca
sejam commitados por acidente. O único CSV versionado é o exemplo sintético.

## Aviso

Não é aconselhamento fiscal e não substitui contabilista certificado nem a Autoridade
Tributária. A declaração é sempre do contribuinte, e os valores da AT prevalecem sobre
qualquer cálculo feito aqui.

## Licença

MIT

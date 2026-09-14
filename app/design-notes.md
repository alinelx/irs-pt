# Notas do design — origem e mapa de ecrãs

Importado de **IRS-PT mobile app design** (Claude Design, projeto
`56e35685-0821-45c5-bd69-058d7f0a6e01`). Este ficheiro era o `github.md` do projeto.

```
repo:   alinelx/irs-pt
branch: main
path:   skills/irs-pt
sync:   2026-09-14T14:01:21Z
```

## Decisões registadas na altura do design

- Procurou-se `CLAUDE.md` na raiz do repo — **não existia**, e foi redigida uma proposta.
  Entretanto o repo passou a ter um; ver a secção *App mobile* no `CLAUDE.md` atual.
- Ecrãs nomeados pelos 5 passos do `SKILL.md`, com o **Passo 2** (o veredicto do limiar)
  como ecrã central.
- Painel visível de fonte para «2026 a confirmar». Desde então 2026 passou a **confirmado**
  (Portaria n.º 480-A/2025/1 + redação em vigor) — o design está desatualizado neste ponto.
- Sem login, sem envio de dados, sem botão de submeter em lado nenhum.

## Mapa de ecrãs → ficheiros do repo

| Ecrã | Ficheiros |
|---|---|
| 1a Início / dashboard | `SKILL.md` (passos 2 e 5), `references/valores-anuais.md`, `references/fiscal.md` |
| 1b Veredicto (abaixo do limiar) | `SKILL.md` § Passo 2, `references/valores-anuais.md` |
| 1c Veredicto (acima do limiar) | `references/fiscal.md` § Regra de justificação (art. 31.º n.º 13) |
| 1d Triagem fatura a fatura | `references/efatura.md` § Regra por fatura, `scripts/exemplo-efatura.csv` |
| 1e Triagem em lote + regras | `references/efatura.md`, `scripts/parse_efatura.py` (resumo por setor) |
| 1f Prazos | `references/valores-anuais.md` § Calendário |
| 1g Fechar o ano (Anexo B) | `references/fiscal.md` § Coeficientes (Q4A 401/403/404) |
| 1h Android — início | os mesmos de 1a |

## Valores no mockup

O design tem valores fiscais literais, o que num mockup é legítimo. Foram conferidos contra
`main` à data da importação e **batem todos**: IAS 522,50 €, dedução 4.462,15 €, limiar
~29.748 €, IAS 2026 537,13 €, dedução 2026 4.587,09 €, SS 21,4%, coeficientes 0,75 / 0,35 / 0,15.

**Na app implementada isto não se repete.** A regra do `CLAUDE.md` mantém-se: a app lê
`skills/irs-pt/references/valores-anuais.json` e não tem tabelas próprias.

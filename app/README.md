# app/ — design da app mobile

Desenho da app **IRS-PT Mobile**, importado do projeto Claude Design
[IRS-PT mobile app design](https://claude.ai/design/p/56e35685-0821-45c5-bd69-058d7f0a6e01)
a 14/09/2026.

**Isto é um design, não a app.** Não há build, não há código de produção aqui.

## Abrir

`IRS-PT Mobile.dc.html` é uma tela do Claude Design. Abre-o no browser a partir desta
pasta — precisa dos outros ficheiros ao lado dele, com estes nomes exatos.

```
app/
  IRS-PT Mobile.dc.html   o design: 8 ecrãs (1a–1h), iOS e Android
  support.js              runtime do canvas   ← do Claude Design
  ios-frame.jsx           moldura iOS 26      ← do Claude Design
  android-frame.jsx       moldura Material 3  ← do Claude Design
  design-notes.md         mapa ecrã → ficheiro do repo, e decisões de design
```

## Proveniência

Três dos ficheiros **não são código deste projeto** e não devem ser editados aqui:

| Ficheiro | O que é |
|---|---|
| `support.js` | Gerado (`dc-runtime/src/*.ts`). O próprio cabeçalho diz *do not edit*. |
| `ios-frame.jsx` | *Omelette starter scaffold*. Recopiar o starter sobrescreve-o. |
| `android-frame.jsx` | O mesmo. |

Estão versionados só para o design abrir a partir de um clone. A cópia canónica vive no
projeto Claude Design; para os atualizar, reimporta de lá em vez de os editares.

> Os dois `.jsx` foram transcritos na importação (vieram inline na resposta da API, não
> como ficheiros). Verificados estruturalmente — chavetas e parênteses equilibrados, todas
> as funções exportadas definidas — mas não comparados byte a byte com a origem. Uma
> reimportação sobrepõe-nos de qualquer forma.

## Regra que o design não dispensa

O mockup tem valores fiscais escritos à mão, o que num desenho é legítimo — e foram
conferidos contra `main` na importação, batendo todos.

**A app implementada não os repete.** Lê `skills/irs-pt/references/valores-anuais.json`.
Ver `CLAUDE.md` § *App mobile*.

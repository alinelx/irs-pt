# ADR-001: Direção da geração entre `valores-anuais.md` e `valores-anuais.json`

**Data:** 2026-09-14
**Estado:** **Aceite** (14/09/2026)
**Decidido por:** @alinelx
**Consultado:** `CLAUDE.md` (repo e proposta vinda do Claude Design), suite de 51 testes

---

## Contexto

### Problema

Os valores legais (IAS, dedução específica, limiar, limites de IVA, isenção de SS) têm dois
consumidores com necessidades opostas:

- a **Agent Skill** lê prosa — precisa das notas, das ressalvas e das fontes para não afirmar
  um valor sem o contexto que o qualifica;
- a **app mobile** lê escalares — precisa de um ficheiro estruturado, sem prosa.

O `CLAUDE.md` exige uma só fonte de verdade. Logo um dos formatos é canónico e o outro é
derivado. Falta decidir qual.

### Porque agora

A questão ficou explícita quando o design da app trouxe a sua própria proposta de `CLAUDE.md`,
que afirma o **JSON canónico com o markdown gerado a partir dele** — exatamente o inverso do
que o repo implementou no PR #3. As duas afirmações não podem coexistir, e a divergência está
neste momento assinalada em `CLAUDE.md § Decisão em aberto`.

### Requisitos

1. Um humano tem de conseguir editar os valores **depois de os verificar em fonte oficial**, e
   registar ao lado de cada um o que verificou e o que ficou por verificar.
2. A app tem de obter escalares e flags sem interpretar prosa.
3. Uma divergência entre os dois formatos tem de fazer os testes falhar.

---

## Decisão

**Manter o markdown canónico**, com `scripts/gerar_valores_json.py` a derivar o JSON.

---

## Opções

### Opção 1 — Markdown canónico → JSON derivado *(atual)*

**Prós**
- A prosa é o ponto: das 47 linhas do markdown, **16 são notas e ressalvas** e 2 são links de
  fonte. Coisas como *«em 2024 não aplicar a fórmula dos 8,54; foi a taxa de atualização do IAS»*
  não têm campo em JSON — teriam de virar strings longas, que ninguém revê em diff.
- Corresponde a quem edita. O `CLAUDE.md` diz «humano, após verificação em fonte oficial»; o
  humano verifica lendo o Portal das Finanças e escreve o que viu, em texto.
- Evidência desta semana: a regressão que `main` sofreu (2024 de volta a 4.349,08 €) só foi
  apanhada por se ler a prosa à volta da tabela. Um diff de JSON teria mostrado dois números
  a mudar, sem dizer que o método estava trocado.

**Contras**
- **O gerador lê a tabela markdown com regex** (`LINHA_ANO`). Reformatar a tabela — mudar a
  ordem das colunas, partir uma célula em duas linhas — parte a geração. É o argumento mais
  forte contra esta opção, e o risco é real.
- Não há esquema. Nada impede escrever `4.462,15 €` numa coluna que devia ter uma percentagem.

### Opção 2 — JSON canónico → Markdown derivado *(a proposta do design)*

**Prós**
- Formato estruturado à entrada: validável com JSON Schema, sem parsing frágil.
- Uma sentinela futura poderia propor a atualização anual como um patch de JSON, mais fácil de
  rever e aplicar do que uma edição de tabela.
- O markdown passaria a ser um artefacto de apresentação, gerável para várias superfícies.

**Contras**
- As notas teriam de viver dentro do JSON como strings. Editar prosa multilinha em JSON é pior
  para quem escreve **e** para quem revê o diff.
- A prosa não é por ano nem por campo: o bloco das duas leis qualifica a tabela inteira, o
  calendário é outra secção. Modelar isso em JSON é inventar um mini-CMS.
- Inverte o gerador e os testes de divergência que acabaram de entrar.

### Opção 3 — Ambos escritos à mão, com teste de igualdade

**Prós**: cada formato fica ótimo para o seu leitor; sem parsing.
**Contras**: duas fontes de verdade, que é exatamente o que o `CLAUDE.md` proíbe. O teste
apanha a divergência mas não diz qual dos lados está certo. **Descartada.**

---

## Justificação

O critério que decide é **quem escreve, e o que escreve**. O ficheiro é editado por uma pessoa
que acabou de ler uma página do Portal das Finanças e precisa de registar não só o número mas a
sua qualificação: que lei o produziu, o que ficou por confirmar, porque é que o valor que circula
online está errado. Esse registo é prosa e é a parte que evita erros — como se viu esta semana.

O JSON é uma **projeção** disso: 9 campos por ano, todos escalares ou flags. Projetar do rico
para o plano não perde nada de que a app precise. O inverso perderia o que torna o ficheiro
fiável.

### Compromissos aceites

- Parsing por regex, frágil a reformatação da tabela. Mitigado, não eliminado: o
  `gerar_valores_json.py --check` falha em qualquer divergência, e
  `TestValoresJSON.test_limiar_coerente_em_todos_os_anos` valida a aritmética dos valores
  lidos — se o parser ler mal uma célula, os testes partem.
- Sem esquema à entrada. Aceite enquanto a tabela tiver 3 linhas e 8 colunas.

### Pressupostos

- O número de anos mantém-se pequeno (uma linha nova por ano).
- A app não precisa de mais do que escalares e flags. Se vier a precisar do texto das notas,
  este ADR é revisto.

---

## Consequências

**Positivas** — o `CLAUDE.md` fica coerente; o gerador e os testes ficam como estão; quem
verifica valores continua a editar um ficheiro legível.

**Negativas** — o risco de parsing mantém-se; a sentinela, se um dia propuser atualizações
automáticas, terá de propor edições de markdown e não um patch estruturado.

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Reformatar a tabela parte a geração | Média | Médio | `--check` no CI; teste de mutação já existente |
| Parser lê a célula errada em silêncio | Baixa | **Alto** | `TestValoresJSON` verifica limiar = dedução ÷ 0,15 em todos os anos |
| App precisa de prosa que o JSON não tem | Baixa | Médio | Rever este ADR; acrescentar campo derivado |

---

## Implementação

Nada a mudar no código: a Opção 1 é o que já está implementado.

**Por fazer:** correr `gerar_valores_json.py --check` em CI, para o markdown e o JSON não
poderem divergir num push. É a mitigação do risco de parsing aceite acima, e a única ação
que esta decisão gera.

A Opção 2, se algum dia for reconsiderada, implica inverter `gerar_valores_json.py`, decidir
como a prosa sobrevive (secção solta no markdown? campo `notas` por ano?), reescrever
`TestValoresJSON` e corrigir o `CLAUDE.md` do repo em vez da proposta.

---

## Validação

Esta decisão está certa se, daqui a uma campanha de IRS: a atualização anual continuar a ser uma
edição de tabela mais uma nota; nenhum valor tiver entrado no JSON sem passar pelo markdown; e
nenhum erro de parsing tiver chegado a `main` sem os testes o apanharem.

**Rever:** janeiro de 2027, quando a linha de 2027 for acrescentada — é o primeiro uso real do
fluxo de atualização.

---

## Referências

- `CLAUDE.md` § Fonte única de verdade, § Decisão em aberto
- `scripts/gerar_valores_json.py`, `skills/irs-pt/scripts/test_parse_efatura.py` (`TestValoresJSON`)
- PR #3 (geração implementada), PR #5 (proposta divergente importada do design)

# e-Fatura — regra por fatura

Só relevante se o Passo 2 da SKILL.md der `C > 0`. Se a dedução automática já cobre os
15%, nada disto muda o imposto da Categoria B.

## Exportar o CSV

<https://faturas.portaldasfinancas.gov.pt> → autenticar com NIF e senha das Finanças →
área **Faturas** → filtrar pelo **ano de rendimentos** → exportar/descarregar.

O portal tem duas vistas distintas e é fácil trocá-las:

- **Consumidor** — despesas pessoais do agregado (saúde, educação, gerais familiares,
  IVA por exigência de fatura). Alimentam deduções **à coleta**.
- **Atividade / adquirente** — despesas com o **NIF de atividade**. São estas que contam
  para a regra dos 15%.

O parser lê qualquer um dos formatos, mas a conta dos 15% só usa as da atividade.

## A decisão, fatura a fatura

Para cada despesa o portal pergunta se foi efetuada no âmbito da atividade profissional.
Três respostas, três efeitos:

| Classificação | Conta para os 15% |
|---|---|
| Afeta **totalmente** à atividade | 100% do valor |
| Afeta **parcialmente** | 25% do valor |
| Não afeta / consumo pessoal | 0% |

Critérios práticos:

- **Totalmente** — a despesa só existe por causa da atividade e não tem uso pessoal:
  software profissional, quotas de ordem, materiais, serviços de contabilidade,
  deslocações a clientes, seguro de responsabilidade profissional.
- **Parcialmente** — uso misto real: eletricidade, água, comunicações e renda quando se
  trabalha em casa; combustível de viatura usada para os dois fins.
- **Nenhuma** — despesa pessoal, ainda que a fatura tenha o NIF.

Classificar mal nos dois sentidos custa. "Parcial" numa despesa integralmente
profissional deita fora 75% do valor elegível; "total" numa despesa mista é incorreto e
fica exposto em inspeção. Na dúvida, documentar o critério de repartição.

## Pendentes

Faturas "pendentes" são as que a AT não conseguiu classificar sozinha — tipicamente
setores ambíguos ou emitentes com várias atividades. **Enquanto ficarem pendentes não
contam.** O parser lista-as com `--resumo`.

Há um prazo anual para as resolver (ver `valores-anuais.md`); passado esse prazo a
classificação fecha e o que estiver pendente perde-se.

## Notas de crédito

Uma nota de crédito anula ou reduz uma fatura anterior e tem de **abater** ao total. O
parser deteta o tipo de documento e inverte o sinal; se aparecer um total inesperadamente
alto, verificar primeiro se havia notas de crédito a somar em vez de subtrair.

## Casos-limite

- **Fatura sem NIF** — não conta. Não é recuperável depois de emitida.
- **Fatura com NIF pessoal numa despesa profissional** — o NIF é o mesmo número; o que
  distingue é a classificação no portal. Verificar se aparece na vista de atividade.
- **Ano errado** — vale a **data de emissão**, não a do pagamento.
- **Fatura-recibo de renda** — rendas de imóvel afeto entram pela alínea c) do art. 31.º
  n.º 13, via recibo eletrónico ou Modelo 44, não pelo e-Fatura.
- **Imóvel próprio afeto** — entra pela alínea d) (% do VPT), não como despesa.
- **Duplicação** — a mesma fatura não pode contar para os 15% da atividade **e** como
  dedução à coleta pessoal.

## Divergências com a AT

Se o total do parser não bater certo com *Despesas Dedutíveis* no Portal das Finanças,
**prevalece a AT**. Causas frequentes, por ordem: faturas pendentes; afetação parcial
aplicada (25%) que o parser somou a 100%; notas de crédito; faturas de outro ano;
documentos anulados pelo emitente.

Investigar a diferença antes de usar qualquer um dos números.

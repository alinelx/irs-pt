# Regras fiscais estruturais (Cat. B, regime simplificado)

Valores numéricos → `valores-anuais.md`. Aqui só a mecânica. Artigos referem-se ao CIRS salvo indicação.

## Coeficientes (art. 31.º n.º 1)

| Natureza do rendimento | Coef. | Campo Q4A Anexo B | Sujeito à regra dos 15%? |
|---|---|---|---|
| Vendas de mercadorias e produtos (inclui comércio em 2.ª mão) | 0,15 | 401 | **Não** |
| Prestações de serviços das atividades da tabela do art. 151.º (design, consultoria, programação, formação, etc.) | 0,75 | 403 | Sim |
| Outras prestações de serviços (ex.: estafeta/entregas, serviços não listados) | 0,35 | 404 | Sim |
| Propriedade intelectual/industrial, mineração de criptoativos | 0,95 | — | Não |
| Subsídios/subvenções **não** destinados à exploração (al. e) | 0,30 | — | Não |
| Subsídios à exploração e restantes rendimentos da Cat. B (al. f) | 0,10 | — | Não |

- Coeficientes confirmados em fonte: OCC e [art. 31.º do CIRS](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cirs_rep/Pages/irs31.aspx), Portal das Finanças.
- Circular n.º 5/2014 da AT: o 0,75 aplica-se a serviços de atividades da tabela do 151.º **mesmo que** o sujeito esteja coletado por CAE, se o serviço corresponder a uma atividade lá prevista.
- **Atividades mistas:** cada rendimento vai no seu campo; a AT aplica cada coeficiente à sua parcela. Não se soma tudo num só coeficiente.
- Redução dos coeficientes no início de atividade (−50% 1.º ano, −25% 2.º; n.º 10) **não se aplica** a quem tem rendimentos de Cat. A ou H nesses anos (informação vinculativa AT, proc. 29288/2025).

## Regra de justificação de despesas (art. 31.º n.º 13 e segs.; OE 2018)

Acresce ao rendimento tributável a **diferença positiva** entre:
- **15% dos rendimentos brutos** dos serviços a 0,75 e 0,35, e
- o somatório de:
  1. dedução específica do ano (o texto da lei diz 4.104 €; na prática o valor em vigor), **ou** contribuições obrigatórias para a SS, se superiores;
  2. despesas com pessoal;
  3. rendas de imóveis afetos à atividade;
  4. 1,5% do VPT dos imóveis afetos (4% hotelaria/AL);
  5. outras despesas da atividade — **100%** se exclusivas, **25%** se parcialmente afetas;
  6. importações e aquisições intracomunitárias de bens/serviços da atividade.

Consequências:
- RB serviços ≤ limiar → o item 1 cobre os 15% sozinho → faturas irrelevantes para o IRS da Cat. B.
- RB serviços > limiar → cada euro afetado (itens 2-6) reduz o acréscimo, até zerá-lo. Afetar mais do que o necessário **não reduz** imposto (o coeficiente já presume as despesas) e perde deduções pessoais.
- Exemplo: RB serviços 100.000 € a 0,75 → base 75.000 €; 15% = 15.000 €; justifica 4.462,15 € + 5.000 € = 9.462,15 €; acresce 5.537,85 € → tributável 80.537,85 €.

## Acumulação Cat. A + Cat. B
- Englobamento obrigatório; taxas progressivas do art. 68.º sobre a soma. Adicional de solidariedade acima de 80.000 €.
- Dedução específica da Cat. A (art. 25.º) é independente da Cat. B.
- Retenção na fonte na Cat. B: dispensa se estimativa anual ≤ 15.000 € (art. 101.º-B).
- Contabilidade organizada compensa quando as despesas reais ultrapassam a presunção do coeficiente (≈25% para serviços a 0,75). Custo típico de contabilista: ~150-200 €/mês (**estimativa de mercado, não oficial**).

## IVA — art. 53.º CIVA (DL n.º 35/2025, de 24 de março)
- Isenção se volume de negócios do ano anterior ≤ limite (ver `valores-anuais.md`). O volume das várias atividades **soma-se**.
- Ultrapassar o limite → regime normal a 1 de janeiro seguinte. Ultrapassar limite + 25% durante o ano → sai **de imediato**; o excesso já leva IVA; 15 dias úteis para comunicar.
- Isento não deduz IVA das compras. No regime normal, a afetação à atividade no e-Fatura é o que sinaliza IVA dedutível.
- Menção obrigatória na fatura: "IVA — regime de isenção (art.º 53.º do CIVA)".
- Bens em 2.ª mão: regime da margem (DL n.º 199/96) — tema de IVA, análise própria.

## Segurança Social (trabalhador independente)
- Declaração trimestral; rendimento relevante = 70% serviços / 20% vendas; taxa 21,4%.
- Isenção por acumulação com Cat. A se rendimento relevante mensal médio < 4×IAS **e** entidades distintas **e** Cat. A com proteção social equivalente **e** remuneração Cat. A ≥ 1 IAS. Acima, paga 21,4% só sobre o excedente.
- Contribuições obrigatórias substituem a dedução específica no item 1 da regra dos 15% se forem superiores.
- **A confirmar:** obrigatoriedade da declaração trimestral enquanto isento.

## Pontos a confirmar com contabilista certificado
1. Enquadramento exato de cada CAE do utilizador na tabela do 151.º (0,75 vs 0,35).
2. Dedução específica do ano corrente (depende do IAS e do OE).
3. Interação regime da margem (2.ª mão) ↔ art. 53.º.
4. Efeito de "afetação parcial" de despesas da habitação em futuras mais-valias.

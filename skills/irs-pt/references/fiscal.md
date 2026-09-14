# Mecânica estrutural

O que não muda de ano para ano. Os montantes estão em `valores-anuais.md`.

## Coeficientes (art. 31.º n.º 1 CIRS)

No regime simplificado o rendimento tributável obtém-se aplicando um coeficiente ao
rendimento bruto. A diferença é presumida como despesa — não se declaram custos reais.

| Coef. | Aplica-se a | Estado |
|---|---|---|
| **0,15** | Vendas de mercadorias e produtos; operações com criptoativos; restauração, bebidas, hotelaria e similares | ✅ |
| **0,75** | Atividades profissionais **especificamente previstas na tabela do art. 151.º** | ✅ |
| **0,35** | Prestações de serviços **não previstas** nas alíneas anteriores | ✅ |
| **0,95** | Mineração de criptoativos; cessão/utilização temporária de propriedade intelectual ou industrial; informações sobre experiência adquirida | ✅ |
| 0,30 | Subsídios/subvenções **não** destinados à exploração | ⚠️ confirmar |
| 0,10 | Subsídios destinados à exploração; restantes rendimentos da Cat. B | ⚠️ confirmar |

**Com vários CAEs**, cada atividade leva o seu coeficiente e o bruto tem de ser separado
por coeficiente. O erro típico é aplicar 0,75 a tudo porque a atividade principal é
profissional: um serviço fora da tabela do art. 151.º vai a 0,35, e a repartição muda a
conta do limiar, porque a regra dos 15% só incide sobre 0,75 e 0,35.

Na dúvida entre 0,75 e 0,35, o critério é a tabela do art. 151.º, não o CAE em si. O CAE
"outras atividades" quase sempre cai em 0,35.

## A regra dos 15% (art. 31.º n.º 13 CIRS)

A dedução implícita no coeficiente está **parcialmente condicionada**: acresce ao
rendimento tributável a **diferença positiva** entre 15% do rendimento bruto das
prestações de serviços (coef. **0,75 e 0,35**) e o somatório das importâncias abaixo.

```
acréscimo = máx(0 ;  0,15 × bruto(0,75 e 0,35)  −  Σ despesas elegíveis)
```

Três consequências que costumam ser mal entendidas:

1. **Não é uma dedução que se perde** — é um valor que se **soma** ao rendimento
   tributável, aumentando o imposto.
2. **Não se aplica a coef. 0,15 nem 0,95** — só à parte sujeita a 0,75 e 0,35.
3. **A dedução automática entra no somatório**, e normalmente domina-o. Por isso a conta
   do limiar vem antes das faturas.

## O que conta para os 15% (art. 31.º n.º 13, alíneas)

| | Despesa |
|---|---|
| a) | Dedução específica do art. 25.º n.º 1 **ou**, se superior, as contribuições obrigatórias para regimes de proteção social efetivamente pagas |
| b) | Despesas com pessoal e encargos a título de remunerações, ordenados ou salários |
| c) | Rendas de imóveis afetos à atividade (recibo de renda eletrónico ou Modelo 44) |
| d) | 1,5% do VPT dos imóveis afetos à atividade (**4%** se afetos a hotelaria/restauração) |
| e) | Outras aquisições de bens e serviços afetas à atividade, comunicadas à AT: consumo corrente, eletricidade, água, transportes e comunicações, rendas, contencioso, seguros, locação financeira, quotizações para ordens e associações, deslocações e estadas |
| f) | Importações e aquisições intracomunitárias de bens e serviços afetas à atividade |

A alínea a) é automática — não exige fatura nenhuma. As restantes exigem documento e
comunicação à AT.

## Afetação total vs. parcial

Uma despesa da alínea e) só conta **na medida da afetação à atividade**:

- **Afetação total** → conta **100%** do valor.
- **Afetação parcial** → conta **25%** do valor.

A classificação é feita pelo contribuinte no portal e-Fatura, fatura a fatura. Ver
`efatura.md`. Escolher "parcial" numa despesa que é integralmente profissional deita
fora 75% do valor elegível; escolher "total" numa despesa mista é incorreto.

⚠️ Confirmar a percentagem de afetação parcial no CIRS em vigor antes de a usar num
cálculo apresentado ao utilizador.

## Fronteiras

- **Contabilidade organizada** — mecânica diferente (custos reais). Esta skill não se
  aplica; encaminhar para contabilista certificado.
- **Despesas da Categoria B vs. deduções à coleta pessoais** — são coisas distintas. Uma
  despesa afeta à atividade conta para os 15%; saúde, educação e despesas gerais
  familiares são deduções à coleta do agregado, noutra fase do cálculo. Não misturar, e
  não contar a mesma fatura duas vezes.
- **IVA** — a exigência de fatura para dedução de IVA (restauração, cabeleireiros,
  oficinas, veterinários, passes) é dedução à coleta pessoal, não despesa de atividade.

## Anexo B

O Anexo B é o da Categoria B em regime simplificado. Rendimentos separados por
coeficiente, e as despesas afetas declaradas nos campos próprios. Confirmar a numeração
dos quadros no formulário do ano — muda entre campanhas.

## Fontes

- CIRS art. 28.º, 31.º, 151.º — <https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cirs_rep/>
- Ordem dos Contabilistas Certificados — <https://www.occ.pt>

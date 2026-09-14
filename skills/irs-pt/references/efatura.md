# e-Fatura — classificação e exportação

## A pergunta do portal
Quem tem atividade aberta tem de responder, por fatura: **"Foi emitida no âmbito da sua atividade profissional?"**

| Resposta | Efeito |
|---|---|
| **Não** | Despesa pessoal → conta para deduções à coleta (saúde 15%/1.000 €, educação 30%/800 €, despesas gerais familiares, IVA por exigência de fatura 15%, etc.) |
| **Sim, total** | 100% despesa da atividade → sai das deduções pessoais |
| **Sim, parcial** | 25% para a atividade, 75% continua pessoal |

Uma fatura afetada à atividade **deixa de contar** para as deduções pessoais na parte afetada.

## Regra por fatura (aplicar nesta ordem)
1. **RB de serviços ≤ limiar do ano?** → tudo "Não". Fim. (Ganhas deduções pessoais; para o IRS da Cat. B não há diferença.)
2. **Acima do limiar:** afeta à atividade só até cobrir o "orçamento" (`15% × RB serviços − dedução específica`), começando pelas despesas **exclusivas** da atividade (material, software, deslocações profissionais, seguros da atividade) como "Sim, total".
3. Despesas **mistas** (eletricidade, comunicações, renda da habitação) → "Sim, parcial" (25%), e só se ainda faltar orçamento. Marcar a habitação como afeta sinaliza uso profissional do imóvel.
4. Despesas ligadas a **vendas de mercadorias** (coef. 0,15) → não entram na justificação; classifica como pessoal ou, se forem inventário, guarda para IVA/contabilidade.
5. **IVA não isento?** → afetar à atividade também é o que permite deduzir o IVA; pode compensar afetar mesmo abaixo do limiar do IRS. Tratar em separado.

## Erros comuns (fonte: contabilistas/OCC)
- Afetar tudo à atividade abaixo do limiar: perde deduções pessoais, ganho zero.
- Marcar "total" o que é misto: risco em inspeção.
- Esquecer que a afetação de despesas da casa sinaliza afetação do imóvel (mais-valias).
- Não classificar até ao prazo (ver `valores-anuais.md § Calendário`): fica tudo como pendente.

## Exportar dados
Portal das Finanças → e-Fatura → **Faturação → Adquirente** → filtrar por data/estado → **"Obter dados para Excel"** (o ficheiro é um CSV).
Colunas habituais: NIF emitente, nome, tipo de documento, n.º, data, total, IVA, base, situação, setor de atividade. Os nomes exatos variam; o script `scripts/parse_efatura.py` deteta-os por aproximação.

Limitações relatadas por terceiros (**não confirmadas pela AT** — testar):
- ~300 registos por exportação → exportar por trimestre/mês se necessário
- registos não ordenados por data
- notas de crédito sem sinal negativo → o script corrige pelo tipo de documento

**Não há API pública.** Bibliotecas de scraping (ex.: `guedesmoney`) existem, mas quebram com mudanças do portal e exigem credenciais — esta skill não as usa. Atenção: pacotes chamados "efatura" no PyPI/npm são quase sempre do sistema turco.

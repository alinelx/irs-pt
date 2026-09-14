# Sentinela legal

Vigia as páginas oficiais listadas em `fontes.json` (CIRS, CIVA, Segurança Social, e-Fatura). Quando o **texto** de qualquer uma muda, abre uma issue com o diff. Não altera a skill — a decisão de atualizar `skills/irs-pt/references/*.md` é humana, e os testes garantem que a tabela de valores fica coerente.

- Corre no dia 1 de cada mês, a 15 de janeiro e a 10 de julho (ou manualmente em *Actions → Sentinela legal → Run workflow*).
- Ordem dos passos: comparar → **abrir a issue** → só depois guardar a nova baseline. Se a issue falhar, a baseline não é atualizada e o run seguinte volta a apanhar a mudança.
- Cada fonte tem um `marcador` (texto que tem de existir): uma página que responde 200 mas só devolve cookies ou menus é **falha**, não ok. Páginas do Portal das Finanças são recortadas a partir de `inicio` ("Artigo N") para ignorar o chrome do SharePoint.
- PDFs (ex. guias práticos) são vigiados por hash de bytes.
- Primeira execução: cria os snapshots, sem alerta.
- Falhas de acesso também abrem issue: uma URL que deixa de responder é sinal de que o portal mudou.
- Para vigiar mais coisas, acrescenta uma linha a `fontes.json`. **Pendente:** Segurança Social (o site é JS puro) — copiar do browser o link do PDF "Guia Prático — Trabalhadores Independentes" e acrescentar. Candidatas: portaria anual do IAS, tabelas de retenção, IRS Jovem.

Porque não em tempo real: a lei muda em datas previsíveis (OE em dezembro/janeiro, IAS em dezembro, raramente a meio do ano). Ler a fonte por máquina e confirmar por humano é mais fiável do que scraping em cada sessão, que quebra sem avisar.

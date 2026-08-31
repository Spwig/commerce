---
title: Relatórios de Campanhas
---

<!-- screenshots-needed:
- url: /admin/campaigns/{campaign_id}/report/
  filename: engagement-over-time-chart.webp
  description: The report page scrolled to the "Engagement over time" chart card, with a campaign that has several days of send history so all three lines (Sent, Opened, Clicked) show a realistic shape.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: top-links-table.webp
  description: The report page's "Top links" card, with a campaign whose email contains at least 3 distinct links and a realistic spread of Clicks/Unique/CTR values.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipients-list.webp
  description: The Recipients page with the filters panel open and a mixed list of rows (some opened, some clicked, some bounced) so the engagement states are visibly distinct.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/recipients/
  filename: recipient-activity-modal.webp
  description: The Recipients page with the "Recipient activity" modal open for a recipient who has multiple event types (delivered, opened, at least one clicked entry naming a link).
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: attributed-revenue-card.webp
  description: A close-up of the report page's "Attributed revenue" stat card, for a campaign with a logged Spend so the orders/AOV/revenue-per-email/ROAS sub-line is fully populated.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: dashboard-attributed-revenue-kpi.webp
  description: The Campaign Studio dashboard's stat card grid, scrolled/cropped to show the "Attributed revenue (30d)" tile alongside its neighboring cards, with a non-zero revenue figure.
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
- url: /admin/campaigns/{campaign_id}/report/
  filename: report-stat-cards.webp
  description: 'RECAPTURE NEEDED: the existing report-stat-cards.webp only shows 6 cards (Recipients, Delivered, Open rate, Click rate, Bounce rate, Spam complaints). The stat grid now has a 7th "Attributed revenue" card — recapture this shot with a campaign that has both attribution data and a logged Spend so all 7 cards are visible in a realistic state.'
  save-to: core/static/core/admin/img/help/campaign-reports/
  viewport: 1440x900
-->

Cada campanha enviada através do Campaign Studio possui sua própria página de **Relatório** — um resumo em uma única página de quantas pessoas foram alcançadas, quantos e-mails chegaram efetivamente e como os destinatários responderam. Use-o para verificar se um envio foi realizado com sucesso, identificar um problema de entregabilidade precocemente ou comparar o desempenho de diferentes campanhas ao longo do tempo.

## Abrindo um relatório

Em **Campaign Studio > Campanhas**, localize a campanha que deseja verificar e clique no ícone de gráfico (**Relatório**) em seu cartão.

![A grade de cartões de estatísticas da página de relatório da campanha, mostrando destinatários, entregues, taxa de abertura, taxa de cliques, taxa de rejeição e reclamações de spam](/static/core/admin/img/help/campaign-reports/report-stat-cards.webp)

Um relatório só exibe números quando a campanha foi efetivamente enviada — uma campanha ainda em **Rascunho** exibe todas as estatísticas como zero, pois ainda não há nada para medir.

## Os cartões de estatísticas

| Cartão | O que exibe |
|------|---------------|
| **Destinatários** | Quantos assinadores esta campanha alcançou, além de uma linha secundária indicando quantos foram ignorados e, desses, quantos foram ignorados especificamente porque o endereço está na sua [lista de supressão](list-hygiene). Um "skip" nem sempre é uma supressão — o Spwig também ignora um assinador que não tem um endereço de e-mail utilizável, por exemplo — por isso, as duas contagens são exibidas separadamente. |
| **Entregues** | Quantos e-mails foram efetivamente aceitos pelo servidor de correio receptor e nunca retornaram como rejeitados, além da **taxa de entrega** — entregues como uma proporção de todos os envios que o Spwig *tentou* (aceitos pelo seu servidor de correio ou provedor, independentemente de terem rejeitado posteriormente). |
| **Taxa de abertura** | A proporção de e-mails *entregues* que foram abertos, além da contagem bruta de **abertos**. |
| **Taxa de cliques** | A proporção de e-mails *entregues* que foram clicados, além da contagem bruta de **clicados** e da **taxa de cliques por abertura** — cliques como uma proporção de aberturas, uma leitura de quão persuasivo foi o seu conteúdo para as pessoas que já o abriram. |
| **Taxa de rejeição** | A proporção de envios *tentados* que foram rejeitados, dividida em rejeições **hard** e **soft**. |
| **Reclamações de spam** | Quantos destinatários marcaram o e-mail como spam ou lixo, além da **taxa de reclamação** — reclamações como uma proporção do correio *entregue*. |
| **Receita atribuída** | Receita de pedidos que o Spwig pode rastrear até esta campanha, além do número de pedidos, o valor médio do pedido (**AOV**), a receita por e-mail entregue e — uma vez que você tenha registrado o custo da campanha — o seu **ROAS**. Veja [Receita atribuída](#attributed-revenue) abaixo. |

## Por que as taxas usam denominadores diferentes

A taxa de abertura, a taxa de cliques e a taxa de reclamação são todas medidas em relação ao correio **entregue** — os destinatários que realmente puderam ver o e-mail — enquanto a taxa de entrega e a taxa de rejeição são medidas em relação aos envios **tentados**. Esta é uma prática padrão da indústria de e-mail, e é por isso que nenhuma dessas taxas pode exceder 100%: um e-mail que foi rejeitado nunca foi entregue, portanto, não pode contar para a sua taxa de abertura ou cliques, e um e-mail que nem sequer foi tentado (um "skip") não conta para nenhuma delas.

## Rejeições hard vs. rejeições soft

- **Rejeição hard** — o endereço é permanentemente inentregável. Ele não existe, ou o domínio se recusa a aceitar correio para ele.
- **Rejeição soft** — um problema temporário: uma caixa de correio cheia, um servidor receptor que estava brevemente indisponível, e similares. As rejeições soft geralmente se resolvem sozinhas.

Observe a divisão, não apenas o total. Um aumento na contagem de **rejeições hard** geralmente significa que a sua lista tem endereços desatualizados ou com erros de digitação; um aumento na contagem de **rejeições soft** é mais frequentemente um problema temporário no lado do destinatário. Qualquer rejeição hard, qualquer reclamação de spam e um endereço que acumula rejeições soft repetidas alimentam a [lista de supressão](list-hygiene) automática do Spwig — você não precisa agir sobre eles por conta própria, mas o relatório é onde você notará primeiro um pico que vale a pena investigar.

## Receita atribuída

Como a sua loja e o Campaign Studio estão no mesmo sistema, o Spwig não precisa de uma plataforma de análise externa ou de um pixel de rastreamento para dizer se uma campanha realmente gerou vendas. Quando um cliente clica em um link no e-mail desta campanha e acessa a sua loja, o Spwig pode acompanhar essa visita até a finalização da compra e creditar a receita do pedido resultante à campanha — é isso que o cartão **Receita atribuída** exibe.

A linha secundária do cartão detalha a figura ainda mais:

- **Pedidos** — quantos pedidos são creditados a esta campanha.
- **AOV** — o valor médio do pedido entre esses pedidos.
- **Receita por e-mail** — receita atribuída dividida pelo número de e-mails *entregues*, o mesmo denominador que o relatório usa para a taxa de abertura e a taxa de cliques.
- **ROAS** — retorno sobre o investimento publicitário, exibido apenas uma vez que você tenha inserido um valor de **Gasto** na própria campanha.

É calculado como receita atribuída dividida pelo gasto.

Se o gasto foi registrado em uma moeda diferente da moeda padrão da sua loja, o Spwig oculta o ROAS em vez de exibir um número que não é realmente comparável — insira o gasto na moeda base da sua loja para visualizá-lo.

Alguns pontos importantes sobre como esse número é calculado:

- **É baseado em cliques, não em aberturas.** O cliente precisa clicar em um link rastreado no e-mail e chegar à sua loja — uma abertura sozinha nunca atribui receita. Isso é intencional: o rastreamento de aberturas está cada vez menos confiável, já que serviços como o Apple Mail Privacy Protection pré-carregam imagens para quase todas as mensagens, inflando as contagens de abertura independentemente de alguém ter lido o e-mail.
- **Segue o modelo de atribuição da sua loja.** Por padrão, é o **último toque não direto** com uma janela de análise de 90 dias — o mesmo clique precisa levar a um pedido dentro dessa janela para ser contabilizado, e uma visita direta posterior não apaga o crédito já conquistado pelo clique desta campanha.
- **Respeita o consentimento de análise.** Apenas visitantes que aceitaram o consentimento de análise no banner de cookies da sua loja são rastreados (se você não usar um banner de consentimento, o rastreamento segue a política padrão da própria loja). Um cliente que recusou o consentimento ainda pode comprar — seu pedido simplesmente não será atribuído a nenhum canal, incluindo este.
- **Não é retroativo.** O rastreamento de receita cobre apenas campanhas enviadas após a ativação do rastreamento de atribuição para a sua loja. Uma campanha enviada antes disso não mostrará receita atribuída aqui, mesmo que tenha gerado vendas reais, simplesmente porque o Spwig não possui dados de cliques registrados para ela.
- **Testes A/B e campanhas recorrentes também agregam sua receita atribuída** — veja [Relatórios de um teste A/B](#reports-on-an-ab-test) abaixo.

Você também encontrará um cartão de **Receita atribuída (30d)** no próprio painel do Campaign Studio, somando a receita atribuída por e-mail de todas as campanhas nos últimos 30 dias — uma verificação rápida sem abrir um relatório individual. Para uma visão geral da loja que inclua todos os canais, não apenas e-mail — busca orgânica, redes sociais, afiliados e mais — veja o painel de [Atribuição de Receita](/help/revenue-attribution) em **Insights**.

## Engajamento ao longo do tempo

Abaixo dos cartões de estatísticas, o gráfico **Engajamento ao longo do tempo** traça três linhas — **Enviados**, **Abertos** e **Clicados** — um ponto por dia, cobrindo os 30 dias anteriores a hoje (ou menos, se a campanha não estiver sendo enviada há tanto tempo — o gráfico nunca começa antes do dia do primeiro envio da campanha).

Alguns pontos sobre como as linhas são contabilizadas:

- **Abertos** e **Clicados** contam cada destinatário uma vez — no dia da *primeira* abertura ou do *primeiro* clique — e não todas as vezes que reabrem o e-mail ou clicam em um link novamente. Isso impede que o gráfico seja distorcido por um pequeno número de pessoas que abrem o mesmo e-mail repetidamente.
- Os totais por trás deste gráfico estão alinhados com os cartões de estatísticas acima: **Enviados** reflete o e-mail que o Spwig tentou entregar, enquanto **Abertos** e **Clicados** são ambos medidos em relação ao e-mail entregue, assim como os cartões de **Taxa de abertura** e **Taxa de cliques**.
- O gráfico só aparece quando a campanha tem pelo menos um envio registrado — uma campanha ainda em **Rascunho** exibe a mensagem "Nenhum envio ainda" em vez disso, assim como os cartões de estatísticas.

Use este gráfico para ver a *forma* de um envio, não apenas seus números finais — uma campanha enviada para uma lista grande frequentemente mostra um pico acentuado de aberturas nos primeiros dias, diminuindo depois. Um segundo pico dias depois pode indicar que o servidor de e-mail do destinatário colocou sua mensagem na fila, ou que sua linha de assunto foi notada mais tarde do que o habitual.

## Principais links

Se o seu e-mail contém links e pelo menos um destinatário clicou em um deles, uma tabela de **Principais links** aparece abaixo do gráfico, listando todos os links rastreados em ordem de popularidade.

| Coluna | O que ela mostra |
|--------|------------------|
| **Link** | A URL de destino como ela apareceu no seu e-mail. |
| **Cliques** | O número total de vezes que esse link foi clicado, incluindo cliques repetidos do mesmo destinatário. |
| **Únicos** | Quantos destinatários distintos clicaram nesse link pelo menos uma vez. |
| **CTR** | A **taxa de cliques** desse link — seu **número de únicos** como uma parcela do e-mail entregue. Isso usa o mesmo denominador que o cartão **Taxa de cliques** do relatório, então você pode comparar diretamente o desempenho de um único link com o desempenho geral da campanha. |

Se seu e-mail vincular a vários produtos ou uma mistura de botões de chamada à ação, essa tabela é a maneira mais rápida de ver qual deles realmente obteve o clique — útil para decidir o que destacar com mais destaque na próxima vez.

## Destinatários

Clique em **Destinatários** no topo do relatório para abrir uma lista completa e pesquisável de todos os destinatários aos quais essa campanha foi enviada, com o resultado da entrega de cada pessoa e seu engajamento.

Duas formas de filtrar a lista:

- **Pesquisa** — filtra por endereço de e-mail (uma correspondência parcial funciona, então digitar parte de um domínio ou nome é suficiente).
- **Engajamento** — filtra para um estado por vez: **Aberto**, **Clicado**, **Entregue, não aberto**, ou **Rejeitado**. Deixe-o em **Todos** para ver a lista completa.

A lista mostra os 100 destinatários mais recentes por vez, em ordem decrescente — o número acima da lista sempre reflete o total real que combina com seus filtros atuais, mesmo que seja maior do que o que está sendo mostrado. Para um grande envio, filtre a lista com Pesquisa ou Engajamento primeiro, em vez de rolar por todos.

### Visualizando o histórico de atividades de um destinatário

Clique no ícone de atividade em qualquer linha do destinatário para abrir o **Histórico de atividades do destinatário** — todos os eventos rastreados para a cópia do e-mail dessa pessoa, em ordem: entregue, aberto, clicado (indicando qual link), rejeitado (com o motivo da rejeição), marcado como spam ou cancelado, cada um com seu próprio carimbo de data/hora.

Essa é a maneira mais rápida de responder a uma pergunta específica sobre um cliente — por exemplo, confirmar se um assinante específico realmente recebeu a campanha antes de seguir em diante com outro canal, ou verificar qual link o cliente clicou antes de fazer o pedido.

## Relatórios em um teste A/B

Se a campanha que você está vendo é o container de um [teste A/B](ab-testing), seu relatório agregará **cada variante** — o todo o teste, combinado, incluindo **Receita atribuída** — e não mostrará uma variante por vez. Para ver como cada variante individual performou, abra a página de resultados própria do teste, em vez do relatório. Uma [campanha recorrente](recurring-campaigns) funciona da mesma forma: seu relatório reúne cada ocorrência que ele enviou.

## O que é considerado bom

Não há um único número saudável que se encaixe em todas as lojas ou listas — o público, a indústria e o conteúdo todos alteram a base — mas alguns padrões valem a pena ser observados em qualquer campanha:

- Uma **taxa de rejeição** que seja principalmente rejeições suaves, com rejeições difíceis raras, indica uma lista limpa e bem mantida. Uma subida repentina nas rejeições difíceis merece investigação antes do próximo envio.
- **Reclamações de spam** próximas de zero são o objetivo em cada envio. As reclamações prejudicam mais a reputação do remetente do que quase qualquer outra coisa — veja [Higiene da lista](list-hygiene) para entender por que elas importam além dessa única campanha.
- Uma **taxa de cliques após abertura** que esteja saudável em relação à taxa de abertura indica que as pessoas que abriram acharam o conteúdo válido para ação — uma taxa baixa de cliques após abertura juntamente com uma taxa de abertura forte geralmente indica que o assunto funcionou melhor do que o conteúdo dentro.

## Dicas

Mantenha todos os formatos de markdown, caminhos de imagens, blocos de código e termos técnicos.

- Verifique o relatório alguns minutos após o envio, não imediatamente — aberturas e cliques (e alguns relatórios de devolução) podem demorar para chegar ao seu provedor de e-mail.
- Se **Entregues** parecer menor do que o esperado, verifique primeiro a análise de pulos na carta **Destinatários** — um lote de pulos devido à supressão costuma ser a verdadeira causa, e não um problema de entrega.
- Use o relatório para comparar uma campanha com seus próprios envios anteriores, em vez de compará-lo com um número genérico da indústria — sua lista, conteúdo e público são o que estabelecem sua base realista.
- Um pico de reclamações em um envio específico merece uma análise mais detalhada sobre o conteúdo ou o público-alvo dessa campanha, e não apenas um registro para seguir em diante.
- Para uma campanha de teste A/B, leia esse relatório para obter o resultado geral e a página [resultados do teste A/B](ab-testing) para ver qual variante realmente venceu e por quê.
- Use a tabela **Links principais** para encontrar o link mais clicado, em seguida verifique se ele combina com o que você *queria* que os destinatários cliquem — se um link secundário estiver superando seu principal chamado à ação, pode valer a pena movê-lo para uma posição mais alta no e-mail na próxima vez.
- Os filtros **Abertos** e **Clicados** da página **Destinatários** são uma forma rápida de montar um público para um follow-up — por exemplo, verificando quem abriu, mas não clicou, antes de planejar um lembrete para o restante da lista.
- Se você pagou por uma promoção em torno de um envio — um post de rede social reforçado, um agradecimento de influenciador, aluguel de lista pagito — anote-o como o **Gasto** da campanha para liberar o **ROAS** no relatório.

É a maneira mais rápida de ver quais tipos de envios valem a pena repetir.
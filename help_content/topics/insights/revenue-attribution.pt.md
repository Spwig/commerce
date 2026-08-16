---
title: Atribuição de Receita
---

A Atribuição de Receita mostra a você onde suas vendas realmente vêm — não apenas o último link que o cliente clicou antes de comprar, mas todos os canais que contribuíram para chegar até ele. Se um cliente ler um artigo que você compartilhou nas redes sociais, voltar uma semana depois por meio de uma pesquisa no Google e, finalmente, comprar após clicar em um link de um e-mail, essas três interações contribuíram para essa venda. Este painel atribui a todas elas, usando um modelo que você escolher, para que você possa ver seu marketing da forma como ele realmente funciona, em vez de como o "último clique vence" pretende que ele funcione.

![O painel de atribuição de receita: o seletor de modelo de atribuição, a faixa de KPI com o selo "Reconcilia-se com a receita líquida", receita por canal, receita ao longo do tempo, o fluxo de jornada do cliente e a tabela de campanhas](/static/core/admin/img/help/revenue-attribution/dashboard-overview.webp)

## Onde encontrá-lo

Navegue até **Insights > Atribuição de Receita** no menu lateral. Insights é um grupo de menu dedicado acima de Produtos, então a Atribuição de Receita tem seu próprio espaço separado de seus relatórios de pedidos e clientes.

Insights é bloqueado pela categoria de permissão **Insights e Análise**. Se você não o vir no seu menu lateral, peça ao administrador da loja para lhe concedê-lo — veja [Funções e Permissões da Equipe](/help/staff-roles) para saber como gerenciar o acesso da equipe.

## Compreendendo a atribuição de múltiplas toques

A maioria das lojas está acostumada a pensar em termos de "para onde este pedido veio?" como se houvesse uma única resposta. Na realidade, os clientes raramente compram em sua primeira visita. Eles descobrem você de uma forma, voltam de outra forma e convertem de uma terceira forma — às vezes em várias visitas espalhadas por dias ou semanas. Cada uma dessas visitas é um **toque**: uma chegada registrada à sua loja com uma indicação de onde ela veio (um link de e-mail, um resultado de pesquisa, um post nas redes sociais, um link de afiliado, e assim por diante).

**Atribuição de múltiplas toques** significa reconhecer cada toque nessa jornada e decidir quanto crédito cada um merece para a venda final, em vez de dar 100% do crédito ao canal que aconteceu por último. Isso importa porque a relatórios de último clique subestimam sistematicamente os canais que fazem o trabalho de descoberta inicial — seu blog, sua presença orgânica nas buscas, seus posts nas redes sociais — porque eles raramente são o clique final antes da compra.

## Escolhendo um modelo de atribuição

O seletor de modelo no topo do painel é o controle mais importante da página. Clique em qualquer modelo e todos os números no painel — a faixa de KPI, as barras de canal, o gráfico, a tabela de campanhas — reatribuem automaticamente para corresponder. Este é um pré-visualização em tempo real: trocar de modelo aqui muda a forma como você está olhando para sua receita existente, não reescreve registros ou muda o modelo padrão salvo da sua loja.

![O seletor de modelo de atribuição — Último toque, Primeiro toque, Linear, Decaimento no tempo e Posição 40/20/40 — com o indicador "Reatribuições em tempo real · sem reprocessamento"](/static/core/admin/img/help/revenue-attribution/model-switcher.webp)

| Modelo | O que ele faz | Melhor para |
|-------|---------------|----------|
| **Último toque** | Dá crédito total ao último canal antes da compra, ignorando toques anteriores (exceto visitas puramente "diretas", que são puladas em favor da última fonte real) | Uma visão rápida e familiar - como a maioria das ferramentas básicas de análise relata receita |
| **Primeiro toque** | Dá crédito total ao canal que trouxe o cliente ao seu site pela primeira vez | Compreender o que está impulsionando a descoberta de novos clientes e o crescimento no topo do funil |
| **Linear** | Divide o crédito igualmente entre todos os toques na jornada | Uma visão equilibrada, sem opinião, quando você não quiser favorecer nenhum canal em particular |
| **Decaimento de tempo** | Dá mais crédito aos toques mais próximos da compra, menos aos toques mais antigos | Campanhas com janela de consideração curta, onde os lembretes recentes importam mais |
| **Posição 40/20/40** | Dá 40% de crédito ao primeiro toque, 40% ao último toque e divide os 20% restantes entre tudo o que estiver no meio | Reconhecer tanto "quem nos encontrou" quanto "quem fechou a venda", enquanto ainda credita a parte intermediária da jornada |

Não há um "modelo correto" - cada um responde a uma pergunta diferente. Uma abordagem comum é verificar **Primeiro toque** para ver o que está impulsionando a descoberta, em seguida **Último toque** ou **Posição 40/20/40** para ver o que está impulsionando as conversões, e usar ambas as visões juntas, em vez de escolher uma e ignorar o restante.

## Lendo a faixa de KPI

Logo abaixo do seletor de modelo, quatro números resumem o período selecionado e o modelo:

- **Receita atribuída** — o total de receita creditado entre todos os canais para o modelo atual. Ele carrega o selo **Reconcilia-se com a receita líquida** quando os números somam corretamente a receita líquida real da sua loja para o período — ou seja, o modelo está dividindo a receita real entre os canais, sem inventar ou perder nenhuma dela.
- **Pedidos** — quantos pedidos caem na faixa de datas selecionada.
- **Média de toques por pedido** — o número médio de toques registrados por pedido. Um número acima de 1 confirma que a maioria das jornadas dos seus clientes envolve mais de uma visita, o que é exatamente por que a atribuição de múltiplos toques importa para a sua loja.
- **Canal líder** — qual canal atualmente detém a maior parte da receita atribuída sob o modelo selecionado, com sua porcentagem de participação e receita.

## Receita por canal

O cartão **Receita por canal** mostra uma barra horizontal para cada canal, dimensionada pela receita atribuída. Troque o modelo de atribuição e veja as barras se reordenarem suavemente por classificação — este é o mesmo lucro subjacente, apenas redividido por um conjunto diferente de regras, então um canal que parece forte sob **Último toque** pode cair vários lugares sob **Primeiro toque** se ele atuar principalmente como apoio.

## Receita ao longo do tempo

O gráfico **Receita ao longo do tempo** empilha a receita atribuída por canal em cada dia da faixa selecionada, para que você possa ver não apenas quão valioso cada canal é, mas também quando ele contribui. Use-o para identificar padrões sazonais, confirmar se o impacto de uma campanha caiu nos dias que você esperava ou verificar se a contribuição de um canal está crescendo ou diminuindo durante o período.

## Como os clientes chegam na verdade

O painel **Como os clientes chegam na verdade** é um gráfico de fluxo de jornada conectando o canal que trouxe o cliente pela primeira vez (à esquerda) ao canal presente quando ele converteu (à direita). Faixas mais grossas significam que mais receita fluíram por esse caminho. É a maneira mais clara de ver jornadas de vários passos de uma só olhada — por exemplo, uma faixa grossa de Pesquisa Orgânica para E-mail diz que a pesquisa traz pessoas, mas o marketing por e-mail é o que as traz de volta para comprar.

![O gráfico de fluxo da jornada do cliente, com a lente "Influenciado" selecionada, mostrando canais de primeiro toque à esquerda fluindo para o canal em que cada pedido foi concluído](/static/core/admin/img/help/revenue-attribution/journey-flow-sankey.webp)

Use o interruptor **Atribuído** / **Influenciado** acima do gráfico para alternar as lentes:

- **Atribuído** divide a receita de cada pedido de acordo com o modelo selecionado, de modo que os totais correspondam a 100% da receita atribuída — os mesmos valores exibidos em outros locais do painel de controle.
- **Influenciado** credita *cada* canal que teve contato com um pedido com o *valor total* desse pedido, contando uma vez por pedido.

Isso não soma 100% intencionalmente — um canal pode ser "influenciado" por receita que também é contabilizada integralmente para outro canal.

Ele existe para revelar o alcance de um canal que o relatório de clique final esconde por completo, como um post de blog ou um compartilhamento nas redes sociais que gerou interesse em alguém, mesmo que ele não tenha clicado nele na visita final.

## Campanhas

A tabela **Campanhas** divide a receita, os pedidos e o valor médio dos pedidos (AOV) para cada uma das suas campanhas com marcação — links ou códigos que você marcou com um nome de campanha, incluindo códigos de cupom com marcação de campanha (consulte [Ideias de Campanha de Cupom](/help/voucher-campaign-ideas)). Use-a para comparar o desempenho de promoções individuais, códigos de influenciadores ou impulsos de marketing entre si, independentemente de qual canal os tivesse levado.

## Intervalo de data e exportação dos seus dados

Use o seletor de intervalo de data no canto superior direito para alternar entre **Últimos 7 dias**, **Últimos 14 dias**, **Últimos 30 dias**, **Últimos 90 dias** e **Mês até hoje**. O todo o painel de controle é atualizado para o novo período.

Clique em **Exportar CSV** para baixar a divisão por canal para o modelo e intervalo de data atualmente selecionados — útil para buscar números em uma planilha ou compartilhar com uma agência parceira.

## Como os toques são registrados

O Spwig captura automaticamente um toque sempre que um visitante chega à sua loja carregando um sinal de origem reconhecível, e somente quando o visitante deu **consentimento de análise** no banner de cookies da sua loja (se você não usar um banner de consentimento, o rastreamento é ativado por padrão, conforme determinado pela política própria da sua loja). Isso mantém a atribuição de receita no mesmo nível de privacidade que o resto da análise da sua loja.

Vários recursos são marcados automaticamente, sem necessidade de configuração:

| Canal | Como ele é identificado |
|---------|----------------------|
| **Email** | Links em seus e-mails de marketing (não e-mails de pedido ou envio) |
| **Pesquisa Orgânica / Paga** | Refereências de mecanhos de pesquisa, ou valores de `utm_medium` que marcam uma campanha de pesquisa paga |
| **Rede Social Orgânica / Paga** | Refereências de redes sociais, ou valores de `utm_medium` de redes sociais |
| **Afiliado** | Links gerados por meio do seu programa de afiliados |
| **Indique um Amigo** | Links gerados por meio do seu programa de indicação de clientes |
| **Campanha** | Qualquer link ou código que carregue uma marcação de campanha, incluindo códigos de cupom com marcação de campanha |
| **Link Externo** | Um link de entrada de outro site que não esteja categorizado de outra forma |
| **Direto** | Nenhum sinal de origem estava presente — o visitante digitou o endereço, usou um favorito, ou chegou de um aplicativo sem referrer |

Posts de blog que foram compartilhados automaticamente para suas contas conectadas nas redes sociais são automaticamente marcados, de modo que o tráfego que eles geram aparece sob o canal de rede social certo, em vez de ser perdido para Direto ou Link Externo.

Você também pode marcar seus próprios links manualmente usando parâmetros padrão `utm_source`, `utm_medium` e `utm_campaign` em qualquer URL que aponte para sua loja — útil para materiais impressos, newsletters de parceiros ou qualquer canal que o Spwig não marque automaticamente.

## Limitações a considerar

- **A atribuição segue um navegador, e não uma pessoa.** Se um cliente pesquisa em seu celular e compra em seu notebook, essas são duas jornadas separadas, no que diz respeito ao rastreamento — não há como vincular atividades em dispositivos diferentes.


Isso significa que alguns créditos que "deveriam" ir para um toque anterior em outro dispositivo acabarão no Direct.
- **Direct é onde o faturamento não rastreado chega.** Uma alta participação de Direct não significa necessariamente que as pessoas estejam digitando seu URL de memória — também pode significar que os toques anteriores de um cliente aconteceram em outro dispositivo, ou que um link que ele usou não tenha sido etiquetado.
- **Consentimento recusado significa que nenhum toque é registrado.** Visitantes que recusam o consentimento de análise no seu banner de cookies não são rastreados, então seus pedidos aparecerão como Direct mesmo que tenham chegado por meio de um canal que normalmente reconheceria.

## Dicas

- Verifique mais de um modelo antes de tirar conclusões — um canal que parece fraco sob **Último toque** pode ser seu maior driver de descoberta sob **Primeiro toque**.
- Se **Direct** representar uma grande parcela de seu faturamento, verifique se mais de seus links de marketing poderiam ser etiquetados com `utm_source`/`utm_medium`/`utm_campaign` — tráfego não etiquetado não tem outro lugar para chegar.
- Use a **Influenciado** como lente no gráfico de jornada quando estiver decidindo se deve continuar investindo em um canal como busca orgânica ou conteúdo de blog que raramente recebe o último clique, mas que consistentemente inicia jornadas.
- Compare a **Média de toques por pedido** ao longo do tempo — um aumento nesse número geralmente significa que os clientes estão levando mais tempo para decidir, o que é um sinal útil ao planejar o timing de e-mails de acompanhamento ou retargeting.
- Exporte o CSV do modelo e do período em que você estiver relatando antes de mudar novamente de modelo, já que a exportação reflete qual modelo estiver selecionado no momento em que você clicar em **Exportar CSV**.
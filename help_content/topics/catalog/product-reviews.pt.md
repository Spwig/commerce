---
title: Avaliações de Produtos
---

As avaliações de produtos permitem que os clientes classifiquem e escrevam sobre sua experiência com um produto. As avaliações que você aprovar aparecem na página do produto em sua loja, onde ajudam outros compradores a decidirem o que comprar. O Spwig lhe dá total controle sobre quais avaliações serão publicadas: nada é publicado até que você as aprova.

As avaliações ficam sob **Produtos > Avaliações** no menu lateral, que se abre como um grupo: o link superior o leva ao **Painel de Avaliações**, e **Moderar Avaliações** o leva diretamente à lista de avaliações.

## O Painel de Avaliações

Navegue até **Produtos > Avaliações** para abrir o painel — uma visão geral de uma tela de como as avaliações estão se saindo em toda a sua loja.

![Painel de Avaliações](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

No topo, seis cartões KPI resumem sua atividade de avaliação:

| Cartão | O que ele mostra |
|---|---|
| **Total de Avaliações** | Todas as avaliações já enviadas, aprovadas ou não |
| **Avaliação Média** | A média das classificações de estrelas em cada avaliação |
| **Aguardando Moderação** | Avaliações aguardando sua aprovação ou rejeição |
| **Taxa de Aprovação** | A parcela de todas as avaliações que você aprovou |
| **Compras Verificadas** | A parcela de avaliações deixadas por clientes com uma encomenda confirmada para aquele produto |
| **Novas (30 dias)** | Avaliações enviadas nos últimos 30 dias |

Logo abaixo dos KPIs, três gráficos dão mais detalhes:

- **Distribuição de Classificações** — um gráfico de barras de quantas avaliações caem em cada classificação de estrelas (1–5). Um agrupamento de avaliações com 1 estrela aqui merece investigação imediata.
- **Volume de Avaliações (12 semanas)** — um gráfico de linha das contagens de avaliações por semana, para que você possa identificar picos após uma promoção ou uma queda que precise de atenção.
- **Canal de Compra dos Avaliadores** — um gráfico de rosca do canal de marketing (direto, e-mail, pesquisa paga, social orgânico, e assim por diante) que trouxe a *compra* por trás de cada avaliação. Isso reutiliza seus dados de atribuição e é verdadeiramente útil para ver quais canais trazem clientes que depois deixam avaliações — mas ele não é um registro de como o cliente encontrou o formulário de avaliação em si. O Spwig não acompanha isso separadamente; veja 

Na aba **Revisão**, marque ou desmarque **Aprovação**.
3.
Clique no botão de marca de seleção no cabeçalho para salvar

## Página de edição de revisão

Abrir uma revisão fornece uma visualização do tipo painel centrada em torno dessa única revisão — um cabeçalho com o nome do produto, a classificação em estrelas, um selo **Aprovado**/**Pendente**, um selo **Compra Verificada** quando aplicável, quem escreveu a revisão e quando, e uma linha de estatísticas (**Classificação**, **Votos Úteis**, **Pedidos do Cliente**, **Gastos ao Longo da Vida**). Abaixo disso, os detalhes são organizados em quatro abas.

![Página de edição de revisão — aba de revisão com galeria de imagens](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Aba de revisão

É aqui que você modera a própria revisão:

- **Imagens da revisão** — se o cliente anexou fotos, elas aparecem aqui como uma galeria de miniaturas; clique em qualquer miniatura para abrir a imagem em tamanho real em uma nova aba. Revisões com fotos são um sinal forte de confiança para os compradores, então vale a pena dar uma olhada antes de aprovar.
- **Classificação**, **Título**, **Comentário** — o conteúdo enviado pelo cliente
- **Aprovação** — controla se a revisão é visível na sua loja virtual
- **Compra Verificada** — sinaliza a revisão como vindo de um comprador confirmado; o Spwig define isso automaticamente quando existe um pedido concluído para o produto (consulte a aba **Compra**), mas você pode substituí-lo aqui, se necessário
- **Imagens** — a lista subjacente de URLs de imagem por trás da galeria acima; normalmente você não precisa tocar nisso, mas ele permanece editável para casos excepcionais (por exemplo, remover uma foto de uma revisão com várias imagens)

Você não pode editar a redação da revisão — aprovar ou recusar, e gerenciar as imagens, é o limite do que você controla aqui.

### Aba de Cliente e Jornada

![Página de edição de revisão — aba de Cliente e Jornada](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Essa aba fornece contexto sobre quem deixou a revisão: pedidos totais, quantas revisões eles escreveram, sua classificação média, o quanto eles são clientes há, e seus dados de contato, com um link para abrir o registro completo do cliente.

Abaixo disso está a **jornada de tráfego** — os canais, campanhas e referrers que trouxeram esse cliente para sua loja, puxados dos dados de atribuição e mostrados como uma linha do tempo.

#### O que a "jornada" faz e o que não faz

Leia esse cronograma como a **jornada de chegada e compra** do cliente — como ele encontrou sua loja originalmente e foi adiante para comprar. Não é um registro da visita em que ele escreveu essa revisão. O Spwig não rastreia onde o cliente estava, ou qual dispositivo ou sessão ele usou, no momento em que ele enviou a revisão. Se o cronograma mostrar "Email > skincare de verão" três semanas antes da data da revisão, isso indica que a campanha de email provavelmente impulsionou a *compra* — não diz nada sobre se o cliente voltou de um resultado de pesquisa, um marcador ou um email de follow-up para realmente deixar a revisão. Trate essa aba como contexto de marketing útil, e não como um rastro literal da submissão da revisão.

### Aba de Compra

![Página de edição de revisão — aba de Compra](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Essa aba lista todos os pedidos em que o cliente comprou o produto revisado — número do pedido, data, total, status e o canal de compra para esse pedido. Se algum desses pedidos atingiu o status concluído (enviado ou entregue), você verá um aviso de confirmação de que esta é uma compra verificada — o mesmo sinal que define automaticamente **Compra Verificada** na aba de Revisão.

Se nenhum pedido correspondente aparecer aqui, o revisor comprou o produto antes de sua loja rastrear pedidos no Spwig, ou eles nunca realmente compraram — algo que vale a pena saber antes de decidir quão peso dar à revisão.

### Aba Avançada

Metadados que você raramente precisa tocar: **Contagem de Ajuda** (quantos clientes marcaram a revisão como útil), origem de importação se a revisão foi migrada de outra plataforma, e os carimbos de data/hora de criação/atualização.

## Dicas

Preserve todos os formatações de markdown, caminhos de imagens, blocos de código e termos técnicos.

- Verifique a lista **Aguardando Moderação** no painel de controle primeiro — é a forma mais rápida de ver o que precisa de uma decisão sem abrir a lista completa de avaliações
- Um grupo de avaliações com 1 estrela no mesmo produto no gráfico **Distribuição de Avaliações** é um sinal claro para investigar embalagem, qualidade do produto ou seu texto de lista
- Use o filtro **Verificado** ao decidir como lidar com avaliações duvidosas — o feedback de clientes com pedido confirmado tem mais peso em qualquer disputa
- Aprovar avaliações prontamente, incluindo as críticas — uma avaliação negativa visível sem resposta pode parecer pior do que uma reclamação resolvida, e avaliações que demoram a aparecer desencorajam os clientes a deixarem comentários futuros
- Não leia demais a **Jornada de Origem do Tráfego** ou o gráfico **Canal de Compra dos Avaliadores** do painel de controle — ambos descrevem como o cliente chegou e comprou, e não como ele chegou para escrever a avaliação
- Avaliações com fotos merecem uma análise mais atenta antes de serem aprovadas; fotos de produtos de clientes reais são alguns dos conteúdos mais persuasivos da sua loja
---
title: Avaliações de Produtos
---

As avaliações de produtos permitem que os clientes classifiquem e escrevam sobre sua experiência com um produto. As avaliações que você aprova aparecem na página do produto na sua loja, ajudando outros compradores a decidir o que comprar. O Spwig oferece controle total sobre quais avaliações são publicadas — nada é publicado até que você o aprove.

As avaliações ficam em **Produtos > Avaliações** na barra lateral, que se abre como um grupo: o link superior leva você ao **Painel de Avaliações**, e **Moderar Avaliações** leva você diretamente à lista de avaliações.

## O Painel de Avaliações

Navegue para **Produtos > Avaliações** para abrir o painel — uma visão geral em uma única tela de como as avaliações estão se comportando em sua loja.

![Painel de Avaliações](/static/core/admin/img/help/product-reviews/reviews-dashboard.webp)

No topo, seis cartões de KPI resumem sua atividade de avaliações:

| Cartão | O que mostra |
|---|---|
| **Total de Avaliações** | Todas as avaliações enviadas, aprovadas ou não |
| **Avaliação Média** | A classificação média de estrelas em todas as avaliações |
| **Pendente de Moderação** | Avaliações aguardando sua aprovação ou rejeição |
| **Taxa de Aprovação** | A proporção de todas as avaliações que você aprovou |
| **Compras Verificadas** | A proporção de avaliações feitas por clientes com um pedido confirmado para aquele produto |
| **Novas (30 dias)** | Avaliações enviadas nos últimos 30 dias |

Abaixo dos KPIs, três gráficos fornecem mais detalhes:

- **Distribuição de Avaliações** — um gráfico de barras de quantas avaliações caem em cada classificação de estrelas (1–5). Um agrupamento de avaliações de 1 estrela aqui merece investigação imediata.
- **Volume de Avaliações (12 semanas)** — um gráfico de linha de contagens de avaliações semana a semana, para que você possa identificar picos após uma promoção ou quedas que precisam de atenção.
- **Canal de Compra dos Avaliadores** — um gráfico de rosca do canal de marketing (direto, e-mail, busca paga, social orgânico, etc.) que impulsionou a *compra* por trás de cada avaliação. Isso reutiliza seus dados de atribuição e é genuinamente útil para ver quais canais trazem clientes que depois deixam avaliações — mas **não** é um registro de como o cliente encontrou o próprio formulário de avaliação. O Spwig não rastreia isso separadamente; veja "O que a jornada mostra e não mostra" mais adiante neste guia.

Duas listas completam o painel:

- **Produtos Mais Avaliados** — seus produtos mais avaliados, cada um com sua contagem de avaliações e avaliação média, com link direto para o produto.
- **Aguardando Moderação** — suas avaliações pendentes mais recentes, para que você possa pular diretamente para qualquer coisa que precise de uma decisão sem sair do painel.

## A lista de avaliações

Clique em **Moderar Avaliações** (ou **Produtos > Avaliações > Moderar Avaliações**) para ver cada avaliação como um cartão, com filtros acima da lista.

![Lista de Avaliações de Produtos com filtros e cartões de avaliação pendente](/static/core/admin/img/help/product-reviews/review-list.webp)

Cada cartão mostra a miniatura do produto, o título da avaliação, a classificação de estrelas, um selo **Aprovada**/**Pendente**, um selo **Compra Verificada** quando aplicável, uma prévia do comentário e quem o escreveu e quando.

### Filtrando avaliações

Use o painel de filtros para reduzir a lista:

- **Pesquisa** — corresponde ao nome do produto, nome de usuário do cliente ou título da avaliação
- **Classificação** — mostrar apenas avaliações com uma classificação de estrelas específica (útil para investigar reclamações de 1 estrela)
- **Aprovação** — separar rapidamente avaliações aprovadas de pendentes
- **Verificada** — filtrar para avaliações de clientes com um pedido confirmado para aquele produto

O filtramento é executado instantaneamente sem recarregar a página.

## Aprovando e rejeitando avaliações

As avaliações não são visíveis na sua loja até que você as aprove. Você pode aprovar ou rejeitar avaliações individualmente ou em massa.

### Ações em massa

1. Na lista de avaliações, marque as caixas de seleção ao lado das avaliações nas quais deseja agir
2. Selecione **Aprovar avaliações selecionadas** ou **Rejeitar avaliações selecionadas** do menu suspenso de ações
3. Clique em **Ir**

Esta é a maneira mais rápida de trabalhar com um lote de novas avaliações.

### Avaliação individual

1.

Clique no ícone de edição em um cartão de avaliação, ou em seu título, para abrir a avaliação
2.

Na aba **Revisão**, marque ou desmarque **Aprovação**
3.

Clique no botão de marca de seleção no cabeçalho para salvar

## Página de edição da revisão

Abrir uma revisão fornece uma visualização do tipo painel voltada para essa única revisão — um cabeçalho com o nome do produto, a classificação em estrelas, um selo **Aprovado**/**Pendente**, um selo **Compra Verificada** quando aplicável, quem escreveu a revisão e quando, e uma linha de estatísticas (**Classificação**, **Votos Úteis**, **Pedidos do Cliente**, **Gastos ao Longo da Vida**). Abaixo disso, os detalhes são organizados em quatro abas.

![Página de edição da revisão — aba Revisão com galeria de imagens](/static/core/admin/img/help/product-reviews/review-edit-review-tab.webp)

### Aba Revisão

É aqui que você moderará a própria revisão:

- **Imagens da revisão** — se o cliente anexou fotos, elas aparecem aqui como uma galeria de miniaturas; clique em qualquer miniatura para abrir a imagem em tamanho real em uma nova aba. Revisões com fotos são um sinal de confiança forte para os compradores, então vale a pena dar uma olhada antes de aprovar.
- **Classificação**, **Título**, **Comentário** — o conteúdo enviado pelo cliente
- **Aprovação** — controla se a revisão é visível na sua loja virtual
- **Compra Verificada** — sinaliza a revisão como vindo de um comprador confirmado; o Spwig define isso automaticamente quando existe um pedido concluído para o produto (consulte a aba **Compra**), mas você pode substituí-lo aqui, se necessário
- **Imagens** — a lista subjacente de URLs de imagem por trás da galeria acima; normalmente você não precisa tocar nisso, mas ele permanece editável para casos especiais (por exemplo, remover uma foto de uma revisão com várias imagens)

Você não pode editar a redação da revisão — aprovar ou rejeitar, e gerenciar as imagens, é o limite do que você controla aqui.

### Aba Cliente & Jornada

![Página de edição da revisão — aba Cliente & Jornada](/static/core/admin/img/help/product-reviews/review-edit-customer-tab.webp)

Essa aba fornece contexto sobre quem deixou a revisão: pedidos totais, quantas revisões eles já escreveram, sua classificação média dada, o quanto tempo eles são clientes e seus dados de contato, com um link para abrir o registro completo do cliente.

Logo abaixo está a **jornada de tráfego** — os canais, campanhas e referrers que trouxeram esse cliente para sua loja, puxados dos dados de atribuição e mostrados como uma linha do tempo.

#### O que a "jornada" faz e o que não faz

Leia esse cronograma como a **jornada de chegada e compra** desse cliente — como ele encontrou originalmente sua loja e foi adiante para comprar. Não é um registro da visita na qual ele escreveu essa revisão. O Spwig não rastreia onde o cliente estava, ou qual dispositivo ou sessão ele usou, no momento em que ele enviou a revisão. Se o cronograma mostrar "Email > skincare de verão" três semanas antes da data da revisão, isso indica que a campanha de email provavelmente impulsionou a *compra* — não diz nada sobre se o cliente voltou de um resultado de pesquisa, um marcador ou um email de follow-up para realmente deixar a revisão. Trate essa aba como contexto de marketing útil, e não como um rastro literal da submissão da revisão.

### Aba Compra

![Página de edição da revisão — aba Compra](/static/core/admin/img/help/product-reviews/review-edit-purchase-tab.webp)

Essa aba lista todos os pedidos nos quais o cliente comprou o produto revisado — número do pedido, data, total, status e o canal de compra para esse pedido. Se algum desses pedidos atingiu o status concluído (enviado ou entregue), você verá um aviso de confirmação de que esta é uma compra verificada — o mesmo sinal que define automaticamente **Compra Verificada** na aba Revisão.

Se nenhum pedido correspondente aparecer aqui, o revisor comprou o produto antes de sua loja rastrear pedidos no Spwig, ou eles nunca realmente compraram — algo que vale a pena saber antes de decidir quão peso dar à revisão.

### Aba Avançada

Metadados que você raramente precisa tocar: **Contagem de Ajuda** (quantos clientes marcaram a revisão como útil), origem de importação se a revisão foi migrada de outra plataforma e os carimbos de data/hora de criação/atualização.

## Dicas

Preserve todos os formatações de markdown, caminhos de imagens, blocos de código e termos técnicos.

- Verifique a lista **Aguardando Moderação** no painel de controle primeiro — é a maneira mais rápida de ver o que precisa de uma decisão sem abrir a lista completa de avaliações
- Um grupo de avaliações com 1 estrela no mesmo produto no gráfico **Distribuição de Avaliações** é um sinal claro para investigar embalagem, qualidade do produto ou seu texto de anúncio
- Use o filtro **Verificado** ao decidir como lidar com avaliações duvidosas — o feedback de clientes com pedido confirmado tem mais peso em qualquer disputa
- Aprovar avaliações prontamente, incluindo as críticas — uma avaliação negativa visível sem resposta pode parecer pior do que uma reclamação resolvida, e avaliações que demoram a aparecer desencorajam os clientes a deixarem comentários futuros
- Não leia demais a **Jornada de Origem do Tráfego** ou o gráfico **Canal de Compra dos Avaliadores** do painel de controle — ambos descrevem como o cliente chegou e comprou, e não como ele chegou para escrever a avaliação
- Avaliações com fotos merecem uma análise mais atenta antes de serem aprovadas; fotos de produtos de clientes reais são alguns dos conteúdos mais persuasivos da sua loja
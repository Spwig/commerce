---
title: Notificações de Estoque
---

As notificações de estoque permitem que os clientes se inscrevam para receber um e-mail quando um produto fora de estoque estiver disponível novamente. As configurações de exibição de estoque controlam o que os clientes veem nas páginas de produtos — como rótulos de status de estoque, avisos de estoque baixo e o que acontece quando um produto se esgota.

## Configurações de exibição de estoque

As configurações de exibição de estoque são padrões globais da loja que se aplicam a todos os produtos, a menos que sejam substituídas no nível de categoria ou produto.

Navegue até **Catálogo > Configurações de Exibição de Estoque** para configurar essas opções. Há um registro de configurações para sua loja — clique nele para editar.

### Exibição do status do estoque

| Configuração | Descrição |
|---------|-------------|
| **Mostrar Status do Estoque** | Exibe os rótulos "Em Estoque" ou "Fora de Estoque" nas páginas de produtos |
| **Mostrar Aviso de Estoque Baixo** | Exibe a mensagem "Apenas X restante" quando o estoque estiver baixo |
| **Limite de Estoque Baixo** | A quantidade em que ou abaixo da qual o aviso de estoque baixo aparece (padrão: 5) |
| **Mostrar Quantidade Exata** | Exibe o número exato restante (ex.: "Apenas 3 restante!") em vez de um aviso genérico |

### Comportamento fora de estoque

A configuração **Ação Fora de Estoque** determina o que os clientes veem quando um produto não tem estoque disponível:

| Ação | O que os clientes veem |
|--------|-------------------|
| **Ocultar da lista** | O produto é removido das páginas de categoria e resultados de pesquisa |
| **Mostrar como indisponível** | O produto está visível, mas não pode ser adicionado ao carrinho |
| **Mostrar botão "Notifique-me"** | Os clientes podem registrar seu e-mail para ser notificado quando o estoque retornar |
| **Permitir pedidos com estoque zero** | Os clientes podem comprar o produto mesmo quando o estoque estiver zero |

Defina **Mensagem Fora de Estoque** para personalizar o texto exibido quando um produto estiver indisponível (padrão: `Fora de Estoque`).

Defina **Mensagem de Pedido com Estoque Zero** para personalizar o texto exibido para produtos com pedido com estoque zero (padrão: `Disponível com pedido com estoque zero`).

### Exibição de envio e entrega

| Configuração | Descrição |
|---------|-------------|
| **Mostrar local de envio** | Exibe o nome do depósito na página do produto |
| **Mostrar data estimada de entrega** | Exibe as datas estimadas de entrega calculadas com base na localização do depósito |

### Permitir pedidos com estoque zero (em toda a loja)

Marque **Permitir pedidos com estoque zero** para permitir que os clientes comprem qualquer produto fora de estoque por padrão. Produtos individuais e categorias podem substituir essa configuração.

## Notificações de volta ao estoque

Quando você define a ação fora de estoque para **Mostrar botão "Notifique-me"**, os clientes podem inserir seu endereço de e-mail na página do produto para receber um e-mail quando o produto for reabastecido.

### Visualizar solicitações de notificação

Navegue até **Catálogo > Notificações de Estoque** para ver todas as solicitações de notificação dos clientes. Cada registro mostra:
- Endereço de e-mail do cliente
- Produto e variante (se aplicável)
- Depósito preferido (se o cliente selecionou uma preferência regional)
- Quando a solicitação foi criada
- Quando a notificação foi enviada (em branco se ainda não foi enviada)

### Quando as notificações são enviadas

O Spwig envia automaticamente e-mails de volta ao estoque quando o nível de estoque de um produto sobe acima de zero. O campo **Notificado em** registra quando o e-mail foi enviado.

Os clientes recebem um e-mail de notificação. Uma vez notificados, eles precisam se inscrever novamente se o produto sair do estoque novamente.

### Filtros de solicitações de notificação

Use os filtros do administrador para encontrar:
- Solicitações para um produto específico
- Solicitações que já foram notificadas (para ver quem foi contatado)
- Solicitações que ainda estão pendentes (clientes aguardando o reabastecimento)

## Sobrescritas no nível do produto

As configurações de exibição de estoque em toda a loja podem ser sobrescritas por produto ou categoria. Na forma de edição do produto, procure a seção **Estoque** onde você pode definir uma ação específica de **Fora de Estoque** para o produto, diferente do padrão global.

Isso é útil quando você deseja que a maioria dos produtos permita pedidos com estoque zero, mas manter alguns produtos definidos como "Notifique-me" — ou quando um produto específico deve ser ocultado quando estiver fora de estoque.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- Defina o **Limiar de Estoque Baixo** para o ponto de reposição que normalmente usa, para que os clientes sejam avisados sobre a disponibilidade limitada antes que você fique totalmente sem estoque.
- Use a opção **Mostrar o botão "Notifique-me"** em vez de ocultar produtos fora de estoque — os clientes que se inscrevem representam uma demanda real que pode justificar um pedido de reposição.
- Ative **Mostrar a Quantidade Exata** com parcimônia.

Para a maioria das lojas, mostrar "Apenas 3 restantes!" funciona melhor do que mostrar o número exato, pois cria urgência sem revelar sua imagem completa de estoque.
- Verifique a lista de notificações de estoque antes de colocar um novo pedido — o número de solicitações de notificação pendentes informa você sobre a quantidade de demanda por esse produto.
- Se você usar pedidos com backorder, atualize sua **Mensagem de Backorder** para estabelecer expectativas precisas (ex.: "Envio em 2-3 semanas — compre agora para reservar sua posição").
- Combine notificações de produtos fora de estoque com marketing por e-mail: quando você reposicionar um produto popular, envie uma campanha para todos que se inscreveram, e não apenas o e-mail de notificação automática.
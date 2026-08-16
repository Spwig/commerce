---
title: Notificações de Estoque
---

As notificações de estoque permitem que os clientes se inscrevam para receberem e-mails quando um produto com estoque esgotado estiver disponível novamente. As configurações de exibição de estoque controlam o que os clientes veem nas páginas de produtos — como rótulos de status de estoque, alertas de estoque baixo e o que acontece quando um produto se esgota.

## Configurações de exibição de estoque

As configurações de exibição de estoque são padrões para toda a loja que se aplicam a todos os produtos, a menos que sejam substituídas no nível da categoria ou produto.

Navegue até **Catálogo > Configurações de Exibição de Estoque** para configurar essas opções. Há um registro de configurações para sua loja — clique nele para editar.

### Exibição do status de estoque

| Configuração | Descrição |
|---------|-------------|
| **Mostrar status de estoque** | Exibe rótulos "Em Estoque" ou "Esgotado" nas páginas de produtos |
| **Mostrar alerta de estoque baixo** | Exibe uma mensagem "Ainda restam X" quando o estoque estiver acabando |
| **Limite de estoque baixo** | A quantidade a partir da qual o alerta de estoque baixo aparece (padrão: 5) |
| **Mostrar quantidade exata** | Exibe o número exato restante (por exemplo, "Ainda restam 3!") em vez de um alerta genérico |

### Comportamento de estoque esgotado

A configuração **Ação de Estoque Esgotado** determina o que os clientes veem quando um produto não tem estoque disponível:

| Ação | O que os clientes veem |
|--------|-------------------|
| **Esconder das listagens** | O produto é removido das páginas da categoria e resultados da pesquisa |
| **Mostrar como indisponível** | O produto é visível, mas não pode ser adicionado ao carrinho |
| **Mostrar botão "Notifique-me"** | Os clientes podem se cadastrar com seu e-mail para serem notificados quando o estoque voltar |
| **Permitir encomendas de volta** | Os clientes podem comprar o produto mesmo quando o estoque estiver zerado |

Defina **Mensagem de Encomenda de Volta** para personalizar o texto mostrado quando um produto estiver indisponível (padrão: `Esgotado`).

Defina **Mensagem de Encomenda de Volta** para personalizar o texto mostrado para produtos com encomendas de volta (padrão: `Disponível para encomenda de volta`).

### Exibição de envio e entrega

| Configuração | Descrição |
|---------|-------------|
| **Mostrar local "Envia a partir de"** | Exibe o nome do armazém na página do produto |
| **Mostrar data de entrega estimada** | Exibe datas estimadas de entrega calculadas a partir da localização do armazém |

### Permitir encomendas de volta (em toda a loja)

Marque **Permitir Encomendas de Volta** para permitir que os clientes comprem qualquer produto esgotado por padrão. Produtos e categorias individuais podem substituir esse recurso.

## Notificações de reposição em estoque

Quando você define a ação de estoque esgotado para **Mostrar botão "Notifique-me"**, os clientes podem inserir seu endereço de e-mail na página do produto para receber um e-mail quando o produto estiver em estoque novamente.

### Visualizando solicitações de notificação

Navegue até **Catálogo > Notificações de Estoque** para ver todos os pedidos de notificação dos clientes. Cada registro mostra:
- O endereço de e-mail do cliente
- Produto e variante (se aplicável)
- Armazém preferido (se o cliente tiver selecionado uma preferência regional)
- Quando o pedido foi criado
- Quando a notificação foi enviada (vazio se ainda não enviada)

### Quando as notificações são enviadas

O Spwig envia e-mails automaticamente quando o nível de estoque de um produto ultrapassa zero. O campo **Notificado às** registra quando o e-mail foi enviado.

Os clientes recebem um e-mail de notificação. Após serem notificados, eles precisam se inscrever novamente se o produto esgotar novamente.

### Filtros de solicitações de notificação

Use os filtros do administrador para encontrar:
- Pedidos para um produto específico
- Pedidos que já foram notificados (para ver quem foi contatado)
- Pedidos que ainda estão pendentes (clientes aguardando reposição)

## Sobrescrita de nível de produto

As configurações de exibição de estoque em toda a loja podem ser substituídas por produto ou categoria. Na forma de edição de produto, procure a seção **Estoque** onde você pode definir uma **Ação de Estoque Esgotado** específica do produto que difira do padrão global.

Isso é útil quando você quer que a maioria dos produtos permita encomendas de volta, mas mantenha alguns produtos definidos para "Notifique-me" — ou quando um produto específico deve ser escondido quando estiver fora de estoque.

## Dicas

Preserve todos os formatações de markdown, caminhos de imagens, blocos de código e termos técnicos.

- Defina o **Limite de Estoque Baixo** para o ponto de reposição que você costuma usar, para que os clientes sejam alertados sobre a disponibilidade limitada antes que você fique sem estoque completamente.
- Use a opção **Mostrar o botão "Notifique-me"** em vez de esconder os produtos sem estoque — os clientes que se inscrevem representam demanda real que pode justificar uma reposição.
- Ative a **Mostrar Quantidade Exata** com parcimônia.

Para a maioria dos lojistas, mostrar "Apenas 3 restantes!" funciona melhor do que mostrar o número exato, pois cria urgência sem revelar a imagem completa do seu estoque.
- Verifique a lista de notificações de estoque antes de fazer um novo pedido — o número de solicitações pendentes de notificação lhe diz quanta demanda existe por aquele produto.
- Se você usar encomendas de volta, atualize sua **Mensagem de Encomenda de Volta** para estabelecer expectativas precisas (ex.: "Envio em 2-3 semanas — compre agora para reservar seu lugar).
- Combine notificações de estoque esgotado com marketing por e-mail: quando você repor um produto popular, envie uma campanha para todos os que se inscreveram, e não apenas o e-mail de notificação automática.
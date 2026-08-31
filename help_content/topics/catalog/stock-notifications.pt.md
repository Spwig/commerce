---
title: Notificações de Estoque
---

As notificações de estoque permitem que os clientes se inscrevam para receber um e-mail quando um produto esgotado voltar a ficar disponível. As configurações de exibição de estoque controlam o que os clientes veem nas páginas de produto — como rótulos de status de estoque, avisos de baixo estoque e o que acontece quando um produto fica sem estoque.

## Configurações de exibição de estoque

As configurações de exibição de estoque são padrões da loja que se aplicam a todos os produtos, a menos que sejam substituídos no nível da categoria ou do produto.

Navegue até **Catálogo > Configurações de Exibição de Estoque** para configurar essas opções. Existe um registro de configurações para a sua loja — clique nele para editar.

### Exibição do status de estoque

| Configuração | Descrição |
|---------|-------------|
| **Mostrar Status de Estoque** | Exibe os rótulos "Em Estoque" ou "Sem Estoque" nas páginas de produto |
| **Mostrar Aviso de Baixo Estoque** | Exibe a mensagem "Só restam X" quando o estoque está baixo |
| **Limite de Baixo Estoque** | A quantidade em ou abaixo da qual o aviso de baixo estoque aparece (padrão: 5) |
| **Mostrar Quantidade Exata** | Mostra o número exato restante (ex.: "Só restam 3!") em vez de um aviso genérico |

### Comportamento sem estoque

A configuração **Ação Sem Estoque** determina o que os clientes veem quando um produto não tem estoque disponível:

| Ação | O que os clientes veem |
|--------|-------------------|
| **Ocultar das listagens** | O produto é removido das páginas de categoria e dos resultados de busca |
| **Mostrar como indisponível** | O produto é visível, mas não pode ser adicionado ao carrinho |
| **Mostrar botão "Avise-me"** | Os clientes podem registrar seu e-mail para serem notificados quando o estoque voltar |
| **Permitir encomendas futuras** | Os clientes podem comprar o produto mesmo quando o estoque é zero |

Defina **Mensagem Sem Estoque** para personalizar o texto exibido quando um produto está indisponível (padrão: `Sem Estoque`).

Defina **Mensagem de Encomenda Futura** para personalizar o texto exibido para produtos com encomenda futura (padrão: `Disponível em encomenda futura`).

### Exibição de envio e entrega

| Configuração | Descrição |
|---------|-------------|
| **Mostrar local de "Enviado de"** | Exibe o nome do armazém na página do produto |
| **Mostrar Entrega Estimada** | Exibe as datas de entrega estimadas calculadas a partir da localização do armazém |

### Permitir encomendas futuras (em toda a loja)

Marque **Permitir Encomendas Futuras** para permitir que os clientes comprem qualquer produto sem estoque por padrão. Produtos e categorias individuais podem substituir essa configuração.

## Notificações de reposição de estoque

Quando você define a ação sem estoque como **Mostrar botão "Avise-me"**, os clientes podem inserir seu endereço de e-mail na página do produto para receber um e-mail quando o produto for reabastecido.

### Visualizar solicitações de notificação

Navegue até **Catálogo > Notificações de Estoque** para ver todas as solicitações de notificação dos clientes. Cada registro mostra:
- Endereço de e-mail do cliente
- Produto e variante (se aplicável)
- Armazém preferido (se o cliente selecionou uma preferência regional)
- Quando a solicitação foi criada
- Quando a notificação foi enviada (vazio se ainda não foi enviada)

### Quando as notificações são enviadas

O Spwig envia e-mails de reposição de estoque automaticamente quando o nível de estoque de um produto sobe acima de zero. O campo **Notificado Em** registra quando o e-mail foi enviado.

Os clientes recebem um e-mail de notificação. Uma vez notificados, eles precisam se inscrever novamente se o produto ficar sem estoque uma segunda vez.

Se você preferir enviar mais do que um simples alerta — por exemplo, mostrando o produto reabastecido com um bloco de conteúdo **Produto em Destaque**, ou fazendo um acompanhamento um dia depois — crie uma jornada **Produto de volta ao estoque** em **Estúdio de Campanhas > Jornadas** e defina como **Ativa**. Uma vez que essa jornada exista, os clientes em espera são inscritos nela em vez de receberem o e-mail único simples; sem uma jornada ativa, esse e-mail único continua sendo enviado exatamente como descrito acima. Veja [Jornadas Disparadas](/help/triggered-journeys) para saber como o gatilho funciona.

### Filtrar solicitações de notificação

Use os filtros do administrador para encontrar:
- Solicitações para um produto específico
- Solicitações que já foram notificadas (para ver quem foi contatado)
- Solicitações que ainda estão pendentes (clientes aguardando reabastecimento)

## Sobrescritas no nível do produto

As configurações de exibição de estoque do site podem ser sobrescritas por produto ou categoria. No formulário de edição do produto, procure a seção **Estoque**, onde você pode definir uma **Ação de Esgotamento** específica para o produto que difira do padrão global.

Isso é útil quando você deseja que a maioria dos produtos permita pedidos de reserva, mas mantenha alguns produtos configurados como "Avise-me" — ou quando um produto específico deve ser ocultado quando estiver esgotado.

## Dicas

- Defina o **Limite de Estoque Baixo** para o ponto de reposição que você normalmente utiliza, para que os clientes sejam alertados sobre a disponibilidade limitada antes que o estoque se esgote completamente.
- Use a opção **Mostrar botão "Avise-me"** em vez de ocultar produtos esgotados — os clientes que se cadastram representam uma demanda real que pode justificar um pedido de reposição.
- Ative o **Mostrar Quantidade Exata** com moderação. Para a maioria das lojas, exibir "Só restam 3!" funciona melhor do que mostrar o número exato, pois cria urgência sem revelar sua situação completa de inventário.
- Verifique a lista de notificações de estoque antes de fazer um novo pedido — o número de solicitações de notificação pendentes indica a quantidade de demanda existente para aquele produto.
- Se você usa pedidos de reserva, atualize sua **Mensagem de Reserva** para definir expectativas precisas (por exemplo, "Envio em 2-3 semanas — faça seu pedido agora para reservar seu lugar").
- Combine as notificações de esgotamento com o marketing por e-mail: quando você repor um produto popular, envie uma campanha para todos que se cadastraram, não apenas o e-mail de notificação automático.
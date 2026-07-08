---
title: Gerenciamento de Pedidos
---

Este guia abrange tudo o que você precisa para gerenciar pedidos de clientes — desde a revisão de novos pedidos até o processamento de envios e tratamento de reembolsos.

## Lista de Pedidos

Navegue até **Pedidos > Todos os Pedidos** na barra lateral para ver todos os pedidos. A lista mostra o número, status, cliente, total e data de cada pedido.

![Order list](/static/core/admin/img/help/manage-orders/order-list.webp)

Use os filtros na parte superior para refinar os pedidos por status, intervalo de datas ou pesquise por número de pedido ou nome do cliente.

## Detalhes do Pedido

Clique em qualquer pedido para abrir sua página de detalhes. Aqui você encontrará todas as informações sobre o pedido organizadas em seções claras.

![Order detail](/static/core/admin/img/help/manage-orders/order-detail.webp)

### Informações do Pedido

A seção superior mostra:

- **Número do Pedido** — O identificador único deste pedido
- **Status** — Status atual do pedido (Pendente, Em Processamento, Enviado, Entregue, Concluído, Cancelado)
- **Cliente** — Nome e email do cliente que realizou o pedido
- **Criado em** — Quando o pedido foi realizado

### Itens do Pedido

A seção de itens lista tudo o que o cliente pediu:

- Nome do produto e SKU
- Quantidade solicitada
- Preço unitário e total da linha
- Quaisquer descontos aplicados

### Detalhes do Pagamento

Mostra o método de pagamento utilizado, ID da transação e status do pagamento. Para pedidos aguardando pagamento, você pode acompanhar o status do gateway de pagamento aqui.

### Endereço de Envio

O endereço de entrega do cliente. Se o endereço de cobrança for diferente, ambos são exibidos.

## Ciclo de Vida do Pedido

Os pedidos normalmente passam por estes status:

1. **Pendente** — Novo pedido recebido, aguardando confirmação de pagamento
2. **Em Processamento** — Pagamento confirmado, preparando para envio
3. **Enviado** — Pedido despachado com informações de rastreamento
4. **Entregue** — Cliente recebeu o pedido
5. **Concluído** — Pedido finalizado

## Processando um Pedido

### 1. Revisar o Pedido

Verifique se:

- Os itens e quantidades estão corretos
- O endereço de envio está completo
- O pagamento foi recebido
- Quaisquer observações do cliente foram atendidas

### 2. Criar um Envio

Para enviar o pedido:

1. Clique em **Criar Envio** na página de detalhes do pedido
2. Selecione quais itens incluir (para envios parciais, selecione apenas alguns itens)
3. Escolha a transportadora e o serviço de envio
4. Insira o número de rastreamento
5. Clique em **Salvar Envio**

O status do pedido é atualizado automaticamente para **Enviado** e o cliente recebe um email de notificação de envio com informações de rastreamento.

### 3. Marcar como Entregue

Quando o cliente confirmar a entrega ou o rastreamento mostrar que foi entregue, atualize o status para **Entregue** e depois **Concluído**.

## Ações do Pedido

### Adicionando Notas

Adicione notas internas ou mensagens visíveis ao cliente:

1. Role até a seção **Notas** na página de detalhes do pedido
2. Digite sua mensagem
3. Escolha se é uma nota interna (apenas equipe) ou uma notificação ao cliente
4. Clique em **Adicionar Nota**

Notas visíveis ao cliente acionam uma notificação por email.

### Processando um Reembolso

Para emitir um reembolso:

1. Clique em **Reembolso** na página de detalhes do pedido
2. Selecione os itens a reembolsar (ou insira um valor personalizado)
3. Escolha um motivo para o reembolso
4. Confirme o reembolso

Os reembolsos são processados pelo gateway de pagamento original. O cliente recebe uma confirmação por email.

### Cancelando um Pedido

Para cancelar:

1. Clique em **Cancelar Pedido**
2. Selecione um motivo de cancelamento
3. Escolha se deseja reabastecer os itens
4. Confirme

O cliente é notificado automaticamente e um reembolso é iniciado se o pagamento já tiver sido realizado.

## Ações em Massa

Na lista de pedidos, você pode selecionar vários pedidos e aplicar ações em massa:

- **Atualizar status** — Mover vários pedidos para o mesmo status
- **Exportar** — Baixar os pedidos selecionados como CSV
- **Imprimir** — Gerar romaneios de envio ou faturas

## Notificações de Pedido

Os clientes recebem emails automaticamente em etapas importantes:

- **Confirmação do pedido** — Imediatamente após realizar o pedido
- **Pagamento recebido** — Quando o pagamento é confirmado
- **Notificação de envio** — Quando um envio é criado (inclui link de rastreamento)
- **Confirmação de entrega** — Quando marcado como entregue

Configure os modelos de email em **Configurações > Configuração de Email**.

## Dicas

- Processe os pedidos diariamente para manter tempos de envio rápidos.
- Use os filtros de status para focar nos pedidos que precisam de atenção (Pendente e Em Processamento).
- Adicione notas internas para rastrear quaisquer requisitos especiais de manuseio.
- Para períodos de alto volume, use ações em massa para atualizar vários pedidos de uma vez.
- Configure regras de envio para automatizar a seleção de transportadora com base no peso do pedido e no destino.

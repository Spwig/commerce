---
title: Visão Geral de Webhooks
---

Webhooks permitem que sua loja notifique automaticamente sistemas externos — como ferramentas de estoque, ERPs, serviços de fulfillment ou aplicações personalizadas — sempre que algo acontecer em sua loja. Em vez desses sistemas perguntarem repetidamente "algo mudou?", sua loja envia uma notificação no momento em que um evento ocorre.

## O que webhooks fazem

Quando um evento acontece em sua loja (uma ordem é colocada, um pagamento é recebido, um produto sai do estoque), o Spwig envia uma solicitação HTTP POST com os dados do evento para uma URL que você configura. O sistema que recebe pode então agir imediatamente com esses dados — por exemplo, atualizar o estoque, disparar um rótulo de envio ou enviar uma notificação personalizada.

Usos comuns para webhooks incluem:

- Sincronizar pedidos em tempo real com um parceiro de fulfillment
- Atualizar o estoque em um ERP quando o estoque mudar
- Disparar notificações por SMS ou push para mudanças no status do pedido
- Registrar eventos em um data warehouse para relatórios
- Conectar-se a ferramentas de automação como Zapier ou Make

## Visualizando e gerenciando endpoints

Navegue até **Integrações > Webhooks** para ver todos os endpoints de webhook configurados.

![Lista de endpoints de webhook](/static/core/admin/img/help/webhooks-overview/endpoint-list.webp)

A lista mostra o nome de cada endpoint, a URL, o status ativo, quantos eventos ele se inscreve, seu status de saúde e quando ele recebeu a última entrega.

### Indicadores de saúde

A coluna **Saúde** mostra, de forma rápida, como cada endpoint está se comportando:

- **Saudável** — Todas as entregas recentes foram bem-sucedidas
- **Degradado** — Algumas falhas recentes, mas o endpoint ainda está ativo
- **Não saudável / Desativado** — O endpoint foi desativado automaticamente após muitas falhas consecutivas (10 por padrão). Você deve reativá-lo manualmente após resolver o problema subjacente.

## Criando um endpoint de webhook

Clique em **+ Adicionar Endpoint de Webhook** para abrir o assistente de configuração. O assistente o guiará por quatro etapas.

### Etapa 1: Informações básicas

- **Nome** — Um rótulo amigável para identificar esse endpoint (ex.: `Serviço de Fulfillment de Pedidos` ou `Sincronização de Estoque`).
- **URL** — O URL completo do servidor que receberá as solicitações POST de webhook. Isso deve ser acessível publicamente (não um URL de localhost).
- **Descrição** — Notas opcionais sobre o que esse endpoint é usado.
- **Ativo** — Se esse endpoint deve receber entregas. Desmarque para pausar temporariamente sem excluir o endpoint.

### Etapa 2: Assinaturas de eventos

Escolha quais eventos devem disparar uma entrega para esse endpoint. Os eventos estão agrupados por categoria:

### Eventos de pedido

| Evento | Quando ele é disparado |
|-------|---------------|
| `order.created` | Um novo pedido é colocado |
| `order.paid` | O pagamento de um pedido é confirmado |
| `order.cancelled` | Um pedido é cancelado |
| `order.fulfilled` | Todos os itens de um pedido são enviados |
| `order.partially_fulfilled` | Alguns itens de um pedido são enviados |
| `order.status_changed` | O status do pedido muda |
| `order.note_added` | Uma nota é adicionada a um pedido |

### Eventos de pagamento

| Evento | Quando ele é disparado |
|-------|---------------|
| `payment.received` | Um pagamento é recebido |
| `payment.failed` | Um tentativa de pagamento falha |
| `payment.pending` | Um pagamento está aguardando confirmação |

### Eventos de envio

| Evento | Quando ele é disparado |
|-------|---------------|
| `shipment.created` | Um envio é criado |
| `shipment.shipped` | Um envio é despachado |
| `shipment.delivered` | Um envio é entregue |
| `shipment.returned` | Um envio é devolvido |
| `shipment.tracking_updated` | Informações de rastreamento são atualizadas |

### Eventos de estoque

| Evento | Quando ele é disparado |
|-------|---------------|
| `inventory.low_stock` | O estoque cai abaixo do limite |
| `inventory.out_of_stock` | Um produto sai do estoque |
| `inventory.restocked` | Um produto é reabastecido |
| `inventory.adjusted` | O estoque é ajustado manualmente |

### Eventos de produto

`product.created`, `product.updated`, `product.deleted`, `product.published`, `product.unpublished`

### Eventos de cliente


customer.created", "customer.updated", "customer.deleted

#### Eventos de assinatura

subscription.created", "subscription.activated", "subscription.renovada", "subscription.cancelada", "subscription.expirada", "subscription.pausada", "subscription.resumida", "subscription.pagamento_falhou

#### Outros eventos

refund.created", "refund.concluída", "refund.falhou", "cart.abandonado", "cart.recuperado", "translation.job_completed", "translation.job_failed

Para receber todos os eventos, inscreva-se em `*` (wildcard). Isso é útil para pontos de extremidade de log de propósito geral, mas gera mais tráfego — inscreva-se apenas nos eventos que realmente precisa para integrações de produção.

### Etapa 3: Configuração

- **Máximo de tentativas** — Quantas vezes o Spwig deve tentar entregar novamente uma entrega falha antes de desistir (padrão: 5). Cada tentativa usa um espaçamento com back-off exponencial.
- **Tempo limite (segundos)** — Quanto tempo esperar pela resposta do servidor de recebimento antes de marcar a entrega como falha (padrão: 30 segundos). Aumente esse valor apenas se seu servidor for conhecido por ser lento.

### Etapa 4: Segurança

Cada ponto de extremidade de webhook recebe uma chave de **segredo de assinatura** gerada automaticamente — uma chave aleatória de 64 caracteres. O Spwig usa esse segredo para assinar cada payload de webhook com uma assinatura HMAC-SHA256.

A assinatura é incluída no cabeçalho de solicitação `X-Webhook-Signature`. Seu servidor de recebimento deve verificar essa assinatura para confirmar que a solicitação realmente veio de sua loja e não foi manipulada.

O segredo é exibido mascarado no administrador. Para ver ou rotacionar o segredo, use a API do Spwig. Rotacione seu segredo imediatamente se suspeitar que ele foi comprometido.

## Habilitar e desabilitar pontos de extremidade

Para habilitar ou desabilitar rapidamente um ou mais pontos de extremidade sem abrir cada um:

1. Selecione as caixas de seleção ao lado dos pontos de extremidade que deseja alterar
2. Use o menu suspenso **Ação** para escolher **Habilitar os pontos de extremidade selecionados** ou **Desabilitar os pontos de extremidade selecionados**
3. Clique em **Ir**

Para reativar um ponto de extremidade que foi desabilitado automaticamente por falhas, selecione-o e use a ação **Redefinir contador de falhas**, depois habilite-o novamente. Corrija o que causou as falhas primeiro, caso contrário, ele será desabilitado novamente rapidamente.

## Dicas

- Inscreva-se apenas nos eventos que realmente precisa — eventos desnecessários criam ruído em seus logs e aumentam a carga de entrega.
- Sempre verifique a assinatura do webhook em seu servidor de recebimento antes de processar o payload. Isso protege você contra solicitações falsificadas.
- Use o campo **Descrição** para registrar qual sistema ou integração esse ponto de extremidade conecta. Isso ajuda ao solucionar problemas meses depois.
- Defina um **Tempo limite** ligeiramente acima do tempo de resposta típico do seu servidor. Um tempo limite de 10–15 segundos é suficiente para a maioria das integrações.
- Se um ponto de extremidade tornar-se **Inadequado**, verifique primeiro os logs de entrega (veja **Entregas de Webhook**) para entender o padrão de falha antes de reativá-lo.
- Para testes, direcione webhooks para uma ferramenta como [webhook.site](https://webhook.site) para inspecionar os payloads brutos sem precisar de um servidor em funcionamento.
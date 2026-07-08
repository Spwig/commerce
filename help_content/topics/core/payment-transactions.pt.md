---
title: Transações de Pagamento
---

As transações de pagamento são o registro completo de cada evento de pagamento processado por meio da sua loja — cobranças, estornos, autorizações e muito mais. Esta seção também inclui logs de webhooks dos seus provedores de pagamento e intenções de pagamento criadas durante o checkout.

## Transações de pagamento

Navegue até **Pagamentos > Transações de Pagamento** para ver todas as transações processadas pela sua loja.

### Tipos de transação

| Tipo | O que significa |
|------|--------------|
| **Cobrança** | Um pagamento imediato — os fundos são coletados no momento da transação |
| **Autorização** | Os fundos são retidos no cartão do cliente, mas ainda não foram coletados |
| **Captura** | Coleta os fundos de uma autorização anterior |
| **Cancelar** | Cancela uma autorização antes que ela seja capturada |
| **Estorno** | Devolve o pagamento ao cliente |

### Status de transação

| Status | O que significa |
|--------|--------------|
| **Pendente** | A transação foi iniciada, mas ainda não foi processada |
| **Processando** | Estando em processamento pelo provedor de pagamento |
| **Autorizado** | Os fundos estão retidos — aguardando captura |
| **Concluído** | O pagamento foi bem-sucedido |
| **Falhou** | O pagamento foi recusado ou ocorreu um erro |
| **Cancelado** | A autorização foi cancelada antes da captura |
| **Estornado** | Um estorno completo foi emitido |
| **Estornado Parcialmente** | Parte do pagamento foi devolvida |

### O que você pode ver em um registro de transação

Cada transação mostra:
- **ID da transação** — referência interna do Spwig
- **ID da transação do provedor** — a referência do seu provedor de pagamento (ex.: ID de cobrança do Stripe)
- **Valor** — o valor da transação e a moeda
- **Status** e **Tipo**
- **E-mail do cliente** e **Nome do cliente**
- **Método de pagamento** — tipo (cartão de crédito, transferência bancária, etc.) e últimos 4 dígitos
- **Pedido** — o pedido ao qual esta transação pertence
- **Conta do provedor** — qual provedor de pagamento processou
- **Resposta do provedor** — a resposta técnica bruta do provedor de pagamento
- **Mensagem de erro** — se a transação falhou, o motivo fornecido pelo provedor
- Carimpos de criação, última atualização e conclusão

### Filtros de transações

Use os filtros do administrador para reduzir as transações por:
- Status (ex.: mostrar apenas transações falhadas)
- Tipo (ex.: mostrar apenas estornos)
- Conta do provedor
- Intervalo de data

Isso é útil para reconciliação no final do dia ou investigar o histórico de pagamento de um cliente específico.

### Quando uma transação pode ser estornada?

Uma transação pode ser estornada quando:
- Seu status é **Concluído**
- Seu tipo é **Cobrança** ou **Captura**

Para emitir um estorno, use a ação **Estorno** na página de detalhes do pedido. Estornos processados por meio do pedido criam um novo registro de transação do tipo **Estorno**.

### Fluxo de autorização e captura

Alguns métodos de pagamento (e alguns provedores de pagamento) suportam autorização e captura separadas. Isso é útil se você quiser verificar o pagamento antes de enviar o produto:

1. **Autorizar** — Os fundos são retidos no cartão do cliente (status: `Autorizado`)
2. **Capturar** — Acionado quando o pedido é enviado ou concluído
3. Se não for capturado dentro do período de autorização, o bloqueio **expira** automaticamente

O campo **Expira em** na transação mostra quando uma autorização vai expirar.

## Webhooks de pagamento

Os provedores de pagamento enviam eventos de webhook para notificar sua loja sobre alterações no status do pagamento — por exemplo, quando um pagamento é bem-sucedido, falha ou uma disputa é levantada. O Spwig registra todos os webhooks recebidos.

Navegue até **Pagamentos > Webhooks de Pagamento** para visualizar o log.

### O que os registros de webhook mostram

| Campo | Descrição |
|-------|-------------|
| **Fornecedor** | Qual provedor de pagamento enviou o webhook |
| **ID do Evento** | O identificador único do evento do provedor |
| **Tipo de Evento** | O tipo de evento (ex.: `payment_intent.succeeded`, `charge.refunded`) |
| **Processado** | Se o Spwig agiu sobre este webhook |
| **Assinatura Verificada** | Se a assinatura de segurança do webhook foi válida |
| **Payload** | Os dados completos enviados pelo provedor |
| **Resultado do Processamento** | O que o Spwig fez em resposta |
| **Erro de Processamento** | Quaisquer erros que ocorreram durante o processamento |
| **Recebido em** | Quando o webhook chegou |

### Usando logs de webhook para solução de problemas

Se um pagamento parecer travado ou o status do pedido não atualizar após o pagamento:

1. Navegue até **Pagamentos > Webhooks de Pagamento**
2. Filtrar por provedor e procurar por eventos recentes
3. Verifique a coluna **Processado** — um webhook não processado pode indicar um problema de entrega
4. Verifique **Assinatura Verificada** — uma assinatura falhada pode significar que seu segredo de webhook está mal configurado
5. Revise **Erro de Processamento** para quaisquer mensagens de erro

Eventos duplicados são tratados automaticamente — o `ID do Evento` e a combinação do provedor são únicos, então o mesmo webhook não pode ser processado duas vezes.

## Intenções de pagamento

Uma intenção de pagamento acompanha o ciclo de vida de um pagamento de checkout do momento em que o cliente começa o processo de pagamento até o resultado final. As intenções de pagamento são criadas automaticamente quando um cliente chega à etapa de pagamento no checkout.

Navegue até **Pagamentos > Intenções de Pagamento** para visualizar a lista.

### Status de intenção de pagamento

| Status | Significado |
|--------|---------|
| **Criado** | A intenção foi criada, aguardando o método de pagamento |
| **Requer Método de Pagamento** | Aguardando que o cliente insira seus detalhes do cartão |
| **Requer Confirmação** | Detalhes do pagamento inseridos, aguardando confirmação |
| **Requer Ação** | O cliente precisa completar uma ação (ex.: autenticação 3D Secure) |
| **Em Processamento** | O pagamento está sendo processado |
| **Concluído** | Pagamento concluído com sucesso |
| **Cancelado** | O pagamento foi abandonado ou cancelado |
| **Falhou** | Tentativa de pagamento falhou |

### Fluxo de intenção de pagamento para pedido

1. O cliente chega à etapa de pagamento do checkout → o Spwig cria uma **Intenção de Pagamento** e um rascunho de **Pedido** (não pago)
2. O cliente insere os detalhes do pagamento e confirma
3. O provedor de pagamento processa o pagamento
4. No sucesso, o Pedido é atualizado para **Pago** e a Intenção de Pagamento move-se para **Concluído**
5. Um registro de **Transação de Pagamento** é criado com os detalhes finais da cobrança

A intenção de pagamento vincula a sessão de checkout, a conta do provedor e o pedido — fornecendo-lhe uma visão completa da jornada de checkout do cliente.

### Usando intenções de pagamento para suporte

Se um cliente relatar que pagou, mas seu pedido mostra como não pago:

1. Encontre o pedido do cliente em **Pedidos**
2. Navegue até **Pagamentos > Intenções de Pagamento** e procure por intenções vinculadas a esse pedido
3. Verifique o status da intenção — se for **Concluído**, verifique a transação vinculada
4. Se a intenção for **Requer Ação**, o cliente pode não ter concluído a autenticação 3D Secure
5. Se a intenção for **Falhou**, os detalhes do erro explicam por que o pagamento foi recusado

## Dicas

- Revise transações falhadas diariamente — padrões de falhas (ex.: um método de pagamento ou país específico) podem indicar um problema de configuração ou tentativa de fraude.
- Os logs de webhook são inestimáveis ao investigar discrepâncias de pagamento.

Se um pedido foi pago, mas não confirmado, o log de webhook geralmente lhe dirá o que deu errado.
- Bloqueios de autorização expiram automaticamente — se você usar autorizar e depois capturar, certifique-se de que seu processo de atendimento captura os fundos antes que a janela de expiração feche (geralmente 7 dias para a maioria dos provedores).
- O campo **Resposta do Provedor** nas transações contém os dados brutos do provedor de pagamento.

Compartilhe isso com a equipe de suporte do seu provedor se precisar de ajuda para resolver um problema específico de transação.
- Falhas na verificação da assinatura em webhooks devem ser investigadas imediatamente — elas podem indicar um segredo de webhook mal configurado ou um tentativa de enviar eventos de webhook fraudulentos para sua loja.
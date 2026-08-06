---
title: Gerenciando assinaturas de clientes
---

A seção de assinaturas de clientes fornece uma visão completa de todas as assinaturas recorrentes ativas, pausadas e canceladas na sua loja. Aqui, você pode monitorar a saúde da cobrança, visualizar os detalhes individuais da assinatura e tomar ações quando surgirem problemas.

## Visualizando assinaturas de clientes

Navegue até **Assinaturas > Assinaturas de Clientes** para ver a lista completa de assinaturas de todos os clientes.

![Lista de assinaturas de clientes](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

A lista mostra o cliente, o nome do plano, o status atual, a data da próxima cobrança e o número de ciclos de cobrança concluídos de cada assinatura.

### Filtros e busca

Use o painel de filtro à direita para reduzir as assinaturas por:

- **Status** — Filtre por Ativo, Trial, Em Dia, Pausado, Cancelado ou Expirado
- **Plano** — Visualize as assinaturas para um plano específico
- **Modo do Provedor** — Nativo (Stripe/PayPal) ou Falta (cobrança interna)

Use a barra de pesquisa para encontrar assinaturas pelo endereço de e-mail do cliente.

## Status das assinaturas

Entender cada status ajuda você a identificar assinaturas que precisam de atenção:

| Status | O que significa |
|--------|----------------|
| **Trial** | O cliente está em período de teste gratuito ou com preço reduzido |
| **Ativo** | A assinatura está saudável — a cobrança está em dia e o acesso está ativo |
| **Em Dia** | Uma tentativa de pagamento falhou — o sistema está tentando novamente. O cliente mantém o acesso durante o período de graça |
| **Pausado** | A assinatura está temporariamente suspensa — nenhuma cobrança, nenhum acesso |
| **Cancelado** | A cancelamento foi solicitado. O cliente pode ainda ter acesso até a data de término do período |
| **Expirado** | A assinatura terminou completamente — o teste expirou, o número máximo de ciclos de cobrança foi atingido ou o período de cancelamento expirou |

Assinaturas que estão **Em Dia** exigem mais atenção — se o pagamento continuar a falhar e o período de graça se esgotar, a assinatura será suspensa.

## Visualizando os detalhes de uma assinatura

Clique em qualquer assinatura para abrir a visualização de detalhes. Isso mostra:

### Período de cobrança atual

- **Início / Fim do Período Atual** — As datas da janela de cobrança ativa
- **Próxima Data de Cobrança** — Quando a próxima cobrança será tentada
- **Última Data de Cobrança** e **Último Status de Cobrança** — O resultado da tentativa de cobrança mais recente
- **Contagem de Ciclos de Cobrança** — Quantos ciclos de cobrança bem-sucedidos foram concluídos

### Informações da assinatura

- **Plano** e **Nível de Preço** — Qual plano e frequência de cobrança o cliente está usando
- **Produto / Variação** — O produto do catálogo vinculado a essa assinatura (se aplicável)
- **Quantidade** — Número de assentos ou unidades (para planos baseados em quantidade)
- **Token de Pagamento** — O método de pagamento armazenado sendo usado para cobrança recorrente

### Detalhes de teste

Se a assinatura estiver em teste, o **Data de Término do Teste** mostrará quando o teste do cliente expirar e a cobrança total começará.

### Detalhes de cancelamento

Para assinaturas canceladas, você pode ver:

- **Tipo de Cancelamento** — Se o cancelamento foi imediato, no final do período ou agendado
- **Cancelado Em** — Quando o cancelamento foi solicitado
- **Motivo do Cancelamento** — Observações sobre por que o cliente cancelou (se registrado)
- **Data Limite para Reativação** — A última data em que o cliente pode reativar sem se inscrever do zero

### Período de graça e compromissos

- **Data Final do Período de Graça** — Se uma cobrança falhou, isso mostra o prazo antes do acesso ser suspenso
- **Data Final do Compromisso Mínimo** — Para planos com compromissos mínimos, a data mais cedo para cancelamento

## Pausando uma assinatura

Uma assinatura pausada interrompe temporariamente a cobrança, bem como a suspensão do acesso. Isso é útil para clientes que desejam fazer uma pausa sem cancelar totalmente.

Para visualizar assinaturas pausadas, filtre por **Status: Pausado**. A visualização de detalhes mostra:

- **Pausado Em** — Quando a pausa começou
- **Motivo da Pausa** — Observações sobre por que foi pausado
- **Data de Retomada Automática** — Se definido, a data em que a assinatura retomará automaticamente a cobrança e o acesso

Assinaturas retomam na data de retomada automática ou quando o cliente reativa manualmente.

## Registros de ciclo de cobrança

Cada tentativa de cobrança — bem-sucedida ou falha — é registrada no histórico do ciclo de cobrança. Navegue até **Assinaturas > Registros de ciclo de cobrança** para ver esse histórico.

![Lista de registros de ciclo de cobrança](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lendo um registro do histórico de ciclo de cobrança

Cada registro registra:

- **Assinatura** — Qual assinatura do cliente essa tentativa de cobrança pertence
- **Número do ciclo** — Ciclo de cobrança sequencial (Ciclo 1 = primeiro pagamento após o teste)
- **Data da cobrança** — Quando a cobrança foi tentada
- **Status** — Pendente, Processando, Bem-sucedido, Falha, ou Tentando novamente
- **Quebra de valor**:
  - **Valor base** — O preço do plano antes de quaisquer ajustes
  - **Valor da quantidade** — Cobrança adicional pela quantidade de assentos/unidades
  - **Valor de complementos** — Custo total dos complementos ativos
  - **Valor de descontos** — Descontos aplicados totalmente
  - **Valor total** — O valor final cobrado (ou tentativa)
- **Forma de pagamento** — O cartão ou método de pagamento usado
- **ID da transação do provedor** — O número de referência do provedor de pagamento (útil para pesquisas de reembolso)
- **Motivo da falha** — Se a cobrança falhou, por que ela falhou (ex: cartão recusado, fundos insuficientes)

### Diagnosticando falhas de pagamento

Se um cliente entrar em contato com você sobre um problema de cobrança, encontre sua assinatura e verifique os registros de ciclo de cobrança. O campo **Motivo da falha** explica o que deu errado. Motivos comuns de falha incluem:

- **Cartão recusado** — O cartão do cliente foi recusado pelo banco do cliente
- **Fundo insuficiente** — O saldo da conta estava muito baixo no momento da cobrança
- **Cartão expirado** — O método de pagamento salvo expirou
- **Erro de rede** — Um problema temporário de conexão com o provedor de pagamento — geralmente resolve-se na tentativa seguinte

Para falhas persistentes, direcione o cliente a atualizar seu método de pagamento em suas configurações de conta.

## Como as renovações são atendidas

Todo pagamento bem-sucedido de renovação cria um novo pedido pago para esse ciclo de cobrança — não é apenas um registro de pagamento. Esse pedido passa pelo processo normal de atendimento exatamente como um pedido feito na checkout:

- **Produtos físicos** — O pedido de renovação entra na fila normal de atendimento para coleta, embalagem e envio. Ele não é automaticamente alocado em estoque no momento em que o cartão é cobrado, então uma falta temporária de estoque nunca bloqueará uma cobrança que já teve sucesso — você ainda verá o pedido e poderá atendê-lo conforme o estoque permitir.
- **Produtos digitais** — O acesso (links de download, chaves de licença) é reatribuído automaticamente no momento em que o pedido de renovação é criado, da mesma forma que seria para uma compra pela primeira vez.

Os pedidos de renovação copiam os detalhes de envio e cobrança do pedido que iniciou a assinatura, então você não precisa reentrar nada. Eles não carregam um selo especial em sua lista de **Pedidos**, mas você sempre pode rastrear um ciclo específico de volta ao seu pedido: abra **Assinaturas > Registros de ciclo de cobrança**, clique no registro do ciclo e o campo **Pedido** leva diretamente a ele.

## E-mails de assinatura automáticos

Spwig envia e-mails de ciclo de vida de assinatura automaticamente — você não precisa dispará-los manualmente. Os que os comerciantes perguntam com mais frequência:

| E-mail | Quando ele é enviado |
|-------|------------------|
| **Lembrete de renovação** | Antes de uma renovação de cobrança em andamento |
| **Fim do teste** | Antes de um teste gratuito ou com desconto se converter em cobrança completa |
| **Falha na cobrança** | Imediatamente após uma renovação falhar, e novamente como um aviso final se o período de graça estiver prestes a expirar (dunning) |
| **Confirmação de cancelamento** | Quando uma assinatura é cancelada |

Spwig também envia e-mails de boas-vindas, confirmação de pagamento, pausa/recuperação, expiração, reativação, mudança de plano e expiração de método de pagamento nos pontos relevantes no ciclo de vida de uma assinatura.


Todos esses são modelos de e-mail comuns — veja [Modelos de E-mail](/ajuda/modelos-de-e-mail) para revisar ou personalizar seu conteúdo e confirmar que estão ativos.

## Autosserviço do cliente

Os clientes não precisam entrar em contato com você para alterações de assinatura rotineiras — eles podem gerenciar suas próprias assinaturas a partir de sua conta: visualizando detalhes e histórico de cobrança, pausando, retomando, cancelando e atualizando o método de pagamento em arquivo. Isso abrange a maioria das coisas que, de outra forma, chegariam à sua fila de suporte, então, quando um cliente procurar sobre sua assinatura, vale a pena verificar primeiro se ele já tentou a página da conta antes de fazer a alteração para ele no admin.

## Dicas

- Verifique o filtro **Vencido** semanalmente para capturar assinaturas em risco de cancelamento. Um e-mail rápido ao cliente geralmente resolve problemas de pagamento antes que o período de carência expire.
- Os registros de ciclo de cobrança são somente leitura — são criados automaticamente e não podem ser modificados. Isso garante uma trilha de auditoria confiável.
- Se a assinatura de um cliente estiver **Vencida** mas ele já tiver atualizado seu método de pagamento, o próximo retry automático pegará o cartão novo. Os retries seguem o cronograma do período de carência configurado no plano.
- Assinaturas **Expiradas** não são excluídas — elas permanecem visíveis para fins de relatório. Use os filtros de data para se concentrar nas assinaturas atualmente ativas.
- Para assinaturas em **Período de Teste**, verifique a **Data de Término do Período de Teste** para antecipar cobranças futuras e resolver proativamente quaisquer problemas com o método de pagamento.
- Se um cliente disser que uma renovação física "não foi enviada", verifique sua fila regular de atendimento em vez da assinatura — os pedidos de renovação são atendidos da mesma forma que quaisquer outros pedidos e não pulam a fila.
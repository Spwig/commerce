---
title: Gerenciando Assinaturas de Clientes
---

A seção de assinaturas de clientes fornece uma visão completa de todas as assinaturas recorrentes ativas, pausadas e canceladas em sua loja. Aqui você pode monitorar a saúde das cobranças, visualizar detalhes de assinaturas individuais e tomar ações quando surgirem problemas.

## Visualizando assinaturas de clientes

Navegue até **Assinaturas > Assinaturas de Clientes** para ver a lista completa de assinaturas de todos os clientes.

![Lista de assinaturas de clientes](/static/core/admin/img/help/managing-subscriptions/subscription-list.webp)

A lista mostra o cliente de cada assinatura, o nome do plano, o status atual, a data da próxima cobrança e o número de ciclos de cobrança concluídos.

### Filtro e busca

Use o painel de filtro à direita para filtrar assinaturas por:

- **Status** — Filtrar por Ativo, Teste, Atrasado, Pausado, Cancelado ou Expirado
- **Plano** — Ver assinaturas para um plano específico
- **Modo do Provedor** — Nativo (gestão Stripe/PayPal) ou Fallback (cobrança interna)

Use a barra de pesquisa para encontrar assinaturas por endereço de e-mail do cliente.

## Status das assinaturas

Entender cada status ajuda a identificar assinaturas que precisam de atenção:

| Status | O que significa |
|--------|---------------|
| **Teste** | O cliente está no período de teste gratuito ou com preço reduzido |
| **Ativo** | A assinatura está saudável — cobranças estão em dia e o acesso está ativo |
| **Atrasado** | Uma tentativa de pagamento falhou — o sistema está tentando novamente. O cliente mantém o acesso durante o período de graça |
| **Pausado** | A assinatura está temporariamente suspensa — nenhuma cobrança, nenhum acesso |
| **Cancelado** | O cancelamento foi solicitado. O cliente pode ainda ter acesso até a data de término do período |
| **Expirado** | A assinatura terminou completamente — o teste expirou, o número máximo de ciclos de cobrança foi atingido ou o período de cancelamento terminou |

As assinaturas que estão **Atrasadas** exigem mais atenção — se os pagamentos continuarem a falhar e o período de graça se esgotar, a assinatura será suspensa.

## Visualizando detalhes de uma assinatura

Clique em qualquer assinatura para abrir a visualização de detalhes. Isso mostra:

### Período de cobrança atual

- **Início / Fim do Período Atual** — As datas do período de cobrança ativo
- **Próxima Data de Cobrança** — Quando a próxima cobrança será tentada
- **Última Data de Cobrança** e **Status da Última Cobrança** — Resultado da tentativa de cobrança mais recente
- **Contagem de Ciclos de Cobrança** — Quantos ciclos de cobrança bem-sucedidos foram concluídos

### Informações da assinatura

- **Plano** e **Nível de Preço** — Qual plano e frequência de cobrança o cliente está usando
- **Produto / Variante** — O produto do catálogo vinculado a esta assinatura (se aplicável)
- **Quantidade** — Número de assentos ou unidades (para planos baseados em quantidade)
- **Token de Pagamento** — O método de pagamento armazenado usado para cobranças recorrentes

### Detalhes do teste

Se a assinatura estiver em teste, a **Data de Fim do Teste** mostra quando o teste do cliente expira e a cobrança completa começa.

### Detalhes do cancelamento

Para assinaturas canceladas, você pode ver:

- **Tipo de Cancelamento** — Se o cancelamento foi imediato, no final do período ou agendado
- **Cancelado em** — Quando o cancelamento foi solicitado
- **Motivo do Cancelamento** — Notas sobre o motivo pelo qual o cliente cancelou (se registrado)
- **Data Limite para Reativação** — A última data em que o cliente pode reativar sem se inscrever novamente do zero

### Período de graça e compromissos

- **Data de Fim do Período de Graça** — Se uma cobrança falhou, isso mostra a data limite antes que o acesso seja suspenso
- **Data de Fim do Compromisso Mínimo** — Para planos com compromissos mínimos, a data mais cedo para cancelamento

## Pausar uma assinatura

Uma assinatura pausada para de cobrar temporariamente, enquanto também suspende o acesso. Isso é útil para clientes que desejam fazer uma pausa sem cancelar totalmente.

Para visualizar assinaturas pausadas, filtre por **Status: Pausado**. A visualização de detalhes mostra:

- **Pausado em** — Quando a pausa começou
- **Motivo da Pausa** — Notas sobre o motivo da pausa
- **Data de Retomada Automática** — Se definida, a data em que a assinatura será retomada automaticamente com cobrança e acesso

As assinaturas retomam either na data de retomada automática ou quando o cliente reativar manualmente.

## Registros do ciclo de cobrança

Toda tentativa de cobrança — bem-sucedida ou falha — é registrada no log do ciclo de cobrança. Navegue até **Subscriptions > Billing Cycle Logs** para visualizar esse histórico.

![Lista de registros do ciclo de cobrança](/static/core/admin/img/help/managing-subscriptions/billing-cycle-log.webp)

### Lendo uma entrada do log do ciclo de cobrança

Cada entrada do log registra:

- **Subscription** — Qual assinatura do cliente esta tentativa de cobrança pertence
- **Cycle Number** — Ciclo de cobrança sequencial (Ciclo 1 = primeira cobrança após o período de teste)
- **Billing Date** — Quando a cobrança foi tentada
- **Status** — Pendente, Processando, Bem-sucedida, Falha ou Tentando novamente
- **Amount breakdown**:
  - **Base Amount** — O preço do plano antes de quaisquer ajustes
  - **Quantity Amount** — Cobrança adicional pela quantidade de assentos/unidades
  - **Add-ons Amount** — Custo total dos add-ons ativos
  - **Discount Amount** — Total de descontos aplicados
  - **Total Amount** — O valor final cobrado (ou tentado)
- **Payment Method** — O cartão ou método de pagamento usado
- **Provider Transaction ID** — O número de referência do provedor de pagamento (útil para consultas de reembolso)
- **Failure Reason** — Se a cobrança falhou, o motivo da falha (ex: cartão recusado, fundos insuficientes)

### Diagnóstico de falhas de pagamento

Se um cliente entrar em contato com você sobre um problema de cobrança, localize sua assinatura e verifique os logs do ciclo de cobrança. O campo **Failure Reason** explica o que deu errado. Motivos comuns de falha incluem:

- **Cartão recusado** — O cartão do cliente foi rejeitado pelo banco
- **Fundos insuficientes** — O saldo da conta era muito baixo no momento da cobrança
- **Cartão expirado** — O método de pagamento salvo expirou
- **Erro de rede** — Um problema temporário de conexão com o provedor de pagamento — geralmente resolvido na tentativa de repetição

Para falhas persistentes, direcione o cliente a atualizar seu método de pagamento nas configurações da conta.

## Dicas

- Verifique o filtro **Past Due** semanalmente para identificar assinaturas em risco de cancelamento. Um e-mail rápido ao cliente muitas vezes resolve problemas de pagamento antes que o período de graça expire.
- Os logs do ciclo de cobrança são somente leitura — eles são criados automaticamente e não podem ser modificados. Isso garante uma pista de auditoria confiável.
- Se uma assinatura do cliente mostrar **Past Due** mas eles já atualizaram seu método de pagamento, a próxima tentativa automática de repetição usará o novo cartão. As tentativas seguem o cronograma de período de graça configurado no plano.
- **Assinaturas expiradas** não são excluídas — elas permanecem visíveis para relatórios. Use os filtros de data para se concentrar nas assinaturas ativas no momento.
- Para assinaturas em **Trial**, verifique a **Data de Fim do Trial** para antecipar as primeiras cobranças e abordar proativamente quaisquer problemas com métodos de pagamento.
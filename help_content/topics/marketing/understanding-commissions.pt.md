---
title: Entendendo Comissões
---

As comissões são registros de ganhos criados quando um afiliado consegue gerar uma venda para sua loja. Cada comissão está vinculada a um pedido específico, afiliado e programa, e passa por um ciclo de vida de pendente para paga. Este guia explica como as comissões funcionam, como são calculadas e como gerenciá-las de forma eficaz.

## O que é uma Comissão?

Uma comissão representa o valor devido a um afiliado por ter referido um cliente que completou uma compra. Quando um cliente clica em um link de referência de um afiliado e faz um pedido dentro do período de validade do cookie, o Spwig cria automaticamente um registro de comissão.

Cada comissão contém:
- **Afiliado** — O parceiro que referiu o cliente
- **Programa** — O programa de afiliados que define as regras da comissão
- **Pedido** — O pedido que gerou a comissão
- **Valor** — O valor calculado da comissão
- **Status** — A etapa atual no ciclo de vida da comissão
- **Datas** — Data de criação, data de aprovação/rejeição e data de pagamento

## Cálculo de Comissões

As comissões são calculadas automaticamente com base no tipo de comissão e na taxa do programa.

| Tipo de Comissão | Cálculo | Exemplo |
|------------------|---------|---------|
| **Percentual** | Total do Pedido × % da Comissão ÷ 100 | Pedido: $200, Taxa: 10% → **Comissão de $20** |
| **Fixo** | Valor fixo por pedido | Taxa: $15 → **Comissão de $15** (independentemente do valor do pedido) |

### Exemplos de Cálculo

**Comissão por Percentual (10%)**:
- Cliente faz um pedido de $50 → $5 de comissão
- Cliente faz um pedido de $150 → $15 de comissão
- Cliente faz um pedido de $300 → $30 de comissão

**Comissão Fixa ($20)**:
- Cliente faz um pedido de $50 → $20 de comissão
- Cliente faz um pedido de $150 → $20 de comissão
- Cliente faz um pedido de $300 → $20 de comissão

A comissão é calculada com base no **subtotal do pedido** (antes do frete e impostos) e é criada imediatamente quando o pedido é feito.

## Ciclo de Vida da Comissão

Toda comissão passa por uma série de status desde a criação até o pagamento:

```
Pending → Approved → Paid
   ↓
Rejected
```

### Definições de Status

| Status | Descrição | O que Acontece |
|--------|-----------|----------------|
| **Pending** | Pedido realizado, comissão aguardando revisão | A comissão é criada, mas ainda não confirmada. O afiliado pode vê-la, mas não pode sacar fundos. |
| **Approved** | Comerciante confirma que a venda é válida | A comissão é verificada e adicionada ao saldo disponível do afiliado. É elegível para pagamento. |
| **Rejected** | Comerciante rejeita a comissão | A comissão é negada (por exemplo, pedido foi reembolsado, fraudulento ou violou termos). Não é elegível para pagamento. |
| **Paid** | Comissão incluída em um pagamento concluído | O afiliado foi pago. A comissão é finalizada e não pode ser modificada. |

![Lista de Comissões](/static/core/admin/img/help/commission-management/commission-list.webp)

## Quando as Comissões são Criadas

As comissões são criadas automaticamente seguindo esta sequência:

1. **Cliente clica no link do afiliado** — O URL de referência contém o código de rastreamento único do afiliado (ex: `?ref=JOHNSMITH`)
2. **Cookie é definido** — Um cookie de rastreamento é armazenado no navegador do cliente com o código do afiliado
3. **Compra dentro do período do cookie** — O cliente completa um pedido antes do cookie expirar (padrão: 30 dias)
4. **Sistema atribui o pedido** — O Spwig verifica um cookie de rastreamento ativo e identifica o afiliado que referiu o cliente
5. **Comissão criada automaticamente** — Um registro de comissão é gerado com o status **Pending**

A comissão é criada **imediatamente** quando o pedido é feito, mesmo antes de confirmar o pagamento. Isso permite que os comerciantes revisem as comissões enquanto os pedidos estão sendo processados.

## Rastreamento e Atribuição

O Spwig usa **atribuição por último clique** para determinar qual afiliado deve receber crédito por uma venda.

### Como a Atribuição Funciona

- **Modelo de último clique** — O link do afiliado mais recente clicado recebe o crédito (mesmo que múltiplos afiliados tenham referido o cliente)
- **Rastreamento com base em cookie** — Um cookie armazena o código do afiliado no navegador do cliente
- **Período de validade do cookie** — Determina a janela durante a qual uma venda pode ser atribuída (configurado por programa, normalmente 30 dias)
- **Rastreamento de IP e sessão** — Dados adicionais ajudam a identificar padrões de fraude

### Exemplo de Atribuição

- Dia 1: Cliente clica no link do Afiliado A → Cookie definido para o Afiliado A
- Dia 5: Cliente clica no link do Afiliado B → Cookie **atualizado** para o Afiliado B (último clique vence)
- Dia 7: Cliente faz um pedido → Comissão vai para **Afiliado B**

Se o cliente retornar no Dia 35 (após o cookie expirar em 30 dias) e fizer um pedido, **não será criada nenhuma comissão**, pois a janela de rastreamento foi fechada.

## Detalhes da Comissão

Navegue até **Marketing > Comissões** para visualizar todos os registros de comissão.

### Campos da Comissão

Cada comissão exibe:

| Campo | Descrição |
|-------|-----------|
| **Afiliado** | O nome e código do afiliado |
| **Programa** | O nome do programa de afiliados |
| **Pedido** | Número do pedido (link clicável para visualizar os detalhes completos do pedido) |
| **Valor** | O valor calculado da comissão |
| **Status** | Etapa atual (Pendente, Aprovada, Rejeitada, Paga) |
| **Criada** | Quando a comissão foi gerada |
| **Data de Aprovação/Rejeição** | Quando o status foi atualizado |
| **Data de Pagamento** | Quando o pagamento foi processado |
| **Notas** | Notas internas sobre a comissão |

### Visualizando Detalhes do Pedido

Clique no **número do pedido** no registro da comissão para visualizar o pedido original. Isso permite que você verifique:
- Total do pedido e itens comprados
- Informações do cliente
- Status do pagamento
- Status do envio
- Quaisquer reembolsos ou devoluções

Esse contexto ajuda você a decidir se aprova ou rejeita a comissão.

## Gerenciamento de Comissões

Embora este guia se concentre em entender comissões, os passos práticos para aprovar, rejeitar e pagar comissões são abordados em detalhes no tópico de ajuda **Gerenciamento de Comissões**.

### Visão Rápida

- **Aprovar** — Verifique se o pedido é legítimo e confirme que a comissão é válida
- **Rejeitar** — Recuse comissões para pedidos fraudulentos, reembolsos ou violações de políticas
- **Adicionar notas** — Documente os motivos para aprovação ou rejeição para referência futura
- **Processar pagamentos** — Agrupe comissões aprovadas em pagamentos em lote

Veja os tópicos relacionados de ajuda para instruções passo a passo sobre cada tarefa de gerenciamento.

## Dicas

- Revise comissões pendentes **diariamente** durante o primeiro mês para estabelecer um ritmo e identificar quaisquer problemas de rastreamento cedo
- Configure **notificações por e-mail** para alertá-lo quando novas comissões forem criadas, para que você possa revisá-las enquanto os detalhes do pedido ainda estão frescos
- Aprova comissões **após a conclusão do pedido** (não imediatamente após o pedido ser feito) para considerar cancelamentos e devoluções
- Use o **campo de notas** para documentar decisões, especialmente para comissões rejeitadas, para que você tenha um registro se os afiliados perguntarem algo
- Procure por **padrões de rejeição** — se um afiliado tiver muitas comissões rejeitadas, pode indicar fraude ou mal-entendido sobre os termos do programa
- Considere criar uma **política de aprovação de comissões** (ex: "aprovada após a janela de devolução de 14 dias") e comunique-a aos afiliados para estabelecer expectativas claras

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.
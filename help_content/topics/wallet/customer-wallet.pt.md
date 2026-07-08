---
title: Carteira do Cliente
---

A carteira do cliente é um sistema de crédito da loja que fornece aos clientes um saldo que podem usar em pedidos futuros. O crédito da loja pode ser adicionado como resultado de reembolsos, recompensas por indicações, campanhas promocionais ou ajustes manuais feitos pela sua equipe. Os clientes podem então aplicar seu saldo da carteira no checkout para reduzir o valor que pagam.

Navegue até **Clientes > Carteiras do Cliente** para visualizar e gerenciar carteiras.

## Entendendo os saldos da carteira

Cada carteira do cliente mostra quatro figuras de saldo:

| Saldo | Descrição |
|---|---|
| **Saldo Disponível** | O valor que o cliente pode gastar agora no checkout |
| **Saldo Pendente** | Créditos que ainda não podem ser gastos — por exemplo, um reembolso que ainda está dentro do período de confirmação |
| **Crédito ao Longo da Vida** | O total de valor já creditado nessa carteira, incluindo todos os créditos anteriores |
| **Usado ao Longo da Vida** | O total de valor que o cliente gastou de sua carteira em todos os pedidos |

O saldo disponível é a única figura que importa no checkout. Os créditos pendentes tornam-se disponíveis uma vez que o período pendente expire.

## Visualizando a carteira de um cliente

1. Navegue até **Clientes > Carteiras do Cliente**
2. Use o campo de pesquisa para encontrar o cliente pelo nome ou e-mail
3. Clique na entrada da carteira para abrir a visualização detalhada

A visualização detalhada mostra os saldos atuais no topo e um histórico completo de transações abaixo. Os carimbos de tempo **Último Crédito em** e **Último Uso em** informam quando a carteira foi ultimamente ativa.

### Filtrando a lista de carteiras

Use o filtro **Ativo** para separar carteiras ativas das congeladas. Uma carteira marcada como inativa não pode ser usada no checkout, mesmo que tenha um saldo positivo.

## Lendo o histórico de transações

Toda alteração no saldo da carteira é registrada como uma transação individual. O histórico de transações é um livro-razão completo e permanente — transações nunca são editadas ou excluídas. Se um erro precisar ser corrigido, uma nova transação compensatória é adicionada em vez disso.

Cada transação mostra:

| Campo | Descrição |
|---|---|
| **Tipo** | Crédito, Débito, Reembolso, Ajuste ou Reversão |
| **Valor** | O valor dessa transação (sempre mostrado como um número positivo) |
| **Saldo Depois** | O saldo da carteira imediatamente após essa transação ser aplicada |
| **Fonte** | Onde o crédito ou débito originou-se |
| **Status** | Concluído, Pendente ou Reverso |
| **Descrição** | Uma explicação curta da transação |
| **ID de Referência** | Um link para o registro original (por exemplo, um número de pedido ou ID de recompensa) |
| **Criado em** | Quando a transação foi registrada |

### Tipos de transação explicados

- **Crédito** — fundos adicionados à carteira (de um reembolso, promoção ou ajuste manual)
- **Débito** — fundos gastos no checkout
- **Reembolso** — crédito adicionado especificamente como resultado de um pedido devolvido ou cancelado
- **Ajuste** — uma correção manual feita pela sua equipe
- **Reversão** — uma transação que anula uma entrada anterior

### Fontes de transação explicadas

- **Reembolso de Pedido** — crédito concedido quando um pedido foi reembolsado para a carteira
- **Recompensa por Indicação** — crédito ganho através do programa de indicação
- **Promoção** — crédito concedido como parte de uma campanha de marketing
- **Ajuste Manual** — crédito adicionado ou removido diretamente por um membro da equipe
- **Pagamento de Pedido** — fundos gastos no checkout para pagar um pedido

## Ajustes manuais de carteira

Você não pode adicionar ou remover fundos diretamente da visualização detalhada da carteira — transações de carteira são criadas através dos processos relevantes (reembolsos, recompensas, promoções). No entanto, membros da equipe com as permissões apropriadas podem criar transações de ajuste manual através da seção **Transações de Carteira**.

Navegue até **Clientes > Transações de Carteira** e use **+ Adicionar Transação de Carteira** se precisar aplicar um crédito que não se encaixa em outra fonte — por exemplo, um crédito de boa vontade após uma reclamação de serviço.

Ao criar um ajuste manual:

1.

Selecione a **Carteira** que está ajustando (pesquise pelo e-mail do cliente)
2.

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

Defina **Tipo de Transação** como `Adjustment`
3.

Defina **Fonte** como `Manual Adjustment`
4.

Insira o **Valor** — sempre um número positivo, independentemente da direção
5.

Defina o **Status** como `Completed` para um crédito imediato
6.

Adicione uma **Descrição** clara explicando o motivo — isso é visível no histórico de transações
7.

Clique em **Salvar**

> **Nota:** Como as transações de carteira são imutáveis, verifique duas vezes o valor e a carteira antes de salvar. Se você cometer um erro, será necessário criar uma transação de reversão para corrigi-lo.

## Congelar uma carteira

Se você precisar impedir que um cliente use seu saldo de carteira — por exemplo, durante uma investigação de fraude — é possível desativá-la sem excluí-la ou remover o saldo.

1. Abra a visualização de detalhes da carteira do cliente
2. Desmarque o botão de alternância **Ativo**
3. Clique em **Salvar**

O saldo é preservado e a carteira pode ser reativada a qualquer momento. Enquanto estiver inativa, o cliente não poderá aplicar o saldo da carteira no checkout.

## Ver todas as transações

Para uma visão geral da atividade da carteira em toda a loja, navegue até **Clientes > Transações de Carteira**. Esta lista mostra todas as transações em todas as carteiras de clientes, com filtros para:

- **Tipo de Transação** — filtre por crédito, débito, ajuste, etc.
- **Fonte** — filtre por onde as transações originaram-se
- **Status** — filtre por concluído, pendente ou revertido
- **Data** — use a hierarquia de data no topo para explorar um dia, mês ou ano específico

A lista de transações é somente leitura — as transações não podem ser editadas ou excluídas nesta visão.

## Dicas

- Verifique **Credito ao Longo da Vida** versus **Usado ao Longo da Vida** para entender quão ativamente um cliente usa seu crédito da loja — um grande saldo não usado pode indicar que o cliente esqueceu que ele existe
- Se um cliente relatar que seu saldo parece estar errado, revise o histórico de transações completo para rastrear exatamente como o saldo mudou ao longo do tempo; a coluna **Saldo Depois** em cada entrada torna isso fácil
- Use créditos de carteira como uma ferramenta de retenção de clientes — um crédito de boa vontade após uma experiência difícil com um pedido pode custar menos do que um reembolso, mantendo o cliente gastando em sua loja
- Carteiras congeladas mantêm seu saldo permanentemente; não há expiração — se você desativar uma carteira temporariamente, lembre-se de reativá-la quando o problema for resolvido
- O **ID de Referência** em cada transação vincula-se ao registro de origem, tornando fácil verificar por que um crédito ou débito foi aplicado, sem precisar procurar em outro lugar
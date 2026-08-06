---
title: Carteira do Cliente
---

A carteira do cliente é um registro de crédito da loja que acompanha o saldo em aberto de cada cliente. O crédito da loja pode ser adicionado como resultado de devoluções, recompensas por indicações, campanhas promocionais ou ajustes manuais feitos pela sua equipe.

> **Os saldos da carteira podem ser usados no checkout.** Um cliente conectado com crédito da loja vê esse valor na etapa de pagamento e pode aplicá-lo com um único clique. O crédito é deduzido do valor final da conta — após impostos e entrega — e qualquer valor restante é cobrado normalmente no cartão dele. Se o crédito cobrir totalmente o pedido, nenhum cartão será necessário. O crédito é reservado quando aplicado e só é realmente deduzido após a confirmação do pagamento, então um checkout abandonado nunca custa nada ao cliente.

Navegue até **Clientes > Carteiras de Clientes** para visualizar e gerenciar carteiras.

## Entendendo os saldos da carteira

Cada carteira do cliente mostra quatro figuras de saldo:

| Saldo | Descrição |
|---|---|
| **Saldo Disponível** | O crédito atual e utilizável do cliente — esse será o valor que poderá ser gasto no checkout quando esse recurso estiver disponível |
| **Saldo Pendente** | Créditos que ainda não estão no saldo disponível — por exemplo, uma devolução que ainda está dentro do período de confirmação |
| **Crédito Total ao Longo do Tempo** | O total de valor já creditado nessa carteira, incluindo todos os créditos anteriores |
| **Uso Total ao Longo do Tempo** | O total de valor já debitado dessa carteira |

O saldo disponível é a figura que importará quando o gasto no checkout estiver ativo. Os créditos pendentes se moverão para ele uma vez que o período pendente expire.

## Visualizando a carteira de um cliente

1. Navegue até **Clientes > Carteiras de Clientes**
2. Use o campo de pesquisa para encontrar o cliente pelo nome ou e-mail
3. Clique na entrada da carteira para abrir a visualização detalhada

A visualização detalhada mostra os saldos atuais no topo e um histórico completo de transações abaixo. Os carimbos de tempo **Último Crédito** e **Último Uso** informam quando a carteira foi ultimamente ativada.

### Filtrando a lista de carteiras

Use o filtro **Ativo** para separar carteiras ativas das congeladas. Uma carteira marcada como inativa está congelada — nenhum crédito ou débito pode ser registrado contra ela, embora ela mantenha seu saldo.

## Lendo o histórico de transações

Toda alteração no saldo da carteira é registrada como uma transação individual. O histórico de transações é um registro completo e permanente — transações nunca são editadas ou excluídas. Se um erro precisar ser corrigido, uma nova transação compensatória é adicionada em vez disso.

Cada transação mostra:

| Campo | Descrição |
|---|---|
| **Tipo** | Crédito, Débito, Devolução, Ajuste ou Reversão |
| **Valor** | O valor dessa transação (sempre mostrado como um número positivo) |
| **Saldo Depois** | O saldo da carteira imediatamente após essa transação ser aplicada |
| **Fonte** | Onde o crédito ou débito originou-se |
| **Status** | Concluído, Pendente ou Reversado |
| **Descrição** | Uma breve explicação da transação |
| **ID de Referência** | Um link para o registro original (por exemplo, um número de pedido ou ID de recompensa) |
| **Criado em** | Quando a transação foi registrada |

### Tipos de transação explicados

- **Crédito** — fundos adicionados à carteira (de uma devolução, promoção ou ajuste manual)
- **Débito** — fundos removidos da carteira. Quando o gasto no checkout estiver ativo, isso significará "gasto em um pedido" — por enquanto, a única forma de ocorrer um débito é por meio de um ajuste manual
- **Devolução** — crédito adicionado especificamente como resultado de um pedido devolvido ou cancelado
- **Ajuste** — uma correção manual feita pela sua equipe
- **Reversão** — uma transação que anula uma entrada anterior

### Fontes de transação explicadas

- **Devolução de Pedido** — crédito concedido quando um pedido foi devolvido para a carteira
- **Recompensa por Indicação** — crédito ganho através do programa de indicação
- **Promoção** — crédito concedido como parte de uma campanha de marketing
- **Ajuste Manual** — crédito adicionado ou removido diretamente por um membro da equipe
- **Pagamento de Pedido** — fundos gastos no checkout para pagar um pedido. Ainda não em uso — reservado para quando o gasto da carteira no checkout estiver ativo

## Ajustes manuais na carteira

Você não pode adicionar ou remover fundos pelo painel de administração — transações de carteira são criadas apenas pelos processos que as possuem: estornos de pedidos, recompensas de fidelidade e recompensas de indicação. Isso é intencional. Cada movimento carrega uma referência de volta ao que o causou, e uma verificação noturna verifica o saldo de cada carteira contra sua própria história; linhas inseridas manualmente são o que quebram essa cadeia.

Para um crédito de boa vontade — uma reclamação de serviço, um gesto após um problema — emita uma **carteira-presente** manualmente em vez disso (veja o tópico de ajuda **Cartões-presente**). Uma carteira-presente foi projetada exatamente para isso: você controla o valor, o cliente recebe um código por e-mail e gasta no checkout da mesma forma que o crédito da loja.

## Bloqueio de carteira

Se você precisar impedir que um cliente use seu saldo de carteira — por exemplo, durante uma investigação de fraude — você pode desativá-la sem excluí-la ou remover o saldo.

1. Abra a visualização de detalhes da carteira do cliente
2. Desmarque o botão de alternância **Ativo**
3. Clique em **Salvar**

O saldo é preservado e a carteira pode ser reativada a qualquer momento. Enquanto inativa, nenhuma nova créditos ou débitos — manuais ou de outra forma — podem ser registrados na carteira.

## Visualizando todas as transações

Para uma visão geral da atividade da carteira, navegue até **Clientes > Transações da Carteira**. Esta lista mostra todas as transações em todas as carteiras dos clientes, com filtros para:

- **Tipo de Transação** — filtre por crédito, débito, ajuste, etc.
- **Fonte** — filtre por onde as transações originaram-se
- **Status** — filtre por concluído, pendente ou revertido
- **Data** — use a hierarquia de data no topo para explorar um dia, mês ou ano específico

A lista de transações é somente leitura — transações não podem ser editadas ou excluídas nesta visão.

## Dicas

- Verifique **Credito ao longo da vida** versus **Usado ao longo da vida** para entender quão ativamente um cliente usa seu crédito da loja — um grande saldo não usado pode indicar que o cliente esqueceu que ele existe
- Se um cliente relatar que seu saldo parece estar errado, revise a história completa das transações para rastrear exatamente como o saldo mudou ao longo do tempo; a coluna **Saldo Depois** em cada entrada torna isso fácil
- Um grande saldo não gasto vale uma dica — os clientes veem seu crédito da loja no painel de controle da conta e na etapa de pagamento no checkout, mas um e-mail curto apontando para ele frequentemente o converte em um pedido
- Carteiras congeladas mantêm seu saldo permanentemente; não há expiração — se você desativar temporariamente uma carteira, lembre-se de reativá-la quando o problema for resolvido
- O **ID de Referência** em cada transação vincula-se ao registro de origem, tornando fácil verificar por que um crédito ou débito foi aplicado sem precisar procurar em outro lugar
---
title: Ações em massa de estoque
---

Além de ajustes pontuais, o Spwig oferece três ações em massa na lista de **Itens de Estoque** para o trabalho de inventário que ocorre em vários produtos de uma vez: mover estoque entre armazéns, dar baixa em unidades danificadas ou perdidas e conciliar o estoque após uma contagem física. Todas as três são executadas a partir do mesmo menu suspenso **Ações**, aplicam a mesma quantidade a cada item de estoque selecionado e são totalmente registradas no rastro de auditoria de movimentações de estoque.

Navegue até **Produtos > Itens de Estoque** para usá-las.

## Executando uma ação em massa de estoque

1. Na lista de **Itens de Estoque**, use os filtros ou a busca para encontrar os itens que deseja atualizar
2. Marque a caixa ao lado de cada item de estoque para incluí-lo (ou use a caixa de seleção no cabeçalho para selecionar todos os itens da página)
3. Escolha uma das três ações no menu suspenso **Ações**:
   - **Transferir estoque para armazém**
   - **Registrar estoque danificado/perdido**
   - **Recontar estoque (contagem física)**
4. Clique em **Ir**
5. Revise a página de confirmação — ela lista cada item de estoque selecionado com suas quantidades atuais de **em mãos**, **alocadas** e **disponíveis**, para que você possa verificar se selecionou os itens corretos
6. Preencha os campos da ação (veja abaixo) e clique no botão de envio para aplicar

![A lista de Itens de Estoque com o menu suspenso de ações em massa aberto, mostrando Transferir estoque para armazém, Registrar estoque danificado/perdido e Recontar estoque (contagem física) junto com as outras ações](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

A mesma quantidade que você insere é aplicada a **todos** os itens selecionados — isso foi projetado para mover, dar baixa ou recontar o mesmo número de unidades em vários SKUs de uma vez (por exemplo, transferindo 10 unidades de vários produtos para uma nova localização de loja). Para um único item com uma quantidade diferente, execute a ação novamente com apenas esse item selecionado, ou use **Ajustar níveis de estoque** em vez disso.

## Transferir estoque para armazém

Use isso para mover o estoque disponível do armazém de cada item selecionado para um armazém diferente — por exemplo, reabastecer uma nova localização de varejo a partir do seu armazém principal ou reequilibrar o inventário entre centros de distribuição regionais.

Na página de confirmação, preencha:

| Campo | Descrição |
|-------|-------------|
| **Armazém de destino** | Para onde o estoque deve ser movido. Apenas armazéns ativos aparecem nesta lista. |
| **Quantidade por item** | Unidades a serem movidas do armazém atual de cada item selecionado. |
| **Motivo** | Nota opcional, por exemplo, "Reabastecimento da nova loja de Auckland". |

Clique em **Transferir Estoque** para aplicar.

![A página de confirmação de Transferir Estoque: um cartão de Itens de Estoque Selecionados listando três itens com suas cifras de em mãos/alocadas/disponíveis, e um formulário de Detalhes da Transferência com armazém de destino, quantidade e motivo preenchidos](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Apenas estoque não reservado pode ser movido.** O Spwig transfere do estoque *disponível* (em mãos menos unidades alocadas para pedidos abertos) — unidades já prometidas para o pedido de um cliente permanecem no armazém de origem para que o pedido ainda possa ser cumprido. Se um item selecionado não tiver estoque disponível suficiente para cobrir a quantidade que você inseriu, esse item será ignorado e um erro explicará o motivo; o restante da seleção ainda será transferido.

Se um item selecionado já estiver estocado no armazém de destino que você escolheu, ele será ignorado automaticamente (não há nada a transferir para si mesmo) e você verá uma mensagem informando quantos itens foram ignorados por esse motivo.

Cada transferência grava um conjunto de movimentações pareadas no rastro de auditoria — uma entrada negativa de **Transferência de Armazém** na origem e uma correspondente positiva no destino — para que o rastro completo mostre exatamente de onde o estoque veio e para onde foi.

## Registrar estoque danificado/perdido

Use isso para dar baixa em unidades que estão quebradas, estragadas ou faltantes — por exemplo, após encontrar mercadorias danificadas em uma entrega ou investigar uma discrepância.

Na página de confirmação, preencha:

| Campo | Descrição |
|-------|-------------|
| **Quantidade a ser escriturada (por item)** | Unidades a serem removidas do estoque disponível para cada item selecionado. |
| **Motivo** | Observação opcional, ex. "Danos por água durante o armazenamento". |

Clique em **Registrar Escrituração** para aplicar.

**Estoque reservado não pode ser escrito off.** O estoque disponível nunca pode cair abaixo da quantidade atualmente alocada para pedidos abertos — o Spwig bloqueia a escrituração para qualquer item em que a quantidade que você digitou possa consumir o estoque alocado, então você não pode acidentalmente deixar um pedido pago sem o estoque para atendê-lo. Se isso acontecer para um item, você verá um erro indicando o item e quantas unidades não reservadas ele realmente tem disponíveis para escrituração.

Cada escrituração é registrada como uma movimentação de **Danificada/Perdida** nesse item de estoque, com uma quantidade negativa.

## Recontagem de estoque (contagem física)

Use isso após uma contagem física de estoque para corrigir as quantidades disponíveis para corresponderem ao que você contou na verdade — o caminho mais rápido para reconciliar muitos itens após uma auditoria do armazém ou contagem cíclica.

Na página de confirmação, preencha:

| Campo | Descrição |
|-------|-------------|
| **Quantidade disponível contada (por item)** | A quantidade que você contou fisicamente. O estoque disponível é definido para esse número exato para cada item selecionado — não adicionado ou subtraído. |
| **Motivo** | Observação opcional, ex. "Contagem de estoque do armazém do Q3". |

Clique em **Aplicar Recontagem** para aplicar.

![A página de confirmação de Recontagem de Estoque: o cartão Itens de Estoque Selecionados e um formulário de Detalhes da Recontagem com a quantidade disponível contada e um motivo preenchidos](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Ao contrário das outras duas ações, a recontagem pode mover o estoque em qualquer direção — para cima se você contou mais do que o sistema esperava, para baixo se você contou menos. Se a contagem que você entrar for menor que a quantidade atualmente alocada para pedidos abertos, o Spwig ainda a aplicará (uma contagem é um fato, não algo para discutir), mas o quadro **Disponível** desse item mostrará como `0` na lista de estoque e seu ícone de status mudará para **Esgotado** — trate disso como um sinal para verificar se os pedidos afetados ainda podem ser atendidos.

Cada recontagem é registrada como uma movimentação de **Recontagem Física**, com a quantidade mostrando a correção (positiva ou negativa) entre as figuras antigas e novas de estoque disponível.

## Revisando o que mudou

Toda transferência, escrituração e recontagem é registrada da mesma forma que qualquer outra alteração de estoque:

- Abra um item de estoque e role para a seção **Movimentações de Estoque** para ver seu histórico completo
- Ou navegue até **Produtos > Movimentações de Estoque** para percorrer as movimentações em todos os itens, filtráveis por tipo

Cada entrada registra o tipo de movimentação, a mudança na quantidade, os valores antigos e novos de estoque disponível, quem fez a alteração e o motivo que você digitou (se houver) — então uma transferência ou escrituração em lote é tão rastreável quanto uma ajuste manual individual.

## Dicas

- Execute **Recontagem de estoque** logo após uma contagem física de estoque enquanto os números contados estiverem frescos — é mais fácil detectar um erro de digitação na página de confirmação do que se esforçar para resolver isso mais tarde a partir do histórico de movimentações.
- Sempre preencha **Motivo** para escrituras e recontagens. Daqui há seis meses, "Danos por água durante o armazenamento" é muito mais útil no histórico de auditoria do que um campo em branco.
- Antes de transferir estoque, verifique a coluna **Disponível** na página de confirmação — ela já leva em conta as unidades alocadas, então você saberá imediatamente se uma quantidade é muito alta para um dos itens que você selecionou.
- Essas ações aplicam a mesma quantidade a todos os itens selecionados. Agrupe sua seleção por itens que realmente precisem da mesma quantidade movida, escriturada ou recontada e trate as exceções um item por vez.
- Se você usar o PON em uma loja de varejo, lembre-se de que o estoque de buffer do armazém não faz parte do "disponível" para pedidos online — mas transferências em lote e escrituras ainda funcionam contra o total real de estoque disponível do armazém.
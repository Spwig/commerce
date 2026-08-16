---
title: AÃ§Ãµes em lote para estoque
---

Além de ajustes individuais, o Spwig oferece trÃªs aÃ§Ãµes em lote na lista de **Itens de Estoque** para o trabalho de estoque que ocorre em muitos produtos de cada vez: transferir estoque entre armazÃ©ns, escrever off unidades danificadas ou perdidas e reconciliar estoque apÃ³s uma contagem fÃ­sica. As trÃªs aÃ§Ãµes sÃ£o executadas a partir do mesmo **Menu de AÃ§Ãµes**, aplicam a mesma quantidade a cada item de estoque que vocÃª selecionar e sÃ£o registradas integralmente no histÃ³rico de movimentaÃ§Ã£o de estoque.

Navegue atÃ© **Produtos > Itens de Estoque** para usÃ¡-los.

## Executando uma aÃ§Ã£o em lote de estoque

1. Na lista de **Itens de Estoque**, use os filtros ou a busca para encontrar os itens que deseja atualizar
2. Marque a caixa ao lado de cada item de estoque para incluÃ­-los (ou use a caixa de seleÃ§Ã£o do cabeÃ§alho para selecionar todos os itens da pÃ¡gina)
3. Escolha uma das trÃªs aÃ§Ãµes no **Menu de AÃ§Ãµes**:
   - **Transferir estoque para o armazÃ©m**
   - **Registrar estoque danificado/perdido**
   - **Recontar estoque (contagem fÃ­sica)**
4. Clique em **Ir**
5. Revise a pÃ¡gina de confirmaÃ§Ã£o — ela lista cada item de estoque selecionado com suas quantidades **em estoque**, **atribuÃ­das** e **disponÃ­veis** para que vocÃª possa verificar se selecionou os itens certos
6. Preencha os campos da aÃ§Ã£o (veja abaixo) e clique no botÃ£o de envio para aplicÃ¡-los

![A lista de Itens de Estoque com o menu de aÃ§Ãµes em lote aberto, mostrando Transferir estoque para o armazÃ©m, Registrar estoque danificado/perdido e Recontar estoque (contagem fÃ­sica) ao lado das outras aÃ§Ãµes](/static/core/admin/img/help/stock-bulk-actions/stock-items-actions-dropdown.webp)

A mesma quantidade que vocÃª digitar serÃ¡ aplicada a **todos** os itens selecionados — isso foi projetado para mover, escrever off ou recalcular o mesmo nÃºmero de unidades em muitos cÃ³digos de produto de cada vez (por exemplo, transferir 10 unidades de vÃ¡rios produtos para uma nova localizaÃ§Ã£o da loja). Para um Ãºnico item com uma quantidade diferente, execute a aÃ§Ã£o novamente com apenas esse item selecionado, ou use **Ajustar os nÃ­veis de estoque** em vez disso.

## Transferir estoque para o armazÃ©m

Use isso para mover estoque disponÃ­vel de cada item selecionado do armazÃ©m para outro armazÃ©m — por exemplo, reabastecer uma nova loja de varejo a partir do seu armazÃ©m principal, ou realocar o estoque entre centros de atendimento regionais.

Na pÃ¡gina de confirmaÃ§Ã£o, preencha:

| Campo | DescriÃ§Ã£o |
|-------|-------------|
| **ArmazÃ©m de destino** | Para onde o estoque deve ser transferido. Apenas armazÃ©ns ativos aparecem nessa lista. |
| **Quantidade por item** | Unidades a serem removidas de cada item selecionado do armazÃ©m atual. |
| **Motivo** | Nota opcional, por exemplo, "Reabastecimento da nova loja de Auckland". |

Clique em **Transferir Estoque** para aplicar.

![A pÃ¡gina de confirmaÃ§Ã£o de TransferÃªncia de Estoque: um cartÃ£o de Itens de Estoque Selecionados listando trÃªs itens com seus valores de estoque/atribuÃ­dos/disponÃ­veis, e um formulÃ¡rio de Detalhes da TransferÃªncia com um armazÃ©m de destino, quantidade e motivo preenchidos](/static/core/admin/img/help/stock-bulk-actions/transfer-stock-confirmation.webp)

**Apenas estoque nÃ£o reservado pode ser transferido.** O Spwig transfere do *estoque disponÃ­vel* (estoque em mÃ£o menos as unidades alocadas para pedidos abertos) — unidades jÃ¡ comprometidas com um pedido de cliente permanecem no armazÃ©m de origem para que esse pedido possa ainda ser atendido. Se um item selecionado nÃ£o tiver estoque disponÃ­vel suficiente para cobrir a quantidade que vocÃª digitou, esse item serÃ¡ pulado e um erro explicarÃ¡ o motivo; o restante da seleÃ§Ã£o ainda serÃ¡ transferido.

Se um item selecionado jÃ¡ estiver estocado no armazÃ©m de destino que vocÃª escolheu, ele serÃ¡ pulado automaticamente (nÃ£o hÃ¡ nada para transferir para si mesmo), e vocÃª verÃ¡ uma mensagem dizendo quantos itens foram pulados por esse motivo.

Cada transferÃªncia escreve um conjunto par de movimentaÃ§Ãµes no histÃ³rico de auditoria — uma entrada negativa de **TransferÃªncia de ArmazÃ©m** na origem e uma positiva correspondente no destino — entÃ£o o rastro completo mostra exatamente de onde o estoque veio e para onde foi.

## Registrar estoque danificado/perdido

Use isso para escrever off unidades que estejam quebradas, estragadas ou faltantes — por exemplo, apÃ³s encontrar mercadorias danificadas em uma entrega ou investigar uma discrepÃ¢ncia.

Na pÃ¡gina de confirmaÃ§Ã£o, preencha:

| Campo | Descrição |
|-------|-------------|
| **Quantidade a ser escriturada (por item)** | Unidades a serem removidas do estoque disponível para cada item selecionado. |
| **Motivo** | Observação opcional, ex. "Danos por água durante o armazenamento". |

Clique em **Registrar Escrituração** para aplicar.

**Estoque reservado não pode ser escrito off.** O estoque disponível nunca pode cair abaixo da quantidade atualmente alocada para pedidos abertos — o Spwig bloqueia a escrita de estoque para qualquer item em que a quantidade que você digitou possa consumir o estoque alocado, então você não pode acidentalmente deixar um pedido pago sem o estoque para atendê-lo. Se isso acontecer para um item, você verá um erro nomeando o item e quantas unidades não reservadas ele realmente tem disponíveis para escrita de estoque.

Cada escrita de estoque é registrada como uma **Movimentação de Danificada/Perdida** nesse item de estoque, com uma quantidade negativa.

## Recontagem de estoque (contagem física)

Use isso após uma contagem física de estoque para corrigir as quantidades disponíveis para corresponderem ao que você contou na verdade — o caminho mais rápido para reconciliar muitos itens após uma auditoria de armazém ou contagem cíclica.

Na página de confirmação, preencha:

| Campo | Descrição |
|-------|-------------|
| **Quantidade disponível contada (por item)** | A quantidade que você contou fisicamente. O estoque disponível é definido para esse número exato para cada item selecionado — não adicionado ou subtraído. |
| **Motivo** | Observação opcional, ex. "Contagem de estoque do armazém do Q3". |

Clique em **Aplicar Recontagem** para aplicar.

![A página de confirmação de Recontagem de Estoque: o cartão de Itens de Estoque Selecionados e um formulário de Detalhes da Recontagem com a quantidade disponível contada e um motivo preenchidos](/static/core/admin/img/help/stock-bulk-actions/recount-stock-confirmation.webp)

Diferente das outras duas ações, a recontagem pode mover o estoque em qualquer direção — para cima se você contou mais do que o sistema esperava, para baixo se você contou menos. Se a contagem que você entrar for menor que a quantidade atualmente alocada para pedidos abertos, o Spwig ainda a aplicará (uma contagem é um fato, não algo para discutir), mas o quadro **Disponível** desse item mostrará como `0` na lista de estoque e seu ícone de status mudará para **Esgotado** — trate disso como um sinal para verificar se os pedidos afetados ainda podem ser atendidos.

Cada recontagem é registrada como uma **Recontagem Física** de movimentação, com a quantidade mostrando a correção (positiva ou negativa) entre as figuras antigas e novas de estoque disponível.

## Revisando o que mudou

Toda transferência, escrita de estoque e recontagem é registrada da mesma forma que qualquer outra alteração de estoque:

- Abra um item de estoque e role para a seção **Movimentações de Estoque** para ver seu histórico completo
- Ou navegue até **Produtos > Movimentações de Estoque** para percorrer as movimentações em todos os itens, filtráveis por tipo

Cada entrada registra o tipo de movimentação, a mudança na quantidade, os valores antigos e novos de estoque disponível, quem fez a alteração e o motivo que você digitou (se houver) — então uma transferência em lote ou escrita de estoque é tão rastreável quanto uma ajuste manual individual.

## Dicas

- Execute **Recontagem de estoque** logo após uma contagem física de estoque enquanto os números contados estão frescos — é mais fácil detectar um erro de digitação na página de confirmação do que desembaraalhar isso mais tarde a partir do histórico de movimentações.
- Sempre preencha **Motivo** para escritas de estoque e recontagens. Daqui há seis meses, "Danos por água durante o armazenamento" é muito mais útil no histórico de auditoria do que um campo em branco.
- Antes de transferir estoque, verifique a coluna **Disponível** na página de confirmação — ela já leva em conta as unidades alocadas, então você saberá imediatamente se uma quantidade é muito alta para um dos itens que você selecionou.
- Essas ações aplicam a mesma quantidade a cada item selecionado. Agrupe sua seleção por itens que realmente precisam da mesma quantidade movida, escrita ou recontada, e trate as exceções um item de cada vez.
- Se você usar o Pdv em uma loja de varejo, lembre-se de que o estoque de buffer do armazém não faz parte do "disponível" para pedidos online — mas transferências em lote e escritas de estoque ainda funcionam contra o total real de estoque disponível do armazém.
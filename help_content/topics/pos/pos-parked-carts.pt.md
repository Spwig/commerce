---
title: Estacionamento e Retomada de Transações POS
---

<!-- screenshots-needed:
- url: /en/admin/pos_app/parkedcart/
  filename: parked-cart-list.webp
  description: Parked cart list view (may be empty on fresh install — capture anyway)
  save-to: core/static/core/admin/img/help/pos/
-->

Carrinhos estacionados permitem que seus caixas pausem uma transação e comecem imediatamente a atender o próximo cliente — sem perder um único item ou desconto. Quando você estiver pronto, o carrinho original é restaurado exatamente como estava e a venda continua a partir do ponto em que parou.

## O que o estacionamento de um carrinho faz

Quando um caixa tocar em **Estacionar** no registrador POS, o Spwig salva um snapshot completo do carrinho atual no servidor. O registrador é limpo para que uma nova transação possa começar imediatamente. O carrinho estacionado é armazenado e vinculado ao terminal em que foi criado.

Nada é perdido no snapshot. O carrinho estacionado preserva:

- Cada item e sua quantidade
- Qualquer cliente que foi vinculado à venda
- Descontos manuais aplicados ao carrinho ou a itens individuais

O carrinho estacionado permanece disponível no mesmo terminal por até **24 horas**. Após esse período, o Spwig o remove automaticamente. Carrinhos que já foram restaurados são removidos imediatamente após a restauração e não contam para a janela de 24 horas.

## Como estacionar uma transação

Você deve ter pelo menos um item no carrinho antes de estacionar. Um carrinho vazio não pode ser estacionado.

1. Enquanto uma venda está em andamento, toque no botão **Estacionar** no registrador POS.
2. O Spwig salva o carrinho e limpa o registrador. Você verá uma confirmação e a contagem de carrinhos estacionados na área de carrinhos estacionados será atualizada.
3. Comece a transação do próximo cliente no registrador agora vazio.

Se o cliente já foi vinculado à venda antes de estacionar, seu nome aparecerá na lista de carrinhos estacionados para identificação fácil.

## Como retomar uma transação estacionada

1. Toque na área ou ícone **Carrinhos Estacionados** no registrador POS. Você verá uma lista de todos os carrinhos atualmente estacionados nesse terminal, mostrando o nome do cliente (se um foi vinculado), a quantidade de itens, o valor total, o caixa que estacionou e o horário em que foi estacionado.
2. Toque no carrinho que deseja retomar.
3. Se o seu registrador atual tiver itens nele, o POS limpará esses itens antes de restaurar o carrinho estacionado. Certifique-se de que você tenha concluído ou estacionado a transação atual antes de retomar outra.
4. Os itens do carrinho estacionado, o vinculo ao cliente e os descontos manuais são todos restaurados. A venda continua normalmente.

## Visibilidade de carrinhos estacionados

Carrinhos estacionados são **vinculados ao terminal** em que foram criados. Qualquer caixa logado no mesmo terminal pode ver e retomar qualquer carrinho estacionado nesse terminal — não há restrição por caixa sobre quem pode pegar um carrinho estacionado.

Carrinhos estacionados em um terminal diferente, mesmo na mesma localização da loja, não são visíveis no seu terminal atual.

## Cancelar um carrinho estacionado do POS

Um caixa pode excluir um carrinho estacionado diretamente da lista de carrinhos estacionados no terminal — toque no carrinho e use a opção de excluir ou descartar. Carrinhos estacionados excluídos são removidos permanentemente e não podem ser recuperados.

## Expiração automática e limpeza

Cada carrinho estacionado expira **24 horas após ter sido estacionado**. O Spwig executa uma tarefa em segundo plano que remove carrinhos expirados que nunca foram retomados. Não há nada que você precise fazer — a limpeza acontece automaticamente.

Se você precisar limpar carrinhos estacionados antes do período de 24 horas, um caixa pode excluí-los um por um da lista de carrinhos estacionados no terminal.

## Turnos e carrinhos estacionados

Não há ligação rígida entre um carrinho estacionado e o turno que estava aberto quando ele foi estacionado. Fechar um turno **não** exclui ou cancela automaticamente quaisquer carrinhos estacionados nesse terminal. Carrinhos estacionados sobrevivem a mudanças de turno e permanecem disponíveis por todo o período de 24 horas.

Isso significa:

- Um carrinho estacionado no final de um turno da manhã pode ser retomado por um caixa em um turno posterior.
- Se você não quiser que carrinhos estacionados sejam transferidos entre turnos, tenha os caixas limparem a lista de carrinhos estacionados antes de fechar seus turnos.

## Dicas

Preserve todos os formatos de markdown, caminhos de imagem, blocos de código e termos técnicos.

- Pouse um carrinho no momento em que um cliente disser "Preciso pegar apenas mais uma coisa" — é mais rápido do que pedir que ele espere na fila novamente ou adicionar os itens manualmente.
- Se a lista de carrinhos pausados estiver ficando longa, verifique se um caixa anterior deixou transações pendentes ao final de seu turno e limpe quaisquer carrinhos antigos.
- Anexe um cliente à venda antes de pausar, quando possível — o nome do cliente aparece na lista, tornando muito mais fácil encontrar o carrinho certo quando ele retornar.
- Os carrinhos pausados expiram após 24 horas, então eles não são adequados para manter transações por toda a noite durante múltiplos dias de negócios.
- Lembre-se de que retomar um carrinho pausado limpará o que estiver atualmente no caixa.

Conclua ou pause a transação ativa antes de pegar um outro carrinho pausado.
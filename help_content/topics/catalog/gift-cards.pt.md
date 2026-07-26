---
title: Cartões-presente
---

Cartões-presente são créditos de loja que os clientes podem comprar para alguém else — ou para si mesmos — entregues por e-mail como um código de resgate único. Você também pode emitir um cartão-presente diretamente do administrador, sem uma compra do cliente.

A venda de cartões-presente está ativa. Quando um cliente compra um, o cartão é criado e enviado por e-mail automaticamente assim que o pagamento for confirmado — nunca antes, para que ninguém receba um código para um pagamento que depois falhar.

Algumas coisas importantes para saber antes de ativar um produto de cartão-presente:

- **Um cartão-presente é dinheiro, não um desconto.** Ele é subtraído do valor final após impostos e frete, e não reduz o imposto que você deve. Isso é o oposto de um cupom, que reduz o preço dos produtos.
- **Os cartões são em uma única moeda.** Um cartão comprado em euros só pode ser gasto em uma encomenda em euros. Se você vender em várias moedas, crie um produto de cartão-presente separado para cada uma. Isso protege você de movimentos cambiais em um saldo que pode não ser gasto por um ano.
- **Cartões-presente não podem ser descontados.** Um cupom não se aplica a uma linha de cartão-presente, porque vender créditos de 100 libras por 80 libras faz você perder 20 libras a cada venda.
- **Um cartão-presente não pode comprar outro cartão-presente.** Isso encerra uma rota que as pessoas usam para lavar detalhes de cartões roubados.
- **Comprar um cartão-presente não gera pontos de fidelidade.** Os pontos são gerados quando o cartão é gasto em produtos, então ninguém ganha pontos duas vezes com o mesmo dinheiro.

![Gerenciamento de cartões-presente](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipos de denominação

Essas configurações controlam como um cliente escolhe o valor ao comprar um cartão-presente:

| Tipo | Descrição |
|------|-------------|
| **Denominações fixas** | Os clientes escolhem entre valores pré-definidos (ex: $25, $50, $100) |
| **Valor personalizado** | Os clientes inserem qualquer valor dentro de um intervalo mínimo/máximo |
| **Ambos** | Ofereça denominações pré-definidas mais uma opção de valor personalizado |

## Criando um Produto de Cartão-presente

Todo cartão-presente — seja ele que eventualmente será vendido ou emitido manualmente hoje — precisa ter um produto do tipo Cartão-presente por trás dele primeiro.

### Etapa 1: Configurar o Produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina **Tipo de Produto** para **Cartão-presente**
3. Preencha o nome e a descrição do produto
4. Configure as configurações de denominação:
   - Escolha um **Tipo de Denominação** (Fixa, Personalizada ou Ambos)
   - Para Fixa: defina os valores de denominação disponíveis
   - Para Personalizada: defina o **Mínimo** e o **Máximo** de valores permitidos
5. Defina **Dias de Validade** (0 = nunca expira) — isso determina por quanto tempo os cartões-presente são válidos após a compra
6. Salve e publique o produto

### Etapa 2: Publicar

Publique o produto quando estiver pronto para vendê-lo. Os clientes podem comprá-lo diretamente no seu site de loja imediatamente, e o cartão é enviado por e-mail automaticamente assim que o pagamento for confirmado.

O produto também é o que você seleciona quando emite um cartão manualmente — então é útil criar um mesmo se você planejar dar cartões-presente apenas de vez em quando.

## Criando um Cartão-presente Manualmente

Essa é a única forma de criar um cartão-presente financiado no momento, e funciona totalmente hoje.

1. Navegue até **Produtos > Cartões-presente** e clique em **+ Adicionar Cartão-presente**
2. Escolha o **Produto** — isso deve ser um produto existente do tipo Cartão-presente (veja acima)
3. Insira o **Valor Inicial** — o saldo inicial, em qualquer valor que você escolher. Diferente de uma compra do cliente, isso não está limitado às configurações de denominação do produto
4. Defina opcionalmente uma data de **Validade** e mantenha **Ativo** marcado para que o cartão possa ser resgatado
5. Preencha a seção **Destinatário**, mais abaixo na mesma página:
   - **E-mail do Destinatário** — obrigatório; onde o e-mail de entrega será enviado
   - **Nome do Destinatário**, **Nome do Remetente** e **Mensagem Pessoal** — todos são opcionais
   - **Data de Envio Agendada** — opcional; deixe em branco e envie quando estiver pronto, ou defina uma data/hora futura (ex: aniversário)
6. Clique em **Salvar**

O código de resgate é gerado automaticamente e o saldo inicial é definido com base no Valor Inicial — você não preenche nenhum desses campos manualmente.

**Salvar o cartão não o envia por e-mail.** Para entregá-lo, volte à lista de cartões-presente, selecione a caixa de seleção do cartão, escolha **Enviar e-mails de cartões-presente** no menu **Ações** e clique em **Ir**.

A mesma ação reenvia o e-mail se você precisar reenviá-lo posteriormente.

## Gerenciamento de Cartões-presente no Admin

Navegue até **Produtos > Cartões-presente** para gerenciar todos os cartões-presente:

### Painel de Estatísticas

No topo da página, quatro cartões mostram métricas principais:

- **Total de Cartões-presente** — Número total de cartões-presente emitidos
- **Ativo** — Cartões ativos com saldo disponível
- **Saldo Total** — Saldo restante combinado de todos os cartões
- **Parcialmente Usado** — Cartões que foram parcialmente resgatados

### Filtros

Filtre cartões-presente por:

- **Pesquisar** — Encontre por código, e-mail ou nome do destinatário
- **Status** — Ativo, Inativo, Expirado, Totalmente Resgatado ou Parcialmente Usado
- **Saldo** — Com Saldo ou Sem Saldo
- **Criado** — Período de tempo (Hoje, Esta Semana, Este Mês, Este Ano)

### Detalhes do Cartão-presente

Cada cartão-presente mostra:

- **Código** — O código único de resgate (ex.: GC-XXXX-XXXX-XXXX)
- **Destinatário** — E-mail e nome
- **Status** — Badges de status com codificação de cor
- **Saldo / Inicial / Resgatado** — Resumo financeiro com porcentagem usada
- **Datas importantes** — Criado, emitido, primeiro uso
- **Remetente** — Quem comprou (ou quem emitiu) o cartão-presente

### Ações

- Clique em um cartão-presente para **editar** seus detalhes e visualizar sua **histórico completo de transações**, exibido inline na mesma página
- Selecione um ou mais cartões e use o menu **Ações** para **Enviar e-mails de cartões-presente** (entrega ou reenvia o e-mail de entrega) ou **Marcar os cartões selecionados como inativos** (desativa — o saldo é preservado, mas o cartão não pode mais ser resgatado)

## Resgate Hoje

**No estabelecimento**, no seu terminal de Ponto de Venda:

1. O caixa recebe o código na etapa de pagamento
2. O código é validado — ativo, não expirado, com saldo e na mesma moeda da venda
3. O saldo é aplicado ao valor total devido, incluindo impostos e entrega
4. Se o saldo não cobrir a venda inteira, o cliente paga o restante de outra forma
5. O saldo é deduzido e a transação é registrada

Observe que o caixa recebe o código na etapa de **pagamento**, e não ao montar o carrinho. Um cartão-presente é dinheiro que o cliente já entregou, então ele liquida a conta em vez de descontar os produtos.

**Online**, o checkout tem um campo de cartão-presente na etapa de pagamento. O cliente insere seu código, o saldo é deduzido do valor devido — após impostos e entrega — e qualquer resto é cobrado de seu cartão como de costume. Se o cartão cobrir a ordem inteira, nenhum outro pagamento é necessário. O saldo só é realmente deduzido uma vez que o pagamento é confirmado, então um checkout abandonado nunca toca no cartão.

Os destinatários também podem verificar seu saldo restante a qualquer momento no link do e-mail de entrega.

## Tratamento de Estornos

Ao estornar pedidos ou vendas que usaram um cartão-presente:

- **Um cartão-presente comprado pelo cliente, ainda não usado** — o cartão é desativado e seu saldo zerado, então o crédito desaparece junto com o estorno.
- **Um cartão-presente comprado pelo cliente e parcialmente gasto** — isso exige sua julgamento. Desativá-lo levaria de volta o crédito que o cliente já usou, então o saldo é deixado inalterado e marcado para você ajustar manualmente.
- **Um cartão-presente usado para pagar o pedido sendo estornado** — o estorno é devolvido ao cartão primeiro, antes de qualquer pagamento de cartão ou banco. Estornar dinheiro para um banco que o vendedor nunca realmente coletou é o pior erro, e devolver o valor onde ele veio também encerra uma rota conhecida de fraude. Se o cartão original já expirou ou foi desativado, um novo cartão é emitido para o mesmo destinatário, sem data de expiração.
- **Estorno total** — Credite o valor de volta ao saldo do cartão-presente por meio de uma transação de estorno

## Dicas

- Use a emissão manual para créditos de cortesia, resoluções de atendimento ao cliente ou qualquer caso em que deseje conceder um crédito de loja ao cliente sem uma compra no site.
- Defina períodos de expiração razoáveis (ex.: 365 dias) para cumprir as regulamentações locais de cartões-presente — algumas jurisdições exigem períodos mínimos de validade.
- Use o tipo de denominação "Both" para oferecer conveniência (quantias pré-definidas) e flexibilidade (uma quantia personalizada).
- Monitore regularmente a métrica Total Balance — ela representa uma obrigação pendente em seus registros contábeis.
- Uma cartão gasta da mesma forma online e presencialmente — no checkout web na etapa de pagamento, ou no caixa.

O e-mail de entrega inclui um link para verificar o saldo, que os destinatários podem usar a qualquer momento.
- Se você vende para clientes em múltiplos países, pode emitir cartões-presente em moedas específicas — veja o tópico de ajuda **Multi-Currency Gift Cards** para detalhes.
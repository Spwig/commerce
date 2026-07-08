---
title: Cartões-presente
---

Cartões-presente permitem que seus clientes comprem créditos para loja que podem ser enviados a alguém como presente ou mantidos para uso pessoal. Os destinatários recebem um código único por e-mail que podem resgatar no checkout.

![Gerenciamento de cartões-presente](/static/core/admin/img/help/gift-cards/gift-card-list.webp)

## Tipos de denominações

Controle como os clientes escolhem o valor do cartão-presente:

| Tipo | Descrição |
|------|-------------|
| **Denominações fixas** | Os clientes escolhem entre valores pré-definidos (ex., $25, $50, $100) |
| **Valor personalizado** | Os clientes inserem qualquer valor dentro de um intervalo mínimo/máximo |
| **Ambos** | Ofereça denominações pré-definidas mais uma opção de valor personalizado |

## Criando um Produto de Cartão-presente

### Etapa 1: Configurar o Produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina **Tipo de Produto** para **Cartão-presente**
3. Preencha o nome e a descrição do produto
4. Configure as configurações de denominação:
   - Escolha um **Tipo de Denominação** (Fixo, Personalizado ou Ambos)
   - Para Fixo: defina os valores de denominação disponíveis
   - Para Personalizado: defina os valores **Mínimo** e **Máximo** permitidos
5. Defina **Dias de Validade** (0 = nunca expira) — isso determina por quanto tempo os cartões-presente são válidos após a compra
6. Salve e publique o produto

### Etapa 2: Publicar e Vender

Após a publicação, o cartão-presente aparece em sua loja virtual como qualquer outro produto. Os clientes podem navegar até ele, selecionar um valor e adicioná-lo ao carrinho.

## Ciclo de Vida do Cartão-presente

Um cartão-presente segue este ciclo de vida:

1. **Compra** — O cliente compra o produto de cartão-presente e fornece os detalhes do destinatário
2. **Entrega** — Um e-mail com o código do cartão-presente é enviado automaticamente ao destinatário
3. **Resgate** — O destinatário insere o código no checkout para aplicar o saldo
4. **Rastreamento do Saldo** — Cada uso deduz do saldo até que ele atinja zero

## Fluxo de Compra do Cliente

Quando um cliente compra um cartão-presente:

1. **Selecionar Valor** — Escolha uma denominação ou insira um valor personalizado
2. **Detalhes do Destinatário** — Insira o endereço de e-mail e o nome do destinatário
3. **Mensagem Pessoal** — Adicione uma mensagem opcional para incluir no e-mail de entrega
4. **Nome do Remetente** — Forneça o nome do remetente para o e-mail
5. **Entrega Agendada** — Opcionalmente, agende o e-mail para uma data futura (ex., aniversário)
6. **Checkout** — Conclua a compra como qualquer outro produto

## Entrega Automática

Após a compra, o cartão-presente é entregue automaticamente:

- Um e-mail estilizado é enviado ao destinatário com:
  - O código único do cartão-presente
  - O valor do cartão-presente
  - A mensagem pessoal do remetente
  - Um link para verificar o saldo restante
- Se a entrega agendada foi definida, o e-mail é enviado na data e hora especificadas
- O remetente recebe uma confirmação de pedido com os detalhes do cartão-presente

## Gerenciamento de Cartões-presente no Admin

Navegue até **Produtos > Cartões-presente** para gerenciar todos os cartões-presente:

### Painel de Estatísticas

No topo da página, quatro cartões mostram métricas-chave:

- **Total de Cartões-presente** — Número total de cartões-presente emitidos
- **Ativos** — Cartões ativos com saldo disponível
- **Saldo Total** — Saldo restante combinado de todos os cartões
- **Parcialmente Usados** — Cartões que foram parcialmente resgatados

### Filtros

Filtre cartões-presente por:

- **Pesquisa** — Encontre por código, e-mail ou nome do destinatário
- **Status** — Ativo, Inativo, Expirado, Totalmente Resgatado ou Parcialmente Usado
- **Saldo** — Tem Saldo ou Saldo Zero
- **Criado** — Período de tempo (Hoje, Esta Semana, Este Mês, Este Ano)

### Detalhes do Cartão-presente

Cada cartão-presente mostra:

- **Código** — O código único de resgate (ex., GC-XXXX-XXXX-XXXX)
- **Destinatário** — E-mail e nome
- **Badges de Status** — Status atual com codificação de cor
- **Saldo / Inicial / Resgatado** — Resumo financeiro com porcentagem usada
- **Datas importantes** — Criado, emitido, primeiro uso
- **Remetente** — Quem comprou o cartão-presente

### Ações

Para cada cartão-presente, você pode:

- **Editar** — Visualizar e modificar os detalhes do cartão-presente
- **Ver Transações** — Ver o histórico completo de transações
- **Reenviar E-mail** — Reenviar o e-mail de entrega ao destinatário
- **Desativar** — Desative o cartão (o saldo é preservado, mas não pode ser usado)

## Resgate no Checkout

Quando um cliente insere um código de cartão-presente no checkout:

1. O código é validado (ativo, não expirado, tem saldo)
2. O saldo disponível é exibido
3. O saldo é aplicado ao total do pedido
4. Se o saldo cobrir o pedido completo, nenhum pagamento adicional é necessário
5. Se o saldo for menor que o total do pedido, o cliente paga o restante
6. A transação é registrada e o saldo é atualizado

## Tratamento de Estornos

Ao estornar pedidos que usaram um cartão-presente:

- **Cartões-presente não usados** — Desative o cartão-presente totalmente
- **Cartões parcialmente usados** — O saldo deve ser ajustado manualmente por meio de uma transação
- **Estorno total** — Credite o valor de volta ao saldo do cartão-presente por meio de uma transação de estorno

## Dicas

- Defina períodos de validade razoáveis (ex., 365 dias) para cumprir as regulamentações locais de cartões-presente — algumas jurisdições exigem períodos mínimos de validade.
- Use o tipo de denominação **Ambos** para oferecer conveniência (valores pré-definidos) e flexibilidade (valores personalizados).
- Monitore regularmente a métrica de Saldo Total — ela representa uma obrigação pendente em seus livros contábeis.
- Use a entrega agendada para promoções sazonais — os clientes podem comprar cartões-presente com antecedência e tê-los entregues na data exata.
- Teste o fluxo completo (compra, entrega por e-mail, resgate) com um pedido de teste antes de lançar.
- Se você vender para clientes em múltiplos países, pode emitir cartões-presente em moedas específicas — veja o tópico de ajuda **Cartões-presente Multimonedas** para detalhes.
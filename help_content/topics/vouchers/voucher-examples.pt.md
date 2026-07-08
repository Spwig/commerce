---
title: Exemplos de Cupons
---

Este guia fornece exemplos concretos, campo por campo, para os tipos de cupons mais comuns. Cada exemplo mostra exatamente o que inserir ao criar um cupom em **Marketing > Cupons** → **+ Adicionar Cupom**.

![Cartão de Cupom](/static/core/admin/img/help/voucher-examples/voucher-card.webp)

## Exemplo 1: Desconto em Percentual com Limite Mínimo

**Cenário:** Ofereça 20% de desconto no carrinho inteiro, mas limite o desconto a $50 para manter pedidos de alto valor lucrativos. Nenhuma data de expiração.

| Campo | Valor |
|-------|-------|
| Código | `SAVE20` |
| Nome | 20% de Desconto — Máximo $50 |
| Tipo de Desconto | Percentual |
| Valor do Desconto | 20 |
| Valor Máximo do Desconto | 50 |
| Escopo de Aplicação | Carrinho Inteiro |
| Usos Máximos Totais | *(vazio — ilimitado)* |
| Usos Máximos por Cliente | 1 |
| Valor Mínimo do Pedido | *(vazio — sem mínimo)* |

**Como o limite funciona:** Em um pedido de $200, o desconto é de $40. Em um pedido de $300, seria $60, mas o limite o reduz a $50. Em um pedido de $500, o desconto ainda é de $50. Isso permite que você execute uma promoção que soa generosa, mantendo o desconto real previsível.

## Exemplo 2: Desconto Fixo com Mínimo

**Cenário:** Dê $10 de desconto em qualquer pedido acima de $75 para incentivar pedidos maiores.

| Campo | Valor |
|-------|-------|
| Código | `TAKE10` |
| Nome | $10 de Desconto em Pedidos Acima de $75 |
| Tipo de Desconto | Valor Fixo |
| Valor do Desconto | 10 |
| Escopo de Aplicação | Carrinho Inteiro |
| Valor Mínimo do Pedido | 75 |
| Usos Máximos por Cliente | 0 *(ilimitado)* |
| Data de Término | *(vazio — sem expiração)* |

> **Nota:** Definir um valor mínimo do pedido protege seus margens. Sem isso, um cliente poderia usar esse código em um pedido de $12 e anular seu lucro. Sempre combine cupons com valor fixo com um mínimo sensato.

## Exemplo 3: Frete Grátis

**Cenário:** Ofereça frete grátis em qualquer pedido, sem valor mínimo.

| Campo | Valor |
|-------|-------|
| Código | `FREESHIP` |
| Nome | Frete Grátis |
| Tipo de Desconto | Frete Grátis |
| Escopo de Aplicação | Carrinho Inteiro |
| Usos Máximos Totais | *(vazio — ilimitado)* |
| Usos Máximos por Cliente | 1 |
| Valor Mínimo do Pedido | *(vazio — sem mínimo)* |

> **Nota:** Selecione o tipo de desconto **Frete Grátis**, que remove automaticamente as taxas de frete do pedido. Este é o método mais limpo e funciona independentemente de qual método de frete o cliente selecionar.

## Exemplo 4: Código de Bem-vindo para Primeiro Cliente

**Cenário:** Dê 15% de desconto no primeiro pedido dos novos clientes para incentivar a conversão.

| Campo | Valor |
|-------|-------|
| Código | `WELCOME15` |
| Nome | Bem-vindo — 15% de Desconto no Primeiro Pedido |
| Tipo de Desconto | Percentual |
| Valor do Desconto | 15 |
| Escopo de Aplicação | Carrinho Inteiro |
| Usos Máximos por Cliente | 1 |
| Apenas Primeiro Cliente | Marcado |

O sistema valida o status de primeiro cliente verificando se o cliente tem algum pedido concluído anteriormente. Se um cliente com histórico de pedidos tentar aplicar esse código, ele verá uma mensagem clara de erro no checkout.

## Exemplo 5: Cupom Específico para Produto

**Cenário:** Ofereça $5 de desconto em produtos selecionados — por exemplo, para acelerar a venda de itens com baixa demanda.

| Campo | Valor |
|-------|-------|
| Código | `PICK5` |
| Nome | $5 de Desconto em Itens Selecionados |
| Tipo de Desconto | Valor Fixo |
| Valor do Desconto | 5 |
| Escopo de Aplicação | Produtos Específicos |
| Produtos Eligeíveis | *(selecione os produtos-alvo)* |
| Usos Máximos por Cliente | 1 |

> **Nota:** Use o escopo de produto quando quiser descontar SKUs individuais. Use o escopo de categoria (próximo exemplo) quando quiser descontar tudo em um departamento. O escopo de produto lhe dá controle preciso; o escopo de categoria é mais fácil de manter quando seu catálogo muda com frequência.

## Exemplo 6: Cupom de Categoria

**Cenário:** Execute uma promoção de 25% de desconto em todos os itens da categoria Eletrônicos.

| Campo | Valor |
|-------|-------|
| Código | `ELEC25` |
| Nome | 25% de Desconto em Eletrônicos |
| Tipo de Desconto | Percentual |
| Valor do Desconto | 25 |
| Escopo de Aplicação | Categorias Específicas |
| Categorias Eligeíveis | Eletrônicos |
| Usos Máximos Totais | *(vazio — ilimitado)* |
| Usos Máximos por Cliente | 1 |


Quando aplicado a uma categoria, o desconto se aplica apenas a itens elegíveis no carrinho.

Itens não eletrônicos são cobrados no preço integral.

## Comparação de Tipos de Desconto

| Tipo | Como Funciona | Melhor Para | Exemplo |
|------|-------------|----------|---------|
| **Percentual** | Deduz uma porcentagem do total elegível | Descontos que crescem com o tamanho do pedido | 20% de desconto no carrinho inteiro |
| **Valor Fixo** | Deduz um valor fixo em dólares | Promoções simples e previsíveis | $10 de desconto em pedidos acima de $75 |
| **Frete Grátis** | Remove as taxas de envio do pedido | Reduzir o abandono de carrinho no checkout | Frete grátis, sem mínimo |

## Comparação de Escopo

| Escopo | Como Funciona | Melhor Para |
|-------|-------------|----------|
| **Carrinho Inteiro** | O desconto se aplica ao total completo do pedido | Promoções em toda a loja e códigos de boas-vindas |
| **Produtos Específicos** | O desconto se aplica apenas aos produtos selecionados no carrinho | Limpar estoque específico ou destaque em ofertas |
| **Categorias Específicas** | O desconto se aplica apenas aos itens nas categorias selecionadas | Vendas por departamento e promoções sazonais |

## Dicas

- **Use códigos memoráveis** — `SUMMER20` é melhor do que `COUPONX1600406498`. Reserve códigos gerados automaticamente para campanhas em massa.
- **Teste antes de distribuir** — Faça um pedido de teste com o código do voucher para verificar se ele é aplicado corretamente e respeita todos os limites.
- **Monitore o uso** — Verifique a contagem de redemptions em cada cartão de voucher para acompanhar o desempenho da campanha em tempo real.
- **Combine com a barra de anúncio** — Promova seu código de voucher em uma mensagem de anúncio em toda a loja para que os clientes o vejam antes de começarem a comprar.
---
title: Códigos de Voucher
---

Códigos de voucher permitem que você crie códigos de desconto, cupons e cartões-presente que os clientes inserem no checkout para receber um desconto. Navegue até **Marketing > Vouchers** no menu lateral do administrador.

![Lista de vouchers](/static/core/admin/img/help/voucher-codes/voucher-list.webp)

## Dashboard de Voucher

A página de voucher mostra uma visão geral com:

- **Cartões de Estatísticas** — Contagens de vouchers ativos, inativos, redemptions e totais
- **Filtros** — Pesquisar por código ou nome, filtrar por Tipo, Status e Escopo
- **Cartões de Voucher** — Cada voucher exibido com detalhes de uso e status

## Criando um Voucher

1. Clique em **+ Adicionar Voucher** no canto superior direito
2. Preencha os detalhes do voucher:
   - **Código** — O código que os clientes inserem no checkout (ex: "SAVE20", "FREESHIP")
   - **Nome/Descrição** — Descrição interna para sua referência
   - **Tipo de Desconto** — Escolha como o desconto é aplicado
   - **Valor do Desconto** — O valor ou porcentagem de desconto
3. Configure as regras de uso:
   - **Limite de Uso** — Máximo de redemptions totais (0 = ilimitado)
   - **Limite por Cliente** — Máximo de usos por cliente
   - **Valor Mínimo do Pedido** — Valor mínimo do carrinho necessário
4. Defina o **escopo**:
   - **Todo o Carrinho** — O desconto se aplica a toda a ordem
   - **Produtos Específicos** — Apenas se aplica a itens selecionados
   - **Categorias Específicas** — Apenas se aplica a itens em categorias selecionadas
5. Defina opcionalmente a expiração:
   - **Data de Expiração** — Quando o voucher deixa de funcionar
6. Clique em **Salvar**

## Tipos de Voucher

| Tipo | Descrição | Exemplo |
|------|-------------|---------|
| **Valor Fixo** | Deduz um valor fixo em dólares | $20 de desconto no pedido |
| **Porcentagem** | Deduz uma porcentagem do total | 15% de desconto no pedido |
| **Frete Grátis** | Remove as taxas de envio | Frete grátis em qualquer pedido |

## Gerenciando Vouchers

### Cartões de Voucher

Cada cartão de voucher mostra:
- **Código** — O código do voucher em negrito
- **Descrição** — O que o voucher faz
- **Badge de Status** — Ativo ou Inativo
- **Detalhes do Desconto** — Tipo e valor (ex: "$ 20.00" ou "15.00%")
- **Escopo** — Se aplica a todo o carrinho ou a itens específicos
- **Contagem de Uso** — Quantas vezes o voucher foi resgatado
- **Data de Criação** — Quando o voucher foi criado
- **Expiração** — Data de expiração ou "Sem expiração"

### Ações de Voucher

Cada cartão tem botões de ação:
- **Editar** — Modificar as configurações do voucher
- **Ver Histórico** — Ver histórico de resgates
- **Excluir** — Remover o voucher

### Filtros de Voucher

Use a barra de filtro para encontrar vouchers específicos:
- **Pesquisar** — Encontrar por código, nome ou descrição
- **Tipo** — Valor Fixo, Porcentagem ou Frete Grátis
- **Status** — Ativo ou Inativo
- **Escopo** — Todo o Carrinho ou específico para produtos

## Geração em Lote de Vouchers

Para campanhas grandes, você pode gerar vouchers em lote:
1. O sistema gera automaticamente códigos únicos (ex: "COUPONX1600406498")
2. Defina parâmetros comuns para todos os vouchers gerados
3. Distribua os códigos por e-mail, redes sociais ou impressos

## Experiência do Cliente

Quando um cliente tem um código de voucher:
1. Eles prosseguem para **checkout**
2. Inserem o código no campo **código de desconto**
3. O desconto é aplicado imediatamente se o voucher for válido
4. A resumo do pedido é atualizado para mostrar o desconto

Se um voucher for inválido (expirado, limite de uso atingido, valor mínimo não atingido), o cliente verá uma mensagem de erro clara.

## Dicas

- Use códigos memoráveis para campanhas de marketing (ex: "SUMMER20" em vez de strings aleatórios).
- Defina limites por cliente para evitar o abuso de descontos valiosos.
- Use valores mínimos de pedido para manter a rentabilidade (ex: "$10 de desconto em pedidos acima de $50").
- Monitore a contagem de redemptions no dashboard para acompanhar a eficácia da campanha.
- Crie vouchers com prazo limitado para criar urgência (ex: "Válido apenas este fim de semana").
- Use o status Ativo/Inativo para pausar vouchers sem excluí-los.

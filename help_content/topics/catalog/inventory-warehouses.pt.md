---
title: Estoque e Armazéns
---

O sistema de armazéns permite gerenciar o estoque em múltiplas localidades, definir prioridades de atendimento e rastrear níveis de estoque em tempo real. Navegue até **Configurações > Gerenciamento de Licenças** na barra lateral, ou acesse armazéns pela aba de estoque do produto.

![Lista de armazéns](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Armazéns

### Lista de Armazéns

A página de armazéns exibe todas as suas localidades de estoque como cartões com:

- **Nome e código** — Identificador do armazém (ex.: "Armazém Principal", código "MAIN-WH")
- **Região de vendas** — Atribuição de região geográfica
- **Indicadores de status** — Ativo/inativo, localidade de varejo
- **Estatísticas** — Produtos estocados, prioridade de atendimento, percentual de estoque reserva
- **Localização** — Cidade e país
- **Última atualização** — Quando os níveis de estoque foram modificados pela última vez

### Criando um Armazém

1. Clique em **+ Adicionar Armazém**
2. Preencha os detalhes do armazém:
   - **Nome** — Rótulo descritivo (ex.: "Armazém Leste dos EUA")
   - **Código** — Identificador único curto (ex.: "US-EAST")
   - **Região de Vendas** — Atribuir a uma região geográfica para roteamento de atendimento
   - **Endereço** — Endereço completo do armazém para cálculos de frete
3. Configure as definições:
   - **Ativo** — Habilitar para incluir no atendimento
   - **Localidade de Varejo** — Marcar se este armazém também funciona como loja física
   - **Prioridade de Atendimento** — Números maiores = prioridade mais alta para atendimento de pedidos
   - **Estoque Reserva** — Percentual do estoque a ser reservado como margem de segurança
4. Clique em **Salvar**

### Prioridade de Atendimento

Quando um pedido é recebido, o sistema seleciona o melhor armazém com base em:

1. **Valor de prioridade** — Armazéns com maior prioridade são preferidos
2. **Disponibilidade de estoque** — Deve ter estoque suficiente
3. **Correspondência de região** — Armazéns na região do cliente são preferidos

Por exemplo, se você tem um armazém nos EUA (prioridade 100) e um armazém na UE (prioridade 60), pedidos dos EUA serão atendidos pelo armazém dos EUA primeiro.

### Estoque Reserva

O estoque reserva reserva um percentual do inventário que não será vendido online. Isso é útil para:
- Lojas físicas de varejo que precisam de estoque de exposição
- Estoque de segurança para evitar vendas em excesso
- Inventário reservado para pedidos de atacado

Uma reserva de 10% em 100 unidades significa que apenas 90 unidades estão disponíveis para pedidos online.

## Itens de Estoque

Itens de estoque representam o inventário real de um produto específico em um armazém específico.

### Visualizando Níveis de Estoque

1. Clique no **ícone de estoque** em qualquer cartão de armazém para ver seus itens de estoque
2. Ou navegue até a aba **Estoque** de um produto para ver o estoque em todos os armazéns

Cada item de estoque exibe:
- **Nome do produto** e variante (se aplicável)
- **Em mãos** — Inventário físico total
- **Alocado** — Quantidade reservada para pedidos pendentes
- **Disponível** — Em mãos menos alocado (o que pode ser vendido)

### Adicionando Estoque

1. Na visualização de estoque do armazém, clique em **Adicionar Item de Estoque**
2. Selecione o produto e a variante
3. Insira a quantidade **em mãos**
4. Salve

### Movimentações de Estoque

Toda alteração no inventário é rastreada como uma **movimentação de estoque**:

| Tipo de Movimentação | Descrição |
|---------------------|-----------|
| **Recebimento** | Novo estoque recebido do fornecedor |
| **Venda** | Estoque deduzido para um pedido atendido |
| **Devolução** | Estoque devolvido por um cliente |
| **Ajuste** | Correção manual (discrepância na contagem) |
| **Transferência** | Movido entre armazéns |
| **Reserva** | Retido temporariamente para um carrinho ativo |

As movimentações de estoque fornecem um histórico completo de auditoria das alterações no inventário.

## Rastreamento de Estoque em Produtos

### Habilitando o Rastreamento de Estoque

Na aba **Estoque** de um produto:

1. Ative **Rastrear Estoque** para habilitar o gerenciamento de estoque
2. Defina o **Limite de Estoque Baixo** — dispara alertas quando o estoque cai abaixo deste nível
3. Configure **Permitir Pedidos em Espera** se deseja aceitar pedidos quando estiver sem estoque

### Estoque Multi-Armazém

Quando o rastreamento de estoque está habilitado, a aba Estoque mostra os níveis de estoque em todos os armazéns em uma tabela resumida:

- Total em mãos em todas as localidades
- Detalhamento por armazém
- Quantidades disponíveis após reservas e alocações

## Alertas de Estoque Baixo

O sistema monitora automaticamente os níveis de estoque e alerta quando:
- Um produto cai abaixo do seu **limite de estoque baixo**
- Um produto atinge **zero de estoque disponível**

Alertas de estoque baixo aparecem em:
- O **Painel da Loja** na seção Ações Necessárias
- A lista de produtos com um indicador visual

## Dicas

- Comece com um único armazém e adicione mais conforme seu negócio cresce.
- Defina prioridades de atendimento com base na velocidade e custo de envio para cada região.
- Use estoques reserva para localidades de varejo para garantir disponibilidade de estoque de exposição.
- Revise as movimentações de estoque regularmente para identificar perdas ou discrepâncias.
- Defina limites de estoque baixo com base no tempo de reposição — se leva 2 semanas para reabastecer, defina o limite para cobrir 2 semanas de vendas.
- Habilite o rastreamento de estoque antes de entrar em operação para evitar vendas em excesso.

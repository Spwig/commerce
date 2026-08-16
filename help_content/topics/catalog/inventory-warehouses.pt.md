---
title: Estoque & Armazéns
---

O sistema de armazéns permite que você gerencie o estoque em múltiplas localizações, defina prioridades de atendimento e acompanhe os níveis de estoque em tempo real. Navegue até **Produtos > Armazéns** no menu lateral do administrador para gerenciar suas localizações de armazém.

![Lista de armazéns](/static/core/admin/img/help/inventory-warehouses/warehouse-list.webp)

## Armazéns

### Lista de Armazéns

A página de armazéns exibe todas as suas localizações de estoque como cartões com:

- **Nome e código** — Identificador do armazém (ex.: "Armazém Principal", código "MAIN-WH")
- **Região de vendas** — Atribuição da região geográfica
- **Crachás de status** — Ativo/inativo, localização de varejo
- **Estatísticas** — Produtos em estoque, prioridade de atendimento, percentual de buffer de estoque
- **Localização** — Cidade e país
- **Última atualização** — Quando os níveis de estoque foram modificados pela última vez

### Criando um armazém

1. Clique em **+ Adicionar Armazém**
2. Preencha as **Informações Básicas**:
   - **Nome** — Rótulo descritivo (ex.: "Armazém Leste dos EUA")
   - **Código** — Identificador curto e único (ex.: "US-EAST") — deve ser único em todos os armazéns
   - **Região de Vendas** — Atribua a uma região geográfica para roteamento de atendimento
   - **Ativo** — Ative para incluir no atendimento
3. Preencha a seção **Endereço** com o endereço completo do armazém
4. Configure as **Configurações de Atendimento**:
   - **Prioridade de Atendimento** — Números maiores = prioridade mais alta para atendimento de pedidos
   - **Percentual de Buffer de Estoque** — Percentual de estoque a ser reservado como buffer de segurança (0–100)
   - **Local de Envio** — Opcionalmente, vincule a um local de coleta se este armazém oferecer coleta pelos clientes
5. Configure o **Display do Cliente** (opcional):
   - **Nome para Exibição** — Rótulo voltado ao cliente (ex.: "Envia da Austrália"). Deixe em branco para usar o nome do armazém.
   - **Exibir na Página Inicial** — Exiba a origem deste armazém aos clientes nas páginas de produtos
6. Configure o **Ponto de Venda / Loja de Varejo** (opcional):
   - **Local de Varejo** — Marque se este armazém também atua como loja física com terminais de Pdv
   - **Nome para Exibição do Pdv** — Nome curto exibido na interface do Pdv
   - **Grupo de Lojas** — Atribua a um grupo de lojas do Pdv para herança de configurações
7. Adicione informações de **Contato** caso necessário (nome, e-mail, telefone)
8. Clique em **Salvar**

### Prioridade de Atendimento

Quando um pedido chega, o sistema seleciona o melhor armazém com base em:

1. **Valor de prioridade** — Armazéns com maior prioridade são preferidos
2. **Disponibilidade de estoque** — Deve ter estoque suficiente
3. **Correspondência de região** — Armazéns na região do cliente são preferidos

Por exemplo, se você tiver um armazém nos EUA (prioridade 100) e um armazém na Europa (prioridade 60), os pedidos dos EUA serão atendidos pelo armazém dos EUA primeiro.

### Buffer de Estoque

O buffer de estoque reserva uma porcentagem do inventário que não será vendido online. Isso é útil para:

- Lojas de varejo físicas que precisam de estoque no chão
- Estoque de segurança para evitar vendas excessivas
- Estoque reservado para pedidos de atacado

Um buffer de 10% em 100 unidades significa que apenas 90 unidades estão disponíveis para pedidos online.

## Itens de Estoque

Itens de estoque representam o estoque real de um produto específico em um armazém específico.

### Visualizando os Níveis de Estoque

1. Clique no **icone de estoque** em qualquer cartão de armazém para ver seus itens de estoque
2. Ou navegue até a aba **Estoque** de um produto para ver o estoque em todos os armazéns

Cada item de estoque mostra:

- **Nome do produto** e variação (se aplicável)
- **Em estoque** — Estoque físico total
- **Alocado** — Quantidade reservada para pedidos pendentes
- **Disponível** — Em estoque menos alocado (o que pode ser vendido)

### Adicionando estoque

1. Navegue até **Produtos > Itens de Estoque** e clique em **+ Adicionar Item de Estoque**, ou
2. Abra o formulário de edição de um produto e use a seção **Itens de Estoque** no final
3. Selecione o **produto** e o **armazém** (e opcionalmente uma **variação** para produtos variáveis)
4. Insira a quantidade de **estoque em mão**
5. Defina o **limite de estoque baixo** — este limiar por item aciona um alerta de estoque baixo
6. Salve

### Movimentações de Estoque

Toda mudança no estoque é registrada como uma **movimentação de estoque**:

| Tipo de Movimento | Descrição |
|--------------|-------------|
| **Recebimento** | Novo estoque recebido do fornecedor |
| **Venda** | Estoque deduzido para um pedido concluído |
| **Devolução** | Estoque devolvido por um cliente |
| **Ajuste** | Correção manual (discrepância na contagem) |
| **Transferência** | Movido entre armazéns |
| **Reserva** | Mantido temporariamente para um carrinho ativo |
| **Danos** | Cancelado como danificado ou perdido |
| **Recontagem** | Corrigido para corresponder a uma contagem física do estoque |

Os movimentos de estoque fornecem um registro completo das alterações no estoque. Além da ação **Ajustar os níveis de estoque**, o Spwig também oferece ações em lote na lista de Itens de Estoque para transferir, cancelar e recontar estoque em muitos itens de uma vez — veja [Ações em Lote de Estoque](/help/stock-bulk-actions).

## Rastreamento de Estoque nos Produtos

### Ativando o rastreamento de estoque

Na seção **Estoque** de um produto:

1. Ative **Rastrear Estoque** para habilitar a gestão de estoque para este produto
2. Defina o **Limite de Estoque Baixo** — dispara alertas no painel de controle quando o estoque em qualquer armazém cai abaixo desse nível
3. Configure **Permitir Encomendas de Devolução** se quiser aceitar pedidos quando estiver sem estoque
4. Defina opcionalmente uma **Ação de Estoque Esgotado** para substituir o comportamento do site ou categoria para este produto específico

Após ativar o rastreamento, gerencie as quantidades reais de estoque usando a seção **Itens de Estoque** no final do formulário do produto, ou através de **Produtos > Itens de Estoque**.

### Estoque em Múltiplos Armazéns

Quando o rastreamento de estoque estiver ativado, a aba de Estoque mostra os níveis de estoque em todos os armazéns em uma tabela resumo:

- Total em estoque em todos os locais
- Divisão por armazém
- Quantidades disponíveis após reservas e alocações

## Alertas de Estoque Baixo

O sistema monitora automaticamente os níveis de estoque e alerta você quando:
- Um produto fica abaixo de seu **limiar de estoque baixo**
- Um produto atinge **estoque disponível zero**

Os alertas de estoque baixo aparecem em:
- O **Painel de Controle da Loja** na seção Ações Necessárias
- Na lista de produtos com um indicador visual

## Dicas

- Comece com um único armazém e adicione mais à medida que o negócio crescer.
- Defina prioridades de atendimento com base na velocidade e no custo de envio para cada região.
- Use buffers de estoque para lojas físicas para garantir a disponibilidade de estoque no chão.
- Revise os movimentos de estoque regularmente para identificar perdas ou discrepâncias.
- Defina os limiares de estoque baixo com base no tempo de reposição — se levar 2 semanas para reposicionar, defina o limiar para cobrir 2 semanas de vendas.
- Ative o rastreamento de estoque antes de ir ao ar para evitar vendas excessivas.
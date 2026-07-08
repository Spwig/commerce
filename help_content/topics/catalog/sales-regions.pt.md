---
title: Regiões de Vendas
---

As regiões de vendas permitem que você defina mercados geográficos para sua loja e controle quais produtos estão disponíveis em cada região. Isso é útil quando você vende em多个国家 ou territórios e precisa de catálogos de produtos diferentes, moedas regionais ou disponibilidade de estoque por localização.

## O que é uma região de venda?

Uma região de venda é uma área geográfica nomeada composta por um ou mais países. Cada região tem uma moeda padrão, uma prioridade e pode estar vinculada a um ou mais armazéns. Quando um cliente navega em sua loja, o Spwig determina sua região com base em sua localização e aplica as regras apropriadas de moeda e visibilidade de produtos.

Casos de uso comuns:
- Mostrar apenas produtos disponíveis localmente para clientes de cada país
- Atribuir moedas padrão específicas da região (ex.: NZD para clientes da Nova Zelândia)
- Controlar quais armazéns atendem pedidos para cada região
- Ocultar produtos que ainda não estão disponíveis em certos mercados

## Criando uma região de venda

1. Navegue até **Catálogo > Regiões de Venda**
2. Clique em **+ Adicionar Região de Venda**
3. Preencha os detalhes da região:

| Campo | Descrição | Exemplo |
|-------|-------------|---------|
| **Nome da Região** | Nome de exibição para esta região | `Asia-Pacific` |
| **Código da Região** | Identificador único curto | `APAC` |
| **Países** | Códigos de país ISO incluídos nesta região | `['NZ', 'AU', 'SG', 'FJ']` |
| **Moeda Padrão** | Código de moeda ISO para esta região | `NZD` |
| **Prioridade** | Regiões com prioridade mais alta são correspondidas primeiro | `10` |
| **Ativo** | Se esta região está atualmente em uso | Marcado |

4. Clique em **Salvar**

### Códigos de país

Insira países como uma lista JSON de códigos ISO de dois caracteres. Por exemplo:
- Nova Zelândia e Austrália: `['NZ', 'AU']`
- Apenas Singapura: `['SG']`
- Todo a Europa: `['DE', 'FR', 'IT', 'ES', 'NL', 'BE', 'AT', 'CH', 'SE', 'NO', 'DK', 'FI', 'PL']`

### Prioridade

Se o país do cliente corresponder a mais de uma região, a região com o número de prioridade mais alto será usada. Defina uma prioridade mais alta para regiões mais específicas (ex.: dê a `NZ` uma prioridade de 20 e `APAC` uma prioridade de 10 para que os clientes da Nova Zelândia sejam correspondidos à região da Nova Zelândia primeiro).

## Controlando a visibilidade do produto por região

Por padrão, cada produto é visível em todas as regiões. Para restringir um produto a regiões específicas, use registros de **Visibilidade da Região do Produto**.

### Restringindo um produto a regiões específicas

1. Navegue até **Catálogo > Visibilidade da Região do Produto**
2. Clique em **+ Adicionar Visibilidade da Região do Produto**
3. Selecione o **Produto**
4. Selecione a **Região**
5. Defina **Visível** como ativo ou inativo conforme necessário
6. Clique em **Salvar**

Uma vez que exista qualquer registro de visibilidade para um produto, o Spwig aplica as regras. Produtos sem registros de visibilidade permanecem visíveis em todos os lugares.

### Padrões comuns

**Limitar a apenas uma região**

Adicione um registro de visibilidade por região que você deseja suportar, definindo **Visível** como `Sim` para as regiões permitidas. Os clientes de outras regiões não verão o produto.

**Excluir de uma região**

Adicione um único registro de visibilidade para a região que deseja excluir e defina **Visível** como `Não`. O produto permanece visível em todas as outras regiões.

### Editando a visibilidade a partir da página do produto

Você também pode gerenciar a visibilidade por região diretamente do formulário de edição do produto. Na seção **Visibilidade da Região** do produto, você encontrará uma tabela inline mostrando todas as regiões e suas configurações de visibilidade para esse produto.

## Moeda regional

Cada região tem uma moeda padrão. Os clientes navegando dentro dessa região veem os preços exibidos na moeda da região. A moeda usada é determinada no checkout.

Para configurar preços em múltiplas moedas, configure taxas de câmbio em **Configurações > Taxas de Câmbio**. Os preços podem ser convertidos automaticamente ou definidos manualmente por moeda.

## Vinculando armazéns a regiões

Os armazéns são vinculados a regiões quando você cria ou edita um armazém em **Catálogo > Armazéns**. Cada armazém pertence a uma região, que controla qual estoque da região é usado para atender pedidos.

Para mais detalhes sobre armazéns, consulte o tópico de ajuda **Inventory and Warehouses**.

## Dicas

- Mantenha os códigos de região curtos e descritivos (`NZ`, `APAC`, `EU`, `US`) — eles são usados internamente e em logs.
- Use números de prioridade mais altos para regiões menores e mais específicas para que elas tenham precedência sobre regiões mais amplas e genéricas.
- Se você vende apenas para um país, não é necessário configurar regiões — o Spwig funciona bem com um único catálogo global.
- Teste a visibilidade baseada em região pré-visualizando sua loja enquanto filtra por uma região específica no administrador.
- Registros de visibilidade de produtos só precisam ser criados quando quiser restringir produtos. Deixar um produto sem registros de visibilidade torna-o universalmente disponível.
- Revise suas regras de visibilidade sempre que adicionar uma nova região para garantir que as restrições de produtos existentes estejam corretas.
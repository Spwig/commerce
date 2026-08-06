---
title: Regiões de Vendas
---

As regiões de vendas permitem que você defina mercados geográficos para sua loja e controle quais produtos estão disponíveis em cada região. Isso é útil quando você vende em vários países ou territórios e precisa de catálogos de produtos diferentes, moedas regionais ou disponibilidade de estoque por localização.

## O que é uma região de vendas?

Uma região de vendas é uma área geográfica nomeada composta por um ou mais países. Cada região tem uma moeda padrão, uma prioridade e pode estar vinculada a um ou mais armazéns. Quando um cliente navega pela sua loja, o Spwig determina sua região com base na localização dele e aplica a moeda e as regras de visibilidade de produtos apropriadas.

Casos de uso comuns:
- Mostrar apenas os produtos localmente disponíveis para os clientes de cada país
- Atribuir moedas padrão específicas da região (por exemplo, NZD para clientes da Nova Zelândia)
- Controlar quais armazéns atendem os pedidos para cada região
- Ocultar produtos que ainda não estão disponíveis em certos mercados

## Criando uma região de vendas

1. Navegue até **Estoque > Regiões de Vendas**. Se você não encontrar, ative **Habilitar Múltiplos Armazéns** em **Configurações > Configurações da Loja > Comércio Eletrônico** para revelar o item do menu — você não precisa realmente usar múltiplos armazéns para isso, ele apenas desbloqueia o link. Você também pode ir diretamente para `/admin/catalog/salesregion/`.
2. Clique em **+ Adicionar Região de Vendas**
3. Preencha os detalhes da região:

| Campo | Descrição | Exemplo |
|-------|-------------|---------|
| **Nome da Região** | Nome de exibição desta região | `Ásia-Pacífico` |
| **Código da Região** | Identificador curto único | `APAC` |
| **Países** | Códigos de país ISO incluídos nesta região | `["NZ", "AU", "SG", "FJ"]` |
| **Moeda Padrão** | Código de moeda ISO para esta região | `NZD` |
| **Prioridade** | Regiões com maior prioridade são correspondidas primeiro | `10` |
| **Ativo** | Se esta região está atualmente em uso | Marcado |

4. Clique em **Salvar**

### Códigos de país

Insira os países como uma lista JSON de códigos de dois caracteres. Por exemplo:
- Nova Zelândia e Austrália: `["NZ", "AU"]`
- Apenas Singapura: `["SG"]`
- Toda a Europa: `["DE", "FR", "IT", "ES", "NL", "BE", "AT", "CH", "SE", "NO", "DK", "FI", "PL"]`

### Prioridade

Se o país de um cliente corresponder a mais de uma região, a região com o número de prioridade mais alto é usada. Defina uma prioridade mais alta para regiões mais específicas (por exemplo, dê à `NZ` uma prioridade de 20 e à `APAC` uma prioridade de 10 para que os clientes da Nova Zelândia sejam correspondidos à região `NZ` primeiro).

## Controlando a visibilidade dos produtos por região

Por padrão, todo produto é visível em todas as regiões. Para restringir um produto, abra-o em **Produtos > Todos os Produtos** e defina o campo **Disponibilidade por Região** (na seção de Status) para permiti-lo apenas em regiões específicas ou em todas as regiões, exceto específicas, e escolha as regiões na tabela abaixo desse campo.

Isso também determina o que os compradores fora das regiões disponíveis para um produto veem — se o produto é oculto totalmente das listagens, ou mostrado com uma notificação de "Não envia para [região]". Consulte o guia **Disponibilidade por Região** para o percurso completo, incluindo esse recurso de exibição e o seletor de Endereço de Entrega na loja.

## Moeda Regional

Cada região tem uma moeda padrão. Se sua loja suporta explicitamente mais de uma moeda (**Configurações > Múltiplas Moedas**), a moeda exibida pelo cliente muda para a moeda padrão da região sempre que sua região muda — seja isso por meio da pergunta automática de região ou do seletor de Endereço de Entrega. Lojas com apenas uma moeda, ou que não ativaram intencionalmente a múltipla moeda, exibem sempre essa única moeda, independentemente da região.

Para configurar preços em múltiplas moedas, configure as taxas de câmbio em **Configurações > Taxas de Câmbio**. Os preços podem ser convertidos automaticamente ou definidos manualmente por moeda.

Para mais detalhes sobre armazéns, consulte o tópico de ajuda **Estoque e Armazéns**.

## Dicas

- Mantenha os códigos de região curtos e descritivos (NZ, APAC, EU, US) — eles são usados internamente e nos registros.
- Use números de prioridade mais altos para regiões menores e mais específicas, para que elas tenham prioridade sobre regiões mais abrangentes.
- Se você vende apenas para um país, não precisa configurar regiões de jeito nenhum — o Spwig funciona perfeitamente com um catálogo global único.
- Defina apenas a **Disponibilidade por Região** de um produto para fora de **Disponível em todas as regiões** quando você precisar realmente restringi-lo — o padrão mantém os produtos universalmente disponíveis sem necessidade de manutenção.
- Revise as regras de região de cada produto sempre que você adicionar uma nova Região de Vendas, para que as restrições ainda correspondam ao que você deseja.
- Adicione o Seletor de Endereço de Entrega ao seu cabeçalho (consulte o guia **Disponibilidade por Região**) para que você possa alternar regiões e verificar se os produtos restritos se comportam conforme o esperado.
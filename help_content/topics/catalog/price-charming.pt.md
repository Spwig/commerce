---
title: Regras de Preço Atraente
---

Preço atraente (também chamado de precificação psicológica) ajusta automaticamente os preços dos seus produtos para terminarem em dígitos específicos que parecem mais atraentes para os clientes. Por exemplo, em vez de exibir um preço de $20,00, o preço atraente pode mostrar $19,99 — uma técnica amplamente usada que faz com que os preços pareçam menores à primeira vista.

O Spwig aplica as regras de preço atraente automaticamente em toda a sua loja, por moeda, então você só precisa definir cada regra uma vez.

## Como o preço atraente funciona

Quando um preço de produto é calculado (incluindo após promoções ou descontos), o Spwig verifica se existe uma regra de preço atraente ativa para essa moeda. Se houver, o preço é ajustado antes de ser exibido aos clientes. O ajuste se aplica a preços acima do seu limite mínimo escolhido.

Você pode configurar regras separadas para cada moeda aceita pela sua loja. Por exemplo, você pode usar terminações `.99` para USD, mas arredondar para o próximo `¥10` para JPY.

## Criando uma regra de preço atraente

1. Navegue até **Catálogo > Regras de Preço Atraente**
2. Clique em **+ Adicionar Regra de Preço Atraente**
3. Selecione a **Moeda** a qual essa regra se aplica (ex: `USD`, `EUR`, `NZD`)
4. Escolha um **Tipo de Regra** (veja a tabela abaixo)
5. Opcionalmente, defina um **Limite Mínimo de Preço** para excluir preços muito baixos
6. Marque **Aplicar a Preços de Venda** se também quiser que o preço atraente seja aplicado quando os itens estiverem em promoção
7. Certifique-se de que **Ativo** esteja marcado
8. Clique em **Salvar**

Apenas uma regra pode existir por moeda. Se você precisar alterar uma regra, edite a existente.

## Tipos de regras

| Tipo de Regra | Exemplo | Melhor para |
|---------------|---------|-------------|
| **Atraente com terminação .99** | $20,50 → $19,99 | Produtos de varejo — o preço psicológico clássico |
| **Atraente com terminação .95** | $20,50 → $19,95 | Alternativa um pouco mais suave para .99 |
| **Atraente com terminação .90** | $20,50 → $19,90 | Arredondado, mas ainda abaixo do próximo dólar |
| **Arredondar para baixo** | $19,50 → $19,00 | Lojas que preferem números inteiros |
| **Arredondar para cima** | $19,50 → $20,00 | Arredondar um pouco para exibições limpas |
| **Arredondar para o múltiplo de 5 mais próximo** | $23,00 → $25,00 | Varejo de alto tráfego e mercados |
| **Arredondar para o múltiplo de 10 mais próximo** | $23,00 → $20,00 | Itens de preço mais alto, como eletrodomésticos |
| **Arredondar para o múltiplo de 100 mais próximo** | $1.234 → $1.200 | Itens de alto valor, como móveis ou eletrônicos |
| **Terminação personalizada** | Qualquer uma — especifique abaixo | Quando sua marca usa uma terminação específica, como `.88` |

### Terminações personalizadas

Se você escolher **Terminação personalizada**, insira o valor da terminação no campo **Terminação Personalizada**. Por exemplo, insira `0,88` para fazer com que todos os preços terminem em `.88` (comum em alguns mercados asiáticos).

## Limite mínimo de preço

Use o campo **Limite Mínimo de Preço** para pular o preço atraente para itens de preço muito baixo, onde o ajuste pareceria estranho. Por exemplo, definir um limite de `5,00` significa que produtos com preço abaixo de $5 serão exibidos com seu preço calculado real, sem o preço atraente aplicado.

Deixe-o em `0` para aplicar o preço atraente a todos os preços.

## Preços de venda

Por padrão, o preço atraente é aplicado tanto aos preços regulares quanto aos de venda. Se você quiser que os preços de venda exibam seus valores calculados exatos (útil para precificação promocional limitada no tempo, onde os valores exatos importam), desmarque **Aplicar a Preços de Venda**.

## Desativando uma regra

Para parar temporariamente o preço atraente sem excluir a regra, desmarque **Ativo** e salve. A regra é preservada e pode ser reativada a qualquer momento.

## Dicas

Preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos.

- Comece com terminações em .99 se estiver em dúvida — é a técnica de precificação psicológica mais amplamente reconhecida e funciona bem para a maioria dos tipos de produtos.
- Defina um limite mínimo se vender itens de baixo custo (abaixo de $5) para que um item de $3,50 não caia para $2,99.
- Verifique seus preços após habilitar uma nova regra visualizando um produto no site de vendas — os preços encantados são exibidos em tempo real.
- O Yen Japonês e moedas semelhantes com números inteiros funcionam melhor com **Arredondar para o múltiplo de 10** ou **Arredondar para o múltiplo de 100**, pois terminações decimais parecem incomuns.
- A encantação de preços é aplicada após todos os descontos e promoções, portanto, seus preços de venda também aparecerão encantados, a menos que desmarque **Aplicar a Preços de Venda**.
- Você pode ter tipos de regras diferentes para diferentes moedas, o que é útil se vender para múltiplos mercados com convenções de precificação diferentes.
---
title: Atributos de Produto
---

Atributos de produto definem as dimensões segundo as quais um produto pode variar — por exemplo, Tamanho, Cor ou Material. Uma vez que você tenha criado um atributo e seus valores possíveis, você pode atribuí-lo a qualquer produto variável e o Spwig gerará o seletor de variações que os clientes usam no checkout.

Navegue até **Catálogo > Atributos de Produto** para gerenciar atributos e seus valores.

## Como os atributos funcionam

Os atributos são reutilizáveis em todo o seu catálogo. Você os cria uma vez e os atribui a tantos produtos quantos forem necessários. Cada atributo tem:

- Um **nome** que o identifica (ex.: "Tamanho")
- Um **tipo de exibição** que controla como o seletor aparece na página do produto
- Um ou mais **valores** que representam as opções disponíveis (ex.: "Pequeno", "Médio", "Grande")

Quando você atribui um atributo a um produto, você também especifica quais de seus valores estão disponíveis para esse produto específico. Isso significa que um atributo "Tamanho" pode ter valores de S a 3XL, mas uma camisa específica pode oferecer apenas S, M e L.

## Tipos de exibição de atributos

O campo **Tipo** em um atributo controla como o widget de seleção aparece na página do produto do seu site:

| Tipo | Aparência | Melhor para |
|---|---|---|
| **Seletor de Dropdown** | Um menu suspenso que o cliente abre para escolher um valor | Atributos com muitos valores (ex.: uma faixa de tamanho com 10+ tamanhos) |
| **Amostra de Cor** | Círculos ou quadrados coloridos que o cliente clica | Atributos de cor onde a identificação visual ajuda |
| **Grupo de Botões** | Botões em formato de pílula exibidos em linha | Atributos com um pequeno número de valores (ex.: S, M, L, XL) |
| **Botões de Rádio** | Lista tradicional de botões de rádio | Qualquer atributo onde você deseja uma lista clara e acessível |

Escolha o tipo de exibição que corresponda à forma como seus clientes pensam sobre o atributo. Para cores, amostras são quase sempre melhores do que um dropdown. Para tamanhos, grupos de botões funcionam bem quando há menos de 8 opções.

## Criando um atributo

1. Navegue até **Catálogo > Atributos de Produto**
2. Clique em **+ Adicionar Atributo de Produto**
3. Insira o **Nome** (ex.: `Tamanho`, `Cor`, `Material`)
4. O **Slug** é preenchido automaticamente — você pode deixá-lo como está
5. Selecione o **Tipo** (Dropdown, Amostra de Cor, Grupo de Botões ou Botões de Rádio)
6. Marque **Obrigatório** se os clientes precisarem selecionar esse atributo antes de adicionarem o produto ao carrinho — isso é apropriado para a maioria dos atributos de tamanho e cor
7. Defina uma **Ordem de Classificação** — atributos com números mais baixos aparecem primeiro no seletor de variações na página do produto
8. Adicione valores de atributo diretamente na seção **Valores** (veja abaixo)
9. Clique em **Salvar**

## Adicionando valores de atributo

Os valores de atributo são as opções individuais dentro de um atributo. Você pode adicioná-los diretamente ao criar ou editar um atributo, usando o formulário de valores inline no final da página de detalhes do atributo.

Para cada valor:

- **Valor** — o rótulo de exibição (ex.: `Pequeno`, `Vermelho`, `Algodão`)
- **Slug** — preenchido automaticamente a partir do valor; usado em URLs e identificadores de variação
- **Hex de Cor** — relevante apenas para atributos de tipo **Amostra de Cor**. Insira um código de cor em hexadecimal (ex.: `#FF0000` para vermelho) para que a amostra mostre a cor correta.
- **Ordem de Classificação** — controla a ordem em que os valores aparecem no seletor. Atribua números mais baixos aos valores que você deseja que apareçam primeiro.

### Ordenando valores logicamente

Para atributos de tamanho, defina a ordem de classificação para que os tamanhos sigam da pequeno para o grande:

| Valor | Ordem de Classificação |
|---|---|
| XS | 1 |
| S | 2 |
| M | 3 |
| L | 4 |
| XL | 5 |
| 2XL | 6 |

Para atributos de cor, você pode ordenar alfabeticamente ou agrupar cores semelhantes — o que fizer mais sentido para seus clientes.

## Gerenciando valores de atributo separadamente

Você também pode gerenciar os valores de atributo de forma independente em **Catálogo > Valores de Atributo**. Esta lista é útil quando você precisa encontrar ou atualizar um valor específico em seu catálogo sem abrir cada atributo individualmente. A lista pode ser filtrada pelo nome do atributo.

## Atribuindo atributos a produtos

Atributos são atribuídos no nível do produto, e não globalmente.

Para adicionar um atributo a um produto:

1. Navegue até **Catalogo > Produtos** e abra um produto variável
2. Na aba **Variações**, localize a seção **Atributos**
3. Selecione o atributo que deseja adicionar
4. Escolha quais dos valores do atributo estão disponíveis para este produto
5. Salve o produto — o Spwig gerará as combinações de variantes correspondentes

Para orientação detalhada sobre como configurar variantes de produto, consulte o tópico de ajuda **Variantes de Produto**.

## Exemplos práticos

### Exemplo: Atributo de tamanho de roupa

| Campo | Valor |
|---|---|
| Nome | Tamanho |
| Tipo | Grupo de Botões |
| É Obrigatório | Sim |
| Ordem de Classificação | 1 |
| Valores | XS (1), S (2), M (3), L (4), XL (5), 2XL (6) |

### Exemplo: Atributo de amostra de cor

| Campo | Valor |
|---|---|
| Nome | Cor |
| Tipo | Amostra de Cor |
| É Obrigatório | Sim |
| Ordem de Classificação | 2 |
| Valores | Preto (#000000), Branco (#FFFFFF), Azul-Marinho (#001F5B), Vermelho (#CC0000) |

### Exemplo: Atributo de material

| Campo | Valor |
|---|---|
| Nome | Material |
| Tipo | Seletor de Dropdown |
| É Obrigatório | Não |
| Ordem de Classificação | 3 |
| Valores | 100% Algodão, Mistura de Algodão/Poliéster, Lã Merino, Linho |

## Dicas

- Crie atributos que representem decisões reais de compra feitas pelos clientes — se os clientes não precisarem escolher, talvez ele não precise ser um atributo
- Use nomes consistentes em todo o seu catálogo: se alguns produtos usarem "Cor" e outros usarem "Color", os clientes e sua equipe podem se confundir com a inconsistência
- A ordem de classificação tanto nos atributos quanto nos valores importa — coloque o atributo mais importante primeiro (geralmente Tamanho ou Cor) e ordene os valores em uma sequência lógica
- O tipo Amostra de Cor requer códigos hexa precisos; teste as cores em um seletor de cor do navegador antes de salvar para garantir que a amostra corresponda à cor real do produto
- Se você precisar renomear um atributo (por exemplo, de "Color" para "Colour"), atualize o campo **Nome** em vez de criar um novo atributo — alterar o nome não afeta as atribuições existentes de produtos
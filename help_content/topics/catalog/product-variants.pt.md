---
title: Variantes de Produto
---

As variantes de produto permitem oferecer um único produto em múltiplas opções — como diferentes tamanhos, cores ou materiais — cada uma com seu próprio SKU, preço e nível de estoque. Navegue até qualquer **Produto Variável** e clique na aba **Variações**.

![Variantes de produto](/static/core/admin/img/help/product-variants/product-variants.webp)

## Entendendo Variantes

Um **Produto Variável** é um tipo de produto que suporta múltiplas variações. Por exemplo, uma camiseta pode estar disponível em:
- **Cores**: Azul, Vermelho, Verde
- **Tamanhos**: P, M, G, GG

Cada combinação (ex.: "Azul / Grande") se torna uma variante separada com seu próprio estoque e preço.

## Configurando um Produto Variável

### Passo 1: Definir o Tipo de Produto

1. Abra o formulário de edição do produto (ou crie um novo produto)
2. Na aba **Informações Básicas**, defina o **Tipo de Produto** como **Produto Variável**
3. Salve o produto

### Passo 2: Definir Atributos

Atributos são as opções que diferenciam suas variantes (ex.: Tamanho, Cor).

1. Vá para a aba **Variações**
2. Na seção **Atributos do Produto**, clique em **+ Adicionar Atributo** para atribuir um atributo existente, ou **Criar Novo** para definir um novo
3. Para cada atributo, especifique os valores disponíveis (ex.: Pequeno, Médio, Grande)

### Passo 3: Criar Variantes

1. Na seção **Variantes do Produto**, clique em **+ Adicionar Nova Variante**
2. Configure cada variante:
   - **Nome** — Rótulo descritivo (ex.: "Azul", "Grande / Vermelho")
   - **SKU** — Código único de unidade de manutenção de estoque
   - **Preço** — Preço específico da variante (pode diferir do produto base)
   - **Estoque** — Nível atual de inventário
3. Repita para cada variante necessária

## Gerenciando Variantes

### Detalhes da Variante

Cada cartão de variante exibe:
- **Nome** e **SKU** — Informações de identificação
- **Preço** — Preço de venda atual
- **Nível de estoque** — Quantidade disponível com indicador de status (Em Estoque / Estoque Baixo / Fora de Estoque)

Clique em um cartão de variante para expandir e editar todos os seus detalhes.

### Configurações Específicas da Variante

Cada variante pode ter suas próprias configurações:

| Configuração | Descrição |
|-------------|-----------|
| **Preço** | Substituir o preço do produto base |
| **Preço Comparativo** | Exibir preço de promoção com tachado |
| **SKU** | Identificador único para inventário |
| **Nível de Estoque** | Rastreamento de inventário independente |
| **Peso** | Para cálculos de frete |
| **Imagem** | Imagem de produto específica da variante |

### Editando uma Variante

1. Clique no **ícone de edição** no cartão da variante
2. Modifique os campos desejados
3. Clique em **Salvar** para atualizar

### Excluindo uma Variante

1. Clique no **ícone de exclusão** no cartão da variante
2. Confirme a exclusão

**Nota:** Excluir uma variante remove seu registro de inventário. Esta ação não pode ser desfeita.

## Atributos

### O Que São Atributos?

Atributos são definições de opções reutilizáveis. Uma vez que você crie um atributo como "Tamanho" com valores "P, M, G, GG", você pode atribuí-lo a qualquer produto variável.

### Criando Atributos

1. Na aba Variações, clique em **Criar Novo** na seção Atributos do Produto
2. Insira o nome do atributo (ex.: "Cor")
3. Adicione valores (ex.: "Vermelho", "Azul", "Verde")
4. Salve o atributo

### Atribuindo Atributos

Atributos podem ser atribuídos a múltiplos produtos. O mesmo atributo "Tamanho" pode ser usado em Camisetas, Calças e Sapatos.

## Exibição na Loja Virtual

Na loja virtual, produtos variáveis exibem:
- Seletores de opções (menus suspensos ou amostras) para cada atributo
- Atualização automática de preço quando uma variante é selecionada
- Disponibilidade de estoque por variante
- Imagens específicas da variante

## Dicas

- Use nomes de atributos consistentes entre os produtos para uma experiência de compra uniforme.
- Configure todos os atributos antes de criar variantes para agilizar o processo.
- Faça upload de imagens específicas por variante para que os clientes vejam exatamente o que estão comprando.
- Mantenha os SKUs sistemáticos (ex.: "CAMISETA-AZUL-G") para facilitar o gerenciamento de inventário.
- Use o preço comparativo em variantes para realizar promoções específicas por tamanho ou cor.

---
title: "Pacotes de Produtos"
---

Pacotes de produtos permitem que você venda conjuntos pré-montados de produtos a um preço especial. Isso é perfeito para conjuntos de presentes, kits iniciais ou qualquer combinação de produtos que você queira oferecer juntos com desconto.

![Bundle components admin](/static/core/admin/img/help/product-bundles/bundle-components.webp)

## Estratégias de Preço

Escolha como o preço do pacote é calculado:

| Estratégia | Descrição |
|------------|-----------|
| **Preço Fixo** | Defina um preço único para todo o pacote, independentemente dos preços dos componentes. |
| **Desconto Percentual** | Calcule automaticamente o preço como uma porcentagem de desconto sobre os preços combinados dos componentes. |
| **Soma dos Componentes** | O preço do pacote é igual ao total de todos os preços dos componentes (útil para exibição agrupada sem desconto). |

## Criando um Pacote

### Passo 1: Criar o Produto

1. Navegue até **Produtos > Todos os Produtos** e clique em **+ Adicionar Produto**
2. Defina o **Tipo de Produto** como **Pacote de Produtos**
3. Preencha o nome do pacote, descrição e imagens
4. Salve o produto

### Passo 2: Adicionar Componentes

Mude para a aba **Itens do Pacote** para adicionar produtos ao seu pacote:

1. Clique em **+ Adicionar Componente**
2. Pesquise e selecione um produto no menu suspenso
3. Defina a **Quantidade** para cada componente (ex.: 2x máscaras faciais em um kit de cuidados com a pele)
4. Defina a **Ordem de Classificação** para controlar a ordem de exibição
5. Opcionalmente, marque um componente como **Opcional** (os clientes podem excluí-lo)
6. Se o componente for um produto variável, escolha:
   - Uma **variante fixa** — todos os clientes recebem a mesma variante
   - **Permitir seleção de variante** — os clientes escolhem sua variante preferida no checkout

O resumo na parte inferior mostra o **Total de Componentes** e o **Valor do Pacote** (soma dos preços dos componentes).

### Passo 3: Configurar Preços

Mude para a aba **Preços**:

1. Selecione sua **Estratégia de Preço do Pacote**
2. Para **Preço Fixo** — insira o preço do pacote diretamente
3. Para **Desconto Percentual** — defina a porcentagem de desconto (ex.: 15% de desconto)
4. Para **Soma dos Componentes** — o preço é calculado automaticamente

## O Que Pode Ser Incluído em Pacotes

| Tipo de Produto | Pode Ser um Componente? |
|----------------|------------------------|
| Produto Simples | Sim |
| Produto Variável | Sim (variante fixa ou escolha do cliente) |
| Produto Digital | Sim |
| Produto Personalizável | Não |
| Produto Configurável | Não |
| Pacote de Produtos | Não (pacotes não podem ser aninhados) |
| Cartão Presente | Não |

## Gestão de Estoque

O estoque do pacote é gerenciado através dos seus componentes:

- **Todos os componentes devem estar em estoque** para que o pacote possa ser comprado
- Quando um pacote é pedido, o estoque é deduzido de cada produto componente individualmente
- Se qualquer componente ficar sem estoque, o pacote fica indisponível
- Os níveis de estoque dos componentes são verificados em tempo real durante o checkout

## Componentes Opcionais

Marque um componente como **Opcional** para permitir que os clientes personalizem seu pacote:

- Componentes opcionais são incluídos por padrão, mas podem ser removidos pelo cliente
- O preço do pacote é ajustado conforme componentes opcionais são excluídos
- Pelo menos um componente deve ser não-opcional (obrigatório)

## Experiência do Cliente

Quando um cliente visualiza um pacote na sua vitrine:

1. **Lista de Componentes** — Todos os produtos incluídos são exibidos com imagens e quantidades
2. **Economia do Pacote** — O desconto em comparação com a compra individual dos itens é mostrado
3. **Seleção de Variante** — Para componentes com seleção de variante habilitada, os clientes escolhem sua opção preferida
4. **Itens Opcionais** — Os clientes podem ativar ou desativar componentes opcionais
5. **Adicionar ao Carrinho Único** — O pacote inteiro é adicionado como um único item

## Dicas

- Use a estratégia de Desconto Percentual para o preço mais flexível — ele se ajusta automaticamente quando os preços dos componentes mudam.
- Mostre o valor da economia de forma proeminente na descrição do produto para incentivar a compra de pacotes.
- Mantenha os pacotes com 3-5 componentes para a melhor experiência do cliente. Muitos itens podem parecer excessivos.
- Use componentes opcionais para oferecer uma versão "básica" e "premium" do mesmo pacote.
- Verifique regularmente se todos os produtos componentes ainda estão ativos e em estoque.

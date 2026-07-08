---
title: Produtos Personalizáveis
---

Produtos personalizáveis permitem que seus clientes criem seus próprios produtos usando um editor visual diretamente em sua loja virtual. Seja você que vende camisetas personalizadas, pôsteres personalizados, mercadorias com marca, ou cartões de felicitação, esta funcionalidade fornece aos clientes as ferramentas para adicionar texto, carregar imagens e usar clipes de arte para criar designs únicos — tudo sem sair de sua loja.

## Como funciona

Um produto personalizável combina um produto padrão Spwig com um **editor de design visual**. Você define as superfícies que podem ser personalizadas do produto (como a frente e a parte de trás de uma camiseta), carrega imagens de mockup para que os clientes vejam seu design no contexto e define as regras para o que os clientes podem fazer em cada superfície.

Quando um cliente visita um produto personalizável em sua loja virtual, ele vê um editor de canvas ao vivo sobreposto na imagem de mockup do produto. Ele pode adicionar texto, carregar suas próprias imagens e navegar na sua biblioteca de clipes de arte para criar seu design. O editor mostra o design exatamente como ele será no produto final.

### Dois casos de uso

Produtos personalizáveis funcionam bem em duas situações comuns:

| Caso de uso | Exemplo | Superfícies | Configuração típica |
|-------------|---------|------------|---------------------|
| **Design de roupas** | Camisetas personalizadas, moletom, sacolas de compras | Múltiplas (frente, trás, mangas) | Fontes em negrito, clipes de arte de humor/esportes, restrições por superfície |
| **Design de impressão** | Pôsteres, cartões de felicitação, cartões de negócios | Única (frente apenas) | Alta DPI, configurações de sangria, fontes elegantes, bordas decorativas |

O processo de configuração é o mesmo para ambos — a diferença está no número de superfícies que você define, quais clipes de arte e fontes você fornece e como você configura as opções de impressão.

## Conceitos-chave

### Configuração de design

Todo produto personalizável tem uma **configuração de design** que controla o comportamento geral do editor: quais ferramentas estão disponíveis (texto, upload de imagem, clipes de arte), limites de upload e regras de preços. Este é o painel de controle mestre para o editor de design do produto.

### Superfícies

Uma **superfície** é uma face personalizável do seu produto. Uma camiseta geralmente tem três superfícies (frente, trás, manga), enquanto um pôster tem apenas uma. Cada superfície tem sua própria imagem de mockup, posição da zona de design, dimensões físicas e configurações de qualidade de impressão.

### Zona de design

A **zona de design** é a área retangular na imagem de mockup onde os clientes podem colocar seus elementos de design. Você posiciona essa zona visualmente na página de configuração do administrador arrastando e redimensionando-a sobre a imagem de mockup. A zona define onde os designs aparecem no produto final.

### Modelos

**Modelos de design** são designs pré-feitos que você cria para os clientes. Em vez de começar com um canvas em branco, os clientes podem navegar na galeria de modelos, escolher um que gostem e personalizá-lo. Os modelos podem incluir elementos bloqueados que os clientes não podem modificar — por exemplo, um logotipo da empresa que deve sempre aparecer na mesma posição.

### Clipes de arte e fontes

Você cria uma **biblioteca de clipes de arte** de imagens que os clientes podem adicionar aos seus designs, organizadas em categorias (por exemplo, "Esportes", "Bordas", "Feriados"). Você também pode carregar **fontes personalizadas** além das fontes do sistema padrão, dando aos clientes mais opções criativas.

### Preços

O editor de design oferece um modelo de preços flexível com quatro componentes de taxa:

| Tipo de taxa | Descrição |
|--------------|-----------|
| **Taxa de design base** | Taxa fixa adicionada quando qualquer personalização é aplicada |
| **Taxa por superfície** | Taxa adicional para cada superfície usada além da primeira |
| **Taxa por upload** | Taxa para cada imagem carregada pelo cliente |
| **Taxa por texto** | Taxa para cada elemento de texto adicionado |

Os preços são atualizados em tempo real conforme o cliente adiciona elementos, então não há surpresas no checkout.

## Modos do editor

O Spwig oferece dois modos de editor:

- **Editor de Canvas** — Um editor de design visual completo com um canvas ao vivo, ferramentas de texto, upload de imagem, navegador de clipes de arte e pré-visualização em tempo real na imagem de mockup do produto.

# Modo recomendado para produtos personalizáveis

Este é o modo recomendado para a maioria dos produtos personalizáveis.
- **Formulário simples** — Abordagem tradicional com base em formulário, onde os clientes preenchem campos de texto e carregam imagens sem um canvas visual.

Apropriado para produtos com personalização mínima (ex.: gravar um nome em uma joia).

## Fluxo de trabalho do vendedor

Configurar um produto personalizável segue este fluxo de trabalho:

1. **Criar o produto** — Adicione um novo produto com o tipo definido como **Produto Personalizável**
2. **Configurar superfícies** — Defina cada face personalizável, carregue imagens de mockup e posicione as zonas de design
3. **Configurar configurações** — Escolha quais ferramentas habilitar, defina limites de upload e configure o preço
4. **Adicionar ativos** — Construa sua biblioteca de clipart e carregue fontes personalizadas
5. **Criar modelos** — Projete pontos de início pré-feitos com controles de bloqueio opcionais
6. **Testar e publicar** — Visualize o editor no site de loja e verifique se tudo funciona

Para instruções detalhadas de configuração, veja [Configurando um Produto Personalizável](/admin/customizable-product/).

## Experiência do cliente

Quando um cliente visita um produto personalizável no seu site de loja:

1. **Navegar por modelos** — Eles podem começar com um modelo pré-feito ou começar com um canvas em branco
2. **Alternar superfícies** — Abas no topo permitem alternar entre superfícies (ex.: frente e verso de uma camisa)
3. **Adicionar elementos** — O painel de ferramentas fornece ferramentas de texto, upload de imagem e clipart
4. **Personalizar** — Eles podem ajustar fontes, cores, tamanhos, posições e aplicar filtros de imagem
5. **Ver preços** — A taxa de design é atualizada em tempo real conforme eles adicionam elementos
6. **Salvar designs** — Clientes registrados podem salvar designs para continuar editando depois
7. **Adicionar ao carrinho** — O design está vinculado ao item do carrinho e congelado quando o pedido é feito

## O que acontece após o pedido

Quando um cliente faz um pedido contendo um produto personalizado:

- O design é **congelado como um instantâneo** — ele não pode ser modificado após a compra
- O sistema gera **arquivos de atendimento de alta resolução** para cada superfície
- Você pode baixar esses arquivos prontos para impressão da página de detalhes do pedido no seu painel de administração
- Os arquivos são renderizados na DPI que você configurou para cada superfície

Para detalhes sobre o atendimento de pedidos personalizados, veja [Atendendo Pedidos de Produtos Personalizáveis](/admin/orders/).

## Dicas

- Comece com um produto simples (uma superfície, como um pôster) para aprender o processo de configuração antes de lidar com produtos de múltiplas superfícies, como camisas.
- Carregue imagens de mockup de alta qualidade — elas são a primeira coisa que os clientes veem e estabelecem a expectativa de qualidade para toda a experiência.
- Crie 3-5 modelos de design para cada produto para reduzir a intimidação do "canvas em branco" e inspirar os clientes.
- Use restrições por superfície para controlar o que os clientes podem fazer em cada superfície. Por exemplo, permita apenas o upload de um logotipo pequeno em um mangote de camisa, enquanto permite liberdade total de design na frente.
- Defina requisitos mínimos de DPI apropriados para o seu método de impressão — 150 DPI para impressão em tela, 300 DPI para impressão digital de alta qualidade.
- Teste o fluxo completo do cliente (design, salvar, adicionar ao carrinho, checkout) antes de publicar um produto personalizável.
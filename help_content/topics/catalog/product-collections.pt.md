---
title: Coleções de Produtos
---

Coleções permitem que você agrupe produtos para exibição em sua loja virtual. Diferente das categorias — que organizam seu catálogo inteiro em uma hierarquia permanente — as coleções são agrupamentos flexíveis e curados que você cria para um propósito específico. Uma coleção pode destacar novidades, mostrar itens para uma campanha sazonal ou apresentar uma seleção cuidadosamente escolhida de best-sellers.

Navegue até **Catálogo > Coleções** para gerenciar suas coleções.

## Coleções vs categorias

Ambas as categorias e as coleções agrupam produtos, mas servem para propósitos diferentes:

| | Categorias | Coleções |
|---|---|---|
| **Propósito** | Estrutura permanente do catálogo | Agrupamentos flexíveis e curados |
| **Hierarquia** | Sim — estrutura aninhada de pai/filho | Não — agrupamentos planos |
| **Produtos por grupo** | Cada produto pertence a uma categoria | Um produto pode aparecer em muitas coleções |
| **Uso típico** | Menu de navegação da loja, pesquisar por departamento | Páginas de destino, campanhas, conjuntos destacados |

Use categorias para "como sua loja está organizada" e coleções para "o que você quer destacar agora".

## Tipos de coleção

Ao criar uma coleção, escolha um tipo que corresponda a como você deseja gerenciar a lista de produtos:

| Tipo | Como os produtos são adicionados |
|---|---|
| **Seleção Manual** | Você escolhe exatamente quais produtos aparecem, um por um |
| **Regras Automáticas** | Produtos são adicionados automaticamente com base em critérios que você define |
| **Produtos Destacados** | Uma seleção editorial curada, gerenciada manualmente |
| **Sazonal** | Uma seleção baseada no tempo, normalmente gerenciada manualmente para campanhas |

Os tipos Manual e Produtos Destacados lhe dão controle preciso. Coleções automáticas podem crescer com seu catálogo sem manutenção contínua.

## Criando uma coleção

1. Navegue até **Catálogo > Coleções**
2. Clique em **+ Adicionar Coleção**
3. Preencha a seção **Informações Básicas**:
   - **Nome** — o nome da coleção como será exibido em sua loja virtual
   - **Slug** — o caminho da URL para a página da coleção (preenchido automaticamente a partir do nome; você pode personalizá-lo)
   - **Descrição** — uma descrição exibida na página da loja virtual da coleção
4. Selecione um **Tipo de Coleção**
5. Adicione produtos:
   - Para os tipos **Seleção Manual** e **Produtos Destacados**: use o campo **Produtos** para pesquisar e adicionar produtos
   - Para o tipo **Automático**: defina os critérios no campo **Critérios Automáticos**
6. Carregue imagens:
   - **Imagem** — a imagem principal da coleção usada em páginas de listagem e miniaturas
   - **Imagem de Banner** — uma imagem de banner mais larga exibida no topo da página da coleção
7. Configure os campos **SEO** (opcionais, mas recomendados):
   - **Título Meta** — o título da página exibido nos resultados de pesquisa
   - **Descrição Meta** — a descrição exibida abaixo do título nos resultados de pesquisa
8. Defina as **Opções de Exibição**:
   - **Ativo** — controla se a coleção é visível em sua loja virtual
   - **Destacado** — marca a coleção para exibição destacada no seu tema
   - **Ordem de Exibição** — controla a ordem em que as coleções aparecem em páginas de listagem (números mais baixos aparecem primeiro)
9. Clique em **Salvar**

## Adicionando produtos a uma coleção

Para coleções manuais, use o campo de autocompletar **Produtos** para pesquisar seu catálogo e selecionar itens. Você pode adicionar tantos produtos quantos precisar — não há limite.

Produtos podem pertencer a múltiplas coleções ao mesmo tempo. Por exemplo, um produto poderia estar tanto na sua coleção "Venda de Verão" quanto na sua coleção "Best-sellers" sem conflito algum.

## Exibindo coleções em sua loja virtual

Cada coleção recebe automaticamente sua própria página em `/collection/{slug}/`. Você pode vincular as páginas das coleções ao seu menu de navegação, ao construtor de páginas ou a banners promocionais.

A bandeira **Destacado** é usada pelo seu tema para determinar quais coleções aparecem em locais destacados — por exemplo, uma grade de coleções destacadas na página inicial. Consulte a documentação do seu tema para entender exatamente como as coleções destacadas são exibidas.

## Gerenciando a visibilidade da coleção

- **Ativo** controla se a página da coleção está acessível publicamente.

Uma coleção inativa é oculta dos clientes, mas mantida no administrador para que você possa reativá-la posteriormente.
- **Ordem de classificação** determina a ordem em que as coleções aparecem em páginas de listagem.

Atribua números mais baixos às coleções que você deseja que apareçam primeiro.

## SEO para coleções

Cada coleção possui seus próprios campos **Título Meta** e **Descrição Meta**. Esses controlam o que aparece nos resultados de motores de busca quando alguém encontrar sua página de coleção. Se você deixar esses campos em branco, seu tema geralmente recorrerá ao nome e descrição da coleção.

Bons títulos de SEO para coleções são descritivos e específicos:
- "Vestidos de Verão 2026 — Estilos Florais e Leves" tem um desempenho melhor do que "Coleção de Verão"
- "Tênis de Corrida para Homens — Leve e Respirável" tem um desempenho melhor do que "Tênis de Corrida"

## Dicas

- Mantenha os nomes das coleções curtos e claros — eles aparecem como títulos de página e texto de link na navegação do seu loja virtual
- Use coleções sazonais ou de campanhas com um plano de início e fim: crie a coleção, ative-a quando a campanha começar e desative-a (em vez de excluí-la) quando ela terminar, para que você possa referenciá-la posteriormente
- O campo **Ordem de classificação** vale a pena ser definido com intenção — o padrão é 0 para todas as coleções, o que significa que elas são classificadas em ordem alfabética. Atribua números específicos para controlar quais coleções aparecem com mais destaque
- Uma coleção sem produtos mostrará uma página vazia para os clientes — adicione produtos antes de ativá-la ou deixe a coleção inativa até que esteja pronta
- Verifique a bandeira **Destacado** apenas para coleções que você realmente deseja destacar; a maioria dos temas reserva os espaços destacados para um pequeno número de coleções e a exibição pode parecer congestionada se muitas forem marcadas
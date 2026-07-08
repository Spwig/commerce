---
title: Gerenciamento de Categorias
---

As categorias ajudam a organizar seu catálogo de produtos para que os clientes possam navegar e encontrar produtos facilmente. Navegue até **Produtos > Categorias** na barra lateral do admin.

![Lista de categorias](/static/core/admin/img/help/manage-categories/category-list.webp)

## Lista de Categorias

A página de gerenciamento de categorias exibe todas as suas categorias como cartões com:

- **Imagem em miniatura** — Identificador visual da categoria
- **Nome e slug** — Nome de exibição e identificador amigável para URL
- **Contagem de produtos** — Número de produtos atribuídos a esta categoria
- **Status** — Publicada ou rascunho

Use as **abas de filtro** no topo para visualizar rapidamente Todas, Publicadas ou Rascunho. A **barra de pesquisa** permite encontrar categorias pelo nome.

## Criando uma Categoria

1. Clique em **+ Adicionar Categoria** no canto superior direito
2. Preencha os detalhes da categoria:
   - **Nome** — O nome de exibição que os clientes verão
   - **Slug** — Gerado automaticamente a partir do nome, usado em URLs
   - **Categoria Pai** — Deixe vazio para uma categoria de nível superior, ou selecione uma categoria pai para criar uma subcategoria
   - **Descrição** — Descrição em texto rico exibida na página da categoria
3. Faça upload de uma **imagem da categoria** — exibida nos menus de navegação e listagens de categorias
4. Configure os **campos de SEO** (meta título, descrição) na aba SEO
5. Clique em **Salvar**

## Hierarquia de Categorias

As categorias suportam aninhamento ilimitado para criar uma estrutura em árvore:

- **Categorias de nível superior** — Itens de navegação principal (ex.: "Roupas", "Eletrônicos")
- **Subcategorias** — Aninhadas sob uma categoria pai (ex.: "Roupas > Masculino > Camisetas")

O menu suspenso de categoria pai mostra o caminho completo da hierarquia para ajudá-lo a escolher o nível correto.

## Configurações de Categoria

### Visibilidade

- **Publicada** — A categoria aparece na loja virtual e na navegação
- **Rascunho** — A categoria está oculta dos clientes, mas acessível no admin

### Categorias em Destaque

Marque categorias como **destaque** para destacá-las na sua página inicial ou em seções especiais de navegação. Categorias em destaque podem ser exibidas usando o elemento de grade de categorias do Page Builder.

### Ordem de Classificação

Controle como as categorias aparecem nos menus de navegação definindo um valor de **ordem de classificação**. Números menores aparecem primeiro.

## Atribuindo Produtos a Categorias

Existem duas maneiras de atribuir produtos:

1. **No formulário de edição do produto** — Selecione uma categoria no menu suspenso Categoria na aba Informações Básicas
2. **Atribuição em massa** — Selecione vários produtos na lista de produtos e use a ação em massa para atribuí-los a uma categoria

Cada produto pode pertencer a uma categoria principal. Use tags ou coleções para agrupamentos adicionais.

## Páginas de Categoria na Loja Virtual

Cada categoria publicada recebe automaticamente uma página dedicada mostrando:
- Nome e descrição da categoria
- Imagem de banner (se definida)
- Grade de produtos com todos os produtos atribuídos
- Opções de filtragem e ordenação

A URL da página da categoria segue o padrão: `sualoja.com/category/slug-da-categoria/`

## Dicas

- Mantenha sua árvore de categorias rasa — 2-3 níveis de profundidade é o ideal para usabilidade de navegação.
- Use nomes de categorias descritivos que correspondam ao que os clientes pesquisam.
- Adicione imagens às categorias para uma experiência de navegação mais visual.
- Configure sua estrutura de categorias antes de adicionar produtos para manter tudo organizado.
- Use a descrição da categoria para SEO — inclua palavras-chave relevantes de forma natural.

---
title: Adicionando um Produto
---

Este é o primeiro de quatro artigos de um documento mais longo.

<!-- screenshots-needed:
- url: /admin/catalog/product/<id>/change/
  filename: inventory-tab.webp
  description: aba de estoque, rolando para mostrar os cartões de Atributos Físicos, Envio,
    e Pré-venda juntos (com a opção de Envio Necessário marcada, um Pacote de Envio Padrão
    selecionado e a opção de Pré-venda marcada com uma data e mensagem de lançamento
    preenchidas, de modo que todos os novos campos sejam visíveis de uma só vez).
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
  notes: Substitui o inventory-tab.webp existente, que data da época dos cartões de Envio
    e Pré-venda e já não corresponde ao formulário em tempo real.
- url: /admin/catalog/product/<id>/change/
  filename: tags-card.webp
  description: aba de Informações Básicas, rolando para mostrar o cartão de Tags, com algumas tags
    já aplicadas ao produto no seletor de tags.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
- url: /admin/catalog/product/<id>/change/
  filename: advanced-tab.webp
  description: aba Avançada mostrando o cartão de Configurações da Página do Produto (caixa de seleção de Modelo de Página com uma opção não padrão selecionada) e o cartão de Detalhes Técnicos
    logo abaixo.
  save-to: core/static/core/admin/img/help/add-product/
  viewport: 1440x900
-->

Este guia o orienta na criação de um novo produto em sua loja. O formulário de produto é organizado em seções que abrangem informações básicas, mídia, preços, estoque, SEO e muito mais — então você pode preencher tudo de uma vez ou voltar para completar as seções posteriormente.

## Começando

A partir da barra lateral, navegue até **Produtos > Todos os Produtos** para ver seu catálogo de produtos. Clique no botão **+ Adicionar Produto** no canto superior direito para abrir o formulário de criação de produto.

![Página de lista de produtos](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informações básicas

A seção **Informações Básicas** é onde você define a identidade central do seu produto.

![Formulário de adição de produto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campos obrigatórios

- **Nome** — O nome do produto exibido aos clientes. Clique no ícone de globo para adicionar traduções para outros idiomas.
- **Slug** — Versão amigável de URL do nome (gerado automaticamente). Personalize-o se necessário.
- **SKU** — Seu código interno de unidade de estoque.
- **Tipo de Produto** — Escolha entre: Simples, Variável, Digital, Pacote, Voucher de Presente, Personalizável, Configurável ou Reserva.
- **Categoria** — Atribua o produto a uma categoria para organização e navegação na loja.

### Status e visibilidade

Encontrado na seção **Status** no final do formulário:

- **Status** — Defina como **Rascunho** enquanto estiver trabalhando, **Publicado** quando estiver pronto para venda, ou **Encerrado** para produtos que você não oferece mais.
- **Destaque** — Marque para destacar este produto em sua loja.
- **Produto Digital** — Marque se este produto incluir downloads digitais (arquivos, licenças). Pode ser combinado com qualquer tipo de produto.
- **Esconder da Loja** — Esconde o produto das listagens do catálogo, mantendo-o disponível como opção de configurador ou componente de pacote.

### Campos opcionais

- **Marca** — Associe a uma marca, se aplicável.
- **Tags** — Atribua uma ou mais tags no cartão de **Tags** mais abaixo nesta aba. As tags são diferentes de Coleções — são rótulos rápidos e livres para organizar e filtrar produtos, em vez de um agrupamento de merchandising. Comece a digitar para procurar uma tag existente, ou digite um novo nome para criá-la na hora. Veja o tópico de ajuda **Tags de Produto** para criar, renomear e excluir em massa tags diretamente.

### Descrições do produto

- **Descrição Curta** — Apresenta-se em listagens e cartões de produtos. Mantenha curta e convincente.
- **Descrição Completa** — Descrição detalhada do produto exibida na página de detalhes do produto. Use o editor de texto rico para adicionar formatação, imagens, vídeos e tabelas.

Ambos os campos de descrição suportam o recurso de tradução — clique no ícone de globo para fornecer conteúdo em outros idiomas.

### Recursos e especificações

A seção **Detalhes do Produto** contém dois campos de dados estruturados:

- **Recursos** — Pares chave-valor para destaque do produto (ex.: "Autonomia da bateria: 20 horas").
- **Especificações** — Detalhes técnicos para a aba de especificações na página do produto (ex.: "Processador: Intel i7").

## Mídia

A seção **Mídia** permite que você gerencie imagens do produto usando o Biblioteca de Mídia integrada.

![Guia de Mídia](/static/core/admin/img/help/add-product/media-tab.webp)

1. Clique em **+ Adicionar Imagens da Biblioteca de Mídia** para abrir o seletor de mídia.
2. Selecione imagens existentes ou faça upload de novas diretamente.
3. Arraste as imagens para reordená-las — a **primeira imagem** torna-se a imagem principal do produto exibida em listas e cards.

O campo **Tipo de Galeria**, no cartão **Configurações da Galeria** abaixo da lista de imagens, controla como as imagens são exibidas na loja: Galeria Padrão, Carrossel, Layout de Grade, Galeria de Zoom ou Visualização de 360°.

## Preços

Defina o preço do seu produto e configure vendas.

![Guia de Preços](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Preço regular

- **Preço Regular** — O preço de varejo padrão que os clientes verão. A moeda é definida junto com o valor do preço.
- **Custo** — Seu custo de mercadoria, usado para cálculos de lucro. Isso nunca é mostrado aos clientes.

### Configurações de venda

Configure descontos temporários:

- **Tipo de Venda** — Escolha entre: Nenhuma Venda, Preço de Venda Fixo, Valor Off, ou Porcentagem Off.
- **Valor da Venda** — O valor do desconto ou porcentagem.
- **Data de Início da Venda / Data de Fim da Venda** — Agende quando a venda ativar e expirar. Deixe em branco para iniciar imediatamente ou sem data de término.

### Preços em múltiplas moedas

Se o suporte a múltiplas moedas estiver habilitado na sua loja, um campo **Estratégia de Preços** aparece:

- **Preço Dinâmico** — Os preços em outras moedas são calculados automaticamente usando as taxas de câmbio configuradas por você.
- **Preço Fixo** — Defina um preço específico para cada moeda independentemente usando a seção **Preços em Múltiplas Moedas** que aparece abaixo.

## Estoque

Gerencie níveis de estoque, comportamento de envio e atributos de produtos físicos.

![Guia de Estoque](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gerenciamento de estoque

- **Rastrear Estoque** — Ative para rastrear as quantidades de estoque (ativado por padrão).
- **Limite de Estoque Baixo** — Receba alertas quando o estoque cair abaixo desse número (padrão: 5).
- **Permitir Encomendas Adiadas** — Ative para aceitar pedidos mesmo quando sem estoque.
- **Ação Quando Esgotado** — Substitua o comportamento site-wide ou de categoria quando este produto se esgotar: oculte-o, mostre-o como indisponível, mostre um botão "Notifique-me", ou permita encomendas adiadas.

As quantidades de estoque são gerenciadas por armazém. Após salvar o produto, use a seção **Itens de Estoque** no final do formulário (ou navegue até **Produtos > Itens de Estoque**) para definir as quantidades em cada localização de armazém.

### Atributos físicos

Digite o peso do produto (kg) e as dimensões (comprimento, largura, altura em cm) para cálculos precisos de envio.

### Envio

- **Requer Envio** — Se este produto precisa ser entregue ao cliente. Ativado por padrão para produtos físicos; sua loja e checkout usam para decidir se coletam o endereço de envio e orçam o frete do pedido. O Spwig desligaá-lo automaticamente para produtos Digitais, de Reserva e de Vales-presente, já que esses nunca são enviados — você não precisa (nem pode) reativá-lo para esses tipos de produtos. Deixe-o marcado para um produto físico que pareça próximo a um digital, como um vale-presente impresso que seja enviado em uma caixa.
- **Pacote de Envio Preferido** — Escolha opcionalmente um dos seus pacotes de envio configurados. Ao definir, as dimensões próprias do pacote são usadas para cálculos de taxa de envio em vez do peso e dimensões deste produto acima — útil quando um produto sempre é enviado na mesma caixa padrão ou envelope. Deixe em branco para usar as próprias características físicas do produto. Gerencie os pacotes disponíveis em **Envio > Pacotes**.

### Pré-venda

Use the **Pré-venda** card to sell a product before it has any stock — useful for upcoming releases you want to start taking orders for ahead of launch:

- **É Pré-venda** — Ative para permitir que os clientes comprem este produto mesmo quando estiver em falta.
- **Data de Lançamento da Pré-venda** — A data esperada de disponibilidade, mostrada aos clientes.
- **Mensagem da Pré-venda** — Uma mensagem curta personalizada mostrada aos clientes, com até 200 caracteres (ex.: "Envio em Março de 2026").

### Identificadores do produto

Códigos padrão de produtos para listagens de mercado e sistemas de estoque:

- **GTIN** — Número de Item de Comércio Global
- **EAN** — Número de Artigo Europeu
- **UPC** — Código de Produto Universal (EUA)
- **ISBN** — Para livros
- **ASIN** — Identificador da Amazon
- **MPN** — Número da Peça do Fabricante

### Envio internacional / alfândega

Necessário para envios internacionais (expanda a seção **Envio internacional / Alfândega**):

- **Código HS** — Código de classificação do Sistema Harmonizado
- **País de Origem** — Onde o produto é fabricado
- **Preço Unitário de Alfândega** — Valor declarado por unidade para alfândega
- **Número da Licença de Exportação** — Necessário somente para itens controlados ou restritos
- **Data de Validade da Licença de Exportação** — Data de expiração da licença de exportação

## SEO

Otimize a visibilidade do seu produto nos mecanismos de busca.

![aba SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Título Meta** — O título mostrado nos resultados dos mecanismos de busca. Clique no ícone do globo para traduzir.
- **Descrição Meta** — Uma breve descrição para os resultados da busca (máx. 160 caracteres). Clique no ícone do globo para traduzir.
- **Gerar automaticamente SEO** — Marque para gerar automaticamente o conteúdo SEO quando o produto for salvo.

Uma **Pré-visualização do Resultado de Pesquisa** ao vivo mostra exatamente como seu produto aparecerá nos resultados da busca do Google.

## Configurações da página do produto

Na aba **Avançado**, o cartão **Configurações da Página do Produto** permite que você controle como a página da loja deste produto parece:

- **Modelo da Página** — Substitua o layout padrão do site para esta página do produto: Clássico, Largura Total, Foco em Galeria, ou Digital. Deixe definido como **Usar Padrão do Site** para herdar qualquer layout que seus ajustes de design especificem — a maioria dos produtos deve ficar no padrão para que as alterações no modelo sejam aplicadas automaticamente.
- **Mostrar Produtos Relacionados** — Exibir produtos relacionados no final da página.
- **Mostrar Avaliações** — Exibir avaliações dos clientes.
- **Mostrar Especificações** — Exibir a aba de especificações.

O campo **Tipo de Galeria** — que controla como as imagens do produto são exibidas (Galeria Padrão, Carrossel, Layout de Grade, Galeria de Zoom, ou Visualização de 360°) — é definido separadamente, na aba **Mídia**.

## Canal de vendas

O campo **Canal de Vendas** (na seção Status) controla onde o produto pode ser vendido:

- **Todos os Canais** — Disponível online e na loja (Ponto de Venda).
- **Apenas Online** — Não disponível através dos terminais do Ponto de Venda.
- **Apenas na Loja** — Não listado online; disponível somente em sua loja física.

Um campo de **Código de Barras** também está disponível para varredura de código de barras do Ponto de Venda.

## Salvando seu produto

Quando estiver pronto, use os botões de salvar no canto superior direito. Seu produto ficará visível na loja assim que seu status for definido como **Publicado**.

## Dicas

Preserve todos os formatações de markdown, caminhos de imagens, blocos de código e termos técnicos.

- Comece com o status **Rascunho** para que você possa aprimorar o produto antes que os clientes o vejam.
- Faça o upload de várias imagens — produtos com várias fotos têm melhor conversão.
- Preencha os campos **SEO** para melhorar a visibilidade nos mecanismos de busca.
- Use **Categorias**, **Marcas** e **Tags** para ajudar os clientes a navegar pelo seu catálogo.
- Para produtos variáveis (por exemplo, tamanhos ou cores diferentes), escolha o tipo **Produto Variável** e adicione variantes após salvar.
- Use **Funcionalidades** e **Especificações** para adicionar dados estruturados do produto que serão exibidos em guias dedicados na página do produto.
- Se **Exige Envio** não permanecer marcado, verifique o **Tipo de Produto** — o Spwig desligaia o envio automaticamente para produtos Digitais, Reservas e Vales-presente, já que nenhum desses é fisicamente enviado.
- Defina um **Pacote de Envio Padrão** para produtos que sempre sejam enviados na mesma caixa — isso economiza você de ter que manter o peso e as dimensões desse produto em sincronia com a caixa que você realmente usa.
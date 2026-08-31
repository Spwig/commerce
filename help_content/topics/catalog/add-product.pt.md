---
title: Adicionando um Produto
---

Este guia o orienta na criação de um novo produto em sua loja. O formulário de produto é organizado em seções que abrangem informações básicas, mídia, preços, estoque, SEO e muito mais - para que você possa preencher tudo de uma vez ou voltar para completar as seções posteriormente.

## Começando

Navegue pelo menu lateral para **Produtos > Todos os Produtos** para ver seu catálogo de produtos. Clique no botão **+ Adicionar Produto** no canto superior direito para abrir o formulário de criação de produto.

![Página de lista de produtos](/static/core/admin/img/help/add-product/product-list-page.webp)

## Informações básicas

A seção **Informações Básicas** é onde você define a identidade central do seu produto.

![Formulário de adição de produto](/static/core/admin/img/help/add-product/add-product-form.webp)

### Campos obrigatórios

- **Nome** — O nome do produto exibido aos clientes. Clique no ícone do globo para adicionar traduções para outros idiomas.
- **Slug** — Versão amigável ao URL do nome (gerado automaticamente). Personalize-o se necessário.
- **SKU** — Seu código interno de unidade de estoque.
- **Tipo de Produto** — Escolha entre: Simples, Variável, Digital, Pacote, Voucher, Personalizável, Configurável ou Reserva.
- **Categoria** — Atribua o produto a uma categoria para organização e navegação na loja.

### Status e visibilidade

Encontrado na seção **Status** no final do formulário:

- **Status** — Defina como **Rascunho** enquanto estiver trabalhando, **Publicado** quando estiver pronto para venda, ou **Encerrado** para produtos que você não oferece mais.
- **Destacado** — Marque para destacar este produto em sua loja.
- **Produto Digital** — Marque se este produto incluir downloads digitais (arquivos, licenças). Pode ser combinado com qualquer tipo de produto.
- **Esconder da Loja** — Esconde o produto das listagens do catálogo, mantendo-o disponível como opção de configurador ou componente de pacote.

### Campos opcionais

- **Marca** — Associe a uma marca, se aplicável.
- **Tags** — Atribua uma ou mais tags na carta **Tags** mais abaixo neste painel. As tags são diferentes de Coleções - elas são rótulos rápidos e livres para organizar e filtrar produtos, em vez de agrupamento de merchandising. Comece a digitar para procurar uma tag existente, ou digite um novo nome para criá-la na hora. Veja o tópico de ajuda **Tags de Produto** para criar, renomear e excluir em massa tags diretamente.

![A carta de tags na aba Informações Básicas, com duas tags aplicadas no seletor de tags](/static/core/admin/img/help/add-product/tags-card.webp)

### Descrições do produto

- **Descrição Curta** — Apresenta-se em listagens e cartões de produtos. Mantenha-a curta e convincente.
- **Descrição Completa** — Descrição detalhada do produto exibida na página de detalhes do produto. Use o editor de texto rico para adicionar formatação, imagens, vídeos e tabelas.

Ambos os campos de descrição suportam o recurso de tradução — clique no ícone do globo para fornecer conteúdo em outros idiomas.

### Recursos e especificações

A seção **Detalhes do Produto** contém dois campos de dados estruturados:

- **Recursos** — Pares chave-valor para destaque do produto (ex.: "Tempo de Bateria: 20 horas").
- **Especificações** — Detalhes técnicos para a aba de especificações na página do produto (ex.: "Processador: Intel i7").

## Mídia

A seção **Mídia** permite que você gerencie imagens de produtos usando o Biblioteca de Mídia integrada.

![Aba de Mídia](/static/core/admin/img/help/add-product/media-tab.webp)

1. Clique em **+ Adicionar Imagens da Biblioteca de Mídia** para abrir o seletor de mídia.
2. Selecione imagens existentes ou faça upload de novas diretamente.
3. Arraste as imagens para reordená-las - a **primeira imagem** se torna a imagem principal do produto exibida nas listagens e cartões.

O campo **Tipo de Galeria**, na carta **Configurações da Galeria** abaixo da lista de imagens, controla como as imagens são exibidas na loja: Galeria Padrão, Carrossel, Layout de Grade, Galeria de Zoom ou Visualização de 360°.

## Preços

Defina o preço do seu produto e configure as vendas.

![Aba de Preços](/static/core/admin/img/help/add-product/pricing-tab.webp)

### Preço regular

- **Preço Regular** — O preço de varejo padrão que os clientes verão.

A moeda é definida junto com o valor da venda.
- **Custo** — Seu custo de mercadorias, usado para cálculos de lucro.

Isso nunca é mostrado aos clientes.

### Configurações de venda

Configure descontos temporários:

- **Tipo de venda** — Escolha entre: Nenhuma venda, Preço Fixo de Venda, Valor Fixo, ou Percentual de Desconto.
- **Valor da venda** — O valor do desconto ou percentual.
- **Data de início da venda / Data de término da venda** — Agende quando a venda será ativada e expirará. Deixe em branco para iniciar imediatamente ou sem data de término.

### Preços em múltiplas moedas

Se a múltipla moeda estiver habilitada na sua loja, um campo **Estratégia de Preços** aparece:

- **Preço Dinâmico** — Os preços em outras moedas são calculados automaticamente usando as taxas de câmbio configuradas.
- **Preço Fixo** — Defina um preço específico para cada moeda independentemente usando a seção **Preços em Múltiplas Moedas** que aparece abaixo.

## Estoque

Gerencie os níveis de estoque, comportamento de envio e atributos de produtos físicos.

![aba de estoque](/static/core/admin/img/help/add-product/inventory-tab.webp)

### Gerenciamento de estoque

- **Rastrear Estoque** — Ative para rastrear as quantidades de estoque (ativado por padrão).
- **Limite de Estoque Baixo** — Receba alertas quando o estoque cair abaixo desse número (padrão: 5).
- **Permitir Encomendas Adiantadas** — Ative para aceitar pedidos mesmo quando sem estoque. Novos produtos começam com o valor **Permitir Encomendas Adiantadas por Padrão** de **Configurações > Configurações da Loja > Comércio**, mas você pode substituí-lo por produto aqui a qualquer momento.
- **Ação quando sem estoque** — Substitua o comportamento do site ou da categoria quando este produto se esgotar: esconda-o, mostre-o como indisponível, mostre um botão "Notifique-me", ou permita encomendas adiantadas.

As quantidades de estoque são gerenciadas por armazém. Após salvar o produto, use a seção **Itens de Estoque** no final do formulário (ou navegue até **Produtos > Itens de Estoque**) para definir as quantidades em cada localização de armazém.

### Atributos físicos

Digite o peso do produto (kg) e as dimensões (comprimento, largura, altura em cm) para cálculos precisos de envio.

### Envio

- **Requer Envio** — Se este produto precisa ser entregue ao cliente. Ativado por padrão para produtos físicos; seu site de venda e checkout usam para decidir se coletam o endereço de envio e orçam o frete do pedido. O Spwig desligaá-lo automaticamente para produtos Digitais, de Reserva e de Voucher de Presente, pois esses nunca são enviados — você não precisa (e não pode) reativá-lo para esses tipos de produtos. Deixe marcado para um produto físico que pareça ter aparência digital, como um voucher impresso que seja enviado em uma caixa.
- **Pacote de Envio Preferido** — Escolha opcionalmente um dos seus pacotes de envio configurados. Quando definido, as dimensões próprias do pacote são usadas para cálculos de taxa de envio em vez do peso e das dimensões deste produto acima — útil quando um produto sempre é enviado na mesma caixa ou envelope padrão. Deixe em branco para usar as próprias características físicas do produto. Gerencie os pacotes disponíveis em **Envio > Pacotes**.

### Venda antecipada

Use o cartão **Venda Antecipada** para vender um produto antes de ter estoque — útil para lançamentos futuros que você deseja começar a receber pedidos antes do lançamento:

- **É Venda Antecipada** — Ative para permitir que os clientes comprem este produto mesmo enquanto está sem estoque.
- **Data de Lançamento da Venda Antecipada** — A data esperada de disponibilidade, mostrada aos clientes.
- **Mensagem de Venda Antecipada** — Uma mensagem curta personalizada mostrada aos clientes, com até 200 caracteres (ex.: "Envio em Março de 2026").

### Identificadores de produto

Códigos padrão de produtos para listagens de mercado e sistemas de estoque:

- **GTIN** — Número de Item de Comércio Global
- **EAN** — Número Europeu de Artigo
- **UPC** — Código Universal de Produto (EUA)
- **ISBN** — Para livros
- **ASIN** — Identificador da Amazon
- **MPN** — Número de Peça do Fabricante

### Envio internacional / alfândega

Necessário para envios internacionais (expanda a seção **Envio internacional / Alfândega**):

- **Código HS** — Código de classificação do Sistema Harmonizado
- **País de Origem** — Onde o produto é fabricado
- **Preço Unitário do Desembaraço** — Valor declarado por unidade para desembaraço
- **Número da Licença de Exportação** — Necessário apenas para itens controlados ou restritos
- **Data de Validade da Licença de Exportação** — Data de expiração da licença de exportação

## SEO

Otimize a visibilidade do seu produto nos mecanismos de busca.

![aba SEO](/static/core/admin/img/help/add-product/seo-tab.webp)

- **Título Meta** — O título exibido nos resultados dos mecanismos de busca. Clique no ícone do globo para traduzir.
- **Descrição Meta** — Uma breve descrição para os resultados da pesquisa (máximo de 160 caracteres). Clique no ícone do globo para traduzir.
- **Geração automática de SEO** — Marque para gerar automaticamente o conteúdo de SEO quando o produto for salvo.

Uma **Visualização do Resultado de Pesquisa** em tempo real mostra exatamente como seu produto aparecerá nos resultados de busca do Google.

## Configurações da página do produto

Na **aba Avançado**, o cartão **Configurações da Página do Produto** permite que você controle como a página da loja deste produto parece:

- **Modelo da Página** — Substitua o layout padrão do site para esta única página de produto: Clássico, Largura Total, Foco em Galeria ou Digital. Deixe definido como **Usar Padrão do Site** para herdar qualquer layout que as configurações de Design especificem — a maioria dos produtos deve permanecer no padrão para que as alterações no modelo sejam aplicadas automaticamente.
- **Mostrar Produtos Relacionados** — Exiba produtos relacionados na parte inferior da página.
- **Mostrar Avaliações** — Exiba avaliações dos clientes.
- **Mostrar Especificações** — Exiba a aba de especificações.

O campo **Tipo de Galeria** — que controla como as imagens do produto são exibidas (Galeria Padrão, Carrossel, Layout de Grade, Galeria de Zoom ou Visualização de 360°) — é definido separadamente, na **aba Mídia**.

![aba Avançado mostrando o cartão Configurações da Página do Produto com uma lista suspensa de Modelo da Página, e o cartão Detalhes Técnicos abaixo](/static/core/admin/img/help/add-product/advanced-tab.webp)

## Canal de Venda

O campo **Canal de Venda** (na seção Status) controla onde o produto pode ser vendido:

- **Todos os Canais** — Disponível online e na loja (Ponto de Venda).
- **Somente Online** — Não disponível por meio de terminais de Ponto de Venda.
- **Somente na Loja** — Não listado online; disponível apenas em sua loja física.

Um campo de **Código de Barras** também está disponível para varredura de código de barras do Ponto de Venda.

## Salvando seu produto

Quando estiver pronto, use os botões de salvar no canto superior direito. Seu produto ficará visível na loja assim que seu status for definido como **Publicado**.

## Dicas

- Comece com o status **Rascunho** para que você possa aperfeiçoar o produto antes que os clientes o vejam.
- Faça o upload de várias imagens — produtos com várias fotos têm melhor conversão.
- Preencha os campos de **SEO** para melhorar a descoberta nos mecanismos de busca.
- Use **Categorias**, **Marcas** e **Tags** para ajudar os clientes a navegar pelo seu catálogo.
- Para produtos variáveis (por exemplo, tamanhos ou cores diferentes), escolha o tipo **Produto Variável** e adicione variantes após salvar.
- Use **Funcionalidades** e **Especificações** para adicionar dados estruturados sobre o produto que são exibidos em guias dedicados na página do produto.
- Se **Requer Envio** não permanecer marcado, verifique o **Tipo de Produto** — o Spwig desligaará automaticamente o envio para produtos Digitais, de Reserva e de Voucher, já que nenhum desses é fisicamente enviado.
- Defina um **Pacote de Envio Padrão** para produtos que sempre sejam enviados na mesma caixa — isso economiza você de ter que manter o peso e as dimensões próprios do produto em sincronia com a caixa que você realmente usa.
---
title: Marcas de Produtos
---

Marcas permitem que você associe produtos ao seu fabricante ou rótulo e dê aos clientes uma forma de navegar em sua loja por marca. Cada marca tem sua própria página no seu site de vendas, onde os clientes podem descobrir todos os produtos dessa marca, ler a história da marca e seguir um link para o site da marca.

Navegue até **Catálogo > Marcas** para gerenciar suas marcas.

## Por que usar marcas

As marcas servem a dois propósitos no Spwig:

1. **Organização** — os produtos são marcados com uma marca, tornando fácil para clientes fiéis a uma determinada marca encontrarem o que procuram
2. **Merchandising** — as páginas de marca são um espaço dedicado para mostrar a história da marca, o logotipo e a gama completa de produtos, o que pode melhorar a conversão para compradores conscientes de marca

As marcas também funcionam com o sistema de promoções — você pode fazer uma venda que se aplique a todos os produtos de uma marca específica, sem precisar selecionar os produtos individualmente.

## Criando uma marca

1. Navegue até **Catálogo > Marcas**
2. Clique em **+ Adicionar Marca**
3. Preencha a seção **Informações Básicas**:
   - **Nome** — o nome da marca como será exibido no seu site de vendas (deve ser único)
   - **Slug** — o caminho da URL para a página da marca (preenchido automaticamente a partir do nome; você pode personalizá-lo)
   - **Descrição** — uma breve descrição da marca exibida na página da marca
   - **Website** — o URL do site oficial da marca (opcional — exibido como um link na página da marca)
4. Adicione ativos da marca:
   - **Logotipo** — a imagem do logotipo da marca, usada em listagens de marcas e na página da marca
   - **Imagem de Banner** — uma imagem de banner larga exibida no topo da página da marca
5. Escreva a **História da Marca** (opcional) — um artigo editorial mais longo sobre a história, valores ou o que torna a marca especial. Isso aparece na página da marca no site de vendas e pode ser uma forma eficaz de contar a história da marca aos clientes interessados.
6. Configure os campos **SEO**:
   - **Título Meta** — o título da página exibido nos resultados de busca
   - **Descrição Meta** — a breve descrição exibida abaixo do título nos resultados de busca
7. Defina as opções de exibição:
   - **Exibir Página da Marca** — controla se a marca tem uma página acessível publicamente. Desmarque para ocultar uma marca do site de vendas, mantendo-a no sistema.
   - **Ativo** — controla se a marca está disponível para ser atribuída a produtos e visível na loja
   - **Destacado** — marca a marca para exibição destacada no seu tema (ex: uma linha de logotipos de marcas na página inicial)
8. Clique em **Salvar**

## Atribuindo produtos a uma marca

As marcas são atribuídas em registros de produtos individuais, e não a partir da página de gerenciamento de marcas. Para atribuir uma marca a um produto:

1. Navegue até **Catálogo > Produtos** e abra o produto
2. No formulário do produto, localize o campo **Marca**
3. Procure e selecione a marca apropriada
4. Salve o produto

Uma vez que uma marca é atribuída, o produto aparecerá automaticamente na página de vendas daquela marca.

## Páginas de marca no seu site de vendas

Cada marca com **Exibir Página da Marca** ativado tem sua própria página em `/brand/{slug}/`. A página exibe:

- O logotipo da marca e a imagem de banner
- O nome da marca e a descrição
- A história da marca (se fornecida)
- Um link para o site da marca (se fornecido)
- Todos os produtos ativos atribuídos a essa marca

Os clientes podem acessar as páginas de marca clicando no nome da marca em uma página de produto, ou por meio de links que você criar em sua navegação ou construtor de páginas.

## SEO para páginas de marca

Preencher os campos **Título Meta** e **Descrição Meta** para cada marca ajuda as páginas de marca a aparecerem bem nos resultados de busca. Títulos de SEO eficazes para marcas geralmente combinam o nome da marca com o que a marca vende:

| Marca | Bom Título Meta |
|---|---|
| Levi's | "Levi's Jeans & Clothing — Official Store" |
| KitchenAid | "KitchenAid Stand Mixers & Kitchen Appliances" |
| Patagonia | "Patagonia Outdoor Clothing & Gear" |

Se você deixar os campos de SEO em branco, seu tema voltará ao nome da marca.

### Geração automática de SEO

Se **SEO Auto Gerado** estiver ativado em uma marca, o Spwig gerará automaticamente o título e a descrição meta quando a marca for salva.

Isso é conveniente para lojas com muitas marcas, mas oferece menos controle sobre a redação exata.

Você sempre pode substituir o conteúdo gerado digitando diretamente nos campos e desativando o botão de geração automática.

## Marcas em destaque

A bandeira **Is Featured** é usada pelos temas para exibir uma linha ou grade curada de logotipos de marcas — comumente na página inicial. Apenas um pequeno número de marcas deve ser destacado de cada vez; consulte a documentação do seu tema para entender quantas marcas em destaque exibem de forma otimizada.

## Dicas

- Faça o upload de um logotipo de marca como PNG ou WebP com fundo transparente — ele será exibido limpo em qualquer cor de fundo no seu tema
- Escreva uma história de marca envolvente, mesmo para marcas menos conhecidas; clientes que não estão familiarizados com uma marca apreciam o contexto que os ajuda a decidir se os produtos são adequados para eles
- Se você executar promoções direcionadas a marcas específicas, certifique-se de que o nome da marca no Spwig corresponda exatamente — as promoções usam a relação de marca nos produtos para determinar a elegibilidade
- Desative uma marca em vez de excluí-la quando parar de carregá-la — a exclusão remove a referência da marca de todos os produtos associados, enquanto a desativação preserva o histórico
- Use a bandeira **Is Featured** com moderação; uma página inicial mostrando 20 logotipos de marcas perde impacto em comparação com 6–8 escolhidos com cuidado
---
title: Elementos Personalizados
---

Elementos personalizados permitem que você crie blocos reutilizáveis do construtor de páginas que atendem às necessidades do seu loja. Você projeta visualmente um elemento usando as ferramentas existentes do construtor de páginas, e depois, opcionalmente, conecta-o a dados reais da loja — como nomes de produtos, preços ou imagens — para que o elemento seja preenchido automaticamente com conteúdo real quando colocado em uma página. Uma vez criado, seus elementos personalizados aparecem na biblioteca de elementos do construtor de páginas, junto com os blocos integrados.

![Biblioteca de Elementos Personalizados](/static/core/admin/img/help/custom-elements/custom-elements-list.webp)

## Quando usar elementos personalizados

Elementos personalizados são mais valiosos quando você se encontrar criando a mesma layout repetidamente. Em vez de reconstruir uma "carta de produto em destaque" do zero em cada página, você cria-a uma vez como um elemento personalizado e coloca-a onde quiser. Se o elemento estiver vinculado a dados, ele puxa automaticamente as informações atuais do produto — nenhuma atualização manual é necessária quando os preços ou nomes mudam.

Usos comuns:

- Cartões de destaque de produto que mostram nome, preço e imagem principal
- Blocos de promoção de categoria com banner, título e link
- Painéis de apresentação de marca com logotipo e descrição
- Resumos de postagens de blog com imagem em destaque, título e resumo

## Criando um novo elemento personalizado

1. Navegue até **Design > Elementos Personalizados**
2. Clique em **+ Adicionar Elemento Personalizado**
3. O Spwig cria imediatamente um rascunho do elemento e abre o **Construtor Visual** — você não precisa preencher um formulário primeiro
4. No Construtor Visual, crie o layout do seu elemento usando as ferramentas do construtor de páginas disponíveis
5. Quando estiver satisfeito com o design, configure as configurações do elemento (nome, vinculação de dados, ícone) no painel lateral
6. Ative **Ativo** quando estiver pronto para publicar o elemento na biblioteca
7. Salve o elemento

O elemento agora está disponível no painel de elementos do construtor de páginas sob a categoria que você atribuiu.

## O construtor visual

O Construtor Visual é um canvas dedicado para projetar seu elemento. Ele funciona como o construtor de páginas padrão, mas se concentra em um único elemento em vez de uma página inteira. Você pode:

- Adicionar e organizar elementos filhos (blocos de texto, imagens, contêineres, etc.)
- Definir estilização, espaçamento e layout para cada elemento filho
- Visualizar como o elemento será exibido com dados de amostra

As alterações no Construtor Visual são salvas diretamente na definição do elemento. Não há etapa de publicação separada — salvar no construtor atualiza o elemento imediatamente para qualquer página que já o use.

## Configurando as configurações do elemento

Cada elemento personalizado tem estas configurações:

| Campo | Descrição |
|-------|-------------|
| **Nome** | Nome de exibição mostrado na biblioteca de elementos |
| **Slug** | Identificador seguro para URL, gerado automaticamente a partir do nome |
| **Descrição** | Nota opcional sobre o que este elemento é usado |
| **Modelo Alvo** | O modelo de loja para vincular dados (veja abaixo) |
| **Ícone** | Ícone mostrado na biblioteca de elementos |
| **Categoria** | Agrupa elementos relacionados juntos na biblioteca |
| **Ativo** | Se o elemento está disponível no construtor de páginas |

## Vinculação de dados

A vinculação de dados conecta partes do layout do seu elemento a dados reais da loja. Quando um editor de página coloca um elemento vinculado a dados em uma página, eles selecionam um registro específico (por exemplo, um produto), e todos os campos vinculados são preenchidos automaticamente com esse registro.

### Escolhendo um modelo alvo

A configuração **Modelo Alvo** determina qual tipo de dados da loja o elemento pode exibir. Os modelos disponíveis são:

| Modelo | O que ele fornece |
|-------|-----------------|
| **Produto** | Nome, preço, status de estoque, imagens, descrição, SKU, categoria, marca e muito mais |
| **Categoria** | Nome, descrição, imagem, banner, contagem de produtos e URL |
| **Marca** | Nome, logotipo, descrição, história da marca e URL |
| **Postagem de Blog** | Título, resumo, imagem em destaque, autor, data de publicação e URL |

Deixe **Modelo Alvo** vazio para criar um elemento estático sem dados dinâmicos. Elementos estáticos são úteis para componentes de design fixos, como banners decorativos ou espaçadores de layout.

### Como as vinculações funcionam

Dentro do Visual Builder, você pode marcar elementos filhos individuais como vinculados a dados selecionando o campo do modelo que eles devem exibir.

Por exemplo:
- Um elemento filho **texto** pode ser vinculado a **Product Name**, para mostrar o nome do produto selecionado
- Um elemento filho **imagem** pode ser vinculado a **Main Image**, para mostrar a foto principal do produto
- Um elemento filho **texto** pode ser vinculado a **Price**, para sempre refletir o preço atual

Cada vinculação mapeia um campo de conteúdo de um elemento para um campo do modelo. Você pode adicionar múltiplas vinculações a um único elemento personalizado — por exemplo, vincular um bloco de texto a **Product Name** e um bloco de imagem separado a **Main Image** ao mesmo tempo.

### Preset de miniaturas de imagem

Para vinculações de imagem, você pode opcionalmente especificar um **Preset de Miniatura** (como `thumbnail` ou `medium`). Isso controla o tamanho da imagem que é carregada, ajudando as páginas a carregarem mais rapidamente ao servir a imagem com o tamanho apropriado para o layout do elemento.

## Desativando e reativando elementos

Desativar um elemento o remove da biblioteca de elementos, então ele não pode ser adicionado a novas páginas. Páginas existentes que já usam o elemento não são afetadas — o elemento continua sendo renderizado nessas páginas.

Para desativar:
1. Navegue até **Design > Custom Elements**
2. Clique no nome do elemento
3. Desmarque **Active**
4. Salve

Para reativar, siga os mesmos passos e marque **Active** novamente.

## Filtrando a biblioteca de elementos

A lista de elementos suporta filtragem por:
- **Ativo / Inativo** — mostrar apenas elementos publicados ou apenas rascunhos
- **Modelo Alvo** — filtrar por modelo ao qual o elemento está vinculado
- **Categoria** — filtrar por categoria do elemento
- **Pesquisa** — pesquisar por nome, slug ou descrição

Isso ajuda quando você tem muitos elementos personalizados e precisa encontrar um específico rapidamente.

## Exemplo: cartão de destaque de produto

**Objetivo:** Um elemento de cartão que mostra a imagem principal, o nome e o preço de um produto.

| Configuração | Valor |
|---------|-------|
| Nome | Product Highlight Card |
| Modelo Alvo | Product |
| Categoria | Products |
| Ícone | fas fa-box |

No Visual Builder, adicione:
- Um elemento **Imagem** vinculado a **Main Image** com o preset de miniatura `medium`
- Um elemento **Texto** vinculado a **Product Name**
- Um elemento **Texto** vinculado a **Price**

Após salvar e ativar, o elemento aparece no construtor de páginas na categoria Products. Quando um editor de página o adiciona a uma página, ele seleciona qual produto destacar, e o cartão se preenche automaticamente.

## Dicas

- Dê a elementos nomes descritivos que incluam seu propósito e o tipo de dados — por exemplo, "Product Highlight Card" em vez de "Card 1" — para que a biblioteca continue fácil de navegar conforme cresce
- Use o campo **Categoria** para agrupar elementos relacionados (Products, Blog, Promotions) — isso mantém a biblioteca de elementos organizada para seus editores de página
- Teste elementos vinculados a dados adicionando-os a uma página em rascunho e selecionando um registro real antes de publicar, para confirmar que a vinculação está puxando as informações corretas
- Desative elementos obsoletos em vez de excluí-los — isso preserva quaisquer páginas que ainda os referenciem e lhe dá a opção de reativá-los mais tarde
- Elementos estáticos (sem modelo alvo) são ideais para padrões de layout que você reutiliza em todo o site, como divisórias, painéis de CTA ou espaçadores de marca
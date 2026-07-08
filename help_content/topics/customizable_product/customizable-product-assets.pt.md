---
title: Clipart e Fontes para Produtos Personalizáveis
---

O editor de design vem com dois tipos de ativos criativos que você pode fornecer aos clientes: **clipart** (gráficos prontos que eles podem adicionar aos seus designs) e **fontes personalizadas** (além das fontes padrão do sistema). Construir uma biblioteca bem selecionada de ativos torna o editor mais útil e ajuda os clientes a criar designs melhores com mais rapidez.

## Biblioteca de Clipart

O clipart fornece aos clientes uma biblioteca de gráficos prontos que podem ser adicionados aos seus designs com um único clique. Em vez de exigir que os clientes procurem e carreguem suas próprias imagens para elementos comuns, como ícones, bordas ou gráficos decorativos, você os fornece prontos para uso.

### Criando categorias de clipart

O clipart é organizado em categorias que os clientes podem navegar. As categorias ajudam os clientes a encontrar o que precisam rapidamente.

1. Navegue até **Produtos Personalizáveis > Categorias de Clipart**
2. Clique em **+ Adicionar Categoria de Clipart**
3. Preencha:
   - **Nome da Categoria** — O que os clientes veem (ex: "Esportes", "Bordas", "Feriados")
   - **Slug** — Gerado automaticamente a partir do nome
   - **Ícone** — Uma classe de ícone Font Awesome para a guia da categoria (ex: `fas fa-football-ball`)
   - **Ordem de Classificação** — Controla a ordem em que as categorias aparecem no editor
4. Clique em **Salvar**

**Exemplos de categorias para uma loja de camisetas:**

| Categoria | Ícone | Exemplo de clipart |
|----------|------|-----------------|
| Esportes | `fas fa-football-ball` | Logos de times, equipamentos esportivos, símbolos esportivos |
| Humor | `fas fa-laugh` | Memes, frases engraçadas, personagens de desenho animado |
| Natureza | `fas fa-leaf` | Animais, flores, paisagens |
| Geométrico | `fas fa-shapes` | Padrões, formas abstratas, designs tribais |

**Exemplos de categorias para uma loja de impressão/posters:**

| Categoria | Ícone | Exemplo de clipart |
|----------|------|-----------------|
| Bordas | `fas fa-border-all` | Molduras decorativas, ornamentos de cantos |
| Sazonal | `fas fa-snowflake` | Ícones de feriados, motivos sazonais |
| Ícones | `fas fa-icons` | Estrelas, corações, setas, marcas de verificação |
| Fundos | `fas fa-image` | Texturas, gradientes, padrões |

### Adicionando ativos de clipart

Cada ativo de clipart é um arquivo de imagem (PNG ou SVG) que os clientes podem colocar em seu canvas.

1. Navegue até **Produtos Personalizáveis > Ativos de Clipart**
2. Clique em **+ Adicionar Ativo de Clipart**
3. Preencha:
   - **Nome** — Nome descritivo (ex: "Estrela Dourada", "Capacete de Futebol")
   - **Categoria** — Selecione de suas categorias de clipart
   - **Ativo de Imagem** — Clique para abrir a Biblioteca de Mídia e selecionar ou carregar o arquivo de imagem
   - **Escopo** — Escolha a disponibilidade (veja abaixo)
   - **Tags** — Palavras-chave pesquisáveis para este clipart (ex: `['estrela', 'dourado', 'decoração']`)
   - **Ordem de Classificação** — Controla a posição dentro da categoria
4. Clique em **Salvar**

### Entendendo o escopo do clipart

Cada ativo de clipart tem um escopo que controla onde ele está disponível:

| Escopo | Descrição | Caso de uso |
|-------|-------------|----------|
| **Disponível para Todos os Produtos** | Aparece no navegador de clipart para cada produto personalizável | Gráficos de uso geral, como estrelas, bordas e ícones comuns |
| **Somente para um Produto Específico** | Aparece apenas para um produto selecionado | Gráficos específicos de produto, como logotipos de marca ou arte temática do produto |

Para a maioria dos ativos, use **Disponível para Todos os Produtos**. Reserve o escopo específico do produto para ativos que só fazem sentido no contexto de um único produto — por exemplo, logotipos específicos de times para um produto de merchandising de time.

### Diretrizes para arquivos de clipart

- **Formato:** Use PNG para gráficos raster e SVG para gráficos vetoriais. Os arquivos SVG se escalam sem perda de qualidade, tornando-os ideais para clipart que os clientes possam redimensionar significativamente
- **Resolução:** Os arquivos PNG devem ter pelo menos 500x500 pixels para boa qualidade de impressão
- **Fundo:** Use fundos transparentes (PNG com canal alfa ou SVG) para que o clipart se funda naturalmente ao design
- **Tamanho do arquivo:** Mantenha os arquivos de clipart individuais abaixo de 500KB para carregamento rápido no editor

## Fontes personalizadas

Fontes personalizadas estendem o seletor de fontes no editor de design além das fontes padrão do sistema.

Isso permite que você ofereça tipografia curada que combina com sua marca ou estilo de produto.

### Adicionando uma fonte personalizada

1. Navegue até **Produtos Personalizáveis > Fontes Personalizadas**
2. Clique em **+ Adicionar Fonte Personalizada**
3. Preencha:
   - **Nome da Fonte** — Nome de exibição mostrado no seletor de fontes (ex.: "Playfair Display")
   - **Família da Fonte** — Nome da font-family CSS usado internamente (ex.: `PlayfairDisplay`)
   - **Regular** — Clique para carregar o arquivo da fonte de peso regular (WOFF2 ou TTF) via Biblioteca de Mídia
   - **Negrito** — Variante opcional de peso negrito
   - **Itálico** — Variante opcional itálica
   - **Negrito Itálico** — Variante opcional negrito itálica
4. Clique em **Salvar**

O peso **Regular** é obrigatório para fontes personalizadas. As variantes negrito, itálico e negrito itálico são opcionais — se não forem fornecidas, o navegador tentará sintetizar esses estilos a partir da fonte regular, embora os resultados possam não parecer tão refinados quanto arquivos de fonte dedicados.

### Fontes do sistema vs. fontes personalizadas

Você também pode registrar fontes do sistema que estão pré-instaladas na maioria dos dispositivos:

1. Adicione uma nova entrada de fonte personalizada
2. Marque **Fonte do Sistema**
3. Insira o nome da família da fonte exatamente como aparece no CSS (ex.: `Georgia`, `Courier New`)
4. Não é necessário carregar nenhum arquivo para fontes do sistema

As fontes do sistema carregam instantaneamente, pois já estão no dispositivo do cliente. As fontes carregadas personalizadas precisam ser baixadas primeiro, o que adiciona um pequeno atraso quando a fonte é selecionada pela primeira vez.

### Recomendações de fontes por tipo de produto

**Para camisetas e roupas de vestir:**
- Fontes ousadas e impactantes funcionam melhor: Impact, Anton, Bebas Neue, Oswald
- Letras em bloco e fontes sans-serif são mais legíveis em tecido
- Evite fontes finas ou delicadas que podem não imprimir bem em superfícies texturizadas

**Para pôsteres e produtos de impressão:**
- Fontes serif elegantes para designs formais: Playfair Display, Merriweather, Lora
- Fontes de escrita para convites e cartões: Great Vibes, Dancing Script, Pacifico
- Sans-serif limpos para designs modernos: Montserrat, Raleway, Open Sans

### Formatos de arquivos de fonte

| Formato | Extensão | Recomendação |
|--------|-----------|----------------|
| WOFF2 | `.woff2` | Preferido — menor tamanho de arquivo, carregamento mais rápido |
| TrueType | `.ttf` | Boa alternativa — amplamente compatível |

Os arquivos WOFF2 são normalmente 30-50% menores que os arquivos TTF, então carregam mais rápido no editor do cliente. Use WOFF2 quando disponível.

## Gerenciando sua biblioteca de ativos

### Organizando para os clientes

A ordem em que os ativos aparecem no editor é controlada pelo campo **Ordem de Classificação** em categorias e ativos individuais. Números mais baixos aparecem primeiro. Use isso para:

- Colocar as categorias de clipart mais populares primeiro
- Colocar os cliparts mais versáteis e de alta qualidade no topo de cada categoria
- Ordenar as fontes com as opções mais usadas primeiro

### Mantendo a biblioteca atualizada

- Adicione clipart sazonal antes de feriados (Halloween, Natal, Dia dos Namorados) e desative-os depois
- Use a caixa de seleção **Ativo** para ocultar temporariamente ativos sem excluí-los
- Monitore quais cliparts e fontes os clientes usam mais e expanda essas categorias

## Dicas

- Comece pequeno — 20-30 cliparts de alta qualidade distribuídos entre 3-4 categorias são melhores que centenas de opções medíocres. Você sempre pode adicionar mais conforme aprender o que os clientes desejam.
- Use o formato SVG para clipart sempre que possível. Os arquivos SVG são menores, escalam perfeitamente para qualquer tamanho e produzem impressões mais nítidas do que imagens raster.
- Teste cada fonte carregada no editor de design para garantir que todos os caracteres sejam renderizados corretamente, especialmente caracteres especiais e acentos, se os clientes usarem múltiplos idiomas.
- Etique os cliparts de forma abrangente — os clientes pesquisam por palavras-chave, então etiquetas descritivas como "dourado", "estrela", "de 5 pontas", "decoração" ajudam a encontrar o ativo certo rapidamente.
- Agrupe cliparts relacionados na mesma categoria. Se você vende mercadorias de equipe, crie uma categoria por esporte em vez de uma única categoria grande chamada "Esportes".
- Revise regularmente sua biblioteca de clipart do ponto de vista do cliente visitando o editor de design no site da loja.
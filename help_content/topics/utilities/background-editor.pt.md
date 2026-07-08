---
title: Editor de Fundo
---

O editor de fundo oferece a você controle total sobre os fundos dos elementos, com quatro tipos: cor sólida, gradiente, imagem e vídeo. Ele também suporta estados separados de **Normal** e **Hover**, para que você possa criar efeitos visuais interativos. Abra a **aba Estilo** de qualquer elemento e procure a seção **Fundo** para acessar o editor.

![Editor de Fundo](/static/core/admin/img/help/background-editor/background-editor.webp)

## Estados Normal e Hover

No topo do editor de fundo, um botão alternador comuta entre os estados **Normal** e **Hover**. Cada estado tem sua própria configuração de fundo independente:

- **Normal** — O fundo padrão exibido quando a página carrega
- **Hover** — O fundo aplicado quando um visitante mover o cursor sobre o elemento

Dois pequenos blocos de pré-visualização ao lado do botão mostram os fundos Normal e Hover lado a lado, para que você possa ver o contraste de uma olhada. Configure o estado Normal primeiro, depois comute para Hover para adicionar um efeito interativo, se desejado.

## Tipos de Fundo

Selecione um tipo de fundo a partir da linha de ícones no topo do painel do editor:

| Tipo | Descrição |
|------|-------------|
| **Cor** | Preenchimento sólido usando um único valor de cor. Fácil de aplicar e leve. |
| **Gradiente** | Uma transição suave entre duas ou mais cores, seja linear ou radial. Inclui pré-definições embutidas como Oceano, Pôr do Sol, Floresta e Framboesa. Para edição avançada de gradientes, consulte o tópico [Criador de Gradiente](gradient-creator). |
| **Imagem** | Uma imagem carregada ou uma selecionada da biblioteca de mídia. Suporta posicionamento, dimensionamento e controle de repetição. |
| **Vídeo** | Um URL de vídeo de fundo com uma imagem de capa opcional que é exibida enquanto o vídeo carrega ou em dispositivos móveis. |

Apenas um tipo pode estar ativo de cada vez por estado. Alternar entre os tipos não apaga sua configuração anterior — você pode voltar e suas configurações serão preservadas.

## Fundos de Cor

Quando **Cor** é selecionada:

- **Entrada de Hex** — Digite um código hexadecimal diretamente (ex.: `#1A1A2E`)
- **Amostras de Cor** — Clique em uma amostra pré-definida para seleção rápida. As amostras são conscientes do tema e refletem a paleta do tema ativo.
- **Botão Editar** — Abre o seletor de cor completo com espectro, barras de rolagem e opções de formato (consulte o tópico [Seletor de Cor](color-picker))

Fundos de cor são renderizados instantaneamente e não têm impacto no desempenho, tornando-os ideais para seções, cartões e contêineres.

## Fundos de Gradiente

Quando **Gradiente** é selecionado:

- **Gradientes Pré-definidos** — Escolha entre gradientes embutidos: Oceano, Pôr do Sol, Floresta, Framboesa e outros
- **Gradiente Personalizado** — Clique em **Editar** para abrir o criador de gradientes, onde você pode definir a direção, o tipo (linear ou radial) e os pontos de cor
- **Barra de Direção** — Ajuste a direção do gradiente para gradientes lineares (0-360 graus)

Os gradientes adicionam profundidade visual sem exigir ativos de imagem e se ajustam perfeitamente a qualquer tamanho de tela.

## Fundos de Imagem

Quando **Imagem** é selecionada:

- **Carregar ou Biblioteca de Mídia** — Clique no espaço reservado da imagem para carregar uma nova imagem ou selecionar uma da sua biblioteca de mídia
- **Tamanho** — Escolha **Cobrir** (preenche o elemento, pode cortar), **Conter** (se encaixa dentro do elemento) ou um tamanho personalizado
- **Posição** — Defina o ponto focal usando uma grade de 9 pontos (canto superior esquerdo, centro, canto inferior direito, etc.) ou insira porcentagens personalizadas de X/Y
- **Repetir** — Ative ou desative a repetição. Útil para padrões de tijolos
- **Sobreposição** — Adicione uma sobreposição de cor sobre a imagem com opacidade ajustável, útil para garantir a legibilidade do texto

Sempre otimize as imagens antes de carregá-las. Imagens grandes e não comprimidas atrasam o tempo de carregamento da página.

## Fundos de Vídeo

Quando **Vídeo** é selecionado:

- **URL do Vídeo** — Insira um URL direto para um arquivo de vídeo MP4 ou WebM
- **Imagem de Capa** — Carregue uma imagem de fallback exibida enquanto o vídeo carrega e em dispositivos que não reproduzem vídeo automaticamente
- **Reprodução Automática / Repetição / Mudo** — Fundos de vídeo reproduzem automaticamente, repetem e são mutados por padrão para cumprir as políticas do navegador

Mantenha os vídeos de fundo curtos (10-30 segundos), comprimidos e visualmente sutis.

Eles devem melhorar a seção sem distrair do conteúdo.

## Onde aparece

O editor de fundo está disponível para cada elemento que suporta fundos:

- **Page Builder** — Seções, contêineres, colunas e elementos individuais têm uma seção de Fundo na guia Estilo
- **Header/Footer Builder** — Fundos de linha e fundos de widgets individuais
- **Menu Builder** — Fundos do contêiner do menu e painel de dropdown

A mesma interface do editor é usada em todos os lugares, então seu fluxo de trabalho permanece consistente entre os construtores.

## Dicas

- Use uma camada de cor semi-transparente em fundos de imagem para garantir que o texto permaneça legível, independentemente do conteúdo da imagem.
- Preset de gradientes são uma forma rápida de adicionar interesse visual — aplique um, depois personalize o ângulo ou as cores para combinar com sua marca.
- Defina fundos Normal e Hover em cartões interativos para dar aos visitantes feedback visual claro quando explorarem seu conteúdo.
- Para fundos de imagem, sempre defina um ponto focal para que a parte mais importante da imagem permaneça visível em todos os tamanhos de tela.
- Prefira fundos de cor ou gradientes em vez de imagens para seções onde a velocidade de carregamento é crítica, como conteúdo acima da pasta.
- Teste fundos de vídeo em dispositivos móveis — a maioria dos navegadores móveis mostrará a imagem de capa em vez de reproduzir o vídeo.
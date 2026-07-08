---
title: Criador de Gradientes
---

O Criador de Gradientes permite que você crie transições suaves de cores para fundos de elementos. Ele é acessado através da aba Gradient (Gradiente) do Editor de Fundo e abre como um painel flutuante com uma barra visual de gradiente, controles de parada de cor e opções de pré-definições.

![Criador de Gradientes](/static/core/admin/img/help/gradient-creator/gradient-creator.webp)

## Acessando o Criador de Gradientes

1. Selecione um elemento no Page Builder ou no Header/Footer Builder
2. Abra a aba **Style** (Estilo) no painel de propriedades
3. Clique na seção **Background** (Fundo) para abrir o Editor de Fundo
4. Mude para a aba **Gradient** (Gradiente)
5. O painel do Criador de Gradientes abre com uma pré-visualização em tempo real e controles de edição

## Pré-visualização em Tempo Real

A parte superior do painel mostra uma comparação lado a lado:

| Box | Purpose |
|-----|---------|
| **Current** | O gradiente existente (ou transparente se nenhum for definido) |
| **New** | Atualizações em tempo real conforme você faz alterações |

Uma seta entre os dois boxes indica a direção da mudança.

## Tipos de Gradiente

Três tipos de gradiente estão disponíveis, selecionáveis por meio de abas no topo do editor:

| Tipo | Descrição | Controles |
|------|-------------|----------|
| **Linear** | Transições de cor ao longo de uma linha reta | Controlador de ângulo (0-360 graus) com botões de direção pré-definidos (para cima, diagonal, para a direita, para baixo, etc.) |
| **Radial** | Transições de cor irradiando a partir de um ponto central | Seletor de forma (círculo ou elipse) e seletor de posição (centro, topo, fundo, cantos) |
| **Conic** | Transições de cor girando em torno de um ponto central | Controlador de ângulo inicial (0-360 graus) e seletor de posição |

### Controles de Direção Linear

Para gradientes lineares, você pode definir o ângulo de três maneiras:
- **Controlador de ângulo** — arraste de 0 a 360 graus
- **Campo de entrada de ângulo** — digite um valor preciso em graus
- **Botões de pré-definição** — clique nos ícones de seta para direções comuns (para cima, para cima-direita, para a direita, para baixo-direita, para baixo, para baixo-esquerda, para a esquerda, para cima-esquerda)

## Paradas de Cor

A barra de gradiente mostra suas paradas de cor atuais como marcadores arrastáveis. Cada parada define uma cor em uma posição específica ao longo do gradiente.

**Adicionar paradas** — Clique no botão **+** na seção Color Stops (Paradas de Cor) para adicionar uma nova parada. Não há limite rígido no número de paradas.

**Editar paradas** — Cada parada na lista mostra:
- Uma amostra de cor que abre o Color Picker (Seletor de Cor) ao ser clicada
- Um valor de posição (0% a 100%) que você pode digitar ou ajustar
- Um controle de opacidade (0 a 1)
- Um botão de exclusão para remover a parada

**Reordenar** — Arraste as paradas ao longo da barra de gradiente para repositioná-las visualmente.

## Pré-definições de Gradiente

Seis pré-definições embutidas estão disponíveis para pontos de início rápidos. Clique em qualquer pré-definição para aplicá-la imediatamente:

| Pré-definição | Cores | Ângulo |
|--------|--------|-------|
| **Ocean** | Azul claro para azul | 120 graus |
| **Sunset** | Laranja quente para rosa coral (3 paradas) | 45 graus |
| **Forest** | Índigo para verde esmeralda | 135 graus |
| **Berry** | Rosa para roxo-azul | 90 graus |
| **Flame** | Vermelho para amarelo dourado | 45 graus |
| **Night** | Pedra escura para azul oceânico | 180 graus |

As pré-definições são pontos de início. Após aplicar uma, você pode modificar as cores, adicionar ou remover paradas e alterar o ângulo para criar sua própria variação.

## Ações do Rodapé

| Botão | Ação |
|--------|--------|
| **Clear** | Remove o gradiente completamente, resetando para transparente |
| **Apply** | Salva o gradiente e fecha o editor |

Fechar o editor sem clicar em Apply descarta suas alterações.

## Onde Ele Aparece

O Criador de Gradientes é usado em:

- **Page Builder** — via a aba Gradient (Gradiente) do Editor de Fundo em qualquer elemento
- **Header/Footer Builder** — para fundos de gradiente em seções de cabeçalho, barras de navegação e áreas de rodapé

Ele funciona junto com o Editor de Fundo, que também oferece opções de fundo em cor sólida, imagem e vídeo.

## Dicas

- **Comece com uma pré-definição** — aplique uma pré-definição que esteja próxima do que você deseja, depois ajuste as cores e o ângulo em vez de construir do zero.
- **Use duas ou três paradas** — gradientes simples com duas paradas parecem limpos e profissionais. Mais paradas são úteis para efeitos complexos, mas podem rapidamente se tornar abrumadores.
- **Use as cores da sua marca** — use o Color Picker (Seletor de Cor) para inserir valores exatos de hexadecimais da paleta da sua marca para gradientes consistentes e alinhados com a sua marca.
- **Teste com conteúdo** — gradientes que parecem impressionantes sozinhos podem reduzir a legibilidade do texto. Sempre verifique se o texto sobre fundos de gradiente tem contraste suficiente.
- **Tente radial para efeitos de luz** — gradientes radiais funcionam bem para chamar atenção para uma área central, como um ponto focal de uma seção hero.

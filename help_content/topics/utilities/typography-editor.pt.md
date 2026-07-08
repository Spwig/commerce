---
title: Editor de Tipografia
---

O Editor de Tipografia é uma ferramenta de estilo compartilhada que lhe dá controle total sobre a aparência do texto. Ele abre como um painel flutuante sempre que você editar propriedades de tipografia em qualquer elemento no Page Builder, Header/Footer Builder ou Menu Builder.

![Editor de Tipografia](/static/core/admin/img/help/typography-editor/typography-editor.webp)

## Pré-visualização em Tempo Real

O editor mostra uma comparação lado a lado no topo do painel:

| Caixa | Propósito |
|-----|---------|
| **Atual** | Exibe "The quick brown fox..." no estilo de tipografia existente |
| **Nova** | Atualiza em tempo real conforme você ajusta as configurações, mostrando o resultado antes de aplicar |

Isso permite que você compare antes e depois sem comprometer nenhuma alteração.

## Aba Fonte

A aba Fonte é a visão padrão quando o editor é aberto.

**Família de Fonte** — Um menu suspenso pesquisável com mais de 70 fontes organizadas por categoria. Cada fonte é pré-visualizada em seu próprio tipo para que você possa ver como ela parece antes de selecionar. As fontes são carregadas sob demanda do Google Fonts quando necessário.

**Tamanho da Fonte** — Entrada numérica com um seletor de unidade que suporta px, em, rem e %. O padrão é 16px.

**Peso da Fonte** — Um controle deslizante de 100 (Fino) a 900 (Negrito):

| Valor | Nome |
|-------|------|
| 100 | Fino |
| 200 | Extra Light |
| 300 | Light |
| 400 | Regular |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

Não todas as fontes suportam todos os nove pesos. O editor mostra quais pesos estão disponíveis para a família de fonte selecionada.

**Estilo da Fonte** — Botões de alternância para Normal, Itálico e Oblíquo.

## Aba Espaçamento

Ajuste finamente o espaço ao redor e entre os caracteres:

| Controle | O Que Ele Faz | Padrão |
|---------|-------------|---------|
| **Altura da Linha** | Espaço vertical entre as linhas de texto | normal |
| **Espaçamento entre Letras** | Espaço horizontal entre caracteres individuais | normal |
| **Espaçamento entre Palavras** | Espaço horizontal entre palavras | normal |
| **Recuo do Texto** | Recuo da primeira linha em um parágrafo | 0 |

Cada controle de espaçamento inclui um seletor de unidade (px, em, rem, %).

## Aba Estilo

Controle decorações de texto e efeitos visuais:

- **Decoração de Texto** — Nenhuma, Sublinhado, Sobrescrito ou Riscado
- **Estilo de Decoração** — Sólido, Tracejado, Pontilhado, Duplo ou Ondulado (aplica-se quando uma decoração estiver ativa)
- **Cor da Decoração** — Seletor de cor para a linha de decoração, padrão é a cor do texto
- **Sombra do Texto** — Efeito de sombra opcional com controles de deslocamento, desfoque e cor

## Aba Transformação

Mude a capitalização do texto sem editar o conteúdo:

| Opção | Resultado |
|--------|--------|
| **Nenhuma** | O texto aparece conforme escrito |
| **Maiúsculas** | TODAS AS LETRAS SÃO MAIÚSCULAS |
| **Minúsculas** | todas as letras são minúsculas |
| **Capitalizar** | A primeira letra de cada palavra é capitalizada |

Controles adicionais nesta aba incluem **Alinhamento do Texto** (esquerda, centro, direita, justificar), **Alinhamento Vertical** e **Direção do Texto** (LTR ou RTL).

## Famílias de Fonte Disponíveis

O editor inclui uma biblioteca curada de fontes do sistema e do Google Fonts, agrupadas por categoria:

| Categoria | Fontes |
|----------|-------|
| **Sistema** | Padrão do Sistema, Arial, Helvetica Neue, Helvetica, Segoe UI, Roboto, Ubuntu, Verdana, Tahoma, Trebuchet MS |
| **Sans-Serif (Modern)** | Inter, Montserrat, Poppins, DM Sans, Space Grotesk, Plus Jakarta Sans, Outfit, Manrope, Figtree, Josefin Sans |
| **Sans-Serif (Clássico)** | Open Sans, Lato, Nunito, Nunito Sans, Source Sans 3, Raleway, Rubik, Work Sans, Mulish, Cabin, Karla, Barlow, Lexend |
| **Sério** | Playfair Display, Merriweather, Lora, Libre Baskerville, Cormorant Garamond, Source Serif 4, EB Garamond, Crimson Pro, Bitter, Fraunces, Spectral, Cardo, Alegreya |
| **Sério (Sistema)** | Georgia, Times New Roman, Palatino, Book Antiqua, Garamond, Cambria |
| **Monospace** | Source Code Pro, Fira Code, JetBrains Mono, Roboto Mono, IBM Plex Mono, Space Mono, Inconsolata, Consolas, Monaco, Menlo, Courier New, SF Mono |
| **Exibição** | Oswald, Bebas Neue, Anton, Archivo Black, Rajdhani, Righteous, Abril Fatface, Archivo, Impact, Arial Black |

As fontes do Google Fonts são carregadas automaticamente ao serem selecionadas. As fontes do sistema usam cadeias de fallback CSS adequadas para renderização confiável em diferentes plataformas.

## Onde aparece

O Editor de Tipografia está disponível em todos os lugares onde o estilo do texto é necessário:

- **Construtor de Página** — Selecione qualquer elemento, abra a guia Estilo e clique na seção Tipografia
- **Construtor de Cabeçalho/Rodapé** — Estilize o texto em links de navegação, texto do logotipo, itens de menu e conteúdo do rodapé
- **Construtor de Menu** — Controle a tipografia para rótulos de menu e itens de submenu
- **Admin de Catálogo** — Usado em descrições de produtos e editores de conteúdo onde os controles de tipografia estão expostos

O editor é sempre acessado por meio da mesma interface consistente, independentemente do contexto.

## Dicas

- **Combine fontes intencionalmente** — use uma fonte de exibição ou séria para títulos e uma sans-serif limpa para o texto do corpo. Combinações clássicas como Playfair Display + Inter ou Montserrat + Merriweather funcionam bem.
- **Limite as famílias de fonte por página** — duas ou três famílias de fonte por página geralmente são suficientes. Mais do que isso pode reduzir a velocidade de carregamento e criar um excesso visual.
- **Use unidades relativas para texto responsivo** — em e rem escalam com o tamanho da fonte base, fazendo com que sua tipografia se adapte automaticamente a diferentes tamanhos de tela.
- **Verifique a disponibilidade de peso** — se o texto parecer o mesmo em 400 e 500, a fonte selecionada pode não suportar esse peso. O editor indica quais pesos cada fonte fornece.
- **Preview em todos os dispositivos** — o texto que parece bom em tamanhos de desktop pode ser muito pequeno ou muito grande em dispositivos móveis. Use o preview de dispositivo do Construtor de Página para verificar.
- **Use o preview em tempo real** — sempre compare Current vs New nas caixas de preview antes de aplicar para evitar mudanças inesperadas.
---
title: Editor de Sombra
---

O editor de sombra permite que você adicione profundidade e dimensão a elementos com sombras de caixa e sombras de texto configuráveis. As sombras criam uma hierarquia visual, atraem a atenção para elementos importantes e dão à sua loja online uma aparência polida e moderna. Abra a guia **Style** de qualquer elemento e procure pelo grupo **Effects** para acessar o editor de sombra.

![Editor de Sombra](/static/core/admin/img/help/shadow-editor/shadow-editor.webp)

## Tipos de Sombra

O editor oferece duas guias no topo:

- **Box Shadow** — Adiciona uma sombra ao redor da caixa delimitadora inteira do elemento. Use isso para cartões, botões, contêineres, imagens e seções.
- **Text Shadow** — Adiciona uma sombra apenas atrás dos caracteres do texto. Use isso para títulos ou texto sobreposto em imagens para melhorar a legibilidade.

Cada guia tem sua própria configuração independente. Você pode aplicar tanto uma sombra de caixa quanto uma sombra de texto ao mesmo elemento, se necessário.

## Propriedades de Sombra

Cada camada de sombra é definida pelas seguintes propriedades:

| Propriedade | Descrição | Intervalo |
|-------------|-----------|----------|
| **Offset X** | Distância horizontal da sombra em relação ao elemento | -50px a 50px |
| **Offset Y** | Distância vertical da sombra em relação ao elemento | -50px a 50px |
| **Blur Radius** | Quão suave ou difusa a borda da sombra parece. Valores mais altos produzem sombras mais suaves. | 0px a 100px |
| **Spread Radius** | Expande ou contrai o tamanho da sombra em relação ao elemento (sombra de caixa apenas) | -50px a 50px |
| **Color** | A cor da sombra, configurável com suporte completo a opacidade via seletor de cor | Qualquer cor com alfa |
| **Inset** | Alternar para renderizar a sombra dentro do elemento em vez de fora (sombra de caixa apenas) | Ligar / Desligar |

Ajuste os valores usando os sliders ou digite números precisos diretamente nos campos de entrada.

## Múltiplas Sombras

Você pode empilhar várias camadas de sombra em um único elemento para criar efeitos de profundidade complexos e realistas:

- Clique no botão **+** para adicionar uma nova camada de sombra
- Cada camada aparece como uma linha na lista de sombras com seus próprios controles
- Arraste as camadas para reordená-las — as sombras são renderizadas na ordem da lista, com a primeira camada no topo
- Ative o ícone **olho** em qualquer camada para ocultá-la temporariamente sem excluir a configuração
- Clique no ícone **lixeira** para remover uma camada

Combinar uma sombra estreita e escura com uma sombra ampla e suave cria um efeito natural de "elevação" que imita a profundidade física.

## Preset de Sombra

Presets de aplicação rápida permitem que você adicione estilos de sombra comuns com um único clique:

| Preset | Descrição |
|--------|-----------|
| **Pequena** | Sombra discreta e próxima para uma leve elevação (cartões, entradas) |
| **Média** | Profundidade moderada para elementos interativos (botões, menus suspensos) |
| **Grande** | Sombra proeminente para elementos flutuantes (modais, pop-ups) |
| **Suave** | Grande desfoque com baixa opacidade para um brilho suave e difuso |
| **Dura** | Mínimo desfoque com maior opacidade para uma borda definida e nítida |
| **Interna** | Sombra interna para um aspecto de botão pressionado ou recuado |

Após aplicar um preset, você pode ajustar propriedades individuais para afinar o resultado.

## Visualização Atual vs. Nova

No fundo do editor, duas caixas de comparação exibem a **sombra atual** (como salva) e a **nova sombra** (suas alterações pendentes). Essa visão lado a lado facilita a avaliação da diferença antes de confirmar. Clique em **Apply** para aceitar, ou clique fora para descartar suas alterações.

## Onde Ele Aparece

O editor de sombra está disponível nos seguintes locais:

- **Page Builder** — Guia **Style**, grupo **Effects** em seções, contêineres, colunas e elementos individuais
- **Header/Footer Builder** — Configurações de sombra no nível do widget para elementos como logotipos, barras de pesquisa e itens de navegação

Qualquer elemento que suporte o grupo de estilo **Effects** mostrará os controles do editor de sombra.

## Dicas

- Use sombras sutis (presets Pequena ou Suave) para a maioria dos elementos — sombras pesadas podem fazer o design parecer bagunçado.
- Combine uma sombra próxima e escura com uma sombra distante e clara para o efeito de elevação mais natural.
- Sombras internas funcionam bem em campos de entrada e contêineres para criar um efeito de painel "profundo".
- Sombras de texto devem ser mínimas — um deslocamento de 1px com um leve desfoque melhora a legibilidade em fundos de imagem sem parecer desatualizado.
- Teste suas sombras contra fundos claros e escuros, se seu tema suportar um botão de alternância para modo escuro.

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.
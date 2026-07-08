---
title: Editor de Espaçamento
---

O editor visual de espaçamento permite que você configure margens e preenchimento usando um diagrama do modelo de caixa intuitivo. O controle preciso do espaçamento garante layouts consistentes e experiências de leitura confortáveis em toda sua loja virtual. Abra a **aba Estilo** de qualquer elemento e procure a seção **Espaçamento** para acessar o editor.

![Editor de Espaçamento](/static/core/admin/img/help/spacing-editor/spacing-editor.webp)

## O Diagrama do Modelo de Caixa

O editor exibe um modelo de caixa visual com três camadas aninhadas:

- **Margem** (anel externo, geralmente mostrado em laranja) — O espaço fora da borda do elemento, separando-o dos elementos vizinhos
- **Preenchimento** (anel interno, geralmente mostrado em verde) — O espaço entre a borda do elemento e seu conteúdo
- **Conteúdo** (área central) — O conteúdo real do elemento, como texto ou uma imagem

Cada lado do diagrama (superior, direito, inferior, esquerdo) tem um manipulador arrastável e uma entrada numérica. Arraste um manipulador para fora para aumentar o valor ou para dentro para diminuí-lo. Você também pode clicar diretamente no valor de um lado para digitar um número preciso.

## Abas de Margem e Preenchimento

Duas abas no topo do editor alternam entre as visualizações de **Margem** e **Preenchimento**. Quando a **Margem** está selecionada, o anel externo é destacado e editável. Quando a **Preenchimento** está selecionada, o anel interno é destacado e editável. O anel inativo permanece visível para referência, mas fica desbotado.

Ambas as abas compartilham as mesmas opções de controle e unidades, então o fluxo de trabalho é idêntico para a configuração de margem e preenchimento.

## Controles por Lado

Cada lado tem uma entrada de valor independente e um seletor de unidade:

| Lado | Descrição |
|------|-------------|
| **Topo** | Espaço acima do elemento (margem) ou acima do conteúdo (preenchimento) |
| **Direita** | Espaço à direita do elemento ou conteúdo |
| **Fundo** | Espaço abaixo do elemento ou conteúdo |
| **Esquerda** | Espaço à esquerda do elemento ou conteúdo |

Clique no valor de qualquer lado no diagrama para selecioná-lo, depois digite um número ou use as teclas de seta para cima/baixo para incrementar em 1. Mantenha a tecla Shift pressionada enquanto pressiona as teclas de seta para incrementar em 10.

## Unidades

O seletor de unidade ao lado de cada entrada de valor permite que você escolha a unidade de medida:

| Unidade | Descrição |
|--------|-------------|
| **px** | Pixels. Tamanho fixo, consistente em todos os dispositivos. Ideal para valores de espaçamento precisos e pequenos. |
| **em** | Relativo ao tamanho da fonte do elemento. Escala com mudanças na tipografia. |
| **rem** | Relativo ao tamanho da fonte raiz. Fornece escala consistente em toda a página. |
| **%** | Percentagem da largura do elemento pai. Útil para layouts fluidos e responsivos. |
| **auto** | Permite que o navegador calcule o valor automaticamente. Comumente usado para centralização horizontal com margens esquerda/direita. |

Escolha uma unidade que corresponda ao seu objetivo — use `px` para lacunas fixas, `rem` para espaçamento escalável que respeita tokens de tipografia do tema e `%` para layouts que devem se adaptar à largura do contêiner.

## Ligar Lados

Um **ícone de ligação** no centro do diagrama ativa o modo de ligação:

- **Ligado** (ícone de cadeia conectado) — Alterar o valor de qualquer lado atualiza os quatro lados para o mesmo valor. Útil para espaçamento uniforme.
- **Desligado** (ícone de cadeia quebrado) — Cada lado é controlado independentemente. Use isso quando você precisar de valores diferentes para cima/baixo e esquerda/direita.

Clique no ícone de ligação para alternar entre os modos. Ao alternar do desligado para o ligado, os quatro lados são definidos para o valor do lado mais recentemente editado.

## Preset Rápido

Uma linha de botões de preset abaixo do diagrama fornece configurações de espaçamento com um clique:

| Preset | Valores |
|--------|--------|
| **Nenhum** | 0 em todos os lados |
| **Pequeno** | Espaçamento compacto adequado para layouts apertados e elementos inline |
| **Médio** | Espaçamento equilibrado para uso geral em cartões e seções |
| **Grande** | Espaçamento generoso para áreas de destaque e seções de alto destaque |
| **XL** | Espaçamento extra-largo para banners de largura total e seções principais da página |

Os presets aplicam-se à aba ativa (Margem ou Preenchimento) e definem os quatro lados ao mesmo tempo. Após aplicar um preset, você pode ajustar os lados individuais conforme necessário.

## Onde Ele Aparece

O editor de espaçamento está disponível para cada elemento que suporta espaçamento de layout:

- **Construtor de Página** — aba Estilo, seção Espaçamento em seções, contêineres, colunas e elementos individuais
- **Construtor de Cabeçalho/Rodapé** — controles de espaçamento entre linhas e widgets para lacunas verticais e horizontais
- **Construtor de Menu** — preenchimento de itens de menu e configurações de margem do contêiner

A mesma interface do editor é usada em todos os locais, garantindo uma experiência consistente entre os construtores.

## Dicas

- Use valores de espaçamento consistentes em todas as suas páginas — escolha 2-3 tamanhos padrão e mantenha-os para um layout limpo e profissional.
- Defina a margem como **auto** em esquerda e direita para centralizar horizontalmente um elemento de largura fixa dentro de seu elemento pai.
- Prefira unidades `rem` para espaçamento se seu tema usar tipografia responsiva, para que o espaçamento escale proporcionalmente ao tamanho do texto.
- Use o modo ligado para definir preenchimento uniforme rapidamente, depois desligue e ajuste individualmente os lados se o conteúdo precisar de espaçamento assimétrico.
- Evite preenchimento excessivo em dispositivos móveis — teste seu espaçamento em larguras de janela estreitas para garantir que o conteúdo não fique apertado ou excessivamente preenchido.
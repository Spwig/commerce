---
title: Editor de Borda
---

O Editor de Borda fornece um controle refinado sobre as bordas dos elementos, incluindo estilo, cor, largura por lado e raio de canto por canto. Ele abre como um painel flutuante com uma pré-visualização em tempo real e duas guias para configurações básicas e avançadas.

![Editor de Borda](/static/core/admin/img/help/border-editor/border-editor.webp)

## Pré-visualização em Tempo Real

Uma caixa de pré-visualização no topo do editor mostra suas alterações de borda em tempo real. A caixa exibe a palavra "Preview" dentro de um retângulo delimitado que se atualiza instantaneamente conforme você ajusta os valores de estilo, cor, largura e raio.

## Modo Básico vs. Avançado

O editor está organizado em duas guias:

| Guia | O que Contém |
|-----|-----------------|
| **Básico** | Estilo da borda, cor, largura (com controles por lado), e raio da borda (com controles por canto) |
| **Avançado** | Ajuste fino do raio de cada canto e a propriedade experimental de Forma de Canto |

A maioria das tarefas de borda é feita totalmente na guia Básico. A guia Avançada é útil quando você precisa de controle preciso sobre cantos individuais ou deseja experimentar com novas funcionalidades CSS.

## Estilo da Borda

Um menu suspenso com nove opções que controlam a aparência da linha da borda:

| Estilo | Descrição |
|-------|-------------|
| **Nenhum** | Nenhuma borda (remove qualquer borda existente) |
| **Sólido** | Uma única linha contínua (padrão) |
| **Tracejado** | Uma série de traços curtos |
| **Pontilhado** | Uma série de pontos redondos |
| **Duplo** | Duas linhas sólidas paralelas |
| **Groove** | Uma borda escavada com efeito 3D que parece pressionada na superfície |
| **Ridge** | Uma borda elevada com efeito 3D (oposto do groove) |
| **Inset** | Torna o elemento parecer embutido ou pressionado |
| **Outset** | Torna o elemento parecer elevado ou saliente |

Definir o estilo como Nenhum remove a borda completamente, independentemente das configurações de largura ou cor.

## Cor da Borda

Um campo de entrada de texto emparelhado com um botão de Seletor de Cor. Insira um valor hexadecimal diretamente (ex. `#3b82f6`) ou clique no swatch de cor para abrir o Seletor de Cor completo com modos de entrada hexadecimal, RGB e HSL, além de uma área visual de cor. A cor padrão é preta (`#000000`).

## Largura da Borda

Controla a espessura da borda em pixels. A guia Básico mostra quatro entradas individuais por lado:

| Lado | Entrada |
|------|-------|
| **Topo** | Entrada numérica, mínimo 0 |
| **Direita** | Entrada numérica, mínimo 0 |
| **Fundo** | Entrada numérica, mínimo 0 |
| **Esquerda** | Entrada numérica, mínimo 0 |

Um **botão de alternância de link** (ícone de cadeia) ao lado da etiqueta controla se todos os quatro lados estão vinculados:

- **Vinculado** (padrão) — alterar qualquer valor atualiza os quatro lados ao mesmo tempo
- **Desvinculado** — cada lado pode ter uma largura diferente, útil para efeitos como borda apenas no fundo ou bordas de destaque à esquerda

## Raio da Borda

Controla o arredondamento de cada canto. A guia Básico mostra quatro entradas de canto:

| Canto | Rótulo |
|--------|-------|
| **Canto Superior Esquerdo** | TL |
| **Canto Superior Direito** | TR |
| **Canto Inferior Esquerdo** | BL |
| **Canto Inferior Direito** | BR |

Um **botão de alternância de link** funciona da mesma forma que a largura da borda:

- **Vinculado** (padrão) — todos os quatro cantos compartilham o mesmo valor de raio
- **Desvinculado** — cada canto pode ter um raio diferente

Valores de raio comuns:

| Valor | Efeito |
|-------|--------|
| 0px | Cantos quadrados afiados |
| 4-8px | Arredondamento sutil, bom para cartões e botões |
| 12-16px | Arredondamento notável, um visual moderno e suave |
| 50% | Círculo completo ou forma de pílula (dependendo das dimensões do elemento) |

O seletor de unidade suporta px, em, rem e % para valores de largura e raio.

## Forma de Canto (Avançado)

A guia Avançada inclui uma propriedade experimental **Forma de Canto**. Esta funcionalidade CSS controla se os cantos arredondados usam a forma padrão redonda ou uma forma mais angular de "scoop". O suporte do navegador é limitado, e o editor exibe um aviso de compatibilidade quando o navegador atual não suporta essa propriedade.

## Ações do Rodapé

| Botão | Ação |
|--------|--------|
| **Redefinir** | Reverte todos os valores para o estado em que o editor foi aberto |
| **Cancelar** | Fecha o editor sem aplicar alterações |
| **Aplicar** | Salva as configurações de borda e fecha o editor |

## Onde Ele Aparece

O Editor de Borda está disponível em vários construtores:

- **Construtor de Página** — selecione qualquer elemento, abra a guia Estilo e clique na seção Borda
- **Construtor de Cabeçalho/Rodapé** — adicione bordas a seções de cabeçalho, contêineres de navegação e áreas de rodapé
- **Construtor de Menu** — estilize bordas em itens de menu e contêineres de menus suspensos

O editor lê os estilos de borda calculados atuais do elemento vivo no canvas, então ele sempre abre com os valores existentes corretos.

## Dicas

- **Use bordas com moderação** — bordas sutis de 1px em cinza claro criam uma separação limpa entre seções sem adicionar peso visual.
- **Combine raio com sombra** — cantos arredondados combinados com uma sombra de caixa suave (via o Editor de Sombra) produzem um efeito de cartão polido.
- **Experimente bordas de um lado** — desvincule os lados e defina apenas uma borda inferior ou esquerda para linhas de destaque, divisórias de seção ou indicadores de barra lateral.
- **Use raio em porcentagem para pílulas** — defina todos os cantos para 50% em um botão ou distintivo para criar uma forma de pílula que se adapta a qualquer tamanho de conteúdo.
- **Verifique a pré-visualização** — a caixa de pré-visualização em tempo real se atualiza imediatamente, então experimente livremente antes de aplicar.

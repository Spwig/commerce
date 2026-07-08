---
title: Page Builder
---

O Page Builder é um editor visual de arrastar e soltar para criar páginas ricas e responsivas sem escrever código. Adicione elementos de uma biblioteca de 39 componentes, estilize-os com utilitários poderosos, defina animações e regras de visibilidade e publique com histórico completo de versões.

![Page Builder](/static/core/admin/img/help/page-builder/builder-overview.webp)

## A Interface do Builder

O builder tem quatro áreas principais:

| Área | Localização | Propósito |
|------|----------|---------|
| **Barra de Ferramentas** | Barra superior | Pré-visualização do dispositivo (desktop/tablet/mobile), desfazer/refazer, configurações da página, salvar rascunho, publicar |
| **Biblioteca de Elementos** | Barra lateral esquerda | Navegue e arraste 39 elementos organizados em 9 categorias |
| **Canvas** | Centro | Área de edição WYSIWYG ao vivo — veja as alterações conforme as faz |
| **Painel de Propriedades** | Barra lateral direita | Edite o conteúdo, estilo, animações e configurações avançadas do elemento selecionado |

## Biblioteca de Elementos

Os elementos estão organizados em categorias. Arraste qualquer elemento da biblioteca para o canvas para adicioná-lo à sua página.

| Categoria | Elementos |
|----------|----------|
| **Layout** | Container, Divisor, Seção Hero, Janela Modal, Menu de Navegação, Espaçador |
| **Básico** | Cabeçalho, Texto, Botão, Ícone |
| **Conteúdo** | Carrossel de Posts do Blog, Grade de Posts do Blog, Acordion de Perguntas Frequentes, Posts Relacionados, Depoimentos |
| **Mídia** | Imagem, Galeria de Imagens, Acordion de Imagens, Incorporação de Vídeo |
| **Formulários** | Formulário de Contato, Formulário, Inscrição para Newsletter |
| **Marketing** | Cronômetro de Contagem Regressiva, Banner de CTA, Banner de Post do Blog Destacado, Banner de Fidelidade, Banner de Promoção, Selos de Confiança, Exibição de Código de Voucher |
| **E-commerce** | Destaque de Categoria, Promoção de Cartão-presente, Carrossel de Produtos, Grade de Produtos, Lista de Produtos, Exibição de Avaliações, Produtos em Promoção, Localizador de Loja |
| **Social** | Links Sociais |
| **Navegação** | Barra de Pesquisa |

### Containers e Aninhamento

O elemento **Container** é a base para layouts complexos. Os containers podem conter outros elementos — incluindo outros containers — permitindo que você crie grades de múltiplas colunas e estruturas aninhadas. Use os presets de layout do container para configurar rapidamente arranjos de coluna comuns (50/50, 33/33/33, 25/75, etc.).

## Adicionando Elementos

1. Encontre o elemento que deseja na barra lateral esquerda
2. **Arraste**-o para o canvas e solte-o onde desejar
3. Os elementos podem ser soltos entre elementos existentes ou dentro de containers
4. A linha de inserção azul mostra onde o elemento será colocado
5. Após soltar, o elemento é automaticamente selecionado e o painel de propriedades abre

Você também pode reordenar elementos arrastando-os para cima ou para baixo no canvas.

## Editando Conteúdo

Selecione qualquer elemento no canvas para abrir suas propriedades no painel direito. A guia **Conteúdo** mostra campos específicos para esse tipo de elemento.

![Painel de Propriedades](/static/core/admin/img/help/page-builder/properties-panel.webp)

Por exemplo:
- **Cabeçalho** — texto, tag HTML (H1–H6), alinhamento, ID de âncora
- **Imagem** — fonte da imagem (biblioteca de mídia), texto alternativo, link, dimensionamento
- **Botão** — rótulo, URL, variante de estilo, ícone
- **Grade de Produtos** — fonte de dados, número de colunas, produtos por página, ordem de classificação
- **Seção Hero** — título, subtítulo, descrição, fundo, botões de ação

Campos de conteúdo traduzíveis mostram um ícone de tradução — clique nele para adicionar traduções para lojas multilíngues.

## Estilizando Elementos

A guia **Estilo** fornece controles visuais para cada elemento. Cada seção abre um editor de utilitário dedicado.

![Guia Estilo](/static/core/admin/img/help/page-builder/style-tab.webp)

| Seção | O Que Controla | Utilitário |
|---------|-----------------|---------|
| **Tipografia** | Família de fonte, tamanho, peso, altura de linha, espaçamento entre letras, estilo do texto | Editor de Tipografia |
| **Cores** | Cor do texto com entrada de hex/RGB/HSL e tokens de tema | Seletor de Cor |
| **Fundo** | Fundo sólido, gradiente, imagem ou vídeo com estados de hover | Editor de Fundo |
| **Borda** | Largura, estilo, cor e raio da borda por lado | Editor de Borda |
| **Espaçamento** | Margem e preenchimento com editor de modelo de caixa visual | Editor de Espaçamento |
| **Efeitos** | Sombra de caixa com presets e suporte a camadas múltiplas, controle de opacidade | Editor de Sombra |

Cada utilitário é documentado em seu próprio tópico de ajuda — procure por "seletor de cor", "editor de fundo", etc. para aprender mais.

## Animações

A guia **Animações** permite adicionar movimento aos elementos.

### Animações de Entrada

Acionadas quando o elemento rola até a vista:

| Animação | Descrição |
|-----------|-------------|
| Fade In | Aparece gradualmente |
| Slide In (Up/Down/Left/Right) | Desliza da direção especificada |
| Zoom In | Cresce de tamanho pequeno para tamanho completo |
| Bounce In | Bate para o lugar |
| Pulse / Shake / Bounce / Flash / Spin | Efeitos para chamar atenção |

Configure **duração** (0,3s–1,5s), **atraso** (0–1s), **função de temporização** (ease, ease-in, ease-out, linear) e **repetição** (uma vez ou infinita).

### Animações de Hover

Acionadas quando um visitante passa o mouse sobre o elemento:

| Efeito | Descrição |
|--------|-------------|
| Scale Up / Scale Down | Cresce ou encolhe |
| Lift | Levita para cima |
| Rotate (CW / CCW) | Gira no sentido horário ou anti-horário |
| Brighten / Fade | Altera a luminosidade ou opacidade |
| Shadow Grow | Sombra se expande |
| Lift with Shadow | Levita com sombra crescente |
| Pulse Scale / Skew / Border Glow | Efeitos especiais |

Configure **duração**, **temporização** e **intensidade** (subtil, normal, forte).

## Configurações Avançadas

A guia **Avançado** fornece controle fino:

### Regras de Visibilidade

Controle quando um elemento é mostrado ou ocultado com base em condições:

- **Status do Usuário** — conectado, desconectado, novo cliente, cliente recorrente
- **Dispositivo** — desktop, tablet, mobile
- **Tempo** — faixa de data, hora do dia, dia da semana
- **Grupo de Clientes** — VIP, atacado, etc.
- **Valor do Carrinho** — total mínimo ou máximo do carrinho
- **Geografia** — país, região
- E mais de 20 tipos de regras

As regras podem ser combinadas com lógica AND/OR para alvo complexo.

### CSS Personalizado

| Campo | Propósito |
|-------|---------|
| **ID do Elemento** | ID único para links de âncora ou direcionamento CSS |
| **Classes CSS Personalizadas** | Classes adicionais para aplicar |
| **Estilos CSS Personalizados** | CSS inline para sobrescritas únicas |
| **Atributos de Dados** | Atributos de dados personalizados como pares chave-valor |
| **Z-Index** | Ordem de empilhamento para elementos sobrepostos |

## Fluxo de Publicação

As páginas usam um sistema de rascunho/publicação com histórico completo de versões:

| Status | Significado |
|--------|---------|
| **Rascunho** | Trabalho em progresso — não visível para visitantes |
| **Publicado** | Ativo no seu loja |
| **Arquivado** | Removido do site, mas preservado |

### Como Funciona

1. Faça alterações no builder — elas são salvas como um **rascunho**
2. Clique em **Salvar Rascunho** para salvar sem publicar
3. Clique em **Publicar** para tornar o rascunho atual ativo
4. Cada publicação cria um **snapshot de versão**
5. Você pode **restaurar** qualquer versão anterior a partir do histórico de versões (ícone de relógio na barra de ferramentas)

Isso significa que você pode experimentar livremente — sua página ativa permanece inalterada até que você publique explicitamente.

## Modelos de Página

Economize tempo trabalhando com modelos:

- **Salvar como Modelo** — salve o design de qualquer página como um modelo reutilizável
- **Criar a partir de Modelo** — comece uma nova página a partir de um modelo existente
- **Categorias de Modelo** — organize modelos por propósito (página de destino, sobre, destaque de produto, etc.)

Modelos capturam a estrutura completa da página, incluindo todos os elementos, conteúdo e estilização.

## Design Responsivo

Use os botões de pré-visualização do dispositivo na barra de ferramentas para ver como sua página se parece em diferentes tamanhos de tela:

- **Desktop** — layout de largura total
- **Tablet** — visor médio
- **Mobile** — visor estreito

Os elementos reorganizam automaticamente com base nas configurações do seu container. Você também pode usar regras de visibilidade para mostrar ou ocultar elementos específicos em dispositivos específicos.

## Dicas

- **Comece com um Container** — a maioria dos layouts começa com um container para criar colunas e estrutura. Use os presets de layout para arranjos comuns.
- **Use seções hero para cabeçalhos de página** — o elemento Hero fornece título, subtítulo, imagem de fundo e botões de ação em um único componente.
- **Pré-visualize antes de publicar** — clique em Pré-visualizar para ver exatamente o que os visitantes verão, depois publique quando estiver satisfeito.
- **Use regras de visibilidade para personalização** — mostre conteúdo diferente para visitantes conectados vs. desconectados, ou alvo grupos de clientes específicos.
- **Mantenha as animações sutis** — uma ou duas animações de entrada por seção de página parecem profissionais. Muitas animações podem parecer esmagadoras.
- **Nomeie seus containers** — use o campo ID do Elemento para rotular containers (ex.: "hero-section", "features") para que sejam fáceis de encontrar em páginas complexas.
- **Teste em todos os dispositivos** — use a pré-visualização do dispositivo para verificar seu layout em desktop, tablet e mobile antes de publicar.
- **Aproveite os modelos** — salve seus melhores designs de página como modelos para acelerar a criação de páginas futuras.
---
title: Biblioteca de Mídia
---

A Biblioteca de Mídia é o centro de gerenciamento de todas as imagens, vídeos, modelos 3D e arquivos usados em toda a sua loja. Carregue arquivos arrastando-os, organize com pastas e tags e deixe o sistema otimizar automaticamente as imagens para carregamento rápido.

![Galeria de Mídia](/static/core/admin/img/help/media-library/media-gallery.webp)

## Interface da Galeria

Navegue até **Biblioteca de Mídia** no menu lateral para abrir a galeria. A interface tem três áreas:

| Área | Localização | Propósito |
|------|----------|---------|
| **Zona de Upload** | Lado esquerdo, topo | Arraste e solte arquivos para carregar (imagens, vídeos, modelos 3D até 100MB) |
| **Pastas & Tags** | Lado esquerdo, abaixo | Navegue por pastas, filtre por tags, acesse o Lixeira |
| **Grade de Mídia** | Área principal | Pesquisar, filtrar, navegar e gerenciar todos os seus ativos |

### Controles da Barra de Ferramentas

A barra de ferramentas acima da grade de mídia fornece:

- **Pesquisa** — encontrar ativos pelo título, texto alternativo, descrição ou nome da tag
- **Filtro de Tipo** — mostrar apenas Imagens, Vídeos ou Modelos 3D
- **Filtro de Tamanho** — filtrar por tamanho de arquivo (Pequeno, Médio, Grande)
- **Ações em Lote** — Seleccionar Itens, Editar Detalhes, Excluir Seleccionados
- **Modos de Visualização** — Grade (grande), Grade Pequena ou Modo Lista (persistido em sessões)

## Carregando Arquivos

Arraste um ou mais arquivos para a zona de **Carregar** no lado esquerdo, ou clique na zona para abrir um seletor de arquivos.

### Formatos Suportados

| Tipo | Formatos |
|------|---------|
| **Imagens** | JPEG, PNG, GIF, WebP, SVG, BMP, TIFF |
| **Vídeos** | MP4, WebM, MOV, MKV, AVI |
| **Modelos 3D** | GLB, glTF |

### Fila de Upload

Ao carregar vários arquivos, um gerenciador de fila aparece mostrando:

- O nome de cada arquivo e a barra de progresso do upload
- Uploads simultâneos (até 2 de cada vez para desempenho)
- Status de processamento conforme os arquivos são otimizados após o upload
- Opção para cancelar uploads individuais ou limpar itens concluídos

A fila é arrastável e pode ser minimizada para que você possa continuar trabalhando enquanto os uploads terminam.

## Otimização Automática de Imagens

Toda imagem que você carrega é otimizada automaticamente:

- **Conversão para WebP** — uma versão WebP é gerada junto com a original (qualidade 85%) para carregamento mais rápido
- **Geração de Miniaturas** — várias versões com dimensões diferentes são criadas com base em seus presets de imagem
- **Orientação EXIF** — as imagens são automaticamente rotacionadas para a orientação correta

### Presets de Imagem do Sistema

A plataforma inclui 21 presets integrados que cobrem casos de uso comuns:

| Preset | Dimensões | Corte | Usado Para |
|--------|-----------|------|---------|
| **Miniatura** | 150 x 150 | Cover | Listas do administrador, pré-visualizações rápidas |
| **Pequena** | 300 x 300 | Cover | Cartões de produto pequenos |
| **Média** | 600 x 600 | Contain | Cartões de produto, miniaturas de blog |
| **Grande** | 1200 x 1200 | Contain | Páginas de detalhes do produto |
| **Galeria** | 800 x 800 | Contain | Galerias de imagens |
| **Destaque** | 1920 x 1080 | Cover | Seções de destaque, banners de página |
| **Banner** | 1200 x 400 | Cover | Banners de promoção |
| **Cartão** | 400 x 300 | Cover | Cartões de recursos, cartões de conteúdo |
| **Avatar** | 200 x 200 | Crop | Avatares de clientes e funcionários |
| **Lista de Produtos** | 400 x 400 | Cover | Cartões de grade de produtos |
| **Detalhe do Produto** | 1200 x 1200 | Cover | Imagens completas do produto |
| **Miniatura do Produto** | 100 x 100 | Cover | Seletor de variantes, carrinhos miniatura |
| **Banner de Categoria** | 1920 x 480 | Cover | Cabeçalhos de páginas de categoria |
| **Miniatura de Categoria** | 300 x 200 | Cover | Cartões de categoria |
| **Logo Cabeçalho** | 300 x 80 | Pad | Logo do cabeçalho do site |
| **Logo Rodapé** | 200 x 60 | Pad | Logo do rodapé do site |
| **Logo E-mail** | 400 x 100 | Pad | Logos de modelos de e-mail |
| **Logo Quadrado** | 160 x 160 | Pad | Posições de logos quadrados |
| **Logo da Marca** | 200 x 100 | Pad | Logos de marcas/parceiros |
| **Banner de Anúncio** | 800 x 300 | Cover | Imagens de anúncios |
| **Fundo de Anúncio** | 1200 x 800 | Cover | Fundos de anúncios |

Os presets do sistema não podem ser renomeados ou excluídos. Você pode criar presets personalizados adicionais sob **Biblioteca de Mídia > Presets de Tamanho de Imagem** se precisar de tamanhos não cobertos pelos padrões.

### Modos de Corte

| Modo | Comportamento |
|------|----------|
| **Cover** | Preenche toda a área, cortando as bordas se necessário — bom para cartões e banners |
| **Contain** | Ajusta a imagem inteira dentro da área, adicionando espaço transparente se necessário — bom para imagens de produto |
| **Crop** | Recorta exatamente as dimensões centrais |
| **Pad** | Ajusta a imagem e adiciona preenchimento (transparente, branco ou preto) — bom para logos |

## Organizando Arquivos

### Pastas

Crie pastas para organizar sua mídia em grupos lógicos. As pastas podem ser aninhadas em qualquer profundidade. Clique em uma pasta no menu lateral esquerdo para mostrar apenas os ativos dentro dela. O link **Todos os Arquivos** mostra tudo.

### Tags

Adicione tags aos ativos para organização flexível entre pastas. As tags aparecem em uma nuvem no menu lateral esquerdo. Clique em uma tag para filtrar ativos por essa tag. Os ativos podem ter várias tags.

### Pesquisa

A barra de pesquisa localiza ativos pelo título, texto alternativo, descrição ou nome da tag. Combine pesquisa com filtros de tipo e tamanho para resultados precisos.

## Detalhes do Ativo

Clique em um ativo para abrir sua visualização de detalhes com uma pré-visualização grande e metadados completos.

![Detalhes do Ativo](/static/core/admin/img/help/media-library/media-detail.webp)

A visualização de detalhes mostra:

- **Pré-visualização** — pré-visualização de imagem grande com as dimensões originais
- **Informações do Arquivo** — tipo, dimensões, tamanho do arquivo, data de upload
- **Abas** para edição:

| Aba | Campos |
|-----|--------|
| **Geral** | Título, Texto Alternativo, Descrição (todos traduzíveis para lojas multilíngue) |
| **Técnico** | Tipo MIME, hash do arquivo, nome do arquivo original, status da versão WebP |
| **Organização** | Atribuição de pasta, tags, alternar público/privado |
| **Avançado** | Coordenadas do ponto focal, ID externo, JSON de metadados |

### Campos Traduzíveis

Título, texto alternativo e descrição suportam traduções. Clique no ícone de tradução ao lado de cada campo para adicionar traduções para seus idiomas habilitados. Isso garante que as imagens tenham texto alternativo e descrições localizadas corretamente para SEO e acessibilidade.

### Rastreamento de Uso

O sistema rastreia onde cada ativo é usado em toda a plataforma. A seção **Usos de Mídia** no final mostra cada modelo e campo que referencia esse ativo, ajudando você a entender o impacto antes de fazer alterações ou excluir.

## Suporte a Vídeos

Vídeos carregados na biblioteca de mídia são analisados automaticamente:

- **Extração de Metadados** — duração, resolução, taxa de quadros, bitrate e códigos de vídeo são capturados
- **Imagem de Capa** — uma miniatura é gerada do vídeo para pré-visualização
- **Streaming** — os vídeos suportam solicitações de intervalo para buscar sem baixar o arquivo completo
- **Conversão Opcional** — os vídeos podem ser convertidos para formatos otimizados WebM/AV1 para entrega mais rápida

## Lixeira

Excluir um ativo move-o para a **Lixeira** em vez de removê-lo permanentemente. Isso protege contra exclusões acidentais.

| Ação | O Que Ela Faz |
|--------|-------------|
| **Excluir** | Move o ativo para a Lixeira (exclusão suave) |
| **Restaurar** | Retorna um ativo excluído para seu local original |
| **Excluir Permanentemente** | Remove o ativo e todas as suas miniaturas do armazenamento permanentemente |
| **Esvaziar Lixeira** | Exclui permanentemente todos os itens na Lixeira |

Clique em **Lixeira** no menu lateral esquerdo para visualizar e gerenciar ativos excluídos.

## Onde a Biblioteca de Mídia é Usada

A biblioteca de mídia é integrada em toda a plataforma:

| Funcionalidade | Como Utiliza a Mídia |
|---------|------------------|
| **Catálogo de Produtos** | Imagens de produto, imagens de variantes, banners de categoria |
| **Blog** | Imagens destacadas, imagens no conteúdo via CKEditor |
| **Construtor de Páginas** | Elementos de imagem, fundos de destaque, componentes de galeria |
| **Construtor de Cabeçalho/Rodapé** | Imagens de logotipo, imagens de fundo |
| **Configurações do Site** | Logotipo do site e favicon |
| **Anúncios** | Imagens de anúncios e fundos de anúncios |
| **CKEditor** | Todos os carregamentos de imagens em texto rico roteiam pela biblioteca de mídia |
| **Programa de Fidelidade** | Imagens de recompensas e níveis |

Quando você seleciona uma imagem em qualquer uma dessas funcionalidades, a galeria da biblioteca de mídia abre como um modal para navegação e seleção fáceis.

## Dicas

- **Use títulos e textos alternativos descritivos** — bons metadados melhoram o SEO e a acessibilidade. O sistema usa o texto alternativo nas tags de imagem em toda a loja.
- **Organize com pastas desde o início** — crie uma estrutura de pastas (ex: Produtos, Blog, Banners, Logos) antes de carregar muitos arquivos. É muito mais fácil organizar enquanto vai adicionando do que reorganizar depois.
- **Use tags para categorias transversais** — tags como "estacional", "venda" ou "estilo de vida" ajudam a encontrar ativos que abrangem múltiplas pastas.
- **Verifique o uso antes de excluir** — a seção de rastreamento de uso mostra onde um ativo é referenciado. Excluir um ativo usado pode deixar imagens quebradas em sua loja.
- **Deixe o WebP fazer o trabalho** — a conversão automática para WebP geralmente reduz os tamanhos de arquivos em 25-35% em comparação com JPEG, sem perda visível de qualidade. Você não precisa converter imagens manualmente antes de carregar.
- **Crie presets personalizados** — se você tiver um layout único que precise de um tamanho de imagem específico, crie um preset personalizado em vez de redimensionar manualmente as imagens.
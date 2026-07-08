---
title: Gerenciamento de Blog
---

O blog permite que você publique artigos, guias e notícias para atrair tráfego e engajar seu público. O blog do Spwig inclui um editor de texto rico, publicação programada, notificações para assinantes, compartilhamento automático em redes sociais e ferramentas de SEO.

![Posts do blog](/static/core/admin/img/help/blog-management/blog-post-list.webp)

## Criando um Post do Blog

Navegue até **Marketing > Posts do Blog** e clique em **Adicionar Post**.

### Conteúdo do Post

Escreva seu post usando o editor de texto rico **CKEditor 5**, que oferece suporte a:
- Formatação de texto (títulos, negrito, itálico, listas, citações)
- Imagens e mídia (carregadas através da biblioteca de mídia)
- Vídeos embutidos (YouTube, Vimeo)
- Tabelas e blocos de código
- Links para produtos, categorias e URLs externas

Para layouts mais complexos, ative o **Page Builder** para usar o construtor de páginas arrastável em vez do editor de texto.

### Configurações do Post

| Configuração | Descrição |
|---------|-------------|
| **Título** | O título principal exibido no blog e nos resultados de pesquisa |
| **Slug** | Identificador amigável para URL (gerado automaticamente a partir do título, editável) |
| **Resumo** | Resumo curto exibido nas cartões de listagem do blog e feeds RSS |
| **Imagem em Destaque** | Imagem principal exibida no topo do post e em cartões de listagem |
| **Categoria** | Categoria principal do post |
| **Tags** | Palavras-chave para filtragem e conteúdo relacionado |
| **Autor** | Membro da equipe creditado como autor |
| **Status** | Rascunho, Agendado, Publicado ou Arquivado |
| **Destaque** | Fixe o post no topo da listagem do blog |

### Configurações de SEO

Cada post inclui campos de SEO:
- **Título Meta** — Título personalizado para resultados de motores de busca (padrão é o título do post)
- **Descrição Meta** — Resumo exibido nos resultados de motores de busca
- **Imagem Open Graph** — Imagem usada quando o post é compartilhado em redes sociais

## Status dos Posts

| Status | Descrição |
|--------|-------------|
| **Rascunho** | Trabalho em andamento, não visível para o público |
| **Agendado** | Será publicado automaticamente em uma data e hora definidas |
| **Publicado** | Ativo e visível para os visitantes |
| **Arquivado** | Oculto da listagem do blog, mas ainda acessível por meio de URL direta |

### Agendando Posts

Para agendar um post para publicação futura:
1. Defina o status como **Agendado**
2. Escolha a **data e hora de publicação**
3. Salve o post

Uma tarefa em segundo plano publica automaticamente o post no horário agendado e aciona notificações para assinantes.

## Categorias

Navegue até **Marketing > Categorias do Blog** para organizar seu conteúdo.

As categorias oferecem suporte a:
- **Hierarquia** — Crie categorias pai e filha (ex: "Guias" > "Começando")
- **URLs Personalizadas** — Cada categoria tem seu próprio slug para URLs limpas
- **Descrições** — Adicione descrições de categorias exibidas na página de arquivos de categorias
- **Ordenação** — Controle a ordem de exibição das categorias na navegação

## Tags

As tags oferecem uma maneira secundária de classificar o conteúdo. Diferente das categorias (que são hierárquicas), as tags são rótulos planos. Os visitantes podem clicar em uma tag para ver todos os posts com essa tag.

## Assinantes

Navegue até **Marketing > Assinantes do Blog** para gerenciar sua lista de assinantes.

### Como Funcionam as Inscrições

1. Os visitantes se inscrevem por meio de um formulário no blog (endereço de e-mail obrigatório)
2. Um e-mail de **confirmação de inscrição dupla** é enviado
3. Após a confirmação, o assinante recebe notificações quando novos posts são publicados

### Frequência das Notificações

Os assinantes escolhem com que frequência recebem notificações:

| Frequência | Descrição |
|-----------|-------------|
| **Imediata** | E-mail enviado assim que um novo post é publicado |
| **Resumo Semanal** | Um resumo semanal de todos os novos posts |
| **Resumo Mensal** | Um resumo mensal de todos os novos posts |

Tarefas em segundo plano lidam com a compilação e entrega dos resumos automaticamente.

### Gerenciando Assinantes

- Visualize a contagem de assinantes, status de confirmação e data de inscrição
- Exporte listas de assinantes para uso em ferramentas de marketing por e-mail externas
- Remova ou cancele o assinato de endereços individuais
- Cada e-mail de notificação inclui um link de **cancelamento de inscrição** com um único clique

## Compartilhamento Automático em Redes Sociais

O Spwig pode compartilhar automaticamente novos posts em suas contas de redes sociais quando são publicados.

### Conectando Contas de Redes Sociais

Navegue até **Marketing > Conectores de Redes Sociais** para conectar suas contas:

| Plataforma | Autenticação |
|----------|---------------|
| **Facebook** | OAuth — conecte sua Página do Facebook |
| **Instagram** | OAuth — conecte sua conta comercial |
| **LinkedIn** | OAuth — conecte sua página da empresa |

### Como Funciona o Compartilhamento Automático

1. Conecte uma ou mais contas de redes sociais
2. Ao criar um post, ative **Compartilhamento Automático** para cada conta conectada
3. Personalize a mensagem de compartilhamento (padrão é o título do post e resumo)
4. Quando o post é publicado (ou atinge o horário agendado), ele é compartilhado automaticamente

O compartilhamento automático também funciona com posts agendados — o compartilhamento nas redes sociais é enviado no mesmo momento em que o post vai ao ar.

## Feed RSS

O blog gera automaticamente um feed RSS em `/blog/feed/`. Isso permite que visitantes e agregadores se inscrevam no seu conteúdo. O feed inclui:
- Título e resumo do post
- Data de publicação
- Informações do autor
- Link direto para o post completo

## Configurações do Blog

Navegue até **Marketing > Configurações do Blog** para configurar opções globais do blog:

- **Posts por Página** — Número de posts exibidos por página na listagem
- **Permitir Comentários** — Ative ou desative comentários em posts
- **Categoria Padrão** — Categoria de fallback para posts sem uma categoria atribuída
- **Botões de Compartilhamento em Redes Sociais** — Exiba botões de compartilhamento em páginas de posts individuais

## Dicas

- Escreva posts com **SEO em mente** — use títulos descritivos, preencha as descrições meta e inclua palavras-chave relevantes naturalmente no conteúdo.
- Use **publicação agendada** para manter uma cadência de postagens consistente sem esforço manual.
- Ative **compartilhamento automático** para maximizar o alcance — posts compartilhados em redes sociais logo após a publicação obtêm mais engajamento.
- Incentive os visitantes a **se inscreverem** colocando o formulário de inscrição em destaque no seu blog e usando uma chamada para ação convincente.
- Use **categorias** para agrupamentos de conteúdo amplos e **tags** para tópicos específicos — isso ajuda os visitantes a encontrar conteúdo relacionado.
- Adicione uma **imagem em destaque** a cada post — posts com imagens performam melhor nos resultados de busca e compartilhamentos em redes sociais.
- Use a opção de **resumo semanal ou mensal** para assinantes que não desejam e-mails frequentes — isso reduz as taxas de cancelamento de inscrição.
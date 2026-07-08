---
title: Explicação sobre Motores de Busca
---

Motores de busca no Spwig não são serviços externos como Elasticsearch ou Algolia - são contextos de configuração dentro do sistema de busca nativo do banco de dados da sua loja. Cada motor define quais tipos de conteúdo pesquisar, o que excluir e como os resultados devem ser classificados. Este guia explica o que são motores de busca, quando criar múltiplos motores e como configurá-los.

A maioria dos varejistas usa um único motor padrão "shop". Crie múltiplos motores apenas quando precisar de misturas de conteúdo diferentes ou exclusões para diferentes casos de uso.

![Lista de Motores de Busca](/static/core/admin/img/help/search-engines-explained/search-engines-list.webp)

## O que são Motores de Busca?

Um motor de busca no Spwig é uma configuração nomeada que especifica:

- **Quais tipos de conteúdo pesquisar** (produtos, categorias, marcas, posts de blog)
- **O que excluir** (categorias ou marcas específicas que você deseja ocultar da busca)
- **Peso de relevância personalizado** (sobrescrita opcional de peso por motor)
- **Status ativo** (motores podem ser desativados temporariamente)

Cada motor tem um slug único usado em chamadas de API e código frontend para especificar qual motor deve lidar com uma solicitação de busca.

## Quando Criar Múltiplos Motores

A maioria das lojas precisa apenas de um motor. Crie motores adicionais para esses cenários:

| Caso de Uso | Exemplo |
|-------------|---------|
| **Misturas de conteúdo diferentes** | Motor de loja busca apenas produtos; motor de blog busca apenas posts de blog |
| **Exclusões seletivas** | Motor de loja principal oculta categoria de liquidação; motor de liquidação mostra apenas itens de liquidação |
| **Busca específica por departamento** | Motor de eletrônicos exclui categorias de roupas; motor de roupas exclui eletrônicos |
| **Separação B2B vs B2C** | Motor de atacado mostra apenas produtos em quantidade; motor de varejo mostra produtos para consumo |

Se você não tiver certeza se precisa de múltiplos motores, mantenha-se com um. Adicionar motores cria complexidade sem benefícios, a menos que você tenha um caso de uso específico.

## O Assistente de 4 Passos

![Etapa 1 do Assistente - Informações Básicas](/static/core/admin/img/help/search-engines-explained/wizard-step1-basic.webp)

Navegue até **Search > Setup Wizard** para criar um novo motor por meio de um processo guiado em 4 etapas:

### Etapa 1: Informações Básicas

**Nome do Motor** - Nome amigável para exibição (ex.: "Busca da Loja", "Busca do Blog"). Usado apenas na interface de administração.

**Slug** - Identificador seguro para URL (ex.: "shop-search", "blog-search"). Usado em chamadas de API e código frontend. Gerado automaticamente a partir do nome se deixado em branco.

**Ativo** - Se este motor está disponível para buscas. Motores inativos não retornam resultados.

### Etapa 2: Tipos de Conteúdo

Selecione quais tipos de conteúdo este motor buscará:

- Produtos (inclui todos os tipos de produtos: físicos, digitais, assinaturas)
- Categorias
- Marcas
- Posts de Blog

**Dica**: Selecione apenas os tipos de conteúdo relevantes para o propósito deste motor. Um motor focado em blog não precisa de produtos habilitados.

### Etapa 3: Pesos (Opcional)

![Etapa 3 do Assistente - Pesos](/static/core/admin/img/help/search-engines-explained/wizard-step3-weights.webp)

Personalize opcionalmente os pesos de relevância para este motor específico. Se pular esta etapa, o motor herda os pesos globais de SearchSettings.

A maioria dos motores deve pular esta etapa e usar os valores padrão globais. Personalize os pesos apenas se este motor tiver necessidades de classificação únicas (ex.: um motor de blog pode aumentar o weight_blog_posts para 1.2).

### Etapa 4: Revisão e Criação

Revise sua configuração e clique em **Criar Motor** para salvar.

## Campos de Configuração do Motor

Se você editar um motor diretamente (ignorando o assistente), verá estes campos:

**Nome e Slug** - Nome de exibição e identificador de URL

**Status Ativo** - Alternar para habilitar/desabilitar

**Tipos de Conteúdo** - Array JSON como `[
---
title: Entendendo as Configurações de Pesquisa
---

A interface SearchSettings controla todo o comportamento global de pesquisa em sua loja Spwig. Esta única página de configuração usa uma interface de 8 abas para organizar as opções de pesquisa, desde a ativação básica até ajustes avançados de desempenho. As alterações aqui se aplicam a todos os motores de pesquisa, a menos que sejam substituídas no nível do motor.

Este guia passa por cada aba, explicando o que cada configuração faz e quando ajustá-la.

![Aba Geral das Configurações de Pesquisa](/static/core/admin/img/help/search-settings-overview/search-settings-general.webp)

## A Interface de 8 Abas

SearchSettings é um modelo singleton - apenas um registro de configuração existe (pk=1) para toda sua loja. A interface é dividida em oito abas:

| Aba | Propósito |
|-----|---------|
| **Geral** | Ativar/desativar a pesquisa, definir parâmetros básicos |
| **Autocomplete** | Configurar o comportamento do menu suspenso de pesquisa preditiva |
| **Tipos de Conteúdo** | Escolher quais tipos de conteúdo são pesquisáveis |
| **Indexação Profunda** | Controlar quais dados do produto são indexados (impacto no desempenho) |
| **Correspondência Fuzzy** | Tolerância a erros de digitação e limites de similaridade |
| **Pesos** | Multiplicadores de relevância para classificar os resultados |
| **Caching** | Compromisso entre tempo de resposta e frescor dos resultados |
| **Análise** | Rastreamento de consultas e configurações de privacidade |

Cada aba se concentra em um aspecto específico da configuração de pesquisa.

## Aba Geral

A aba Geral contém configurações principais que afetam todas as pesquisas:

**Ativar Pesquisa** - Interruptor mestre para o sistema de pesquisa. Quando desativado, todas as funcionalidades de pesquisa estão inativas em toda sua loja, incluindo autocomplete e a página de resultados de pesquisa.

**Comprimento Mínimo da Consulta** - Padrão: 2 caracteres. Consultas mais curtas que isso são rejeitadas. Definir isso para 1 permite consultas com um único caractere (ex.: "A") mas aumenta a carga do servidor.

**Resultados por Página** - Padrão: 20 itens. Controla a paginação para páginas de resultados de pesquisa. Valores mais altos (30-50) reduzem cliques de paginação, mas aumentam o tempo de carregamento da página.

## Aba Tipos de Conteúdo

![Configurações de Tipos de Conteúdo](/static/core/admin/img/help/search-settings-overview/search-settings-content-types.webp)

Ative/desative quais tipos de conteúdo aparecem nos resultados da pesquisa:

- **Produtos** - Produtos físicos, digitais e de assinatura
- **Categorias** - Categorias de produtos
- **Marcas** - Marcas de produtos
- **Posts do Blog** - Conteúdo do blog

**Nota de Desempenho**: Menos tipos de conteúdo = pesquisas mais rápidas. Cada tipo ativado adiciona consultas adicionais ao banco de dados. Se você não tiver um blog, desative os Posts do Blog para melhorar os tempos de resposta.

## Aba Indexação Profunda

⚠️ **AVISO DE DESEMPENHO** - Essas configurações têm implicações significativas no desempenho.

![Configurações de Indexação Profunda](/static/core/admin/img/help/search-settings-overview/search-settings-deep-indexing.webp)

A indexação profunda controla quais dados relacionados aos produtos são incluídos nas pesquisas:

**Indexar SKUs** - Padrão: LIGADO, baixo impacto. Inclui SKUs de produtos e variantes na pesquisa. Essencial para lojas B2B onde os clientes pesquisam por códigos de produto.

**Indexar Atributos** - Padrão: LIGADO, impacto médio. Inclui atributos de produtos (cor, tamanho, material) na pesquisa. Adiciona JOIN à tabela de atributos. Importante para produtos de moda e configuráveis.

**Indexar Campos Personalizados** - Padrão: LIGADO, impacto médio. Inclui campos personalizados definidos pelo vendedor nos resultados da pesquisa. Requer percurso de JSONField.

**Indexar Avaliações** - Padrão: LIGADO, impacto médio-alto. Inclui títulos e comentários de avaliações aprovadas na pesquisa. Junta-se à tabela de avaliações e adiciona sobrecarga de pesquisa de texto. Útil para catálogos com muitas avaliações.

**Indexar Documentos** - Padrão: DESATIVADO, **IMPACTO MUITO ALTO** ⚠️

A indexação de documentos extrai texto de arquivos PDF, DOCX e XLSX anexados a produtos digitais. Esta funcionalidade:

- Requer indexação inicial muito cara
- Adiciona sobrecarga significativa de consulta em cada pesquisa
- Pode causar tempos de resposta longos em arquivos grandes
- **Deve ser ativada apenas para lojas de produtos digitais com documentos pesquisáveis**
- **Nunca ative casualmente** - teste o impacto no desempenho de forma abrangente

## Aba Correspondência Fuzzy

![Configurações de Correspondência Fuzzy](/static/core/admin/img/help/search-settings-overview/search-settings-fuzzy-matching.webp)

A correspondência fuzzy usa a distância de Levenshtein para lidar com erros de digitação:

**Ativar Correspondência Fuzzy** - Permite que as pesquisas correspondam a termos semelhantes (ex.: "laptop" corresponde a "labtop")

**Limiar de Similaridade** - Padrão: 0,80 (80% de similaridade). Intervalo: 0,0-1,0. Valores mais altos exigem correspondências mais próximas e executam mais rápido. Valores mais baixos capturam mais erros de digitação, mas podem retornar resultados irrelevantes.

**Máximo de Distância de Edição** - Padrão: 2 mudanças de caracteres. Número máximo de inserções, exclusões ou substituições permitidas. Valores mais baixos (1) melhoram o desempenho, mas capturam menos erros de digitação.

## Aba Pesos

Os pesos controlam o pontuamento de relevância - como os resultados são classificados. A aba Pesos mostra os multiplicadores padrão para cada campo pesquisável:

- weight_name: 1,50 (nomes de produtos são os mais importantes)
- weight_sku: 1,20
- weight_description: 0,80
- weight_categories: 0,80
- weight_attributes: 0,70
- weight_brands: 0,70
- weight_blog_posts: 0,60
- weight_reviews: 0,50

Esses valores padrão funcionam bem para a maioria das lojas de e-commerce. Para informações detalhadas sobre como ajustar pesos e entender seu impacto, consulte o tópico [Pesos de Relevância e Indexação Profunda](/en/admin/help/relevance-weights-deep-indexing/).

## Aba Caching

![Configurações de Caching](/static/core/admin/img/help/search-settings-overview/search-settings-caching.webp)

O caching melhora drasticamente o desempenho da pesquisa armazenando resultados recentes:

**TTL do Cache de Autocomplete** - Padrão: 60 segundos. Quanto tempo os resultados do autocomplete são armazenados em cache. TTL mais curto (30-45s) = resultados mais recentes, mas mais consultas ao banco de dados. TTL mais longo (90-120s) = mais rápido, mas resultados potencialmente desatualizados.

**TTL do Cache de Resultados** - Padrão: 300 segundos (5 minutos). Duração do cache da página inteira de resultados de pesquisa. TTL mais longo melhora significativamente o desempenho, mas atrasa a visibilidade de novos produtos.

**Compromissos**: O caching é a otimização de desempenho mais eficaz. Se as pesquisas forem lentas, aumente esses valores antes de desativar funcionalidades.

## Aba Análise

![Configurações de Análise](/static/core/admin/img/help/search-settings-overview/search-settings-analytics.webp)

**Rastrear Consultas de Pesquisa** - Habilita o painel de análise de pesquisa. Registra o texto da consulta, a contagem de resultados, o tempo de resposta e o carimbo de data/hora.

**Rastrear Informações do Usuário** - Associa pesquisas a usuários autenticados. Desative para conformidade com privacidade (GDPR, CCPA).

**Rastrear Informações da Sessão** - Usa IDs de sessão para rastrear pesquisas de usuários anônimos. Útil para identificar padrões de pesquisa sem dados pessoais.

## Padrão Singleton

SearchSettings usa um padrão singleton - apenas um registro de configuração existe em seu banco de dados (pk=1). Quando você navega até Configurações de Pesquisa no administrador, você está sempre editando o mesmo registro.

Não há opção de "Adicionar" ou "Excluir" - apenas "Alterar". Todos os motores de pesquisa herdam essas configurações, a menos que especifiquem substituições por motor (raro).

## Dicas

- **Mantenha os valores padrão a menos que tenha uma necessidade específica** - As configurações padrão são otimizadas para lojas de e-commerce típicas
- **NUNCA ative a indexação de documentos casualmente** - Apenas para lojas de produtos digitais com documentos pesquisáveis, e teste o impacto no desempenho primeiro
- **Monitore os tempos de resposta na análise** - Alvo <200ms para autocomplete, <500ms para pesquisa completa
- **Aumente o TTL do cache se o desempenho for lento** - O caching é a vitória mais fácil de desempenho
- **Revise consultas com zero resultados semanalmente** - Elas revelam produtos ausentes ou sinônimos necessários
- **Desative tipos de conteúdo não utilizados** - Se você não tiver um blog, desative os Posts do Blog para acelerar as pesquisas

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.
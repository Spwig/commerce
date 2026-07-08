---
title: Configurando Autocomplete
---

Autocomplete, também chamado de pesquisa preditiva ou pesquisa enquanto digita, exibe resultados enquanto os clientes digitam suas consultas. Isso melhora drasticamente a experiência do usuário ajudando os clientes a encontrar produtos mais rapidamente e reduzindo pesquisas sem resultados. Este guia explica como configurar o comportamento do autocomplete, as configurações de exibição e os trade-offs de desempenho.

O autocomplete está ativado por padrão com configurações razoáveis. Ajuste essas configurações apenas se você tiver preocupações específicas de desempenho ou preferências de exibição.

![Configurações de Autocomplete](/static/core/admin/img/help/configuring-autocomplete/autocomplete-settings-main.webp)

## Habilitando Autocomplete

Navegue até **Search > Search Settings** e clique na guia **Autocomplete**.

**Enable Autocomplete** - Interruptor mestre para pesquisa preditiva. Quando habilitado, os campos de pesquisa mostram um menu suspenso de resultados conforme os clientes digitam.

**Max Results Per Type** - Padrão: 8 itens. Quantos resultados mostrar para cada tipo de conteúdo (produtos, categorias, marcas, posts de blog). Valores mais baixos (5-6) reduzem o tamanho da carga do API e renderizam mais rápido. Valores mais altos (10-12) dão aos clientes mais opções, mas atrasam a resposta.

## Timing de Debounce

⚠️ **AVISO DE DESEMPENHO** - O timing de debounce afeta significativamente a carga do servidor.

**Debounce Delay** - Padrão: 300ms. Quanto tempo esperar após o último toque de tecla antes de disparar uma solicitação de autocomplete.

Esta configuração equilibra a responsividade com a carga do servidor:

| Delay | Experiência do Usuário | Impacto no Servidor |
|-------|----------------|---------------|
| **100ms** | Muito responsivo | 3x mais chamadas de API do que 300ms - alta carga |
| **200ms** | Responsivo | 1,5x mais chamadas de API do que 300ms |
| **300ms** | Bom equilíbrio (recomendado) | Padrão |
| **400ms** | Levemente lento | Menos chamadas de API - menor carga |
| **500ms** | Atraso notável | 50% menos chamadas, mas parece lento |

**Recomendação**: Mantenha entre 250-350ms. Apenas aumente acima de 350ms se seu servidor estiver com dificuldades com a carga de autocomplete. Nunca vá abaixo de 200ms a menos que você tenha um servidor muito rápido e um catálogo pequeno.

## Configurações de Exibição para Produtos

Estes interruptores controlam o que informações aparecem nos resultados do autocomplete de produtos:

**Show Thumbnail** - Padrão: LIGADO. Exibe a imagem do produto ao lado do resultado. **Impacto no desempenho**: Adiciona uma consulta de imagem e aumenta o tamanho do payload JSON. Desative para autocomplete mais rápido em conexões lentas.

**Show Description** - Padrão: DESATIVADO. Exibe a descrição curta do produto. **Impacto no desempenho**: Adiciona processamento de texto e aumenta significativamente o tamanho do payload. Mantenha desativado a menos que as descrições sejam críticas para a seleção do produto.

**Show Price** - Padrão: LIGADO. Exibe o preço do produto. **Impacto no desempenho**: Baixo - os dados de preço já estão carregados com o produto. Seguro manter habilitado.

**Show SKU** - Padrão: LIGADO. Exibe o SKU do produto. **Impacto no desempenho**: Baixo - SKU já indexado. Essencial para lojas B2B.

**Show Stock Status** - Padrão: DESATIVADO. **⚠️ AVISO DE DESEMPENHO MAIOR**

Exibe os carimbos "In Stock", "Low Stock" ou "Out of Stock". **NUNCA habilite isso em catálogos grandes**.

O status do estoque requer a agregação `with_stock_totals()` - calculando as quantidades disponíveis em todos os centros de distribuição para cada produto nos resultados do autocomplete. Isso adiciona:
- Carga significativa no banco de dados (consultas de agregação)
- 200-500ms de latência adicional em catálogos com mais de 1.000 produtos
- Potenciais tempos limite em catálogos com mais de 10.000 produtos

Apenas habilite se for absolutamente crítico e você tiver menos de 500 produtos.

## Configurações de Exibição para Posts de Blog

**Show Featured Image** - Padrão: LIGADO. Miniatura do post de blog nos resultados do autocomplete.

**Show Excerpt** - Padrão: LIGADO. Texto de prévia breve do conteúdo do post.

**Excerpt Length** - Padrão: 60 caracteres. Quanto texto de prévia mostrar.

Essas configurações têm impacto mínimo no desempenho, já que os posts de blog são normalmente poucos em número em comparação aos produtos.

## Configurações de Exibição para Categorias e Marcas

**Show Thumbnail/Logo** - Padrão: LIGADO. Imagem da categoria ou marca nos resultados.

**Show Product Count** - Padrão: DESATIVADO. **⚠️ AVISO DE DESEMPENHO**

Exibe quantos produtos estão em cada categoria ou marca (ex: "Electronics (234)").

**NUNCA habilite isso em catálogos grandes**. As contagens de produtos são recalculadas em cada solicitação de autocomplete:
- Cada tipo de conteúdo com contagens habilitadas adiciona 2 consultas extras
- As consultas incluem junções e agregações
- Latência adicional típica de 100-300ms
- Aumenta linearmente com o número de categorias/marcas

Apenas habilite se você tiver menos de 50 categorias/marcas E menos de 1.000 produtos no total.

## Caching

**Autocomplete Cache TTL** - Padrão: 60 segundos (definido na guia Caching).

Os resultados do autocomplete são armazenados em cache para melhorar o desempenho. O TTL de 60 segundos significa:
- O primeiro cliente pesquisando "laptop" aciona uma consulta no banco de dados
- Nos próximos 59 segundos, todas as pesquisas de "laptop" retornam resultados em cache
- Após 60 segundos, o cache expira e a próxima pesquisa atualiza os dados

**Recomendação para TTL**:
- **45-60s**: Bom equilíbrio para a maioria das lojas (padrão)
- **90-120s**: Melhor desempenho se o estoque de produtos mudar raramente
- **30s**: Resultados mais recentes se você adicionar produtos com frequência

Aumentar o TTL do cache é a forma mais fácil de melhorar o desempenho do autocomplete.

## Autocomplete Multilíngue

Se você tiver múltiplos idiomas configurados, o autocomplete pesquisa automaticamente o conteúdo traduzido armazenado em campos JSONField de traduções.

**Como funciona**:
- O cliente pesquisa em espanhol: "zapatos"
- O sistema pesquisa as traduções dos nomes dos produtos em espanhol
- Os resultados mostram os nomes dos produtos em espanhol dos dados do JSONField
- Recai no idioma base se a tradução em espanhol estiver faltando

**Desempenho**: Sobrecarga mínima para 1-3 idiomas. Com 5+ idiomas, aumento leve na complexidade da consulta.

## Testando Autocomplete

Depois de configurar as configurações, teste a experiência do autocomplete:

1. **Abra a homepage do seu site** em uma janela incógnita
2. **Clique na caixa de pesquisa** para focá-la
3. **Digite o nome de um produto comum** lentamente (ex: "laptop")
4. **Observe**:
   - Quão rápido os resultados aparecem após você parar de digitar (o debounce está funcionando?)
   - Quais informações são exibidas (miniaturas, preços, SKUs conforme configurado)
   - Se os resultados são relevantes (verifique os pesos de relevância se não forem)
5. **Teste em dispositivos móveis** - Certifique-se de que o dropdown seja amigável para toque e legível

## Dicas

- **Desative descrições de produtos para velocidade** - Descrições aumentam significativamente o tamanho do payload com pouco valor no contexto do autocomplete
- **NUNCA habilite o status do estoque em catálogos grandes** - A agregação de estoque destrói o desempenho do autocomplete
- **Teste em dispositivos móveis com alvos de toque** - Os resultados do autocomplete devem ser facilmente tocáveis em telefones
- **Monitore os tempos de resposta semanalmente** - Alvo: <200ms para solicitações de autocomplete
- **Aumente o TTL do cache se for lento** - Otimização de desempenho mais fácil
- **Contagens de produtos são caras - desative a menos que sejam críticas** - Cada contagem de categoria/marca adiciona 2 consultas a cada solicitação de autocomplete

Lembre-se: Preserve all markdown formatting, image paths, code blocks, and technical terms exactly as shown in the preservation rules.
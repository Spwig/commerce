---
title: Otimização do Desempenho de Pesquisa
---

O desempenho da pesquisa impacta diretamente a experiência do cliente e as conversões. Pesquisas lentas frustram os clientes e aumentam as taxas de saída. Este guia abrangente identifica os gargalos comuns de desempenho no sistema de pesquisa nativo do banco de dados do Spwig, fornece estratégias de otimização e estabelece metas de desempenho. Use este guia quando os tempos de resposta da pesquisa ultrapassarem os limites aceitáveis ou você estiver planejando o crescimento do catálogo.

Tempos de resposta alvo: <200ms para autocompletar, <500ms para pesquisa completa. Siga a lista de verificação de otimização abaixo para atingir essas metas.

## Entendendo Métricas de Desempenho

Monitore essas métricas em **Search > Search Analytics**:

**Response Time** - Milissegundos para executar uma consulta de pesquisa (somente lado do servidor, exclui latência de rede)

**Cache Hit Rate** - Percentual de pesquisas servidas do cache versus banco de dados

**Query Count** - Número de consultas do banco de dados por pesquisa (menos é melhor)

**Database Query Time** - Tempo gasto no banco de dados versus código de aplicativo

## Metas de Desempenho

| Tipo de Consulta | Alvo | Aceitável | Requer Otimização |
|------------------|------|-----------|-------------------|
| Autocomplete | <200ms | 200-300ms | >300ms consistentemente |
| Pesquisa Completa | <500ms | 500-800ms | >800ms consistentemente |
| Pesquisa de Admin | <1000ms | 1000-1500ms | >1500ms consistentemente |

Se seus tempos de resposta médios ultrapassarem os limites de "Requer Otimização", implemente as estratégias abaixo.

## Monitoramento de Desempenho

**Média de Tempo de Resposta do Painel de Análise**

Navegue até **Search > Search Analytics** para visualizar o tempo de resposta médio em todas as pesquisas. Este é seu métrica principal de monitoramento de desempenho.

**Quando Investigar**: Tempo de resposta médio >300ms para autocompletar ou >800ms para pesquisa completa consistentemente por vários dias.

**Monitoramento Semanal**: Revise as análises toda segunda-feira para identificar degradação de desempenho cedo.

## Gargalos de Desempenho Conhecidos

A pesquisa nativa do banco de dados do Spwig tem vários gargalos documentados para evitar:

### Cálculo de CTR com N+1 Consultas

**O que é**: O cálculo da taxa de cliques em AnalyticsService executa consultas separadas para cada item de resultado agregado.

**Impacto**: Severo em lojas de alto tráfego com muitas consultas rastreadas.

**Local do Código**: `search/services/analytics_service.py` - método `get_click_through_rate()`

**Mitigação**: Evite chamar cálculos de CTR em produção. Isso é principalmente uma funcionalidade de análise de admin que deve ser calculada assincronamente, não durante solicitações de clientes.

### Agregação de Estoque

**O que é**: `with_stock_totals()` calcula as quantidades disponíveis em todos os armazéns por produto.

**Impacto**: Caro em catálogos >1.000 produtos. Chamado quando o filtro `in_stock` é usado ou o status do estoque é exibido no autocompletar.

**Gatilho**: **Search Settings > Autocomplete** - opção "Show Stock Status"

**Recomendação**: NUNCA habilite o status do estoque no autocompletar em catálogos grandes. Adiciona 200-500ms por solicitação.

### Junções de Variantes

**O que é**: Pesquisas por SKU acionam JOIN na tabela de variantes para pesquisar SKUs de variantes.

**Impacto**: 2-3x mais lento em produtos com muitas variantes (10+ variantes por produto).

**Mitigação**: Usa `.distinct()` para evitar duplicatas, o que adiciona sobrecarga. Necessário para funcionalidade de SKU - não desative a menos que SKUs não sejam usados.

### Contagem de Produtos no Autocompletar

**O que é**: Resultados de autocompletar de categoria/marca mostram contagens de produtos ("Electronics (234)")

**Impacto**: Cada tipo de conteúdo com contagens habilitadas adiciona 2 consultas extras. Consultas incluem junções e agregações.

**Gatilho**: **Search Settings > Autocomplete** - "Show Product Count" para categorias/marcas

**Recomendação**: Desative contagens de produtos. Salva 2-4 consultas por solicitação de autocompletar. Maior otimização de autocompletar.

### Índice de Documentos

**O que é**: Extração de texto de arquivos PDF/DOCX/XLSX durante consultas de pesquisa.

**Impacto**: Muito caro (E/S de arquivo + extração de texto). Operações bloqueantes síncronas.

**Gatilho**: **Search Settings > Deep Indexing** - "Index Documents"

**Recomendação**: Quase nunca vale o custo de desempenho. HABILITE APENAS para catálogos pequenos de produtos digitais (<500 produtos) após testes rigorosos.

## Configuração de Cache

O cache é a otimização de desempenho mais eficaz.

**Cache de Autocompletar** - Padrão: 60s
- **Faixa Recomendada**: 45-90s
- **TTL Mais Alto (90-120s)**: Melhor desempenho se alterações de estoque forem raras
- **TTL Mais Baixo (30-45s)**: Resultados mais recentes se você adicionar produtos com frequência

**Cache de Resultados** - Padrão: 300s (5 minutos)
- **Faixa Recomendada**: 180-600s
- **TTL Mais Alto (600s/10min)**: Melhora significativa no desempenho para catálogos estáticos
- **TTL Mais Baixo (180s)**: Mais recente se atualizações frequentes de dados do produto

**Estratégia de Otimização**: Se as pesquisas forem lentas, dobre o TTL do cache antes de desativar funcionalidades. Ir de 60s → 120s de cache de autocompletar reduz a carga do banco de dados pela metade.

## Lista de Verificação de Otimização de Autocompletar

Aplique essas alterações nas configurações de autocompletar para o máximo de desempenho:

**1. Aumente o Debounce para 300-400ms**
- Local: **Search Settings > Autocomplete** - "Debounce Delay"
- Impacto: Reduz as chamadas de API esperando mais tempo entre teclas pressionadas
- Compromisso: Um pouco menos responsivo (imperceptível para a maioria dos usuários)

**2. Reduza o Max Results de 8 para 5-6**
- Local: **Search Settings > Autocomplete** - "Max Results Per Type"
- Impacto: Resultados menores = consultas mais rápidas e payloads JSON menores
- Compromisso: Menos opções mostradas (geralmente suficiente)

**3. Desative Contagens de Produtos (MAIOR GANHO)**
- Local: **Search Settings > Autocomplete** - Desmarque "Show Product Count" para categorias/marcas
- Impacto: Salva 2-4 consultas por solicitação de autocompletar
- Compromisso: Nenhuma contagem de produtos no dropdown (raramente necessária)

**4. Desative Status de Estoque**
- Local: **Search Settings > Autocomplete** - Desmarque "Show Stock Status"
- Impacto: Elimina a agregação cara de estoque
- Compromisso: Nenhum badge de estoque (não crítico no contexto de autocompletar)

**5. Desative Descrições de Produtos**
- Local: **Search Settings > Autocomplete** - Desmarque "Show Description"
- Impacto: Reduz o processamento de texto e o tamanho do payload
- Compromisso: Menos texto de pré-visualização (nome do produto normalmente suficiente)

**6. Aumente o TTL do Cache para 90s**
- Local: **Search Settings > Caching** - "Autocomplete Cache TTL"
- Impacto: Mais solicitações servidas do cache
- Compromisso: Resultados até 90 segundos desatualizados (aceitável para a maioria das lojas)

**Melhora Esperada**: Aplicar todas as 6 otimizações normalmente reduz o tempo de resposta de autocompletar em 50-70%.

## Otimização de Índice Profundo

Cada opção de índice profundo adiciona sobrecarga. Desative com base no tamanho do catálogo:

| Tamanho do Catálogo | Índice Profundo Recomendado |
|--------------------|-----------------------------|
| **<1.000 produtos** | Todos LIGADOS (impacto mínimo) |
| **1.000-10.000** | Mantenha SKUs, Atributos, Campos Personalizados LIGADOS; Desative Avaliações |
| **10.000-20.000** | Mantenha SKUs, Atributos LIGADOS; Desative Campos Personalizados, Avaliações |
| **20.000-50.000** | Mantenha SKUs LIGADOS apenas; Desative tudo o mais |
| **>50.000** | Mantenha SKUs LIGADOS; Considere migração para Elasticsearch |

**Índice de Documentos**: SEMPRE DESLIGADO, a menos que crítico (produtos digitais com documentos pesquisáveis E <500 produtos no total).

## Otimização de Tipos de Conteúdo

Desative tipos de conteúdo não usados em **Search Settings > Content Types**:

- **Nenhuma blog?** Desative "Blog Posts" - economiza consultas
- **Nenhuma filtragem por marca?** Desative "Brands" - economiza consultas
- **Loja apenas de compras?** Desative "Categories" e "Blog Posts"

Cada tipo de conteúdo desativado remove consultas do banco de dados de cada pesquisa.

## Otimização do Banco de Dados

O Spwig cria índices necessários por meio de migrações. Confie neles - não crie índices adicionais sem perfilar.

**Manutenção do PostgreSQL** (se usando PostgreSQL):
- Execute `VACUUM ANALYZE` semanalmente para atualizar estatísticas do planejador de consultas
- Catálogos grandes beneficiam-se de `VACUUM FULL` mensal (requer tempo de inatividade)

**Monitore o Tempo de Consulta do Banco de Dados**: Durante o desenvolvimento, identifique consultas lentas usando ferramentas de perfilamento. A maioria da otimização de consulta já foi implementada:
- `.select_related('brand', 'category')` em produtos
- `.prefetch_related('images')` para miniaturas
- `.distinct()` para pesquisas de variantes

## Desempenho de Correspondência Fuzzy

A distância de Levenshtein é computacionalmente cara (complexidade O(m*n)):

**Otimização do Limiar**:
- **Limiar mais alto (0,85 vs 0,80)**: Mais rápido, mas captura menos erros de digitação
- **Limiar mais baixo (0,75 vs 0,80)**: Mais lento, mas mais tolerante

**Otimização do Máximo de Edições**:
- **Menor máximo de edições (1 vs 2)**: Mais rápido, mas perde mais erros de digitação
- **Maior máximo de edições (2 vs 3)**: Mais lento, mas captura mais erros de digitação

**Desempenho da Biblioteca**: O Spwig usa `rapidfuzz` se disponível (10x mais rápido que Python puro). Certifique-se de que ele está instalado: `pip install rapidfuzz`

## Desempenho de Sinônimos e Redirecionamentos

**Expansão de Consulta de Sinônimos**: Cada sinônimo adiciona cláusulas OR à consulta de pesquisa. Limite a 10-20 sinônimos por termo máximo.

**Tipo de Correspondência Regex**: Redirecionamentos regex são mais lentos que exato/contém/inicia com. Evite padrões complexos.

**Recomendação**: Use tipos de correspondência simples sempre que possível. Reserve regex para casos em que outros tipos de correspondência não funcionam.

## Otimização para Catálogos Grandes (>10.000 produtos)

Estratégias específicas para catálogos grandes:

**1. Caching Agressivo**
- Autocomplete: TTL de 90-120s
- Resultados: TTL de 600s (10min)
- Aceite desatualização para desempenho

**2. Índice Profundo Mínimo**
- Apenas SKUs (desative atributos, campos personalizados, avaliações)
- Teste o desempenho com e sem atributos

**3. Resultados de Autocomplete Reduzidos**
- Máximo 5 resultados por tipo (abaixo de 8)
- Reduz sobrecarga de consulta

**4. Desative Status de Estoque em Todos os Lados**
- No autocomplete
- Nos resultados de pesquisa se exibido

**5. Considere Elasticsearch com >50K Produtos**
- Pesquisa nativa do banco de dados adequada até ~50.000 produtos
- Além disso, Elasticsearch recomendado para:
  - Pesquisa facetada complexa
  - Carga de pesquisa concorrente alta (>100 pesquisas/seg)
  - Tempos de resposta consistentemente >500ms mesmo com otimização

## Desempenho Multilíngue

O índice JSONField JSONB (PostgreSQL) torna o multilíngue eficiente:

- **1-3 idiomas**: Sobrecarga mínima (5-10ms)
- **5+ idiomas**: Aumento mínimo na complexidade da consulta (20-40ms)
- **10+ idiomas**: Sobrecarga notável (50-100ms)

A sobrecarga aumenta linearmente com o número de idiomas.

## Correções de Desempenho de Emergência

Se as pesquisas forem criticamente lentas (>2s de tempos de resposta), aplique essas correções imediatas na ordem:

**Imediato** (aplique agora):
1. Desative o índice de documentos
2. Desative contagens de produtos no autocompletar
3. Aumente os TTLs do cache para 120s de autocompletar / 600s de resultados

**Rápido** (aplique dentro de 24 horas):
4. Desative o status de estoque no autocompletar
5. Reduza o máximo de resultados do autocompletar para 5
6. Desative descrições de produtos no autocompletar

**Médio** (aplique dentro de uma semana):
7. Desative o índice de avaliações se >20K produtos
8. Revise e desative tipos de conteúdo não usados
9. Aumente o debounce para 400ms

**Melhora Esperada**: Essas 9 correções normalmente reduzem os tempos de resposta em 60-80% em catálogos grandes.

## Dicas

- **Monitore os tempos de resposta semanalmente** - Identifique degradação de desempenho cedo
- **Aumentos de cache são a primeira otimização** - Dobrar o TTL do cache é o maior ganho fácil
- **Contagens de produtos no autocompletar = cara** - Maior assassino de desempenho de autocompletar
- **Índice de documentos quase nunca vale a pena** - Custo de desempenho raramente justifica o benefício
- **Teste uma alteração de cada vez** - Não é possível identificar causa/efeito com alterações simultâneas
- **Benchmark com volumes de dados realistas** - Teste com catálogos de tamanho de produção
- **Agregação de estoque mata o desempenho em catálogos grandes** - Evite exibir estoque no autocompletar
- **Considere Elasticsearch com 50K+ produtos** - Pesquisa nativa do banco de dados tem limites

Lembre-se: preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos exatamente conforme mostrado nas regras de preservação.
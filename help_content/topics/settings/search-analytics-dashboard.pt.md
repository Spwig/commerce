---
title: Painel de Análise de Pesquisa
---

O painel de análise de pesquisa rastreia todas as consultas de pesquisa em sua loja, fornecendo insights sobre o que os clientes pesquisam, quais pesquisas têm sucesso ou falham e quão rápido seu sistema de pesquisa responde. Use esses dados para identificar produtos populares, descobrir faltas de estoque, criar sinônimos e otimizar o desempenho da pesquisa.

O rastreamento de análise deve estar ativado em **Configurações de Pesquisa > aba de Análise** para que os dados sejam exibidos.

![Painel de Análise](/static/core/admin/img/help/search-analytics-dashboard/analytics-dashboard.webp)

## Visão Geral do Painel

Navegue até **Pesquisa > Análise de Pesquisa** para acessar o painel. A página mostra:

**Cartões de Estatísticas** - Métricas rápidas para hoje e a semana passada:
- Total de pesquisas hoje
- Total de pesquisas esta semana
- Consultas com zero resultados (pesquisas que retornam nenhum produto)
- Tempo médio de resposta em milissegundos

**Tabela das Principais Consultas** - Termos de pesquisa mais frequentes com contagens de resultados

**Consultas com Zero Resultados** - Pesquisas que retornaram nenhum resultado (crítico para melhorias)

**Lista de Consultas** - Todos os registros de pesquisa individuais com filtros

## Estatísticas do Dia

**Total de Pesquisas Hoje** - Contagem de todas as solicitações de pesquisa desde a meia-noite no fuso horário da sua loja. Inclui tanto as solicitações de autocomplete quanto as de páginas de pesquisa completas.

**Consultas Únicas Hoje** - Contagem de termos de pesquisa distintos usados hoje. Se 5 clientes pesquisarem "notebook", isso conta como 1 consulta única apesar de 5 pesquisas totais.

**Zero Resultados Hoje** - Pesquisas hoje que retornaram nenhum produto. Altas contagens de zero resultados indicam produtos ausentes ou cobertura insuficiente de sinônimos.

Atualizações de dados em tempo real conforme as pesquisas ocorrem.

## Estatísticas Semanais

**Total da Semana** - Total de pesquisas nas últimas 7 dias

**Consultas Únicas** - Termos de pesquisa distintos usados nesta semana

**Crescimento Semanal** - Percentual de mudança em relação à semana anterior (se exibido)

Use os dados semanais para identificar tendências: aumento no volume de pesquisa geralmente está correlacionado com crescimento no tráfego ou campanhas de marketing.

## Tempo Médio de Resposta

⚠️ **MONITORAMENTO DE DESEMPENHO**

Tempo médio (em milissegundos) para executar consultas de pesquisa. Metas para tempo de resposta:

| Tipo de Consulta | Meta | Limiar de Alerta |
|------------------|------|------------------|
| Autocomplete     | < 200ms | > 300ms consistentemente |
| Pesquisa Completa | < 500ms | > 800ms consistentemente |

Se o tempo médio de resposta ultrapassar os limites de alerta:
1. Verifique **Configurações de Pesquisa > aba de Caching** - aumente os TTLs de cache
2. Revise **aba de Indexação Profunda** - desative funcionalidades caras (indexação de documentos, indexação de avaliações em catálogos grandes)
3. Veja o guia [Otimização do Desempenho da Pesquisa](/en/admin/help/search-performance-optimization/)

## Principais Consultas

A tabela das principais consultas mostra os termos de pesquisa mais frequentes:

**Use esses dados para**:
- **Destacar produtos populares** - Se "fones de ouvido sem fio" for uma consulta principal, destaque esses produtos em destaque em sua homepage
- **Decisões de estoque** - Volume alto de pesquisa em uma categoria indica demanda
- **Identificar tendências** - Pesquisas sazonais revelam o que está popular no momento
- **Criação de conteúdo** - Escreva posts de blog ou guias sobre temas frequentemente pesquisados

Revise as principais consultas mensalmente para alinhar seu merchandising com os interesses dos clientes.

## Consultas com Zero Resultados

**CRÍTICO PARA MELHORIAS** - Consultas com zero resultados são uma mina de ouro para otimizar sua loja.

Consultas com zero resultados ocorrem por três razões principais:

### 1. Produtos Ausentes

Clientes pesquisam por produtos que você não vende.

**Exemplo**: Pesquisas repetidas por "mats de ioga" mas você vende apenas equipamentos de fitness, não suprimentos de ioga.

**Ação**: Considere adicionar esses produtos ao seu catálogo se as pesquisas forem frequentes.

### 2. Sinônimos Ausentes

Clientes usam termos que não correspondem às descrições dos seus produtos.

**Exemplo**: Clientes pesquisam "laptop" mas seus produtos dizem todos "computador portátil".

**Ação**: Crie mapeamento de sinônimos associando termos dos clientes ao seu idioma de produto. Veja [Gerenciamento de Sinônimos e Redirecionamentos](/en/admin/help/managing-synonyms-redirects/).

### 3. Correspondência Fuzzy Pobre

Erros de digitação ou erros de ortografia não correspondem mesmo com a pesquisa fuzzy habilitada.

**Exemplo**: A pesquisa "accomodate" não encontra produtos "accommodate".

**Ação**:
- Reduza o limiar de similaridade em **Configurações de Pesquisa > aba de Correspondência Fuzzy** (de 0,80 para 0,75)
- Adicione sinônimos unidirecionais para erros de ortografia comuns

**Fluxo de Trabalho Semanal**:
1. Revise consultas com zero resultados toda segunda-feira
2. Classifique: Produtos ausentes, sinônimos ausentes ou erros de ortografia
3. Adicione sinônimos para termos frequentemente pesquisados
4. Anote lacunas de produtos para planejamento de estoque

## Detalhes da Consulta

Clique em qualquer consulta na lista para ver os detalhes completos:

**Campos Rastreados**:
- **Texto da consulta** - O que o cliente pesquisou
- **Carimbo de data/hora** - Quando a pesquisa ocorreu
- **Contagem de resultados** - Quantos resultados foram retornados
- **Tempo de resposta** - Milissegundos para executar (monitoramento de desempenho)
- **Usuário** - Cliente conectado (se o rastreamento de usuários estiver ativado)
- **ID da Sessão** - Identificador de sessão anônimo
- **Idioma** - Idioma da loja durante a pesquisa
- **Motor** - Qual motor de pesquisa processou a consulta

## Filtros e Pesquisa

Use filtros para analisar segmentos específicos:

**Hierarquia de Data** - Filtre por data, mês ou ano

**Filtro de Idioma** - Veja pesquisas por idioma (útil para lojas multilíngues)

**Filtro de Motor** - Compare o comportamento de pesquisa entre diferentes motores

**Comutador de Zero Resultados** - Mostre apenas consultas que retornaram nenhum resultado

**Caixa de Pesquisa** - Encontre texto de consulta específico

## Exportando Dados

Clique em **Exportar** para baixar os dados da consulta como CSV para análise mais profunda no Excel ou em ferramentas de dados.

**O CSV inclui**:
- Todos os textos de consulta
- Carimbos de data/hora
- Contagens de resultados
- Tempos de resposta
- Dados de idioma e motor

Use as exportações para:
- Análise de tendências ao longo do tempo
- Identificar padrões de pesquisa sazonais
- Auditoria de desempenho
- Apresentação para partes interessadas

## Considerações sobre Privacidade

O rastreamento de análise de pesquisa respeita a privacidade:

**Rastreamento de Usuário** (opcional) - Liga pesquisas a contas de clientes conectados. Desative para conformidade com GDPR/CCPA em **Configurações de Pesquisa > aba de Análise**.

**Rastreamento de Sessão** (padrão) - Usa IDs de sessão anônimos para rastrear padrões de pesquisa sem identificar clientes. Amigável à privacidade.

**Retenção de Dados** - Consultas de pesquisa permanecem no banco de dados indefinidamente. Implemente uma política de retenção personalizada se necessário para conformidade.

## Usando Análises para Melhorar a Pesquisa

Insights açõesáveis das análises de pesquisa:

**Tarefas Semanais**:
- Revise zero-resultados e adicione sinônimos para termos comuns
- Monitore tempos de resposta e otimize se consistentemente lento
- Identifique as principais pesquisas e garanta que esses produtos estejam bem estocados

**Tarefas Mensais**:
- Analise as principais consultas para informar a seleção de produtos
- Exporte dados para identificar tendências sazonais
- Revise padrões de pesquisa específicos de idioma
- Rastreie contagens de cliques em redirecionamentos para otimizar atalhos de navegação

**Tarefas Trimestrais**:
- Auditoria da eficácia dos sinônimos (os zero-resultados diminuíram?)
- Compare o crescimento do volume de pesquisa com o tráfego geral
- Teste A/B alterações de peso e meça a relevância dos resultados
- Revise se novas categorias de produtos devem ser adicionadas com base na demanda de pesquisa

## Dicas

- **Consultas com zero resultados são minas de ouro para melhorias** - Elas dizem diretamente o que os clientes querem que você não fornece
- **Revise as análises às segundas-feiras de manhã** - Comece sua semana otimizando com base nos dados da semana anterior
- **Tempo de resposta >300ms consistentemente = investigue** - Verifique as configurações de cache primeiro, depois as funcionalidades de indexação profunda
- **Exporte CSV para análise de tendências** - A análise em planilhas revela padrões não óbvios na interface de administração
- **Crie sinônimos antes de adicionar produtos** - Se os clientes pesquisarem por "cases para tablet" mas você os chama de "capas protetoras", adicione o sinônimo primeiro
- **Rastreie padrões de pesquisa sazonais** - "Botas de inverno" em outubro, "biquíni" em março - estoque conforme necessário
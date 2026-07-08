---
title: Análise de Visitantes
---

A Análise de Visitantes fornece uma visão clara de como os clientes estão se movendo pela sua loja. Você pode ver quais páginas atraem mais visitas, como o tráfego geral se comporta ao longo do tempo, quais dispositivos seus clientes usam e como os visitantes novos versus os retornantes se comparam — tudo isso sem a necessidade de ferramentas de análise externas.

## Visão geral das telas de análise

Sua loja rastreia a atividade dos visitantes automaticamente uma vez que o sistema GeoIP estiver ativo. Os dados são organizados em três visões, cada uma oferecendo um nível diferente de detalhe.

### Resumo do tráfego diário

Navegue até **Clientes > Estatísticas de Tráfego Diário** para ver o tráfego geral da sua loja para cada dia. Cada linha representa um dia do calendário e mostra:

| Coluna | O que isso lhe diz |
|--------|-------------------|
| **Data** | O dia em que o tráfego foi registrado |
| **Total de Visualizações** | Todas as visualizações de páginas, incluindo bots |
| **Visitantes Únicos** | Visitantes distintos (por sessão) |
| **Visualizações de Bots** | Visualizações de crawlers e ferramentas automatizadas |
| **Novos Visitantes** | Sessões sem histórico anterior |
| **Visitantes Retornantes** | Sessões de visitantes vistos anteriormente |
| **Visualizações de Desktop** | Visualizações de navegadores de desktop |
| **Visualizações de Mobile** | Visualizações de dispositivos móveis |
| **Visualizações de Tablet** | Visualizações de dispositivos de tablet |

Use a navegação hierárquica de data no topo da lista para pular rapidamente para um mês ou ano específico. Os totais são atualizados diariamente por meio de um processo de fundo automatizado, então os dados do dia atual aparecerão no dia seguinte pela manhã.

### Estatísticas por página

Navegue até **Clientes > Estatísticas de Página Diária** para ver o tráfego dividido por página individual. Cada linha mostra um caminho de URL em um dia, então você pode comparar o desempenho de páginas específicas ao longo do tempo.

| Coluna | O que isso lhe diz |
|--------|-------------------|
| **Data** | O dia em que essas estatísticas se aplicam |
| **Caminho da URL** | O caminho da página normalizado (ex: `/products/blue-widget`) |
| **Visualizações** | Total de visualizações dessa página naquele dia |
| **Visitantes Únicos** | Visitantes distintos que visualizaram essa página |
| **Visualizações de Bots** | Visualizações de bots nessa página |
| **Entradas** | Quantas sessões começaram nesta página (ela foi a página de destino) |

Use a caixa de pesquisa **Caminho da URL** para encontrar estatísticas para uma página específica. Por exemplo, procure por `/products/` para ver todo o tráfego de páginas de produtos, ou procure por um slug de produto específico para se concentrar em um item.

### Eventos de visualização de páginas individuais

Navegue até **Clientes > Visualizações de Páginas** para ver um registro bruto de todas as navegações de páginas rastreadas. Este é um registro somente leitura — você não pode adicionar ou editar entradas. Use-o para investigar sessões específicas ou para verificar se o rastreamento está registrando corretamente.

Cada registro mostra:
- **Caminho da URL** — a página que foi visitada
- **Sessão** — um identificador curto para a sessão do visitante
- **Fonte** — se a visita veio do frontend sem cabeça ou da loja virtual padrão
- **É Bot** — se o visitante foi identificado como tráfego automatizado
- **É Página de Entrada** — se esta foi a primeira página em sua sessão
- **Marcação de Tempo** — o horário exato da visita

Você pode filtrar por **É Bot**, **Fonte** e **É Página de Entrada** usando os filtros da barra lateral, e navegar por data usando a hierarquia de data no topo.

## Lendo tendências de tráfego

O resumo do tráfego diário é sua melhor ferramenta para identificar tendências. Procure por padrões como:

- **Picos de tráfego** após executar uma promoção ou enviar um e-mail de marketing
- **Crescimento gradual** ao longo de semanas e meses à medida que sua loja ganha visibilidade orgânica
- **Padrões de fim de semana vs. dias úteis** para entender quando seus clientes estão mais ativos
- **Divisão entre mobile e desktop** para decidir se deve priorizar mudanças no design otimizado para mobile

As colunas **Novos Visitantes** e **Visitantes Retornantes** juntas lhe dizem como bem você está retenendo clientes. Uma loja saudável geralmente vê uma mistura de ambos — uma proporção alta de novos visitantes sugere forte aquisição, enquanto uma proporção maior de visitantes retornantes sugere que a fidelização dos clientes está se formando.

A visão de estatísticas por página, classificada por visualizações em ordem decrescente (o padrão), mostra imediatamente quais páginas geram mais tráfego em qualquer dia específico.

Procure por:

- **Páginas com alto tráfego de entrada e baixo número de visualizações** — páginas que atraem visitantes de busca ou anúncios, mas podem não manter o interesse
- **Páginas com alto número de visualizações e muitos visitantes únicos** — páginas populares que valem a pena manter atualizadas
- **Páginas de produtos com contagem crescente de visualizações** — produtos que podem estar ganhando visibilidade nos resultados de busca

### Exemplo: encontrar o tráfego de um produto

Para verificar quanto tráfego seu produto mais vendido recebeu na semana passada:

1. Navegue até **Clientes > Estatísticas de Páginas Diárias**
2. Use a hierarquia de datas para selecionar a semana relevante
3. Na caixa de pesquisa, insira o slug da URL do produto (ex.: `/blue-widget`)
4. Revise as **Visualizações**, **Visitantes Únicos** e **Entradas** ao longo dos dias mostrados

## Dados de localização dos visitantes

Navegue até **Clientes > Localizações dos Visitantes** para ver uma visão no nível de sessão de onde seus visitantes estão localizados. Cada registro representa uma sessão de visitante e inclui:

- País e cidade (resolvidos automaticamente pelo sistema GeoIP)
- Tipo de dispositivo (desktop, mobile, tablet)
- Preferências de moeda e idioma selecionadas pelo visitante
- Atribuição de campanha UTM (fonte, meio, nome da campanha)
- Indicadores de tráfego de bots e de administradores

Você pode filtrar visitantes por país, tipo de dispositivo, fonte UTM e se eles eram bots ou membros da equipe de administração. Use o filtro **É Bot** definido como falso para se concentrar no tráfego real de clientes, e o filtro **É Tráfego de Admin** para excluir suas próprias sessões de testes da análise.

## Dicas

- As visualizações de bots são rastreadas separadamente e excluídas automaticamente das contagens de visitantes únicos — suas estatísticas de tráfego refletem a atividade real dos clientes
- A coluna **Entradas** nas estatísticas por página informa quais páginas atuam como a porta de entrada do seu loja a partir de buscas e anúncios; otimizar essas páginas tem o maior impacto
- Filtrar localizações de visitantes por **Fonte UTM** ajuda a medir quanto tráfego um canal de marketing específico (ex.: um boletim informativo por e-mail ou um anúncio do Google) está realmente enviando
- As estatísticas diárias são agregadas durante a noite — se você precisar verificar o tráfego do mesmo dia, use diretamente o log de Visualizações de Páginas
- A divisão por dispositivo no resumo diário ajuda você a priorizar o trabalho de design; se mais da metade de suas visitas forem de dispositivos móveis, certifique-se de que suas páginas de produtos e checkout pareçam ótimas em telas pequenas
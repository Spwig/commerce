---
title: Exemplos de Promoções
---

Este guia mostra exemplos concretos de como configurar diferentes tipos de promoções. Cada exemplo inclui os valores exatos dos campos a serem inseridos no assistente de promoções, para que você possa seguir ou adaptar para sua loja.

![Cartão de Promoção](/static/core/admin/img/help/promotion-examples/promotion-card.webp)

## Exemplo: Percentual de Desconto em uma Categoria

**Cenário:** 30% de desconto em todos os calçados para a liquidação de inverno.

Navegue até **Marketing > Vendas & Promoções** e clique em **+ Criar Promoção**. Insira os seguintes valores em cada etapa do assistente:

| Etapa | Campo | Valor |
|-------|-------|-------|
| Básicos | Nome | Liquidação de Inverno — 30% de Desconto em Calçados |
| Básicos | Descrição | Liquidação de fim de temporada para todos os calçados |
| Básicos | Ativo | Marcado |
| Desconto | Tipo | Percentual de Desconto |
| Desconto | Valor | 30 |
| Agendamento | Data de Início | 15 de jan de 2026 |
| Agendamento | Data de Fim | 28 de fev de 2026 |
| Produtos | Aplicar a | Categorias |
| Produtos | Selecionado | Calçados, Botas, Sandálias |

Isso cria uma venda limitada por tempo que desconta automaticamente cada produto nas categorias selecionadas. Um par de botas de $120 se torna $84, e um par de sandálias de $60 se torna $42.

## Exemplo: Valor Fixo de Desconto em uma Coleção

**Cenário:** $15 de desconto em itens da coleção Essentials de Verão.

| Etapa | Campo | Valor |
|-------|-------|-------|
| Básicos | Nome | Essentials de Verão — $15 de Desconto |
| Básicos | Ativo | Marcado |
| Desconto | Tipo | Valor de Desconto Fixo |
| Desconto | Valor | 15,00 |
| Agendamento | Data de Início | 1º de jun de 2026 |
| Agendamento | Data de Fim | (vazio — sem expiração) |
| Produtos | Aplicar a | Coleções |
| Produtos | Selecionado | Essentials de Verão |

> **Nota:** O desconto de $15 se aplica a cada produto elegível individualmente. Um produto de $50 se torna $35, um produto de $30 se torna $15. Deixar a Data de Fim vazia significa que a promoção funcionará indefinidamente até que você a desative manualmente.

## Exemplo: Preço Fixo de Venda para Liquidação

**Cenário:** Defina todos os itens de liquidação para $9,99.

| Etapa | Campo | Valor |
|-------|-------|-------|
| Básicos | Nome | Liquidação Final — Tudo a $9,99 |
| Básicos | Ativo | Marcado |
| Desconto | Tipo | Preço de Venda Fixo |
| Desconto | Valor | 9,99 |
| Agendamento | Data de Início | (hoje) |
| Produtos | Aplicar a | Coleções |
| Produtos | Selecionado | Liquidação Final |

> **Nota:** O Preço de Venda Fixo define o preço exato de venda, independentemente do preço original. Um item de $75 e um item de $25 tornam-se ambos $9,99. Use isso para prateleiras de liquidação ou precificação uniforme, onde deseja que todos os itens tenham o mesmo ponto de preço.

![Promoção por Categoria](/static/core/admin/img/help/promotion-examples/category-promotion.webp)

## Escolhendo o Tipo de Desconto Adequado

| Tipo | Como Funciona | Melhor Para | Exemplo |
|------|-------------|----------|---------|
| **Percentual de Desconto** | Reduz o preço por percentual | Vendas amplas onde os produtos têm preços variados | 20% de desconto — $100 se torna $80, $50 se torna $40 |
| **Valor de Desconto Fixo** | Subtrai um valor fixo em dólares | Promoções com uma mensagem de economia específica em dólares | $15 de desconto — $100 se torna $85, $50 se torna $35 |
| **Preço de Venda Fixo** | Define o preço exato de venda | Liquidações, precificação uniforme, "tudo a $X" | $9,99 — todos os itens se tornam $9,99, independentemente do preço original |

## Escolhendo o Alvo Adequado

| Alvo | Como Funciona | Melhor Para |
|--------|-------------|----------|
| **Todos os Produtos** | Aplica a todos os produtos da sua loja | Vendas em toda a loja, eventos em toda a loja |
| **Categorias** | Aplica a todos os produtos nas categorias selecionadas | Vendas por departamento, liquidações sazonais por tipo |
| **Marcas** | Aplica a todos os produtos das marcas selecionadas | Parcerias com marcas, eventos específicos de marca |
| **Coleções** | Aplica a todos os produtos nas coleções selecionadas | Promoções curadas, vendas temáticas |
| **Produtos** | Aplica a produtos selecionados individualmente | Ofertas selecionadas à mão, seleções limitadas |

## Padrões de Agendamento

Três padrões comuns para configurar agendamentos de promoções:

| Padrão | Data de Início | Data de Fim | Caso de Uso |
|---------|-----------|----------|----------|
| **Imediato e contínuo** | Hoje | (vazio) | Reduções de preço permanentes, vendas de longo prazo |
| **Intervalo de data** | Data futura | Data futura | Eventos sazonais, vendas de feriados |
| **Início futuro, sem fim** | Data futura | (vazio) | Novas precificações permanentes que começam em uma data específica |

Definir uma Data de Início no futuro cria uma promoção agendada. Ela aparecerá na guia **Agendada** no painel de promoções e será ativada automaticamente quando a data chegar. Deixar a Data de Fim vazia significa que a promoção permanece ativa até que você a desative manualmente.

## Dicas

- **Use nomes descritivos** — Inclua o valor do desconto e o alvo no nome (ex: "Verão 20% de Desconto em Calçados") para que você possa identificar rapidamente as promoções no painel.
- **Verifique a quantidade de produtos afetados** — A etapa Revisão mostra quantos produtos serão descontados. Se o número parecer errado, volte e verifique seu alvo.
- **Comece com algo pequeno** — Se você tiver dúvidas sobre um desconto, comece com um percentual menor e aumente-o se necessário.
- **Use Valor de Desconto Fixo para marketing** — "$15 de desconto" é uma economia concreta que é fácil de comunicar em anúncios e campanhas de e-mail.
- **Use Percentual de Desconto para justiça** — Um desconto percentual se ajusta com o preço, oferecendo economias proporcionais em diferentes pontos de preço.
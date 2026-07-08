---
title: Gerenciamento de Sinônimos e Redirecionamentos
---

Sinônimos e redirecionamentos tornam sua busca mais inteligente ao lidar com termos equivalentes e rotear consultas específicas para páginas específicas. Sinônimos expandem as buscas para incluir termos relacionados ("laptop" também encontra "notebook"), enquanto redirecionamentos enviam consultas como "sale" diretamente para sua página de vendas. Este guia explica como criar e gerenciar ambas as funcionalidades para melhorar a relevância da busca e a experiência do cliente.

Use sinônimos para equivalência de termos e redirecionamentos para atalhos de navegação.

![Lista de Sinônimos](/static/core/admin/img/help/managing-synonyms-redirects/synonym-list.webp)

## Entendendo Sinônimos

Sinônimos informam ao sistema de busca que certos termos devem ser tratados como equivalentes. Quando um cliente busca por um termo, o sistema inclui automaticamente resultados correspondentes aos termos de sinônimo.

**Exemplo**: Crie um mapeamento de sinônimos "laptop" → "notebook", "portable computer". Agora, quando alguém busca "laptop", ele também obtém resultados para produtos que contêm "notebook" ou "portable computer" em seus nomes ou descrições.

Sinônimos são especialmente valiosos para:
- Inglês britânico vs. americano (jumper/sweater, trainers/sneakers)
- Termos de marca vs. termos genéricos (tissues/Kleenex)
- Erros comuns de digitação (accommodate/accomodate)
- Jargões do setor vs. linguagem comum (CPU/processor)

## Criando Sinônimos

Navegue até **Search > Synonyms** e clique em **+ Adicionar Sinônimo**.

![Formulário de Adicionar Sinônimo](/static/core/admin/img/help/managing-synonyms-redirects/synonym-form.webp)

**Term** - O termo original de busca que aciona a expansão de sinônimos

**Sinônimos** - Array JSON de termos equivalentes, por exemplo `['sweater', 'pullover', 'jumper']`

**Bidirecional** - Padrão: Marque. Quando ativado, as relações de sinônimos funcionam em ambas as direções:
- Buscar "laptop" encontra produtos "notebook"
- Buscar "notebook" encontra produtos "laptop"

Desmarque para mapeamentos unidirecionais (veja abaixo).

**Idioma** - Opcional. Restrinja este sinônimo a buscas em um idioma específico. Deixe em branco para aplicar a todos os idiomas.

**Motor** - Opcional. Restrinja este sinônimo a um motor de busca específico. Deixe em branco para aplicar globalmente.

**Ativo** - Se este sinônimo está atualmente em uso. Desmarque para desativar temporariamente sem excluir.

## Exemplos Bidirecionais

A maioria dos sinônimos deve ser bidirecional - verdadeiros equivalentes que funcionam em ambas as direções:

| Term | Sinônimos | Caso de Uso |
|------|----------|----------|
| laptop | notebook, portable computer | Inglês britânico/estadunidense + termos genéricos |
| sofa | couch, settee | Variações regionais |
| trainers | sneakers, running shoes | Inglês do Reino Unido/Estados Unidos |
| mobile | cell phone, cellular | Variações internacionais |

Com o bidirecional ativado, todos esses termos encontram os mesmos produtos independentemente de qual termo o cliente usar.

## Exemplos Unidirecionais

Desmarque "Bidirecional" para relações unidirecionais:

**Casos de Uso Comuns**:
- **Erros de digitação**: Termo: "acco

mmodate" → Sinônimos: `['accommodate']` (unidirecional, então a forma correta não encontra o erro de digitação)
- **Específico → Genérico**: Termo: "MacBook" → Sinônimos: `['laptop']` (MacBooks são laptops, mas nem todos os laptops são MacBooks)
- **Abreviações**: Termo: "CPU" → Sinônimos: `['processor']` (CPU encontra produtos de processador, mas buscas por processador não devem sempre incluir CPU)

## Sinônimos Específicos de Idioma

Use o campo de idioma para criar sinônimos apropriados para a região:

**Exemplo**: Loja em Inglês Britânico
- Termo: "jumper", Sinônimos: `['sweater', 'pullover']`, Idioma: Inglês (Reino Unido)
- Termo: "trainers", Sinônimos: `['sneakers']`, Idioma: Inglês (Reino Unido)

**Exemplo**: Loja multilingue
- Termo: "ordinateur portable", Sinônimos: `['laptop', 'notebook']`, Idioma: Francês
- Termo: "zapatos", Sinônimos: `['shoes']`, Idioma: Espanhol

Sinônimos específicos de idioma só se aplicam quando um cliente está navegando em esse idioma.

## Sinônimos Específicos de Motor

A maioria dos sinônimos deve se aplicar globalmente (deixe o campo do motor em branco). Use sinônimos específicos de motor apenas quando diferentes contextos de busca precisam de diferentes mapeamentos de termos:

**Exemplo**: Você tem motores separados para "shop" e "blog"
- Sinônimo do blog: Termo: "tutorial" → Sinônimos: `['guide', 'how-to']`, Motor: blog
- Este sinônimo se aplica apenas a buscas no blog, não em buscas de produtos

## Entendendo Redirecionamentos

Redirecionamentos de busca enviam consultas específicas diretamente para páginas designadas, ignorando os resultados de busca normais. Use redirecionamentos quando souber exatamente para onde o cliente deve ir.

**Exemplo**: Crie um redirecionamento para "sale" → "/products/sale/". Agora, quando alguém busca "sale", ele pula os resultados de busca e chega diretamente em sua página de vendas.

Redirecionamentos são ideais para:
- Atalhos de navegação comuns ("returns" → página de política de devoluções)
- Promoções sazonais ("summer sale" → coleção de verão)
- Categorias populares ("laptops" → página da categoria de laptops)
- Páginas de política ("shipping" → informações de envio)

![Lista de Redirecionamentos](/static/core/admin/img/help/managing-synonyms-redirects/redirect-list.webp)

## Tipos de Correspondência

Redirecionamentos suportam quatro tipos de correspondência que controlam quão estritamente a consulta de busca deve corresponder:

**Exata** - Correspondência exata insensível a maiúsculas e minúsculas. A consulta deve corresponder exatamente ao termo (ignorando a capitalização).
- Termo: "sale"
- Correspondências: "sale", "SALE", "Sale"
- Não corresponde: "summer sale", "on sale"

**Contém** - A consulta contém o termo em qualquer lugar.
- Termo: "sizing"
- Correspondências: "sizing guide", "help with sizing", "what sizing"
- Não corresponde: "size chart" (palavra diferente)

**Começa com** - A consulta começa com o termo.
- Termo: "return"
- Correspondências: "returns", "return policy", "returning items"
- Não corresponde: "how to return" (não começa com o termo)

**Regex** - Correspondência de padrão usando expressões regulares. **⚠️ Cuidado com o desempenho** - padrões regex complexos desaceleram as buscas. Use com parcimônia.
- Padrão: `^(laptop|notebook)s?$`
- Correspondências: "laptop", "laptops", "notebook", "notebooks"
- Use apenas se outros tipos de correspondência não funcionarem

## Criando Redirecionamentos

Navegue até **Search > Redirects** e clique em **+ Adicionar Redirecionamento**.

![Formulário de Adicionar Redirecionamento](/static/core/admin/img/help/managing-synonyms-redirects/redirect-form.webp)

**Term** - A consulta de busca a ser correspondida

**Tipo de Correspondência** - Exata, Contém, Começa com ou Regex (veja acima)

**URL de Redirecionamento** - Para onde enviar o cliente. Pode ser relativo (`/products/sale/`) ou absoluto (`https://example.com/page/`)

**Tipo de Redirecionamento** - Código de status HTTP:
- **302 (Temporário)**: Recomendado. O navegador não armazena em cache, você pode mudar o destino depois
- **301 (Permanente)**: O navegador e os motores de busca armazenam em cache. Use apenas para redirecionamentos permanentes

**Motor** - Opcional. Restrinja a um motor de busca específico

**Contagem de Acessos** - Incrementa automaticamente cada vez que este redirecionamento é usado. Ajuda a identificar atalhos de navegação mais usados.

**Ativo** - Ative/desative este redirecionamento

## Exemplos de Redirecionamento

| Term | Tipo de Correspondência | URL | Caso de Uso |
|------|------------------------|-----|----------|
| sale | Exata | `/products/sale/` | Direciona buscas por "sale" para a página de vendas |
| clearance | Exata | `/clearance/` | Pule a busca para itens de liquidação |
| sizing | Contém | `/pages/size-guide/` | Qualquer consulta sobre sizing vai para o guia |
| return | Começa com | `/pages/returns/` | Consultas relacionadas a devoluções vão para a política |

Todos usam redirecionamentos 302 (temporários) para flexibilidade.

## Tipo de Redirecionamento: 302 vs 301

**302 (Temporário)** - Recomendado para a maioria dos redirecionamentos
- O navegador faz uma nova solicitação cada vez
- Você pode mudar a URL de destino a qualquer momento
- Escolha mais segura se você não tiver certeza

**301 (Permanente)** - Use com parcimônia
- O navegador armazena em cache o redirecionamento
- Motores de busca atualizam seus índices
- Mais difícil de mudar depois

**Recomendação**: Use 302, a menos que tenha certeza absoluta de que o redirecionamento nunca mudará.

## Análise da Contagem de Acessos

O campo Contagem de Acessos incrementa automaticamente cada vez que um redirecionamento é acionado. Use isso para:
- Identificar os atalhos de navegação mais usados
- Encontrar redirecionamentos que nunca são usados (considere removê-los)
- Descobrir padrões populares de busca

Revise as contagens de acessos mensalmente para otimizar sua estratégia de redirecionamento.

## Encontrando Oportunidades de Sinônimos

**Use Consultas com Resultados Zerados**: Navegue até **Search > Search Analytics** e filtre por consultas com zero resultados. Essas revelam:
- Termos usados pelos clientes que não correspondem às descrições dos seus produtos
- Variações regionais que você não considerou
- Erros comuns de digitação

**Fluxo de Trabalho**:
1. Revise consultas com zero resultados semanalmente
2. Identifique padrões (mesmos termos aparecendo repetidamente)
3. Adicione sinônimos para mapear a linguagem dos clientes para os nomes dos seus produtos
4. Monitore se as consultas com zero resultados diminuem

## Dicas

- **Monitore consultas com zero resultados semanalmente para ideias de sinônimos** - Elas revelam lacunas entre a linguagem dos clientes e as descrições dos seus produtos
- **Comece com sinônimos comuns, expanda com base nos dados** - Comece com variações regionais óbvias, depois adicione com base no comportamento real de busca
- **Use bidirecional para verdadeiros equivalentes** - A maioria dos sinônimos deve funcionar em ambas as direções (laptop ↔ notebook)
- **Evite padrões regex complexos** - Correspondência com regex é mais lenta do que outros tipos de correspondência; use apenas quando necessário
- **Use redirecionamentos 302 (temporários) por padrão** - Dá flexibilidade para mudar os destinos depois
- **Teste sinônimos com consultas reais** - Busque por termos de sinônimos para verificar se retornam os resultados esperados
- **Sinônimos específicos de idioma para lojas multilingue** - Crie mapeamentos de termos apropriados para cada idioma que você suporta

Lembre-se: preserve todos os formatos markdown, caminhos de imagem, blocos de código e termos técnicos exatamente como mostrado nas regras de preservação.
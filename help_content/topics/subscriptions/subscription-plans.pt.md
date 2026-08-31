---
title: Planos de Assinatura
---

Os planos de assinatura permitem oferecer cobrança recorrente para seus produtos — ideal para consumíveis, serviços, caixas curadas ou qualquer produto que os clientes comprem repetidamente. Este guia explica como criar e configurar planos, definir níveis de preço, adicionar períodos de teste e anexar extras opcionais.

## Primeiros passos

Navegue até **Assinaturas > Planos de Assinatura** na barra lateral de administração. A lista de planos mostra todos os seus planos com seu modelo de preço, número de assinantes ativos e status de visibilidade.

![Lista de planos de assinatura](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Para criar um novo plano, clique no botão **Criar com Assistente** — isso abre o assistente de criação de planos, que o guia passo a passo pela configuração. O botão **+ Adicionar Plano** ao lado abre um formulário em branco para comerciantes que preferem configurar tudo manualmente.

Um plano por si só não é comprável — é um modelo. Depois de construí-lo aqui, anexe-o a um ou mais produtos na aba **Assinaturas** do produto (apenas produtos Simples, Variáveis e Digitais) para que os clientes possam realmente assinar. Veja [Vendendo Produtos como Assinaturas](/help/selling-products-as-subscriptions) para essa etapa.

## O editor de planos

Abrir um plano existente (clique no nome dele, ou no ícone de lápis, a partir da lista) leva você ao editor de planos. O cabeçalho mostra o nome do plano, seu modelo de preço, os selos de status **Ativo**/**Inativo** e **Público**/**Privado**, e a data em que foi criado. Os dois botões no canto superior direito do cabeçalho salvam suas alterações — o ícone de círculo com check salva e retorna à lista, o ícone de check simples salva e mantém você na página para que você possa continuar editando.

Abaixo do cabeçalho, uma faixa de estatísticas resume o plano de relance: **Assinaturas Ativas**, **Níveis de Preço**, **Extras** e **Receita Total**.

O restante do formulário é organizado em cinco abas:

| Aba | O que contém |
|-----|-------------------|
| **Geral** | Informações do Plano (nome, slug, descrição) e Status (ativo/público) |
| **Preços** | Configuração de Preços, Período de Teste e Limites & Restrições |
| **Níveis & Extras** | Os editores de Níveis de Preço e Extras |
| **Ciclo de Vida** | Política de Cancelamento e Comportamento de Mudança de Plano |
| **Avançado** | Integração com Provedor e Estatísticas |

As seções abaixo percorrem as configurações de cada aba. Quando você cria um plano totalmente novo diretamente de **+ Adicionar Plano** (em vez do assistente), os mesmos campos aparecem em um formulário rolável único em vez de abas — salve o plano uma vez e reabra-o para obter o editor completo com abas.

## Informações do plano (aba Geral)

O cartão **Informações do Plano** captura a identidade central do seu plano.

- **Nome do Plano** — O nome que os clientes veem ao assinar. Clique no ícone de globo para adicionar traduções para outros idiomas da loja.
- **Slug** — Um identificador amigável para URL gerado automaticamente a partir do nome (ex.: `premium-plan`). Isso é usado internamente e em integrações.
- **Descrição** — Texto opcional descrevendo o que o plano inclui. Suporta traduções.

O cartão **Status** na mesma aba controla as alternâncias **Ativo** e **Público** — veja [Visibilidade e status](#visibility-and-status) abaixo.

![Aba Geral do editor de planos](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modelo de preço (aba Preços)

O cartão **Configuração de Preços** controla como a precificação é estruturada para este plano:

| Modelo de Preço | Melhor Para |
|---------------|----------|
| **Preço por Nível** | Oferecer opções de compromisso mensal, trimestral e anual com descontos para prazos mais longos |
| **Baseado em Quantidade** | Preço por assento ou por usuário onde o total escala com a quantidade (ex.: licenças de equipe) |
| **Taxa Fixa** | Um único preço fixo sem variações |

Para planos **Baseados em Quantidade**, marque **Permitir Quantidade** e defina a **Quantidade Mínima** (número mínimo de assentos exigidos) e, opcionalmente, uma **Quantidade Máxima** para limitar quantos assentos um assinante pode comprar.

[![](https://dash.spwig.com/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Níveis de preços (aba Níveis & Adicionais)

Os níveis de preços definem a frequência de cobrança e as opções de desconto disponíveis aos clientes neste plano. Adicione-os no cartão **Níveis de Preços** da aba **Níveis & Adicionais**, junto com o editor de Adicionais.

Cada nível possui os seguintes campos:

- **Nome do Nível** — A etiqueta exibida aos clientes (ex.: `Mensal`, `Anual — Ganhe 20%`). Suporta traduções.
- **Ciclo de Cobrança** — Com que frequência o cliente é cobrado: Diariamente, Semanalmente, Mensalmente, Trimestralmente, Semestralmente ou Anualmente.
- **Intervalo de Cobrança** — O multiplicador para o ciclo de cobrança. Defina como `2` com Mensal para cobrar a cada 2 meses.
- **Percentual de Desconto** — O desconto aplicado ao preço do produto para este nível. Defina como `0` para preço cheio, ou `20` para dar 20% de desconto. Este desconto é acumulado sobre qualquer preço de venda no próprio produto.
- **Nível Padrão** — Marque um nível como padrão para selecioná-lo automaticamente para os clientes quando eles visualizarem as opções de assinatura.

O desconto se aplica a partir do primeiro ciclo de cobrança do cliente, não apenas em renovações — um nível com 20% de desconto cobra 20% de desconto desde o primeiro dia (ou do primeiro pagamento após uma tentativa, se o plano tiver uma).

### Exemplo: plano com três opções

Para um plano de assinatura "Clube de Café":

| Nome do Nível | Ciclo de Cobrança | Desconto |
|-----------|---------------|----------|
| Mensal | Mensal | 0% |
| Trimestral — Ganhe 10% | Trimestral | 10% |
| Anual — Ganhe 20% | Anual | 20% |

## Adicionais do plano (aba Níveis & Adicionais)

Adicionais são extras opcionais que os assinantes podem anexar ao seu plano. Adicione-os no cartão **Adicionais**, logo abaixo dos Níveis de Preços na mesma aba:

- **Nome do Adicional** — O nome exibido aos clientes. Suporta traduções.
- **Descrição** — O que o adicional oferece.
- **Preço** — Custo do adicional.
- **Frequência de Cobrança** — Se o adicional é cobrado **Por Ciclo de Cobrança** (recorrente) ou **Único** no início da assinatura.
- **Permitir Quantidade** — Ative para permitir que os clientes comprem múltiplas unidades do adicional.
- **Obrigatório** — Marque esta opção para incluir automaticamente o adicional em todas as novas assinaturas. Adicionais obrigatórios não podem ser removidos pelo cliente.

[![](https://dash.spwig.com/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)](/static/core/admin/img/help/subscription-plans/edit-form-tiers-addons-tab.webp)

## Período de teste (aba Preços)

Um período de teste permite que os clientes experimentem sua assinatura antes da primeira cobrança completa. Configure isso no cartão **Período de Teste**, abaixo de Configurações de Preço:

- **Período de Teste (Dias)** — Número de dias de teste gratuito. Defina como `0` para desativar os testes. O máximo é 365 dias.
- **Preço de Teste** — Preço reduzido opcional durante o teste (ex.: $1 para o primeiro mês). Deixe em branco para um teste totalmente gratuito.

## Limites e restrições (aba Preços)

O cartão **Limites & Restrições**, também na aba Preços, contém:

- **Máximo de Ciclos de Cobrança** — O número total de ciclos de cobrança antes da assinatura terminar automaticamente. Deixe em branco para cobrança recorrente ilimitada. Útil para planos parcelados ou assinaturas com prazo limitado.

**Taxa de Configuração** e **Ordem de Classificação** não fazem parte deste cartão — elas são definidas uma vez, quando você cria o plano pela primeira vez pelo fluxo **Criar com Assistente**, e não podem ser alteradas a partir da tela de edição posteriormente. Se precisar ajustar algum desses valores, desative o plano e o recrie com o assistente, em vez de editá-lo. Observe que as taxas de configuração ainda não são cobradas automaticamente no checkout nesta versão — trate o campo como reservado para uma atualização futura, em vez de uma cobrança funcional.

## Política de Cancelamento (aba Ciclo de Vida)

Controle como os clientes podem cancelar sua assinatura no cartão **Política de Cancelamento**.

| Política | Descrição |
|--------|-------------|
| **Cancelar a Qualquer Momento** | Os clientes podem cancelar imediatamente a qualquer momento |
| **Cancelar no Fim do Período** | O cancelamento entra em vigor no final do período pago — os clientes mantêm o acesso até a expiração |
| **Compromisso Mínimo Exigido** | Os clientes devem completar um número mínimo de ciclos de faturamento antes de cancelar |

Configurações adicionais:

- **Compromisso Mínimo (Ciclos)** — Ao usar a política de compromisso, defina o número de ciclos de faturamento exigidos (ex.: `3` para um mínimo de 3 meses).
- **Período de Carência (Dias)** — Dias de acesso contínuo após uma falha de pagamento antes que a assinatura seja suspensa. Defina como `0` para suspensão imediata.
- **Período de Reativação (Dias)** — Dias após o cancelamento durante os quais um cliente pode reativar sua assinatura sem precisar se inscrever novamente do zero.

## Comportamento de mudança de plano (Aba Ciclo de Vida)

O cartão **Comportamento de Mudança de Plano**, abaixo de Política de Cancelamento, controla o que acontece quando os clientes fazem upgrade ou downgrade entre planos:

- **Comportamento de Upgrade** — Defina como **Imediato** (cobrar o valor proporcional agora) ou **Na Renovação** (mudar na próxima data de faturamento).
- **Comportamento de Downgrade** — Defina como **Imediato** (aplicar crédito à próxima fatura) ou **Na Renovação** (mudar na próxima data de faturamento).

![Aba Ciclo de Vida do editor de planos](/static/core/admin/img/help/subscription-plans/edit-form-lifecycle-tab.webp)

## Aba Avançado

A aba **Avançado** contém configurações que raramente serão necessárias no dia a dia:

- **Integração com Provedor** — Mapeie este plano para IDs de plano/preço dos seus provedores de pagamento (ex.: `{"stripe": "price_xxx", "paypal": "P-xxx"}`), para lojas que gerenciam assinaturas nativamente através do provedor em vez do próprio mecanismo de faturamento do Spwig.
- **Estatísticas** — Valores somente leitura: **Assinaturas Ativas**, **Receita Total** e os timestamps **Criado Em** / **Atualizado Em** do plano. Estes espelham a faixa de estatísticas no topo da página.

![Aba Avançado do editor de planos](/static/core/admin/img/help/subscription-plans/edit-form-advanced-tab.webp)

## Visibilidade e status (Aba Geral)

- **Ativo** — Desmarque para desativar um plano, impedindo a criação de novas assinaturas. As assinaturas existentes não são afetadas.
- **Público** — Desmarque para ocultar o plano das páginas voltadas ao cliente (útil para planos internos ou legados nos quais os assinantes existentes permanecem).

## Dicas

- Use um **período de teste** para reduzir a hesitação — mesmo uma breve prova gratuita de 7 dias pode melhorar significativamente as taxas de conversão em produtos de assinatura.
- Configure **três níveis de preço** (mensal, trimestral, anual) com descontos crescentes para incentivar compromissos anuais e melhorar seu fluxo de caixa.
- Para assinaturas baseadas em serviços, defina a **Política de Cancelamento** como **Cancelar no Fim do Período** para que os clientes mantenham o acesso durante o período pago — isso parece justo e reduz chargebacks.
- Mantenha o **Período de Carência** em 3–7 dias para falhas de pagamento. Isso dá aos clientes tempo para atualizar seu método de pagamento antes de perder o acesso.
- Use o sinalizador **Obrigatório** em adicionais com moderação — use-o apenas para itens que são genuinamente obrigatórios (ex.: um acordo de serviço), não como uma forma de inflar o preço.
- Desative planos sem assinantes em vez de excluí-los — isso preserva dados históricos para clientes que anteriormente se inscreveram.
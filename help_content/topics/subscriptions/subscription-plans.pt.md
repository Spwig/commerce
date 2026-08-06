---
title: Assinaturas de Planos
---

Os planos de assinatura permitem que você ofereça cobrança recorrente para seus produtos — ideal para itens consumíveis, serviços, caixas personalizadas ou qualquer produto que os clientes comprem repetidamente. Este guia explica como criar e configurar planos, definir níveis de preços, adicionar períodos de teste e anexar adendos opcionais.

## Começando

Navegue até **Assinaturas > Planos de Assinatura** no menu lateral do administrador. A lista de planos mostra todos os seus planos com seu modelo de preços, quantidade de assinantes ativos e status de visibilidade.

Para criar um novo plano, clique no botão **+ Adicionar Plano de Assinatura** — isso abre o assistente de criação de plano, que o leva passo a passo pela configuração.

![Lista de planos de assinatura](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Um plano por si só não é comprável — é um modelo. Depois de criá-lo aqui, anexe-o a um ou mais produtos a partir da aba **Assinaturas** do produto (apenas produtos simples, variáveis e digitais), para que os clientes possam se inscrever. Veja [Vendendo Produtos como Assinaturas](/help/selling-products-as-subscriptions) para esse passo.

## Informações do Plano

A primeira seção captura a identidade central do seu plano.

- **Nome do Plano** — O nome que os clientes veem ao se inscrever. Clique no ícone do globo para adicionar traduções para outros idiomas da loja.
- **Slug** — Um identificador amigável para URLs gerado automaticamente a partir do nome (ex: `plano-premium`). Esse é usado internamente e em integrações.
- **Descrição** — Texto opcional descrevendo o que o plano inclui. Suporta traduções.

## Modelo de Preço

Escolha como o preço é estruturado para este plano:

| Modelo de Preço | Ideal Para |
|---------------|----------|
| **Preço em Níveis** | Oferecendo opções de compromisso mensal, trimestral e anual com descontos para prazos maiores |
| **Baseado em Quantidade** | Preço por assento ou por usuário, onde o total escala com a quantidade (ex: licenças de equipe) |
| **Taxa Fixa** | Um preço único sem variações |

Para planos **Baseados em Quantidade**, defina a **Quantidade Mínima** (número mínimo de assentos necessários) e, opcionalmente, uma **Quantidade Máxima** para limitar quantos assentos um assinante pode comprar.

## Níveis de Preço

Os níveis de preço definem a frequência da cobrança e as opções de desconto disponíveis para os clientes neste plano. Adicione-os na seção **Níveis de Preço** abaixo do formulário principal.

Cada nível tem os seguintes campos:

- **Nome do Nível** — A etiqueta exibida aos clientes (ex: `Mensal`, `Anual — Ganhe 20%`). Suporta traduções.
- **Ciclo de Cobrança** — Com que frequência o cliente é cobrado: Diário, Semanal, Mensal, Trimestral, Semestral ou Anual.
- **Intervalo de Cobrança** — O multiplicador para o ciclo de cobrança. Defina como `2` com Mensal para cobrar a cada 2 meses.
- **Percentual de Desconto** — O desconto aplicado ao preço do produto para este nível. Defina como `0` para o preço cheio, ou `20` para dar 20% de desconto. Este desconto é acumulado sobre qualquer preço de venda no próprio produto.
- **Nível Padrão** — Marque um nível como padrão para selecioná-lo automaticamente para os clientes quando eles visualizarem as opções de assinatura.

O desconto se aplica a partir do primeiro ciclo de cobrança do cliente, não apenas em renovações — um nível com 20% de desconto cobra 20% de desconto desde o primeiro dia (ou do primeiro pagamento após um teste, se o plano tiver um).

### Exemplo: plano em níveis com três opções

Para um plano de assinatura "Clube de Café":

| Nome do Nível | Ciclo de Cobrança | Desconto |
|-----------|---------------|----------|
| Mensal | Mensal | 0% |
| Trimestral — Ganhe 10% | Trimestral | 10% |
| Anual — Ganhe 20% | Anual | 20% |

## Período de Teste

Um período de teste permite que os clientes experimentem sua assinatura antes da primeira cobrança completa. Configure isso na seção **Período de Teste**:

- **Período de Teste (Dias)** — Número de dias de teste gratuito. Defina como `0` para desativar os testes. O máximo é 365 dias.
- **Preço de Teste** — Preço reduzido opcional durante o teste (ex: $1 para o primeiro mês). Deixe em branco para um teste totalmente gratuito.

## Política de Cancelamento

Controle como os clientes podem cancelar sua assinatura na seção **Política de Cancelamento**:

| Política | Descrição |
|--------|-------------|
| **Cancelar a qualquer momento** | Os clientes podem cancelar imediatamente a qualquer momento |
| **Cancelar ao final do período** | O cancelamento entra em vigor ao final do período pago — os clientes mantêm acesso até a expiração |
| **Compromisso Mínimo Necessário** | Os clientes devem completar um número mínimo de ciclos de cobrança antes de cancelar |

Configurações adicionais:

- **Compromisso Mínimo (Ciclos)** — Ao usar a política de compromisso, defina o número necessário de ciclos de cobrança (por exemplo, `3` para um mínimo de 3 meses).
- **Período de Carência (Dias)** — Dias de acesso contínuo após uma falha no pagamento antes que a assinatura seja suspensa. Defina como `0` para suspensão imediata.
- **Período de Reativação (Dias)** — Dias após o cancelamento durante os quais um cliente pode reativar sua assinatura sem recomeçar do zero.

## Comportamento de alteração de plano

Ao atualizar ou baixar entre planos, você pode controlar quando a alteração entra em vigor:

- **Comportamento de Atualização** — Defina como **Imediato** (cobrar valor proporcional agora) ou **Na Renovação** (mudar na próxima data de cobrança).
- **Comportamento de Baixa** — Defina como **Imediato** (aplicar crédito na próxima fatura) ou **Na Renovação** (mudar na próxima data de cobrança).

## Limites e restrições

- **Máximo de Ciclos de Cobrança** — O número total de ciclos de cobrança antes que a assinatura termine automaticamente. Deixe em branco para cobrança recorrente ilimitada. Útil para planos em parcelas ou assinaturas com prazo de validade.
- **Taxa de Configuração** — Uma cobrança única coletada quando a assinatura é criada pela primeira vez (por exemplo, taxa de onboarding ou ativação). Defina como `0.00` para nenhuma taxa de configuração.

## Add-ons do plano

Add-ons são extras opcionais que os assinantes podem anexar ao seu plano. Adicione-os na seção **Add-ons do Plano**:

- **Nome do Add-on** — O nome exibido aos clientes. Suporta traduções.
- **Descrição** — O que o add-on oferece.
- **Preço** — Custo do add-on.
- **Frequência de Cobrança** — Se o add-on é cobrado **Por Ciclo de Cobrança** (recorrente) ou **Único** no início da assinatura.
- **Permitir Quantidade** — Ative para permitir que os clientes comprem múltiplas unidades do add-on.
- **Obrigatório** — Marque esta opção para incluir automaticamente o add-on em todas as novas assinaturas. Add-ons obrigatórios não podem ser removidos pelo cliente.

## Visibilidade e status

- **Ativo** — Desmarque para desativar um plano para que nenhuma nova assinatura possa ser criada. Assinaturas existentes não são afetadas.
- **Público** — Desmarque para ocultar o plano das páginas visíveis ao cliente (útil para planos internos ou legados que os assinantes existentes permaneçam neles).
- **Ordem de Classificação** — Controla a ordem de exibição nas páginas de seleção de assinatura. Números menores aparecem primeiro.

## Dicas

- Use um **período de teste** para reduzir a hesitação — mesmo um teste gratuito de 7 dias pode melhorar significativamente as taxas de conversão em produtos de assinatura.
- Configure **três níveis de preços** (mensal, trimestral, anual) com descontos crescentes para incentivar compromissos anuais e melhorar seu fluxo de caixa.
- Para assinaturas baseadas em serviços, defina a **Política de Cancelamento** como **Cancelar ao Final do Período** para que os clientes mantenham acesso durante seu período pago — isso parece justo e reduz as reembolsos.
- Mantenha o **Período de Carência** entre 3–7 dias para falhas na cobrança. Isso dá aos clientes tempo para atualizar seu método de pagamento antes de perder o acesso.
- Use a opção **Obrigatório** em add-ons com parcimônia — use-a apenas para coisas que sejam verdadeiramente obrigatórias (por exemplo, um acordo de serviço), e não como forma de aumentar os preços.
- Desative os planos sem assinantes em vez de excluí-los — isso preserva os dados históricos para quaisquer clientes que tenham se inscrito anteriormente.
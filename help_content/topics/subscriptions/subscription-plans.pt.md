---
title: Planos de Assinatura
---

Planos de assinatura permitem que você ofereça cobrança recorrente para seus produtos — ideal para produtos de consumo, serviços, caixas curadas ou qualquer produto que os clientes comprem repetidamente. Este guia explica como criar e configurar planos, definir níveis de preços, adicionar períodos de avaliação e anexar add-ons opcionais.

## Começando

Navegue até **Assinaturas > Planos de Assinatura** no menu lateral do administrador. A lista de planos mostra todos os seus planos com seu modelo de preços, número de assinantes ativos e status de visibilidade.

Para criar um novo plano, clique no botão **+ Adicionar Plano de Assinatura** — isso abre o assistente de criação de planos, que o guia passo a passo no setup.

![Lista de planos de assinatura](/static/core/admin/img/help/subscription-plans/plan-list.webp)

## Informações do plano

A primeira seção captura a identidade central do seu plano.

- **Nome do plano** — O nome que os clientes veem ao se inscrever. Clique no ícone da bola de futebol para adicionar traduções para outros idiomas do loja.
- **Slug** — Um identificador amigável para URL gerado automaticamente a partir do nome (ex: `premium-plan`). Este é usado internamente e em integrações.
- **Descrição** — Texto opcional descrevendo o que o plano inclui. Suporta traduções.

## Modelo de preços

Escolha como o preço é estruturado para este plano:

| Modelo de Preço | Melhor Para |
|----------------|-------------|
| **Preço por Nível** | Oferecer opções de compromisso mensal, trimestral e anual com descontos para termos mais longos |
| **Baseado em Quantidade** | Preço por assento ou por usuário, onde o total escala com a quantidade (ex: licenças de equipe) |
| **Taxa Fixa** | Um preço fixo único sem variações |

Para planos **Baseados em Quantidade**, defina a **Quantidade Mínima** (número mínimo de assentos exigidos) e opcionalmente uma **Quantidade Máxima** para limitar quantos assentos um assinante pode comprar.

## Níveis de preço

Níveis de preço definem a frequência de cobrança e as opções de desconto disponíveis para os clientes neste plano. Adicione-os na seção **Níveis de Preço** abaixo do formulário principal.

Cada nível tem os seguintes campos:

- **Nome do Nível** — O rótulo mostrado aos clientes (ex: `Mensal`, `Anual — Economize 20%`). Suporta traduções.
- **Ciclo de Cobrança** — Quão frequentemente o cliente é cobrado: Diário, Semanal, Mensal, Trimestral, Semestral ou Anual.
- **Intervalo de Cobrança** — O multiplicador para o ciclo de cobrança. Defina como `2` com Mensal para cobrar a cada 2 meses.
- **Percentual de Desconto** — O desconto aplicado ao preço do produto para este nível. Defina como `0` para preço integral, ou `20` para dar 20% de desconto. Este desconto se soma a qualquer preço promocional no próprio produto.
- **Nível Padrão** — Marque um nível como padrão para pré-selecioná-lo para os clientes quando eles visualizarem as opções de assinatura.

### Exemplo: plano por nível com três opções

Para um plano de assinatura "Clube de Café":

| Nome do Nível | Ciclo de Cobrança | Desconto |
|---------------|-------------------|----------|
| Mensal | Mensal | 0% |
| Trimestral — Economize 10% | Trimestral | 10% |
| Anual — Economize 20% | Anual | 20% |

## Período de avaliação

Um período de avaliação permite que os clientes experimentem sua assinatura antes da primeira cobrança completa. Configure isso na seção **Período de Avaliação**:

- **Período de Avaliação (Dias)** — Número de dias de avaliação gratuita. Defina como `0` para desativar avaliações. Máximo é 365 dias.
- **Preço de Avaliação** — Preço reduzido opcional durante a avaliação (ex: $1 para o primeiro mês). Deixe vazio para uma avaliação completamente gratuita.

## Política de cancelamento

Controle como os clientes podem cancelar sua assinatura na seção **Política de Cancelamento**:

| Política | Descrição |
|----------|-----------|
| **Cancelar a qualquer momento** | Os clientes podem cancelar imediatamente a qualquer momento |
| **Cancelar no final do período** | O cancelamento entra em vigor no final do período pago — os clientes mantêm o acesso até a expiração |
| **Requer compromisso mínimo** | Os clientes devem completar um número mínimo de ciclos de cobrança antes de cancelar |

Configurações adicionais:

- **Mínimo de Compromisso (Ciclos)** — Ao usar a política de compromisso, defina o número necessário de ciclos de cobrança (por exemplo, `3` para um mínimo de 3 meses).
- **Período de Graça (Dias)** — Dias de acesso contínuo após uma falha de pagamento antes que a assinatura seja suspensa.

Defina para `0` para suspensão imediata.
- **Período de Reativação (Dias)** — Dias após a cancelamento durante os quais um cliente pode reativar sua assinatura sem se inscrever novamente do zero.

## Comportamento de mudança de plano

Quando os clientes atualizam ou reduzem entre planos, você pode controlar quando a mudança entra em vigor:

- **Comportamento de Atualização** — Defina para **Imediato** (cobrar valor proporcional agora) ou **Na Renovação** (mudar na próxima data de cobrança).
- **Comportamento de Redução** — Defina para **Imediato** (aplicar crédito na próxima fatura) ou **Na Renovação** (mudar na próxima data de cobrança).

## Limites e restrições

- **Máximo de Ciclos de Cobrança** — O número total de ciclos de cobrança antes que a assinatura termine automaticamente. Deixe vazio para cobrança recorrente ilimitada. Útil para planos de parcelamento ou assinaturas com prazo limitado.
- **Taxa de Instalação** — Uma cobrança única coletada quando a assinatura é criada pela primeira vez (por exemplo, taxa de onboarding ou ativação). Defina para `0.00` para não ter taxa de instalação.

## Add-ons de plano

Add-ons são extras opcionais que os assinantes podem anexar ao seu plano. Adicione-os na seção **Add-ons de Plano**:

- **Nome do Add-on** — O nome exibido aos clientes. Suporta traduções.
- **Descrição** — O que o add-on fornece.
- **Preço** — Custo do add-on.
- **Frequência de Cobrança** — Se o add-on é cobrado **Por Ciclo de Cobrança** (recorrente) ou **Única Vez** no início da assinatura.
- **Permitir Quantidade** — Ative para permitir que os clientes comprem múltiplas unidades do add-on.
- **Obrigatório** — Marque para incluir automaticamente o add-on em todas as novas assinaturas. Add-ons obrigatórios não podem ser removidos pelo cliente.

## Visibilidade e status

- **Ativo** — Desmarque para desativar um plano, impedindo a criação de novas assinaturas. Assinaturas existentes não são afetadas.
- **Público** — Desmarque para ocultar o plano das páginas voltadas ao cliente (útil para planos internos ou legados que assinantes existentes ainda estão usando).
- **Ordem de Classificação** — Controla a ordem de exibição nas páginas de seleção de assinatura. Números mais baixos aparecem primeiro.

## Dicas

- Use um **período de teste** para reduzir a hesitação — mesmo um curto período de teste gratuito de 7 dias pode melhorar significativamente as taxas de conversão de produtos assinados.
- Configure **três níveis de preços** (mensal, trimestral, anual) com descontos crescentes para incentivar compromissos anuais e melhorar seu fluxo de caixa.
- Para assinaturas baseadas em serviço, defina a **Política de Cancelamento** para **Cancelar no Final do Período** para que os clientes mantenham o acesso durante seu período pago — isso parece justo e reduz os estornos.
- Mantenha o **Período de Graça** entre 3–7 dias para falhas de pagamento. Isso dá aos clientes tempo para atualizar seu método de pagamento antes de perderem o acesso.
- Use o sinalizador **Obrigatório** nos add-ons com moderação — use-o apenas para coisas que são verdadeiramente obrigatórias (por exemplo, um acordo de serviço), e não como uma forma de inflar o preço.
- Desative planos sem assinantes em vez de excluí-los — isso preserva os dados históricos para quaisquer clientes que anteriormente se inscreveram.
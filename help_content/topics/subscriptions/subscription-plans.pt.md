---
title: Assinaturas de Planos
---

Os planos de assinatura permitem que você ofereça cobrança recorrente para seus produtos — ideal para itens consumíveis, serviços, caixas personalizadas ou qualquer produto que os clientes comprem repetidamente. Este guia explica como criar e configurar planos, definir níveis de preços, adicionar períodos de teste e anexar complementos opcionais.

## Começando

Navegue até **Assinaturas > Planos de Assinatura** no menu lateral do administrador. A lista de planos mostra todos os seus planos com seu modelo de preços, quantidade de assinantes ativos e status de visibilidade.

![Lista de planos de assinatura](/static/core/admin/img/help/subscription-plans/plan-list.webp)

Para criar um novo plano, clique no botão **Criar com o Assistente** — isso abre o assistente de criação de plano, que o leva passo a passo pela configuração. O botão **+ Adicionar Plano** ao lado abre um formulário em branco para comerciantes que preferem configurar tudo manualmente.

Um plano por si só não é comprável — é um modelo. Depois de criá-lo aqui, anexe-o a um ou mais produtos a partir da aba **Assinaturas** do produto (apenas produtos simples, variáveis e digitais), para que os clientes possam se inscrever. Veja [Vendendo Produtos como Assinaturas](/help/selling-products-as-subscriptions) para esse passo.

## O editor de planos

Abrir um plano existente (clique no nome ou no ícone de lápis, da lista) o leva ao editor de planos. O cabeçalho mostra o nome do plano, seu modelo de preços, os selos de status **Ativo**/**Inativo** e **Público**/**Privado**, e a data de criação. Os dois botões no canto superior direito do cabeçalho salvam suas alterações — o ícone de círculo verde salva e retorna à lista, o ícone de check simples salva e mantém você na página para continuar editando.

Logo abaixo do cabeçalho, uma faixa de estatísticas resume o plano de uma olhada: **Assinaturas Ativas**, **Níveis de Preços**, **Complementos** e **Receita Total**.

O restante do formulário é organizado em cinco guias:

| Guia | O que contém |
|-----|------------------|
| **Geral** | Informações do plano (nome, slug, descrição) e Status (ativo/público) |
| **Preço** | Configuração de Preço, Período de Teste e Limites & Restrições |
| **Níveis & Complementos** | Editores de Níveis de Preço e Complementos |
| **Ciclo de Vida** | Política de Cancelamento e Comportamento de Alteração de Plano |
| **Avançado** | Integração com Provedor e Estatísticas |

As seções a seguir percorrem os ajustes de cada guia. Quando você cria um novo plano diretamente a partir de **+ Adicionar Plano** (em vez do assistente), os mesmos campos aparecem em um único formulário rolável em vez de guias — salve o plano uma vez e o reabra para obter o editor com guias completo.

## Informações do plano (aba Geral)

O cartão **Informações do Plano** captura a identidade central do seu plano.

- **Nome do Plano** — O nome que os clientes veem ao se inscrever. Clique no ícone de globo para adicionar traduções para outros idiomas da loja.
- **Slug** — Um identificador amigável para URLs gerado automaticamente a partir do nome (ex.: `plano-premium`). Esse é usado internamente e em integrações.
- **Descrição** — Texto opcional descrevendo o que o plano inclui. Suporta traduções.

O cartão **Status** na mesma aba controla os interruptores **Ativo** e **Público** — veja [Visibilidade e status](#visibilidade-e-status) abaixo.

![Aba Geral do editor de planos](/static/core/admin/img/help/subscription-plans/edit-form-general-tab.webp)

## Modelo de Preço (aba Preço)

O cartão **Configuração de Preço** controla como a estrutura de preços é feita para este plano:

| Modelo de Preço | Melhor para |
|-----------------|--------------|
| **Preço em Níveis** | Oferecendo opções de compromisso mensal, trimestral e anual com descontos para prazos maiores |
| **Baseado em Quantidade** | Preço por assento ou por usuário, onde o total escala com a quantidade (ex.: licenças de equipe) |
| **Taxa Fixa** | Um preço único fixo sem variações |

Para planos **Baseados em Quantidade**, marque **Permitir Quantidade** e defina a **Quantidade Mínima** (mínimo de assentos necessários) e, opcionalmente, uma **Quantidade Máxima** para limitar quantos assentos um assinante pode comprar.

[![](https://d35f7a7175p2f6.cloudfront.net/9/2023/04/12/15/1555455512593-7554555512593.png)](/static/core/admin/img/help/subscription-plans/edit-form-pricing-tab.webp)

## Níveis de preços (aba Níveis & Adicionais)

Os níveis de preços definem a frequência de cobrança e as opções de desconto disponíveis aos clientes neste plano. Adicione-os no cartão **Níveis de Preços** da aba **Níveis & Adicionais**, junto com o editor de Adicionais.

Cada nível possui os seguintes campos:

- **Nome do Nível** — A etiqueta exibida aos clientes (por exemplo, `Mensal`, `Anual — Ganhe 20%`). Suporta traduções.
- **Ciclo de Cobrança** — Com que frequência o cliente é cobrado: Diariamente, Semanalmente, Mensalmente, Trimestralmente, Semestralmente ou Anualmente.
- **Intervalo de Cobrança** — O multiplicador do ciclo de cobrança. Defina como `2` com Mensal para cobrar a cada 2 meses.
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

## Período de teste

Um período de teste permite que os clientes experimentem sua assinatura antes da primeira cobrança completa. Configure isso na seção **Período de Teste**:

- **Período de Teste (Dias)** — Número de dias de teste gratuito. Defina como `0` para desativar os testes. O máximo é 365 dias.
- **Preço de Teste** — Preço reduzido opcional durante o teste (por exemplo, $1 para o primeiro mês). Deixe em branco para um teste totalmente gratuito.

## Política de Cancelamento

Controle como os clientes podem cancelar sua assinatura na seção **Política de Cancelamento**:

| Política | Descrição |
|--------|-------------|
| **Cancelar a qualquer momento** | Os clientes podem cancelar imediatamente a qualquer momento |
| **Cancelar no Fim do Período** | O cancelamento entra em vigor no final do período pago — os clientes mantêm acesso até a expiração |
| **Compromisso Mínimo Necessário** | Os clientes devem completar um número mínimo de ciclos de cobrança antes de cancelar |

Configurações adicionais:

- **Compromisso Mínimo (Ciclos)** — Ao usar a política de compromisso, defina o número necessário de ciclos de cobrança (por exemplo, `3` para um mínimo de 3 meses).
- **Período de Carência (Dias)** — Dias de acesso contínuo após uma falha de pagamento antes da suspensão da assinatura. Defina como `0` para suspensão imediata.
- **Período de Reativação (Dias)** — Dias após o cancelamento durante os quais um cliente pode reativar sua assinatura sem se inscrever do zero.

## Comportamento da Alteração de Plano

Quando os clientes atualizarem ou baixarem entre planos, você pode controlar quando a mudança entra em vigor:

- **Comportamento da Atualização** — Defina como **Imediato** (cobrar valor proporcional agora) ou **Na Renovação** (mudar na data de cobrança seguinte).
- **Comportamento da Baixa** — Defina como **Imediato** (aplicar crédito na próxima fatura) ou **Na Renovação** (mudar na data de cobrança seguinte).

## Limites e Restrições

- **Máximo de Ciclos de Cobrança** — O número total de ciclos de cobrança antes da assinatura terminar automaticamente. Deixe em branco para cobrança recorrente ilimitada. Útil para planos em parcelas ou assinaturas com prazo de validade.
- **Taxa de Configuração** — Uma cobrança única coletada quando a assinatura é criada pela primeira vez (por exemplo, taxa de onboarding ou ativação). Defina como `0.00` para nenhuma taxa de configuração.

## Adicionais do Plano

Adicionais são extras opcionais que os assinantes podem anexar ao seu plano. Adicione-os na seção **Adicionais do Plano**:

- **Nome do Adicional** — O nome exibido aos clientes.

Suporte a traduções.
- **Descrição** — O que o complemento oferece.
- **Preço** — Custo do complemento.
- **Frequência de cobrança** — Se o complemento é cobrado **Por Ciclo de Cobrança** (recorrente) ou **Único** no início da assinatura.
- **Permitir Quantidade** — Ative para permitir que os clientes comprem múltiplas unidades do complemento.
- **Obrigatório** — Marque esta opção para incluir automaticamente o complemento em todas as novas assinaturas.

Complementos obrigatórios não podem ser removidos pelo cliente.

## Visibilidade e status

- **Ativo** — Desmarque para desativar um plano para que nenhum nova assinatura possa ser criada. Assinaturas existentes não são afetadas.
- **Público** — Desmarque para ocultar o plano das páginas visíveis ao cliente (útil para planos internos ou legados que os assinantes existentes permaneçam neles).
- **Ordem de Classificação** — Controla a ordem de exibição nas páginas de seleção de assinatura. Números menores aparecem primeiro.

## Dicas

- Use um **período de teste** para reduzir a hesitação — mesmo um teste gratuito de 7 dias curto pode melhorar significativamente as taxas de conversão em produtos de assinatura.
- Configure **três níveis de preços** (mensal, trimestral, anual) com descontos crescentes para incentivar compromissos anuais e melhorar seu fluxo de caixa.
- Para assinaturas baseadas em serviço, defina **Política de Cancelamento** como **Cancelar ao Final do Período** para que os clientes mantenham acesso durante seu período pago — isso parece justo e reduz as reembolsos.
- Mantenha o **Período de Graça** entre 3 a 7 dias para falhas de pagamento. Isso dá aos clientes tempo para atualizar seu método de pagamento antes de perder o acesso.
- Use a opção **Obrigatório** em complementos com parcimônia — use-a apenas para coisas que sejam verdadeiramente obrigatórias (por exemplo, um contrato de serviço), e não como forma de aumentar os preços.
- Desative planos sem assinantes em vez de excluí-los — isso preserva os dados históricos para quaisquer clientes que tenham se inscrito anteriormente.
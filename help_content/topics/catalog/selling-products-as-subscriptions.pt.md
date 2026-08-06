---
title: Vendendo Produtos como Assinaturas
---

Qualquer produto Simples, Variável ou Digital pode agora ser vendido em um regime recorrente, lado a lado - ou em vez de - uma compra única. Este guia aborda como ativar as assinaturas para um produto, escolher quais planos os clientes podem selecionar e o que os clientes realmente veem ao comprarem.

<!-- screenshots-needed:
- url: /admin/catalog/product/{id}/change/
  filename: subscriptions-tab.webp
  description: O formulário de edição do produto com a guia Assinaturas ativa, mostrando
    Ativar Assinatura marcado, um ou mais planos selecionados no campo Planos de Assinatura, e as caixas de seleção Permitir Compra Única / Padrão para Assinatura visíveis.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
- url: (storefront) página de detalhe do produto para um produto com assinatura habilitada
  filename: subscribe-and-save-selector.webp
  description: O seletor "Compra Única" vs "Assine e Salve" expandido, mostrando uma lista de níveis de frequência de entrega com o selo "Salve X%" nos níveis com desconto.
  save-to: core/static/core/admin/img/help/selling-products-as-subscriptions/
  viewport: 1440x900
  notes: Exige um produto com assinatura habilitada, com pelo menos um plano público ativo e níveis de preços, visualizado a partir do site (não do admin).
-->

## Quais tipos de produto podem ser vendidos como assinaturas

As assinaturas estão disponíveis apenas para estes tipos de produto:

| Elegíveis | Não elegíveis |
|----------|---------------|
| Produto Simples | Pacote de Produto |
| Produto Variável | Cartão de Presente |
| Produto Digital | Produto Personalizável |
| | Produto Configurável |
| | Produto de Reserva |

O motivo é a entrega, não o preço: uma assinatura re-cobra seu cliente a cada ciclo e reentrega o produto por meio de um novo pedido a cada vez. O Spwig sabe como re-entregar um produto simples ou variável e re-conceder o download ou licença de um produto digital em cada renovação - mas não pode reexecutar com segurança a emissão de um cartão de presente, um pacote de múltiplos componentes, uma personalização salva do cliente, uma montagem de configurador ou uma vaga de reserva em um horário recorrente. Permitir que esses tipos sejam vendidos como assinaturas correria o risco de pegar o dinheiro do cliente no ciclo 2 sem poder entregar nada.

A caixa de seleção **Ativar Assinatura** não está oculta ou desativada para tipos não elegíveis - você pode, tecnicamente, marcá-la em qualquer produto. Se tentar salvar um produto com assinatura habilitada, como Cartão de Presente, Pacote, Personalizável, Configurável ou Reserva, o Spwig recusará o salvamento com um erro de validação explicando que este tipo de produto não pode ser vendido como assinatura. Mude o **Tipo de Produto** primeiro (aba Informações Básicas), ou deixe as assinaturas desativadas para esse produto.

## Ativando assinaturas em um produto

1. Navegue até **Produtos > Todos os Produtos** e abra o produto que deseja vender como assinatura (ou crie um novo).
2. Confirme que o **Tipo de Produto** na aba Informações Básicas é Simples, Variável ou Digital.
3. Clique na guia **Assinaturas**.
4. Marque **Ativar Assinatura**.
5. No campo **Planos de Assinatura**, selecione um ou mais planos que este produto deve oferecer. Você só pode escolher planos que já existam - se ainda não criou nenhum, consulte [Planos de Assinatura](/help/subscription-plans) primeiro.
6. Configure os dois checkboxes de modo de compra (abaixo).
7. Clique em **Salvar**.

## Anexando planos de assinatura

Um **Plano de Assinatura** é um modelo reutilizável - opções de frequência de cobrança, teste, taxa de instalação, regras de cancelamento - que você cria uma vez e pode anexar a qualquer número de produtos elegíveis. O campo **Planos de Assinatura** na guia Assinaturas do produto é onde você conecta o produto aos planos em que ele deve ser vendido.

Você pode anexar mais de um plano ao mesmo produto.

Isso é útil, por exemplo, quando você deseja oferecer uma "camada padrão" e uma "camada premium" recorrente para o mesmo item - cada plano pode ter sua própria hierarquia de preços, teste e política de cancelamento.


Quando um produto tem mais de um plano anexado, os clientes veem um seletor de plano na página do produto antes de escolher a frequência de cobrança.

## Controlando compras únicas vs. assinaturas

Dois checkboxes na aba Assinaturas controlam como os clientes podem comprar o produto:

- **Permitir compra única** — Ativado por padrão. Quando marcado, os clientes escolhem entre uma compra regular única ou se inscreverem. Desmarque-o para tornar o produto somente assinatura — cada compra se torna uma ordem recorrente e nenhuma opção única é exibida de forma alguma.
- **Padrão para assinatura** — Seleciona automaticamente a opção de assinatura (e seu plano/padrão padrão) quando a página do produto carrega, em vez de fazer com que os clientes escolham ativamente. Isso só tem efeito quando **Permitir compra única** também estiver marcado — se a compra única estiver desativada, o produto é somente assinatura, independentemente deste recurso.

Use **Padrão para assinatura** para produtos onde a entrega recorrente é a expectativa natural (café, suplementos, produtos consumíveis) — ele remove um clique e orienta os clientes para a opção que os mantém voltando, sem remover sua capacidade de comprar apenas uma vez.

## O que os clientes veem

### Na página do produto

Quando um produto tem assinaturas ativadas e pelo menos um plano ativo, público anexado, um seletor de modo de compra aparece na página do produto:

- Se a compra única for permitida, os clientes veem uma escolha de **"Compra única"** vs **"Assine e economize"**, padrão para qualquer modo que você configurou.
- Se o produto tiver mais de um plano anexado, um seletor de plano aparece assim que **"Assine e economize"** for selecionado.
- Para o plano escolhido, os clientes veem uma lista de **frequência de entrega** construída a partir dos níveis de preços desse plano (ex.: Mensal, Trimestral, Anual), cada um mostrando seu preço e um selo de **"Economize X%"** quando o nível carrega um desconto.
- O comprimento do teste, taxa de instalação e a política de cancelamento do plano (ex.: "Cancele a qualquer momento") são exibidos junto com a lista de níveis, juntamente com uma observação de que um método de pagamento é adicionado no checkout.

### No carrinho e no checkout

Itens de linha de assinatura no carrinho carregam um selo de **Assinatura**, a frequência de cobrança (ex.: "A cada mês") e uma observação de teste se aplicável, para que fique claro para o cliente quais linhas são recorrentes. No checkout, o cliente escolhe um provedor de pagamento como de costume — este é o método de pagamento que será cobrado nas renovações futuras.

> **Limitação conhecida:** Salvar automaticamente uma cartão do cliente para renovações de assinatura no checkout ainda está sendo conectado para alguns provedores de pagamento. Até que um provedor específico suporte isso, as assinaturas colocadas por meio dele podem precisar de um follow-up adicional (por exemplo, contactar o cliente para obter detalhes de pagamento atualizados antes de uma renovação) em vez de serem totalmente sem intervenção desde o início. Verifique com sua configuração de provedor de pagamento se você notar que as renovações não estão sendo cobradas automaticamente para uma assinatura.

## Dicas

- Crie e teste o plano de assinatura primeiro (níves de preços, teste, política de cancelamento), depois o anexe aos produtos — é mais fácil acertar o plano uma vez do que corrigi-lo em vários produtos depois.
- Deixe **Permitir compra única** marcado para a maioria dos produtos. Reserve produtos somente assinatura para casos em que uma compra única realmente não faz sentido para o seu negócio.
- Se você estiver convertendo um produto de venda em uma opção de assinatura, mantenha **Padrão para assinatura** desativado no início para que não interfira com clientes acostumados a comprá-lo uma vez — ative-o mais tarde depois que você tiver visto como os assinantes respondem.
- Produtos digitais são um ótimo enquadramento para assinaturas (licenças de software, membros de conteúdo) desde que a renovação restabeleça automaticamente o acesso sem envolver envio.
- Se você precisar de um tipo de produto que não é elegível (um pacote ou um item personalizável, por exemplo) para ser vendido em base recorrente, considere se um equivalente Simplificado ou Digital simplificado poderia carregar a assinatura em vez disso.
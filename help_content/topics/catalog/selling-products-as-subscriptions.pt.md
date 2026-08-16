---
title: Vendendo Produtos como Assinaturas
---

Qualquer produto Simples, Variável ou Digital pode agora ser vendido em um regime recorrente, lado a lado com — ou em vez de — uma compra única. Este guia aborda como ativar as assinaturas para um produto, escolher quais planos os clientes podem selecionar e o que os clientes realmente veem ao comprarem.

## Quais tipos de produto podem ser vendidos como assinaturas

As assinaturas estão disponíveis apenas para estes tipos de produto:

| Elegível | Não elegível |
|----------|---------------|
| Produto Simples | Produto Pacote |
| Produto Variável | Cartão de Presente |
| Produto Digital | Produto Personalizável |
| | Produto Configurável |
| | Produto de Reserva |

O motivo é a entrega, e não o preço: uma assinatura re-cobra o cliente a cada ciclo e reentrega o produto por meio de um novo pedido a cada vez. O Spwig sabe como re-entregar um produto simples ou variável e re-conceder o download ou licença de um produto digital a cada renovação — mas ele não consegue reexecutar com segurança a emissão de um cartão de presente, um pacote de múltiplos componentes, uma personalização salva do cliente, uma montagem de configurador ou uma vaga de reserva em um horário recorrente. Permitir que esses tipos sejam vendidos como assinaturas correria o risco de pegar o dinheiro do cliente no ciclo 2 sem conseguir entregar nada.

O **checkbox Ativar Assinatura** não está escondido ou desativado para os tipos não elegíveis — você pode, tecnicamente, marcá-lo em qualquer produto. Se você tentar salvar um produto Cartão de Presente, Pacote, Personalizável, Configurável ou Reserva com assinaturas ativadas, o Spwig recusará o salvamento com um erro de validação explicando que este tipo de produto não pode ser vendido como assinatura. Mude o **Tipo de Produto** primeiro (aba Informações Básicas), ou deixe as assinaturas desativadas para esse produto.

## Ativando assinaturas em um produto

1. Navegue até **Produtos > Todos os Produtos** e abra o produto que você quer vender como assinatura (ou crie um novo).
2. Confirme o **Tipo de Produto** na aba Informações Básicas é Simples, Variável ou Digital.
3. Clique na aba **Assinaturas**.
4. Marque **Ativar Assinatura**.
5. No campo **Planos de Assinatura**, selecione um ou mais planos que este produto deve oferecer. Você só pode escolher planos que já existam — se você ainda não criou nenhum, consulte [Planos de Assinatura](/help/subscription-plans) primeiro.
6. Configure os dois checkboxes de modo de compra (abaixo).
7. Clique em **Salvar**.

![A aba Assinaturas do formulário de edição do produto: Ativar Assinatura marcado, um plano selecionado na lista de Planos de Assinatura, e os checkboxes Permitir Compra Única e Padrão para Assinatura](/static/core/admin/img/help/selling-products-as-subscriptions/subscriptions-tab.webp)

## Anexando planos de assinatura

Um **Plano de Assinatura** é um modelo reutilizável — opções de frequência de cobrança, teste, taxa de instalação, regras de cancelamento — que você cria uma vez e pode anexar a qualquer número de produtos elegíveis. O campo **Planos de Assinatura** na aba Assinaturas do produto é onde você conecta o produto aos planos aos quais ele deve ser vendido.

Você pode anexar mais de um plano ao mesmo produto. Isso é útil, por exemplo, quando você quer oferecer uma "Camada Padrão" e uma "Camada Premium" recorrente para o mesmo item — cada plano pode ter suas próprias faixas de preços, teste e política de cancelamento. Quando um produto tem mais de um plano anexado, os clientes veem um seletor de plano na página do produto antes de escolher a frequência de cobrança.

## Controlando compras únicas vs. assinaturas

Dois checkboxes na aba Assinaturas controlam como os clientes podem comprar o produto:

- **Permitir Compra Única** — ativado por padrão.

Ao ser marcado, os clientes escolhem entre uma compra única regular e uma assinatura.

Desmarque-o para tornar o produto apenas assinatura — toda compra se torna uma ordem recorrente, e nenhuma opção única é exibida de forma alguma.
- **Padrão para Assinatura** — seleciona a opção de assinatura (e seu plano/padrão padrão) quando a página do produto carregar, em vez de fazer com que os clientes escolham ativamente.


Isso só tem efeito quando **Permitir compra única** também estiver marcado — se a compra única estiver desativada, o produto é apenas assinatura, independentemente deste ajuste.

Use **Padrão para assinatura** para produtos em que a entrega recorrente é a expectativa natural (café, suplementos, produtos consumíveis) — ele remove um clique e orienta os clientes para a opção que os mantém voltando, sem lhes remover a capacidade de comprar apenas uma vez.

## O que os clientes veem

### Na página do produto

Quando um produto tem assinaturas ativadas e pelo menos um plano ativo, público anexado, um seletor de modo de compra aparece na página do produto:

![O seletor de compra da loja com "Assinar e Salvar" escolhido: uma opção de compra única vs. Assinar e Salvar acima de uma lista de frequência de entrega mostrando os níveis Anual (Salve 20%), Mensal e Trimestral (Salve 10%) com preços, mais notas de tentativa, cancelamento e pagamento](/static/core/admin/img/help/selling-products-as-subscriptions/subscribe-and-save-selector.webp)

- Se a compra única for permitida, os clientes verão uma escolha de **"Compra única"** vs. **"Assinar e Salvar"**, padrão para qualquer modo que você tenha configurado.
- Se o produto tiver mais de um plano anexado, um seletor de plano aparecerá uma vez que "Assinar e Salvar" seja selecionado.
- Para o plano escolhido, os clientes verão uma lista de **frequência de entrega** construída a partir dos níveis de preços desse plano (ex.: Mensal, Trimestral, Anual), cada um mostrando seu preço e um **selo de "Salve X%"** quando o nível tiver desconto.
- O comprimento da tentativa, taxa de instalação e a política de cancelamento do plano (ex.: "Cancele a qualquer momento") são mostrados junto com a lista de níveis, juntamente com uma observação de que um método de pagamento é adicionado no checkout.

### No carrinho e no checkout

Itens de assinatura no carrinho carregam um selo de **Assinatura**, a frequência de cobrança (ex.: "A cada mês") e uma nota de tentativa se aplicável, para que fique claro para o cliente quais linhas são recorrentes. No checkout, o cliente escolhe um provedor de pagamento como de costume — este é o método de pagamento que será cobrado nas renovações futuras.

> **Limitação conhecida:** Salvar automaticamente uma cartão do cliente para renovações de assinatura no checkout ainda está sendo conectado para alguns provedores de pagamento. Até que um provedor específico suporte isso, as assinaturas colocadas por meio dele podem precisar de mais acompanhamento (por exemplo, contactar o cliente para obter detalhes de pagamento atualizados antes de uma renovação) em vez de serem totalmente sem intervenção desde o início. Verifique com sua configuração de provedor de pagamento se você notar que renovações não estão sendo cobradas automaticamente para uma assinatura.

## Dicas

- Crie e teste o plano de assinatura primeiro (níveis de preços, tentativa, política de cancelamento), depois o anexe aos produtos — é mais fácil acertar o plano uma vez do que corrigi-lo em vários produtos depois.
- Deixe **Permitir compra única** marcado para a maioria dos produtos. Reserve produtos apenas com assinatura para casos em que a compra única realmente não faça sentido para o seu negócio.
- Se você estiver convertendo um produto de venda em uma opção de assinatura, deixe **Padrão para assinatura** desativado no início para que não interfira nos clientes acostumados a comprá-lo uma vez — ative-o mais tarde uma vez que você tenha visto como os assinantes respondem.
- Produtos digitais são um ótimo enquadramento para assinaturas (licenças de software, membros de conteúdo) desde que a renovação restabeleça automaticamente o acesso sem envolver envio.
- Se você precisar de um tipo de produto que não esteja elegível (um pacote ou item personalizável, por exemplo) para ser vendido de forma recorrente, considere se um equivalente Simplificado ou Digital simplificado poderia carregar a assinatura em vez disso.
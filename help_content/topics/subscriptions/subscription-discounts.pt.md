---
title: Descontos de Assinaturas
---

Descontos de assinaturas permitem que você aplique reduções de preço a assinaturas individuais de clientes — por exemplo, recompensar assinantes fiéis, honrar um cupom promocional ou resolver uma disputa de cobrança com um crédito de boa vontade. Diferente das camadas de preços no nível do plano, esses descontos são aplicados diretamente a uma assinatura específica.

## Visualizando descontos de assinaturas

Navegue até **Assinaturas > Descontos de Assinaturas** para ver todos os descontos atualmente aplicados em suas assinaturas.

Cada entrada mostra a assinatura a qual pertence, o tipo e o valor do desconto, por quanto tempo o desconto dura e se ainda está ativo.

Você também pode encontrar descontos anexados a uma assinatura específica abrindo **Assinaturas > Assinaturas do Cliente**, clicando em uma assinatura e rolando até a seção **Descontos** no final da página de detalhes.

## Adicionando um desconto a uma assinatura

Para adicionar um novo desconto:

1. Navegue até **Assinaturas > Descontos de Assinaturas**
2. Clique em **+ Adicionar Desconto de Assinatura**
3. Selecione a **Assinatura** à qual deseja aplicar o desconto
4. Configure as configurações do desconto (descritas abaixo)
5. Clique em **Salvar**

O desconto entra em vigor no próximo ciclo de cobrança.

## Tipos de desconto

Escolha como o desconto é calculado:

| Tipo de Desconto | Como funciona | Exemplo |
|------------------|----------------|---------|
| **Percentual de Desconto** | Reduz a conta por um percentual | `20` reduz uma conta de $50 para $40 |
| **Valor Fixo de Desconto** | Subtrai um valor fixo da conta | `10` reduz uma conta de $50 para $40 |
| **Preço Fixo Substituído** | Define a assinatura para um preço específico, independentemente do preço normal do plano | `29` define a conta para $29/ciclo |

Defina o campo **Valor do Desconto** com o número correspondente ao tipo escolhido (percentual, valor em dólar ou preço fixo).

### Exemplo: oferta de retenção

Um cliente entra em contato querendo cancelar. Você oferece a ele 3 meses com 25% de desconto para permanecer:

| Campo | Valor |
|-------|-------|
| Tipo de Desconto | Percentual de Desconto |
| Valor do Desconto | `25` |
| Tipo de Duração | Repetitivo |
| Duração (Meses) | `3` |

## Duração do desconto

Controle por quanto tempo o desconto se aplica aos próximos ciclos de cobrança:

| Tipo de Duração | Quando se aplica |
|------------------|------------------|
| **Aplicar uma vez** | Reduz apenas a cobrança do próximo ciclo de cobrança, depois expira automaticamente |
| **Para sempre** | Aplica-se a todos os próximos ciclos de cobrança até ser desativado manualmente |
| **Repetitivo** | Aplica-se por um número fixo de meses, depois expira |

Para descontos **Repetitivos**, defina o campo **Duração (Meses)** com o número de meses que o desconto deve durar. O campo **Ciclos Restantes** rastreia quantos ciclos restam — ele conta para trás com cada ciclo de cobrança.

## Códigos de cupom

Se o desconto foi acionado por um código promocional, insira-o no campo **Código de Cupom**. Isso é informativo — ele registra de onde o desconto originou-se para seus próprios propósitos de rastreamento.

## Desativando um desconto

Para parar um desconto antes que expire naturalmente, abra o registro do desconto e desmarque a caixa de seleção **Ativo**, depois salve. O desconto não será mais aplicado aos próximos ciclos de cobrança. A assinatura retornará ao preço normal do plano no próximo ciclo de cobrança.

Você também pode definir uma data **Expira em** ao criar o desconto — o sistema desativará automaticamente o desconto após essa data.

## Dicas

- Use descontos **Aplicar uma vez** para gestos de boa vontade únicos (por exemplo, compensar um assinante por uma interrupção no serviço).

Eles são limpos e se expiram sozinhos.
- Descontos de **Percentual de Desconto** são mais seguros do que descontos de **Valor Fixo de Desconto** para assinaturas com preços variáveis, pois o desconto se ajusta com o valor real da conta.
- Ao oferecer uma oferta de retenção, use **Repetitivo** com uma duração de 3 meses — isso dá aos clientes uma razão para permanecerem sem reduzir permanentemente sua receita.
- Mantenha o campo **Código de Cupom** consistente com o código usado pelos clientes.

# Facilita a auditoria de quais promoções geraram quais descontos ao revisar sua receita de assinaturas.
- Os descontos são aplicados a assinaturas individuais, e não a planos.

Se quiser reduzir o preço de um plano para todos os novos assinantes, atualize as camadas de preços do plano em vez disso.
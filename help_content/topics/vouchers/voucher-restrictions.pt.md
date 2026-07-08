---
title: Restrições de Cupom
---

As restrições de cupom controlam quem pode usar um cupom, quando e com que frequência. Configure essas configurações ao criar ou editar um cupom em **Marketing > Cupons**.

![Regras de Restrição](/static/core/admin/img/help/voucher-restrictions/restriction-rules.webp)

## Limites de Uso

Defina limites globais e por cliente na seção **Limites de Uso** do formulário do cupom.

- **Máximo de usos total** — O número máximo de vezes que esse cupom pode ser resgatado por todos os clientes. Deixe vazio para ilimitado.
- **Máximo de usos por cliente** — Quantas vezes um único cliente pode usar esse cupom. Defina como 1 para a maioria das campanhas.

| Padrão | Máximo Total | Por Cliente | Caso de Uso |
|---------|-----------|--------------|----------|
| Campanha limitada | 100 | 1 | "Primeiros 100 clientes" escassez |
| Código compartilhado ilimitado | (vazio) | 1 | Código de marketing contínuo |
| Multiuso ilimitado | (vazio) | (vazio) | Desconto interno/funcionário |
| Códigos únicos de uso único | 1 | 1 | Códigos de campanha gerados em lote |

## Valor Mínimo do Pedido

O campo **Valor mínimo do pedido** protege seus margens exigindo um valor total do carrinho antes que o cupom seja aplicado. Por exemplo, "$10 de desconto em pedidos acima de $50" garante que você nunca desconte um pedido pequeno até o ponto de não lucratividade.

| Desconto | Mínimo Sugerido | Proporção |
|----------|-------------------|-------|
| $5 de desconto | $30+ | ~6:1 |
| $10 de desconto | $50+ | ~5:1 |
| $20 de desconto | $100+ | ~5:1 |
| 15% de desconto | $40+ | Depende do catálogo |

## Limite de Desconto (Máximo de Desconto)

O campo **Máximo de desconto** em **Configuração do Desconto** limita quanto um cupom de porcentagem pode deduzir. Isso se aplica apenas a cupons de tipo porcentagem e impede descontos descontrolados em carrinhos de alto valor.

Exemplo: "20% de desconto, máximo de $50 de desconto"
- Carrinho de $200 = $40 de desconto (20%)
- Carrinho de $300 = $50 de desconto (limitado)
- Carrinho de $1.000 = ainda $50 de desconto (limitado)

Adicione um limite de desconto em qualquer cupom de porcentagem que compartilhe publicamente.

## Regras de Combinar

O campo **Restrições & Regras** (clique para expandir) contém caixas de seleção que controlam como os cupons interagem com outros descontos.

| Configuração | O Que Ele Faz | Quando Habilitar |
|---------|--------------|----------------|
| **Excluir itens em promoção** | O cupom pula produtos já em promoção | A maioria das campanhas — protege margens de promoção |
| **Não pode ser combinado com outros cupons** | Apenas um cupom por pedido | Padrão para a maioria dos cupons |
| **Não pode ser combinado com itens em promoção** | Bloqueia o cupom se o carrinho tiver QUALQUER item em promoção | Campanhas rigorosas onde o cupom substitui os preços de promoção |
| **Apenas para novos clientes** | Apenas clientes com zero pedidos anteriores | Campanhas de boas-vindas/aquisição |

## Restrições de Cliente

Para alvo simples, marque **Apenas para novos clientes** no campo **Restrições & Regras**.

Para alvo avançado, use a tabela **Restrições de Cupom** no final do formulário. Clique em **+ Adicionar outra Restrição de Cupom** para adicionar linhas. Cada restrição tem três campos:

- **Tipo** — A categoria de restrição (dropdown)
- **Valor** — O valor correspondente (separado por vírgula ou JSON)
- **É inclusivo** — Marque = o cliente deve corresponder; não marque = o cliente NÃO deve corresponder

| Tipo | Valor | Inclusivo | Efeito |
|------|-------|-----------|--------|
| user_email_domain | @company.com | Sim | Apenas funcionários da empresa podem usá-lo |
| shipping_country | US,CA | Sim | Apenas clientes dos EUA e Canadá |
| shipping_country | RU | Não | Todos EXCETO Rússia |
| day_of_week | monday,tuesday | Sim | Apenas válido em segunda e terça-feira |
| payment_method | stripe | Sim | Apenas para pagamentos Stripe |

Combine várias linhas para restrições em camadas. Todos os limites inclusivos devem corresponder, e nenhum limite exclusivo pode corresponder, para que o cupom seja aplicado.

## Estratégias de Expiração

Controle quando um cupom expira usando os campos de data e validade.

- **Data de término** — Uma data de corte rígida (ex: 31 de dezembro de 2026).

O cupom para de funcionar às meia-noite.
- **Dias válidos** — Validade rolante a partir da criação ou primeiro uso do cupom.

Substitui a data de término quando definido.


Útil para códigos de boas-vindas: "válido por 30 dias após recebê-lo".

| Estratégia | Data de Término | Dias Válidos | Caso de Uso |
|----------|----------|------------|----------|
| Prazo rígido | Definido | (vazio) | Campanhas sazonais, eventos |
| Janela rolante | (vazio) | 30 | Códigos de boas-vindas, cupons de recompensa |
| Sem validade | (vazio) | (vazio) | Códigos contínuos, descontos para funcionários |

## Previniendo o Abuso

Siga este checklist para manter seus cupons seguros:

- Sempre defina **Máximo de usos por cliente** como 1, a menos que haja uma razão específica para não fazê-lo.
- Defina **Valor mínimo do pedido** em todos os cupons de valor fixo.
- Adicione um **Limite máximo de desconto** em cupons de percentagem públicos.
- Use códigos difíceis de adivinhar para cupons de alto valor — evite códigos óbvios como "DISCOUNT50".
- Monitore as análises de uso em cada cartão de cupom no painel.
- Desative um cupom imediatamente se notar padrões de resgate incomuns.
- Para campanhas de alto valor, use códigos únicos gerados em lote em vez de um único código compartilhado.

## Dicas

- Comece com restrições e afrouxe os limites se o resgate for muito baixo — é mais fácil relaxar as regras do que apertá-las depois que os códigos estiverem em circulação.
- Teste cada cupom com um checkout real antes de distribuí-lo aos clientes.
- Verifique regularmente o painel de análise de cupons para identificar problemas cedo.
- Combine várias restrições para proteção em camadas — por exemplo, limite por cliente + valor mínimo do pedido + limite de desconto + exclua itens em promoção.
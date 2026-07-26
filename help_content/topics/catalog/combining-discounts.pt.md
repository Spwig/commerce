---
title: Combinando Descontos
---

A plataforma oferece quatro tipos de descontos que podem funcionar juntos: vendas de produtos, promoções, códigos de cupom e cartões-presente. Entender como eles interagem ajuda você a executar campanhas eficazes sem resultados inesperados ou descontos duplos acidentais.

> **Cartões-presente ainda não podem ser aplicados no checkout online.** O design descrito abaixo — cartão-presente aplicado por último, após todos os outros descontos — é como funcionará quando esse recurso for lançado. Atualmente, um cartão-presente só pode ser resgatado pessoalmente no **Ponto de Venda**, então as interações descritas para a loja online ainda não se aplicam especificamente aos cartões-presente. Veja o tópico de ajuda **Cartões-presente** para o estado atual.

## As Quatro Camadas de Desconto

Cada tipo de desconto opera em um nível diferente e é visível para os clientes de formas diferentes.

| Camada | Onde É Definido | Como É Aplicado | Visível para o Cliente |
|-------|---------------|-----------------|-------------------|
| **Venda de Produto** | Formulário de edição do produto > Seção de Venda | Altera automaticamente o preço exibido | Sim — mostrado como o preço original riscado |
| **Promoção** | Marketing > Vendas e Promoções | Aplicado automaticamente aos produtos correspondentes | Sim — mostrado como preço de venda nas cartas do produto |
| **Código de Cupom** | Marketing > Cupons | O cliente insere um código no checkout | Apenas no checkout após inserir o código |
| **Cartão-presente** | Resgatado contra o saldo do cartão-presente | Reduz o total do pagamento | Apenas no Ponto de Venda por enquanto (veja a nota acima) |

## Como Funciona a Prioridade

As promoções têm um campo **Prioridade** que aceita valores de 0 em diante. Números mais altos significam prioridade mais alta.

Quando várias promoções correspondem ao mesmo produto, a de **maior prioridade vence**. Elas não se acumulam — apenas uma promoção se aplica por produto.

**Exemplo:** "Venda Flash 50% de desconto" (prioridade 10) e "Venda de Verão 20% de desconto" (prioridade 5) ambas visam todos os produtos. O cliente vê o preço da venda flash de 50%, e não 70% combinado.

Dentro do mesmo nível de prioridade, o sistema seleciona a promoção que oferece o maior desconto ao cliente.

## Regras de Acumulação

A tabela a seguir mostra quais combinações de descontos são permitidas e como controlá-las.

| Combinação | Permitido? | Como Controlar |
|-------------|----------|-------------------|
| Venda de Produto + Promoção | Apenas se habilitado | Marque **"Empilhar com Vendas de Produto"** nas Configurações Avançadas da promoção |
| Promoção + Promoção | Não — a de maior prioridade vence | Defina valores de Prioridade para controlar qual se aplica |
| Promoção + Código de Cupom | Sim | A promoção desconta o preço do produto, o cupom desconta o total do carrinho separadamente |
| Cupom + Cupom | Configurável | A bandeira **"Não pode ser combinado com outros cupons"** do cupom controla isso (habilitada por padrão) |
| Cupom + Itens em Venda | Configurável | A bandeira **"Excluir itens em venda"** do cupom controla isso |
| Cartão-presente + Qualquer Desconto | Sim — sempre | Os cartões-presente são aplicados por último, reduzindo o valor final do pagamento após todos os outros descontos. Atualmente apenas possível no Ponto de Venda — veja a nota acima |

## Cenários Comuns

### Cenário A: Promoção de site + código de cupom

- **Configuração:** 20% de desconto em tudo (promoção) + cliente tem um cupom de $10 de desconto
- **Resultado:** Um produto de $100 se torna $80 (promoção), depois o cupom de $10 é aplicado ao total do carrinho. O cliente paga **$70**.

### Cenário B: Produto em promoção + promoção de site

- **Configuração:** O produto tem uma venda de 30% no nível do produto + existe uma promoção de 20% no site inteiro
- **Resultado (acumulação desativada):** Apenas a venda do produto se aplica. O cliente paga **$70**.
- **Resultado (acumulação ativada):** Ambas se aplicam. 30% de desconto primeiro = $70, depois 20% de desconto = **$56**.

### Cenário C: Duas promoções no mesmo produto

- **Configuração:** "Venda Flash 40% de desconto" (prioridade 10) + "Venda de Verão 20% de desconto" (prioridade 5), ambas visam todos os produtos
- **Resultado:** A Venda Flash vence porque tem prioridade mais alta. O cliente paga **$60** em um produto de $100.

### Cenário D: Cupom em um item em promoção

- **Configuração:** O produto está em promoção com 25% de desconto.


# Resultados de Cupons e Promoções

O cliente insere um código de cupom de 10% que tem a opção "Excluir itens em promoção" ativada.
- **Resultado:** O cupom não se aplica a esse produto.

Se o carrinho tiver itens não em promoção, o cupom se aplica apenas a esses.

## Qual Tipo de Desconto Utilizar

| Objetivo | Abordagem Recomendada | Por quê |
|---------|----------------------|--------|
| Movimentar estoque sazonal | **Promoção** (alvo de categoria ou coleção) | Automático, não requer ação do cliente, visível nas cartas do produto |
| Recompensar um cliente específico | **Código de Cupom** (uso único, limite por cliente) | Alvo específico, rastreável, parece pessoal |
| Oferta rápida para um único produto | **Venda do Produto** (no formulário de edição do produto) | Mais rápido de configurar, não é necessário o assistente de promoção |
| Crédito de loja ou presente | **Cartão-presente** | Baseado em saldo; atualmente redimível apenas no caixa |
| Evento em toda a loja | **Promoção** (alvo de todos os produtos) | Maior alcance, uma configuração cobre tudo |
| Campanha de retenção | **Código de Cupom** (restrições para clientes de primeira ou retorno) | Pode alvo segmentos específicos de clientes |

## Dicas

- **Teste com um carrinho real** — após configurar promoções e cupons, adicione produtos a um carrinho e passe pelo checkout para verificar se os descontos se aplicam conforme o esperado.
- **Verifique a contagem de "produtos afetados"** — na etapa de revisão da promoção, verifique se o número de produtos afetados corresponde ao seu objetivo.
- **Use a prioridade com intenção** — se você executar múltiplas promoções simultaneamente, sempre defina valores de prioridade diferentes para que você controle qual vence.
- **Mantenha o empilhamento desativado por padrão** — ative "Empilhar com Vendas de Produtos" apenas quando quiser especificamente descontos duplos.
- **Documente sua estratégia** — use o campo Descrição da promoção para anotar por que uma promoção existe e como se relaciona com outras promoções ativas.
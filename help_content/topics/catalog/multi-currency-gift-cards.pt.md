---
title: Cartões-presente em múltiplas moedas
---

Se você vende para clientes em多个国家, você pode emitir cartões-presente em moedas específicas. Por exemplo, um cliente da Nova Zelândia pode comprar um cartão-presente de $50 NZD e o destinatário o resgata em NZD — o valor nominal permanece o mesmo, independentemente das flutuações das taxas de câmbio.

Este recurso requer que a multi-moeda esteja habilitada com pelo menos um provedor de taxas de câmbio configurado.

## Como funciona

Quando você define uma **Moeda do Cartão-presente** em um produto de cartão-presente, o sistema converte o preço do produto para a moeda-alvo no momento da compra usando a taxa de câmbio atual. O cartão-presente resultante é denominado em essa moeda e só pode ser resgatado por clientes que estão comprando na mesma moeda.

| Etapa | O que acontece |
|------|-------------|
| **Configuração do produto** | Você define o preço do produto de cartão-presente em sua moeda base e escolhe uma moeda-alvo (por exemplo, NZD) |
| **Compra** | Um cliente compra o cartão-presente. O preço base é convertido para NZD com a taxa de câmbio atual |
| **Cartão-presente criado** | O cartão-presente é emitido com seu valor em NZD (por exemplo, NZ$78,50) |
| **Resgate** | O destinatário aplica o código no checkout enquanto está comprando em NZD. O saldo em NZD é deduzido |

## Pré-requisitos

Antes de configurar cartões-presente em múltiplas moedas, certifique-se de ter:

1. **Multi-moeda habilitada** — Vá para **Configurações > Configurações da Loja** e habilite o suporte a multi-moeda
2. **Moedas suportadas configuradas** — Adicione as moedas que deseja oferecer (por exemplo, NZD, SGD, EUR)
3. **Provedor de taxas de câmbio conectado** — Vá para **Configurações > Taxas de Câmbio** e configure um provedor para que as taxas em tempo real estejam disponíveis

## Configurando um produto de cartão-presente em múltiplas moedas

### Etapa 1: Criar ou editar um produto de cartão-presente

1. Navegue até **Produtos > Todos os Produtos**
2. Clique em **+ Adicionar Produto** ou abra um produto de cartão-presente existente
3. Defina **Tipo de Produto** para **Cartão-presente**

### Etapa 2: Definir a moeda do cartão-presente

1. Clique na guia **Cartão-presente**
2. Configure suas configurações de denominação como de costume (valores fixos, valores personalizados ou ambos)
3. No final da guia Cartão-presente, localize o menu suspenso **Moeda do Cartão-presente**
4. Selecione a moeda-alvo (por exemplo, **NZD - Dólar da Nova Zelândia**)
5. Salve o produto

O menu suspenso mostra todas as moedas habilitadas nas configurações da sua loja. Selecionar **Moeda base da loja (padrão)** significa que os cartões-presente serão emitidos em sua moeda base — este é o comportamento padrão.

### Etapa 3: Definir o preço

Defina o preço do produto em sua moeda base como normalmente faria. Quando um cliente compra esse cartão-presente, o preço é automaticamente convertido para a moeda-alvo usando a taxa de câmbio atual.

**Exemplo:** Sua moeda base é USD. Você cria um produto de cartão-presente com preço de $50 USD e a Moeda do Cartão-presente definida como NZD. Se a taxa de câmbio for 1 USD = 1,57 NZD, o cartão-presente resultante terá um valor de NZ$78,50.

## Correspondência de moeda e resgate

Cartões-presente em múltiplas moedas usam **resgate na mesma moeda** — a moeda ativa de compra do cliente deve corresponder à moeda do cartão-presente.

### O que os clientes experimentam

- Um cliente comprando em **NZD** pode aplicar um cartão-presente em NZD no checkout
- Um cliente comprando em **USD** não pode aplicar um cartão-presente em NZD — eles verão uma mensagem explicando a discordância de moeda
- Os clientes podem alternar sua moeda de compra usando o seletor de moeda em sua loja antes de aplicar o cartão-presente

### Como o saldo funciona

O saldo do cartão-presente sempre é rastreado em sua moeda nativa:

- Um cartão-presente de NZ$78,50 começa com um saldo de NZ$78,50
- Se um cliente fizer uma compra de NZ$30, o saldo restante será NZ$48,50
- O saldo não flutua com as taxas de câmbio — o valor nominal é fixo

Quando o cartão-presente é aplicado no checkout, o sistema converte o desconto para sua moeda base internamente para cálculos de pedidos, mas o saldo do cartão-presente sempre é deduzido em sua moeda nativa.

## Gerenciando cartões-presente em múltiplas moedas

Navegue até **Produtos > Cartões-presente** para visualizar todos os cartões-presente emitidos. Cartões-presente em múltiplas moedas exibem sua moeda nativa:

- **Saldo** mostra na moeda do cartão-presente (por exemplo, NZ$48,50)
- **Transações** registram valores na moeda do cartão-presente
- **Valor inicial** mostra o valor convertido no momento da compra

### Verificando detalhes da taxa de câmbio

Cada transação do cartão-presente registra a taxa de câmbio usada no momento da transação. Isso fornece uma auditoria completa para fins contábeis.

## Exemplos

### Exemplo 1: Cartão-presente regional para a Nova Zelândia

**Cenário:** Você opera a partir dos EUA, mas tem clientes na Nova Zelândia. Deseja vender cartões-presente denominados em NZD.

| Configuração | Valor |
|---------|-------|
| Nome do produto | Cartão-presente da Nova Zelândia |
| Tipo de produto | Cartão-presente |
| Preço | $50,00 (USD — sua moeda base) |
| Tipo de denominação | Denominações Fixas |
| Denominações fixas | 25, 50, 100, 200 |
| Moeda do Cartão-presente | NZD - Dólar da Nova Zelândia |
| Expiração | 365 dias |

Quando um cliente seleciona a denominação de $50:
- O sistema converte $50 USD para NZD com a taxa de câmbio atual
- Um cartão-presente é criado com o equivalente em NZD (por exemplo, NZ$78,50)
- O destinatário pode resgatá-lo enquanto estiver comprando em NZD

### Exemplo 2: Cartões-presente em múltiplas moedas

**Cenário:** Você vende para clientes na Singapura, Austrália e Reino Unido. Crie três produtos de cartão-presente:

1. **Cartão-presente SG** — Moeda do Cartão-presente: SGD
2. **Cartão-presente AU** — Moeda do Cartão-presente: AUD
3. **Cartão-presente UK** — Moeda do Cartão-presente: GBP

Cada produto converte seu preço base para a moeda-alvo no momento da compra. Os clientes em cada região podem resgatar o cartão-presente em sua moeda local.

### Exemplo 3: Oferta mista de cartões-presente

**Cenário:** Você deseja oferecer tanto cartões-presente em moeda base quanto cartões-presente regionais.

- **Cartão-presente da Loja** — Moeda do Cartão-presente: *Moeda base da loja (padrão)* — resgatável em sua moeda base
- **Cartão-presente NZ** — Moeda do Cartão-presente: NZD — resgatável apenas em NZD

Ambos os produtos podem coexistir em seu catálogo. Os clientes veem qual moeda um cartão-presente está denominado ao verificar o saldo.

## Dicas

- Comece com uma moeda regional e teste o fluxo completo (compra, entrega, resgate) antes de adicionar mais moedas.
- A taxa de câmbio no momento da compra determina o valor do cartão-presente. Se as taxas mudarem significativamente, o valor do cartão-presente permanece fixo — isso protege tanto você quanto seus clientes.
- Faça a moeda clara no nome do produto (por exemplo, "Cartão-presente da Nova Zelândia" ou "Cartão-presente (NZD)") para que os clientes saibam o que estão comprando.
- Cartões-presente sem uma moeda definida continuam a funcionar exatamente como antes em sua moeda base — os produtos existentes não são afetados.
- Monitore seu provedor de taxas de câmbio para garantir que as taxas estejam atualizadas. Taxas desatualizadas podem levar a cartões-presente supervalorizados ou subvalorizados.
- Considere cuidadosamente suas denominações. Uma denominação de $25 USD converte-se aproximadamente em NZ$39 — denominações arredondadas na moeda-alvo podem parecer melhores. Você pode criar produtos separados com denominações que sejam números arredondados na moeda-alvo.
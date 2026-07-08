---
title: Programa de Afiliados
---

O programa de afiliados permite que você recrute parceiros que promovem seus produtos e ganham comissões pelas vendas que geram. Os afiliados compartilham links de indicação únicos, e o Spwig rastreia automaticamente os cliques, atribui pedidos e calcula comissões.

![Programas de afiliados](/static/core/admin/img/help/affiliate-program/program-list.webp)

## Como Funciona

1. Você cria um ou mais **programas de afiliados** com taxas de comissão e regras
2. Os afiliados **se cadastram** por meio de um portal público ou são adicionados manualmente
3. Cada afiliado recebe um **link de indicação único** com um código de rastreamento
4. Quando um cliente clica no link e faz uma compra, uma **comissão** é registrada
5. Você revisa e aprova as comissões, depois processa **pagamentos**

## Criando um Programa

Navegue até **Marketing > Programas de Afiliados** e clique em **Adicionar Programa**.

### Configurações do Programa

| Configuração | Descrição |
|---------|-------------|
| **Nome** | Nome do programa visível aos afiliados (ex: "Programa de Parceiros") |
| **Tipo de Comissão** | **Percentual** do total da ordem ou **Valor Fixo** por venda |
| **Taxa de Comissão** | O percentual ou valor fixo que os afiliados ganham |
| **Duração do Cookie** | Quantos dias o cookie de rastreamento de indicação dura (padrão: 30 dias) |
| **Mínimo para Pagamento** | Valor mínimo de ganhos antes que um afiliado possa solicitar um pagamento |
| **Aprovar Afiliados Automaticamente** | Aceitar automaticamente novas solicitações de afiliados ou exigir aprovação manual |
| **Status** | Ativo, pausado ou fechado |

### Tipos de Comissão

- **Percentual** — Os afiliados ganham um percentual do subtotal de cada ordem indicada (ex: 10% de uma ordem de $100 = $10 de comissão)
- **Valor Fixo** — Os afiliados ganham um valor fixo por venda, independentemente do valor da ordem (ex: $5 por venda)

## Gerenciando Afiliados

Navegue até **Marketing > Afiliados** para visualizar e gerenciar contas de afiliados.

### Detalhes do Afiliado

Cada afiliado tem:
- **Código do Afiliado** — Um código único usado em URLs de indicação (gerado automaticamente ou personalizado)
- **Link de Indicação** — O URL completo de rastreamento que o afiliado compartilha (ex: `yourstore.com/?ref=CODE`)
- **Status** — Pendente, aprovado ou rejeitado
- **Método de Pagamento** — Como o afiliado recebe os pagamentos (PayPal ou transferência bancária)
- **Membros do Programa** — Quais programas o afiliado pertence

### Adicionando Afiliados Manualmente

1. Clique em **Adicionar Afiliado**
2. Selecione uma conta de cliente existente ou crie uma nova
3. Atribua o afiliado a um ou mais programas
4. Defina o código do afiliado (ou deixe em branco para gerar automaticamente)

### Portal do Afiliado

Os afiliados acessam um portal público onde podem:
- Ver seu painel com ganhos e estatísticas de cliques
- Copiar seus links de indicação
- Rastrear histórico de comissões
- Solicitar pagamentos

O URL do portal está automaticamente disponível em `/affiliate/` no seu loja.

## Rastreamento e Comissões

### Como Funciona o Rastreamento

1. Um cliente clica em um link de indicação de um afiliado
2. Um cookie de rastreamento é definido no navegador do cliente (com duração configurada para o cookie)
3. Se o cliente fizer um pedido dentro do período de validade do cookie, a ordem é atribuída ao afiliado
4. Um registro de comissão é criado com o status **Pendente**

### Status de Comissões

| Status | Descrição |
|--------|-------------|
| **Pendente** | Comissão registrada, aguardando revisão |
| **Aprovada** | Verificada e pronta para pagamento |
| **Rejeitada** | Comissão negada (ex: pedido fraudulento ou item devolvido) |
| **Paga** | Comissão incluída em um pagamento concluído |

### Revisando Comissões

Navegue até **Marketing > Comissões** para revisar comissões pendentes:

1. Verifique os detalhes do pedido para confirmar que a venda é legítima
2. Clique em **Aprovar** para confirmar ou **Rejeitar** com uma razão
3. As comissões aprovadas se acumulam no saldo de pagamento do afiliado

## Pagamentos

Quando o saldo de comissão aprovado de um afiliado atinge o limite mínimo de pagamento, você pode processar um pagamento.

### Processando Pagamentos

1. Navegue até **Marketing > Pagamentos**
2. Selecione afiliados com saldos disponíveis
3. Escolha o método de pagamento:
   - **PayPal** — Envie os fundos diretamente para o e-mail PayPal do afiliado
   - **Transferência Bancária** — Registre uma transferência bancária manual
4. Confirme e processe o pagamento
5. O status do pagamento é atualizado para **Concluído** e as comissões são marcadas como **Pagas**

### Provedores de Pagamentos

O Spwig integra-se com provedores de pagamento para pagamentos automatizados:
- **PayPal** — Pagamentos em massa automatizados via API do PayPal
- **Airwallex** — Pagamentos internacionais com taxas de câmbio competitivas
- **Manual** — Registre pagamentos processados fora do Spwig

## Links de Indicação

Cada link de indicação de um afiliado segue esse padrão:

```
https://yourstore.com/?ref=AFFILIATE_CODE
```

Os afiliados também podem criar links para produtos ou categorias específicas:

```
https://yourstore.com/products/shoe-name/?ref=AFFILIATE_CODE
```

O parâmetro `ref` funciona em qualquer página — o cookie de rastreamento é definido independentemente da página de destino.

## Análise do Programa

O painel do programa de afiliados mostra:
- **Total de Cliques** — Quantas vezes os links de indicação foram clicados
- **Total de Pedidos** — Pedidos atribuídos aos afiliados
- **Total de Comissões** — Soma de todas as comissões (pendentes, aprovadas e pagas)
- **Afiliados Ativos** — Número de afiliados aprovados que estão gerando indicações

## Dicas

- Comece com uma **comissão baseada em percentual** (5–15%) — ela se ajusta naturalmente com o valor da ordem e é fácil para os afiliados entenderem.
- Defina uma **duração do cookie de 30 dias** como base — isso dá aos clientes tempo para retornar e concluir a compra, ainda assim atribuindo a venda ao afiliado.
- Ative **aprovação automática** para programas públicos para reduzir a fricção, ou use aprovação manual para programas por convite onde você deseja verificar cada afiliado.
- Defina um **limite mínimo de pagamento** razoável (ex: $25–$50) para evitar processar muitas transações pequenas.
- Personalize o **portal do afiliado** para combinar com sua marca — os afiliados são mais propensos a promover sua loja quando a experiência parece profissional.
- Monitore regularmente as comissões para **padrões fraudulentos** como indicações auto-referidas, taxas de devolução anormalmente altas ou volumes de cliques suspeitos.
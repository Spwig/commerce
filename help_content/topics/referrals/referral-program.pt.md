---
title: Programa de Indicações
---

O programa de indicações permite que seus clientes existentes compartilhem um link de indicação único com seus amigos e familiares. Quando um amigo indicado fizer sua primeira compra qualificada, tanto o indicador quanto o novo cliente podem receber uma recompensa — promovendo a aquisição de novos clientes por meio de indicações orais.

## Como o programa de indicações funciona

1. Um cliente compartilha seu link de indicação único (ou código) com um amigo.
2. O amigo clica no link e é rastreado por meio de um cookie por até 30 dias (configurável).
3. O amigo se inscreve e faz sua primeira compra qualificada.
4. O sistema cria um registro de atribuição de indicação e executa verificações de fraude e elegibilidade.
5. Se a atribuição for aprovada, recompensas são concedidas a ambas as partes.

Sua loja tem uma única configuração do programa de indicações. Navegue até **Marketing > Programa de Indicações** para configurá-lo.

## Configurando seu programa de indicações

### Status do programa

O programa tem três estados:

- **Rascunho** — O programa está sendo configurado, mas ainda não está ativo. Os links de indicação estão inativos.
- **Ativo** — O programa está ativo. Os clientes podem compartilhar links e ganhar recompensas.
- **Pausado** — O programa está temporariamente parado. As atribuições existentes ainda são processadas, mas nenhuma nova indicação é rastreada.

Defina o **Status** como **Ativo** quando estiver pronto para lançar. Você pode pausá-lo a qualquer momento.

### Configuração de recompensas

Defina as recompensas que são concedidas quando uma indicação for convertida. O programa suporta **recompensas de ambos os lados** — ou seja, você pode recompensar tanto o indicador (o cliente que compartilhou o link) quanto o indicado (o novo cliente que usou o link).

Configure recompensas para cada destinatário no campo **Configuração de Recompensas**. Os tipos de recompensas disponíveis são:

| Tipo de Recompensa | Descrição |
|-------------------|-----------|
| **Crédito de Loja** | Adiciona crédito à carteira do cliente, utilizável em pedidos futuros |
| **Código de Cupom** | Gera um código de voucher de desconto único |
| **Desconto em Percentual** | Emite um desconto em percentual para uso no checkout |
| **Benefício Exclusivo** | Um benefício personalizado (ex.: presente gratuito, acesso prioritário) — descrito no campo de descrição da recompensa |

Recompensas de Código de Cupom e Desconto em Percentual estão bloqueadas para o cliente que as ganhou — o código do voucher só funciona quando esse cliente estiver conectado. Se um indicador compartilhar seu código de recompensa com alguém em vez do link de indicação, o amigo não poderá usá-lo; apenas o link de indicação em si deve ser compartilhado.

**Exemplo de configuração** — $10 de crédito de loja para o indicador e $10 de desconto para o novo cliente:

```json
{
  "referrer": {"kind": "credit", "amount": 10},
  "referee": {"kind": "discount", "amount": 10},
  "double_sided": true
}
```

Defina `"double_sided": false` se desejar recompensar apenas o indicador.

### Regras de elegibilidade

As regras de elegibilidade determinam quais indicações são elegíveis para recompensas. Configure-as no campo **Regras de Elegibilidade**:

| Regra | O que ela faz |
|-------|----------------|
| `new_customer_only` | Se `true`, o amigo indicado deve ser um novo cliente (sem pedidos anteriores) |
| `min_order_value` | O valor mínimo do pedido (em sua moeda da loja) que o amigo indicado deve gastir |
| `exclude_discounts` | Se `true`, pedidos em que o cliente indicado usou um voucher não são elegíveis |
| `exclude_staff` | Se `true`, contas de funcionários não podem ser indicadores ou indicados |

**Exemplo** — apenas novos clientes, valor mínimo de $40, funcionários excluídos:

```json
{
  "new_customer_only": true,
  "min_order_value": 40.0,
  "exclude_discounts": false,
  "exclude_staff": true
}
```

### Configuração de tempo

O campo **Configuração de Tempo** controla quando as recompensas são concedidas após um pedido qualificado:

| Configuração | O que ela faz |
|--------------|----------------|
| `issue_on` | Quando conceder a recompensa: `signup` (imediatamente no registro), `first_purchase` (imediatamente após o pedido) ou `post_refund` (após o período de reembolso expirar) |
| `refund_window_days` | Quantos dias aguardar antes de conceder recompensas ao usar `post_refund` (padrão: 14 dias) |

Usar `post_refund` é a abordagem mais cautelosa — ele espera até que o período de devolução tenha passado antes de emitir recompensas, reduzindo o risco de recompensar pedidos que depois são reembolsados.

### Limites e caps

Impedir que um único referenciador ganhe recompensas ilimitadas definindo limites no campo **Caps & Limits**:

| Configuração | O que ela faz |
|---------|--------------|
| `monthly_per_referrer` | Número máximo de referências bem-sucedidas recompensadas por mês, por referenciador |
| `lifetime_per_referrer` | Número total máximo de referências bem-sucedidas recompensadas já, por referenciador |
| `max_reward_per_order` | Valor máximo de recompensa (em sua moeda de loja) emitido para uma única conversão de referência |

**Exemplo** — 20 referências por mês, 200 ao longo da vida, $50 máximo de recompensa por conversão:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configuração de rastreamento

Configure como os links de referência são rastreados no campo **Tracking Configuration**:

| Configuração | O que ela faz |
|---------|--------------|
| `cookie_ttl_days` | Quantos dias o cookie de rastreamento de referência permanece ativo após um amigo clicar no link (padrão: 30) |
| `attribution` | Método de atribuição — atualmente `last_touch` (o clique mais recente no link de referência é creditado) |

### Política de fraude

O sistema de detecção de fraude classifica automaticamente cada atribuição de referência para risco antes de aprova-la. Configure a política no campo **Fraud Policy**:

| Configuração | O que ela faz |
|---------|--------------|
| `policy` | Rigidez geral: `strict`, `balanced` ou `lenient` |
| `auto_reject_threshold` | Pontuação de risco (0–100) acima da qual as atribuições são automaticamente rejeitadas (padrão: 80) |
| `auto_approve_threshold` | Pontuação de risco abaixo da qual as atribuições são automaticamente aprovadas (padrão: 30) |
| `check_ip` | Se `true`, verifica se o referenciador e o referenciado compartilham o mesmo endereço IP |
| `check_device` | Se `true`, verifica se há impressões digitais de dispositivos compartilhadas entre referenciador e referenciado |
| `check_velocity` | Se `true`, monitora para taxas de referência anormalmente altas de uma única fonte |
| `velocity_window_hours` | Janela de tempo (em horas) para verificação de velocidade |
| `max_referrals_per_window` | Número máximo de referências permitidas de uma única fonte dentro da janela de velocidade |

Atribuições com uma pontuação de risco entre os limites de rejeição automática e aprovação automática entram em um status **Pending** e requerem revisão manual.

### Termos e condições

Insira quaisquer termos e condições legais para o programa no campo **Terms & Conditions**. Esse texto é exibido aos clientes quando eles visualizam o programa de referência. Formatação em markdown é suportada.

## Visualizando atribuições de referência

Navegue até **Marketing > Referral Attributions** para ver todos os casos de referência — o link entre um referenciador e um cliente referenciado.

![Lista de atribuições de referência](/static/core/admin/img/help/referral-program/attribution-list.webp)

Cada atribuição mostra o referenciador, o cliente referenciado, o primeiro pedido que eles fizeram, o status atual e a pontuação de risco.

### Status de atribuição

| Status | O que significa |
|--------|---------------|
| **Pending** | Aguardando revisão — a pontuação de risco está na faixa de revisão manual |
| **Approved** | A referência é válida — recompensas já foram ou serão emitidas |
| **Rejected** | A referência não qualificou ou foi marcada como fraudulenta |
| **Expired** | A referência não foi convertida dentro da janela de rastreamento |

### Aprovar ou rejeitar atribuições manualmente

Para atribuições no status **Pending**, você pode aprovar ou rejeitar manualmente abrindo o registro da atribuição e usando os botões de ação. Ao rejeitar, escolha um **Motivo de Rejeição**:

- Referência própria
- Não é um novo cliente
- Abaixo do valor mínimo do pedido
- E-mail descartável
- Limite excedido
- Risco de fraude
- Pedido reembolsado ou cancelado
- Rejeição manual

Você também pode adicionar **Notas de Rejeição** para seus próprios registros.

### Filtrar por nível de risco

Use o filtro **Nível de Risco** no painel lateral para se concentrar em atribuições de alto risco que precisam de revisão:

- Risco Baixo (pontuação 0–30) — Aprovado automaticamente
- Risco Médio (pontuação 31–70) — Revisão manual
- Risco Alto (pontuação 71–89) — Revisão manual, trate com cuidado
- Risco Muito Alto (pontuação 90+) — Recusado automaticamente

## Visualizando recompensas emitidas

Navegue até **Marketing > Recompensas Emitidas** para ver todas as recompensas que foram emitidas como resultado de atribuições aprovadas.

Cada entrada de recompensa mostra o cliente, se ele é o indicador ou o indicado, o tipo e o valor da recompensa, e o status atual de resgate.

### Status de recompensas

| Status | O que significa |
|--------|---------------|
| **Pendente** | A recompensa foi criada, mas ainda não foi entregue ao cliente |
| **Emitida** | A recompensa está ativa e disponível para o cliente usar |
| **Resgatada** | O cliente utilizou a recompensa |
| **Expirada** | A recompensa passou da data de validade sem ser usada |
| **Revogada** | A recompensa foi cancelada manualmente (por exemplo, se o pedido original foi reembolsado após a recompensa ter sido emitida) |

### Revogando uma recompensa

Se uma recompensa precisar ser cancelada — por exemplo, o pedido qualificador foi devolvido — abra o registro da recompensa e use a ação **Revogar**. Adicione uma nota explicando o motivo da revogação para seus registros.

## Dicas

- Comece com a configuração de horário `post_refund`. Esperar pelo término do período de devolução antes de emitir recompensas impede que pedidos que sejam devolvidos sejam recompensados.
- A política de fraude `balanced` é uma boa opção padrão para a maioria das lojas. Mude para `strict` se você notar um aumento inusitado de indicações vindo de um pequeno número de contas.
- Defina limites mensais e de toda a vida realistas. Se o valor da recompensa for alto, um limite de 10–20 por mês por indicador é razoável para evitar abusos.
- Revise as atribuições **Pendentes** semanalmente. Deixar as atribuições pendentes por muito tempo sem revisão pode frustrar indicadores legítimos que estão esperando por sua recompensa.
- Use o filtro **Nível de Risco** para priorizar sua fila de revisão manual — comece com as atribuições de risco muito alto antes de passar para as de risco médio.
- Mantenha seus Termos & Condições curtos e em linguagem simples. Os clientes são mais propensos a participar quando entendem claramente as regras.
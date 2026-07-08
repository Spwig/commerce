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

As regras de elegibilidade determinam quais indicações qualificam-se para recompensas. Configure-as no campo **Regras de Elegibilidade**:

| Regra | O que ela faz |
|-------|----------------|
| `new_customer_only` | Se `true`, o amigo indicado deve ser um novo cliente (sem pedidos anteriores) |
| `min_order_value` | O valor mínimo do pedido (em sua moeda da loja) que o amigo indicado deve gastir |
| `exclude_discounts` | Se `true`, pedidos em que o cliente indicado usou um voucher não qualificam |
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

Usar `post_refund` é a abordagem mais cautelosa — ele aguarda até que o período de devolução tenha passado antes de conceder recompensas, reduzindo o risco de recompensar pedidos que sejam posteriormente reembolsados.

### Limites e tetos

Impedir que um único indicador ganhe recompensas ilimitadas definindo tetos no campo **Limites e Tetos**:

| Configuração | O que ela faz |
|---------|--------------|
| `monthly_per_referrer` | Número máximo de indicações bem-sucedidas recompensadas por mês, por indicador |
| `lifetime_per_referrer` | Número total máximo de indicações bem-sucedidas recompensadas ao longo da vida, por indicador |
| `max_reward_per_order` | Valor máximo de recompensa (em moeda do seu loja) concedido por conversão de indicação |

**Exemplo** — 20 indicações por mês, 200 ao longo da vida, $50 máximo de recompensa por conversão:

```json
{
  "monthly_per_referrer": 20,
  "lifetime_per_referrer": 200,
  "max_reward_per_order": 50
}
```

### Configuração de rastreamento

Configure como os links de indicação são rastreados no campo **Configuração de Rastreamento**:

| Configuração | O que ela faz |
|---------|--------------|
| `cookie_ttl_days` | Quantos dias o cookie de rastreamento de indicação permanece ativo após um amigo clicar no link (padrão: 30) |
| `attribution` | Método de atribuição — atualmente `last_touch` (o clique mais recente no link de indicação é creditado) |

### Política de fraude

O sistema de detecção de fraude classifica automaticamente cada atribuição de indicação para risco antes de aprova-la. Configure a política no campo **Política de Fraude**:

| Configuração | O que ela faz |
|---------|--------------|
| `policy` | Rigidez geral: `strict`, `balanced` ou `lenient` |
| `auto_reject_threshold` | Pontuação de risco (0–100) acima da qual as atribuições são automaticamente rejeitadas (padrão: 80) |
| `auto_approve_threshold` | Pontuação de risco abaixo da qual as atribuições são automaticamente aprovadas (padrão: 30) |
| `check_ip` | Se `true`, verifica se o indicador e o indicado compartilham o mesmo endereço IP |
| `check_device` | Se `true`, verifica se há impressões digitais de dispositivos compartilhados entre indicador e indicado |
| `check_velocity` | Se `true`, monitora para taxas de indicação anormalmente altas de uma única fonte |
| `velocity_window_hours` | Janela de tempo (em horas) para verificação de velocidade |
| `max_referrals_per_window` | Número máximo de indicações permitidas de uma única fonte dentro da janela de velocidade |

Atribuições com uma pontuação de risco entre os limites de rejeição automática e aprovação automática entram em um status **Pendente** e exigem revisão manual.

### Termos e condições

Insira quaisquer termos e condições legais para o programa no campo **Termos & Condições**. Esse texto é exibido aos clientes quando eles visualizam o programa de indicação. Formatação em markdown é suportada.

## Visualizando atribuições de indicação

Navegue até **Marketing > Atribuições de Indicação** para ver todos os casos de indicação — o link entre um indicador e um cliente indicado.

![Lista de atribuições de indicação](/static/core/admin/img/help/referral-program/attribution-list.webp)

Cada atribuição mostra o indicador, o cliente indicado, a primeira ordem que eles fizeram, o status atual e a pontuação de risco.

### Status de atribuição

| Status | O que significa |
|--------|---------------|
| **Pendente** | Aguardando revisão — a pontuação de risco está na faixa de revisão manual |
| **Aprovado** | Indicação válida — recompensas já foram ou serão concedidas |
| **Rejeitado** | Indicação não qualificou ou foi marcada como fraudulenta |
| **Expirado** | A indicação não foi convertida dentro da janela de rastreamento |

### Aprovar ou rejeitar atribuições manualmente

Para atribuições no status **Pendente**, você pode aprovar ou rejeitar manualmente abrindo o registro da atribuição e usando os botões de ação. Ao rejeitar, escolha um **Motivo de Rejeição**:

- Indicação própria
- Não é um novo cliente
- Valor da ordem abaixo do mínimo
- E-mail descartável
- Limite excedido
- Risco de fraude
- Ordem reembolsada ou cancelada
- Rejeição manual

Você também pode adicionar **Notas de Rejeição** para seus próprios registros.

### Filtrar por nível de risco

Use o filtro **Nível de Risco** no painel lateral para se concentrar em atribuições de alto risco que precisam de revisão:

- Baixo risco (pontuação 0–30) — Aprovado automaticamente
- Médio risco (pontuação 31–70) — Revisão manual
- Alto risco (pontuação 71–89) — Revisão manual, trate com cuidado
- Muito alto risco (pontuação 90+) — Rejeição automática

## Visualizando recompensas concedidas

Navegue até **Marketing > Recompensas Emitidas** para ver todas as recompensas que foram emitidas como resultado de atribuições aprovadas.

Cada entrada de recompensa mostra o cliente, se ele é o indicador ou o indicado, o tipo e o valor da recompensa, e o status atual de resgate.

### Status de recompensas

| Status | O que significa |
|--------|---------------|
| **Pendente** | A recompensa foi criada, mas ainda não foi entregue ao cliente |
| **Emitida** | A recompensa está ativa e disponível para o cliente usar |
| **Resgatada** | O cliente usou a recompensa |
| **Expirada** | A recompensa passou da data de validade sem ser usada |
| **Revogada** | A recompensa foi cancelada manualmente (por exemplo, se o pedido original foi reembolsado após a emissão da recompensa) |

### Revogar uma recompensa

Se uma recompensa precisar ser cancelada — por exemplo, o pedido qualificador foi devolvido — abra o registro da recompensa e use a ação **Revogar**. Adicione uma nota explicando o motivo da revogação para seus registros.

## Dicas

- Comece com a configuração de horário `post_refund`. Esperar pelo fim do período de devolução antes de emitir recompensas impede que pedidos que sejam devolvidos sejam recompensados.
- A política de fraude `balanced` é uma boa opção padrão para a maioria das lojas. Mude para `strict` se você notar um aumento anormal de indicações vindo de um pequeno número de contas.
- Defina limites mensais e de toda a vida realistas. Se o valor da recompensa for alto, um limite de 10–20 por mês por indicador é razoável para evitar abusos.
- Revise as atribuições **Pendentes** semanalmente. Deixar as atribuições pendentes sem revisão por muito tempo pode frustrar indicadores legítimos que estão esperando por sua recompensa.
- Use o filtro **Nível de Risco** para priorizar sua fila de revisão manual — comece com as atribuições de alto risco antes de passar para as de risco médio.
- Mantenha seus Termos & Condições curtos e em linguagem simples. Os clientes são mais propensos a participar quando entendem as regras claramente.
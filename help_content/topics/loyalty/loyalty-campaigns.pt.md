---
title: Campanhas de Fidelidade
---

Campanhas de fidelidade permitem que você execute promoções com prazo limitado e recompensas automatizadas que vão além das regras de acumulação comuns. Use-as para executar fins de semana com pontos duplos, recompensar clientes no aniversário deles, recuperar compradores inativos e entregar bônus direcionados a grupos específicos de membros.

Cada campanha define um gatilho ou agendamento, os membros a que se aplica e as ações a serem executadas. Uma vez ativa, as campanhas são acionadas automaticamente — você configura uma vez e o Spwig cuida do resto.

## Tipos de campanhas

| Tipo | Quando é acionada |
|------|------------------|
| **Baseada em Gatilho** | Quando um evento específico ocorre (ex.: uma compra é feita, um aniversário é detectado) |
| **Agendada** | Em um agendamento repetitivo (diário, semanal, mensal) |
| **Manual** | Apenas quando você a executar explicitamente do admin |
| **Comportamental** | Quando um cliente corresponde a um padrão comportamental (ex.: navegação sem compra) |

## Criando uma campanha

Navegue até **Promotions > Loyalty Campaigns** e clique em **+ Add Loyalty Campaign**.

### Etapa 1: informações básicas

- **Nome** — um nome claro e descritivo visível apenas no admin (ex.: `Birthday Bonus — 200 Points`)
- **Slug** — gerado automaticamente a partir do nome; usado internamente
- **Descrição** — notas opcionais sobre o propósito da campanha
- **Tipo de Campanha** — selecione o tipo da tabela acima

### Etapa 2: gatilho ou agendamento

**Para campanhas baseadas em gatilho**, defina o **Evento de Gatilho** que aciona a campanha. Os gatilhos disponíveis incluem:

| Gatilho | Descrição |
|---------|-----------|
| Order Placed | Acionado quando um membro completa um pedido |
| First Purchase | Acionado no primeiro pedido de um membro |
| Customer Birthday | Acionado no aniversário do membro |
| Membership Anniversary | Acionado anualmente no aniversário de adesão do membro |
| Cart Abandoned | Acionado quando um carrinho é abandonado sem finalização |
| Tier Promotion | Acionado quando um membro avança para uma camada superior |
| Points Expiring Soon | Acionado quando um membro tem pontos prestes a expirar |
| Inactive 90 Days | Acionado quando um membro não fez uma compra em 90 dias |
| Review Submitted | Acionado quando um membro submete uma avaliação de produto |
| Referral Converted | Acionado quando um cliente referenciado faz uma compra |

Você pode adicionar **Condições de Gatilho** como um objeto JSON para filtrar ainda mais quando a campanha é acionada. Por exemplo, para acionar apenas pedidos acima de $100:

```json
{
  "min_order_amount": 100
}
```

**Para campanhas agendadas**, defina o **Tipo de Agendamento** (Diário, Semanal, Mensal ou Cron Personalizado) e configure o horário no campo **Configuração do Agendamento**:

```json
{
  "hour": 9,
  "minute": 0
}
```

### Etapa 3: ações

O campo **Ações** define o que acontece quando a campanha é acionada. Insira um array JSON de objetos de ação. A ação mais comum é conceder pontos bônus:

```json
[
  {
    "type": "award_points",
    "points": 200,
    "description": "Birthday bonus — thank you for being a member!"
  }
]
```

Outras ações disponíveis incluem enviar uma notificação por e-mail ou conceder um distintivo. Consulte a documentação do componente do seu provedor para a lista completa.

### Etapa 4: direcionamento

Controle quais membros a campanha se aplica usando os campos de direcionamento:

- **Direcionar Todos os Membros** — marcado por padrão; a campanha se aplica a todos os membros ativos de fidelidade
- **Direcionar Segmento** — restringir a campanha a membros de um segmento específico (veja [Segments](#managing-member-segments) abaixo)
- **Direcionar Camadas** — restringir a campanha a membros de camadas específicas de fidelidade

### Etapa 5: limites e cooldowns

- **Máximo de Gatilhos por Membro** — quantas vezes o mesmo membro pode se beneficiar dessa campanha. Defina como `1` para bônus únicos, como uma recompensa de aniversário. Deixe em branco para ilimitado.
- **Dias de Cooldown** — dias mínimos entre acionamentos da campanha para o mesmo membro. Por exemplo, defina como `365` para impedir que uma campanha de aniversário seja acionada mais de uma vez por ano.

### Etapa 6: datas da campanha

Defina **Data de Início** e **Data de Fim** para tornar a campanha limitada a um período de tempo. Deixe ambas em branco para uma campanha contínua.

Campanhas podem estar em um desses status:

| Status | Descrição |
|--------|-------------|
| **Rascunho** | Criado, mas ainda não ativo; seguro para configurar e testar |
| **Ativo** | Em execução e será acionado quando as condições forem atendidas |
| **Pausado** | Parado temporariamente, sem perder a configuração |
| **Encerrado** | Passou da data de término; não aciona mais |
| **Arquivado** | Oculto da lista ativa, mas preservado para registros |

Depois de preencher todos os campos, clique em **Salvar**. Em seguida, altere o status para **Ativo** para iniciar a campanha.

## Exemplos práticos

### Exemplo: pontos duplos no fim de semana

**Cenário:** Conceder 2x pontos em todas as compras realizadas durante um fim de semana específico.

| Campo | Valor |
|-------|-------|
| Nome | `Double Points Weekend — March` |
| Tipo de Campanha | Baseado em Gatilho |
| Evento de Gatilho | Pedido Realizado |
| Ações | `["{\"type\": \"award_points_multiplier\", \"multiplier\": 2.0}"]` |
| Data de Início | Noite de sexta-feira |
| Data de Término | Meia-noite de domingo |
| Alvo Todos os Membros | Marcado |

### Exemplo: bônus de aniversário

**Cenário:** Conceder 200 pontos bônus a cada membro do programa de fidelidade no seu aniversário.

| Campo | Valor |
|-------|-------|
| Nome | `Birthday Bonus` |
| Tipo de Campanha | Baseado em Gatilho |
| Evento de Gatilho | Aniversário do Cliente |
| Ações | `["{\"type\": \"award_points\", \"points\": 200, \"description\": \"Happy birthday from us!\"}"]` |
| Máximo de Gatilhos por Membro | 1 |
| Dias de Resfriamento | 365 |
| Alvo Todos os Membros | Marcado |

### Exemplo: campanha de recuperação de clientes

**Cenário:** Enviar 100 pontos bônus aos membros que não compraram em 90 dias.

| Campo | Valor |
|-------|-------|
| Nome | `90-Day Win-Back Bonus` |
| Tipo de Campanha | Baseado em Gatilho |
| Evento de Gatilho | Inativo há 90 Dias |
| Ações | `["{\"type\": \"award_points\", \"points\": 100, \"description\": \"We miss you — here are some bonus points\"}"]` |
| Máximo de Gatilhos por Membro | 1 |
| Dias de Resfriamento | 180 |
| Alvo Todos os Membros | Marcado |

## Gerenciamento de segmentos de membros

Os segmentos permitem que você direcione campanhas a grupos específicos de membros do programa de fidelidade. Navegue até **Promotions > Loyalty Segments** para gerenciá-los.

### Tipos de segmento

| Tipo | Descrição |
|------|-------------|
| **Baseado em Regras** | Membros determinados por regras (ex: membros com mais de 1.000 pontos) |
| **Cálculo Dinâmico** | Membros calculados sob demanda com base em critérios em tempo real |
| **Atribuição Manual** | Membros são adicionados ao segmento manualmente |

### Criando um segmento

1. Navegue até **Promotions > Loyalty Segments** e clique em **+ Adicionar Segmento de Fidelidade**
2. Preencha:
   - **Nome** — nome descritivo (ex: `High-Value Customers`, `Silver Tier Members`)
   - **Slug** — gerado automaticamente
   - **Tipo de Critério** — como a membresia é determinada
   - **Configuração de Critério** — objeto JSON definindo as regras de membresia
3. Clique em **Salvar**

#### Exemplo: segmento para membros com 500+ pontos

```json
{
  "min_available_points": 500
}
```

#### Exemplo: segmento apenas para membros da camada Gold

```json
{
  "tier_slugs": ["gold"]
}
```

A coluna **Member Count** na lista de segmentos mostra quantos membros atualmente correspondem. Clique em um segmento e use a ação **Refresh Member Count** para recalculá-la se seus dados tiverem mudado.

## Rastreamento do desempenho da campanha

### Histórico de execução da campanha

Navegue até **Promotions > Campaign Executions** para ver um registro de cada vez que uma campanha foi acionada para qualquer membro. Cada registro de execução mostra qual campanha foi executada, para qual membro foi executada e o resultado.

### Revisão do alcance de uma campanha

Abra qualquer registro de campanha para ver a contagem de **Times Triggered** e quando a campanha foi acionada pela última vez. Isso lhe dá uma visão rápida de quantos membros se beneficiaram da campanha.

## Dicas

Preserve todos os formatos de marcação, caminhos de imagem, blocos de código e termos técnicos.

- Crie campanhas com o status **Rascunho** primeiro para que você possa revisar todas as configurações antes que fiquem ativas
- Use **Max Triggers Per Member** em todas as campanhas de bônus únicas (aniversário, primeira compra, cadastro) para evitar que os clientes ganhem o bônus mais de uma vez
- Combine um **Target Segment** com uma campanha baseada em gatilho para executar promoções exclusivas por nível — por exemplo, pontos duplos em compras apenas para membros Ouro e Platina
- Defina um valor de **Cooldown Days** em campanhas de recuperação de clientes para que os membros não sejam sobrecarregados se fizerem uma compra pequena e depois ficarem inativos novamente em breve
- A lista de campanhas é sua melhor ferramenta para manter o controle do que está ativo atualmente — revise-a antes de lançar novas ofertas para garantir que as campanhas não se sobreponham acidentalmente
- Arquive campanhas encerradas em vez de excluí-las para que você tenha um registro histórico do que promoções você executou e quando
---
title: Jornadas Disparadas
---

<!-- screenshots-needed:
- url: /admin/campaigns/journeys/{journey_id}/report/
  filename: journey-report.webp
  description: A página de relatório da Jornada para uma jornada com histórico de inscrição significativo — os cartões do funil de inscrição (Inscrito/Ativo agora/Concluído/Exitos) e o cartão de receita atribuída mostrando números diferentes de zero, mais a tabela "Receita por etapa" (Etapa/Receita/Ordens/Enviadas/Abriram/Clicaram) com pelo menos uma etapa simples e uma etapa A/B, ambas mostrando contagens reais de Enviadas/Abriram/Clicaram.
  save-to: core/static/core/admin/img/help/triggered-journeys/
  viewport: 1440x900
-->

Os **Journeys** do Campaign Studio são sequências de e-mails automatizadas e de vários passos que começam sozinhas sempre que um cliente faz algo específico — cadastrar-se, fazer um pedido, deixar itens no carrinho, ficar inativo por um tempo ou ter um pedido entregue. Em vez de lembrar de enviar um e-mail de boas-vindas, um lembrete de recuperação de carrinho ou um pedido de avaliação manualmente, você cria a sequência uma vez e o Spwig a executa para cada cliente que se enquadra, enquanto a jornada estiver ativa.

## Três maneiras de enviar e-mails

O Campaign Studio agora abrange três padrões de envio distintos:

| Tipo | Comportamento |
|------|-----------|
| **Transmissão** | Enviado uma vez — imediatamente ou em uma data e horário agendados. Use para uma comunicação única ou uma venda. |
| **Recorrente** | Um modelo que é enviado em um horário recorrente (consulte [Campanhas Recorrentes](/help/recurring-campanhas)). |
| **Jornada** | Uma sequência de vários passos que começa automaticamente para um cliente quando um evento de ciclo de vida ocorre, e depois envia seus passos ao longo de horas ou dias. |

Uma jornada não tem seu próprio botão de "enviar" e nenhuma agenda para configurar — ela reage a eventos em vez de a um relógio.

## Gatilhos

Toda jornada ouve exatamente um evento, definido como o **Gatilho** da jornada:

| Gatilho | Dispara quando |
|---------|-----------|
| **Cliente se cadastra** | Uma nova conta de cliente é criada. |
| **Pedido realizado** | Qualquer pedido é feito, por um cliente novo ou recorrente. |
| **Primeiro pedido realizado** | Especificamente o primeiro pedido de um cliente. |
| **Carrinho abandonado** | Um cliente adiciona algo ao seu carrinho, depois fica inativo sem finalizar a compra. |
| **Cliente inativo (recuperação)** | Um cliente não fez um pedido há algum tempo. |
| **Pedido entregue** | O status de um pedido muda para Entregue. |
| **Produto novamente em estoque** | Um produto que um cliente pediu para ser notificado fica disponível novamente. |

## Os gatilhos de recuperação e reengajamento, em detalhes

**Pedido entregue** e **Produto novamente em estoque** são acionados imediatamente, da mesma forma que **Pedido realizado**. **Carrinho abandonado** e **Cliente inativo (recuperação)** funcionam de forma diferente: em vez de reagir a um momento único, o Spwig verifica periodicamente os clientes e compradores que se encaixam, então pode haver um pequeno atraso entre o carrinho ficar inativo (ou o cliente ficar inativo) e a inscrição.

**Carrinho abandonado** — inscreve um cliente que adicionou algo ao seu carrinho e depois ficou inativo sem concluir a compra. Por padrão, esse é após cerca de uma hora de inatividade; o período exato de inatividade (e quão longe o Spwig procurará) é um limite que seu host pode ajustar para a sua loja. Funciona tanto para compradores logados quanto convidados — para um convidado, o Spwig usa o endereço de e-mail capturado no checkout. Se o cliente voltar e concluir seu pedido, ele é automaticamente removido da jornada, então uma compra concluída nunca receberá um e-mail "você esqueceu de algo?". Adicione um bloco de conteúdo **Carrinho Abandonado** no e-mail de recuperação para mostrar exatamente o que foi deixado para trás, com preços, imagens e um link de volta para o carrinho — ou use um bloco **Produto em Destaque** para destacar um item em vez disso.

**Cliente inativo (recuperação)** — inscreve um cliente que não fez um pedido há algum tempo, para dar a ele um motivo para voltar.

Por padrão, esse é de 90 dias sem compra (também um limite ajustável pelo host).

Um cliente só é reinserido em uma jornada de reativação no máximo uma vez por essa janela, portanto, alguém que permanece inativo não é reinscrito novamente imediatamente.

**Pedido entregue** — inscreve um cliente quando o status do pedido muda para **Entregue**, o que é um momento natural para solicitar uma avaliação alguns dias depois. Dispara uma vez por pedido, na transição para Entregue — edições posteriores a um pedido já entregue não o disparam novamente. Observe que a ação em massa **Marcar pedidos selecionados como Entregue** na lista de pedidos atualiza os pedidos diretamente e não dispara este gatilho (nem o e-mail de confirmação de entrega); atualize os pedidos um a um, ou pelo aplicativo móvel do Spwig, para que ele seja disparado.

**Produto de volta ao estoque** — quando um produto sobre o qual um cliente solicitou notificação volta ao estoque, o Spwig verifica se você tem uma jornada ativa ouvindo este gatilho. Se tiver, o cliente é inscrito nessa jornada em vez do alerta único simples — assim, você pode adicionar um atraso, um bloco **Produto em Destaque** mostrando o item reabastecido, ou um e-mail de acompanhamento. Se nenhuma jornada de reabastecimento estiver ativa, os clientes ainda recebem o e-mail de notificação único padrão exatamente como antes, portanto, ativar uma jornada para este gatilho é totalmente opcional.

## Criando uma jornada

Navegue até **Campaign Studio > Journeys** e clique em **Add Journey**.

1. Dê à jornada um **Name** — isso é apenas para sua referência; os clientes nunca o veem.
2. Escolha o evento de **Trigger**.
3. Opcionalmente, defina **Only for segment** para um Segment — quando definido, apenas os assinantes que pertencem a esse segmento são inscritos. Deixe em branco para inscrever todos os assinantes elegíveis.
4. Defina **Once per subscriber** e **Re-enrollment cooldown (days)** — veja [Proteção contra excesso de inscrição](#guarding-against-over-enrollment) abaixo.
5. Defina **Status** como **Active** para ativar a jornada. Deixe como **Draft** enquanto ainda estiver projetando, ou defina como **Paused** para parar novas inscrições sem perder sua configuração.
6. Clique em **Save** — o Spwig leva você diretamente para o [Journey Builder](/help/journey-builder), o canvas visual onde você projeta a sequência real: quais e-mails são enviados, quanto tempo esperar entre eles e se diferentes assinantes devem seguir caminhos diferentes.

Uma série de boas-vindas simples de três etapas, uma vez projetada no canvas, pode parecer assim:

| Etapa | Aguarda | Envia |
|------|-------|-------|
| 1 | Imediatamente | E-mail de Boas-vindas |
| 2 | 3 dias depois | Dicas para Começar |
| 3 | 7 dias depois | Desconto no Primeiro Pedido |

Os e-mails em si são Campanhas comuns que você projeta no mesmo construtor visual que usaria para um Broadcast — linha de assunto, blocos de conteúdo, tudo. Não é necessário agendar ou enviar um por conta própria; deixe como **Draft** e apenas selecione-o no menu suspenso da etapa no construtor. A jornada o envia por você, uma vez por assinante que atinge essa etapa.

Veja [Journey Builder](/help/journey-builder) para o guia completo sobre o design de etapas no canvas, ramificação de uma jornada com uma condição **Yes/No** e início a partir de um modelo pronto em vez de um canvas em branco.

## Teste A/B de uma etapa

Qualquer etapa de **Send email** pode ser transformada em um teste A/B, para que uma jornada descubra automaticamente — e depois continue usando — o e-mail que tem o melhor desempenho. Como uma jornada é executada continuamente (os assinantes chegam ao longo do tempo), o Spwig não testa um lote fixo e para; em vez disso, **divide os inscritos igualmente entre as variantes conforme eles entram, observa o desempenho de cada uma e, uma vez que uma seja uma vencedora estatística clara, trava essa variante para todos os inscritos futuros.** Assinantes que já estão no meio do processo mantêm a versão que lhes foi enviada primeiro.

Abra uma etapa de Send email no [Journey Builder](/help/journey-builder) e defina **Step type**:

- **Email único** — o comportamento normal: todos recebem o único email que você escolher.
- **A/B: emails diferentes** — selecione **dois a quatro** emails (diferentes em design, ofertas ou layout); cada inscrito recebe um.
- **A/B: assuntos diferentes** — selecione um email e insira **dois a quatro** assuntos; cada inscrito recebe esse email com um assunto diferente.

Escolha **Escolher o vencedor por** — **Taxa de abertura** (geralmente ideal para um teste de assunto) ou **Taxa de clique** — e está pronto. Defina a jornada como **Ativa** e os inscritos começam a ser divididos entre os variantes.

O painel da etapa mostra um **placar em tempo real** à medida que os dados chegam — cada variante, o número de destinatários, a taxa de abertura e a taxa de clique, além de quão confiante o Spwig está no líder ("Levando em 92% de confiança"). Um vencedor só é bloqueado quando o Spwig tem pelo menos **95% de confiança** *e* há dados suficientes para confiar nele, então uma jornada com baixo tráfego não chega a conclusões precipitadas. Assim que bloqueado, a etapa exibe **"Vencedor bloqueado: Variante B"** e todo novo inscrito recebe essa variante; no canvas, o cartão exibe **"A/B · N emails"** durante o teste, e **"Vencedor A/B: B"** assim que decidido.

Alguns pontos importantes:

- **Dê-lhe tráfego.** A confiança depende do volume — uma etapa que poucas pessoas atingem pode ficar em "Dados insuficientes ainda" por um tempo. O teste A/B brilha em jornadas com inscrição constante.
- **Editar as variantes ou a métrica de vencedor inicia um teste fresco** — um vencedor anteriormente bloqueado é limpo para que o novo conjunto de configurações ganhe seus próprios resultados.
- Uma etapa A/B com menos de duas variantes **bloqueia a jornada de ir para Ativa** até que você a conclua (ou a mude para um email único).

Veja [Teste A/B](ab-testing) para mais informações sobre como o Spwig lê confiança e significância.

## Como o cadastro funciona

Quando o evento de gatilho ocorre para um cliente, o Spwig verifica todas as jornadas ativas que estão ouvindo por esse evento e, para cada uma em que o cliente é elegível, **o cadastra** na parte inicial do fluxo. A partir daí, o Spwig move o assinante para frente por tudo o que você projetou no canvas — esperando cada etapa de **Aguardar**, enviando o email de cada etapa de **Enviar email** e seguindo o caminho **Sim**/**Não** correto em qualquer **Ramificação** — até que ele atinja uma etapa de **Sair**, momento em que a jornada é marcada como **Concluída** para esse assinante.

**O consentimento é sempre respeitado.** Um assinante que não se inscreveu para e-mails de marketing, ou que se desinscreveu desde então, é simplesmente pulado — a jornada não para para outros assinantes, e desistências durante a jornada interrompem automaticamente os envios restantes desse assinante. Você nunca precisa filtrar suas jornadas pelo status de consentimento por conta própria.

## Protegendo contra cadastro excessivo

Dois ajustes na jornada controlam quão frequentemente um assinante pode passar por ela:

| Configuração | O que ela faz | Uso comum |
|---------|--------------|-------------|
| **Uma vez por assinante** *(ativado por padrão)* | Cada assinante é inscrito no máximo uma vez, independentemente de quantas vezes o evento de gatilho acontecer novamente para ele. | Uma série de boas-vindas — um cliente deve recebê-la apenas uma vez. |
| **Período de carência para reinscrição (dias)** | Quando **Uma vez por assinante** está desativado, define o número mínimo de dias que devem passar desde a última inscrição de um assinante antes que ele possa ser inscrito novamente. Defina como `0` para nenhuma carência. | Uma série acionada por pedido que deve ser executada novamente para um novo pedido, mas não deve ser acionada novamente para cada pedido colocado na mesma semana. |

Desative **Uma vez por assinante** para uma jornada que você queira executar por pedido (como um agradecimento pós-compra), e aja com um período de carência para que um cliente que compre duas vezes no mesmo dia receba inscrição apenas uma vez. Um assinante que já esteja trabalhando em uma jornada não é inscrito em uma segunda execução da mesma jornada, independentemente dessas configurações.

A lista **Campaign Studio > Journeys** exibe o **Trigger** (Gatilho), o **Status**, o número de **Emails** enviados e os totais em execução de **Enrolled** (Inscritos) / **Completed** (Concluídos) de cada jornada, permitindo que você veja de relance se uma jornada está realmente alcançando as pessoas.

![A lista de Journeys mostrando duas jornadas ativas com contagens de inscrição e conclusão](/static/core/admin/img/help/triggered-journeys/journey-list.webp)

Para ver assinantes individuais em vez de totais, abra a lista **Journey Enrollments** em `/admin/email_marketing/journeyenrollment/`. Cada linha mostra o progresso de um assinante em uma jornada: qual **Journey** (Jornada) ele está, sua **Current step** (Etapa atual), **Status** (Ativo, Concluído ou Cancelado) e quando sua **Next step** (Próxima etapa) está prevista. Use os filtros para restringir a uma jornada ou a um status — por exemplo, filtrar por **Active** (Ativo) mostra todos que estão atualmente no meio da sequência.

![A lista de Journey Enrollments mostrando o progresso dos assinantes em duas jornadas](/static/core/admin/img/help/triggered-journeys/journey-enrollments.webp)

## Journey report (Relatório da Jornada)

Cada jornada tem sua própria página de **Report** (Relatório), aberta clicando no botão **Report** no cartão da jornada em **Campaign Studio > Journeys**, ou na própria página de configurações da jornada. É um resumo em uma única página de até onde os inscritos chegam na sequência e, onde seus e-mails contêm links rastreados, quanto de receita a jornada gerou.

![A página do relatório da Jornada mostrando o funil de inscrição, o cartão de receita atribuída e a tabela de receita por etapa](/static/core/admin/img/help/triggered-journeys/journey-report.webp)

### Enrollment funnel (Funil de inscrição)

Quatro cartões mostram onde os inscritos estão atualmente:

| Cartão | O que mostra |
|------|---------------|
| **Enrolled** | O número total de assinantes que já entraram nesta jornada. |
| **Active now** | Inscritos atualmente no meio da sequência, aguardando ou trabalhando em sua próxima etapa. |
| **Completed** | Inscritos que atingiram a etapa **Exit** (Saída) da jornada. |
| **Exited** | Inscritos removidos da jornada antes de concluí-la — por exemplo, um comprador que finalizou o checkout no meio de uma sequência de abandono de carrinho, ou um assinante que cancelou a inscrição. |

Se a jornada ainda não tem inscrições, todos os quatro cartões mostram zero e uma nota lembra que as métricas aparecem assim que os clientes começarem a entrar na jornada.

### Attributed revenue (Receita atribuída)

O cartão **Attributed revenue** funciona da mesma forma que um [relatório de campanha](campaign-reports) — o Spwig rastreia pedidos de volta aos cliques em links nos e-mails da jornada, a mesma atribuição por clique, controlada por consentimento, descrita em [Attributed revenue](campaign-reports#attributed-revenue) naquela página. Os mesmos avisos se aplicam aqui: a atribuição é apenas por clique (uma abertura sozinha nunca atribui receita), segue o modelo de atribuição ativo da sua loja e a janela de retrospectiva, respeita o consentimento de análise e não é retroativo — uma jornada só mostra receita de e-mails enviados após a ativação do rastreamento de atribuição para a sua loja.

A linha secundária do cartão detalha o total em:

- **Orders** (Pedidos) — quantos pedidos são creditados a esta jornada, combinando os e-mails de todas as etapas.
- **AOV** — o valor médio do pedido entre esses pedidos.
- **Revenue per enrollee** (Receita por inscrito) — receita atribuída dividida pelo total de **Enrolled**. Uma jornada não tem um único "gasto" como uma campanha — ela roda continuamente em vez de custar algo uma vez — então não há uma figura de ROAS aqui. **Revenue per enrollee** é o equivalente mais próximo: uma medida estável e comparável de quão eficientemente a jornada converte uma inscrição em uma venda, que você pode acompanhar ao longo do tempo ou comparar com outra jornada.

### Revenue by step (Receita por etapa)

Quando a jornada tem pelo menos uma etapa **Send email** (Enviar e-mail), uma tabela **Revenue by step** detalha o total ainda mais, uma linha por etapa, para que você possa ver qual e-mail na sequência está realmente valendo a pena:

| Coluna | O que exibe |
|--------|---------------|
| **Etapa** | O e-mail da etapa, com um selo **A/B** se essa etapa estiver executando um [teste A/B](ab-testing). |
| **Receita** | Receita atribuída de pedidos rastreados até o e-mail dessa etapa. |
| **Pedidos** | O número de pedidos por trás dessa cifra de receita. |
| **Enviados** | Quantas vezes o e-mail desta etapa foi enviado. |
| **Aberturas** / **Cliques** | Quantos desses envios foram abertos e quantos foram clicados. O Spwig rastreia aberturas e cliques para todos os envios de cada etapa, sejam simples ou A/B. |

Use esta tabela para identificar um elo fraco em uma jornada de outro modo saudável — por exemplo, uma série de boas-vindas em que o primeiro e-mail gera a maior parte da receita e uma etapa posterior contribui pouco pode ser um candidato para uma oferta mais forte ou uma reescrita, em vez de assumir que toda a sequência precisa ser repensada.

## Dicas

- A maneira mais rápida de iniciar uma jornada de abandono de carrinho, recuperação de clientes, solicitação de avaliação pós-entrega ou alerta de reposição é um modelo inicial — ao salvar uma nova jornada com um desses gatilhos, o seletor **Modelos** do [Journey Builder](/help/journey-builder) oferece um fluxo pronto (**Recuperação de carrinho abandonado**, **Recuperação de clientes inativos**, **Solicitação de avaliação pós-entrega** ou **Alerta de reposição**) que você pode ajustar em vez de construir do zero.
- Comece toda jornada como **Rascunho** enquanto constrói suas etapas, depois alterne o **Status** para **Ativo** após verificar os e-mails e os atrasos — nenhum assinante é inscrito até que esteja Ativo.
- Mantenha **Uma vez por assinante** ativado para qualquer coisa ligada a uma marco único (cadastro, primeiro pedido); desative com um tempo de espera razoável para qualquer coisa que deva se repetir, como uma série pós-compra.
- Use **Somente para segmento** para executar uma série de boas-vindas diferente para uma audiência específica — por exemplo, um segmento VIP recebe uma sequência mais rica do que todos os outros.
- Defina a espera da primeira etapa como `0` se você quiser que o primeiro e-mail seja enviado imediatamente após o gatilho disparar, em vez de esperar.
- Verifique a lista **Inscrições na Jornada** após ativar uma nova jornada para confirmar que os assinantes estão realmente sendo inscritos e avançando por suas etapas como esperado.
- Pausar uma jornada (**Status: Pausado**) interrompe novas inscrições, mas não cancela assinantes que já estão no meio do processo — eles continuam recebendo suas etapas restantes.
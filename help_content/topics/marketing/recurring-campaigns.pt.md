---
title: Campanhas Recorrentes
---

As **Campanhas Recorrentes** do Campaign Studio permitem configurar um boletim uma única vez — um resumo semanal de produtos, um digest mensal do blog — e deixar que o Spwig o envie automaticamente em um agendamento repetitivo, em vez de você criar e enviar uma nova campanha manualmente a cada vez.

## Transmissão única vs. recorrente

Cada campanha no Campaign Studio tem um **Tipo de campanha**:

| Tipo | Comportamento |
|------|-----------|
| **Transmissão única** | Enviada uma vez — imediatamente ou em uma data e hora agendada específicas. Use isso para um anúncio pontual, promoção ou lançamento de produto. |
| **Recorrente** | Funciona como um modelo que é enviado em um agendamento repetitivo. Cada envio é uma cópia nova e datada chamada **ocorrência** — o próprio modelo nunca é enviado diretamente. |

Para transformar uma campanha em recorrente, abra-a em **Campaign Studio > Campanhas** e defina o **Tipo de campanha** como **Recorrente**, depois salve. Uma seção **Agendamento** aparece na campanha quando você a reabrir — ela só aparece para campanhas recorrentes.

![Tipo de campanha definido como Recorrente](/static/core/admin/img/help/recurring-campaigns/campaign-type-selector.webp)

## Definindo um agendamento

Uma vez que a campanha é recorrente, sua seção **Agendamento** controla quando ela será disparada:

| Campo | Descrição |
|-------|-------------|
| **Ativo** | Liga ou desliga a recorrência sem excluir o agendamento. |
| **Frequência** | **Diária**, **Semanal** ou **Mensal**. |
| **Intervalo** | Enviar a cada N unidades de frequência — por exemplo, intervalo `2` com frequência **Semanal** significa a cada 2 semanas. |
| **Dia da semana** | Qual dia enviar para uma frequência semanal (`0` = segunda-feira … `6` = domingo). |
| **Dia do mês** | Qual dia enviar para uma frequência mensal (`1`–`28`, para que todo mês tenha esse dia). |
| **Hora de envio** | A hora do dia em que a campanha será enviada. |
| **Fuso horário** | Um nome de fuso horário IANA, por exemplo, `Europe/London` ou `America/New_York` — a hora de envio é interpretada nesta zona, não no servidor. |

![Seção de agendamento semanal em uma campanha recorrente](/static/core/admin/img/help/recurring-campaigns/schedule-section.webp)

Assim que você salvar um agendamento ativo, ele **se ativa** — o Spwig calcula a próxima hora de disparo e a exibe em **Próxima execução em**. Você não precisa acionar nada manualmente; uma tarefa em segundo plano verifica agendamentos vencidos e envia a ocorrência quando a hora chega. **Última execução em** e **Ocorrências enviadas** são atualizadas automaticamente após cada envio, para que você possa ver que o agendamento está ativo.

## A política de sem novo conteúdo

Boletins recorrentes frequentemente apresentam conteúdo dinâmico — mais comumente um bloco **Posts do Blog** (ou uma **Grade de Produtos**) definido como **Novo desde o último envio** no construtor visual, que apenas traz posts publicados — ou produtos adicionados — desde o envio anterior da campanha. Isso levanta uma pergunta óbvia: o que acontece se uma execução agendada chegar e não houver nada novo para apresentar?

O Spwig responde a isso com a **Política de sem novo conteúdo** do agendamento:

| Política | O que acontece | Ideal para |
|--------|---------------|----------|
| **Pular este envio** *(padrão)* | A ocorrência é pulada por completo — nada é enviado. O agendamento avança diretamente para a próxima execução programada. | Um resumo de blog ou produtos, para que os assinantes nunca recebam um e-mail que apenas repita o que já viram. |
| **Enviar mesmo assim (omitir blocos vazios)** | O e-mail é enviado conforme o agendamento, independentemente. Qualquer bloco que não tenha nada de novo — como um bloco de Publicações de Blog "Novo desde o último envio" vazio — simplesmente não renderiza nada naquele local. | Boletins que sempre têm outro conteúdo que vale a pena enviar (uma mensagem de boas-vindas, seções evergreen ou vários blocos dinâmicos), mesmo que um bloco fique vazio. |
| **Retenção e envio tardio** | O envio é adiado. O Spwig verifica novamente uma vez por dia por conteúdo novo, até o limite da **Janela de retenção (dias)**. Se novo conteúdo aparecer dentro dessa janela, a ocorrência é enviada com atraso; se a janela expirar sem nada de novo, essa ocorrência é descartada e o agendamento avança para o próximo horário. | Uma frequência que você deseja proteger (por exemplo, enviar *alguma coisa* eventualmente) sem disparar uma edição vazia no momento em que nada de novo aconteceu para publicar naquela semana. |

Apenas campanhas que usam conteúdo consciente de delta — um bloco de Publicações de Blog ou uma Grade de Produtos configurada para **Novo desde o último envio** — acionam esta verificação. Uma campanha recorrente sem tais blocos é sempre considerada ter conteúdo novo e envia normalmente conforme o agendamento.

**Janela de retenção (dias)** se aplica apenas à política **Retenção e envio tardio** — ela define quantos dias o Spwig continuará tentando antes de desistir dessa ocorrência.

## Teste A/B de cada ocorrência

Um boletim recorrente é um lugar natural para testar A/B suas **linhas de assunto** — você envia em uma frequência regular para o mesmo público, então pode continuar aprendendo qual redação gera mais aberturas. O Spwig pode executar um teste A/B de linha de assunto novo em **cada ocorrência** automaticamente.

Configure na seção **Agendamento**:

1. Em **Linhas de assunto A/B**, insira **dois a quatro** linhas de assunto, uma por linha. Deixe em branco para enviar as ocorrências normalmente com o assunto do próprio modelo.
2. Defina a **% da amostra do teste A/B** — a parte do público de cada ocorrência usada para o teste, dividida igualmente entre os assuntos. O restante é o grupo de controle que recebe o vencedor.
3. Escolha a **Métrica do vencedor A/B** (taxa de abertura ou de clique), a **Janela do teste A/B (horas)** para coletar resultados antes de decidir e se deve **enviar automaticamente o vencedor** para o grupo de controle.

A partir de então, cada vez que o agendamento dispara, essa ocorrência divide seu público, envia cada linha de assunto para uma fatia, aguarda o fim da janela do teste e então escolhe o assunto vencedor e o envia para todos os outros — sem nenhuma ação adicional da sua parte. Cada ocorrência é um teste autônomo, então você obtém uma leitura fresca a cada envio e pode observar quais assuntos vencem ao longo das semanas. O resultado de cada ocorrência aparece em **Histórico de ocorrências** abaixo, com um link direto para sua página de resultados com as taxas por variante, o vencedor e o quão confiante o Spwig está (veja [Teste A/B](ab-testing) para saber como ler esses resultados).

Duas coisas que valem a pena saber:

- **O teste A/B aqui é apenas para linhas de assunto.** Para comparar designs completamente diferentes, use um teste A/B de transmissão única — o assistente completo, que suporta variantes de conteúdo, é para campanhas de transmissão.
- Se o público de uma ocorrência for **pequeno demais para dividir** entre as variantes, o Spwig envia silenciosamente essa ocorrência como um boletim normal — uma semana fraca nunca significa um envio perdido.

## Histórico de ocorrências

Cada vez que uma campanha recorrente envia de fato, o Spwig cria uma **ocorrência** datada — um registro de campanha real e independente com seu próprio assunto, destinatários e estatísticas de envio (enviados, falhas, pulados, aberturas, cliques). A ocorrência é nomeada com base no modelo com a data de envio anexada, por exemplo, "Resumo Semanal do Blog — 2026-08-19".

A página de edição da campanha recorrente lista o seu **Histórico de ocorrências** — as ocorrências mais recentes, cada uma com um link para o próprio registro de campanha daquela ocorrência, para que você possa revisar exatamente o que foi enviado e como foi o desempenho.

![Lista de histórico de ocorrências em uma campanha recorrente](/static/core/admin/img/help/recurring-campaigns/occurrence-history.webp)

## Dicas

- Combine uma campanha recorrente com um bloco de **Posts do Blog** configurado para **Novos desde o último envio** para criar um resumo autossustentável de "novos posts desta semana" — você escreve os posts e o Spwig cuida do envio dos e-mails.
- Comece com **Pular este envio** para resumos de conteúdo. É o padrão mais seguro: os assinantes nunca recebem uma repetição do conteúdo da última vez.
- Alterne para **Enviar mesmo assim** apenas se o seu modelo tiver outro conteúdo que valha a pena ser enviado por si só, mesmo quando o bloco dinâmico estiver vazio.
- Use **Retenção e envio tardio** quando perder ocasionalmente um ritmo de envio não for um problema, mas perdê-lo por semanas seguidas for — defina a janela de retenção de acordo com a duração de um intervalo com a qual você está confortável.
- Verifique o **Próxima execução em** após salvar um agendamento para confirmar que ele caiu no dia e horário esperados, especialmente ao trabalhar em fusos horários diferentes.
- Revise o **Histórico de ocorrências** regularmente — um modelo que continua pulando é um sinal de que a fonte de conteúdo dinâmico (por exemplo, o blog) ficou silenciosa.
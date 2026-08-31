---
title: Higiene da Lista e Supressões
---

Cada endereço de e-mail que gera um rejeição definitiva (hard-bounce), marca seu e-mail como spam ou falha repetidamente em receber suas mensagens coloca o restante da sua lista em risco — os provedores de caixa postal avaliam a reputação do seu remetente com base na limpeza do seu envio, e uma lista suja significa que mais de *cada* campanha cairá na caixa de spam. O Campaign Studio protege você automaticamente contra isso com a **higiene da lista**: ele monitora endereços não entregáveis e queixosos e para de enviar e-mails de marketing para eles, sem nenhuma configuração por parte sua.

Isso é separado das cancelamentos de inscrição. Um endereço com inscrição cancelada retirou o consentimento; um endereço **suprimido** é aquele que o Spwig aprendeu ser inseguro ou impossível de continuar enviando, independentemente do consentimento.

## Como os endereços são suprimidos

O Spwig adiciona um endereço à **Lista de Supressão** automaticamente quando:

| Gatilho | O que significa |
|---------|---------------|
| **Rejeição definitiva (Hard bounce)** | O endereço não existe, ou o domínio recusou aceitar o e-mail para ele — permanentemente não entregável. |
| **Reclamação de spam** | Um destinatário marcou seu e-mail como spam ou lixo. |
| **Rejeições temporárias repetidas (Soft bounces)** | O endereço teve uma rejeição temporária (caixa postal cheia, servidor temporariamente indisponível) 5 vezes dentro de uma janela móvel de 30 dias. Uma única rejeição temporária é tratada como um imprevisto passageiro e ignorada — apenas um padrão de falhas repetidas aciona a supressão. |
| **Bloqueado manualmente** | Você adicionou o endereço você mesmo. |

Uma vez que um endereço é suprimido, o Spwig para de enviar qualquer **campanha** ou e-mails de **jornada** para ele imediatamente — nenhuma outra ação é necessária da sua parte.

## De onde vem o sinal

O Spwig pode aprender sobre uma rejeição ou reclamação de vários lugares diferentes, exibidos como a **Origem** em cada endereço suprimido:

- **Rejeitado no envio** — seu servidor de e-mail recusou o endereço imediatamente quando o Spwig tentou enviar para ele.
- **Webhook do provedor** — se você conectou um provedor de e-mail (como SendGrid, Amazon SES, Mailgun ou Postmark), esse provedor relata rejeições e reclamações de volta ao Spwig conforme elas ocorrem.
- **Portal de e-mail (Mail gateway)** — se sua loja envia através do portal de e-mail hospedado pelo Spwig, o Spwig obtém os relatórios de rejeição do portal em seu nome.
- **Adicionado manualmente** — você inseriu o endereço você mesmo a partir do painel administrativo.

Você não precisa configurar nada para se beneficiar disso — de qualquer forma que você envie e-mails, o Spwig está monitorando falhas e mantendo sua lista limpa.

## O painel do Campaign Studio

Abra o **Campaign Studio** e procure pelo cartão **Endereços suprimidos**. Ele mostra o número total de endereços atualmente suprimidos, além de quantos são novos nos últimos 30 dias. Clique no cartão para abrir a lista completa de Supressões.

![O cartão de estatísticas de Endereços suprimidos no painel do Campaign Studio, mostrando um total e uma contagem de "novos nos últimos 30 dias"](/static/core/admin/img/help/list-hygiene/dashboard-suppressed-card.webp)

Uma contagem em constante aumento é normal — toda lista acumula alguns endereços ruins ao longo do tempo, à medida que as pessoas mudam de emprego, fecham contas ou abandonam caixas postais. Um pico súbito vale a pena investigar; veja [Caixa de Saída de E-mails](email-outbox) para verificar se um envio específico atingiu um número incomum de falhas.

## A lista de Supressões

Clique em **Supressões** para ver todos os endereços suprimidos, por que foram suprimidos e de onde veio o sinal.

![A lista de Supressões mostrando endereços suprimidos com suas colunas de Motivo e Origem](/static/core/admin/img/help/list-hygiene/suppressions-list.webp)

Use os filtros à direita para filtrar a lista por **Motivo** ou **Origem** — por exemplo, para revisar todos os endereços bloqueados manualmente, ou tudo que veio através de um webhook de provedor.

## Adicionando um endereço manualmente

Para bloquear um endereço você mesmo — um endereço de abuso conhecido, um concorrente raspando sua newsletter, ou qualquer outra coisa que você queira manter fora da sua lista — clique em **+ Adicionar endereço suprimido** e preencha:

- **Email** — o endereço a ser bloqueado
- **Motivo** — escolha **Bloqueado manualmente** para uma entrada adicionada por você
- **Fonte** — escolha **Adicionado manualmente"
- **Detalhe** — um comentário opcional explicando por quê (útil para seus próprios registros, e para qualquer funcionário que revise a lista posteriormente)

Salve a entrada e o Spwig deixa de enviar qualquer campanha ou e-mail de jornada para esse endereço imediatamente.

## Quando eu liberaria um endereço?

Liberar (desbloquear) um endereço deve ser raro e deliberado. Faça isso somente quando tiver certeza de que o problema subjacente foi resolvido — por exemplo:

- Um cliente lhe diz que seu correio estava cheio e foi esvaziado.
- Um endereço foi suprimido por uma sequência de bounces suaves que você sabe ter sido causada por uma falha temporária no provedor deles, e não por um correio inativo.
- Você bloqueou um endereço manualmente e depois decidiu que o bloqueio foi um erro.

Para liberar um endereço, abra-o na lista de supressões e exclua a entrada — isso remove o bloqueio, permitindo que o endereço receba e-mails novamente. Não libere um endereço com bounce rígido somente por que é inconveniente perder um assinante; o endereço não existe, e enviar para ele novamente só causará um bounce e custará reputação novamente. Da mesma forma, liberar um endereço com reclamação de spam raramente ajuda — esse destinatário informou ao provedor do seu correio que não quer seu e-mail, e enviar novamente para eles corre o risco de outra reclamação.

## O que não é afetado

A supressão se aplica somente a **campanhas de marketing e jornadas** enviadas pelo Campaign Studio. Ela não afeta **e-mails transacionais** — confirmações de pedidos, atualizações de envio, redefinições de senha e outros e-mails que sua loja envia como parte de uma ação de pedido ou conta, sempre passam, mesmo para um endereço suprimido. A supressão existe para proteger sua reputação de remetente de marketing; não é um lista geral de bloqueio de e-mails para sua loja.

## Dicas

- Não lute contra o sistema manualmente liberando cada bounce que vir — um bounce rígido significa que o endereço está inativo, e adicioná-lo novamente aos envios só causará outro bounce.
- Verifique a lista de supressões após um grande envio se sua taxa de abertura parecer inusitadamente baixa — uma onda de bounces suaves em um domínio compartilhado (ex. um servidor de e-mail corporativo com problemas) pode ser um sinal de problema de entrega temporário que vale a pena investigar com seu provedor.
- Se você estiver se mudando para o Spwig de outra plataforma, não importe manualmente sua lista completa de bloqueios antiga como supressões — deixe o Spwig aprender com os próprios bounces e reclamações nessa lista, para que você não bloquee acidentalmente endereços que teriam entregue normalmente.
- Revise a coluna **Fonte** ocasionalmente — muitas entradas de **webhook do provedor** confirmam que o relato de bounce do seu provedor de e-mail está conectado e funcionando.
- Mantenha o campo **Detalhe** significativo ao adicionar um bloqueio manual; é o único registro de por que essa decisão foi tomada depois que o tempo tiver passado.
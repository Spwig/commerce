---
title: Runbook de Entregabilidade de E-mail
---

<!-- screenshots-needed:
- url: /admin/email_system/emailaccount/add/
  filename: wizard-dns-step.webp
  description: Step 4 (DNS Configuration) of the email account setup wizard for the built-in SMTP provider, showing the SPF/DKIM/DMARC validation one-liners and the DNS provider tabs (Cloudflare/GoDaddy/Namecheap/Route 53/Other) with at least one record's "Details" panel expanded so a copyable TXT record is visible.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/email_system/emailaccount/{account_id}/change/
  filename: dkim-dns-record.webp
  description: An existing built-in SMTP EmailAccount's change form scrolled to the "DKIM keys configured" panel, showing the DNS TXT record Name/Value and the Copy DNS Record button.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
- url: /admin/campaigns/dashboard/
  filename: suppressed-addresses-card.webp
  description: The Campaign Studio dashboard's Suppressed addresses stat card, for the "monitor" section of this runbook.
  save-to: core/static/core/admin/img/help/deliverability/
  viewport: 1440x900
-->

Enviar um e-mail é fácil. Fazer com que ele chegue à caixa de entrada, em vez da pasta de spam, é o verdadeiro trabalho — e provedores de caixa de entrada como Gmail e Yahoo agora impõem requisitos técnicos rigorosos antes de sequer considerá-lo. Este runbook explica o que configurar, em que ordem, para que suas confirmações de pedido e campanhas cheguem onde os clientes podem vê-las.

Nada aqui é uma tarefa de uma única vez. A entregabilidade é uma reputação que você constrói ao longo do tempo e pode perder rapidamente — a lista de verificação no final vale a pena ser revisada sempre que algo parecer estranho.

## Por que isso é importante

Todos os principais provedores de caixa de entrada pontuam os e-mails recebidos com base na reputação do remetente antes de decidir se entregam, movem para a pasta de spam ou rejeitam por completo. Desde 2024, o Gmail e o Yahoo formalizaram isso em **requisitos explícitos para remetentes em massa** para qualquer pessoa que envie volume significativo:

- **Autentique seu domínio** — registros SPF, DKIM e DMARC válidos.
- **Facilite o cancelamento da inscrição** — um opt-out funcional e de baixa fricção em todos os e-mails de marketing.
- **Mantenha as reclamações de spam baixas** — remetentes em massa que ultrapassam aproximadamente 0,3% de reclamações correm o risco de ter seus e-mails rejeitados ou movidos para a pasta de spam; o alvo mais seguro é bem abaixo de 0,1%.

Se você falhar nesses requisitos, não são apenas as campanhas de marketing que sofrem — uma reputação de domínio danificada pode arrastar e-mails transacionais (confirmações de pedido, redefinições de senha) para o spam também, pois o Gmail e o Yahoo cada vez mais julgam a reputação no nível do domínio de envio, e não apenas por tipo de mensagem. As etapas abaixo mostram como atender a todos os três requisitos.

## Etapa 1: Autentique seu domínio de envio

SPF, DKIM e DMARC são registros TXT de DNS que provam aos servidores de e-mail receptores que os e-mails que afirmam ser do seu domínio realmente foram enviados por você. Como você os configura depende do modo de envio que sua loja usa — todos os três são configurados em **Configuração de E-mail** na barra lateral de administração (isso abre a lista de Contas de E-mail; veja [Configuração de E-mail](email-configuration) para o guia completo de configuração de contas).

| Modo de envio | Como a autenticação funciona |
|---|---|
| **SMTP integrado** (o próprio servidor de e-mail da Spwig) | A Spwig gera automaticamente um par de chaves DKIM para o seu domínio. Ao adicionar uma conta de e-mail, a **Etapa 4** do assistente de configuração exibe o status do SPF, DKIM e DMARC, além do registro exato a ser adicionado, com opção de copiar para a área de transferência e instruções específicas para Cloudflare, GoDaddy, Namecheap e AWS Route 53. O mesmo registro DNS DKIM também é exibido na própria página de administração da conta, posteriormente, sob **Chaves DKIM configuradas**, caso precise localizá-lo novamente. |
| **SMTP genérico** (um provedor próprio como SendGrid, Mailgun, Amazon SES ou Google Workspace, conectado via credenciais SMTP) | A autenticação ocorre parcialmente no próprio painel do provedor. A etapa de DNS do assistente de configuração inclui instruções em abas específicas para Gmail, Outlook, SendGrid, Mailgun e Amazon SES — cada uma explica o que configurar no console do provedor (por exemplo, verificar um domínio de envio no SendGrid) e quais registros DNS resultantes adicionar no seu host DNS. |
| **Gateway de e-mail hospedado pela Spwig** | Disponível em planos hospedados pela Spwig como uma opção de envio gerenciada. Ele assina automaticamente os e-mails de saída com DKIM e, por padrão, envia a partir de um endereço no próprio domínio verificado da Spwig, funcionando sem nenhuma configuração. Se desejar enviar a partir do seu próprio domínio através do gateway, converse com seu provedor de hospedagem sobre a verificação — este é um serviço gerenciado, não um fluxo DNS de autoatendimento. |

Independentemente do modo utilizado, **a adição do registro DNS em si é sempre uma etapa externa** — você a realiza no seu registrador de domínio ou host DNS (Cloudflare, GoDaddy, Namecheap, Route 53 ou onde quer que os servidores de nome do seu domínio apontem), e não dentro da Spwig. A Spwig pode informar exatamente o que adicionar e validar que está ativo, mas não pode acessar seu registrador para adicioná-lo por você.

Algumas coisas importantes a saber antes de começar:

- **As alterações de DNS não são instantâneas.** A propagação pode levar de alguns minutos a 48 horas. A etapa de validação do assistente mostrará um registro como falho ou ausente até que ele tenha se propagado de fato — isso é esperado, não é um sinal de que algo está errado.
- **Apenas um registro SPF é permitido por domínio.** Se você já possui um (do Google Workspace, outro serviço de e-mail, etc.), adicione seu novo remetente ao registro existente com `include:` em vez de criar um segundo registro TXT SPF — dois registros SPF quebrarão a autenticação para todos.
- **O DMARC requer que o SPF ou DKIM já esteja passando.** Configure-o por último, uma vez que o SPF e o DKIM estejam ambos verificados.

## Etapa 2: Usar uma identidade de envio real

Uma vez que seu domínio esteja autenticado, certifique-se de que o que os destinatários realmente veem o respalde:

- **Endereço de remetente** — use um endereço no seu próprio domínio autenticado (`orders@yourstore.com`), nunca um endereço de provedor gratuito (`yourstore@gmail.com`). Um endereço de remetente de provedor gratuito não pode ser autenticado pelos seus registros SPF/DKIM/DMARC de forma alguma, e os provedores de caixa de entrada o tratam como um forte sinal de spam vindo de uma loja.
- **Nome de remetente** — use o nome reconhecível da sua loja, não um rótulo genérico como "Notificações" ou "Não responder".
- **Responder para** — defina um endereço monitorado. Um endereço `noreply@` não monitorado que devolve ou descarta silenciosamente as respostas é, em si, um leve sinal de reputação, e bloqueia o único canal que os clientes têm para informar que algo deu errado.

Defina os três em **Configuração de E-mail > (sua conta) > Configuração do Remetente** — veja [Configuração de E-mail](email-configuration) para o guia completo dos campos.

## Etapa 3: Aquecer antes de escalar

Um domínio ou IP sem histórico de envio ainda não tem reputação — boa ou ruim — e os provedores de caixa de entrada são cautelosos com o desconhecido. Enviar um grande volume inicial de uma vez a partir de um domínio totalmente novo parece estatisticamente idêntico a um spammer iniciando uma nova campanha, e pode acabar na pasta de spam mesmo que todas as caixas técnicas estejam marcadas.

- Comece com volumes menores.

Envie suas primeiras campanhas para o público mais engajado e com maior probabilidade de abrir, em vez de enviar para toda a sua lista de uma vez — consulte [Audiências](audiences) para criar um segmento inicial direcionado.
- Aumente o volume gradualmente nas primeiras semanas, em vez de pular diretamente para envios para a lista completa.
- Se você estiver migrando uma lista existente de outra plataforma, trate isso como o primeiro dia para fins de reputação também — o histórico de envios da sua antiga plataforma não é transferido com o domínio.

## Etapa 4: Mantenha sua lista limpa

Cada reclamação ou rejeição (bounce) custa reputação, e ambas são em grande parte uma função de quem está na sua lista e como chegou lá:

- **Envie e-mails apenas para pessoas que deram consentimento.** Contatos importados, listas compradas e endereços raspados são a forma mais rápida de aumentar as reclamações de spam e rejeições definitivas (hard bounces).
- **Use a dupla confirmação (double opt-in).** O fluxo de consentimento de marketing do Spwig verifica o endereço de e-mail de um assinante antes de enviar e-mails de marketing — consulte [Preferências de Comunicação](communication-preferences) para saber como isso é configurado.
- **Deixe a supressão automática do Spwig fazer seu trabalho.** O Spwig monitora rejeições definitivas, reclamações de spam e rejeições temporárias repetidas e para de enviar e-mails para esses endereços automaticamente, sem necessidade de configuração — consulte [Higiene da Lista e Supressões](list-hygiene) para saber exatamente como isso funciona e quando (raramente) sobrescrevê-lo.
- **Remova assinantes inativos periodicamente** em vez de enviar e-mails para os mesmos endereços não engajados indefinidamente — uma lista que diminui, mas abre e clica, vale mais para sua reputação do que uma grande que não o faz.

## Etapa 5: Monitorar

Problemas de entregabilidade aparecem nos números antes que um cliente avise que um e-mail não chegou.

Abra o [Relatório](campaign-reports) de uma campanha após cada envio e observe:

| Métrica | O que observar |
|---|---|
| **Taxa de rejeição (bounce rate)** | Predominância de rejeições temporárias (soft bounces) é normal; uma participação crescente de **rejeições definitivas (hard bounces)** significa que sua lista está acumulando endereços obsoletos ou inválidos. |
| **Reclamações de spam** | Deve permanecer perto de zero em cada envio. Mantenha bem abaixo do limiar de aproximadamente 0,3% que aciona a aplicação de regras para remetentes em massa no Gmail e Yahoo — trate até mesmo um pequeno pico como algo que merece investigação imediata. |
| **Taxa de abertura / taxa de cliques por abertura** | Uma queda súbita e inexplicada entre envios para a mesma lista (não apenas uma campanha) pode ser um sinal precoce de que os e-mails estão caindo na caixa de spam em vez da caixa de entrada, mesmo antes que os números de rejeição ou reclamação se movam. |

Verifique também periodicamente o cartão **Endereços suprimidos** no painel do Campaign Studio — um fluxo constante é um decaimento normal da lista, mas um pico súbito merece investigação antes do seu próximo envio (veja [Higiene da Lista](list-hygiene)).

Se algo disparar: pause e verifique primeiro se seus registros DNS ainda são válidos (uma renovação de domínio expirada ou uma alteração acidental no DNS pode quebrar silenciosamente o SPF/DKIM), depois veja o que mudou no conteúdo ou na audiência do envio que o disparou.

## Etapa 6: Higiene de conteúdo

Autenticação e qualidade da lista te levam à porta; o conteúdo ainda afeta como você é tratado uma vez lá dentro.

- **Evite padrões que disparam spam** nas linhas de assunto — MAIÚSCULAS, pontuação excessiva ("!!!") e frases como "aja agora" ou "dinheiro grátis" ainda pesam contra você nos filtros de spam, mesmo de um domínio autenticado.
- **Não envie e-mails apenas com imagens.** Um e-mail que é uma única imagem sem texto real é um padrão clássico de spam; mantenha uma quantidade significativa de conteúdo textual real junto com qualquer imagem.
- **Visualize antes de enviar.** Verifique como o e-mail realmente é renderizado — incluindo em dispositivos móveis — antes de ir para sua lista completa.
- **O link de cancelamento de inscrição já é tratado.** O Spwig adiciona automaticamente um link de cancelamento de inscrição funcional, sem necessidade de login, no rodapé de todos os e-mails de marketing — você não precisa adicionar o seu próprio (veja [Preferências de Comunicação](communication-preferences) para saber exatamente como esse fluxo funciona). Não remova ou oculte-o; um link de cancelamento ausente ou quebrado é em si uma violação de política com as regras de remetentes em massa do Gmail e Yahoo, independentemente dos seus outros números.

## "Meus e-mails estão indo para o spam" — checklist de resolução de problemas

Percore estas etapas na ordem:

1. **Verifique novamente os registros DNS.** Abra o assistente de configuração da conta no passo DNS (ou o painel DKIM na página de administração da conta para SMTP interno) e confirme que SPF, DKIM e DMARC ainda aparecem como aprovados. A renovação de um domínio, a migração de provedor de DNS ou uma alteração não relacionada ao seu arquivo de zona pode quebrar um desses de forma silenciosa.
2. **Verifique os números de rejeição e reclamação no relatório da campanha** para os envios afetados — consulte [Relatórios de Campanha](campaign-reports). Um pico em qualquer um indica um problema de qualidade da lista ou conteúdo, em vez de autenticação.
3. **Verifique a lista de supressões** ([Higiene da Lista](list-hygiene)) para uma subida repentina — se uma grande parte da sua lista estiver com falhas há algum tempo, a entrega para o restante também sofrerá degradação.
4. **Confirme que o endereço de remetente está no seu domínio autenticado**, não em um endereço de provedor gratuito ou em um domínio que não corresponda ao que SPF/DKIM/DMARC foi configurado.
5. **Envie um e-mail de teste para um endereço do Gmail e do Yahoo/Outlook que você controle** e verifique a pasta em que ele realmente caiu, e não apenas se chegou.
6. **Se você alterou bruscamente o volume de envio ou o público-alvo,** trate-o como um aquecimento novo — reduza o volume e aumente gradualmente.
7. **Se tudo acima estiver correto e o problema persistir,** pode ser uma limitação específica do provedor, em vez de um problema na sua configuração — isso pode levar algum tempo para se resolver sozinho, uma vez que a causa subjacente (normalmente reclamações ou rejeições) tenha sido corrigida.

## Dicas

- Corrija a autenticação DNS antes de resolver qualquer outra coisa — qualquer outro fator de entrega (conteúdo, higiene da lista, aquecimento) importa menos se SPF/DKIM/DMARC não estiverem aprovados.
- Trate a validação DNS do assistente de configuração como uma verificação em um momento específico, e não como uma única etapa — execute-a novamente sempre que migrar provedores de DNS ou renovar um domínio por meio de um registrador diferente.
- Uma lista limpa que abre e clica sempre supera uma lista maior que não o faz — resista à tentação de importar uma lista antiga, não verificada, 
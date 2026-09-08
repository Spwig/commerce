---
title: Plano de Ação para Entregabilidade de E-mails
---

Enviar um e-mail é fácil. Fazer com que ele chegue à caixa de entrada, em vez da pasta de spam, é o verdadeiro trabalho — e provedores de caixa de entrada como Gmail e Yahoo agora exigem requisitos técnicos rigorosos antes de sequer considerá-lo. Este plano de ação explica o que configurar, em que ordem, para que suas confirmações de pedido e campanhas cheguem onde os clientes podem vê-las.

Nada aqui é uma tarefa de uma única vez. A entregabilidade é uma reputação que você constrói ao longo do tempo e pode perder rapidamente — a lista de verificação no final vale a pena ser revisada sempre que algo parecer estranho.

## Por que isso é importante

Todos os principais provedores de caixa de entrada pontuam os e-mails recebidos com base na reputação do remetente antes de decidir se entregam, movem para a pasta de spam ou rejeitam completamente. Desde 2024, o Gmail e o Yahoo formalizaram isso em **requisitos explícitos para remetentes em massa** para qualquer pessoa que envie volume significativo:

- **Autentique seu domínio** — registros SPF, DKIM e DMARC válidos.
- **Facilite o cancelamento de inscrição** — um opt-out funcional e de baixa fricção em todos os e-mails de marketing.
- **Mantenha as reclamações de spam baixas** — remetentes em massa que ultrapassam aproximadamente 0,3% de reclamações correm o risco de ter seus e-mails rejeitados ou movidos para a pasta de spam; o alvo mais seguro é bem abaixo de 0,1%.

Se você falhar nesses pontos, não são apenas as campanhas de marketing que sofrem — uma reputação de domínio danificada pode arrastar e-mails transacionais (confirmações de pedido, redefinições de senha) para o spam também, pois o Gmail e o Yahoo julgam cada vez mais a reputação no nível do domínio de envio, e não apenas por tipo de mensagem. As etapas abaixo mostram como atender a todos os três requisitos.

## Etapa 1: Autentique seu domínio de envio

SPF, DKIM e DMARC são registros TXT de DNS que provam aos servidores de e-mail receptores que os e-mails que alegam ser do seu domínio realmente foram enviados por você. A forma como você os configura depende do modo de envio usado pela sua loja — todos os três são configurados em **Configuração de E-mail** na barra lateral de administração (isso abre a lista de Contas de E-mail; consulte [Configuração de E-mail](email-configuration) para o guia completo de configuração de contas).

| Modo de envio | Como a autenticação funciona |
|---|---|
| **SMTP Integrado** (o próprio servidor de e-mail do Spwig) | O Spwig gera automaticamente um par de chaves DKIM para o seu domínio. Adicione uma conta de e-mail, e a **Etapa 4** do assistente de configuração mostrará o status do seu SPF, DKIM e DMARC, além do registro exato a ser adicionado, com opção de copiar para a área de transferência e instruções específicas para Cloudflare, GoDaddy, Namecheap e AWS Route 53. O mesmo registro DNS DKIM também é exibido na própria página de administração da conta, posteriormente, sob **Chaves DKIM configuradas**, caso você precise encontrá-lo novamente. |
| **SMTP Genérico** (um provedor próprio como SendGrid, Mailgun, Amazon SES ou Google Workspace, conectado via credenciais SMTP) | A autenticação ocorre parcialmente no próprio painel desse provedor. A etapa de DNS do assistente de configuração inclui instruções em abas específicas para Gmail, Outlook, SendGrid, Mailgun e Amazon SES — cada uma explica o que configurar no console do provedor (por exemplo, verificar um domínio de envio no SendGrid) e quais registros DNS resultantes adicionar no seu host DNS. |
| **Gateway de e-mail hospedado pelo Spwig** | Disponível em planos hospedados pelo Spwig como uma opção de envio gerenciada. Ele assina os e-mails de saída com DKIM automaticamente e, por padrão, envia de um endereço no próprio domínio verificado do Spwig, funcionando sem nenhuma configuração. Se você quiser enviar do seu próprio domínio através do gateway, converse com seu provedor de hospedagem sobre a verificação — este é um serviço gerenciado, não um fluxo DNS de autoatendimento. |

![Etapa 4 do assistente de configuração de conta de e-mail, mostrando validação de SPF/DKIM/DMARC, abas de provedores DNS e um registro DKIM expandido pronto para copiar](/static/core/admin/img/help/deliverability/wizard-dns-step.webp)

![Painel de chaves DKIM configuradas de uma conta de e-mail SMTP integrada existente, com o registro TXT de DNS e um botão Copiar Registro DNS](/static/core/admin/img/help/deliverability/dkim-dns-record.webp)

Independentemente do modo que você usar, **adicionar o registro DNS em si é sempre uma etapa externa** — você o faz no seu registrador de domínio ou hospedagem de DNS (Cloudflare, GoDaddy, Namecheap, Route 53, ou onde quer que os servidores de nomes do seu domínio apontem), e não dentro do Spwig.

O Spwig pode lhe dizer exatamente o que adicionar e validar que ele está ativo, mas ele não pode acessar seu registrador e adicioná-lo por você.

Alguns pontos importantes antes de começar:

- **Mudanças no DNS não são imediatas.** A propagação pode levar de alguns minutos a 48 horas. O passo de validação do assistente mostrará um registro como com falha ou ausente até que ele tenha se propagado realmente — isso é esperado, não um sinal de que algo está errado.
- **Apenas um registro SPF é permitido por domínio.** Se você já tiver um (da Google Workspace, outro serviço de e-mail, etc.), adicione seu remetente novo ao registro existente com `include:` em vez de criar um segundo registro TXT SPF — dois registros SPF quebrarão a autenticação para todos.
- **O DMARC precisa de SPF ou DKIM para já passar.** Configure-o por último, depois que SPF e DKIM estiverem ambos verificados.

## Etapa 2: Use uma identidade de envio real

Assim que seu domínio estiver autenticado, certifique-se de que o que os destinatários realmente veem apoia isso:

- **Endereço de remetente** — use um endereço no seu próprio domínio autenticado (`orders@seusite.com`), nunca um endereço de provedor gratuito (`seusite@gmail.com`). Um endereço de remetente de provedor gratuito não pode ser autenticado pelos seus registros SPF/DKIM/DMARC, e provedores de caixa de entrada tratam disso como um forte sinal de spam de uma loja.
- **Nome do remetente** — use o nome reconhecível da sua loja, não um rótulo genérico como "Notificações" ou "Sem Resposta".
- **Resposta** — defina um endereço monitorado. Um endereço `noreply@` não monitorado que bata ou descarte silenciosamente respostas é por si só um sinal de reputação moderado, e bloqueia o único canal que os clientes têm para lhe dizer que algo deu errado.

Defina os três sob **Configuração de E-mail > (sua conta) > Configuração do Remetente** — veja [Configuração de E-mail](email-configuration) para o percurso completo dos campos.

## Etapa 3: Aqueça antes de escalar

Um domínio ou IP sem histórico de envio não tem reputação ainda — boa ou ruim — e provedores de caixa de entrada são cautelosos com o desconhecido. Enviar um grande primeiro lote de um domínio novo parece estatisticamente idêntico a um spamer iniciando uma nova campanha, e pode ser colocado na pasta de caixa de entrada mesmo que todos os requisitos técnicos estejam preenchidos.

- Comece com algo menor. Envie suas primeiras campanhas para o público mais engajado e mais propenso a abrir do que para toda a lista de uma só vez — veja [Públicos](audiences) para construir um segmento inicial alvo.
- Aumente gradualmente o volume nas primeiras semanas em vez de pular diretamente para envios da lista completa.
- Se você estiver migrando uma lista existente de outra plataforma, trate-a como o dia 1 para propósito de reputação também — o histórico de envio da sua plataforma antiga não se transfere com o domínio.

## Etapa 4: Mantenha sua lista limpa

Toda reclamação ou erro de entrega custa reputação, e ambos são em grande parte função de quem está na sua lista e de como eles chegaram lá:

- **Envie apenas para pessoas que concordaram.** Contatos importados, listas compradas e endereços coletados de forma não autorizada são a forma mais rápida de aumentar reclamações de spam e erros de entrega.
- **Use confirmação dupla.** O fluxo de consentimento de marketing do Spwig verifica o endereço de e-mail de um assinante antes de enviá-lo e-mails de marketing — veja [Preferências de Comunicação](communication-preferences) para como isso é configurado.
- **Deixe o Spwig fazer sua tarefa de supressão.** O Spwig monitora erros de entrega, reclamações de spam e erros de entrega recorrentes e para de enviar para esses endereços automaticamente, sem necessidade de configuração — veja [Higiene da Lista e Supressões](list-hygiene) para exatamente como isso funciona e quando (raramente) substituí-lo.
- **Remova os assinantes inativos periodicamente** em vez de enviar para os mesmos endereços não engajados por tempo indeterminado — uma lista que está diminuindo, mas que abre e clica, é mais valiosa para sua reputação do que uma lista grande que não o faz.

## Etapa 5: Monitore

Preserve todos os formatos de markdown, caminhos de imagem, blocos de código e termos técnicos.

Problemas de entregabilidade aparecem nos números antes de um cliente informar que um e-mail não chegou.

Abra o [Relatório](campaign-reports) de uma campanha após cada envio e observe:

| Métrica | O que observar |
|---|---|
| **Taxa de rejeição (bounce)** | Predominância de rejeições temporárias (soft bounces) é normal; um aumento na proporção de **rejeições permanentes (hard bounces)** indica que sua lista está acumulando endereços obsoletos ou inválidos. |
| **Reclamações de spam** | Deve permanecer próxima de zero em cada envio. Mantenha-a bem abaixo do limiar de aproximadamente 0,3% que aciona a aplicação de regras para remetentes em massa no Gmail e Yahoo — trate até mesmo um pequeno pico como algo que merece investigação imediata. |
| **Taxa de abertura / taxa de cliques por abertura** | Uma queda súbita e inexplicada entre envios para a mesma lista (não apenas em uma campanha) pode ser um sinal precoce de que os e-mails estão caindo na caixa de spam em vez da caixa de entrada, mesmo antes que os números de rejeição ou reclamações se movam. |

Verifique também periodicamente o cartão de **Endereços suprimidos** no painel do Campaign Studio — um fluxo constante é um decaimento normal da lista, mas um pico súbito merece investigação antes do seu próximo envio (veja [Higiene da Lista](list-hygiene)).

![O cartão de estatísticas de Endereços suprimidos no painel do Campaign Studio](/static/core/admin/img/help/deliverability/suppressed-addresses-card.webp)

Se algo apresentar um pico: pause e verifique primeiro se seus registros DNS ainda são válidos (uma renovação de domínio expirada ou uma alteração acidental no DNS podem quebrar silenciosamente o SPF/DKIM), depois examine o que mudou no conteúdo ou na audiência do envio que o provocou.

## Etapa 6: Higiene de conteúdo

Autenticação e qualidade da lista garantem sua entrada; o conteúdo ainda afeta como você é tratado uma vez lá dentro.

- **Evite padrões que disparam filtros de spam** nas linhas de assunto — MAIÚSCULAS, pontuação excessiva ("!!!") e frases como "aja agora" ou "dinheiro grátis" ainda pesam contra você nos filtros de spam, mesmo de um domínio autenticado.
- **Não envie e-mails apenas com imagens.** Um e-mail que é uma única imagem sem texto real é um padrão clássico de spam; mantenha uma quantidade significativa de conteúdo textual real ao lado de quaisquer imagens.
- **Pré-visualize antes de enviar.** Verifique como o e-mail é renderizado na prática — incluindo em dispositivos móveis — antes de ir para sua lista completa.
- **O link de cancelamento de inscrição já é tratado.** O Spwig adiciona automaticamente um link de cancelamento de inscrição funcional, sem necessidade de login, no rodapé de todos os e-mails de marketing — você não precisa adicionar o seu próprio (veja [Preferências de Comunicação](communication-preferences) para saber exatamente como esse fluxo funciona). Não remova ou oculte-o; um link de cancelamento ausente ou quebrado é, em si, uma violação de política nas regras de remetentes em massa do Gmail e Yahoo, independentemente dos seus outros números.

## "Meus e-mails estão indo para o spam" — lista de verificação para solução de problemas

Siga estes itens em ordem:

1. **Reverifique seus registros DNS.** Abra a etapa de DNS do assistente de configuração da conta (ou o painel DKIM na página administrativa da conta para SMTP integrado) e confirme se SPF, DKIM e DMARC ainda mostram como aprovados.

Uma renovação de domínio, uma migração de provedor de DNS ou uma alteração não relacionada no seu arquivo de zona podem quebrar silenciosamente um destes.
2. **Verifique os números de rejeição e reclamações no relatório da campanha** para o(s) envio(s) afetado(s) — veja [Relatórios de Campanha](campaign-reports).


Um pico em qualquer um deles indica um problema de qualidade da lista ou de conteúdo, em vez de um problema de autenticação.
3. **Verifique a lista de Supressões** ([Higiene da Lista](list-hygiene)) por um salto súbito — se uma grande parte da sua lista estiver falhando há algum tempo, a entregabilidade para o restante também se degrada.
4. **Confirme que seu endereço de Remetente está no seu domínio autenticado**, não em um endereço de provedor gratuito ou em um domínio que não corresponde ao que foi configurado para SPF/DKIM/DMARC.
5. **Envie um e-mail de teste para um endereço Gmail e um endereço Yahoo/Outlook que você controla** e verifique a pasta real em que ele é entregue, não apenas se ele chegou.
6. **Se você alterou recentemente o volume de envio ou o público de forma acentuada,** trate isso como um novo aquecimento — reduza o volume e aumente-o de forma mais gradual.
7. **Se tudo acima estiver correto e o problema persistir,** pode ser uma limitação específica do provedor em vez de uma falha na sua configuração — isso pode levar algum tempo para se resolver por conta própria, uma vez que a causa subjacente (geralmente reclamações ou rejeições) tenha sido corrigida.

## Dicas

- Corrija a autenticação DNS antes de corrigir qualquer outra coisa — cada alavanca de entregabilidade (conteúdo, higiene da lista, aquecimento) é menos importante se o SPF/DKIM/DMARC não estiver passando.
- Trate a validação de DNS do assistente de configuração como uma verificação pontual, não como algo único — execute-a novamente sempre que migrar provedores de DNS ou renovar um domínio por meio de um registrador diferente.
- Uma lista limpa que abre e clica sempre terá melhor desempenho do que uma lista maior que não o faz — resista à tentação de importar uma lista antiga e não verificada "só por garantia".
- Observe seus números em relação aos seus próprios envios passados, não a uma métrica genérica da indústria — seu próprio histórico é o sinal mais confiável de um problema real.
- Se você estiver em um plano hospedado pela Spwig, a assinatura DKIM do gateway de e-mail hospedado e o gerenciamento de reputação são tratados para você — sua responsabilidade restante é a qualidade da lista e o conteúdo, não o DNS.
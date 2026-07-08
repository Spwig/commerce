---
title: Caixa de Saída de SMS
---

A Caixa de Saída de SMS é um registro completo de cada mensagem de texto que sua loja tentou enviar. Use-a para confirmar que as notificações chegaram aos clientes, investigar falhas no envio e entender sua atividade geral de mensagens.

Navegue até **Sistema de SMS > Caixa de Saída de SMS** para visualizar o log das mensagens.

![Lista da Caixa de Saída de SMS com badges de status](/static/core/admin/img/help/sms-outbox/outbox-list.webp)

## Lendo a caixa de saída

Cada linha na caixa de saída representa um tentativa de mensagem e mostra:

- **Telefone** — o número de telefone do destinatário
- **Tipo de Mensagem** — SMS ou WhatsApp
- **Status** — o status atual de entrega (veja abaixo)
- **Criado em** — quando a mensagem foi criada
- **Enviado em** — quando a mensagem foi enviada ao provedor

A barra de resumo no topo mostra contagens agregadas para os status mais importantes, à primeira vista.

## Status das mensagens

| Status | Significado |
|--------|-------------|
| Pendente | A mensagem está aguardando para ser coletada pela fila de envio |
| Em fila | A mensagem foi adicionada à fila e será enviada em breve |
| Enviado | O provedor aceitou a mensagem para entrega |
| Entregue | O provedor confirmou que a mensagem chegou ao dispositivo do destinatário |
| Falhou | O provedor rejeitou ou não conseguiu entregar a mensagem |
| Pulado | O envio foi intencionalmente pulado (veja as razões de pulo abaixo) |
| Registrado no Sandbox | A mensagem foi registrada apenas (a loja está em modo de teste/sandbox) |

> **Enviado vs. Entregue:** Um status **Enviado** significa que a mensagem saiu da sua loja e foi aceita pelo provedor. Um status **Entregue** significa que o provedor recebeu um comprovante de entrega do operador. Nem todos os provedores suportam comprovantes de entrega — se o seu provedor não suportar, as mensagens podem mostrar **Enviado** mas nunca avançar para **Entregue**, o que é normal.

## Visualizando detalhes da mensagem

Clique em qualquer linha na caixa de saída para ver os detalhes completos dessa mensagem:

- O texto completo da **Mensagem** que foi enviada
- O **ID da Mensagem do Provedor** — o número de referência do provedor de SMS (útil ao contactar o suporte do provedor)
- A **Mensagem de Erro** (para mensagens falhadas) — a mensagem de erro exata retornada pelo provedor
- A **Contagem de Tentativas** — quantas vezes o Spwig tentou enviar a mensagem
- Todos os timestamps (criado, em fila, enviado, entregue)

## Filtrando a caixa de saída

Use os filtros do lado direito para reduzir a lista:

- **Status** — mostrar apenas mensagens com um status específico
- **Tipo de Mensagem** — mostrar apenas SMS ou apenas mensagens do WhatsApp
- **Data** — filtrar por dia em que a mensagem foi criada

A caixa de pesquisa no topo permite pesquisar por número de telefone, conteúdo da mensagem ou ID da mensagem do provedor.

## Entendendo razões de pulo

Mensagens puladas não foram enviadas porque o Spwig determinou que o envio era inapropriado ou desnecessário. Razões comuns de pulo:

| Razão de Pulo | O que significa |
|---------------|----------------|
| `user_preference_disabled` | O cliente desativou as notificações por SMS em suas configurações de conta |
| `unsubscribed` | O cliente se desinscreveu das mensagens por SMS |
| `no_provider` | Nenhuma conta de provedor de SMS padrão ativa está configurada |
| `template_inactive` | O modelo para este tipo de notificação está inativo |

Uma mensagem pulada não é um fracasso — significa que o sistema funcionou conforme o esperado. No entanto, uma contagem alta de pulos `no_provider` indica que você precisa configurar e ativar uma conta de provedor de SMS.

## Solução de problemas de entregas falhadas

Se as mensagens mostrarem um status **Falhou**, siga estas etapas:

1. Clique na mensagem falhada para ver sua **Mensagem de Erro**
2. Causas comuns de erro:

   | Erro | Causa provável |
   |-------|-------------|
   | Número de telefone inválido | O número de telefone do cliente está faltando ou não está no formato E.164 |
   | Autenticação falhou | Suas credenciais do provedor são inválidas ou expiraram — atualize-as em **SMS Provider Accounts** |
   | Conta suspensa | Sua conta do provedor foi suspensa — faça login no painel de controle do provedor |
   | Fundos insuficientes | O saldo da conta do provedor está muito baixo — recarregue-a |
   | Rejeição do operador | O operador de destino bloqueou a mensagem (muitas vezes devido a filtros de conteúdo) |

3. Após resolver o problema subjacente, as mensagens futuras serão enviadas normalmente — a fila de saída é um log somente leitura e as mensagens individuais não podem ser reenviadas manualmente

## A fila de saída é somente leitura

A fila de saída de SMS é um registro apenas. Você não pode adicionar mensagens à fila de saída manualmente, nem pode reenviar mensagens individuais a partir daqui. As mensagens são enviadas automaticamente pelo Spwig quando os eventos relevantes ocorrem (por exemplo, um pedido é feito).

## Dicas

- Revise a fila de saída após um período de alta atividade para confirmar que todas as mensagens de confirmação de pedido foram entregues com sucesso
- Se um cliente disser que não recebeu um SMS, procure na fila de saída pelo seu número de telefone para ver se a mensagem foi enviada, falhou ou foi pular
- Um aumento súbito em mensagens **Falhadas** geralmente indica um problema com suas credenciais ou saldo da conta do provedor — verifique imediatamente esses itens
- Se você ver muitas mensagens **Puladas** com a razão `no_provider`, navegue até **SMS System > SMS Provider Accounts** e certifique-se de que uma conta padrão ativa foi configurada
- A hierarquia de datas no topo da lista permite que você navegue rapidamente por dia, mês ou ano para revisar mensagens históricas
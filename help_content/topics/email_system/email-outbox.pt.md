---
title: Caixa de Saída de E-mail
---

A Caixa de Saída de E-mail é um registro completo de todos os e-mails enviados ou tentados de serem enviados pela sua loja — confirmações de pedidos, atualizações de envio, relatórios de administrador e todas as outras mensagens transacionais. Use-a para confirmar entregas, investigar falhas e gerenciar a fila de e-mails.

Navegue até **Sistema de E-mail > Caixa de Saída de E-mail** para visualizar o registro de e-mails.

![Lista da Caixa de Saída de E-mail com badges de status](/static/core/admin/img/help/email-outbox/outbox-list.webp)

## Lendo a caixa de saída

A barra de resumo no topo mostra contagens para cada categoria de status. A lista abaixo mostra e-mails individuais com:

- **Assunto** — a linha do assunto do e-mail
- **Para** — o endereço de e-mail do destinatário
- **De** — o endereço do remetente usado
- **Status** — o status atual de entrega
- **Enfileirado em** — quando o e-mail entrou na fila
- **Enviado em** — quando o e-mail foi enviado ao provedor
- **Contagem de tentativas** — quantas tentativas de envio foram feitas

## Status dos e-mails

| Status | Significado |
|--------|-------------|
| Enfileirado | O e-mail está aguardando na fila para ser enviado |
| Enviando | O e-mail está sendo atualmente enviado ao provedor |
| Enviado | O provedor aceitou o e-mail |
| Retido | O e-mail está pausado e não será enviado até ser liberado |
| Registrado | O e-mail foi registrado, mas não foi enviado (modo de teste ou configuração apenas de registro) |
| Falhado | O provedor rejeitou ou não conseguiu entregar o e-mail |
| Rejeitado | O e-mail foi enviado, mas foi rejeitado pelo servidor de e-mail do destinatário |
| Pulado | O envio foi pulado por um motivo do sistema |

## Visualizando detalhes do e-mail

Clique em qualquer e-mail na lista para ver os detalhes completos:

- O **corpo HTML** e o **corpo de texto** completos do e-mail
- **ID da mensagem do provedor** — a referência do seu provedor de e-mail (use isso ao entrar em contato com o suporte do provedor)
- **Mensagem de erro** — a mensagem de erro exata para e-mails falhados ou rejeitados
- **Contagem de tentativas** e **Máximo de tentativas** — quantas vezes o envio foi tentado
- Todos os carimbos de tempo: criado, enfileirado, enviado e falhado

## Filtrando a caixa de saída

Use os filtros à direita para estreitar sua visão:

- **Status** — mostrar e-mails de um status específico de entrega
- **Data** — filtrar por quando os e-mails foram criados ou enviados
- **Tipo de modelo** — mostrar apenas e-mails de um tipo específico de notificação (por exemplo, apenas confirmações de pedidos)

A caixa de pesquisa no topo busca por assunto, endereço do destinatário, endereço do remetente ou ID da mensagem do provedor.

## Liberando e-mails retidos

E-mails com status **Retido** estão pausados — eles não serão enviados até que você os libere. Um e-mail pode estar retido se sua loja estivesse em modo de manutenção quando foi gerado, ou se uma ação de administrador o colocou em pausa.

Para liberar e-mails retidos:
1. Selecione os e-mails que deseja liberar (marque as caixas à esquerda)
2. Escolha **Liberar e-mails retidos para envio** no menu suspenso **Ações**
3. Clique em **Ir**

E-mails liberados passam para o status **Enfileirado** e são enviados no próximo ciclo de processamento da fila.

## E-mails agendados

Alguns e-mails são agendados para serem enviados em um horário futuro — por exemplo, relatórios de digesto semanal são agendados para serem enviados em um dia e hora específicos. Navegue até **Sistema de E-mail > E-mails Agendados** para visualizar os envios agendados próximos.

A lista de e-mails agendados mostra:

- **Tipo de modelo** — o tipo de e-mail agendado
- **E-mail do destinatário** — o endereço para o qual será enviado
- **Agendado para** — a data e hora em que o e-mail deve ser enviado
- **Status** — Pendente (ainda não enviado), Enviado ou Falhado

Os e-mails agendados são processados automaticamente quando chegam ao horário agendado — nenhuma ação manual é necessária.

## Solucionando entregas falhadas

Se os e-mails mostrarem um status **Falhado**, clique para ver a mensagem de erro e siga estas etapas:

### Causas comuns e soluções

| Sintoma | Causa provável | O que fazer |
|---------|-------------|------------|
| "Autenticação falhou" | As credenciais do provedor de e-mail são inválidas | Atualize as credenciais em **Sistema de E-mail > Contas de E-mail** |
| "Conexão recusada" / "Tempo esgotado" | Seu servidor de e-mail não está acessível | Verifique a página de status do provedor de e-mail; teste a conexão em **Contas de E-mail** |
| "Destinatário inválido" | O endereço de e-mail do cliente está malformado | Revise a conta do cliente e corrija seu e-mail |
| E-mails rejeitados | O servidor de e-mail do destinatário rejeitou o e-mail | O endereço pode não existir ou sua caixa de entrada está cheia; não tente novamente excessivamente |
| Taxa de falha alta de repente | Problema do provedor ou credenciais expiradas | Verifique o status do provedor; re-teste a conexão em **Contas de E-mail** |

### Verificando a conexão da sua conta de e-mail

Se muitos e-mails estão falhando, teste sua conta de e-mail:

1. Navegue até **Sistema de E-mail > Contas de E-mail**
2. Encontre sua conta ativa e verifique o status de **Conexão**
3. Se a conexão mostrar um erro, clique na conta e use a opção **Testar Conexão** para diagnosticar o problema

### Comportamento de tentativas

O Spwig tenta automaticamente reenviar e-mails falhos até o limite de **Máximo de Tentativas**. A contagem de tentativas mostrada em cada e-mail informa quantas tentativas foram feitas. Uma vez atingido o limite de tentativas, o e-mail permanece em status **Falhou** e nenhuma tentativa automática adicional ocorre.

## E-mails rejeitados

Um e-mail **Rejeitado** foi enviado, mas foi retornado pelo servidor de e-mail do destinatário. Existem dois tipos de rejeições:

- **Rejeição dura** — o endereço de e-mail não existe ou o domínio não aceita e-mails. Não tente reenviar rejeições duras; o endereço é inválido
- **Rejeição suave** — um problema temporário (caixa de entrada cheia, servidor temporariamente indisponível). Pode ter sucesso em uma nova tentativa

Muitas rejeições para o mesmo endereço podem prejudicar sua reputação de remetente com os provedores de e-mail. Se você notar rejeições repetidas para o mesmo endereço do cliente, atualize ou remova esse endereço da conta do cliente.

## Dicas

- Revise a pasta de saída após eventos importantes, como uma venda flash ou o lançamento de um produto grande, para confirmar que todos os e-mails de confirmação de pedido foram enviados com sucesso
- Se um cliente disser que não recebeu um e-mail, procure na pasta de saída pelo seu endereço de e-mail para ver se foi enviado, falhou ou foi ignorado
- Um aumento súbito em falhas geralmente indica um problema de credencial ou conta — verifique **Contas de E-mail** imediatamente
- O status **Retido** não é um falha — apenas significa que o e-mail está aguardando. Libere os e-mails retidos quando estiver pronto para enviá-los
- Use o filtro **Tipo de Modelo** para revisar rapidamente todos os e-mails de um tipo — por exemplo, verifique se todos os pedidos confirmados nas últimas 7 dias têm o status **Enviado**
- A navegação hierárquica de data (dia / mês / ano) no topo da lista é útil para revisar a pasta de saída para um período específico
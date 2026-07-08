---
title: Logs de Entrega de Webhook
---

Toda vez que sua loja tenta enviar um webhook, um registro de entrega é criado. Esses logs permitem que você veja exatamente o que foi enviado, se foi bem-sucedido e o que aconteceu durante quaisquer tentativas de repetição. Este guia explica como ler os logs de entrega e depurar problemas quando as entregas falham.

## Visualizando logs de entrega

Navegue até **Integrações > Entregas de Webhook** para ver o histórico completo de todas as tentativas de entrega de webhook em todos os seus endpoints.

![Logs de entregas de webhook](/static/core/admin/img/help/webhook-deliveries/delivery-list.webp)

A lista mostra o nome do endpoint de cada entrega, o tipo de evento, o status, o código de resposta HTTP, o tempo de resposta e quantas tentativas foram feitas.

Os logs de entrega são somente leitura — eles são criados automaticamente quando os eventos ocorrem e não podem ser editados.

## Status de entrega

Cada entrega tem um desses status:

| Status | O que significa |
|--------|---------------|
| **Pendente** | A entrega está na fila e ainda não foi tentada |
| **Sucesso** | O servidor de destino respondeu com um código de status HTTP 2xx — entrega confirmada |
| **Falha** | Todas as tentativas de entrega foram esgotadas — a entrega não será repetida novamente |
| **Repetindo** | A tentativa mais recente falhou, mas o sistema tentará novamente no horário de repetição agendado |
| **Bloqueado no Ambiente de Teste** | A entrega foi bloqueada porque o URL do endpoint não está acessível no ambiente atual |

Uma entrega é considerada bem-sucedida quando o servidor de destino retorna qualquer código de resposta HTTP 2xx (200, 201, 202, etc.). Qualquer outro código de resposta — incluindo 3xx redirecionamentos ou erros 4xx/5xx — é tratado como uma falha.

## Filtros de entregas

Use o painel de filtro à direita para reduzir a lista:

- **Status** — Visualizar apenas entregas com falha, em repetição ou bem-sucedidas
- **Tipo de Evento** — Ver todas as entregas para um evento específico (por exemplo, todas as entregas `order.created`)
- **Endpoint** — Visualizar entregas para um endpoint específico
- **Criado em** — Filtrar por intervalo de data

Use a barra de pesquisa para pesquisar por tipo de evento ou nome do endpoint, ou para encontrar uma entrega específica pelo seu ID.

## Lendo detalhes de uma entrega

Clique em qualquer entrega para ver seus detalhes completos. Os registros de entrega são somente leitura.

### Resumo

- **ID** — O identificador único para esta tentativa de entrega
- **Endpoint** — Qual endpoint de webhook esta entrega foi enviada (link para o registro do endpoint)
- **Tipo de Evento** — O evento que disparou esta entrega (por exemplo, `order.paid`)
- **Status** — Status atual da entrega

### Payload

A seção **Payload** mostra os dados exatos em formato JSON que foram enviados ao seu endpoint. Isso inclui o tipo de evento, um carimbo de data/hora e os dados completos do evento. Use isso para verificar se seu servidor de destino está recebendo a estrutura de dados correta.

### Resposta

A seção **Resposta** mostra o que seu servidor respondeu:

- **Código de Status da Resposta** — O código de status HTTP retornado por seu servidor. Colorido: verde para 2xx (sucesso), amarelo para 4xx (erro do cliente), vermelho para 5xx (erro do servidor).
- **Tempo de Resposta** — Quanto tempo seu servidor levou para responder em milissegundos. Colorido: verde abaixo de 500ms, amarelo até 2 segundos, vermelho acima de 2 segundos.
- **Corpo da Resposta** — O corpo da resposta do seu servidor (cortado em 1.000 caracteres). Isso pode ajudar a identificar por que seu servidor rejeitou o webhook.
- **Cabeçalhos da Resposta** — Os cabeçalhos retornados por seu servidor.

### Detalhes do erro

Se a entrega falhou, a seção **Detalhes do Erro** mostra a mensagem de erro — por exemplo, `Conexão recusada`, `Timeout após 30s` ou o erro HTTP do seu servidor.

### Informações de repetição

- **Contagem de Tentativas** — Quantas tentativas de entrega foram feitas (incluindo a primeira tentativa)
- **Próxima Tentativa em** — Quando a próxima tentativa será feita (mostrado apenas para entregas no status **Repetindo**)

As repetições seguem um agendamento de back-off exponencial — o intervalo entre as repetições aumenta com cada tentativa para evitar sobrecarregar um servidor temporariamente indisponível. Com um máximo de 5 repetições (padrão), o agendamento de repetição abrange várias horas.

## Tentar novamente entregas falhas manualmente

Se quiser tentar novamente uma entrega imediatamente, sem esperar pelo agendamento automático:

1. Selecione as caixas de seleção ao lado das entregas que deseja tentar novamente
2. No menu suspenso **Ação**, escolha **Tentar novamente as entregas selecionadas**
3. Clique em **Ir**

Apenas entregas que não estão no status **Sucesso** serão enfileiradas para tentativa novamente. As entregas bem-sucedidas são ignoradas.

Isso é útil quando você corrigiu um problema com seu servidor de recebimento e deseja reprocessar eventos falhos sem esperar.

## Diagnóstico de falhas comuns

### Códigos de resposta HTTP 4xx

Uma resposta 4xx do seu servidor normalmente significa que há um problema com a solicitação — autenticação falhou, a URL do endpoint mudou ou seu servidor rejeitou o formato da carga útil. Verifique:

- A URL do endpoint está correta?
- Seu servidor está verificando a assinatura HMAC corretamente? Uma discordância causa muitos servidores a retornarem 401 ou 403.
- A estrutura da carga útil mudou? Verifique a carga útil no log de entrega contra o que seu servidor espera.

### Códigos de resposta HTTP 5xx

Uma resposta 5xx significa que seu servidor encontrou um erro interno ao processar o webhook. Verifique os próprios logs de erro do servidor para diagnosticar o problema.

### Conexão recusada / Timeout

Esses erros significam que o Spwig não conseguiu acessar seu servidor de forma alguma:

- O servidor está em execução e publicamente acessível?
- A URL está correta (incluindo o protocolo correto — http ou https)?
- Um firewall está bloqueando solicitações entrantes?
- O tempo de resposta do servidor está ultrapassando o tempo limite configurado? Se sim, aumente a configuração de **Timeout** no endpoint ou otimize o manipulador de webhook do seu servidor para responder rapidamente (idealmente dentro de 5 segundos).

### Bloqueado no Sandbox

As entregas são bloqueadas para URLs de localhost ou endereços de rede interna. Os endpoints de webhook devem ser acessíveis publicamente. Use uma ferramenta como ngrok durante o desenvolvimento para expor um servidor local publicamente.

## Dicas

- Trate as entregas **Falhas** com urgência — os dados do evento ainda estão na carga útil, e você pode tentar novamente manualmente uma vez que o problema esteja resolvido.
- Se você ver muitas entregas **Tentando novamente** para um único endpoint, abra o registro do endpoint e verifique a seção **Saúde** — o endpoint pode estar prestes a ser desativado automaticamente.
- O tempo de resposta importa: configure seu manipulador de webhook para responder rapidamente (em alguns segundos) e processe a carga útil assincronamente em segundo plano. Um manipulador lento causa falhas de timeout mesmo que sua lógica esteja correta.
- Use o filtro **Tipo de Evento** para verificar o histórico de entregas para um tipo de evento específico ao investigar se sua integração está recebendo os eventos corretos.
- Os logs de entrega se acumulam ao longo do tempo. Use o filtro de data para se concentrar nas entregas recentes e evitar navegar por um histórico antigo.
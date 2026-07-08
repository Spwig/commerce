---
title: Eventos de Rastreamento
---

Eventos de rastreamento registram pontos de verificação do status do envio ao longo do ciclo de vida de entrega — cada evento captura status (em trânsito, saiu para entrega, entregue), carimbo de data/hora, localização, descrição e dados brutos do transportador. Os eventos são criados automaticamente via notificações de webhook do transportador ou manualmente pelos comerciantes. Os clientes veem o histórico de eventos de rastreamento em suas contas e e-mails de confirmação de pedido, fornecendo visibilidade em tempo real sobre a entrega.

Essa página de administração exibe o histórico de eventos somente para leitura para fins de auditoria e suporte ao cliente.

## Estrutura de Evento de Rastreamento

Cada evento contém:

**Informações de Status**:
- **Status**: in_transit, out_for_delivery, delivered, exception, failed, returned
- **Descrição**: Status legível por humano (ex.: "Pacote chegou na instalação de triagem")
- **Código de Status do Transportador**: Status original do transportador (ex.: "DEP" para saiu)

**Dados de Localização**:
- **Cidade**: Cidade do local do evento
- **Estado**: Estado/província do local do evento
- **País**: País do local do evento
- **Código Postal**: Código postal/CEP do local do evento

**Carimbos de Data/Hora**:
- **Ocorreu Em**: Quando o evento realmente aconteceu (hora do transportador)
- **Criado Em**: Quando o evento foi registrado no Spwig (hora do sistema)

**Metadados**:
- **Dados Brutos**: Resposta JSON completa da API do transportador
- **Envio**: ID do envio vinculado

---

## Tipos de Status de Evento

**in_transit**: Pacote se movendo pela rede do transportador
- Exemplos: "Saiu da instalação", "Chegou ao centro de distribuição", "Em trânsito para a próxima instalação"

**out_for_delivery**: Pacote em veículo de entrega
- Exemplos: "Saiu para entrega", "No veículo de entrega"

**delivered**: Pacote entregue com sucesso
- Exemplos: "Entregue à porta principal", "Deixado na recepção", "Entregue ao destinatário"

**exception**: Problema de entrega que requer atenção
- Exemplos: "Atraso por condições climáticas", "Endereço incorreto", "Tentativa de entrega falhou"

**failed**: Entrega falhou permanentemente
- Exemplos: "Indeliverável conforme endereçado", "Recusado pelo destinatário"

**returned**: Pacote sendo devolvido ao remetente
- Exemplos: "Iniciada a devolução ao remetente", "Pacote retornando"

---

## Como os Eventos de Rastreamento são Criados

### Automático (Webhooks do Transportador)

**Fluxo de Trabalho**:
1. Transportador escaneia o pacote (saída, chegada, entrega)
2. Transportador envia webhook para o endpoint de webhook do Spwig
3. Webhook registrado na tabela WebhookLog
4. Sistema analisa a carga útil do webhook
5. TrackingEvent criado com dados extraídos
6. Notificação por e-mail ao cliente enviada (se configurado)

**Benefícios**:
- Atualizações em tempo real (não é necessário polling)
- Carimbos de data/hora precisos do transportador
- Histórico de eventos completo mantido automaticamente

### Manual (Entrada do Comerciante)

**Fluxo de Trabalho**:
1. Navegue até os detalhes do envio
2. Clique em "Adicionar Evento de Rastreamento"
3. Selecione o status do menu suspenso
4. Insira a descrição
5. Opcional: Insira dados de localização
6. Defina o carimbo de data/hora de ocorrência
7. Salve

**Casos de Uso**:
- Transportadores sem suporte a webhook
- Correções manuais de envio
- Entrega local (não transportador)
- Atualizações de status internas

---

## Ordem de Exibição de Eventos

Eventos exibidos em **ordem cronológica reversa** (mais recentes primeiro):

**Exemplo de Exibição**:
```
13 de fev de 2026 10:30 AM - Entregue (Brooklyn, NY)
13 de fev de 2026 08:15 AM - Saiu para entrega (Brooklyn, NY)
12 de fev de 2026 11:45 PM - Chegou na instalação local (Brooklyn, NY)
12 de fev de 2026 06:30 PM - Em trânsito (Newark, NJ)
12 de fev de 2026 02:15 PM - Saiu da origem (Filadélfia, PA)
12 de fev de 2026 09:00 AM - Coletado (Filadélfia, PA)
```

---

## Visibilidade para Clientes

Eventos de rastreamento exibidos aos clientes em:

**E-mail de Confirmação de Pedido**:
- Status do evento mais recente
- Data estimada de entrega
- Link de rastreamento

**Conta do Cliente > Detalhes do Pedido**:
- Cronologia completa de eventos
- Descrições dos eventos
- Histórico de localização
- Carimbos de data/hora

**Página de Rastreamento** (se habilitada):
- URL dedicada de rastreamento
- Cronologia visual
- Logotipo do transportador
- Mapa de entrega (se dados de localização disponíveis)

---

## Filtros de Eventos de Rastreamento

**Filtros Úteis**:
- **Envio**: Visualizar eventos para um envio específico
- **Status**: Filtrar por tipo de evento (entregue, in_transit, etc.)
- **Intervalo de Data**: Eventos dentro de um período de tempo
- **Localização**: Eventos em uma cidade/estado específico

**Casos de Uso**:
- "Mostrar todos os envios entregues hoje"
- "Encontrar todas as exceções da semana passada"
- "Rastrear envios atualmente em trânsito"

---

## Dados Brutos (Depuração)

**Campo de Dados Brutos**:
- Armazena a resposta completa da API do transportador como JSON
- Útil para depurar problemas de webhook
- Contém metadados específicos do transportador

**Exemplo de Dados Brutos** (FedEx):
```json
{
  "event_type": "OD",
  "event_description": "Out for delivery",
  "timestamp": "2026-02-13T08:15:00Z",
  "location": {
    "city": "Brooklyn",
    "state": "NY",
    "postal_code": "11201",
    "country": "US"
  },
  "delivery_signature": null,
  "estimated_delivery": "2026-02-13T17:00:00Z"
}
```

**Quando Verificar Dados Brutos**:
- Descrição do evento não clara
- Dados de localização ausentes
- Erros de processamento de webhook
- Elevação de suporte ao transportador

---

## Temporização de Eventos

**Ocorreu Em** vs **Criado Em**:

**Ocorreu Em**: Quando o evento do transportador realmente aconteceu
- Exemplo: Pacote escaneado às 10:30 AM

**Criado Em**: Quando o Spwig recebeu o webhook
- Exemplo: Webhook recebido às 10:32 AM (atraso de 2 minutos)

**Por Que Diferente?**:
- Latência de rede
- Processamento em lote do transportador
- Atrasos em tentativas de webhook

**Use Ocorreu Em para exibição ao cliente** — reflete mais precisamente o progresso real da entrega.

---

## Dicas

- **Eventos são somente leitura** — Não podem ser editados após a criação (integridade de auditoria)
- **Verifique os dados brutos para detalhes** — Mais informações do que os campos exibidos
- **Monitore o atraso de webhook** — Atrasos grandes entre occurred_at e created_at indicam problemas com webhooks
- **Use para suporte ao cliente** — A cronologia de eventos ajuda a diagnosticar problemas de entrega
- **Rastreie padrões de entrega** — Analise a temporização dos eventos para desempenho do transportador
- **Configure notificações** — Envie e-mails automáticos aos clientes em eventos-chave (out_for_delivery, delivered)
- **Não exclua eventos** — Mantenha o histórico completo de auditoria
- **Verifique WebhookLog para falhas** — Eventos ausentes podem indicar erros no processamento de webhooks
- **Dados de localização variam por transportador** — Alguns transportadores fornecem localização detalhada, outros mínima
- **Eventos de exceção precisam de atenção** — Monitore e acompanhe exceções de entrega

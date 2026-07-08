---
title: Logs de Webhook
---

Os logs de webhook fornecem um rastreamento de auditoria permanente de todas as solicitações de webhook recebidas dos correios — capturando o método da solicitação, URL do endpoint, cabeçalhos, payload, status de processamento (pendente/processado/falhado) e resposta. Cada webhook é registrado antes do processamento para garantir que nenhum evento seja perdido em caso de falha no processamento. Os logs permitem depurar problemas de integração de webhook, monitorar a confiabilidade da API dos correios e reconstruir cronologias de entregas para suporte ao cliente.

Essa página de administração somente leitura ajuda a solucionar problemas de webhook e verificar a saúde da integração com os correios.

## Estrutura do Log de Webhook

Cada entrada de log registra:

**Detalhes da Solicitação**:
- **Chave do Fornecedor**: Qual correio enviou o webhook (fedex, ups, dhl)
- **Endpoint**: Caminho da URL do webhook (ex.: `/webhooks/shipping/fedex/`)
- **Método**: Método HTTP (geralmente POST)
- **Cabeçalhos**: Cabeçalhos da solicitação (JSON)
- **Payload**: Corpo da solicitação (JSON)

**Processamento**:
- **Status de Processamento**: pendente, processado, falhado
- **Mensagem de Erro**: Motivo da falha (se status=falhado)
- **Resposta**: Resposta HTTP enviada ao correio
- **Código de Status da Resposta**: 200, 400, 500, etc.

**Marcadores de Tempo**:
- **Recebido em**: Quando o webhook chegou
- **Processado em**: Quando o processamento foi concluído

---

## Valores de Status de Processamento

**pendente**: Webhook recebido, aguardando processamento
- Normal por um breve momento após o recebimento
- Se estiver preso em pendente, indica backlog da fila de processamento

**processado**: Webhook processado com sucesso
- Criado o TrackingEvent
- Notificação ao cliente enviada (se aplicável)
- Resposta 200 enviada ao correio

**falhado**: Processamento do webhook falhou
- Verifique o campo error_message para a razão
- Causas comuns: JSON inválido, envio desconhecido, evento duplicado

---

## Fluxo de Webhook

**Fluxo Normal**:
```
1. Correio escaneia o pacote
   ↓
2. Correio envia POST para o endpoint de webhook do Spwig
   ↓
3. Spwig cria WebhookLog (status=pending)
   ↓
4. Trabalhador de fundo processa o webhook
   ↓
5. Analisa o payload JSON
   ↓
6. Localiza o envio correspondente (pelo número de rastreamento)
   ↓
7. Cria TrackingEvent
   ↓
8. Atualiza WebhookLog (status=processed)
   ↓
9. Envia resposta HTTP 200 ao correio
```

**Cenários de Falha**:
- **JSON Inválido**: Correio enviou dados malformados → status=falhado, erro="erro de análise de JSON"
- **Envio Desconhecido**: Número de rastreamento não corresponde a nenhum envio → status=falhado, erro="Envio não encontrado"
- **Duplicado**: Evento já existe → status=falhado, erro="Evento duplicado"

---

## Depuração de Falhas de Webhook

**Passo a Passo**:

**1. Filtrar por Status=Falhado**
- Navegue até Transporte > Logs de Webhook
- Filtro: Status de Processamento = "falhado"
- Revise as falhas recentes

**2. Verificar Mensagem de Erro**
- Clique na entrada do log
- Leia o campo error_message
- Erros comuns:
  - "Envio não encontrado" → Mismatch no número de rastreamento
  - "Erro de decodificação de JSON" → Correio enviou JSON inválido
  - "Campo obrigatório ausente" → Payload está faltando dados esperados

**3. Inspecionar Payload**
- Visualize o payload JSON bruto
- Verifique se a estrutura corresponde ao formato esperado
- Confira campos ausentes (tracking_id, event_type, etc.)

**4. Verificar se o Envio Existe**
- Extraia o número de rastreamento do payload
- Pesquise os Envios pelo número de rastreamento
- Garanta que o envio exista e use o correio correto

**5. Verificar Configuração do Fornecedor**
- Verifique se a conta do fornecedor está ativa
- Confirme se a URL do endpoint de webhook está correta
- Teste as credenciais da API do fornecedor

**6. Reenviar Processamento** (se aplicável)
- Alguns processadores de webhook suportam reenvio manual
- Resolva o problema subjacente primeiro
- Reenvie o webhook falhado

---

## Problemas Comuns de Webhook

**Problema 1: "Envio não encontrado"**

**Causa**: Número de rastreamento no webhook não corresponde a nenhum envio
- Erro de digitação ao criar o envio
- Webhook para conta diferente
- Envio excluído antes do recebimento do webhook

**Solução**:
- Verifique a ortografia do número de rastreamento
- Confira se o fornecedor do envio corresponde ao provedor do webhook
- Recrie o envio se necessário

---

**Problema 2: "Erro de decodificação de JSON"**

**Causa**: Correio enviou JSON malformado
- Raro, geralmente bug na API do correio
- Problemas de codificação de caracteres

**Solução**:
- Entre em contato com o suporte do correio com o payload bruto
- Verifique os cabeçalhos para codificação de charset
- Confirme a URL do endpoint no painel do correio

---

**Problema 3: Webhooks duplicados**

**Causa**: Correio envia o mesmo evento múltiplas vezes
- Lógica de reenvio (correio não recebeu resposta 200)
- Bug no correio

**Solução**:
- Sistema rejeita automaticamente duplicados (comportamento normal)
- Verifique se o response_status_code é 200
- Se persistir, entre em contato com o suporte do correio

---

**Problema 4: Webhooks ausentes**

**Causa**: Webhook esperado nunca foi recebido
- Correio não enviou (escaneio perdido)
- Endpoint de webhook malconfigurado no painel do correio
- Firewall bloqueando solicitações

**Solução**:
- Verifique a configuração do webhook no painel do correio
- Confirme se a URL do endpoint é pública e acessível
- Teste o endpoint com curl/Postman
- Verifique as regras de firewall do servidor

---

## Configuração do Endpoint de Webhook

**URLs de Webhook Típicas**:
```
FedEx: https://yourdomain.com/webhooks/shipping/fedex/
UPS: https://yourdomain.com/webhooks/shipping/ups/
DHL: https://yourdomain.com/webhooks/shipping/dhl/
```

**Configuração no Painel do Correio**:
1. Faça login no portal de desenvolvedores do correio
2. Navegue até as configurações de webhook
3. Insira a URL de webhook do Spwig
4. Selecione os eventos para assinar (atualizações de rastreamento, entregas, exceções)
5. Salve a configuração
6. Teste o webhook com a ferramenta de teste do correio

**Segurança**:
- Webhooks requerem HTTPS (não HTTP)
- Alguns correios assinam as solicitações (verifique a assinatura)
- Lista de IPs permitidos (se o correio fornecer IPs estáticos)

---

## Monitoramento da Saúde do Webhook

**Métricas Principais**:

**Taxa de Sucesso**:
```
Taxa de Sucesso = (Processado / Total) × 100%

Meta: >98%
```

**Tempo de Processamento**:
```
Tempo Médio = Processado Em - Recebido Em

Meta: <2 segundos
```

**Padrões de Falha**:
- Pico súbito de falhas → Mudança ou falha na API do correio
- Falhas consistentes "envio não encontrado" → Problema de sincronização de números de rastreamento
- Todos os webhooks falhados → Problema na configuração do endpoint

**Estratégia de Monitoramento**:
- Verifique a taxa de falha diariamente
- Alertar se taxa de falha >5%
- Revise as mensagens de erro semanalmente
- Compare com a página de status do correio

---

## Retenção de Webhook

**Os logs são permanentes** - nunca são excluídos automaticamente

**Por que permanentes**:
- Conformidade com auditoria
- Suporte ao cliente (reconstruir cronologia de entregas)
- Resolução de disputas
- Depuração de webhook

**Armazenamento**: Logs armazenados de forma eficiente (JSON compactado)

---

## Dicas

- **Webhooks são logs de auditoria permanentes** - Nunca exclua, mesmo que sejam processados com sucesso
- **Verifique webhooks falhados diariamente** - Identifique problemas de integração cedo
- **Monitore o atraso de processamento** - Atraso longo indica problema de desempenho
- **Salve payloads brutos** - Essencial para depurar mudanças na API do correio
- **Teste a configuração do endpoint** - Use ferramentas de teste do correio para verificar a configuração
- **Ative assinatura de webhook** - Verifique se as solicitações realmente vêm do correio
- **Liste IPs do correio** - Se o correio fornecer faixas de IPs estáticos
- **Configure alertas** - Notifique quando a taxa de falha ultrapassar o limite
- **Compare com o status do correio** - Falhas em webhooks podem indicar falha no correio
- **Documente formatos de payload do correio** - Ajuda quando o correio atualiza a API
- **Mantenha URLs de webhook estáveis** - Alterar URLs exige atualização no painel do correio

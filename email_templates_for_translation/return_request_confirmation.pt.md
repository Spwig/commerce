---
template_type: return_request_confirmation
category: Returns
---

# Email Template: return_request_confirmation

## Subject
Solicitação de Devolução Recebida - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#eff6ff' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1e40af' }}">
          Solicitação de Devolução Recebida
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1e40af' }}">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nós recebemos sua solicitação de devolução para o pedido <strong>#{{ order_number }}</strong>.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Devolução:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Motivo:</strong> {{ return_reason }}<br/>
              <strong>Itens:</strong> {{ items_count }} item(s)<br/>
              <strong>Status:</strong> {{ return_status }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que acontece em seguida?
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Nossa equipe revisará sua solicitação de devolução em 24-48 horas<br/>
          2. Uma vez aprovada, enviaremos um rótulo de envio de devolução por e-mail<br/>
          3. Empacote os itens com segurança e anexe o rótulo de devolução<br/>
          4. Entregue o pacote na localização de envio mais próxima de você<br/>
          5. Seu reembolso será processado assim que recebermos e inspecionarmos os itens
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se tiver alguma dúvida, não hesite em nos contatar.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
SOLICITAÇÃO DE DEVOLUÇÃO RECEBIDA
Pedido #{{ order_number }}

Olá {{ customer_name }},

Nós recebemos sua solicitação de devolução para o pedido #{{ order_number }}.

DETALHES DA DEVOLUÇÃO:
- Motivo: {{ return_reason }}
- Itens: {{ items_count }} item(s)
- Status: {{ return_status }}

O QUE ACONTECE EM SEGUIDA?
1. Nossa equipe revisará sua solicitação de devolução em 24-48 horas
2. Uma vez aprovada, enviaremos um rótulo de envio de devolução por e-mail
3. Empacote os itens com segurança e anexe o rótulo de devolução
4. Entregue o pacote na localização de envio mais próxima de você
5. Seu reembolso será processado assim que recebermos e inspecionarmos os itens

Se tiver alguma dúvida, não hesite em nos contatar.
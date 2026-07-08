---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Atualização da Solicitação de Devolução - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Atualização da Solicitação de Devolução
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Nós revisamos sua solicitação de devolução para o pedido <strong>#{{ order_number }}</strong> e, no momento, não conseguimos aprova-la.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Motivo:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se você tiver dúvidas sobre essa decisão ou acreditar que houve um erro, por favor, entre em contato com nossa equipe de suporte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Atualização da Solicitação de Devolução - Pedido #{{ order_number }}

Olá {{ customer_name }},

Nós revisamos sua solicitação de devolução para o pedido #{{ order_number }} e, no momento, não conseguimos aprova-la.

{% if rejection_reason %}Motivo: {{ rejection_reason }}{% endif %}

Se você tiver dúvidas sobre essa decisão ou acreditar que houve um erro, por favor, entre em contato com nossa equipe de suporte.
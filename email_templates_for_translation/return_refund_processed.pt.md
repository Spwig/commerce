---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Reembolso Processado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Reembolso Processado
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
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
          Seu retorno para o pedido <strong>#{{ order_number }}</strong> foi inspecionado e seu reembolso foi processado.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Detalhes do Reembolso
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Valor do Reembolso:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Taxa de Reembolso:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Nota:</strong> Pode levar de 5 a 10 dias úteis para o reembolso aparecer em sua conta, dependendo do seu provedor de pagamento.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Se tiver alguma dúvida sobre seu reembolso, entre em contato com nossa equipe de suporte.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Reembolso Processado - Pedido #{{ order_number }}

Olá {{ customer_name }},

Seu retorno para o pedido #{{ order_number }} foi inspecionado e seu reembolso foi processado.

Detalhes do Reembolso:
- Valor do Reembolso: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Taxa de Reembolso: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Nota: Pode levar de 5 a 10 dias úteis para o reembolso aparecer em sua conta, dependendo do seu provedor de pagamento.

Se tiver alguma dúvida sobre seu reembolso, entre em contato com nossa equipe de suporte.
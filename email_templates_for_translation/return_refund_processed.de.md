---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Rückerstattung verarbeitet - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Rückerstattung verarbeitet
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Bestellung #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre Rücksendung für die Bestellung <strong>#{{ order_number }}</strong> wurde geprüft und Ihre Rückerstattung wurde verarbeitet.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Rückerstattungsdetails
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Rückerstattungsbetrag:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Rückstellungsgebühr:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Hinweis:</strong> Es kann 5–10 Werktagen dauern, bis die Rückerstattung auf Ihrem Konto erscheint, abhängig von Ihrem Zahlungsdienstleister.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wenn Sie Fragen zu Ihrer Rückerstattung haben, wenden Sie sich bitte an unser Support-Team.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rückerstattung verarbeitet - Bestellung #{{ order_number }}

Hi {{ customer_name }},

Ihre Rücksendung für die Bestellung #{{ order_number }} wurde geprüft und Ihre Rückerstattung wurde verarbeitet.

Rückerstattungsdetails:
- Rückerstattungsbetrag: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Rückstellungsgebühr: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Hinweis: Es kann 5–10 Werktagen dauern, bis die Rückerstattung auf Ihrem Konto erscheint, abhängig von Ihrem Zahlungsdienstleister.

Wenn Sie Fragen zu Ihrer Rückerstattung haben, wenden Sie sich bitte an unser Support-Team.
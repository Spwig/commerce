---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Rücksendeantrag - Bestellung #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Rücksendeantrag aktualisiert
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          Wir haben Ihren Rücksendeantrag für die Bestellung <strong>#{{ order_number }}</strong> geprüft und können ihn derzeit leider nicht genehmigen.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Grund:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Wenn Sie Fragen zu dieser Entscheidung haben oder glauben, dass ein Fehler vorliegt, wenden Sie sich bitte an unser Support-Team.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Rücksendeantrag - Bestellung #{{ order_number }}

Hi {{ customer_name }},

Wir haben Ihren Rücksendeantrag für die Bestellung #{{ order_number }} geprüft und können ihn derzeit leider nicht genehmigen.

{% if rejection_reason %}Grund: {{ rejection_reason }}{% endif %}

Wenn Sie Fragen zu dieser Entscheidung haben oder glauben, dass ein Fehler vorliegt, wenden Sie sich bitte an unser Support-Team.
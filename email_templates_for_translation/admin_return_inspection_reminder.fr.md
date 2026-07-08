---
template_type: admin_return_inspection_reminder
category: Admin Notifications
---

# Email Template: admin_return_inspection_reminder

## Subject
Retour reçu - Inspection requise pour la commande #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Inspection du retour requise
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Un colis de retour a été reçu et nécessite une inspection.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Commande :</strong> #{{ order_number }}<br/>
              <strong>Reçu le :</strong> {{ received_at }}<br/>
              <strong>Articles à inspecter :</strong> {{ items_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if admin_url %}
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir le retour dans l'admin
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Inspection du retour requise

Un colis de retour a été reçu et nécessite une inspection.

Commande : #{{ order_number }}
Reçu le : {{ received_at }}
Articles à inspecter : {{ items_count }}

{% if admin_url %}Voir dans l'admin : {{ admin_url }}{% endif %}
---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
Votre commande n°{{ order_number }} a été annulée

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Commande annulée
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre commande <strong>#{{ order_number }}</strong> a été annulée.
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Raison :</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si un paiement a été effectué, un remboursement sera traité selon le mode de paiement original.
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Voir les détails de la commande
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Commande annulée

Bonjour {{ customer_name }},

Votre commande #{{ order_number }} a été annulée.

{% if cancellation_reason %}Raison : {{ cancellation_reason }}{% endif %}

Si un paiement a été effectué, un remboursement sera traité selon le mode de paiement original.

{% if order_url %}Voir les détails de la commande : {{ order_url }}{% endif %}

Questions concernant cette annulation ?
Email : {{ support_email }}
Téléphone : {{ support_phone }}
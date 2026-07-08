---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
Remboursement effectué - Commande #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Remboursement effectué
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Commande #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Votre retour pour la commande <strong>#{{ order_number }}</strong> a été examiné et votre remboursement a été traité.
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              Détails du remboursement
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Montant du remboursement :</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Frais de réapprovisionnement :</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Note :</strong> Il peut prendre 5 à 10 jours ouvrés pour que le remboursement apparaisse sur votre compte, selon votre fournisseur de paiement.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si vous avez des questions concernant votre remboursement, veuillez contacter notre équipe de support.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Remboursement effectué - Commande #{{ order_number }}

Bonjour {{ customer_name }},

Votre retour pour la commande #{{ order_number }} a été inspecté et votre remboursement a été traité.

Détails du remboursement:
- Montant du remboursement: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- Frais de réapprovisionnement: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

Note: Il peut prendre 5-10 jours ouvrés pour que le remboursement apparaisse sur votre compte, selon votre fournisseur de paiement.

Si vous avez des questions concernant votre remboursement, veuillez contacter notre équipe de support.
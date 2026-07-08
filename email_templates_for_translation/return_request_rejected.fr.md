---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
Mise à jour de la demande de retour - Commande n°{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          Mise à jour de la demande de retour
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
          Commande n°{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous avons examiné votre demande de retour pour la commande <strong>#{{ order_number }}</strong> et ne pouvons pas l'approuver pour le moment.
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Raison :</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Si vous avez des questions concernant cette décision ou si vous pensez qu'une erreur a été commise, veuillez contacter notre équipe de support.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Mise à jour de la demande de retour - Commande n°{{ order_number }}

Bonjour {{ customer_name }},

Nous avons examiné votre demande de retour pour la commande #{{ order_number }} et ne pouvons pas l'approuver pour le moment.

{% if rejection_reason %}Raison : {{ rejection_reason }}{% endif %}

Si vous avez des questions concernant cette décision ou si vous pensez qu'une erreur a été commise, veuillez contacter notre équipe de support.
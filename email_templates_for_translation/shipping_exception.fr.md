---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
Exception d'expédition - La commande #{{ order_number }} nécessite une attention particulière

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Exception d'expédition
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bonjour {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Nous vous écrivons pour vous informer d'une exception concernant votre colis. Nous travaillons à résoudre ce problème aussi rapidement que possible.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Détails de l'exception :
            </mj-text>
            <mj-text color="#92400e">
              <strong>Type d'exception :</strong> {{ exception_type }}<br/>
              <strong>Description :</strong> {{ exception_description }}<br/>
              <strong>Survenu le :</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Informations sur la commande :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Numéro de commande :</strong> {{ order_number }}<br/>
              <strong>Numéro de suivi :</strong> {{ tracking_number }}<br/>
              <strong>Transporteur :</strong> {{ carrier_name }}<br/>
              <strong>Emplacement actuel :</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Qu'advient-il ensuite ?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ Action requise : 
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Suivre votre commande
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Contacter le support
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ EXCEPTION D'EXPÉDITION

Bonjour {{ customer_name }},

Nous vous écrivons pour vous informer d'une exception concernant votre colis. Nous travaillons à résoudre ce problème aussi rapidement que possible.

DÉTAILS DE L'EXCEPTION :
- Type d'exception : {{ exception_type }}
- Description : {{ exception_description }}
- Survenu le : {{ exception_date }}

INFORMATIONS SUR LA COMMANDE :
- Numéro de commande : {{ order_number }}
- Numéro de suivi : {{ tracking_number }}
- Transporteur : {{ carrier_name }}
- Emplacement actuel : {{ current_location }}

QU'ADVIENT-IL ENSUITE ?
{{ resolution_steps }}

{% if action_required %}
⚠️ ACTION REQUISE : 
{{ action_required_description }}
{% endif %}

Suivre votre commande : {{ tracking_url }}
Contacter le support : {{ support_url }}
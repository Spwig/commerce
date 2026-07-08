---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Abonnement confirmé - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Abonnement confirmé !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Bienvenue sur Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Bonjour {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Merci d'avoir souscrit ! Votre abonnement <strong>{{ plan_name }}</strong> pour <strong>{{ store_name }}</strong> a été confirmé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Détails de l'abonnement
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan : {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervalle de facturation : {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Montant : {{ currency }}{{ amount }}{% if intro_period %} (tarif d'essai){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Votre tarif d'essai s'applique pendant {{ intro_period }}. Après cela, votre abonnement se renouvelle à {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Votre boutique est en cours de configuration et vous recevrez un autre e-mail lorsqu'elle sera prête.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Prochaine date de facturation : {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Abonnement confirmé !

Bonjour {{ name|default:'there' }},

Merci d'avoir souscrit ! Votre abonnement {{ plan_name }} pour {{ store_name }} a été confirmé.

Détails de l'abonnement:
- Plan : {{ plan_name }}
- Intervalle de facturation : {{ billing_interval }}
- Montant : {{ currency }}{{ amount }}{% if intro_period %} (tarif d'essai){% endif %}
{% if intro_period %}
C'est votre tarif d'essai pendant {{ intro_period }}. Après cela, votre abonnement se renouvelle à {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Votre boutique est en cours de configuration et vous recevrez un autre e-mail lorsqu'elle sera prête.

Prochaine date de facturation : {{ next_billing_date }}

Besoin d'aide ? Contactez {{ support_email }}
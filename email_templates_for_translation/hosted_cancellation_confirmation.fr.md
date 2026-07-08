---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Annulation confirmée - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Annulation confirmée
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          Votre abonnement <strong>{{ plan_name }}</strong> a été annulé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ce qui se passe maintenant
        </mj-text>
        <mj-text font-size="14px">
          Vous disposerez toujours d'un accès complet jusqu'à <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Après cela, vos données de magasin seront conservées pendant 30 jours jusqu'à <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Si vous souhaitez exporter vos données avant la fin de l'accès, vous pouvez le faire depuis votre tableau de bord. Changé d'avis ? Vous pouvez réactiver votre abonnement à tout moment.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Réactiver l'abonnement" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Annulation confirmée - {{ store_name }}

Bonjour {{ name|default:'there' }},

Votre abonnement {{ plan_name }} a été annulé.

Ce qui se passe maintenant:
- Vous disposerez toujours d'un accès complet jusqu'à {{ access_until_date }}.
- Après cela, vos données de magasin seront conservées pendant 30 jours jusqu'à {{ termination_date }}.

Si vous souhaitez exporter vos données avant la fin de l'accès, vous pouvez le faire depuis votre tableau de bord. Changé d'avis ? Vous pouvez réactiver votre abonnement à tout moment.

Réactiver l'abonnement: https://spwig.com/account

Besoin d'aide ? Contactez {{ support_email }}
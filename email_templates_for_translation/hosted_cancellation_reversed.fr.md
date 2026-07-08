---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
Annulation annulée - {{ store_name }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Annulation annulée
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
          Bonjour,
        </mj-text>
        <mj-text>
          Votre demande d'annulation pour <strong>{{ store_name }}</strong> a été annulée. Votre abonnement <strong>{{ plan_name }}</strong> continuera normalement — aucune action de votre part n'est requise.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Détails de l'abonnement
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan : {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Date de prochaine facturation : {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Votre boutique continue de fonctionner normalement. La facturation reprendra à la date indiquée ci-dessus.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Annulation annulée - {{ store_name }}

Bonjour,

Votre demande d'annulation pour {{ store_name }} a été annulée. Votre abonnement {{ plan_name }} continuera normalement — aucune action de votre part n'est requise.

Détails de l'abonnement:
- Plan: {{ plan_name }}
- Date de prochaine facturation: {{ next_billing_date }}

Votre boutique continue de fonctionner normalement. La facturation reprendra à la date indiquée ci-dessus.

{% if admin_url %}Aller à votre boutique: {{ admin_url }}

{% endif %}Besoin d'aide ? Contactez {{ support_email }}
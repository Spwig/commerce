---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Mise à jour de la facturation - {{ store_name }}

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
          Mise à jour de la facturation
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
          L'intervalle de facturation de votre plan <strong>{{ plan_name }}</strong> sur <strong>{{ store_name }}</strong> a été mis à jour.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Détails de la facturation
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervalle de facturation précédent: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nouvel intervalle de facturation: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Date de prochaine facturation: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Votre abonnement reste actif. Vous pouvez gérer vos préférences de facturation à tout moment depuis votre compte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Gérer l'abonnement" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Mise à jour de la facturation - {{ store_name }}

Bonjour,

L'intervalle de facturation de votre plan {{ plan_name }} sur {{ store_name }} a été mis à jour.

Détails de la facturation:
- Plan: {{ plan_name }}
- Intervalle de facturation précédent: {{ old_interval }}
- Nouvel intervalle de facturation: {{ new_interval }}
- Date de prochaine facturation: {{ next_billing_date }}

Votre abonnement reste actif. Vous pouvez gérer vos préférences de facturation à tout moment depuis votre compte.

Gérer l'abonnement: https://spwig.com/account

Besoin d'aide ? Contactez {{ support_email }}
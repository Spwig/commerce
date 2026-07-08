---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Important: Suppression des données dans 7 jours - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Avertissement de suppression des données
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
          Votre magasin <strong>{{ store_name }}</strong> et toutes les données associées seront définitivement supprimés le <strong>{{ termination_date }}</strong>. Cette action est irréversible.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ce que vous pouvez faire
        </mj-text>
        <mj-text font-size="14px">
          Si vous souhaitez conserver vos données, veuillez les exporter avant cette date ou réactiver votre abonnement pour empêcher la suppression.
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
Avertissement de suppression des données - {{ store_name }}

Bonjour {{ name|default:'there' }},

Votre magasin {{ store_name }} et toutes les données associées seront définitivement supprimés le {{ termination_date }}. Cette action est irréversible.

Ce que vous pouvez faire:
Si vous souhaitez conserver vos données, veuillez les exporter avant cette date ou réactiver votre abonnement pour empêcher la suppression.

Réactiver l'abonnement: https://spwig.com/account

Besoin d'aide ? Contactez {{ support_email }}
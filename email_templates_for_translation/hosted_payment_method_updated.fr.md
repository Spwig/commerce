---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
Méthode de paiement mise à jour - {{ store_name }}

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
          Méthode de paiement mise à jour
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
          Hi there,
        </mj-text>
        <mj-text>
          La méthode de paiement pour votre <strong>{{ plan_name }}</strong> plan sur <strong>{{ store_name }}</strong> a été mise à jour avec succès.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          N'avez-vous pas effectué ce changement ?
        </mj-text>
        <mj-text font-size="14px">
          Si vous n'avez pas mis à jour votre méthode de paiement, veuillez contacter immédiatement notre équipe de support afin que nous puissions sécuriser votre compte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Méthode de paiement mise à jour - {{ store_name }}

Hi there,

La méthode de paiement pour votre {{ plan_name }} plan sur {{ store_name }} a été mise à jour avec succès.

N'avez-vous pas effectué ce changement ?
Si vous n'avez pas mis à jour votre méthode de paiement, veuillez contacter immédiatement notre équipe de support afin que nous puissions sécuriser votre compte.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}
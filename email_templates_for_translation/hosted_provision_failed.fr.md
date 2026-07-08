---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
Action Required - Store Setup Issue for {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Store Setup Issue
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
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Nous avons rencontré un problème lors de la configuration de votre magasin <strong>{{ store_name }}</strong>. Notre équipe a été notifiée et enquête à ce sujet.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          What happened
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          What happens next?
        </mj-text>
        <mj-text font-size="14px">
          Notre équipe de support a été automatiquement notifiée à ce sujet. Vous n'avez pas besoin de prendre aucune action - nous vous contacterons dès que le problème sera résolu.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          Si vous avez des questions en attendant, n'hésitez pas à nous contacter.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Store Setup Issue - {{ store_name }}

Hi {{ name|default:'there' }},

Nous avons rencontré un problème lors de la configuration de votre magasin {{ store_name }}. Notre équipe a été notifiée et enquête à ce sujet.

What happened:
{{ provision_error }}

What happens next?
Notre équipe de support a été automatiquement notifiée à ce sujet. Vous n'avez pas besoin de prendre aucune action - nous vous contacterons dès que le problème sera résolu.

Si vous avez des questions en attendant, n'hésitez pas à nous contacter.

Need help? Contact {{ support_email }}
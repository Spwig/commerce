---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Avertissement de suspension - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Avertissement de suspension
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Action requise pour {{ store_name }}
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
          Votre paiement pour <strong>{{ plan_name }}</strong> est en retard. Si cela n'est pas résolu d'ici <strong>{{ grace_end_date }}</strong>, votre boutique sera placée en mode lecture seule.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Qu'est-ce que la suspension signifie ?
        </mj-text>
        <mj-text font-size="14px">
          Si votre boutique est suspendue, elle restera visible pour les visiteurs, mais vous ne pourrez pas apporter de modifications. Les nouvelles commandes seront suspendues jusqu'à ce que le solde impayé soit réglé.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Veuillez mettre à jour votre mode de paiement afin d'éviter toute interruption de votre boutique.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Mettre à jour le mode de paiement" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Avertissement de suspension - {{ store_name }}

Bonjour {{ name|default:'there' }},

Votre paiement pour {{ plan_name }} est en retard. Si cela n'est pas résolu d'ici {{ grace_end_date }}, votre boutique sera placée en mode lecture seule.

Qu'est-ce que la suspension signifie ?
Si votre boutique est suspendue, elle restera visible pour les visiteurs, mais vous ne pourrez pas apporter de modifications. Les nouvelles commandes seront suspendues jusqu'à ce que le solde impayé soit réglé.

Veuillez mettre à jour votre mode de paiement afin d'éviter toute interruption de votre boutique.

Mettre à jour le mode de paiement: https://spwig.com/account

Besoin d'aide ? Contactez {{ support_email }}
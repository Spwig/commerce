---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Bienvenue de retour ! {{ store_name }} est à nouveau active

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
          Bienvenue de retour !
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} est à nouveau active
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
          Grande nouvelle ! Votre <strong>{{ store_name }}</strong> a été réactivée. Votre abonnement <strong>{{ plan_name }}</strong> est désormais actif et votre boutique revient en ligne.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Détails de la réactivation
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan : {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Paiement effectué : {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Date de prochaine facturation : {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Votre boutique revient en ligne maintenant. Il peut prendre quelques minutes pour que tout soit pleinement restauré. Une fois en ligne, votre boutique sera accessible à {{ store_url }}.
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
Bienvenue de retour ! {{ store_name }} est à nouveau active

Bonjour,

Grande nouvelle ! Votre {{ store_name }} a été réactivée. Votre {{ plan_name }} subscription est désormais active et votre boutique revient en ligne.

Détails de la réactivation:
- Plan: {{ plan_name }}
- Paiement effectué: {{ currency }}{{ amount }}
- Date de prochaine facturation: {{ next_billing_date }}

Votre boutique revient en ligne maintenant. Il peut prendre quelques minutes pour que tout soit pleinement restauré. Une fois en ligne, votre boutique sera accessible à {{ store_url }}.

Aller à votre boutique: {{ admin_url }}

Besoin d'aide ? Contactez {{ support_email }}
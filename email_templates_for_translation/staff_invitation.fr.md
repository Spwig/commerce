---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Vous avez été invité(e) à rejoindre {{ store_name }}

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
          Invitation au personnel
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Vous avez été invité(e) à rejoindre {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Bonjour {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} vous a invité(e) à rejoindre <strong>{{ store_name }}</strong> en tant que membre du personnel. Vous pourrez aider à gérer le magasin depuis le tableau de bord administrateur.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accepter l'invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Cette invitation expire le {{ expires_at|date:"N j, Y" }}. Si vous n'attendiez pas cette invitation, vous pouvez ignorer ce courriel sans problème.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Vous avez été invité(e) à rejoindre {{ store_name }}

Bonjour {{ first_name }},

{{ invited_by }} vous a invité(e) à rejoindre {{ store_name }} en tant que membre du personnel. Vous pourrez aider à gérer le magasin depuis le tableau de bord administrateur.

Accepter votre invitation: {{ invitation_url }}

Cette invitation expire le {{ expires_at|date:"N j, Y" }}. Si vous n'attendiez pas cette invitation, vous pouvez ignorer ce courriel sans problème.

Besoin d'aide ? Contactez {{ support_email }}
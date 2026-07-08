---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Sei stato invitato a unirti a {{ store_name }}

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
          Invito allo staff
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Sei stato invitato a unirti a {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Ciao {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} ti ha invitato a unirti a <strong>{{ store_name }}</strong> come membro dello staff. Potrai aiutare a gestire il negozio dal pannello di amministrazione.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accetta l'invito" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Questo invito scadrà il {{ expires_at|date:"N j, Y" }}. Se non ti aspettavi questo invito, puoi tranquillamente ignorare questa email.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Sei stato invitato a unirti a {{ store_name }}

Ciao {{ first_name }},

{{ invited_by }} ti ha invitato a unirti a {{ store_name }} come membro dello staff. Potrai aiutare a gestire il negozio dal pannello di amministrazione.

Accetta l'invito: {{ invitation_url }}

Questo invito scadrà il {{ expires_at|date:"N j, Y" }}. Se non ti aspettavi questo invito, puoi tranquillamente ignorare questa email.

Hai bisogno di aiuto? Contatta {{ support_email }}
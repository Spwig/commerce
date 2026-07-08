---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
Has sido invitado a unirse a {{ store_name }}

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
          Invitación de personal
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Has sido invitado a unirse a {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} te ha invitado a unirte a <strong>{{ store_name }}</strong> como miembro del personal. Podrás ayudar a administrar la tienda desde el panel de administración.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Aceptar invitación" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Esta invitación expira el {{ expires_at|date:"N j, Y" }}. Si no esperabas esta invitación, puedes ignorar este correo con seguridad.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Has sido invitado a unirse a {{ store_name }}

Hola {{ first_name }},

{{ invited_by }} te ha invitado a unirte a {{ store_name }} como miembro del personal. Podrás ayudar a administrar la tienda desde el panel de administración.

Acepta tu invitación: {{ invitation_url }}

Esta invitación expira el {{ expires_at|date:"N j, Y" }}. Si no esperabas esta invitación, puedes ignorar este correo con seguridad.

¿Necesitas ayuda? Contacta a {{ support_email }}
---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Crea tu cuenta en {{ site_name }}

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
          ¡Te has invitado!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Crea tu cuenta en {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola {{ customer_name }},
        </mj-text>
        <mj-text>
          Nos dimos cuenta de que has estado comprando con nosotros como invitado. Crea una cuenta completa para desbloquear beneficios como el seguimiento de pedidos, un checkout más rápido y ofertas exclusivas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Tu historial de compras
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total de pedidos: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total gastado: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ¿Por qué crear una cuenta?
        </mj-text>
        <mj-text font-size="14px">
          - Rastrea tus pedidos y ve tu historial de pedidos
        </mj-text>
        <mj-text font-size="14px">
          - Pago más rápido con detalles guardados
        </mj-text>
        <mj-text font-size="14px">
          - Gestiona tus direcciones y preferencias
        </mj-text>
        <mj-text font-size="14px">
          - Accede a ofertas y promociones exclusivas
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Crea tu cuenta" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Este enlace te permitirá establecer una contraseña para tu cuenta. Tu historial de pedidos existente se mantendrá.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
¡Te has invitado a crear tu cuenta!

Hola {{ customer_name }},

Nos dimos cuenta de que has estado comprando con nosotros como invitado. Crea una cuenta completa para desbloquear beneficios como el seguimiento de pedidos, un checkout más rápido y ofertas exclusivas.

Tu historial de compras:
- Total de pedidos: {{ total_orders }}
- Total gastado: {{ total_spent }}

¿Por qué crear una cuenta?
- Rastrea tus pedidos y ve tu historial de pedidos
- Pago más rápido con detalles guardados
- Gestiona tus direcciones y preferencias
- Accede a ofertas y promociones exclusivas

Crea tu cuenta: {{ activation_url }}

Este enlace te permitirá establecer una contraseña para tu cuenta. Tu historial de pedidos existente se mantendrá.

¿Necesitas ayuda? Contacta a {{ support_email }}
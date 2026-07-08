---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Tienda Suspendida - {{ store_name }}

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
          Cuenta Suspendida
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
          Hola {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Tu tienda <strong>{{ store_name }}</strong> ha sido suspendida debido a un pago pendiente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ¿Qué Esto Significa?
        </mj-text>
        <mj-text font-size="14px">
          Tu tienda ahora está en modo de solo lectura — los clientes pueden navegar, pero los pedidos están deshabilitados. Tus datos están seguros y se conservarán durante 30 días.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Para restaurar el acceso completo, por favor actualiza tu método de pago y salda el monto pendiente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactiva Tu Tienda" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cuenta Suspendida - {{ store_name }}

Hola {{ name|default:'there' }},

Tu tienda {{ store_name }} ha sido suspendida debido a un pago pendiente.

¿Qué Esto Significa?:
Tu tienda ahora está en modo de solo lectura — los clientes pueden navegar, pero los pedidos están deshabilitados. Tus datos están seguros y se conservarán durante 30 días.

Para restaurar el acceso completo, por favor actualiza tu método de pago y salda el monto pendiente.

Reactiva Tu Tienda: https://spwig.com/account

¿Necesitas ayuda? Contacta a {{ support_email }}
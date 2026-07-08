---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Acción requerida - {{ store_name }}

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
          Advertencia de suspensión
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Acción requerida para {{ store_name }}
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
          Su pago por <strong>{{ plan_name }}</strong> está atrasado. Si no se resuelve para <strong>{{ grace_end_date }}</strong>, su tienda se colocará en modo de solo lectura.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ¿Qué significa la suspensión?
        </mj-text>
        <mj-text font-size="14px">
          Si su tienda se suspende, seguirá siendo visible para los visitantes, pero no podrá realizar cambios. Las nuevas órdenes se pausarán hasta que se resuelva el saldo pendiente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Por favor, actualice su método de pago para evitar cualquier interrupción en su tienda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Advertencia de suspensión - {{ store_name }}

Hola {{ name|default:'there' }},

Su pago por {{ plan_name }} está atrasado. Si no se resuelve para {{ grace_end_date }}, su tienda se colocará en modo de solo lectura.

¿Qué significa la suspensión?:
Si su tienda se suspende, seguirá siendo visible para los visitantes, pero no podrá realizar cambios. Las nuevas órdenes se pausarán hasta que se resuelva el saldo pendiente.

Por favor, actualice su método de pago para evitar cualquier interrupción en su tienda.

Actualizar método de pago: https://spwig.com/account

¿Necesita ayuda? Póngase en contacto con {{ support_email }}
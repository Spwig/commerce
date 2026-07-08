---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Cancelación confirmada - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Cancelación confirmada
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
          Tu suscripción a <strong>{{ plan_name }}</strong> ha sido cancelada.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ¿Qué sucede a continuación
        </mj-text>
        <mj-text font-size="14px">
          Continuarás teniendo acceso completo hasta <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Después de eso, tus datos de tienda se conservarán durante 30 días hasta <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Si deseas exportar tus datos antes de que termine el acceso, puedes hacerlo desde tu panel de administración. ¿Cambiaste de idea? Puedes reactivar tu suscripción en cualquier momento.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivar suscripción" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Cancelación confirmada - {{ store_name }}

Hola {{ name|default:'there' }},

Tu suscripción a {{ plan_name }} ha sido cancelada.

¿Qué sucede a continuación:
- Continuarás teniendo acceso completo hasta {{ access_until_date }}.
- Después de eso, tus datos de tienda se conservarán durante 30 días hasta {{ termination_date }}.

Si deseas exportar tus datos antes de que termine el acceso, puedes hacerlo desde tu panel de administración. ¿Cambiaste de idea? Puedes reactivar tu suscripción en cualquier momento.

Reactivar suscripción: https://spwig.com/account

¿Necesitas ayuda? Contacta a {{ support_email }}
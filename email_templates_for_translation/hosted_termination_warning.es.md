---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Importante: Eliminación de datos en 7 días - {{ store_name }}

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
          Advertencia de eliminación de datos
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
          Tu tienda <strong>{{ store_name }}</strong> y todos los datos asociados se eliminarán permanentemente el <strong>{{ termination_date }}</strong>. Esta acción no se puede deshacer.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Qué puedes hacer
        </mj-text>
        <mj-text font-size="14px">
          Si deseas conservar tus datos, por favor exporta los datos antes de esta fecha o reactiva tu suscripción para evitar la eliminación.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Advertencia de eliminación de datos - {{ store_name }}

Hola {{ name|default:'there' }},

Tu tienda {{ store_name }} y todos los datos asociados se eliminarán permanentemente el {{ termination_date }}. Esta acción no se puede deshacer.

Qué puedes hacer:
Si deseas conservar tus datos, por favor exporta los datos antes de esta fecha o reactiva tu suscripción para evitar la eliminación.

Reactivar suscripción: https://spwig.com/account

¿Necesitas ayuda? Contacta a {{ support_email }}
---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
Tienda Eliminada - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Tienda Eliminada
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
          Tu tienda <strong>{{ store_name }}</strong> ha sido eliminada permanentemente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Backup de Datos
        </mj-text>
        <mj-text font-size="14px">
          Un respaldo de tus datos estará disponible durante 90 días si lo solicitas. Contacta a <strong>support@spwig.com</strong> si necesitas un exportado de datos.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Gracias por ser un cliente de Spwig. Esperamos verte nuevamente en el futuro.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Tienda Eliminada - {{ store_name }}

Hola {{ name|default:'there' }},

Tu tienda {{ store_name }} ha sido permanentemente eliminada.

Backup de Datos:
Un respaldo de tus datos estará disponible durante 90 días si lo solicitas. Contacta a support@spwig.com si necesitas un exportado de datos.

Gracias por ser un cliente de Spwig. Esperamos verte nuevamente en el futuro.

¿Necesitas ayuda? Contacta a {{ support_email }}
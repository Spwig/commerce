---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Enlace de descarga caducado - Orden #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Enlace de descarga caducado
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola {{ customer_name }},
        </mj-text>
        <mj-text>
          Tu enlace de descarga para <strong>{{ product_name }}</strong> de la orden #{{ order_number }} ha caducado.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Los enlaces de descarga caducan {{ expiration_days }} días después de la compra por razones de seguridad.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          ¿Necesitas un nuevo enlace de descarga?
        </mj-text>
        <mj-text>
          Puedes solicitar un nuevo enlace de descarga iniciando sesión en tu cuenta o contactando a nuestro equipo de soporte.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Ir a Mi Cuenta
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ¿Tienes preguntas? Contacta a {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Enlace de descarga caducado

Hola {{ customer_name }},

Tu enlace de descarga para {{ product_name }} de la orden #{{ order_number }} ha caducado.

Los enlaces de descarga caducan {{ expiration_days }} días después de la compra por razones de seguridad.

¿Necesitas un nuevo enlace de descarga?
You can request a new download link by logging into your account or contacting our support team.

Ir a Mi Cuenta: {{ account_url }}

¿Tienes preguntas? Contacta a {{ support_email }}
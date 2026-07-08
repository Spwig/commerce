---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Tu producto digital está listo - Pedido #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Tu producto digital está listo!
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
          Gracias por tu compra. Tu producto digital ya está listo para descargar.
        </mj-text>
        <mj-text font-weight="bold">
          Pedido #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Versión: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tamaño del archivo: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Descargar ahora
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Información importante:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Puedes descargar este producto {{ download_limit }} vez/veces
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • El enlace de descarga expira en {{ expiration_days }} días
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Guarda este correo electrónico para futura referencia
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ¿Necesitas ayuda? Contacta a nuestro equipo de soporte en {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tu producto digital está listo!

Hola {{ customer_name }},

Gracias por tu compra. Tu producto digital ya está listo para descargar.

Pedido #{{ order_number }}

Producto: {{ product_name }}
Versión: {{ product_version }}
Tamaño del archivo: {{ file_size }}

Descarga tu producto aquí:
{{ download_url }}

Información importante:
{% if download_limit %}• Puedes descargar este producto {{ download_limit }} vez/veces
{% endif %}{% if expiration_days %}• El enlace de descarga expira en {{ expiration_days }} días
{% endif %}• Guarda este correo electrónico para futura referencia

¿Necesitas ayuda? Contacta a nuestro equipo de soporte en {{ support_email }}
---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Tu clave de licencia - Pedido #{{ order_number }}

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
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Tu clave de licencia está lista
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
          Gracias por tu compra de {{ product_name }}! Aquí tienes tu clave de licencia para activar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          TU CLAVE DE LICENCIA
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Haz clic para copiar o anota cuidadosamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Detalles de la licencia:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Producto: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Versión: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Tipo de licencia: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Máximo de activaciones: {{ max_activations }} dispositivo(s)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Válida: Licencia de por vida
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Válida hasta: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Cómo activar:
        </mj-text>
        <mj-text font-size="14px">
          1. Descarga e instala el software
        </mj-text>
        <mj-text font-size="14px">
          2. Abre la aplicación
        </mj-text>
        <mj-text font-size="14px">
          3. Ingresa tu clave de licencia cuando se te pida
        </mj-text>
        <mj-text font-size="14px">
          4. Haz clic en "Activar" para completar el proceso
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Descargar Software
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Guarda este correo electrónico - necesitarás la clave de licencia para reinstalación
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • No compartas tu clave de licencia con otras personas
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Puedes desactivar dispositivos desde tu panel de control de cuenta
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ¿Necesitas ayuda con la activación? Contacta a {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Tu clave de licencia está lista

Hola {{ customer_name }},

Gracias por tu compra de {{ product_name }}! Aquí tienes tu clave de licencia para activar.

TU CLAVE DE LICENCIA:
{{ license_key }}

Detalles de la licencia:
• Producto: {{ product_name }}
• Versión: {{ product_version }}
• Tipo de licencia: {{ license_type }}
• Máximo de activaciones: {{ max_activations }} dispositivo(s)
{% if is_lifetime %}• Válida: Licencia de por vida{% else %}• Válida hasta: {{ expiration_date }}{% endif %}

Cómo activar:
1. Descarga e instala el software
2. Abre la aplicación
3. Ingresa tu clave de licencia cuando se te pida
4. Haz clic en "Activar" para completar el proceso

{% if download_url %}Descargar Software: {{ download_url }}

{% endif %}IMPORTANTE:
• Guarda este correo electrónico - necesitarás la clave de licencia para reinstalación
• No compartas tu clave de licencia con otras personas
• Puedes desactivar dispositivos desde tu panel de control de cuenta

¿Necesitas ayuda con la activación? Contacta a {{ support_email }}
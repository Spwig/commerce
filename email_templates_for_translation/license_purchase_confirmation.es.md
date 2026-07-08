---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Su licencia de Spwig - Pedido #{{ order_number }}

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
          ¡Gracias por su compra!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Pedido #{{ order_number }}
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
          Su compra de <strong>{{ product_name }}</strong> está completa. A continuación encontrará su clave de licencia y token de configuración para comenzar.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Resumen del Pedido
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Producto: {{ product_name }}{% if includes_pos %} (incluye POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Monto: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Número de Pedido: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          SU CLAVE DE LICENCIA
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Guarde esta clave - la necesitará para la reinstalación
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          SU TOKEN DE CONFIGURACIÓN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Use este token durante la instalación para activar su tienda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Comenzando
        </mj-text>
        <mj-text font-size="14px">
          1. Siga nuestra guía de configuración para instalar Spwig en su servidor
        </mj-text>
        <mj-text font-size="14px">
          2. Ingrese su token de configuración cuando se le solicite durante la instalación
        </mj-text>
        <mj-text font-size="14px">
          3. Su tienda se activará automáticamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Ver Guía de Configuración" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Cree su cuenta
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Establezca una contraseña para gestionar sus licencias, acceder a descargas y recibir actualizaciones.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Cree su cuenta" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Importante:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Guarde este correo electrónico - contiene su clave de licencia y token de configuración para futura referencia. No comparta estas credenciales con otras personas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
¡Gracias por su compra!

Pedido #{{ order_number }}

Hola {{ customer_name }},

Su compra de {{ product_name }} está completa. A continuación encontrará su clave de licencia y token de configuración para comenzar.

Resumen del Pedido:
- Producto: {{ product_name }}{% if includes_pos %} (incluye POS){% endif %}
- Monto: {{ price }}
- Número de Pedido: {{ order_number }}

SU CLAVE DE LICENCIA:
{{ license_key }}
Guarde esta clave - la necesitará para la reinstalación.

SU TOKEN DE CONFIGURACIÓN:
{{ setup_token }}
Use este token durante la instalación para activar su tienda.

Comenzando:
1. Siga nuestra guía de configuración para instalar Spwig en su servidor
2. Ingrese su token de configuración cuando se le solicite durante la instalación
3. Su tienda se activará automáticamente

Ver Guía de Configuración: {{ setup_url }}
{% if activation_url %}
Cree su cuenta:
Establezca una contraseña para gestionar sus licencias, acceder a descargas y recibir actualizaciones.
{{ activation_url }}
{% endif %}
IMPORTANTE:
Guarde este correo electrónico - contiene su clave de licencia y token de configuración para futura referencia. No comparta estas credenciales con otras personas.

¿Necesita ayuda? Póngase en contacto con {{ support_email }}
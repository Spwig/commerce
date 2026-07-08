---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Bienvenido a Spwig - Tu prueba gratuita de {{ trial_days }} días

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Bienvenido a Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tu prueba gratuita de {{ trial_days }} días está lista
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
          Gracias por probar <strong>{{ product_name }}</strong>! Tu prueba ha sido activada y tienes <strong>{{ trial_days }} días</strong> para explorar todo lo que ofrece Spwig{% if includes_pos %}, incluyendo nuestro sistema de Punto de Venta{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          TU TOKEN DE CONFIGURACIÓN
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Usa este token durante la instalación para activar tu tienda de prueba
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
          1. Sigue nuestra guía de configuración para instalar Spwig en tu servidor
        </mj-text>
        <mj-text font-size="14px">
          2. Ingresa tu token de configuración cuando se te pida durante la instalación
        </mj-text>
        <mj-text font-size="14px">
          3. Comienza a construir tu tienda en línea!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Ver Guía de Configuración" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Qué incluye tu prueba
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Acceso completo a todas las funciones principales durante {{ trial_days }} días
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Catálogo de productos, pedidos y gestión de clientes
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Personalización de temas y constructor de páginas
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Integraciones con proveedores de pago y envío
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sistema de Punto de Venta (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tu prueba expirará en {{ trial_days }} días. Cuando estés listo, actualiza a una licencia completa para continuar operando tu tienda sin pérdida de datos.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Bienvenido a Spwig!
Tu prueba gratuita de {{ trial_days }} días está lista.

Hola {{ customer_name }},

Gracias por probar {{ product_name }}! Tu prueba ha sido activada y tienes {{ trial_days }} días para explorar todo lo que ofrece Spwig{% if includes_pos %}, incluyendo nuestro sistema de Punto de Venta{% endif %}.

TU TOKEN DE CONFIGURACIÓN:
{{ setup_token }}
Usa este token durante la instalación para activar tu tienda de prueba.

Comenzando:
1. Sigue nuestra guía de configuración para instalar Spwig en tu servidor
2. Ingresa tu token de configuración cuando se te pida durante la instalación
3. Comienza a construir tu tienda en línea!

Ver Guía de Configuración: {{ setup_url }}

Qué incluye tu prueba:
- Acceso completo a todas las funciones principales durante {{ trial_days }} días
- Catálogo de productos, pedidos y gestión de clientes
- Personalización de temas y constructor de páginas
- Integraciones con proveedores de pago y envío
{% if includes_pos %}- Sistema de Punto de Venta (POS){% endif %}

Tu prueba expirará en {{ trial_days }} días. Cuando estés listo, actualiza a una licencia completa para continuar operando tu tienda sin pérdida de datos.

¿Necesitas ayuda? Contacta a {{ support_email }}
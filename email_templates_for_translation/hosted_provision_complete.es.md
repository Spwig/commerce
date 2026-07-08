---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Tu tienda está lista - {{ store_name }}

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
          Tu tienda está en línea!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} está lista para ti
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
          ¡Buena noticia! Tu tienda de Spwig <strong>{{ store_name }}</strong> ha sido provisionada y ahora está en línea. Puedes comenzar a configurar tus productos, marca y métodos de pago de inmediato.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalles de tu tienda
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL de la tienda: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Panel de administración: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Región: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Inicio rápido
        </mj-text>
        <mj-text font-size="14px">
          1. Inicia sesión en tu panel de administración usando el correo electrónico y la contraseña que estableciste durante el pago
        </mj-text>
        <mj-text font-size="14px">
          2. Añade tu logotipo y marca en Diseño > Configuración del tema
        </mj-text>
        <mj-text font-size="14px">
          3. Añade tus primeros productos en Catálogo > Productos
        </mj-text>
        <mj-text font-size="14px">
          4. Configura un proveedor de pago en Configuración > Proveedores de pago
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Ir al Panel de Administración" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Tu tienda está en línea!

{{ store_name }} está lista para ti.

Hola {{ name|default:'there' }},

¡Buena noticia! Tu tienda de Spwig {{ store_name }} ha sido provisionada y ahora está en línea. Puedes comenzar a configurar tus productos, marca y métodos de pago de inmediato.

Detalles de tu tienda:
- URL de la tienda: {{ store_url }}
- Panel de administración: {{ admin_url }}
- Región: {{ region }}

Inicio rápido:
1. Inicia sesión en tu panel de administración usando el correo electrónico y la contraseña que estableciste durante el pago
2. Añade tu logotipo y marca en Diseño > Configuración del tema
3. Añade tus primeros productos en Catálogo > Productos
4. Configura un proveedor de pago en Configuración > Proveedores de pago

Ir al Panel de Administración: {{ admin_url }}

¿Necesitas ayuda? Contacta a {{ support_email }}
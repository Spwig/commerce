---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
Consejos para sacar el máximo provecho de {{ store_name }}

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
          Consejos para empezar
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Saque el máximo provecho de su tienda Spwig
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
          Ahora que <strong>{{ store_name }}</strong> está en funcionamiento, aquí tiene algunos consejos para ayudarle a sacar el máximo provecho de su tienda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Personalice su aspecto
        </mj-text>
        <mj-text font-size="14px">
          Visite <strong>Design > Theme Settings</strong> para elegir un tema, subir su logotipo y establecer los colores de su marca. Su tienda se actualiza de inmediato, por lo que puede previsualizar los cambios en tiempo real.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Añada sus productos
        </mj-text>
        <mj-text font-size="14px">
          Vaya a <strong>Catalog > Products</strong> para comenzar a añadir sus artículos. Puede crear variantes de productos (tamaño, color), establecer precios, gestionar el inventario y subir imágenes de alta calidad.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure los pagos
        </mj-text>
        <mj-text font-size="14px">
          Vaya a <strong>Settings > Payment Providers</strong> para conectar Stripe, PayPal u otro método de pago. Puede habilitar múltiples proveedores para que sus clientes paguen de la forma que prefieran.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Configure el envío
        </mj-text>
        <mj-text font-size="14px">
          Bajo <strong>Settings > Shipping</strong>, configure sus zonas de envío y tarifas. Puede crear reglas de envío de tarifa plana, basadas en peso o gratuitas para diferentes regiones.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          Mejore su SEO
        </mj-text>
        <mj-text font-size="14px">
          Spwig genera automáticamente mapas de sitio y etiquetas meta. Visite <strong>Settings > SEO</strong> para personalizar los títulos de sus páginas, descripciones e imágenes para compartir en redes sociales, lo que ayudará a que los clientes encuentren su tienda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Consejos para empezar - {{ store_name }}

Hola {{ name|default:'there' }},

Ahora que {{ store_name }} está en funcionamiento, aquí tiene algunos consejos para ayudarle a sacar el máximo provecho de su tienda.

1. Personalice su aspecto
Visite Design > Theme Settings para elegir un tema, subir su logotipo y establecer los colores de su marca.

2. Añada sus productos
Vaya a Catalog > Products para comenzar a añadir sus artículos con variantes, precios e imágenes.

3. Configure los pagos
Vaya a Settings > Payment Providers para conectar Stripe, PayPal u otro método de pago.

4. Configure el envío
Bajo Settings > Shipping, configure sus zonas de envío y tarifas para diferentes regiones.

5. Mejore su SEO
Visite Settings > SEO para personalizar los títulos de sus páginas, descripciones e imágenes para compartir en redes sociales.

Vaya al Panel de Administración: {{ admin_url }}

¿Necesita ayuda? Póngase en contacto con {{ support_email }}
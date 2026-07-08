---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
¡Bienvenido de nuevo! {{ store_name }} está activo nuevamente

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          ¡Bienvenido de nuevo!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} está activo nuevamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hola,
        </mj-text>
        <mj-text>
          ¡Buena noticia! Tu tienda <strong>{{ store_name }}</strong> ha sido reactivada. Tu suscripción a <strong>{{ plan_name }}</strong> ahora está activa y tu tienda está volviendo en línea.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalles de reactivación
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pago procesado: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Próxima fecha de facturación: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Tu tienda está volviendo en línea ahora. Puede tomar unos minutos para que todo se restaure completamente. Una vez en línea, tu tienda estará accesible en {{ store_url }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
¡Bienvenido de nuevo! {{ store_name }} está activo nuevamente

Hola,

¡Buena noticia! Tu tienda {{ store_name }} ha sido reactivada. Tu suscripción a {{ plan_name }} ahora está activa y tu tienda está volviendo en línea.

Detalles de reactivación:
- Plan: {{ plan_name }}
- Pago procesado: {{ currency }}{{ amount }}
- Próxima fecha de facturación: {{ next_billing_date }}

Tu tienda está volviendo en línea ahora. Puede tomar unos minutos para que todo se restaure completamente. Una vez en línea, tu tienda estará accesible en {{ store_url }}.

Ir a tu tienda: {{ admin_url }}

¿Necesitas ayuda? Contacta a {{ support_email }}
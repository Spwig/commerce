---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
Reversión de cancelación - {{ store_name }}

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
          Reversión de cancelación
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
          Hola,
        </mj-text>
        <mj-text>
          Su solicitud de cancelación para <strong>{{ store_name }}</strong> ha sido revertida. Su suscripción a <strong>{{ plan_name }}</strong> continuará normalmente — no se requiere ninguna acción por su parte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalles de la suscripción
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Fecha de facturación siguiente: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Su tienda continúa operando normalmente. La facturación reanudará en la fecha mostrada anteriormente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Reversión de cancelación - {{ store_name }}

Hola,

Su solicitud de cancelación para {{ store_name }} ha sido revertida. Su {{ plan_name }} suscripción continuará normalmente — no se requiere ninguna acción por su parte.

Detalles de la suscripción:
- Plan: {{ plan_name }}
- Fecha de facturación siguiente: {{ next_billing_date }}

Su tienda continúa operando normalmente. La facturación reanudará en la fecha mostrada anteriormente.

{% if admin_url %}Ir a su tienda: {{ admin_url }}

{% endif %}¿Necesita ayuda? Póngase en contacto con {{ support_email }}
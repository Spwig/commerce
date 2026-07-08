---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ ¡Tu plan de suscripción ha sido actualizado!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ ¡Plan Actualizado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bienvenido a {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tu plan de suscripción ha sido actualizado con éxito. Ahora tienes acceso a todos los beneficios de {{ new_plan_name }}!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles del Cambio de Plan:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Plan:</strong> {{ old_plan_name }}<br/>
              <strong>New Plan:</strong> {{ new_plan_name }}<br/>
              <strong>Upgraded On:</strong> {{ upgrade_date }}<br/>
              <strong>Effective Immediately</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ¿Qué hay de nuevo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Información de Facturación:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>New Price:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Next Billing Date:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Prorated Charge Today:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Hoy se te cobró {{ prorated_charge }} por el resto de tu período de facturación actual.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver mi suscripción
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ¿Tienes preguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contáctanos</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ¡PLAN ACTUALIZADO!

Bienvenido a {{ new_plan_name }}

Hola {{ customer_name }},

Tu plan de suscripción ha sido actualizado con éxito. Ahora tienes acceso a todos los beneficios de {{ new_plan_name }}!

DETALLES DEL CAMBIO DE PLAN:
- Plan anterior: {{ old_plan_name }}
- Nuevo plan: {{ new_plan_name }}
- Actualizado el: {{ upgrade_date }}
- Aplicable de inmediato

¿QUÉ HAY DE NUEVO:
{{ new_features }}

INFORMACIÓN DE FACTURACIÓN:
- Nuevo precio: {{ new_price }} / {{ billing_period }}
- Próxima fecha de facturación: {{ next_billing_date }}
{% if prorated_charge %}- Cargo proporcional hoy: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Hoy se te cobró {{ prorated_charge }} por el resto de tu período de facturación actual.
{% endif %}

Ver mi suscripción: {{ account_url }}
¿Tienes preguntas? Contactar soporte: {{ support_url }}
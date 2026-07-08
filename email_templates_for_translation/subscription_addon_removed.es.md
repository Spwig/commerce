---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
Se ha eliminado {{ addon_name }} de su suscripción

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Add-on Removed
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on Removed
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ addon_name }} se ha eliminado de su suscripción {{ plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Removal Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Add-on:</strong> {{ addon_name }}<br/>
              <strong>Subscription:</strong> {{ plan_name }}<br/>
              <strong>Removed On:</strong> {{ removed_date }}<br/>
              <strong>Effective:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if access_until %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Acceso hasta {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Continuarás teniendo acceso a {{ addon_name }} hasta el final de tu período de facturación actual.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Información de Facturación:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Previous Total:</strong> {{ old_total }} / {{ billing_period }}<br/>
              <strong>Add-on Price:</strong> -{{ addon_price }} / {{ billing_period }}<br/>
              <strong>New Total:</strong> {{ new_total }} / {{ billing_period }}<br/>
              <strong>Effective Date:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Se ha aplicado un crédito de {{ credit_amount }} a su cuenta por la parte no utilizada de este add-on.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Información Importante:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ data_retention_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ¿Necesita volver a incluirlo?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Puede agregar {{ addon_name }} de vuelta a su suscripción en cualquier momento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Explorar Add-ons
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver mi suscripción
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ADD-ON REMOVED

Add-on Removed

Hola {{ customer_name }},

{{ addon_name }} se ha eliminado de su suscripción {{ plan_name }}.

REMOVAL DETAILS:
- Add-on: {{ addon_name }}
- Subscription: {{ plan_name }}
- Removed On: {{ removed_date }}
- Effective: {{ effective_date }}

{% if access_until %}
ACCESO HASTA {{ access_until }}:
Continuarás teniendo acceso a {{ addon_name }} hasta el final de tu período de facturación actual.
{% endif %}

BILLING INFORMATION:
- Previous Total: {{ old_total }} / {{ billing_period }}
- Add-on Price: -{{ addon_price }} / {{ billing_period }}
- New Total: {{ new_total }} / {{ billing_period }}
- Effective Date: {{ effective_date }}

{% if credit_applied %}
💰 Se ha aplicado un crédito de {{ credit_amount }} a su cuenta por la parte no utilizada de este add-on.
{% endif %}

{% if data_retention_info %}
INFORMACIÓN IMPORTANTE:
{{ data_retention_info }}
{% endif %}

¿NECESITA VOLVER A INCLUIRLO?
Puede agregar {{ addon_name }} de vuelta a su suscripción en cualquier momento.

Explorar add-ons: {{ addons_url }}
Ver mi suscripción: {{ account_url }}
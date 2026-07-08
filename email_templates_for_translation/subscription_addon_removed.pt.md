---
template_type: subscription_addon_removed
category: Subscriptions
---

# Email Template: subscription_addon_removed

## Subject
O {{ addon_name }} foi removido da sua assinatura

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Add-on Removido
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Add-on Removido
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          O {{ addon_name }} foi removido da sua assinatura {{ plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Remoção:
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
              Acesso Até {{ access_until }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Você continuará a ter acesso ao {{ addon_name }} até o final do seu período de faturamento atual.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informações de Cobrança:
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
              💰 Um crédito de {{ credit_amount }} foi aplicado à sua conta pela parte não utilizada desse add-on.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if data_retention_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informação Importante:
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
          Precisa Voltar?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Você pode adicionar o {{ addon_name }} de volta à sua assinatura a qualquer momento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ addons_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Navegar por Add-ons
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ account_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Minha Assinatura
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ADD-ON REMOVIDO

Add-on Removido

Olá {{ customer_name }},

O {{ addon_name }} foi removido da sua assinatura {{ plan_name }}.

DETALHES DA REMOÇÃO:
- Add-on: {{ addon_name }}
- Subscription: {{ plan_name }}
- Removed On: {{ removed_date }}
- Effective: {{ effective_date }}

{% if access_until %}
ACESSO ATÉ {{ access_until }}:
Você continuará a ter acesso ao {{ addon_name }} até o final do seu período de faturamento atual.
{% endif %}

INFORMAÇÕES DE COBRANÇA:
- Previous Total: {{ old_total }} / {{ billing_period }}
- Add-on Price: -{{ addon_price }} / {{ billing_period }}
- New Total: {{ new_total }} / {{ billing_period }}
- Effective Date: {{ effective_date }}

{% if credit_applied %}
💰 Um crédito de {{ credit_amount }} foi aplicado à sua conta pela parte não utilizada desse add-on.
{% endif %}

{% if data_retention_info %}
INFORMAÇÃO IMPORTANTE:
{{ data_retention_info }}
{% endif %}

PRECISA VOLTA?
Você pode adicionar {{ addon_name }} de volta à sua assinatura a qualquer momento.

Browse add-ons: {{ addons_url }}
View my subscription: {{ account_url }}
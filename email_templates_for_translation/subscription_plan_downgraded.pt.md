---
template_type: subscription_plan_downgraded
category: Subscriptions
---

# Email Template: subscription_plan_downgraded

## Subject
Seu plano de assinatura foi alterado para {{ new_plan_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          Plano Alterado
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Plano de Assinatura Atualizado
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu plano de assinatura foi alterado para {{ new_plan_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalhes da Alteração do Plano:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Plano Anterior:</strong> {{ old_plan_name }}<br/>
              <strong>Novo Plano:</strong> {{ new_plan_name }}<br/>
              <strong>Alterado em:</strong> {{ downgrade_date }}<br/>
              <strong>Válido a partir de:</strong> {{ effective_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que Mudou:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ plan_changes }}
        </mj-text>

        {% if features_lost %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Recursos Não Disponíveis Mais:
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ features_lost }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Informações de Cobrança:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Novo Preço:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Data de Vigência:</strong> {{ effective_date }}<br/>
              <strong>Data de Cobrança Próxima:</strong> {{ next_billing_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if credit_applied %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              💰 Um crédito de {{ credit_amount }} foi aplicado à sua conta pela parte não utilizada do seu plano anterior.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Mudou de Ideia?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color_secondary|default:'#6b7280' }}" align="center">
          Você pode atualizar de volta para {{ old_plan_name }} a qualquer momento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ upgrade_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Atualizar Plano
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
PLANO ALTERADO

Plano de Assinatura Atualizado

Olá {{ customer_name }},

Seu plano de assinatura foi alterado para {{ new_plan_name }}.

DETALHES DA ALTERAÇÃO DO PLANO:
- Plano Anterior: {{ old_plan_name }}
- Novo Plano: {{ new_plan_name }}
- Alterado em: {{ downgrade_date }}
- Válido a partir de: {{ effective_date }}

O QUE MUDOU:
{{ plan_changes }}

{% if features_lost %}
RECURSOS NÃO MAIS DISPONÍVEIS:
{{ features_lost }}
{% endif %}

INFORMAÇÕES DE COBRANÇA:
- Novo Preço: {{ new_price }} / {{ billing_period }}
- Data de Vigência: {{ effective_date }}
- Data de Cobrança Próxima: {{ next_billing_date }}

{% if credit_applied %}
💰 Um crédito de {{ credit_amount }} foi aplicado à sua conta pela parte não utilizada do seu plano anterior.
{% endif %}

MUDOU DE IDEIA?
Você pode atualizar de volta para {{ old_plan_name }} a qualquer momento.

Upgrade plan: {{ upgrade_url }}
View my subscription: {{ account_url }}
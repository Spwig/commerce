---
template_type: subscription_plan_upgraded
category: Subscriptions
---

# Email Template: subscription_plan_upgraded

## Subject
✓ Seu plano foi atualizado!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Plano Atualizado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bem-vindo ao {{ new_plan_name }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Seu plano de assinatura foi atualizado com sucesso. Você agora tem acesso a todos os benefícios do {{ new_plan_name }}!
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
              <strong>Atualizado em:</strong> {{ upgrade_date }}<br/>
              <strong>Aplicado imediatamente</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que é novo:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ new_features }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Informações de Cobrança:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Novo Preço:</strong> {{ new_price }} / {{ billing_period }}<br/>
              <strong>Data da Próxima Cobrança:</strong> {{ next_billing_date }}<br/>
              {% if prorated_charge %}<strong>Cobrança Proporcional Hoje:</strong> {{ prorated_charge }}{% endif %}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if prorated_charge %}
        <mj-spacer height="20px" />
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Você foi cobrado {{ prorated_charge }} hoje pelo restante do seu período de cobrança atual.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver Minha Assinatura
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Perguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Entrar em contato com o suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ PLANO ATUALIZADO!

Bem-vindo ao {{ new_plan_name }}

Olá {{ customer_name }},

Seu plano de assinatura foi atualizado com sucesso. Você agora tem acesso a todos os benefícios do {{ new_plan_name }}!

DETALHES DA ALTERAÇÃO DO PLANO:
- Plano Anterior: {{ old_plan_name }}
- Novo Plano: {{ new_plan_name }}
- Atualizado em: {{ upgrade_date }}
- Aplicado imediatamente

O QUE É NOVO:
{{ new_features }}

INFORMAÇÕES DE COBRANÇA:
- Novo Preço: {{ new_price }} / {{ billing_period }}
- Data da Próxima Cobrança: {{ next_billing_date }}
{% if prorated_charge %}- Cobrança Proporcional Hoje: {{ prorated_charge }}{% endif %}

{% if prorated_charge %}
💡 Você foi cobrado {{ prorated_charge }} hoje pelo restante do seu período de cobrança atual.
{% endif %}

Ver minha assinatura: {{ account_url }}
Perguntas? Entrar em contato com o suporte: {{ support_url }}
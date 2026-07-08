---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Assinatura Confirmada - {{ store_name }}

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
          Assinatura Confirmada!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Bem-vindo ao Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Obrigado por se inscrever! Sua assinatura <strong>{{ plan_name }}</strong> para <strong>{{ store_name }}</strong> foi confirmada.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalhes da Assinatura
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Intervalo de Cobrança: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Valor: {{ currency }}{{ amount }}{% if intro_period %} (taxa introdutória){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Sua taxa introdutória se aplica por {{ intro_period }}. Após esse período, sua assinatura renova por {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Sua loja está sendo configurada agora e você receberá outro e-mail quando estiver pronta.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Próxima data de cobrança: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Assinatura Confirmada!

Olá {{ name|default:'there' }},

Obrigado por se inscrever! Sua assinatura {{ plan_name }} para {{ store_name }} foi confirmada.

Detalhes da Assinatura:
- Plano: {{ plan_name }}
- Intervalo de Cobrança: {{ billing_interval }}
- Valor: {{ currency }}{{ amount }}{% if intro_period %} (taxa introdutória){% endif %}
{% if intro_period %}
Esta é sua taxa introdutória por {{ intro_period }}. Após esse período, sua assinatura renova por {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Sua loja está sendo configurada agora e você receberá outro e-mail quando estiver pronta.

Próxima data de cobrança: {{ next_billing_date }}

Precisa de ajuda? Entre em contato com {{ support_email }}
---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Bem-vindo de volta! {{ store_name }} está ativo novamente

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
          Bem-vindo de volta!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} está ativo novamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá,
        </mj-text>
        <mj-text>
          Boas notícias! Sua loja <strong>{{ store_name }}</strong> foi reativada. Sua assinatura <strong>{{ plan_name }}</strong> está agora ativa e sua loja está voltando online.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detalhes da reativação
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plano: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Pagamento processado: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Próxima data de cobrança: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Sua loja está voltando online agora. Pode levar alguns minutos para tudo estar totalmente restaurado. Uma vez online, sua loja estará acessível em {{ store_url }}.
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
Bem-vindo de volta! {{ store_name }} está ativo novamente

Olá,

Boas notícias! Sua loja {{ store_name }} foi reativada. Sua assinatura {{ plan_name }} está agora ativa e sua loja está voltando online.

Detalhes da reativação:
- Plano: {{ plan_name }}
- Pagamento processado: {{ currency }}{{ amount }}
- Próxima data de cobrança: {{ next_billing_date }}

Sua loja está voltando online agora. Pode levar alguns minutos para tudo estar totalmente restaurado. Uma vez online, sua loja estará acessível em {{ store_url }}.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}
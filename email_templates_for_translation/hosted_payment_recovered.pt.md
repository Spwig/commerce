---
template_type: hosted_payment_recovered
category: License
---

# Email Template: hosted_payment_recovered

## Subject
Pagamento Bem-sucedido - {{ store_name }}

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
          Pagamento Bem-sucedido
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
          Olá {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Boas notícias! Seu pagamento de <strong>{{ currency }}{{ amount }}</strong> para <strong>{{ plan_name }}</strong> foi processado com sucesso. Sua assinatura continua sem interrupções.
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
Pagamento Bem-sucedido - {{ store_name }}

Olá {{ name|default:'there' }},

Boas notícias! Seu pagamento de {{ currency }}{{ amount }} para {{ plan_name }} foi processado com sucesso. Sua assinatura continua sem interrupções.

Go to Your Store: {{ admin_url }}

Need help? Contact {{ support_email }}
---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
Bem-vindo de volta! Conta reativada

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          🎉 Conta Reactivada!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          Bem-vindo de volta!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          Sua conta de afiliado está ativa novamente
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Olá {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Boas notícias! Sua conta de afiliado com {{ shop_name }} foi reativada.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Você pode retomar a promoção dos nossos produtos e a obtenção de comissões imediatamente.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Acessar Painel do Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contate o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Bem-vindo de volta! Conta reativada

Olá {{ affiliate_name }},

Boas notícias! Sua conta de afiliado com {{ shop_name }} foi reativada.

Vocês pode retomar a promoção dos nossos produtos e a obtenção de comissões imediatamente.

Acessar seu painel: {{ portal_url }}

{{ shop_name }}
Perguntas? Contate {{ support_email }}
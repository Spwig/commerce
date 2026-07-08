---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Importante: Conta Suspensa

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          Conta Suspensa
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
          Sua conta de afiliado com {{ shop_name }} foi suspensa.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Isso geralmente ocorre devido à violação dos termos e condições do nosso programa de afiliados.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Se você acredita que isso é um erro ou deseja discutir essa decisão, entre em contato com nossa equipe de suporte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Entre em Contato com o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Importante: Conta Suspensa

Olá {{ affiliate_name }},

Sua conta de afiliado com {{ shop_name }} foi suspensa.

Isso geralmente ocorre devido à violação dos termos e condições do nosso programa de afiliados.

Se você acredita que isso é um erro ou deseja discutir essa decisão, entre em contato com nossa equipe de suporte.

{{ shop_name }}
Perguntas? Contate {{ support_email }}
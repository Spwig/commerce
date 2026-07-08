---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
Link de Download Expirado - Pedido #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Link de Download Expirado
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Olá {{ customer_name }},
        </mj-text>
        <mj-text>
          Seu link de download para <strong>{{ product_name }}</strong> do pedido #{{ order_number }} expirou.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          Os links de download expiram {{ expiration_days }} dias após a compra por motivos de segurança.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Precisa de um novo link de download?
        </mj-text>
        <mj-text>
          Você pode solicitar um novo link de download fazendo login na sua conta ou entrando em contato com nossa equipe de suporte.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Ir para Minha Conta
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Dúvidas? Entre em contato com {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Link de Download Expirado

Olá {{ customer_name }},

Seu link de download para {{ product_name }} do pedido #{{ order_number }} expirou.

Os links de download expiram {{ expiration_days }} dias após a compra por motivos de segurança.

Precisa de um novo link de download?
Você pode solicitar um novo link de download fazendo login na sua conta ou entrando em contato com nossa equipe de suporte.

Ir para Minha Conta: {{ account_url }}

Dúvidas? Entre em contato com {{ support_email }}
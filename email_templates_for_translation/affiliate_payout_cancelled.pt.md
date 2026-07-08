---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
Pagamento cancelado - {{ payout_amount }}

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
          Pagamento Cancelado
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
          Seu pagamento de {{ payout_amount }} (ID do Pagamento: {{ payout_id }}) foi cancelado.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Se tiver dúvidas sobre por que este pagamento foi cancelado, entre em contato com nossa equipe de suporte.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          Ver Painel do Afiliado
        </mj-button>
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
Pagamento cancelado - {{ payout_amount }}

Olá {{ affiliate_name }},

Seu pagamento de {{ payout_amount }} (ID do Pagamento: {{ payout_id }}) foi cancelado.

Se tiver dúvidas sobre por que este pagamento foi cancelado, entre em contato com nossa equipe de suporte.

Ver seu painel: {{ portal_url }}

{{ shop_name }}
Perguntas? Entre em contato {{ support_email }}
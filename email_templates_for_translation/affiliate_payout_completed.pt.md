---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ Pagamento concluído: {{ payout_amount }}

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
          🎉 Pagamento Concluído!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Pagamento Concluído com Sucesso
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID do Pagamento: {{ payout_id }}
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
          Seu pagamento de {{ payout_amount }} foi concluído com sucesso!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Os fundos foram enviados para o seu método de pagamento. Dependendo do seu banco ou processador de pagamento, pode levar de 1 a 2 dias úteis para aparecer na sua conta.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Obrigado por promover {{ shop_name }}. Continue com o excelente trabalho!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver Detalhes do Pagamento
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Dúvidas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Entre em Contato com o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Pagamento concluído: {{ payout_amount }}

Olá {{ affiliate_name }},

Seu pagamento de {{ payout_amount }} foi concluído com sucesso!

Detalhes do Pagamento:
- ID do Pagamento: {{ payout_id }}
- Valor: {{ payout_amount }}
- Método de Pagamento: {{ payout_method }}

Os fundos foram enviados para o seu método de pagamento. Dependendo do seu banco ou processador de pagamento, pode levar de 1 a 2 dias úteis para aparecer na sua conta.

Obrigado por promover {{ shop_name }}. Continue com o excelente trabalho!

Ver detalhes do pagamento: {{ portal_url }}

{{ shop_name }}
Dúvidas? Entre em contato com {{ support_email }}
---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
Seu pagamento de {{ payout_amount }} está sendo processado

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
          💸 Processamento de Pagamento
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          Processando seu pagamento
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID do pagamento: {{ payout_id }}
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
          Boa noticia! Seu pagamento de {{ payout_amount }} está sendo processado agora.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Os fundos deverão chegar em sua conta em 3-5 dias únicos. Você receberá outro e-mail quando o pagamento for concluído.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID do pagamento:</strong> {{ payout_id }}<br/>
          <strong>Valor:</strong> {{ payout_amount }}<br/>
          <strong>Método de pagamento:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver história de pagamentos
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Dúvidas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Entrar em contato com o suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Seu {{ payout_amount }} pagamento está sendo processado

Olá {{ affiliate_name }},

Boa noticia! Seu pagamento de {{ payout_amount }} está sendo processado agora.

Detalhes do pagamento:
- ID do pagamento: {{ payout_id }}
- Valor: {{ payout_amount }}
- Método de pagamento: {{ payout_method }}

Os fundos deverão chegar em sua conta em 3-5 dias únicos. Você receberá outro e-mail quando o pagamento for concluído.

Ver história de pagamentos: {{ portal_url }}

{{ shop_name }}
Dúvidas? Entre em contato {{ support_email }}
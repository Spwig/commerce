---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Ação necessária: Pagamento falhou

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
          ⚠️ Pagamento Falhou
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          ID de Pagamento: {{ payout_id }}
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
          Nós encontramos um problema ao processar o seu pagamento de {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Isso geralmente é devido a informações de pagamento incorretas ou um problema com o seu provedor de pagamento.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Por favor, atualize suas informações de pagamento no seu painel de afiliado e entre em contato com nossa equipe de suporte para resolver esse problema.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Atualizar Informações de Pagamento
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Precisa de ajuda? <a href="mailto:{{ support_email }}" style="color: #007bff;">Entre em Contato com o Suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Ação necessária: Pagamento falhou

Olá {{ affiliate_name }},

Nós encontramos um problema ao processar o seu pagamento de {{ payout_amount }} (ID de Pagamento: {{ payout_id }}).

Isso geralmente é devido a informações de pagamento incorretas ou um problema com o seu provedor de pagamento.

Por favor, atualize suas informações de pagamento no seu painel de afiliado e entre em contato com nossa equipe de suporte para resolver esse problema.

Atualizar informações de pagamento: {{ portal_url }}

{{ shop_name }}
Precisa de ajuda? Entre em contato {{ support_email }}
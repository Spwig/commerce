---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
Você ganhou uma comissão de {{ commission_amount }}!

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
          💰 Comissão Ganha!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Boas notícias de {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Sua Comissão
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Da Ordem #{{ order_number }}
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
          Parabéns! Você ganhou uma comissão de {{ commission_amount }} da ordem #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Continue promovendo {{ shop_name }} para ganhar mais comissões. Quanto mais vendas você gerar, mais você ganhará!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Número da Ordem:</strong> #{{ order_number }}<br/>
          <strong>Valor da Comissão:</strong> {{ commission_amount }}<br/>
          <strong>Taxa de Comissão:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Ver Painel do Afiliado
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Perguntas? <a href="mailto:{{ support_email }}" style="color: #007bff;">Entre em contato com o suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Você ganhou uma comissão de {{ commission_amount }}!

Olá {{ affiliate_name }},

Parabéns! Você ganhou uma comissão de {{ commission_amount }} da ordem #{{ order_number }}.

Detalhes da Comissão:
- Número da Ordem: #{{ order_number }}
- Valor da Comissão: {{ commission_amount }}
- Taxa de Comissão: {{ commission_rate }}%

Continue promovendo {{ shop_name }} para ganhar mais comissões.

Ver seu painel: {{ portal_url }}

{{ shop_name }}
Perguntas? Entre em contato com {{ support_email }}
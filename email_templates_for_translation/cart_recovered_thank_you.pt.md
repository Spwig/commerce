---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Obrigado por sua ordem #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Obrigado por sua ordem!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Estamos felizes que você concluiu sua compra! Sua ordem foi confirmada e estamos a prepará-la para envio.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Resumo da ordem
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Número da ordem:</strong> {{ order_number }}<br/>
              <strong>Data da ordem:</strong> {{ order_date }}<br/>
              <strong>Total:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Rastrear sua ordem
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O que acontece a seguir?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Prepararemos sua ordem (normalmente dentro de 1-2 dias úteis)<br/>
          2. Você receberá uma confirmação de envio com informações de rastreamento<br/>
          3. Sua ordem será entregue para: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Você sabia?</strong><br/>
              Você pode rastrear sua ordem a qualquer momento no painel do seu conta.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Perguntas? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Entre em contato com nossa equipe de suporte</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 OBRIGADO POR SUA ORDEM!

Olá {{ customer_name }},

Estamos felizes que você concluiu sua compra! Sua ordem foi confirmada e estamos a prepará-la para envio.

RESUMO DA ORDEM:
- Número da ordem: {{ order_number }}
- Data da ordem: {{ order_date }}
- Total: {{ order_total }}

Rastrear sua ordem: {{ order_tracking_url }}

O QUE ACONTECE A SEGUIR?
1. Prepararemos sua ordem (normalmente dentro de 1-2 dias úteis)
2. Você receberá uma confirmação de envio com informações de rastreamento
3. Sua ordem será entregue para: {{ shipping_address }}

💡 VOCÊ SABIA?
Você pode rastrear sua ordem a qualquer momento no painel do seu conta.

Perguntas? Entre em contato com nossa equipe de suporte: {{ support_url }}

---
Ordem #{{ order_number }} em {{ shop_name }}
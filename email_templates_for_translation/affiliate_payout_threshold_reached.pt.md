---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Você atingiu o limite mínimo de saque!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Limite Mínimo de Saque Alcançado!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grande Novidade!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Olá {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Parabéns! Seu saldo de afiliado atingiu o limite mínimo de saque. Você pode agora solicitar um saque.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Seu Saldo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Saldo Disponível:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Valor Mínimo de Saque:</strong> {{ minimum_payout }}<br/>
              <strong>Comissões Pendentes:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          O Que Fazer Em Seguida:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Solicite um saque no painel de controle do seu afiliado<br/>
          • Pagamentos são processados {{ payout_schedule }}<br/>
          • Os fundos serão enviados via {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Solicitar Saque
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Ver Painel de Controle
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 LIMITE MÍNIMO DE SAQUE ATINGIDO!

Grande Novidade!

Olá {{ affiliate_name }},

Parabéns! Seu saldo de afiliado atingiu o limite mínimo de saque. Você pode agora solicitar um saque.

SEU SALDO:
- Saldo Disponível: {{ available_balance }}
- Valor Mínimo de Saque: {{ minimum_payout }}
- Comissões Pendentes: {{ pending_balance }}

O QUE FAZER EM SEGUIDA:
• Solicite um saque no painel de controle do seu afiliado
• Pagamentos são processados {{ payout_schedule }}
• Os fundos serão enviados via {{ payment_method }}

Solicitar saque: {{ request_payout_url }}
Ver painel de controle: {{ portal_url }}
---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Hai raggiunto il limite minimo per il pagamento!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Limite di pagamento raggiunto!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grandi notizie!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ciao {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Congratulazioni! Il tuo saldo affiliato ha raggiunto il limite minimo per il pagamento. Ora puoi richiedere un pagamento.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Il tuo saldo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Saldo disponibile:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Minimo pagamento:</strong> {{ minimum_payout }}<br/>
              <strong>Commissioni in sospeso:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cosa fare adesso:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Richiedi un pagamento dal tuo dashboard affiliato<br/>
          • I pagamenti vengono elaborati {{ payout_schedule }}<br/>
          • I fondi verranno inviati tramite {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Richiedi pagamento
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Visualizza dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 LIMITE MINIMO PER IL PAGAMENTO RAGGIUNTO!

Grandi notizie!

Ciao {{ affiliate_name }},

Congratulazioni! Il tuo saldo affiliato ha raggiunto il limite minimo per il pagamento. Ora puoi richiedere un pagamento.

IL TUO SALDO:
- Saldo disponibile: {{ available_balance }}
- Minimo pagamento: {{ minimum_payout }}
- Commissioni in sospeso: {{ pending_balance }}

COSA FARE AD ORA:
• Richiedi un pagamento dal tuo dashboard affiliato
• I pagamenti vengono elaborati {{ payout_schedule }}
• I fondi verranno inviati tramite {{ payment_method }}

Richiedi pagamento: {{ request_payout_url }}
Visualizza dashboard: {{ portal_url }}
---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Sie haben die Mindestauszahlungsschwelle erreicht!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Mindestauszahlungsschwelle erreicht!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Große Nachricht!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Herzlichen Glückwunsch! Ihr Affiliate-Konto hat die Mindestauszahlungsschwelle erreicht. Sie können nun eine Auszahlung anfordern.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Ihr Kontostand:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Verfügbares Guthaben:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Mindestauszahlung:</strong> {{ minimum_payout }}<br/>
              <strong>Warteendeinnahmen:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was kommt als nächstes:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Fordern Sie eine Auszahlung über Ihr Affiliate-Dashboard an<br/>
          • Zahlungen werden {{ payout_schedule }} verarbeitet<br/>
          • Das Geld wird über {{ payment_method }} gesendet
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Auszahlung anfordern
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Dashboard ansehen
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 MINDESTAUSZAHLUNGSSCHWELLE ERREICHT!

Große Nachricht!

Hi {{ affiliate_name }},

Herzlichen Glückwunsch! Ihr Affiliate-Konto hat die Mindestauszahlungsschwelle erreicht. Sie können nun eine Auszahlung anfordern.

IHR KONTOSTAND:
- Verfügbares Guthaben: {{ available_balance }}
- Mindestauszahlung: {{ minimum_payout }}
- Warteendeinnahmen: {{ pending_balance }}

WAS KOMMT ALS NÄCHSTES:
• Fordern Sie eine Auszahlung über Ihr Affiliate-Dashboard an
• Zahlungen werden {{ payout_schedule }} verarbeitet
• Das Geld wird über {{ payment_method }} gesendet

Auszahlung anfordern: {{ request_payout_url }}
Dashboard ansehen: {{ portal_url }}
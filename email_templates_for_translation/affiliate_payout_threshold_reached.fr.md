---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 Seuil de retrait atteint !

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Seuil de retrait atteint !
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Grande nouvelle !
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Félicitations ! Votre solde d'affiliation a atteint le seuil minimum de retrait. Vous pouvez maintenant demander un retrait.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Votre solde :
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Solde disponible :</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Montant minimum à retirer :</strong> {{ minimum_payout }}<br/>
              <strong>Commissions en attente :</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          À faire ensuite :
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Demandez un retrait depuis votre tableau de bord d'affiliation<br/>
          • Les paiements sont traités {{ payout_schedule }}<br/>
          • Les fonds seront envoyés via {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Demander un retrait
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Voir le tableau de bord
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 SEUIL DE RETRAIT ATTEINT !

Grande nouvelle !

Hi {{ affiliate_name }},

Félicitations ! Votre solde d'affiliation a atteint le seuil minimum de retrait. Vous pouvez maintenant demander un retrait.

VOTRE SOLDE :
- Solde disponible : {{ available_balance }}
- Montant minimum à retirer : {{ minimum_payout }}
- Commissions en attente : {{ pending_balance }}

À FAIRE EN SUITE :
• Demandez un retrait depuis votre tableau de bord d'affiliation
• Les paiements sont traités {{ payout_schedule }}
• Les fonds seront envoyés via {{ payment_method }}

Demander un retrait : {{ request_payout_url }}
Voir le tableau de bord : {{ portal_url }}
---
template_type: affiliate_payout_threshold_reached
category: Affiliate Program
---

# Email Template: affiliate_payout_threshold_reached

## Subject
💰 You've reached the minimum payout threshold!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          💰 Payout Threshold Reached!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Great News!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ affiliate_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Congratulations! Your affiliate balance has reached the minimum payout threshold. You can now request a payout.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Your Balance:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Available Balance:</strong> <span style="font-size: 24px; font-weight: bold; color: #059669;">{{ available_balance }}</span><br/>
              <strong>Minimum Payout:</strong> {{ minimum_payout }}<br/>
              <strong>Pending Commissions:</strong> {{ pending_balance }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What's Next:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Request a payout from your affiliate dashboard<br/>
          • Payments are processed {{ payout_schedule }}<br/>
          • Funds will be sent via {{ payment_method }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ request_payout_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Request Payout
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ portal_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          View Dashboard
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 PAYOUT THRESHOLD REACHED!

Great News!

Hi {{ affiliate_name }},

Congratulations! Your affiliate balance has reached the minimum payout threshold. You can now request a payout.

YOUR BALANCE:
- Available Balance: {{ available_balance }}
- Minimum Payout: {{ minimum_payout }}
- Pending Commissions: {{ pending_balance }}

WHAT'S NEXT:
• Request a payout from your affiliate dashboard
• Payments are processed {{ payout_schedule }}
• Funds will be sent via {{ payment_method }}

Request payout: {{ request_payout_url }}
View dashboard: {{ portal_url }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| available_balance | Available for payout | $247.50 |
| minimum_payout | Minimum threshold | $100.00 |
| pending_balance | Pending approval | $45.30 |
| payout_schedule | When payouts process | within 7 business days |
| payment_method | How affiliate gets paid | PayPal |
| request_payout_url | Payout request page | https://shop.com/en/affiliate/payout |
| portal_url | Affiliate dashboard | https://shop.com/en/affiliate |

## Notes

- Affiliate notification
- Sent when balance >= minimum payout threshold
- Encourages payout request
- Positive, congratulatory tone
- Transactional email

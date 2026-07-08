---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
Action required: Payout failed

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
          ⚠️ Payout Failed
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
          Payout ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          We encountered an issue processing your payout of {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          This is usually due to incorrect payment information or an issue with your payment provider.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Please update your payment information in your affiliate dashboard and contact our support team to resolve this issue.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          Update Payment Information
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Need help? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Action required: Payout failed

Hi {{ affiliate_name }},

We encountered an issue processing your payout of {{ payout_amount }} (Payout ID: {{ payout_id }}).

This is usually due to incorrect payment information or an issue with your payment provider.

Please update your payment information in your affiliate dashboard and contact our support team to resolve this issue.

Update payment info: {{ portal_url }}

{{ shop_name }}
Need help? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| shop_name | Store name | Amazing Shop |
| payout_id | Payout identifier | PAYOUT-2026-001 |
| payout_amount | Payout amount | $247.50 |
| portal_url | Affiliate dashboard URL | https://shop.com/en/affiliate |
| support_email | Support email address | support@shop.com |

## Notes

- Affiliate notification
- Sent when payout fails
- Transactional email - CRITICAL
- Requires immediate action from affiliate
- Empathetic but urgent tone
- Clear call-to-action to resolve issue

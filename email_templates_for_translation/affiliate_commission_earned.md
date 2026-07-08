---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
You earned a {{ commission_amount }} commission!

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
          💰 Commission Earned!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          Great news from {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 Your Commission
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          From Order #{{ order_number }}
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
          Congratulations! You've earned a {{ commission_amount }} commission from order #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Keep promoting {{ shop_name }} to earn more commissions. The more sales you generate, the more you earn!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>Order Number:</strong> #{{ order_number }}<br/>
          <strong>Commission Amount:</strong> {{ commission_amount }}<br/>
          <strong>Commission Rate:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          View Affiliate Dashboard
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
You earned a {{ commission_amount }} commission!

Hi {{ affiliate_name }},

Congratulations! You've earned a {{ commission_amount }} commission from order #{{ order_number }}.

Commission Details:
- Order Number: #{{ order_number }}
- Commission Amount: {{ commission_amount }}
- Commission Rate: {{ commission_rate }}%

Keep promoting {{ shop_name }} to earn more commissions.

View your dashboard: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| shop_name | Store name | Amazing Shop |
| order_number | Order number | 2026-001234 |
| commission_amount | Commission earned | $47.50 |
| commission_rate | Commission percentage | 10 |
| portal_url | Affiliate dashboard URL | https://shop.com/en/affiliate |
| support_email | Support email address | support@shop.com |

## Notes

- Affiliate notification
- Sent immediately when commission is earned
- Transactional email
- Positive, congratulatory tone
- Encourages continued promotion

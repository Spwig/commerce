---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
Commission reversed - Order #{{ order_number }}

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
          Commission Reversed
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
          The commission for order #{{ order_number }} ({{ commission_amount }}) has been reversed due to a customer refund.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          When customers request refunds, any associated commissions are automatically reversed to ensure accurate accounting.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          This is a normal part of the affiliate process. Continue promoting {{ shop_name }} to earn new commissions!
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
Commission reversed - Order #{{ order_number }}

Hi {{ affiliate_name }},

The commission for order #{{ order_number }} ({{ commission_amount }}) has been reversed due to a customer refund.

When customers request refunds, any associated commissions are automatically reversed to ensure accurate accounting.

This is a normal part of the affiliate process. Continue promoting {{ shop_name }} to earn new commissions!

View your dashboard: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| shop_name | Store name | Amazing Shop |
| order_number | Order number | 2026-001234 |
| commission_amount | Commission amount | $47.50 |
| portal_url | Affiliate dashboard URL | https://shop.com/en/affiliate |
| support_email | Support email address | support@shop.com |

## Notes

- Affiliate notification
- Sent when commission is reversed after customer refund
- Transactional email
- Explains reversal is normal process
- Encouraging tone to continue promoting

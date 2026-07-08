---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
Important: Account Suspended

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
          Account Suspended
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
          Your affiliate account with {{ shop_name }} has been suspended.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          This is usually due to a violation of our affiliate program terms and conditions.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          If you believe this is an error or would like to discuss this decision, please contact our support team.
        </mj-text>
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
Important: Account Suspended

Hi {{ affiliate_name }},

Your affiliate account with {{ shop_name }} has been suspended.

This is usually due to a violation of our affiliate program terms and conditions.

If you believe this is an error or would like to discuss this decision, please contact our support team.

{{ shop_name }}
Questions? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| shop_name | Store name | Amazing Shop |
| support_email | Support email address | support@shop.com |

## Notes

- Affiliate notification
- Sent when affiliate account is suspended
- Transactional email - CRITICAL
- Serious, professional tone
- Explains reason generally (TOS violation)
- Provides path to appeal/discuss

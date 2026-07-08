---
template_type: affiliate_account_rejected
category: Affiliate Program
---

# Email Template: affiliate_account_rejected

## Subject
Affiliate Application Update

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
          Application Update
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
          Thank you for your interest in joining the {{ shop_name }} affiliate program.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          After reviewing your application, we've decided not to move forward at this time.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          This decision is based on our current affiliate program requirements and may not reflect your qualifications or potential.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          You're welcome to reapply in the future if your circumstances change.
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
Affiliate Application Update

Hi {{ affiliate_name }},

Thank you for your interest in joining the {{ shop_name }} affiliate program.

After reviewing your application, we've decided not to move forward at this time.

This decision is based on our current affiliate program requirements and may not reflect your qualifications or potential.

You're welcome to reapply in the future if your circumstances change.

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
- Sent when affiliate account application is rejected
- Transactional email
- Professional, respectful tone
- Leaves door open for future application
- Provides support contact

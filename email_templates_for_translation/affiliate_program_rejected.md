---
template_type: affiliate_program_rejected
category: Affiliate Program
---

# Email Template: affiliate_program_rejected

## Subject
Program Application Update

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
          Thank you for applying to promote {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          After reviewing your application, we've decided not to approve it at this time.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          You can still promote other programs in our affiliate network.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          View Other Programs
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
Program Application Update

Hi {{ affiliate_name }},

Thank you for applying to promote {{ program_name }}.

After reviewing your application, we've decided not to approve it at this time.

You can still promote other programs in our affiliate network.

View other programs: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| affiliate_name | Affiliate's name | John Smith |
| shop_name | Store name | Amazing Shop |
| program_name | Specific program name | Premium Products Program |
| portal_url | Affiliate dashboard URL | https://shop.com/en/affiliate |
| support_email | Support email address | support@shop.com |

## Notes

- Affiliate notification
- Sent when affiliate is rejected for a specific program/category
- Transactional email
- Professional, respectful tone
- Redirects to other opportunities
- For multi-tier or category-based affiliate programs

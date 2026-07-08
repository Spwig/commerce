---
template_type: affiliate_program_approved
category: Affiliate Program
---

# Email Template: affiliate_program_approved

## Subject
Genehmigt für {{ program_name }}!

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
          ✓ Program Approved!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          {{ program_name }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          You've been approved!
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
          Great news! You've been approved to promote {{ program_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Start sharing this program to earn commissions!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          Get Affiliate Links
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Fragen? <a href="mailto:{{ support_email }}" style="color: #007bff;">Kontaktieren Sie den Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Genehmigt für {{ program_name }}!

Hi {{ affiliate_name }},

Great news! You've been approved to promote {{ program_name }}.

Start sharing this program to earn commissions!

Get affiliate links: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}
---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
भुगतान रद्द - {{ payout_amount }}

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
          भुगतान रद्द
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          हेलो {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ payout_amount }} (भुगतान सीधा: {{ payout_id }}) का आपका भुगतान रद्द कर दिया गया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          यदि आप इस भुगतान के रद्द करने के कारण के बारे में सवाल हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          अपने एफिलिएट डैशबोर्ड को देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
भुगतान रद्द - {{ payout_amount }}

हेलो {{ affiliate_name }},

{{ payout_amount }} (भुगतान सीधा: {{ payout_id }}) का आपका भुगतान रद्द कर दिया गया है।

यदि आप इस भुगतान के रद्द करने के कारण के बारे में सवाल हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।

अपने डैशबोर्ड को देखें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
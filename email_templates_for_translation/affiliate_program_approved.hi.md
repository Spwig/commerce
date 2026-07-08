---
template_type: affiliate_program_approved
category: Affiliate Program
---

# Email Template: affiliate_program_approved

## Subject
अनुमोदित के लिए {{ program_name }}!

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
          ✓ प्रोग्राम अनुमोदित!
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
          आप अनुमोदित कर दिया गया है!
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
          अच्छी खबर! आपको {{ program_name }} के लिए प्रचार करने के लिए अनुमोदित कर दिया गया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          इस प्रोग्राम को साझा करना शुरू करें और कमीशन कमा लीजिए!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          अफिलिएट लिंक प्राप्त करें
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
अनुमोदित के लिए {{ program_name }}!

हेलो {{ affiliate_name }},

अच्छी खबर! आपको {{ program_name }} के लिए प्रचार करने के लिए अनुमोदित कर दिया गया है।

इस प्रोग्राम को साझा करना शुरू करें और कमीशन कमा लीजिए!

अफिलिएट लिंक प्राप्त करें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
वापस आओ! खाता पुनः जीवित कर दिया गया

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
          🎉 खाता पुनः जीवित कर दिया गया!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          वापस आओ!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          आपका अफिलिएट खाता फिर से सक्रिय हो गया है
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
          अच्छी खबर! {{ shop_name }} के साथ आपका अफिलिएट खाता पुनः जीवित कर दिया गया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          आप तुरंत हमारे उत्पादों के प्रचार और कमीशन कमाना शुरू कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          अफिलिएट डैशबोर्ड पहुंचें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            समर्थन से संपर्क करें
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
वापस आओ! खाता पुनः जीवित कर दिया गया

हेलो {{ affiliate_name }},

अच्छी खबर! {{ shop_name }} के साथ आपका अफिलिएट खाता पुनः जीवित कर दिया गया है।

आप तुरंत हमारे उत्पादों के प्रचार और कमीशन कमाना शुरू कर सकते हैं।

अपने डैशबोर्ड तक पहुंच: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
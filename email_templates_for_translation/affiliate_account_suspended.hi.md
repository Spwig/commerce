---
template_type: affiliate_account_suspended
category: Affiliate Program
---

# Email Template: affiliate_account_suspended

## Subject
महत्वपूर्ण: खाता बंद कर दिया गया

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
महत्वपूर्ण: खाता बंद कर दिया गया

हैलो {{ affiliate_name }},

आपका अफिलिएट खाता {{ shop_name }} के साथ बंद कर दिया गया है।

यह आमतौर पर हमारे अफिलिएट प्रोग्राम के शर्तों और प्रतिबंधों के उल्लंघन के कारण होता है।

अगर आपको लगता है कि यह एक त्रुटि है या इस फैसले के बारे में चर्चा करना चाहते हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।

{{ shop_name }}
सवाल? {{ support_email }} से संपर्क करें।
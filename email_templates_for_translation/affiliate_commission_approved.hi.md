---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
कमीशन मंजूर कर दिया गया: {{ commission_amount }}

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
          ✓ कमीशन मंजूर कर दिया गया!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          पैमेंट के लिए मंजूर कर दिया गया
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          हैलो {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          आपका कमीशन {{ commission_amount }} ऑर्डर #{{ order_number }} से मंजूर कर दिया गया है और आपके अगले पैमेंट में शामिल किया जाएगा।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          पैमेंट आपके भुगतान अनुसूची के अनुसार प्रक्रिया में रखा जाता है। आपको पैमेंट प्रक्रिया में एक अन्य ईमेल प्राप्त होगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          कमीशन देखें
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
कमीशन मंजूर कर दिया गया: {{ commission_amount }}

हैलो {{ affiliate_name }},

आपका कमीशन {{ commission_amount }} ऑर्डर #{{ order_number }} से मंजूर कर दिया गया है और आपके अगले पैमेंट में शामिल किया जाएगा।

पैमेंट आपके भुगतान अनुसूची के अनुसार प्रक्रिया में रखा जाता है। आपको पैमेंट प्रक्रिया में एक अन्य ईमेल प्राप्त होगा।

कमीशन देखें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें


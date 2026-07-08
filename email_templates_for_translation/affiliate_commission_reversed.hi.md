---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
कमीशन वापस - आदेश #{{ order_number }}

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
          कमीशन वापस
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
          आदेश #{{ order_number }} ({{ commission_amount }}) के लिए कमीशन एक ग्राहक रिफंड के कारण वापस कर दिया गया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          जब ग्राहक रिफंड के लिए अनुरोध करते हैं, तो किसी भी संबंधित कमीशन को स्वचालित रूप से वापस कर दिया जाता है ताकि लेखा ठीक से बनाए रखा जा सके।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          यह एफिलिएट प्रक्रिया का एक सामान्य हिस्सा है। {{ shop_name }} के प्रचार को जारी रखें और नए कमीशन कमाएं!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          अफिलिएट डैशबोर्ड देखें
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
कमीशन वापस - आदेश #{{ order_number }}

हेलो {{ affiliate_name }},

आदेश #{{ order_number }} ({{ commission_amount }}) के लिए कमीशन एक ग्राहक रिफंड के कारण वापस कर दिया गया है।

जब ग्राहक रिफंड के लिए अनुरोध करते हैं, तो किसी भी संबंधित कमीशन को स्वचालित रूप से वापस कर दिया जाता है ताकि लेखा ठीक से बनाए रखा जा सके।

यह एफिलिएट प्रक्रिया का एक सामान्य हिस्सा है। {{ shop_name }} के प्रचार को जारी रखें और नए कमीशन कमाएं!

अपने डैशबोर्ड को देखें: {{ portal_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें

कृपया ध्यान दें: सभी Django टेम्पलेट सिंटैक्स ({{ }}, {% %}), सभी MJML टैग (<mj-*>), सभी HTML एट्रिब्यूट्स और सभी इमोजी को संरक्षित रखें।
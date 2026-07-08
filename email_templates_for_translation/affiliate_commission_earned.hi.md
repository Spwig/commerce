---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
आपने {{ commission_amount }} कमीशन कमाया है!

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
          💰 कमीशन कमाया है!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          {{ shop_name }} से अच्छी खबर
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 आपका कमीशन
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ऑर्डर #{{ order_number }} से
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
          बधाई हो! आपने ऑर्डर #{{ order_number }} से {{ commission_amount }} कमीशन कमाया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          {{ shop_name }} के अधिक बिक्री के लिए प्रचार जारी रखें ताकि अधिक कमीशन कमाया जा सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ऑर्डर नंबर:</strong> #{{ order_number }}<br/>
          <strong>कमीशन राशि:</strong> {{ commission_amount }}<br/>
          <strong>कमीशन दर:</strong> {{ commission_rate }}%
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
          प्रश्न हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपने {{ commission_amount }} कमीशन कमाया है!

हेलो {{ affiliate_name }},

बधाई हो! आपने ऑर्डर #{{ order_number }} से {{ commission_amount }} कमीशन कमाया है।

कमीशन विवरण:
- ऑर्डर नंबर: #{{ order_number }}
- कमीशन राशि: {{ commission_amount }}
- कमीशन दर: {{ commission_rate }}%

{{ shop_name }} के अधिक बिक्री के लिए प्रचार जारी रखें ताकि अधिक कमीशन कमाया जा सके।

अपने डैशबोर्ड को देखें: {{ portal_url }}

{{ shop_name }}
प्रश्न हैं? {{ support_email }} से संपर्क करें
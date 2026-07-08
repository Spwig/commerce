---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
कमीशन स्थिति अपडेट - आर्डर #{{ order_number }}

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
          कमीशन स्थिति अपडेट
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
          हम आपको बताना चाहते हैं कि आर्डर #{{ order_number }} ({{ commission_amount }}) के लिए कमीशन स्वीकृत नहीं किया गया।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          यह आमतौर पर तब होता है जब एक आर्डर कमीशन अवधि समाप्त होने से पहले रद्द या वापसी कर दिया जाता है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          अगर आप इस कमीशन के बारे में कोई सवाल पूछना चाहते हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          अफिलिएट डैशबोर्ड देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          सवाल? <a href="mailto:{{ support_email }}" style="color: #007bff;">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
कमीशन स्थिति अपडेट - आर्डर #{{ order_number }}

हेलो {{ affiliate_name }},

हम आपको बताना चाहते हैं कि आर्डर #{{ order_number }} ({{ commission_amount }}) के लिए कमीशन स्वीकृत नहीं किया गया।

यह आमतौर पर तब होता है जब एक आर्डर कमीशन अवधि समाप्त होने से पहले रद्द या वापसी कर दिया जाता है।

अगर आप इस कमीशन के बारे में कोई सवाल पूछना चाहते हैं, तो कृपया हमारी समर्थन टीम से संपर्क करें।

अपने डैशबोर्ड को देखें: {{ portal_url }}

{{ shop_name }}
सवाल? {{ support_email }} से संपर्क करें

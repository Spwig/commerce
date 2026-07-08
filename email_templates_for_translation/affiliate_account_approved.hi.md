---
template_type: affiliate_account_approved
category: Affiliate Program
---

# Email Template: affiliate_account_approved

## Subject
🎉 {{ shop_name }} के सहायता कार्यक्रम में आपका स्वागत है!

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
          🎉 आवेदन स्वीकृत!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          हमारे सहायता कार्यक्रम में आपका स्वागत है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          अब आप एक सहायक हैं!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          आज कमीशन कमाना शुरू करें
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
          बधाई हो! आपके {{ shop_name }} सहायता कार्यक्रम में शामिल होने के आवेदन को स्वीकृत कर दिया गया है।
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          अब आप हमारे उत्पादों के प्रचार करना शुरू कर सकते हैं और आपके द्वारा उत्पन्न प्रत्येक बिक्री पर कमीशन कमाएं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#212529" align="center" padding-bottom="10px">
          कैसे काम करता है
        </mj-text>
        <mj-text font-size="14px" color="#6c757d">
          1. डैशबोर्ड से अपने अद्वितीय सहायता लिंक प्राप्त करें<br/>
          2. अपने श्रोताओं के साथ इन लिंकों को साझा करें<br/>
          3. जब लोग आपके लिंक के माध्यम से खरीदते हैं तो कमीशन कमाएं<br/>
          4. अपने भुगतान अनुलगन के अनुसार भुगतान प्राप्त करें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          सहायक डैशबोर्ड पहुँचें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          प्रश्न हैं? <a href="mailto:{{ support_email }}" style="color: #007bff;">
          समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ shop_name }} के सहायता कार्यक्रम में आपका स्वागत है!

हेलो {{ affiliate_name }},

बधाई हो! आपके {{ shop_name }} सहायता कार्यक्रम में शामिल होने के आवेदन को स्वीकृत कर दिया गया है।

अब आप हमारे उत्पादों के प्रचार करना शुरू कर सकते हैं और आपके द्वारा उत्पन्न प्रत्येक बिक्री पर कमीशन कमाएं।

कैसे काम करता है:
1. डैशबोर्ड से अपने अद्वितीय सहायता लिंक प्राप्त करें
2. अपने श्रोताओं के साथ इन लिंकों को साझा करें
3. जब लोग आपके लिंक के माध्यम से खरीदते हैं तो कमीशन कमाएं
4. अपने भुगतान अनुलगन के अनुसार भुगतान प्राप्त करें

आपके डैशबोर्ड तक पहुँचें: {{ portal_url }}

{{ shop_name }}
प्रश्न हैं? {{ support_email }} से संपर्क करें
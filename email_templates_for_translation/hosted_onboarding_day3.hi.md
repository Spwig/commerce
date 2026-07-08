---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
अपना कैटलॉग बनाएं - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          शुरू करें: आपके उत्पाद
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} के लिए एक अच्छा कैटलॉग बनाएं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हैलो {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          आपका स्टोर <strong>{{ store_name }}</strong> तैयार है। अब आपके उत्पाद कैटलॉग बनाने का समय है। शुरू करने के लिए पांच सुझाव हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          CSV से उत्पाद आयात करें
        </mj-text>
        <mj-text font-size="14px">
          पहले से ही एक उत्पाद सूची है? <strong>Admin > Catalog > Import</strong> जाएं और CSV फ़ाइल से अपने उत्पादों को बैच आयात करें। यह अपने स्टोर को भरने के लिए सबसे तेज़ तरीका है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          श्रेणियों और फ़िल्टर्स के साथ संगठित करें
        </mj-text>
        <mj-text font-size="14px">
          ग्राहकों के लिए आसानी से ब्राउज़ और खोज करने के लिए श्रेणियाँ और गुण फ़िल्टर बनाएं। अच्छी तरह से संगठित कैटलॉग उच्च परिवर्तन दर के लिए जिम्मेदार होता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          आकर्षक उत्पाद विवरण लिखें
        </mj-text>
        <mj-text font-size="14px">
          अच्छे विवरण उत्पादों को बेचते हैं। लाभों पर ध्यान केंद्रित करें, केवल विशेषताओं पर नहीं। ग्राहकों को बताएं कि वे अपने उत्पाद की आवश्यकता क्यों है और यह उनकी समस्या कैसे हल करता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          उच्च गुणवत्ता वाले उत्पाद चित्र अपलोड करें
        </mj-text>
        <mj-text font-size="14px">
          स्पष्ट, व्यावसायिक चित्र बहुत अंतर बनाते हैं। विभिन्न कोणों के चित्र अपलोड करें और एकसमान प्रकाश का उपयोग करें। Spwig चित्रों को त्वरित लोडिंग के लिए स्वचालित रूप से अपटेट करता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          उत्पाद वैरिएंट्स सेट अप करें
        </mj-text>
        <mj-text font-size="14px">
          यदि आपके उत्पाद विभिन्न आकारों, रंगों या स्टाइल में आते हैं, तो ग्राहकों के लिए वैरिएंट्स बनाएं ताकि वे अपने अनुसार बिल्कुल चुन सकें। प्रत्येक वैरिएंट के अपने अलग मूल्य, स्टॉक स्तर और चित्र हो सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Manage Your Products" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
शुरू करें: आपके उत्पाद - {{ store_name }}

हैलो {{ name|default:'there' }},

आपका स्टोर {{ store_name }} तैयार है। अब आपके उत्पाद कैटलॉग बनाने का समय है। शुरू करने के लिए पांच सुझाव हैं।

1. CSV से उत्पाद आयात करें
पहले से ही एक उत्पाद सूची है? Admin > Catalog > Import जाएं और CSV फ़ाइल से अपने उत्पादों को बैच आयात करें।

2. श्रेणियों और फ़िल्टर्स के साथ संगठित करें
ग्राहकों के लिए आसानी से ब्राउज़ और खोज करने के लिए श्रेणियाँ और गुण फ़िल्टर बनाएं।

3. आकर्षक उत्पाद विवरण लिखें
अच्छे विवरण उत्पादों को बेचते हैं। लाभों पर ध्यान केंद्रित करें, केवल विशेषताओं पर नहीं। ग्राहकों को बताएं कि वे अपने उत्पाद की आवश्यकता क्यों है।

4. उच्च गुणवत्ता वाले उत्पाद चित्र अपलोड करें
स्पष्ट, व्यावसायिक चित्र बहुत अंतर बनाते हैं। विभिन्न कोणों के चित्र अपलोड करें और एकसमान प्रकाश का उपयोग करें।

5. उत्पाद वैरिएंट्स सेट अप करें
यदि आपके उत्पाद विभिन्न आकारों, रंगों या स्टाइल में आते हैं, तो ग्राहकों के लिए वैरिएंट्स बनाएं ताकि वे अपने अनुसार बिल्कुल चुन सकें।

आपके उत्पादों का प्रबंधन करें: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
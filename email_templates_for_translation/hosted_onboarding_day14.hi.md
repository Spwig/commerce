---
template_type: hosted_onboarding_day14
category: License
---

# Email Template: hosted_onboarding_day14

## Subject
आगे बढ़े - {{ store_name }}

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
          शुरू करें: उन्नत विशेषताएं
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} के पूर्ण संभावना को खोलें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          आपके {{ store_name }} के चलाने के कुछ सप्ताह हो गए हैं। यहां कुछ उन्नत विशेषताएं हैं जो आपके स्टोर को अगले स्तर पर ले जाने में मदद करेंगी।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          स्वचालित ईमेल वर्कफ़्लो सेट करें
        </mj-text>
        <mj-text font-size="14px">
          ईमेल वर्कफ़्लो के साथ अपनी ग्राहक संचार को स्वचालित करें। बैठक के बाद के फॉलो-अप, पोस्ट-खरीद फॉलो-अप और पुनर्जीवित करने के अभियानों के लिए <strong>मार्केटिंग > ईमेल वर्कफ़्लो</strong> में वर्कफ़्लो सेट करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने क्षेत्रों के लिए कर नियमों को सेट करें
        </mj-text>
        <mj-text font-size="14px">
          यह सुनिश्चित करें कि आप सही कर दर वसूल रहे हैं। <strong>सेटिंग्स > कर</strong> जाएं और उन क्षेत्रों के लिए कर नियमों को सेट करें जहां आप बेच रहे हैं। आप कर-समावेशी या कर-अपवर्जित मूल्य निर्धारण सेट कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          एपीआई के लिए एक्सप्लोर करें
        </mj-text>
        <mj-text font-size="14px">
          यदि आपका योजना एपीआई पहुंच शामिल करता है, तो आप अपने स्टोर को बाहरी उपकरणों और सेवाओं के साथ एकीकृत कर सकते हैं। <strong>सेटिंग्स > एपीआई</strong> जाएं और एपीआई कुंजियों बनाएं और दस्तावेज़ को एक्सप्लोर करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने एनालिटिक्स डैशबोर्ड की जांच करें
        </mj-text>
        <mj-text font-size="14px">
          अपने स्टोर के प्रदर्शन पर नज़र रखें। आपका <strong>डैशबोर्ड</strong> राजस्व, आदेश, शीर्ष उत्पाद और ग्राहक अंतर्दृष्टि शामिल कुछ महत्वपूर्ण मीट्रिक्स दिखाता है जो आपको डेटा-आधारित निर्णय लेने में मदद करता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          ऑन-साइट बिक्री के लिए पॉइंट-ऑफ-सेल के बारे में सोचें
        </mj-text>
        <mj-text font-size="14px">
          ऑन-साइट बिक्री भी करते हैं? Spwig के पॉइंट-ऑफ-सेल विशेषता आपके ऑनलाइन स्टॉक और ऑर्डर प्रबंधन के साथ ऑन-साइट लेनदेन को प्रोसेस करता है। <strong>सेटिंग्स > पॉइंट ऑफ सेल</strong> जाएं और अधिक जानें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="अपने डैशबोर्ड को एक्सप्लोर करें" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
शुरू करें: उन्नत विशेषताएं - {{ store_name }}

हेलो {{ name|default:'there' }},

आपके {{ store_name }} के चलाने के कुछ सप्ताह हो गए हैं। यहां कुछ उन्नत विशेषताएं हैं जो आपके स्टोर को अगले स्तर पर ले जाने में मदद करेंगी।

1. स्वचालित ईमेल वर्कफ़्लो सेट करें
ईमेल वर्कफ़्लो के साथ अपनी ग्राहक संचार को स्वचालित करें। बैठक के बाद के फॉलो-अप, पोस्ट-खरीद फॉलो-अप और पुनर्जीवित करने के अभियानों के लिए।

2. अपने क्षेत्रों के लिए कर नियमों को सेट करें
यह सुनिश्चित करें कि आप सही कर दर वसूल रहे हैं। सेटिंग्स > कर जाएं और उन क्षेत्रों के लिए कर नियमों को सेट करें जहां आप बेच रहे हैं। आप कर-समावेशी या कर-अपवर्जित मूल्य निर्धारण सेट कर सकते हैं।

3. एपीआई के लिए एक्सप्लोर करें
यदि आपका योजना एपीआई पहुंच शामिल करता है, तो आप अपने स्टोर को बाहरी उपकरणों और सेवाओं के साथ एकीकृत कर सकते हैं। सेटिंग्स > एपीआई जाएं और एपीआई कुंजियों बनाएं और दस्तावेज़ को एक्सप्लोर करें।

4. अपने एनालिटिक्स डैशबोर्ड की जांच करें
अपने स्टोर के प्रदर्शन पर नज़र रखें। आपका डैशबोर्ड राजस्व, आदेश, शीर्ष उत्पाद और ग्राहक अंतर्दृष्टि शामिल कुछ महत्वपूर्ण मीट्रिक्स दिखाता है जो आपको डेटा-आधारित निर्णय लेने में मदद करता है।

5. ऑन-साइट बिक्री के लिए पॉइंट-ऑफ-सेल के बारे में सोचें
ऑन-साइट बिक्री भी करते हैं? Spwig के पॉइंट-ऑफ-सेल विशेषता आपके ऑनलाइन स्टॉक और ऑर्डर प्रबंधन के साथ ऑन-साइट लेनदेन को प्रोसेस करता है। सेटिंग्स > पॉइंट ऑफ सेल जाएं और अधिक जानें।

अपने डैशबोर्ड को एक्सप्लोर करें: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
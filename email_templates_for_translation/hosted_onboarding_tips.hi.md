---
template_type: hosted_onboarding_tips
category: License
---

# Email Template: hosted_onboarding_tips

## Subject
आपके {{ store_name }} से अधिक लाभ उठाने के लिए टिप्स

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
          शुरू करने के टिप्स
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          अपने Spwig स्टोर का अधिकतम लाभ उठाएं
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
          अब जबकि <strong>{{ store_name }}</strong> चल रहा है, यहां कुछ टिप्स हैं जो आपके स्टोर से अधिकतम लाभ उठाने में आपकी मदद करेंगे।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1: Theme -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने लुक का अनुकूलन करें
        </mj-text>
        <mj-text font-size="14px">
          <strong>डिज़ाइन > थीम सेटिंग्स</strong> जाएं और एक थीम चुनें, अपने लोगो को अपलोड करें, और अपने ब्रांड के रंगों को सेट करें। आपका स्टोर तुरंत अपडेट हो जाएगा ताकि आप वास्तविक समय में परिवर्तनों का पूर्वाभ्यास कर सकें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2: Products -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने उत्पादों को जोड़ें
        </mj-text>
        <mj-text font-size="14px">
          <strong>कैटलॉग > उत्पाद</strong> जाएं और अपने आइटम को जोड़ना शुरू करें। आप उत्पाद वैरिएंट (आकार, रंग), मूल्य निर्धारित कर सकते हैं, स्टॉक का प्रबंधन कर सकते हैं, और उच्च गुणवत्ता वाली छवियों को अपलोड कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3: Payments -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          भुगतान की सुविधा करें
        </mj-text>
        <mj-text font-size="14px">
          <strong>सेटिंग्स > भुगतान प्रदाता</strong> जाएं और स्ट्राइप, पेपैल या अन्य भुगतान विधि के साथ जोड़ें। आप एक से अधिक प्रदाताओं को सक्षम कर सकते हैं ताकि आपके ग्राहक अपने पसंद के अनुसार भुगतान कर सकें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4: Shipping -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          शिपिंग को सेट करें
        </mj-text>
        <mj-text font-size="14px">
          <strong>सेटिंग्स > शिपिंग</strong> के तहत अपने शिपिंग जोन और दरों को सेट करें। आप विभिन्न क्षेत्रों के लिए फ्लैट दर, वजन आधारित या मुफ्त शिपिंग के नियम बना सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5: SEO -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने SEO को बढ़ाएं
        </mj-text>
        <mj-text font-size="14px">
          Spwig स्वचालित रूप से साइटमैप और मेटा टैग उत्पन्न करता है। <strong>सेटिंग्स > SEO</strong> जाएं और अपने पृष्ठ शीर्षक, विवरण और सोशल शेयरिंग छवियों को अनुकूलित करें ताकि ग्राहक आपके स्टोर को ढूंढ सकें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
शुरू करने के टिप्स - {{ store_name }}

हेलो {{ name|default:'there' }},

अब जबकि {{ store_name }} चल रहा है, यहां कुछ टिप्स हैं जो आपके स्टोर से अधिकतम लाभ उठाने में आपकी मदद करेंगे।

1. अपने लुक का अनुकूलन करें
डिज़ाइन > थीम सेटिंग्स जाएं और एक थीम चुनें, अपने लोगो को अपलोड करें, और अपने ब्रांड के रंगों को सेट करें।

2. अपने उत्पादों को जोड़ें
कैटलॉग > उत्पाद जाएं और अपने आइटम को जोड़ना शुरू करें वैरिएंट, मूल्य निर्धारित करें, और छवियों को अपलोड करें।

3. भुगतान की सुविधा करें
सेटिंग्स > भुगतान प्रदाता जाएं और स्ट्राइप, पेपैल या अन्य भुगतान विधि के साथ जोड़ें।

4. शिपिंग को सेट करें
सेटिंग्स > शिपिंग के तहत अपने शिपिंग जोन और दरों को सेट करें। आप विभिन्न क्षेत्रों के लिए फ्लैट दर, वजन आधारित या मुफ्त शिपिंग के नियम बना सकते हैं।

5. अपने SEO को बढ़ाएं
सेटिंग्स > SEO जाएं और अपने पृष्ठ शीर्षक, विवरण और सोशल शेयरिंग छवियों को अनुकूलित करें ताकि ग्राहक आपके स्टोर को ढूंढ सकें।

प्रशासन पैनल जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} से संपर्क करें
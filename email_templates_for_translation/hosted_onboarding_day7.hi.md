---
template_type: hosted_onboarding_day7
category: License
---

# Email Template: hosted_onboarding_day7

## Subject
बिक्री बढ़ाएं - {{ store_name }}

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
          शुरुआत: बाजार व मार्केटिंग
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} के लिए ट्रैफिक और बिक्री बढ़ाएं
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
          अब जबकि {{ store_name }} आकार ले रहा है, तो ट्रैफिक बढ़ाने और आपकी बिक्री को बढ़ाने पर ध्यान केंद्रित करने का समय है। यहां पांच मार्केटिंग के सुझाव हैं जो आपको शुरुआत के लिए मदद कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपना पहला डिस्काउंट कोड बनाएं
        </mj-text>
        <mj-text font-size="14px">
          अपने पहले ग्राहकों को आकर्षित करने के लिए लॉन्च डिस्काउंट पेश करें। डिस्काउंट कोड बनाने के लिए <strong>मार्केटिंग > डिस्काउंट कोड</strong> जाएं और उपयोग की सीमा और अवधि के विकल्प के साथ प्रतिशत या निश्चित राशि के डिस्काउंट बनाएं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          छोड़े गए कार्ट के पुनर्प्राप्ति को सेट अप करें
        </mj-text>
        <mj-text font-size="14px">
          खोए हुए बिक्री को स्वचालित रूप से पुनर्प्राप्त करें। <strong>मार्केटिंग > छोड़े गए कार्ट</strong> के तहत छोड़े गए कार्ट के पुनर्प्राप्ति ईमेल को एनेबल करें ताकि ग्राहकों को उन आइटम्स के बारे में याद दिलाया जा सके जो वे पीछे छोड़ गए।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          अपने सोशल मीडिया अकाउंट को कनेक्ट करें
        </mj-text>
        <mj-text font-size="14px">
          अपने सोशल मीडिया प्रोफाइल को अपने स्टोर से लिंक करें ताकि ग्राहक आपको ढूंढ सकें और फॉलो कर सकें। <strong>सेटिंग्स > सोशल मीडिया</strong> के तहत सोशल लिंक जोड़ें ताकि आपके स्टोर के फूटर में दिखाए जा सकें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          गूगल एनालिटिक्स ट्रैकिंग को सेट अप करें
        </mj-text>
        <mj-text font-size="14px">
          जानें कि आपके आगंतुक कहां से आ रहे हैं और वे आपके स्टोर के साथ कैसे बर्ताव कर रहे हैं। <strong>सेटिंग्स > एनालिटिक्स</strong> के तहत अपने गूगल एनालिटिक्स ट्रैकिंग आईडी जोड़ें ताकि डेटा के संग्रह को शुरू किया जा सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          एक न्यूज़लेटर साइनअप फॉर्म बनाएं
        </mj-text>
        <mj-text font-size="14px">
          एक दिन से अपने ईमेल सूची को बनाएं। अपने स्टोर में एक न्यूज़लेटर साइनअप फॉर्म जोड़ें ताकि आगंतुक ईमेल एकत्र किए जा सकें। इन संपर्कों का उपयोग प्रोमोशन, उत्पाद लॉन्च और ग्राहक भागीदारी के लिए किया जा सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Marketing" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
शुरुआत: बाजार व मार्केटिंग - {{ store_name }}

हेलो {{ name|default:'there' }},

अब जबकि {{ store_name }} आकार ले रहा है, तो ट्रैफिक बढ़ाने और आपकी बिक्री को बढ़ाने पर ध्यान केंद्रित करने का समय है। यहां पांच मार्केटिंग के सुझाव हैं जो आपको शुरुआत के लिए मदद कर सकते हैं।

1. अपना पहला डिस्काउंट कोड बनाएं
अपने पहले ग्राहकों को आकर्षित करने के लिए लॉन्च डिस्काउंट पेश करें। डिस्काउंट कोड बनाने के लिए मार्केटिंग > डिस्काउंट कोड जाएं और उपयोग की सीमा और अवधि के विकल्प के साथ प्रतिशत या निश्चित राशि के डिस्काउंट बनाएं।

2. छोड़े गए कार्ट के पुनर्प्राप्ति को सेट अप करें
खोए हुए बिक्री को स्वचालित रूप से पुनर्प्राप्त करें। मार्केटिंग > छोड़े गए कार्ट के तहत छोड़े गए कार्ट के पुनर्प्राप्ति ईमेल को एनेबल करें ताकि ग्राहकों को उन आइटम्स के बारे में याद दिलाया जा सके जो वे पीछे छोड़ गए।

3. अपने सोशल मीडिया अकाउंट को कनेक्ट करें
अपने सोशल मीडिया प्रोफाइल को अपने स्टोर से लिंक करें ताकि ग्राहक आपको ढूंढ सकें और फॉलो कर सकें। सेटिंग्स > सोशल मीडिया के तहत सोशल लिंक जोड़ें ताकि आपके स्टोर के फूटर में दिखाए जा सकें।

4. गूगल एनालिटिक्स ट्रैकिंग को सेट अप करें
जानें कि आपके आगंतुक कहां से आ रहे हैं और वे आपके स्टोर के साथ कैसे बर्ताव कर रहे हैं। सेटिंग्स > एनालिटिक्स के तहत अपने गूगल एनालिटिक्स ट्रैकिंग आईडी जोड़ें ताकि डेटा के संग्रह को शुरू किया जा सके।

5. एक न्यूज़लेटर साइनअप फॉर्म बनाएं
एक दिन से अपने ईमेल सूची को बनाएं। अपने स्टोर में एक न्यूज़लेटर साइनअप फॉर्म जोड़ें ताकि आगंतुक ईमेल एकत्र किए जा सकें। इन संपर्कों का उपयोग प्रोमोशन, उत्पाद लॉन्च और ग्राहक भागीदारी के लिए किया जा सके।

मार्केटिंग जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
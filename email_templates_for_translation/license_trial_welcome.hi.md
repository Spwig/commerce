---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
स्पविग में आपका स्वागत है - आपका {{ trial_days }}-दिन का मुफ्त परीक्षण

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          स्पविग में आपका स्वागत है!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          आपका {{ trial_days }}-दिन का मुफ्त परीक्षण तैयार है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text>
          {{ product_name }} के साथ आपका परीक्षण करने के लिए धन्यवाद! आपका परीक्षण सक्रिय कर दिया गया है और आपके पास {{ trial_days }} दिन हैं जिसमें आप स्पविग के सभी विशेषताओं का अनुसंधान कर सकते हैं{% if includes_pos %}, जिसमें हमारा पॉइंट ऑफ सेल (POS) सिस्टम भी शामिल है{% endif %}।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          आपका सेटअप टोकन
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          इस टोकन का उपयोग आपके परीक्षण स्टोर को सक्रिय करने के लिए स्थापना के दौरान करें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          शुरू करना
        </mj-text>
        <mj-text font-size="14px">
          1. हमारे सेटअप गाइड के अनुसार स्पविग को अपने सर्वर पर स्थापित करें
        </mj-text>
        <mj-text font-size="14px">
          2. स्थापना के दौरान प्रदर्शित होने पर अपना सेटअप टोकन दर्ज करें
        </mj-text>
        <mj-text font-size="14px">
          3. अपने ऑनलाइन स्टोर के निर्माण को शुरू करें!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          आपके परीक्षण में क्या शामिल है
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ trial_days }} दिन के लिए सभी मुख्य विशेषताओं के पूर्ण पहुंच
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          उत्पाद कैटलॉग, ऑर्डर और ग्राहक प्रबंधन
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          थीम कस्टमाइजेशन और पेज बिल्डर
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          भुगतान और डिलीवरी प्रदाता एंटीग्रेशन
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          पॉइंट ऑफ सेल (POS) सिस्टम
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          आपका परीक्षण {{ trial_days }} दिन में समाप्त हो जाएगा। जब आप तैयार हो जाएंगे, तो एक पूर्ण लाइसेंस में अपग्रेड करें ताकि आपके स्टोर को डेटा के बिना काम करते रह सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
स्पविग में आपका स्वागत है!
आपका {{ trial_days }}-दिन का मुफ्त परीक्षण तैयार है।

हेलो {{ customer_name }},

{{ product_name }} के साथ आपका परीक्षण करने के लिए धन्यवाद! आपका परीक्षण सक्रिय कर दिया गया है और आपके पास {{ trial_days }} दिन हैं जिसमें आप स्पविग के सभी विशेषताओं का अनुसंधान कर सकते हैं{% if includes_pos %}, जिसमें हमारा पॉइंट ऑफ सेल (POS) सिस्टम भी शामिल है{% endif %}।

आपका सेटअप टोकन:
{{ setup_token }}
इस टोकन का उपयोग आपके परीक्षण स्टोर को सक्रिय करने के लिए स्थापना के दौरान करें।

शुरू करना:
1. हमारे सेटअप गाइड के अनुसार स्पविग को अपने सर्वर पर स्थापित करें
2. स्थापना के दौरान प्रदर्शित होने पर अपना सेटअप टोकन दर्ज करें
3. अपने ऑनलाइन स्टोर के निर्माण को शुरू करें!

सेटअप गाइड देखें: {{ setup_url }}

आपके परीक्षण में क्या शामिल है:
- {{ trial_days }} दिन के लिए सभी मुख्य विशेषताओं के पूर्ण पहुंच
- उत्पाद कैटलॉग, ऑर्डर और ग्राहक प्रबंधन
- थीम कस्टमाइजेशन और पेज बिल्डर
- भुगतान और डिलीवरी प्रदाता एंटीग्रेशन
{% if includes_pos %}- पॉइंट ऑफ सेल (POS) सिस्टम{% endif %}

आपका परीक्षण {{ trial_days }} दिन में समाप्त हो जाएगा। जब आप तैयार हो जाएंगे, तो एक पूर्ण लाइसेंस में अपग्रेड करें ताकि आपके स्टोर को डेटा के बिना काम करते रह सके।

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
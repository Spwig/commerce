---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
आपका स्टोर तैयार है - {{ store_name }}

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
          आपका स्टोर लाइव है!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} आपके लिए तैयार है
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
          अच्छी खबर! आपका Spwig स्टोर <strong>{{ store_name }}</strong> तैयार कर दिया गया है और अब लाइव है। आप तुरंत अपने उत्पादों, ब्रैंडिंग और भुगतान विधियों को सेट कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          आपका स्टोर विवरण
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          स्टोर URL: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          एडमिन पैनल: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          क्षेत्र: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          त्वरित शुरुआत
        </mj-text>
        <mj-text font-size="14px">
          1. चेकआउट के दौरान आप द्वारा सेट किए गए ईमेल और पासवर्ड का उपयोग करके अपने एडमिन पैनल में लॉग इन करें
        </mj-text>
        <mj-text font-size="14px">
          2. डिज़ाइन > थीम सेटिंग्स के तहत अपने स्टोर लोगो और ब्रैंडिंग जोड़ें
        </mj-text>
        <mj-text font-size="14px">
          3. कैटलॉग > उत्पादों के तहत अपने पहले उत्पाद जोड़ें
        </mj-text>
        <mj-text font-size="14px">
          4. सेटिंग्स > भुगतान प्रदाताओं के तहत एक भुगतान प्रदाता सेट करें
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
आपका स्टोर लाइव है!

{{ store_name }} आपके लिए तैयार है।

हेलो {{ name|default:'there' }},

अच्छी खबर! आपका Spwig स्टोर {{ store_name }} तैयार कर दिया गया है और अब लाइव है। आप तुरंत अपने उत्पादों, ब्रैंडिंग और भुगतान विधियों को सेट कर सकते हैं।

आपका स्टोर विवरण:
- स्टोर URL: {{ store_url }}
- एडमिन पैनल: {{ admin_url }}
- क्षेत्र: {{ region }}

त्वरित शुरुआत:
1. चेकआउट के दौरान आप द्वारा सेट किए गए ईमेल और पासवर्ड का उपयोग करके अपने एडमिन पैनल में लॉग इन करें
2. डिज़ाइन > थीम सेटिंग्स के तहत अपने स्टोर लोगो और ब्रैंडिंग जोड़ें
3. कैटलॉग > उत्पादों के तहत अपने पहले उत्पाद जोड़ें
4. सेटिंग्स > भुगतान प्रदाताओं के तहत एक भुगतान प्रदाता सेट करें

एडमिन पैनल जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
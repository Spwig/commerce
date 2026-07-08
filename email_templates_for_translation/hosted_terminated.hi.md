---
template_type: hosted_terminated
category: License
---

# Email Template: hosted_terminated

## Subject
स्टोर हटा दिया गया - {{ store_name }}

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
    <mj-section background-color="#374151" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          स्टोर हटा दिया गया
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          आपका स्टोर <strong>{{ store_name }}</strong> स्थायी रूप से हटा दिया गया है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Data Backup Info -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          डेटा बैकअप
        </mj-text>
        <mj-text font-size="14px">
          आपके डेटा का एक बैकअप 90 दिनों के लिए अनुरोध के बाद उपलब्ध रहेगा। यदि आपको डेटा एग्जपोर्ट की आवश्यकता है, तो <strong>support@spwig.com</strong> पर संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Thank You -->
    <mj-section>
      <mj-column>
        <mj-text>
          Spwig के एक ग्राहक बने रहने के लिए धन्यवाद। हम आशा करते हैं कि भविष्य में आपको फिर से देखेंगे।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
स्टोर हटा दिया गया - {{ store_name }}

हेलो {{ name|default:'there' }},

आपका स्टोर {{ store_name }} स्थायी रूप से हटा दिया गया है।

डेटा बैकअप:
आपके डेटा का एक बैकअप 90 दिनों के लिए अनुरोध के बाद उपलब्ध रहेगा। यदि आपको डेटा एग्जपोर्ट की आवश्यकता है, तो support@spwig.com पर संपर्क करें।

Spwig के एक ग्राहक बने रहने के लिए धन्यवाद। हम आशा करते हैं कि भविष्य में आपको फिर से देखेंगे।

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
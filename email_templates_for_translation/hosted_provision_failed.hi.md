---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
कार्रवाई की आवश्यकता - {{ store_name }} के लिए स्टोर सेटअप समस्या

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          स्टोर सेटअप समस्या
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
          हमने आपके स्टोर <strong>{{ store_name }}</strong> के सेटअप के दौरान एक समस्या का सामना किया। हमारी टीम को सूचना दी गई है और इस पर विचार कर रही है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          क्या हुआ
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          अगला क्या होगा?
        </mj-text>
        <mj-text font-size="14px">
          हमारी समर्थन टीम को इस समस्या के बारे में स्वचालित रूप से सूचना दी गई है। आपको कोई कार्रवाई करने की आवश्यकता नहीं है - हम आपसे समस्या के समाधान के बाद संपर्क करेंगे।
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          अगर आपके पास इस बीच कोई प्रश्न है, तो कृपया हमसे संपर्क करने में जरा भी संकोच न करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
स्टोर सेटअप समस्या - {{ store_name }}

हेलो {{ name|default:'there' }},

हमने आपके स्टोर {{ store_name }} के सेटअप के दौरान एक समस्या का सामना किया। हमारी टीम को सूचना दी गई है और इस पर विचार कर रही है।

क्या हुआ:
{{ provision_error }}

अगला क्या होगा?
हमारी समर्थन टीम को इस समस्या के बारे में स्वचालित रूप से सूचना दी गई है। आपको कोई कार्रवाई करने की आवश्यकता नहीं है - हम आपसे समस्या के समाधान के बाद संपर्क करेंगे।

अगर आपके पास इस बीच कोई प्रश्न है, तो कृपया हमसे संपर्क करने में जरा भी संकोच न करें।

सहायता की आवश्यकता है? {{ support_email }} पर संपर्क करें।
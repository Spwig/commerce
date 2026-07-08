---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
भुगतान विफल - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          भुगतान समस्या
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} के लिए कार्रवाई आवश्यक है
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
          हम आपके लिए <strong>{{ plan_name }}</strong> के भुगतान को प्रक्रिया नहीं कर सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          भुगतान विवरण
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          राशि: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          योजना: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}। किसी भी सेवा बाधा को रोकने के लिए, कृपया अपनी भुगतान विधि को अपडेट करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
भुगतान समस्या - {{ store_name }}

हैलो {{ name|default:'there' }},

हम आपके लिए {{ plan_name }} के भुगतान को प्रक्रिया नहीं कर सके।

भुगतान विवरण:
- राशि: {{ currency }}{{ amount }}
- योजना: {{ plan_name }}

{{ retry_info }}। किसी भी सेवा बाधा को रोकने के लिए, कृपया अपनी भुगतान विधि को अपडेट करें।

भुगतान विधि अपडेट करें: https://spwig.com/account

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
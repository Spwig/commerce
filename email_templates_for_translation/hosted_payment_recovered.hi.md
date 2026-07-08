---
template_type: hosted_payment_recovered
category: License
---

# Email Template: hosted_payment_recovered

## Subject
भुगतान सफल - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          भुगतान सफल
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
          अच्छी खबर! आपका {{ plan_name }} के लिए {{ currency }}{{ amount }} का भुगतान सफलतापूर्वक प्रक्रिया कर लिया गया है। आपका सदस्यता अविच्छिन्न रहता है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
भुगतान सफल - {{ store_name }}

हेलो {{ name|default:'there' }},

अच्छी खबर! आपका {{ plan_name }} के लिए {{ currency }}{{ amount }} का भुगतान सफलतापूर्वक प्रक्रिया कर लिया गया है। आपका सदस्यता अविच्छिन्न रहता है।

आपके स्टोर तक जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
रद्द कर दिया गया - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          रद्द कर दिया गया
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
          आपका <strong>{{ plan_name }}</strong> सदस्यता रद्द कर दी गई है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          अगला क्या होता है
        </mj-text>
        <mj-text font-size="14px">
          आपके पास अभी तक <strong>{{ access_until_date }}</strong> तक पूर्ण पहुँच बनी रहेगी।
        </mj-text>
        <mj-text font-size="14px">
          उसके बाद, आपके स्टोर डेटा 30 दिनों तक <strong>{{ termination_date }}</strong> तक सुरक्षित रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          यदि आप अपने डेटा को पहुँच समाप्त होने से पहले निर्यत करना चाहते हैं, तो आप अपने प्रशासन पैनल से ऐसा कर सकते हैं। मन बदल गया? आप कभी भी अपनी सदस्यता को पुनः सक्रिय कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="सदस्यता पुनः सक्रिय करें" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
रद्द कर दिया गया - {{ store_name }}

हेलो {{ name|default:'there' }},

आपका {{ plan_name }} सदस्यता रद्द कर दी गई है।

अगला क्या होता है:
- आपके पास अभी तक {{ access_until_date }} तक पूर्ण पहुँच बनी रहेगी।
- उसके बाद, आपके स्टोर डेटा 30 दिनों तक {{ termination_date }} तक सुरक्षित रहेगा।

यदि आप अपने डेटा को पहुँच समाप्त होने से पहले निर्यत करना चाहते हैं, तो आप अपने प्रशासन पैनल से ऐसा कर सकते हैं। मन बदल गया? आप कभी भी अपनी सदस्यता को पुनः सक्रिय कर सकते हैं।

सदस्यता पुनः सक्रिय करें: https://spwig.com/account

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
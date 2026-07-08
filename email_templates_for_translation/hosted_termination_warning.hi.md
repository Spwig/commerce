---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
महत्वपूर्ण: 7 दिनों में डेटा हटा दिया जाएगा - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          डेटा हटाने की चेतावनी
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
          आपका स्टोर <strong>{{ store_name }}</strong> और सभी संबंधित डेटा <strong>{{ termination_date }}</strong> के दिन स्थायी रूप से हटा दिया जाएगा। यह कार्रवाई वापस नहीं की जा सकती।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          आप क्या कर सकते हैं
        </mj-text>
        <mj-text font-size="14px">
          अगर आप अपने डेटा को बचाना चाहते हैं, तो कृपया इस तारीख से पहले इसे एक्सपोर्ट करें या अपने सब्सक्रिप्शन को पुनः सक्रिय करें ताकि डेटा हटाया न जा सके।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
डेटा हटाने की चेतावनी - {{ store_name }}

हेलो {{ name|default:'there' }},

आपका स्टोर {{ store_name }} और सभी संबंधित डेटा {{ termination_date }} के दिन स्थायी रूप से हटा दिया जाएगा। यह कार्रवाई वापस नहीं की जा सकती।

आप क्या कर सकते हैं:
अगर आप अपने डेटा को बचाना चाहते हैं, तो कृपया इस तारीख से पहले इसे एक्सपोर्ट करें या अपने सब्सक्रिप्शन को पुनः सक्रिय करें ताकि डेटा हटाया न जा सके।

सब्सक्रिप्शन पुनः सक्रिय करें: https://spwig.com/account

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
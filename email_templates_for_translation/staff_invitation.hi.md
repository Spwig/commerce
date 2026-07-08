---
template_type: staff_invitation
category: Core E-commerce
---

# Email Template: staff_invitation

## Subject
आपके लिए {{ store_name }} में शामिल होने के लिए आमंत्रण है

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
          Staff Invitation
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          आपके लिए {{ store_name }} में शामिल होने के लिए आमंत्रण है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हेलो {{ first_name }},
        </mj-text>
        <mj-text>
          {{ invited_by }} ने आपको {{ store_name }} में स्टाफ के रूप में शामिल होने के लिए आमंत्रित किया है। आप प्रशासन डैशबोर्ड से स्टोर के प्रबंधन में मदद कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=invitation_url text="Accept Invitation" %}

    <!-- Expiry Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          यह आमंत्रण {{ expires_at|date:"N j, Y" }} तक वैध रहेगा। यदि आप इस आमंत्रण की उम्मीद नहीं कर रहे हैं, तो आप इस ईमेल को अनदेखा कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
आपके लिए {{ store_name }} में शामिल होने के लिए आमंत्रण है

हेलो {{ first_name }},

{{ invited_by }} ने आपको {{ store_name }} में स्टाफ के रूप में शामिल होने के लिए आमंत्रित किया है। आप प्रशासन डैशबोर्ड से स्टोर के प्रबंधन में मदद कर सकते हैं।

आमंत्रन स्वीकृत करें: {{ invitation_url }}

यह आमंत्रण {{ expires_at|date:"N j, Y" }} तक वैध रहेगा। यदि आप इस आमंत्रण की उम्मीद नहीं कर रहे हैं, तो आप इस ईमेल को अनदेखा कर सकते हैं।

मदद की आवश्यकता है? {{ support_email }} संपर्क करें
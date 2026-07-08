---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
सदस्यता पुष्टि - {{ store_name }}

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
          सदस्यता पुष्टि!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Spwig में आपका स्वागत है
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
          सदस्यता लेने के लिए धन्यवाद! आपकी <strong>{{ plan_name }}</strong> योजना के लिए <strong>{{ store_name }}</strong> की पुष्टि कर दी गई है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          योजना विवरण
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          योजना: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          बिलिंग अंतराल: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          राशि: {{ currency }}{{ amount }}{% if intro_period %} (परिचय दर){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          आपकी परिचय दर {{ intro_period }} के लिए लागू होती है। उसके बाद, आपकी योजना {{ currency }}{{ full_amount }}/{{ billing_interval }} पर नवीनीकृत होगी।
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          आपका स्टोर अब तैयार किया जा रहा है और जब तैयार हो जाएगा तो आपको एक अन्य ईमेल मिलेगा।
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          अगला बिलिंग तिथि: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
सदस्यता पुष्टि!

हेलो {{ name|default:'there' }},

सदस्यता लेने के लिए धन्यवाद! आपकी {{ plan_name }} योजना के लिए {{ store_name }} की पुष्टि कर दी गई है।

योजना विवरण:
- योजना: {{ plan_name }}
- बिलिंग अंतराल: {{ billing_interval }}
- राशि: {{ currency }}{{ amount }}{% if intro_period %} (परिचय दर){% endif %}
{% if intro_period %}
यह आपकी परिचय दर {{ intro_period }} के लिए है। उसके बाद, आपकी योजना {{ currency }}{{ full_amount }}/{{ billing_interval }} पर नवीनीकृत होगी।
{% endif %}
आपका स्टोर अब तैयार किया जा रहा है और जब तैयार हो जाएगा तो आपको एक अन्य ईमेल मिलेगा।

अगला बिलिंग तिथि: {{ next_billing_date }}

मदद की आवश्यकता है? {{ support_email }} संपर्क करें
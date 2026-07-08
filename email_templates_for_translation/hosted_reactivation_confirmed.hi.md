---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
वापस आओ! {{ store_name }} फिर से सक्रिय है

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
          वापस आओ!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} फिर से सक्रिय है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          हैलो,
        </mj-text>
        <mj-text>
          अच्छी खबर! आपका <strong>{{ store_name }}</strong> स्टोर फिर से सक्रिय कर दिया गया है। आपका <strong>{{ plan_name }}</strong> सब्सक्रिप्शन अब सक्रिय है और आपका स्टोर ऑनलाइन वापस आ रहा है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          सक्रियता के विवरण
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          योजना: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          भुगतान प्रक्रिया: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          अगला बिलिंग तिथि: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          आपका स्टोर अब ऑनलाइन वापस आ रहा है। सभी चीजें पूरी तरह से बहाल होने में कुछ मिनट लग सकते हैं। जब लाइव हो जाएगा, तो आपका स्टोर {{ store_url }} पर एक्सेस कर सकते हैं।
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
वापस आओ! {{ store_name }} फिर से सक्रिय है

हैलो,

अच्छी खबर! आपका {{ store_name }} स्टोर फिर से सक्रिय कर दिया गया है। आपका {{ plan_name }} सब्सक्रिप्शन अब सक्रिय है और आपका स्टोर ऑनलाइन वापस आ रहा है।

सक्रियता के विवरण:
- योजना: {{ plan_name }}
- भुगतान प्रक्रिया: {{ currency }}{{ amount }}
- अगला बिलिंग तिथि: {{ next_billing_date }}

आपका स्टोर अब ऑनलाइन वापस आ रहा है। सभी चीजें पूरी तरह से बहाल होने में कुछ मिनट लग सकते हैं। जब लाइव हो जाएगा, तो आपका स्टोर {{ store_url }} पर एक्सेस कर सकते हैं।

आपके स्टोर तक जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} पर संपर्क करें
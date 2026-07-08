---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
रद्दीकरण वापसी - {{ store_name }}

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
          रद्दीकरण वापसी
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
          हाय,
        </mj-text>
        <mj-text>
          {{ store_name }} के आपके रद्दीकरण अनुरोध को वापस कर दिया गया है। आपका <strong>{{ plan_name }}</strong> सदस्यता सामान्य रूप से जारी रहेगा - आपकी ओर से कोई कार्रवाई आवश्यक नहीं है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          सदस्यता विवरण
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          योजना: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          अगला बिलिंग तिथि: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          आपका स्टोर सामान्य रूप से संचालित रहता है। बिलिंग ऊपर दिखाए गए तिथि पर जारी रहेगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
रद्दीकरण वापसी - {{ store_name }}

हाय,

{{ store_name }} के आपके रद्दीकरण अनुरोध को वापस कर दिया गया है। आपका {{ plan_name }} सदस्यता सामान्य रूप से जारी रहेगा — आपकी ओर से कोई कार्रवाई आवश्यक नहीं है।

सदस्यता विवरण:
- योजना: {{ plan_name }}
- अगला बिलिंग तिथि: {{ next_billing_date }}

आपका स्टोर सामान्य रूप से संचालित रहता है। बिलिंग ऊपर दिखाए गए तिथि पर जारी रहेगा।

{% if admin_url %}Go to Your Store: {{ admin_url }}

{% endif %}Need help? Contact {{ support_email }}
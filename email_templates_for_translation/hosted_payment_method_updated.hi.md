---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
भुगतान विधि अपडेट करें - {{ store_name }}

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
          भुगतान विधि अपडेट करें
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
          आपके <strong>{{ plan_name }}</strong> प्लान के लिए <strong>{{ store_name }}</strong> पर भुगतान विधि सफलतापूर्वक अपडेट कर दी गई है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          इस परिवर्तन को आपने नहीं किया?
        </mj-text>
        <mj-text font-size="14px">
          यदि आपने अपनी भुगतान विधि को अपडेट नहीं किया है, तो कृपया तुरंत हमारी समर्थन टीम से संपर्क करें ताकि हम आपके खाते को सुरक्षित कर सकें।
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
भुगतान विधि अपडेट करें - {{ store_name }}

हाय,

आपके {{ plan_name }} प्लान के लिए {{ store_name }} पर भुगतान विधि सफलतापूर्वक अपडेट कर दी गई है।

इस परिवर्तन को आपने नहीं किया?
यदि आपने अपनी भुगतान विधि को अपडेट नहीं किया है, तो कृपया तुरंत हमारी समर्थन टीम से संपर्क करें ताकि हम आपके खाते को सुरक्षित कर सकें।

आपके स्टोर तक जाएं: {{ admin_url }}

मदद की आवश्यकता है? {{ support_email }} से संपर्क करें
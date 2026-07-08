---
template_type: review_request
category: Enhanced E-commerce
---

# Email Template: review_request

## Subject
आपकी खरीदारी कैसी रही? अपना समीक्षा छोड़े

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          हम आपकी प्रतिक्रिया के लिए उत्सुक हैं!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आर्डर #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" line-height="1.8">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="10px" line-height="1.8">
          हम उम्मीत करते हैं कि आप अपनी हालिया खरीदारी का आनंद ले रहे हैं! आपकी प्रतिक्रिया हमारी सुधार में मदद करती है और अन्य ग्राहकों को जानकार निर्णय लेने में मदद करती है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Products to Review -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          अपनी खरीदारी की समीक्षा करें
        </mj-text>
      </mj-column>
    </mj-section>

    {% for item in items %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px" css-class="review-item">
      <mj-column width="100px">
        <mj-image src="{{ item.product_thumbnail_url }}" alt="{{ item.name }}" width="80px" border-radius="6px" />
      </mj-column>
      <mj-column width="60%" vertical-align="middle">
        <mj-text font-size="14px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ item.name }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px">
          Qty: {{ item.quantity }}
        </mj-text>
      </mj-column>
      <mj-column width="30%" vertical-align="middle">
        <mj-button
          href="{{ item.review_url }}"
          background-color="{{ theme.color.primary|default:'#2563eb' }}"
          color="{{ theme.color.background|default:'#ffffff' }}"
          font-size="12px"
          border-radius="4px"
          padding="8px 16px"
          inner-padding="8px 16px"
        >
          समीक्षा लिखें
        </mj-button>
      </mj-column>
    </mj-section>
    {% endfor %}

    <!-- Incentive (if offered) -->
    {% if incentive_offered %}
    <mj-section background-color="{{ theme.color.info_light|default:'#dbeafe' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" font-weight="600" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎁 बोनस पुरस्कार
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-top="10px">
          {{ incentive_details }}
        </mj-text>
        {% if incentive_code %}
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" padding-top="10px">
          कोड: {{ incentive_code }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Block -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
हम आपकी प्रतिक्रिया के लिए उत्सुक हैं!

आर्डर #{{ order_number }}

हेलो {{ customer_name }},

हम उम्मीत करते हैं कि आप अपनी हालिया खरीदारी का आनंद ले रहे हैं! आपकी प्रतिक्रिया हमारी सुधार में मदद करती है और अन्य ग्राहकों को जानकार निर्णय लेने में मदद करती है।

अपनी खरीदारी की समीक्षा करें:
{% for item in items %}
- {{ item.name }} (Qty: {{ item.quantity }})
  समीक्षा लिखें: {{ item.review_url }}
{% endfor %}

{% if incentive_offered %}
🎁 बोनस पुरस्कार
{{ incentive_details }}
{% if incentive_code %}कोड: {{ incentive_code }}{% endif %}
{% endif %}

मदद की आवश्यकता है?
ईमेल: {{ support_email }}
फोन: {{ support_phone }}
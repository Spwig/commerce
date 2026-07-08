---
template_type: order_cancelled
category: Core E-commerce
---

# Email Template: order_cancelled

## Subject
आपका ऑर्डर #{{ order_number }} रद्द कर दिया गया है

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ऑर्डर रद्द कर दिया गया है
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपका ऑर्डर <strong>#{{ order_number }}</strong> रद्द कर दिया गया है।
        </mj-text>

        {% if cancellation_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कारण:</strong> {{ cancellation_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          यदि कोई भुगतान किया गया है, तो वापसी के अनुसार मूल भुगतान विधि के अनुसार रिफंड प्रक्रिया कर दिया जाएगा।
        </mj-text>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ऑर्डर विवरण देखें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ऑर्डर रद्द कर दिया गया है

हेलो {{ customer_name }},

आपका ऑर्डर #{{ order_number }} रद्द कर दिया गया है।

{% if cancellation_reason %}कारण: {{ cancellation_reason }}{% endif %}

यदि कोई भुगतान किया गया है, तो वापसी के अनुसार मूल भुगतान विधि के अनुसार रिफंड प्रक्रिया कर दिया जाएगा।

{% if order_url %}ऑर्डर विवरण देखें: {{ order_url }}{% endif %}

इस रद्द के बारे में प्रश्न?
ईमेल: {{ support_email }}
फोन: {{ support_phone }}
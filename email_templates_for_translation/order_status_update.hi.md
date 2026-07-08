---
template_type: order_status_update
category: Core E-commerce
---

# Email Template: order_status_update

## Subject
आदेश #{{ order_number }} - स्थिति अपडेट: {{ new_status_display }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आदेश स्थिति अपडेट
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#6b7280' }}">
          आदेश #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके आदेश <strong>#{{ order_number }}</strong> की स्थिति अपडेट कर दी गई है।
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>पुरानी स्थिति:</strong> {{ old_status_display }}<br/>
              <strong>नई स्थिति:</strong> {{ new_status_display }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          आदेश विवरण देखें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आदेश स्थिति अपडेट - आदेश #{{ order_number }}

हेलो {{ customer_name }},

आपके आदेश #{{ order_number }} की स्थिति अपडेट कर दी गई है।

पुरानी स्थिति: {{ old_status_display }}
नई स्थिति: {{ new_status_display }}

{% if order_url %}आदेश विवरण देखें: {{ order_url }}{% endif %}
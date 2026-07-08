---
template_type: order_note_notification
category: Core E-commerce
---

# Email Template: order_note_notification

## Subject
आपके ऑर्डर #{{ order_number }} के बारे में अपडेट

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          आपके ऑर्डर के बारे में एक संदेश
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ staff_name }} ने आपके ऑर्डर <strong>#{{ order_number }}</strong> में एक नोट जोड़ा है:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ note_content }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        {% if order_url %}
        <mj-button href="{{ order_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ऑर्डर देखें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपके ऑर्डर के बारे में एक संदेश

हेलो {{ customer_name }},

{{ staff_name }} ने आपके ऑर्डर #{{ order_number }} में एक नोट जोड़ा है:

---
{{ note_content }}
---

{% if order_url %}ऑर्डर देखें: {{ order_url }}{% endif %}

मदद की आवश्यकता है?
ईमेल: {{ support_email }}
फोन: {{ support_phone }}
---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
वितरण अपवाद - आदेश #{{ order_number }} के लिए ध्यान दें

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ वितरण अपवाद
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हेलो {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हम आपके वितरण के साथ एक अपवाद के बारे में आपको सूचित कर रहे हैं। हम इस समस्या को जल्द से जल्द ठीक करने के लिए काम कर रहे हैं।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              अपवाद विवरण:
            </mj-text>
            <mj-text color="#92400e">
              <strong>अपवाद प्रकार:</strong> {{ exception_type }}<br/>
              <strong>विवरण:</strong> {{ exception_description }}<br/>
              <strong>हुआ:</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              आदेश जानकारी:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>आदेश संख्या:</strong> {{ order_number }}<br/>
              <strong>ट्रैकिंग संख्या:</strong> {{ tracking_number }}<br/>
              <strong>वाहक:</strong> {{ carrier_name }}<br/>
              <strong>वर्तमान स्थान:</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अगला क्या होगा?
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ कार्रवाई आवश्यक:
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          अपना आदेश ट्रैक करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          समर्थन से संपर्क करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ वितरण अपवाद

हेलो {{ customer_name }},

हम आपके वितरण के साथ एक अपवाद के बारे में आपको सूचित कर रहे हैं। हम इस समस्या को जल्द से जल्द ठीक करने के लिए काम कर रहे हैं।

अपवाद विवरण:
- अपवाद प्रकार: {{ exception_type }}
- विवरण: {{ exception_description }}
- हुआ: {{ exception_date }}

आदेश जानकारी:
- आदेश संख्या: {{ order_number }}
- ट्रैकिंग संख्या: {{ tracking_number }}
- वाहक: {{ carrier_name }}
- वर्तमान स्थान: {{ current_location }}

अगला क्या होगा?
{{ resolution_steps }}

{% if action_required %}
⚠️ कार्रवाई आवश्यक:
{{ action_required_description }}
{% endif %}

अपना आदेश ट्रैक करें: {{ tracking_url }}
समर्थन से संपर्क करें: {{ support_url }}
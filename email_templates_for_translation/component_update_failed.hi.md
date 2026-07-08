---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ अपडेट विफल: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ अपडेट विफल
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          इंस्टॉलेशन त्रुटि
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} के लिए अपडेट संस्करण {{ target_version }} को इंस्टॉल करने में विफल रहा।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              विफलता विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>एप्लिकेशन:</strong> {{ component_name }}<br/>
              <strong>लक्ष्य संस्करण:</strong> {{ target_version }}<br/>
              <strong>विफल हुआ:</strong> {{ failed_at }}<br/>
              <strong>त्रुटि कोड:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          त्रुटि संदेश:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>पूरा त्रुटि लॉग:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          क्या करें:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. प्रणाली आवश्यकताओं और निर्भरताओं की जांच करें<br/>
          2. विवरण के लिए त्रुटि लॉग की जांच करें<br/>
          3. पुनः इंस्टॉल करने की कोशिश करें, या समर्थन से संपर्क करें<br/>
          4. आपकी दुकान अभी भी {{ current_version }} पर चल रही है
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पुनः इंस्टॉल करें
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
❌ अपडेट विफल

इंस्टॉलेशन त्रुटि

{{ component_name }} के लिए अपडेट संस्करण {{ target_version }} को इंस्टॉल करने में विफल रहा।

विफलता विवरण:
- एप्लिकेशन: {{ component_name }}
- लक्ष्य संस्करण: {{ target_version }}
- विफल हुआ: {{ failed_at }}
- त्रुटि कोड: {{ error_code }}

त्रुटि संदेश:
{{ error_message }}

{% if error_log %}
पूरा त्रुटि लॉग:
{{ error_log|truncatewords:50 }}
{% endif %}

क्या करें:
1. प्रणाली आवश्यकताओं और निर्भरताओं की जांच करें
2. विवरण के लिए त्रुटि लॉग की जांच करें
3. पुनः इंस्टॉल करने की कोशिश करें, या समर्थन से संपर्क करें
4. आपकी दुकान अभी भी {{ current_version }} पर चल रही है

पुनः इंस्टॉल करें: {{ retry_url }}
समर्थन से संपर्क करें: {{ support_url }}
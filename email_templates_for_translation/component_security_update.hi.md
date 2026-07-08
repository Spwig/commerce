---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 तत्काल: {{ component_name }} के लिए सुरक्षा अपडेट उपलब्ध है

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 सुरक्षा अपडेट आवश्यक है
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          महत्वपूर्ण सुरक्षा पैच
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} में एक सुरक्षा दुर्बलता पाई गई है। अपने स्टोर की रक्षा के लिए तत्काल अपडेट करें।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ सुरक्षा जानकारी
            </mj-text>
            <mj-text color="#991b1b">
              <strong>संघटक:</strong> {{ component_name }}<br/>
              <strong>वर्तमान संस्करण:</strong> {{ current_version }}<br/>
              <strong>पैच किया गया संस्करण:</strong> {{ patched_version }}<br/>
              <strong>गंभीरता:</strong> {{ severity_level }}<br/>
              <strong>CVE आईडी:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          दुर्बलता का विवरण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          संभावित प्रभाव:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              अस्थायी सुरक्षा उपाय
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          कार्रवाई की आवश्यकता: तत्काल अपडेट स्थापित करें
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          सुरक्षा पैच स्थापित करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          सुरक्षा सलाह पढ़ें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          यदि आपको सहायता की आवश्यकता है, तो तत्काल Spwig समर्थन से संपर्क करें।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 सुरक्षा अपडेट आवश्यक है

महत्वपूर्ण सुरक्षा पैच

{{ component_name }} में एक सुरक्षा दुर्बलता पाई गई है। अपने स्टोर की रक्षा के लिए तत्काल अपडेट करें।

⚠️ सुरक्षा जानकारी:
- संघटक: {{ component_name }}
- वर्तमान संस्करण: {{ current_version }}
- पैच किया गया संस्करण: {{ patched_version }}
- गंभीरता: {{ severity_level }}
- CVE आईडी: {{ cve_id }}

दुर्बलता का विवरण:
{{ vulnerability_description }}

संभावित प्रभाव:
{{ impact_description }}

{% if mitigation_steps %}
अस्थायी सुरक्षा उपाय:
{{ mitigation_steps }}
{% endif %}

कार्रवाई की आवश्यकता: तत्काल अपडेट स्थापित करें

सुरक्षा पैच स्थापित करें: {{ update_url }}
सुरक्षा सलाह पढ़ें: {{ advisory_url }}

यदि आपको सहायता की आवश्यकता है, तो तत्काल Spwig समर्थन से संपर्क करें।
---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 गंभीर चेतावनी: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 गंभीर प्रणाली चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          तत्काल ध्यान आवश्यक
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपकी Spwig स्थापना पर एक गंभीर प्रणाली स्वास्थ्य समस्या का पता लगाया गया है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 गंभीर समस्या
            </mj-text>
            <mj-text color="#991b1b">
              <strong>मेट्रिक:</strong> {{ metric_name }}<br/>
              <strong>वर्तमान मान:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>गंभीर सीमा:</strong> {{ critical_threshold }}<br/>
              <strong>पता लगाया गया:</strong> {{ detected_at }}<br/>
              <strong>गंभीरता:</strong> गंभीर
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          प्रभाव:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          तत्काल कार्रवाई आवश्यक:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          लक्ष्य:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ सेवा कमी चेतावनी
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              यह समस्या सेवा बाधा या प्रदर्शन कमी का कारण बन सकती है। ग्राहक प्रभाव को रोकने के लिए तत्काल समाधान करें।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          प्रणाली डैशबोर्ड देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          प्रणाली लॉग देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 गंभीर प्रणाली चेतावनी

तत्काल ध्यान आवश्यक

आपकी Spwig स्थापना पर एक गंभीर प्रणाली स्वास्थ्य समस्या का पता लगाया गया है।

🚨 गंभीर समस्या:
- मेट्रिक: {{ metric_name }}
- वर्तमान मान: {{ current_value }}
- गंभीर सीमा: {{ critical_threshold }}
- पता लगाया गया: {{ detected_at }}
- गंभीरता: गंभीर

प्रभाव:
{{ impact_description }}

तत्काल कार्रवाई आवश्यक:
{{ recommended_actions }}

{% if trend_data %}
लक्ष्य:
{{ trend_data }}
{% endif %}

⚠️ सेवा कमी चेतावनी:
यह समस्या सेवा बाधा या प्रदर्शन कमी का कारण बन सकती है। ग्राहक प्रभाव को रोकने के लिए तत्काल समाधान करें।

प्रणाली डैशबोर्ड देखें: {{ dashboard_url }}
प्रणाली लॉग देखें: {{ logs_url }}
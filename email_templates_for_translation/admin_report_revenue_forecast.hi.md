---
template_type: admin_report_revenue_forecast
category: Admin Reports
---

# Email Template: admin_report_revenue_forecast

## Subject
📈 राजस्व पूर्वानुमान - {{ forecast_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 राजस्व पूर्वानुमान
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          प्रदर्शित किया गया प्रदर्शन
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>पूर्वानुमान अवधि:</strong> {{ forecast_period }}<br/>
              <strong>प्रदर्शित राजस्व:</strong> <span style="font-size: 20px; color: #059669;">{{ projected_revenue }}</span><br/>
              <strong>वर्तमान ट्रेंड:</strong> {{ trend_direction }}<br/>
              <strong>विश्वास:</strong> {{ confidence_level }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          विश्लेषण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ analysis }}
        </mj-text>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अनुशंसाएं:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          विस्तृत पूर्वानुमान देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 राजस्व पूर्वानुमान

प्रदर्शित किया गया प्रदर्शन

पूर्वानुमान:
- पूर्वानुमान अवधि: {{ forecast_period }}
- प्रदर्शित राजस्व: {{ projected_revenue }}
- वर्तमान ट्रेंड: {{ trend_direction }}
- विश्वास: {{ confidence_level }}%

विश्लेषण:
{{ analysis }}

{% if recommendations %}
अनुशंसाएं:
{{ recommendations }}
{% endif %}

विस्तृत पूर्वानुमान देखें: {{ full_report_url }}
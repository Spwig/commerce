---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ कार्यक्षमता में गिरावट पाई गई - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ कार्यक्षमता में गिरावट
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          स्लो रिस्पॉन्स टाइम डिटेक्टेड
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके Spwig इंस्टॉलेशन में कार्यक्षमता में गिरावट हो रही है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              कार्यक्षमता समस्या:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>प्रभावित क्षेत्र:</strong> {{ affected_area }}<br/>
              <strong>वर्तमान रिस्पॉन्स समय:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>सामान्य रिस्पॉन्स समय:</strong> {{ normal_response_time }}ms<br/>
              <strong>गिरावट:</strong> {{ degradation_percentage }}% धीमा<br/>
              <strong>डिटेक्ट किया गया:</strong> {{ detected_at }}
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
          संभावित कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सबसे धीमा एंडपॉइंट:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} अनुरोध)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          प्रदर्शन डैशबोर्ड देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          धीमे प्रश्नों की जांच करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          हम आपको सामान्य कार्यक्षमता पर वापस आने पर सूचना देंगे।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ कार्यक्षमता में गिरावट 

स्लो रिस्पॉन्स टाइम डिटेक्टेड 

आपके Spwig इंस्टॉलेशन में कार्यक्षमता में गिरावट हो रही है।

कार्यक्षमता समस्या:
- प्रभावित क्षेत्र: {{ affected_area }}
- वर्तमान रिस्पॉन्स समय: {{ current_response_time }}ms
- सामान्य रिस्पॉन्स समय: {{ normal_response_time }}ms
- गिरावट: {{ degradation_percentage }}% धीमा
- डिटेक्ट किया गया: {{ detected_at }}

प्रभाव:
{{ impact_description }}

संभावित कारण:
{{ possible_causes }}

सबसे धीमा एंडपॉइंट:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} अनुरोध)
{% endfor %}

सिफारिश की गई कार्रवाई:
{{ recommended_actions }}

प्रदर्शन डैशबोर्ड देखें: {{ performance_dashboard_url }}
धीमे प्रश्नों की जांच करें: {{ slow_queries_url }}

हम आपको सामान्य कार्यक्षमता पर वापस आने पर सूचना देंगे।
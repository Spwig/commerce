---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ {{ feed_name }} के {{ platform_name }} पर सिंक करने में विफल

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ सिंक विफल
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिंक त्रुटि
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ feed_name }} के {{ platform_name }} पर सिंक करने में विफल।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              विफलता के विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • अमान्य API योग्यता या अतीत के टोकन<br/>
          • नेटवर्क कनेक्टिविटी समस्या<br/>
          • प्लेटफॉर्म API दर सीमा को पार कर दिया गया<br/>
          • फीड प्रारूप प्लेटफॉर्म आवश्यकताओं को पूरा नहीं करता है
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              सिफारिश की गई कार्रवाई
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          दुबारा सिंक करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          फीड सेटिंग्स जांचें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ सिंक विफल

सिंक त्रुटि

{{ feed_name }} के {{ platform_name }} पर सिंक करने में विफल।

विफलता के विवरण:
- फीड: {{ feed_name }}
- प्लेटफॉर्म: {{ platform_name }}
- विफलता के समय: {{ failed_at }}
- त्रुटि कोड: {{ error_code }}

त्रुटि संदेश:
{{ error_message }}

सामान्य कारण:
• अमान्य API योग्यता या अतीत के टोकन
• नेटवर्क कनेक्टिविटी समस्या
• प्लेटफॉर्म API दर सीमा को पार कर दिया गया
• फीड प्रारूप प्लेटफॉर्म आवश्यकताओं को पूरा नहीं करता है

{% if recommended_action %}
सिफारिश की गई कार्रवाई:
{{ recommended_action }}
{% endif %}

दुबारा सिंक करें: {{ retry_url }}
फीड सेटिंग्स जांचें: {{ admin_feed_url }}
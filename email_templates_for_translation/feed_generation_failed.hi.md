---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ फीड उत्पादन विफल रहा: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ फीड उत्पादन विफल रहा
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          उत्पादन त्रुटि
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          एक त्रुटि के कारण {{ feed_name }} उत्पाद फीड उत्पादित नहीं कर सका।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              त्रुटि विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>फीड:</strong> {{ feed_name }}<br/>
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
          <strong>त्रुटि लॉग:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:30 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • आवश्यक उत्पाद डेटा की कमी (शीर्षक, मूल्य, छवि)<br/>
          • अमान्य उत्पाद डेटा प्रारूप<br/>
          • डेटाबेस कनेक्शन समस्याएं<br/>
          • अपर्याप्त हार्ड डिस्क स्थान या मेमोरी
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पुन: उत्पादन करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          फीड सेटिंग्स देखें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          यदि समस्या बनी रहती है, तो समर्थन से संपर्क करें और त्रुटि कोड {{ error_code }} के साथ।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ फीड उत्पादन विफल रहा

उत्पादन त्रुटि

एक त्रुटि के कारण {{ feed_name }} उत्पाद फीड उत्पादित नहीं कर सका।

त्रुटि विवरण:
- फीड: {{ feed_name }}
- विफल हुआ: {{ failed_at }}
- त्रुटि कोड: {{ error_code }}

त्रुटि संदेश:
{{ error_message }}

{% if error_log %}
त्रुटि लॉग:
{{ error_log|truncatewords:30 }}
{% endif %}

सामान्य कारण:
• आवश्यक उत्पाद डेटा की कमी (शीर्षक, मूल्य, छवि)
• अमान्य उत्पाद डेटा प्रारूप
• डेटाबेस कनेक्शन समस्याएं
• अपर्याप्त हार्ड डिस्क स्थान या मेमोरी

पुन: उत्पादन करें: {{ retry_url }}
फीड सेटिंग्स देखें: {{ admin_feed_url }}

यदि समस्या बनी रहती है, तो समर्थन से संपर्क करें और त्रुटि कोड {{ error_code }} के साथ।
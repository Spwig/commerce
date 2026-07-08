---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ अनुवाद कार्य समाप्त नहीं हो सका: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ अनुवाद कार्य विफल रहा
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अनुवाद त्रुटि
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपका बैच अनुवाद कार्य एक त्रुटि से ग्रस्त रहा और पूरा नहीं किया जा सका।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              कार्य विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>कार्य के आईडी:</strong> {{ job_id }}<br/>
              <strong>कंटेंट प्रकार:</strong> {{ content_type }}<br/>
              <strong>लक्ष्य भाषाएं:</strong> {{ target_languages }}<br/>
              <strong>त्रुटि में विफल रहा:</strong> {{ failed_at }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              आंशिक पूर्णता
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              त्रुटि के बाद {{ items_completed }} आइटम {{ total_items }} आइटम सफलतापूर्वक अनुवादित किए गए।
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सामान्य कारण:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • अनुवाद सेवा API कनेक्शन समस्या<br/>
          • अनुवाद क्रेडिट की कमी<br/>
          • अमान्य या खराब स्रोत कंटेंट<br/>
          • समर्थित भाषा जोड़ी नहीं
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश की गई कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. अपने अनुवाद सेवा सेटिंग्स की जांच करें<br/>
          2. अनुवाद क्रेडिट की उपलब्धता की पुष्टि करें<br/>
          3. विशिष्ट समस्याओं के लिए त्रुटि संदेश की जांच करें<br/>
          4. अनुवाद कार्य को पुनः प्रयास करें
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          पुनः प्रयास करें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          सेटिंग्स की जांच करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          यदि समस्या बनी रहती है, तो टीम से संपर्क करें और त्रुटि कोड {{ error_code }} के साथ।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ अनुवाद कार्य विफल रहा

अनुवाद त्रुटि

आपका बैच अनुवाद कार्य एक त्रुटि से ग्रस्त रहा और पूरा नहीं किया जा सका।

कार्य विवरण:
- कार्य के आईडी: {{ job_id }}
- कंटेंट प्रकार: {{ content_type }}
- लक्ष्य भाषाएं: {{ target_languages }}
- त्रुटि में विफल रहा: {{ failed_at }}
- त्रुटि कोड: {{ error_code }}

त्रुटि संदेश:
{{ error_message }}

{% if partial_completion %}
आंशिक पूर्णता:
{{ items_completed }} आइटम {{ total_items }} आइटम के बाद त्रुटि के बाद सफलतापूर्वक अनुवादित किए गए।
{% endif %}

सामान्य कारण:
• अनुवाद सेवा API कनेक्शन समस्या
• अनुवाद क्रेडिट की कमी
• अमान्य या खराब स्रोत कंटेंट
• समर्थित भाषा जोड़ी नहीं

सिफारिश की गई कार्रवाई:
1. अपने अनुवाद सेवा सेटिंग्स की जांच करें
2. अनुवाद क्रेडिट की उपलब्धता की पुष्टि करें
3. विशिष्ट समस्याओं के लिए त्रुटि संदेश की जांच करें
4. अनुवाद कार्य को पुनः प्रयास करें

पुनः अनुवाद करें: {{ retry_url }}
सेटिंग्स की जांच करें: {{ settings_url }}

यदि समस्या बनी रहती है, तो टीम से संपर्क करें और त्रुटि कोड {{ error_code }} के साथ।
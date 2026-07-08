---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ प्रणाली स्वास्थ्य चेतावनी: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ प्रणाली स्वास्थ्य चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          चेतावनी सीमा के ऊपर
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके Spwig स्थापना पर एक प्रणाली स्वास्थ्य मापदंड चेतावनी सीमा के ऊपर है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              चेतावनी विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>मापदंड:</strong> {{ metric_name }}<br/>
              <strong>वर्तमान मूल्य:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>चेतावनी सीमा:</strong> {{ warning_threshold }}<br/>
              <strong>महत्वपूर्ण सीमा:</strong> {{ critical_threshold }}<br/>
              <strong>पता लगाया गया:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          संभावित प्रभाव:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          प्रस्तावित कार्रवाई:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          लचीलापन विश्लेषण:
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

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 कार्रवाई आवश्यक: अभी तक यह महत्वपूर्ण नहीं है, लेकिन इस चेतावनी के तुरंत संबोधन करने से भविष्य में सेवा समस्याओं को रोका जा सकता है।
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          प्रणाली डैशबोर्ड देखें
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          विस्तृत मापदंड देखें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ प्रणाली स्वास्थ्य चेतावनी

चेतावनी सीमा के ऊपर

आपके Spwig स्थापना पर एक प्रणाली स्वास्थ्य मापदंड चेतावनी सीमा के ऊपर है।

चेतावनी विवरण:
- मापदंड: {{ metric_name }}
- वर्तमान मूल्य: {{ current_value }}
- चेतावनी सीमा: {{ warning_threshold }}
- महत्वपूर्ण सीमा: {{ critical_threshold }}
- पता लगाया गया: {{ detected_at }}

संभावित प्रभाव:
{{ impact_description }}

प्रस्तावित कार्रवाई:
{{ recommended_actions }}

{% if trend_data %}
लचीलापन विश्लेषण:
{{ trend_data }}
{% endif %}

💡 कार्रवाई आवश्यक: अभी तक यह महत्वपूर्ण नहीं है, लेकिन इस चेतावनी के तुरंत संबोधन करने से भविष्य में सेवा समस्याओं को रोका जा सकता है।

प्रणाली डैशबोर्ड देखें: {{ dashboard_url }}
विस्तृत मापदंड देखें: {{ metrics_url }}
---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ संगतता समस्या: {{ component_name }} और {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ संगतता चेतावनी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          संस्करण संघर्ष का पता चला
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          आपके Spwig स्टोर में घटकों के बीच संगतता समस्या का पता चला।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              संघर्ष विवरण:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>घटक 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>घटक 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>पता चला:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          संगतता समस्या:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              संभावित प्रभाव
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          सिफारिश करते हैं:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              संगत संस्करण
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          संघर्ष को हल करें
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          समर्थन से संपर्क करें
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          आपका स्टोर अभी भी संचालित है, लेकिन हम इस संघर्ष को जल्दी हल करने की सिफारिश करते हैं।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ संगतता चेतावनी

संस्करण संघर्ष का पता चला

आपके Spwig स्टोर में घटकों के बीच संगतता समस्या का पता चला।

संघर्ष विवरण:
- घटक 1: {{ component_name }} v{{ component_version }}
- घटक 2: {{ conflicting_component }} v{{ conflicting_version }}
- पता चला: {{ detected_at }}

संगतता समस्या:
{{ incompatibility_description }}

संभावित प्रभाव:
{{ impact_description }}

सिफारिश करते हैं:
{{ recommended_action }}

{% if compatible_versions %}
संगत संस्करण:
{{ compatible_versions }}
{% endif %}

{% if update_url %}संघर्ष को हल करें: {{ update_url }}{% endif %}
समर्थन से संपर्क करें: {{ support_url }}

आपका स्टोर अभी भी संचालित है, लेकिन हम इस संघर्ष को जल्दी हल करने की सिफारिश करते हैं।
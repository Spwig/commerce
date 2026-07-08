---
template_type: form_submission_auto_response
category: Form Builder
---

# Email Template: form_submission_auto_response

## Subject
{{ auto_response_subject }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ auto_response_heading }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Merhaba {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ auto_response_message }}
        </mj-text>

        <mj-spacer height="30px" />

        {% if cta_text and cta_url %}
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text }}
        </mj-button>
        <mj-spacer height="30px" />
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Başvurunuzun referansı:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if support_url %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Hemen yardım mı istersiniz? <a href="{{ support_url }}">Destek ile iletişime geçin</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ auto_response_heading }}

Merhaba {{ submitter_name }},

{{ auto_response_message }}

{% if cta_text and cta_url %}{{ cta_text }}: {{ cta_url }}{% endif %}

Başvurunuzun referansı: {{ submission_id }}

{% if support_url %}Hemen yardım mı istersiniz? Destek ile iletişime geçin: {{ support_url }}{% endif %}
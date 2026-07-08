---
template_type: newsletter
category: Marketing
---

# Email Template: newsletter

## Subject
{{ newsletter_subject }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ newsletter_heading }}
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ newsletter_content }}
        </mj-text>

        {% if cta_url %}
        <mj-spacer height="30px" />
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text|default:'Learn More' }}
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ newsletter_heading }}

{{ newsletter_content }}

{% if cta_url %}{{ cta_text|default:'Learn More' }}: {{ cta_url }}{% endif %}
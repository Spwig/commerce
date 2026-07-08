---
template_type: form_submission_approved
category: Form Builder
---

# Email Template: form_submission_approved

## Subject
✓ Ihre {{ form_name }} wurde genehmigt!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Genehmigt!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Große Nachrichten!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ihre {{ form_name }}-Einreichung wurde genehmigt!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Einreichungsdetails:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Formular:</strong> {{ form_name }}<br/>
              <strong>Einreichung:</strong> {{ submission_date }}<br/>
              <strong>Genehmigung:</strong> {{ approval_date }}<br/>
              <strong>Referenz #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if approval_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nachricht von unserem Team:
        </mj-text>
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ approval_message }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Was passiert als nächstes?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        <mj-spacer height="30px" />

        {% if cta_url %}
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text|default:'Details ansehen' }}
        </mj-button>
        {% endif %}

        {% if support_url %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Fragen? <a href="{{ support_url }}">Support kontaktieren</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ GENEHMIGT!

Große Nachrichten!

Hi {{ submitter_name }},

Ihre {{ form_name }}-Einreichung wurde genehmigt!

EINREICHUNGSDETAILS:
- Formular: {{ form_name }}
- Einreichung: {{ submission_date }}
- Genehmigung: {{ approval_date }}
- Referenz #: {{ submission_id }}

{% if approval_message %}
MESSAGE VOM TEAM:
{{ approval_message }}
{% endif %}

WAS PASSIERT ALS NÄCHSTES?
{{ next_steps }}

{% if cta_url %}Details ansehen: {{ cta_url }}{% endif %}

{% if support_url %}Fragen? Support kontaktieren: {{ support_url }}{% endif %}
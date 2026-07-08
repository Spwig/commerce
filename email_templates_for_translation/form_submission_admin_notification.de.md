---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
Neue {{ form_name }}-Einreichung von {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 Neue Formular-Einreichung
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Neue Einreichung empfangen
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Eine neue {{ form_name }}-Einreichung wurde empfangen.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Einreichungsinformationen:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Formular:</strong> {{ form_name }}<br/>
              <strong>Einreichender:</strong> {{ submitter_name }}<br/>
              <strong>E-Mail:</strong> {{ submitter_email }}<br/>
              <strong>Einreichdatum:</strong> {{ submission_date }}<br/>
              <strong>Referenz #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Einreichungsdaten:
        </mj-text>

        {% for field in submission_data %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="12px">
          <mj-column>
            <mj-text font-size="13px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ field.label }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ field.value }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_submission_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          In Admin ansehen
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Auf Einreichenden antworten
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 NEUE FORMULAR-EINREICHUNG

Neue Einreichung empfangen

Eine neue {{ form_name }}-Einreichung wurde empfangen.

EINREICHUNGSINFORMATIONEN:
- Formular: {{ form_name }}
- Einreichender: {{ submitter_name }}
- E-Mail: {{ submitter_email }}
- Einreichdatum: {{ submission_date }}
- Referenz #: {{ submission_id }}

EINREICHUNGSDATEN:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

In Admin ansehen: {{ admin_submission_url }}
{% if reply_to_email %}Auf Einreichenden antworten: mailto:{{ reply_to_email }}{% endif %}
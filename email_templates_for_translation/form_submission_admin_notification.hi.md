---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
नई {{ form_name }} जमा करें द्वारा {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 नई फॉर्म जमा करें
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          नई जमा प्राप्त
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          एक नई {{ form_name }} जमा प्राप्त कर ली गई है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              जमा जानकारी:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>फॉर्म:</strong> {{ form_name }}<br/>
              <strong>द्वारा जमा करें:</strong> {{ submitter_name }}<br/>
              <strong>ईमेल:</strong> {{ submitter_email }}<br/>
              <strong>जमा करें:</strong> {{ submission_date }}<br/>
              <strong>संदर्भ #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          जमा करें डेटा:
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
          प्रशासन में देखें
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          जमाकर्ता को जवाब दें
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 नई फॉर्म जमा करें

नई जमा प्राप्त

एक नई {{ form_name }} जमा प्राप्त कर ली गई है।

जमा जानकारी:
- फॉर्म: {{ form_name }}
- द्वारा जमा करें: {{ submitter_name }}
- ईमेल: {{ submitter_email }}
- जमा करें: {{ submission_date }}
- संदर्भ #: {{ submission_id }}

जमा करें डेटा:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

प्रशासन में देखें: {{ admin_submission_url }}
{% if reply_to_email %}जमाकर्ता को जवाब दें: mailto:{{ reply_to_email }}{% endif %}
---
template_type: form_submission_confirmation
category: Form Builder
---

# Email Template: form_submission_confirmation

## Subject
✓ {{ form_name }} 제출을 받았습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Submission Received
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thank You!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Thank you for submitting the {{ form_name }} form. We've received your information and will get back to you soon.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Submission Details:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          What Happens Next?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        {% if expected_response_time %}
        <mj-spacer height="20px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 Typical response time: {{ expected_response_time }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if submission_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Your Submission:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for field in submission_data %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ field.label }}:</strong> {{ field.value }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if support_url %}
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Questions? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact Support</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ SUBMISSION RECEIVED

Thank You!

Hi {{ submitter_name }},

Thank you for submitting the {{ form_name }} form. We've received your information and will get back to you soon.

SUBMISSION DETAILS:
- Form: {{ form_name }}
- Submitted: {{ submission_date }}
- Reference #: {{ submission_id }}

WHAT HAPPENS NEXT?
{{ next_steps }}

{% if expected_response_time %}💡 Typical response time: {{ expected_response_time }}{% endif %}

{% if submission_data %}
YOUR SUBMISSION:
{% for field in submission_data %}
{{ field.label }}: {{ field.value }}
{% endfor %}
{% endif %}

{% if support_url %}Questions? Contact Support: {{ support_url }}{% endif %}
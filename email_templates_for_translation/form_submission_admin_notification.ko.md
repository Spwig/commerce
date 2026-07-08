---
template_type: form_submission_admin_notification
category: Form Builder
---

# Email Template: form_submission_admin_notification

## Subject
새로운 {{ form_name }} 제출: {{ submitter_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📝 새로운 폼 제출
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          새로운 제출이 수신되었습니다
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          새로운 {{ form_name }} 제출이 수신되었습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              제출 정보:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>폼:</strong> {{ form_name }}<br/>
              <strong>제출자:</strong> {{ submitter_name }}<br/>
              <strong>이메일:</strong> {{ submitter_email }}<br/>
              <strong>제출 시간:</strong> {{ submission_date }}<br/>
              <strong>참조 #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          제출 데이터:
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
          관리자에서 보기
        </mj-button>

        {% if reply_to_email %}
        <mj-spacer height="10px" />
        <mj-button href="mailto:{{ reply_to_email }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          제출자에게 답장 보내기
        </mj-button>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📝 새로운 폼 제출

새로운 제출이 수신되었습니다

새로운 {{ form_name }} 제출이 수신되었습니다.

제출 정보:
- 폼: {{ form_name }}
- 제출자: {{ submitter_name }}
- 이메일: {{ submitter_email }}
- 제출 시간: {{ submission_date }}
- 참조 #: {{ submission_id }}

제출 데이터:
{% for field in submission_data %}
{{ field.label }}:
{{ field.value }}

{% endfor %}

관리자에서 보기: {{ admin_submission_url }}
{% if reply_to_email %}제출자에게 답장 보내기: mailto:{{ reply_to_email }}{% endif %}
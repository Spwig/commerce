---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
ご提出いただいた{{ form_name }}の更新情報

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご提出いただいた申請の更新情報
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ submitter_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ form_name }}のフォームを提出いただき、ありがとうございます。慎重な審査の後、この度は申請の承認ができません。
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              申請の詳細:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Reviewed:</strong> {{ rejection_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          原因:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ご再提出が可能です
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          再提出する
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          サポートに連絡
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          この決定についてご質問がある場合は、お気軽にお問い合わせください。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
申請の更新情報

こんにちは {{ submitter_name }}、

{{ form_name }}のフォームを提出いただき、ありがとうございます。慎重な審査の後、この度は申請の承認ができません。

申請の詳細:
- Form: {{ form_name }}
- Submitted: {{ submission_date }}
- Reviewed: {{ rejection_date }}
- Reference #: {{ submission_id }}

{% if rejection_reason %}
原因:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
ご再提出が可能です:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}再提出: {{ resubmit_url }}{% endif %}
{% if support_url %}サポートに連絡: {{ support_url }}{% endif %}

この決定についてご質問がある場合は、お気軽にお問い合わせください。
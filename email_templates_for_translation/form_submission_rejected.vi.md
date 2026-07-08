---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
Cập nhật về việc gửi biểu mẫu {{ form_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cập nhật về Việc Gửi Của Bạn
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã gửi biểu mẫu {{ form_name }}. Sau khi xem xét kỹ lưỡng, chúng tôi hiện tại không thể phê duyệt việc gửi của bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết Việc Gửi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Biểu mẫu:</strong> {{ form_name }}<br/>
              <strong>Gửi lúc:</strong> {{ submission_date }}<br/>
              <strong>Xem xét lúc:</strong> {{ rejection_date }}<br/>
              <strong>Số tham chiếu:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lý do:
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
              Bạn có thể gửi lại
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
          Gửi lại
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Liên hệ hỗ trợ
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu bạn có câu hỏi về quyết định này, vui lòng không ngần ngại liên hệ với chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
CẬP NHẬT VỀ VIỆC GỬI CỦA BẠN

Chào {{ submitter_name }},

Cảm ơn bạn đã gửi biểu mẫu {{ form_name }}. Sau khi xem xét kỹ lưỡng, chúng tôi hiện tại không thể phê duyệt việc gửi của bạn.

CHI TIẾT VIỆC GỬI:
- Biểu mẫu: {{ form_name }}
- Gửi lúc: {{ submission_date }}
- Xem xét lúc: {{ rejection_date }}
- Số tham chiếu: {{ submission_id }}

{% if rejection_reason %}
LÝ DO:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
BẠN CÓ THỂ GỬI LẠI:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}Gửi lại: {{ resubmit_url }}{% endif %}
{% if support_url %}Liên hệ hỗ trợ: {{ support_url }}{% endif %}

Nếu bạn có câu hỏi về quyết định này, vui lòng không ngần ngại liên hệ với chúng tôi.
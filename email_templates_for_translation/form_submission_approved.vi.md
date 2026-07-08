---
template_type: form_submission_approved
category: Form Builder
---

# Email Template: form_submission_approved

## Subject
✓ Đơn đăng ký {{ form_name }} của bạn đã được phê duyệt!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          ✓ Đã phê duyệt!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tin Tức Tuyệt Vời!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Đơn đăng ký {{ form_name }} của bạn đã được phê duyệt!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi Tiết Đơn Đăng Ký:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Form:</strong> {{ form_name }}<br/>
              <strong>Submitted:</strong> {{ submission_date }}<br/>
              <strong>Approved:</strong> {{ approval_date }}<br/>
              <strong>Reference #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if approval_message %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông Điệp Từ Đội Ngũ Chúng Tôi:
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
          Điều Gì Sẽ Xảy Ra Tiếp Theo?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>

        <mj-spacer height="30px" />

        {% if cta_url %}
        <mj-button href="{{ cta_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          {{ cta_text|default:'Xem Chi Tiết' }}
        </mj-button>
        {% endif %}

        {% if support_url %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Có Thắc Mắc? <a href="{{ support_url }}">Liên Hệ Hỗ Trợ</a>
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ĐÃ PHÊ DUYỆT!

Tin Tức Tuyệt Vời!

Chào {{ submitter_name }},

Đơn đăng ký {{ form_name }} của bạn đã được phê duyệt!

CHI TIẾT ĐƠN ĐĂNG KÝ:
- Form: {{ form_name }}
- Submitted: {{ submission_date }}
- Approved: {{ approval_date }}
- Reference #: {{ submission_id }}

{% if approval_message %}
THÔNG ĐIỆP TỪ ĐỘI NGŨ CHÚNG TÔI:
{{ approval_message }}
{% endif %}

ĐIỀU GÌ SẼ XẢY RA TIẾP THEO?
{{ next_steps }}

{% if cta_url %}Xem Chi Tiết: {{ cta_url }}{% endif %}

{% if support_url %}Có Thắc Mắc? Liên Hệ Hỗ Trợ: {{ support_url }}{% endif %}
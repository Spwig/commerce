---
template_type: dev_submission_rejected
category: Developer Portal
---

# Email Template: dev_submission_rejected

## Subject
Cập nhật đánh giá thành phần: {{ component_name }} v{{ version }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Cập nhật đánh giá
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Hoàn thành đánh giá thành phần
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          Rất tiếc, thành phần bạn gửi không vượt qua được quy trình đánh giá của chúng tôi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Component Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Thành phần:</strong> {{ component_name }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="8px">
          <strong>Loại:</strong> {{ component_type }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Phiên bản:</strong> v{{ version }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Review Feedback (if provided) -->
    {% if review_notes %}
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          Phản hồi đánh giá:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" border-left="3px solid {{ theme.color.error|default:'#ef4444' }}">
          {{ review_notes }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="25px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Bạn có thể xử lý phản hồi và gửi lại phiên bản mới của thành phần.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ submission_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Xem chi tiết gửi thành phần
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Cổng phát triển Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Có câu hỏi? Liên hệ hỗ trợ phát triển
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Chào {{ developer_name }},

Rất tiếc, thành phần bạn gửi không vượt qua được quy trình đánh giá của chúng tôi.

Thành phần: {{ component_name }}
Loại: {{ component_type }}
Phiên bản: v{{ version }}

{% if review_notes %}Phản hồi đánh giá:
{{ review_notes }}{% endif %}

Bạn có thể xử lý phản hồi và gửi lại phiên bản mới của thành phần.

Xem chi tiết gửi thành phần: {{ submission_url }}

---
Cổng phát triển Spwig
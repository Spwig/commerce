---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
Chúng tôi đã nhận được đơn ứng tuyển của bạn, {{ developer_name }}

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
          Đơn ứng tuyển đã được nhận!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Chúng tôi đang xem xét đơn ứng tuyển của bạn
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
          Cảm ơn bạn đã ứng tuyển vào chương trình Nhà phát triển Spwig. Chúng tôi đã nhận được đơn ứng tuyển của bạn và đội ngũ của chúng tôi sẽ xem xét ngay lập tức.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Đội ngũ của chúng tôi sẽ xem xét đơn ứng tuyển của bạn (thường mất 2-3 ngày làm việc)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Bạn sẽ nhận được email thông báo quyết định của chúng tôi
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> Sau khi được chấp thuận, bạn sẽ có quyền truy cập đầy đủ vào bảng điều khiển nhà phát triển
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Xem Bảng điều khiển Nhà phát triển
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Bảng điều khiển Nhà phát triển Spwig</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Có câu hỏi? Liên hệ hỗ trợ nhà phát triển
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Chào {{ developer_name }},

Cảm ơn bạn đã ứng tuyển vào chương trình Nhà phát triển Spwig. Chúng tôi đã nhận được đơn ứng tuyển của bạn và đội ngũ của chúng tôi sẽ xem xét ngay lập tức.

Điều gì sẽ xảy ra tiếp theo?
1. Đội ngũ của chúng tôi sẽ xem xét đơn ứng tuyển của bạn (thường mất 2-3 ngày làm việc)
2. Bạn sẽ nhận được email thông báo quyết định của chúng tôi
3. Sau khi được chấp thuận, bạn sẽ có quyền truy cập đầy đủ vào bảng điều khiển nhà phát triển

Xem Bảng điều khiển Nhà phát triển: {{ portal_url }}

---
Bảng điều khiển Nhà phát triển Spwig
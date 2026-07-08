---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
Chào mừng bạn đến với chương trình Nhà phát triển Spwig, {{ developer_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Chào mừng đến với Spwig!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Ứng dụng nhà phát triển của bạn đã được phê duyệt
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
          Chúc mừng! Ứng dụng nhà phát triển của bạn đã được phê duyệt. Bạn giờ đây đã có quyền truy cập đầy đủ vào Trung tâm Nhà phát triển Spwig.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          Giấy phép nhà phát triển miễn phí của bạn đang chờ bạn
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Với tư cách là nhà phát triển đã được phê duyệt, bạn sẽ nhận được <strong>lắp đặt miễn phí Spwig Shop + POS</strong> với cập nhật vĩnh viễn. Nhận giấy phép của bạn, cài đặt Spwig trên máy chủ của bạn và bắt đầu xây dựng các thành phần ngay lập tức.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Nhận giấy phép miễn phí
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          Bắt đầu:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> Nhận giấy phép nhà phát triển miễn phí của bạn
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> Cài đặt Spwig trên máy chủ của bạn
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> Xây dựng thành phần đầu tiên của bạn bằng SDK của chúng tôi
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> Gửi từ bảng điều khiển của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          Đến bảng điều khiển
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Trung tâm Nhà phát triển Spwig</strong>
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

Chúc mừng! Ứng dụng nhà phát triển của bạn đã được phê duyệt. Bạn giờ đây đã có quyền truy cập đầy đủ vào Trung tâm Nhà phát triển Spwig.

GIẤY PHÉP NHÀ PHÁT TRIỂN MIỄN PHÍ CỦA BẠN ĐANG CHỜ BẠN
Với tư cách là nhà phát triển đã được phê duyệt, bạn sẽ nhận được cài đặt miễn phí Spwig Shop + POS với cập nhật vĩnh viễn. Nhận giấy phép của bạn, cài đặt Spwig trên máy chủ của bạn và bắt đầu xây dựng các thành phần ngay lập tức.

Nhận giấy phép miễn phí: {{ license_url }}

Bắt đầu:
1. Nhận giấy phép nhà phát triển miễn phí của bạn: {{ license_url }}
2. Cài đặt Spwig trên máy chủ của bạn
3. Xây dựng thành phần đầu tiên của bạn bằng SDK của chúng tôi
4. Gửi từ bảng điều khiển của bạn

Đến bảng điều khiển: {{ dashboard_url }}

---
Trung tâm Nhà phát triển Spwig
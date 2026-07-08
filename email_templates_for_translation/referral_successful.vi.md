---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 Bạn bè của bạn {{ referee_name }} vừa đăng ký!

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Thành công giới thiệu!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ referee_name }} Đã Tham Gia!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Người được giới thiệu của bạn giờ đã là thành viên
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Tin vui! {{ referee_name }} vừa đăng ký bằng liên kết giới thiệu của bạn.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Khi họ thực hiện lần mua hàng đầu tiên, bạn và họ sẽ đều nhận được phần thưởng! Chúng tôi sẽ gửi email khác cho bạn khi điều đó xảy ra.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Điều gì sẽ xảy ra tiếp theo?
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }} thực hiện lần mua hàng đầu tiên<br/>
          2. Bạn và họ sẽ nhận được phần thưởng tự động<br/>
          3. Bạn có thể sử dụng phần thưởng cho bất kỳ lần mua hàng nào trong tương lai
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          Tiếp tục chia sẻ để kiếm thêm phần thưởng!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          Xem Danh Sách Giới Thiệu Của Tôi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 Bạn bè của bạn {{ referee_name }} vừa đăng ký!

Chào {{ customer_name }},

Tin vui! {{ referee_name }} vừa đăng ký bằng liên kết giới thiệu của bạn.

Khi họ thực hiện lần mua hàng đầu tiên, bạn và họ sẽ đều nhận được phần thưởng! Chúng tôi sẽ gửi email khác cho bạn khi điều đó xảy ra.

Điều gì sẽ xảy ra tiếp theo?
1. {{ referee_name }} thực hiện lần mua hàng đầu tiên
2. Bạn và họ sẽ nhận được phần thưởng tự động
3. Bạn có thể sử dụng phần thưởng cho bất kỳ lần mua hàng nào trong tương lai

Tiếp tục chia sẻ để kiếm thêm phần thưởng:
{{ referral_link }}

Xem danh sách giới thiệu của bạn: {{ referral_dashboard_url }}

{{ shop_name }}
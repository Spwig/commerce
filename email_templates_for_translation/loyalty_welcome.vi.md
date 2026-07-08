---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
Chào mừng bạn đến với Chương trình Thưởng của {{ shop_name }}!

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
          🎉 Chào mừng bạn đến với Chương trình Thưởng!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Bắt đầu tích điểm với mỗi lần mua hàng
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
          Chào mừng bạn đến với chương trình Thưởng của {{ shop_name }}! Bạn đã được đăng ký tự động và có thể bắt đầu tích điểm ngay lập tức.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Quà tặng chào mừng: {{ bonus_points }} điểm!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Tầng của bạn:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Cách để tích điểm
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Mua hàng - Tích điểm cho mỗi đơn hàng<br/>
          • Viết đánh giá - Chia sẻ ý kiến của bạn<br/>
          • Mời bạn bè - Lan tỏa thông tin<br/>
          • Quà sinh nhật - Điểm đặc biệt vào ngày sinh nhật của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          Xem Thưởng của Tôi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Chào mừng bạn đến với Chương trình Thưởng của {{ shop_name }}!

Chào {{ customer_name }},

Chào mừng bạn đến với chương trình Thưởng của {{ shop_name }}! Bạn đã được đăng ký tự động và có thể bắt đầu tích điểm ngay lập tức.

{% if bonus_points %}Quà tặng chào mừng: {{ bonus_points }} điểm!{% endif %}

Tầng của bạn: {{ current_tier }}
{{ tier_benefits }}

Cách để tích điểm:
- Mua hàng - Tích điểm cho mỗi đơn hàng
- Viết đánh giá - Chia sẻ ý kiến của bạn
- Mời bạn bè - Lan tỏa thông tin
- Quà sinh nhật - Điểm đặc biệt vào ngày sinh nhật của bạn

Xem thưởng của bạn: {{ account_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}
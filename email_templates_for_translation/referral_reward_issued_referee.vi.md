---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
Chào mừng! Đây là phần thưởng {{ reward_amount }} của bạn

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
          🎁 Quà chào mừng!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Cảm ơn bạn đã tham gia cùng chúng tôi
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Phần thưởng chào mừng của bạn
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Hết hạn: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào mừng bạn đến với {{ shop_name }}! {{ referrer_name }} đã giới thiệu bạn, và chúng tôi muốn gửi lời cảm ơn với phần thưởng chào mừng {{ reward_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Phần thưởng của bạn đã được thêm vào tài khoản và sẵn sàng sử dụng cho lần mua hàng tiếp theo!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Cách sử dụng phần thưởng của bạn
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Xem sản phẩm và thêm các mặt hàng vào giỏ hàng<br/>
          2. Tiến hành thanh toán<br/>
          3. Phần thưởng của bạn sẽ được áp dụng tự động<br/>
          4. Tận hưởng khoản tiết kiệm của bạn!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Bắt đầu mua sắm
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Bạn cũng có thể kiếm được phần thưởng!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Chia sẻ liên kết giới thiệu của bạn với bạn bè và kiếm phần thưởng khi họ thực hiện lần mua hàng đầu tiên.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          Nhận liên kết giới thiệu của tôi
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
Chào mừng! Đây là phần thưởng {{ reward_amount }} của bạn

Chào {{ customer_name }},

Chào mừng bạn đến với {{ shop_name }}! {{ referrer_name }} đã giới thiệu bạn, và chúng tôi muốn gửi lời cảm ơn với phần thưởng chào mừng {{ reward_amount }}.

Phần thưởng của bạn: {{ reward_amount }}
Loại: {{ reward_type_display }}
{% if expires_at %}Hết hạn: {{ expires_at }}{% endif %}

Cách sử dụng phần thưởng của bạn:
1. Xem sản phẩm và thêm các mặt hàng vào giỏ hàng
2. Tiến hành thanh toán
3. Phần thưởng của bạn sẽ được áp dụng tự động
4. Tận hưởng khoản tiết kiệm của bạn!

Bắt đầu mua sắm: {{ shop_url }}

Bạn cũng có thể kiếm được phần thưởng!
Chia sẻ liên kết giới thiệu của bạn với bạn bè và kiếm phần thưởng khi họ thực hiện lần mua hàng đầu tiên.
Nhận liên kết giới thiệu của bạn: {{ my_referral_link_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}
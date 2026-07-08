---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} đã gửi cho bạn một món quà!

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
          🎁 Bạn đã được mời!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} muốn chia sẻ {{ shop_name }} với bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          Nhận quà chào mừng của bạn
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          Trên đơn hàng đầu tiên của bạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chào bạn,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} nghĩ bạn sẽ yêu thích mua sắm tại {{ shop_name }}. Để chào mừng bạn, chúng tôi đang cung cấp giảm giá {{ reward_amount }} cho đơn hàng đầu tiên của bạn!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Chỉ cần nhấn vào nút bên dưới để bắt đầu và phần thưởng của bạn sẽ được áp dụng tự động cho đơn hàng đầu tiên của bạn.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          Cách hoạt động
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Nhấn vào nút để truy cập {{ shop_name }}<br/>
          2. Duyệt và thêm các mặt hàng vào giỏ hàng<br/>
          3. Hoàn tất đơn hàng<br/>
          4. Phần thưởng {{ reward_amount }} của bạn sẽ được áp dụng tự động!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          Nhận quà {{ reward_amount }} của tôi
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Mời bạn này được gửi bởi {{ referrer_name }}<br/>
          Có câu hỏi? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Liên hệ hỗ trợ</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} đã gửi cho bạn một món quà!

Chào bạn,

{{ referrer_name }} nghĩ bạn sẽ yêu thích mua sắm tại {{ shop_name }}. Để chào mừng bạn, chúng tôi đang cung cấp giảm giá {{ reward_amount }} cho đơn hàng đầu tiên của bạn!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

Cách hoạt động:
1. Truy cập {{ shop_name }}
2. Duyệt và thêm các mặt hàng vào giỏ hàng
3. Hoàn tất đơn hàng
4. Phần thưởng {{ reward_amount }} của bạn sẽ được áp dụng tự động!

Nhận quà của bạn: {{ referral_link }}

{{ shop_name }}
Mời bạn này được gửi bởi {{ referrer_name }}
Có câu hỏi? Liên hệ {{ support_email }}
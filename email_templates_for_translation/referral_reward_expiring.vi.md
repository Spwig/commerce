---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
Nhắc nhở: Phần thưởng {{ reward_amount }} của bạn sắp hết hạn

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ Phần thưởng sắp hết hạn
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Banner -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center" padding-top="10px">
          hết hạn trong {{ days_until_expiration }} ngày
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          Ngày hết hạn: {{ expiration_date }}
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
          Đừng để phần thưởng giới thiệu {{ reward_amount }} của bạn bị lãng quên! Nó sẽ hết hạn trong {{ days_until_expiration }} ngày.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hãy sử dụng nó ngay trên đơn hàng tiếp theo của bạn trước khi quá muộn!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Loại phần thưởng:</strong> {{ reward_type_display }}<br/>
          <strong>Số tiền:</strong> {{ reward_amount }}<br/>
          <strong>Hết hạn:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Mua sắm ngay
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
Nhắc nhở: Phần thưởng {{ reward_amount }} của bạn sắp hết hạn

Chào {{ customer_name }},

Đừng để phần thưởng giới thiệu {{ reward_amount }} của bạn bị lãng quên! Nó sẽ hết hạn trong {{ days_until_expiration }} ngày.

Chi tiết phần thưởng:
- Loại: {{ reward_type_display }}
- Số tiền: {{ reward_amount }}
- Hết hạn: {{ expiration_date }}

Hãy sử dụng nó ngay trên đơn hàng tiếp theo của bạn trước khi quá muộn!

Mua sắm ngay: {{ shop_url }}

{{ shop_name }}
Có câu hỏi? Liên hệ {{ support_email }}
---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 Điểm thưởng giới thiệu cho {{ referee_name }}!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 Bạn đã nhận được điểm thưởng giới thiệu!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cảm ơn bạn đã chia sẻ, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin vui! {{ referee_name }} vừa tham gia chương trình khách hàng thân thiết thông qua lời giới thiệu của bạn, và bạn đã nhận được điểm thưởng!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Bạn đã nhận được
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} Điểm
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Cho việc giới thiệu {{ referee_name }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Số dư của bạn được cập nhật:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Số dư điểm:</strong> {{ total_points }} điểm<br/>
          <strong>Điểm thưởng giới thiệu:</strong> +{{ bonus_points }} điểm<br/>
          <strong>Số người bạn đã giới thiệu:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tiếp tục chia sẻ, tiếp tục nhận thưởng!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Nhận {{ points_per_referral }} điểm cho mỗi người bạn giới thiệu tham gia. Không có giới hạn!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              Chia sẻ liên kết giới thiệu của bạn
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Bắt đầu mua sắm
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 ĐÃ NHẬN ĐƯỢC ĐIỂM THƯỞNG GIỚI THIỆU!

Cảm ơn bạn đã chia sẻ, {{ customer_name }}!

Tin vui! {{ referee_name }} vừa tham gia chương trình khách hàng thân thiết thông qua lời giới thiệu của bạn, và bạn đã nhận được điểm thưởng!

BẠN ĐÃ NHẬN ĐƯỢC:
+{{ bonus_points }} Điểm
Cho việc giới thiệu {{ referee_name }}

SỐ DƯ CẬP NHẬT CỦA BẠN:
- Số dư điểm: {{ total_points }} điểm
- Điểm thưởng giới thiệu: +{{ bonus_points }} điểm
- Số người bạn đã giới thiệu: {{ total_referrals }}

TIẾP TỤC CHIA SẺ, TIẾP TỤC NHẬN THƯỞNG!
Nhận {{ points_per_referral }} điểm cho mỗi người bạn giới thiệu tham gia. Không có giới hạn!

Chia sẻ liên kết giới thiệu của bạn: {{ referral_url }}
Bắt đầu mua sắm: {{ shop_url }}
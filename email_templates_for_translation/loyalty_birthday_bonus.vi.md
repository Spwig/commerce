---
template_type: loyalty_birthday_bonus
category: Loyalty Program
---

# Email Template: loyalty_birthday_bonus

## Subject
🎂 Chủc mኒng sinh nhật {{ customer_name }}! Đây là một đồi tạng đặc biệt từ {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="32px" align="center">🎂🎉🎁</mj-text>
        <mj-text font-size="26px" font-weight="bold" color="#92400e" align="center">
          Chủc mኒng sinh nhật!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chủc mኒng sinh nhật, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Để chủc mኒng ngày sinh nhật đặc biệt cỡa bạn, chúng tôi đã thêm {{ bonus_points }} điểm thống nhật vào tài khoản thống nhật cỡa bạn!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Quá tạng sinh nhật cỡa bạn
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Điểm
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Đã thêm vào tài khoản cỡa bạn!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tài khoản thống nhật cỡa bạn:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Số điểm:</strong> {{ total_points }} điểm<br/>
          <strong>Thống tạp hiện tại:</strong> {{ loyalty_tier }}<br/>
          <strong>Điểm sinh nhật:</strong> +{{ bonus_points }} điểm
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Bạt đầu mua sản và sử dụng điểm cỡa bạn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Chủc bạn có mኒt ngày sinh nhật tốt lợp! 🎉<br/>
          - Nhóm {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎂🎉🎁 CHỌC MኒNG SINH NHật!

Chủc mኒng sinh nhật, {{ customer_name }}!

Để chủc mኒng ngày sinh nhật đặc biệt cỡa bạn, chúng tôi đã thêm {{ bonus_points }} điểm thống nhật vào tài khoản thống nhật cỡa bạn!

QUÁ TẠNG SINH NHật CỢA BạN:
{{ bonus_points }} Điểm
Đã thêm vào tài khoản cỡa bạn!

TàI KHOẢN THỐNG NHật CỢA BạN:
- Số điểm: {{ total_points }} điểm
- Thống tạp hiện tại: {{ loyalty_tier }}
- Điểm sinh nhật: +{{ bonus_points }} điểm

Bạt đầu mua sản và sử dụng điểm cỡa bạn: {{ shop_url }}

Chủc bạn có mኒt ngày sinh nhật tốt lợp! 🎉
- Nhóm {{ shop_name }} Team
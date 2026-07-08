---
template_type: loyalty_anniversary_bonus
category: Loyalty Program
---

# Email Template: loyalty_anniversary_bonus

## Subject
🎉 {{ years_as_member }} Năm {{ years_as_member|pluralize }} Với {{ shop_name }} - Cảm Ơn!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="28px" align="center">🎉</mj-text>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          {{ years_as_member }} Năm {{ years_as_member|pluralize }} Cùng Nhau!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hôm nay đánh dấu {{ years_as_member }} năm {{ years_as_member|pluralize }} kể từ khi bạn tham gia chương trình khách hàng thân thiết của chúng tôi. Cảm ơn bạn đã là một thành viên được trân trọng như vậy!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              Quà Tặng Kỷ Niệm
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              {{ bonus_points }} Điểm
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              Được thêm để kỷ niệm {{ years_as_member }} năm {{ years_as_member|pluralize }}!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hành Trình {{ years_as_member }} Năm Của Bạn:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          <strong>Member Since:</strong> {{ member_since }}<br/>
          <strong>Total Orders:</strong> {{ total_orders }}<br/>
          <strong>Points Earned:</strong> {{ lifetime_points }} điểm<br/>
          <strong>Current Tier:</strong> {{ loyalty_tier }}<br/>
          <strong>Total Savings:</strong> {{ total_savings }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ loyalty_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem Bảng Điều Khiển Khách Hàng Thân Thiết Của Bạn
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Cảm ơn bạn vì {{ years_as_member }} năm tuyệt vời {{ years_as_member|pluralize }}!<br/>
          Chúc mừng nhiều hơn nữa 🥂
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ years_as_member }} NĂM {{ years_as_member|pluralize|upper }} CÙNG NHAU!

Chào {{ customer_name }},

Hôm nay đánh dấu {{ years_as_member }} năm {{ years_as_member|pluralize }} kể từ khi bạn tham gia chương trình khách hàng thân thiết của chúng tôi. Cảm ơn bạn đã là một thành viên được trân trọng như vậy!

QUÀ TẶNG KỶ NIỆM:
{{ bonus_points }} Điểm
Được thêm để kỷ niệm {{ years_as_member }} năm {{ years_as_member|pluralize }}!

HÀNH TRÌNH {{ years_as_member }} NĂM CỦA BẠN:
- Member Since: {{ member_since }}
- Tổng Số Đơn Hàng: {{ total_orders }}
- Điểm Đã Nhận: {{ lifetime_points }} điểm
- Tier Hiện Tại: {{ loyalty_tier }}
- Tổng Tiết Kiệm: {{ total_savings }}

Xem bảng điều khiển khách hàng thân thiết của bạn: {{ loyalty_dashboard_url }}

Cảm ơn bạn vì {{ years_as_member }} năm tuyệt vời {{ years_as_member|pluralize }}!
Chúc mừng nhiều hơn nữa 🥂

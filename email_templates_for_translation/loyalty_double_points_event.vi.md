---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 Sự kiện 2 lần điểm bắt đầu ngay bây giờ! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 Sự kiện 2 lần điểm!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Dành riêng cho thành viên trung thành!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Bạn chuẩn bị để kiếm được nhiều điểm! Trong thời gian giới hạn, bạn sẽ kiếm được {{ points_multiplier }}X điểm cho mỗi lần mua hàng.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              Kiếm được {{ points_multiplier }}X điểm
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              Trên tất cả các lần mua hàng<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Ví dụ về số điểm kiếm được:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Chi 50 đô la → Kiếm được {{ example_points_normal }} điểm bình thường<br/>
              <strong style="color: #047857;">Trong sự kiện này → Kiếm được {{ example_points_bonus }} điểm! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Chi 100 đô la → Kiếm được {{ example_points_normal_2 }} điểm bình thường<br/>
              <strong style="color: #047857;">Trong sự kiện này → Kiếm được {{ example_points_bonus_2 }} điểm! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Số dư hiện tại của bạn:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Điểm:</strong> {{ current_points }} điểm<br/>
          <strong>Cấp bậc:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          Mua sắm ngay & kiếm được {{ points_multiplier }}X điểm
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          Sự kiện kết thúc vào {{ event_end }} - Đừng bỏ lỡ!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 Sự kiện 2 lần điểm!
{{ event_start }} - {{ event_end }}

Dành riêng cho thành viên trung thành!

Chào {{ customer_name }},

Bạn chuẩn bị để kiếm được nhiều điểm! Trong thời gian giới hạn, bạn sẽ kiếm được {{ points_multiplier }}X điểm cho mỗi lần mua hàng.

KIẾM ĐƯỢC {{ points_multiplier }}X ĐIỂM
Trên tất cả các lần mua hàng
{{ event_start }} - {{ event_end }}

VÍ DỤ VỀ SỐ ĐIỂM KIẾM ĐƯỢC:
- Chi 50 đô la → Kiếm được {{ example_points_normal }} điểm bình thường
  Trong sự kiện này → Kiếm được {{ example_points_bonus }} điểm! 🎉

- Chi 100 đô la → Kiếm được {{ example_points_normal_2 }} điểm bình thường
  Trong sự kiện này → Kiếm được {{ example_points_bonus_2 }} điểm! 🎉

SỐ DƯ HIỆN TẠI CỦA BẠN:
- Điểm: {{ current_points }} điểm
- Cấp bậc: {{ loyalty_tier }}

Mua sắm ngay & kiếm được {{ points_multiplier }}X điểm: {{ shop_url }}

Sự kiện kết thúc vào {{ event_end }} - Đừng bỏ lỡ!
---
template_type: loyalty_double_points_event
category: Loyalty Program
---

# Email Template: loyalty_double_points_event

## Subject
🔥 เหตุการณ์ได้คะแนน 2 เท่าเริ่มต้นทันที! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#92400e" align="center">
          🔥 เหตุการณ์ได้คะแนน 2 เท่า!
        </mj-text>
        <mj-text font-size="18px" color="#92400e" align="center">
          {{ event_start }} - {{ event_end }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เฉพาะสมาชิกผู้ซื้อสินค้า!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณกำลังจะได้คะแนนเยอะมาก! ชั่วคราว คุณจะได้รับคะแนน {{ points_multiplier }} เท่า สำหรับการซื้อทุกครั้ง
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#dcfce7" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="24px" font-weight="bold" color="#047857" align="center">
              ได้คะแนน {{ points_multiplier }} เท่า
            </mj-text>
            <mj-text font-size="16px" color="#065f46" align="center">
              สำหรับการซื้อทั้งหมด<br/>
              {{ event_start }} - {{ event_end }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ตัวอย่างการได้คะแนน:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ใช้เงิน $50 → ได้คะแนน {{ example_points_normal }} ตามปกติ<br/>
              <strong style="color: #047857;">ในช่วงเหตุการณ์นี้ → ได้คะแนน {{ example_points_bonus }} ! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              ใช้เงิน $100 → ได้คะแนน {{ example_points_normal_2 }} ตามปกติ<br/>
              <strong style="color: #047857;">ในช่วงเหตุการณ์นี้ → ได้คะแนน {{ example_points_bonus_2 }} ! 🎉</strong>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ยอดคงเหลือปัจจุบันของคุณ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>คะแนน:</strong> {{ current_points }} คะแนน<br/>
          <strong>ระดับ:</strong> {{ loyalty_tier }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ไปช้อปเลย & ได้คะแนน {{ points_multiplier }} เท่า
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="#dc2626" align="center" font-weight="bold">
          เหตุการณ์จะสิ้นสุด {{ event_end }} - อย่าพลาด!
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 เหตุการณ์ได้คะแนน 2 เท่า!
{{ event_start }} - {{ event_end }}

เฉพาะสมาชิกผู้ซื้อสินค้า!

Hi {{ customer_name }},

คุณกำลังจะได้คะแนนเยอะมาก! ชั่วคราว คุณจะได้รับคะแนน {{ points_multiplier }} เท่า สำหรับการซื้อทุกครั้ง

ได้คะแนน {{ points_multiplier }} เท่า
สำหรับการซื้อทั้งหมด
{{ event_start }} - {{ event_end }}

ตัวอย่างการได้คะแนน:
- ใช้เงิน $50 → ได้คะแนน {{ example_points_normal }} ตามปกติ
  ในช่วงเหตุการณ์นี้ → ได้คะแนน {{ example_points_bonus }} ! 🎉

- ใช้เงิน $100 → ได้คะแนน {{ example_points_normal_2 }} ตามปกติ
  ในช่วงเหตุการณ์นี้ → ได้คะแนน {{ example_points_bonus_2 }} ! 🎉

ยอดคงเหลือปัจจุบันของคุณ:
- คะแนน: {{ current_points }} คะแนน
- ระดับ: {{ loyalty_tier }}

Shop now & earn {{ points_multiplier }}X points: {{ shop_url }}

เหตุการณ์จะสิ้นสุด {{ event_end }} - อย่าพลาด!
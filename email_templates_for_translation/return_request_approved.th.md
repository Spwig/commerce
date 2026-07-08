---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
การคืนสินค้าของคุณได้รับการอนุมัติ - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          การคืนสินค้าได้รับการอนุมัติ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          คำสั่งซื้อ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การขอคืนสินค้าสำหรับคำสั่งซื้อ <strong>#{{ order_number }}</strong> ของคุณได้รับการอนุมัติแล้ว。
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>ขั้นตอนต่อไป:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. ดาวน์โหลดและพิมพ์ฉลากคืนสินค้าด้านล่าง<br/>
          2. บรรจุสินค้าอย่างปลอดภัยในบรรจุภัณฑ์เดิมหากเป็นไปได้<br/>
          3. ติดฉลากคืนสินค้าไว้ด้านนอกของกล่อง<br/>
          4. ส่งไปยังสถานที่จัดส่งใกล้คุณที่สุด
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดาวน์โหลดฉลากคืนสินค้า
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>หมายเลขติดตามการคืนสินค้า:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>สำคัญ:</strong> กรุณาส่งคืนภายใน 7 วันเพื่อให้การคืนเงินของคุณได้รับการดำเนินการอย่างรวดเร็ว
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เมื่อเราได้รับและตรวจสอบการคืนสินค้าของคุณ เราจะดำเนินการคืนเงินไปยังวิธีการชำระเงินเดิมของคุณ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การคืนสินค้าได้รับการอนุมัติ - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

การขอคืนสินค้าสำหรับคำสั่งซื้อ #{{ order_number }} ของคุณได้รับการอนุมัติแล้ว。

ขั้นตอนต่อไป:
1. ดาวน์โหลดและพิมพ์ฉลากคืนสินค้า
2. บรรจุสินค้าอย่างปลอดภัยในบรรจุภัณฑ์เดิมหากเป็นไปได้
3. ติดฉลากคืนสินค้าไว้ด้านนอกของกล่อง
4. ส่งไปยังสถานที่จัดส่งใกล้คุณที่สุด

{% if return_label_url %}ดาวน์โหลดฉลากคืนสินค้า: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}หมายเลขติดตามการคืนสินค้า: {{ return_tracking_number }}{% endif %}

สำคัญ: กรุณาส่งคืนภายใน 7 วันเพื่อให้การคืนเงินของคุณได้รับการดำเนินการอย่างรวดเร็ว

เมื่อเราได้รับและตรวจสอบการคืนสินค้าของคุณ เราจะดำเนินการคืนเงินไปยังวิธีการชำระเงินเดิมของคุณ
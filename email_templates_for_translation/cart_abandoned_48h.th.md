---
template_type: cart_abandoned_48h
category: Cart Recovery
---

# Email Template: cart_abandoned_48h

## Subject
โอกาสสุดท้าย! ตะกร้าของคุณจะหมดอายุใน 24 ชั่วโมง - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="#92400e" align="center">
          ⏰ โอกาสสุดท้าย - ตะกร้าจะหมดอายุใน 24 ชั่วโมง
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          อย่าพลาดเลยนะ {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          นี่คือการเตือนสุดท้ายของคุณ ตะกร้าของคุณจะหมดอายุใน 24 ชั่วโมง และเราไม่สามารถรักษาสินค้าเหล่านี้ไว้ได้นานขึ้นไปอีก
        </mj-text>

        <mj-spacer height="20px" />

        {% for item in cart_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ item.product_image }}" alt="{{ item.product_name }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="20px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          ยอดรวม: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ติดต่อสั่งซื้อก่อนที่จะสายเกินไป
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          มีคำถามไหม? ทีมงานของเราพร้อมช่วยเหลือ: <a href="{{ support_url }}">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⏰ โอกาสสุดท้าย - ตะกร้าจะหมดอายุใน 24 ชั่วโมง

อย่าพลาดเลยนะ {{ customer_name }}!

นี่คือการเตือนสุดท้ายของคุณ ตะกร้าของคุณจะหมดอายุใน 24 ชั่วโมง และเราไม่สามารถรักษาสินค้าเหล่านี้ไว้ได้นานขึ้นไปอีก

ตะกร้าของคุณ:
{% for item in cart_items %}
- {{ item.product_name }}
  {{ item.quantity }} × {{ item.price }}
{% endfor %}

ยอดรวม: {{ cart_total }}

ติดต่อสั่งซื้อก่อนที่จะสายเกินไป: {{ cart_url }}

มีคำถามไหม? ทีมงานของเราพร้อมช่วยเหลือ: {{ support_url }}

---
นี่คือการเตือนสุดท้ายสำหรับตะกร้า #{{ cart_id }}.
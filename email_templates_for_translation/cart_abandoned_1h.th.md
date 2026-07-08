---
template_type: cart_abandoned_1h
category: Cart Recovery
---

# Email Template: cart_abandoned_1h

## Subject
ตะกร้าของคุณกำลังรออยู่! ให้เสร็จสิ้นการสั่งซื้อของคุณ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คุณได้ทิ้ง {{ cart_item_count }} สินค้า{{ cart_item_count|pluralize }} ในตะกร้าของคุณ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj:text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราสังเกตเห็นว่าคุณยังไม่ได้ทำการสั่งซื้อ สินค้าของคุณยังคงรออยู่ในตะกร้า!
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
              Qty: {{ item.quantity }} × {{ item.price }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="20px" />

        <mj-text font-size="18px" font-weight="bold" align="right" color="{{ theme.color.text|default:'#1f2937' }}">
          รวม: {{ cart_total }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ cart_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ให้เสร็จสิ้นการสั่งซื้อของคุณ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ต้องการความช่วยเหลือ? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ติดต่อทีมสนับสนุนของเรา</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
คุณได้ทิ้ง {{ cart_item_count }} สินค้า{{ cart_item_count|pluralize }} ในตะกร้าของคุณ

สวัสดี {{ customer_name }},

เราสังเกตเห็นว่าคุณยังไม่ได้ทำการสั่งซื้อ สินค้าของคุณยังคงรออยู่ในตะกร้า!

ตะกร้าของคุณ:
{% for item in cart_items %}
- {{ item.product_name }}
  Qty: {{ item.quantity }} × {{ item.price }}
{% endfor %}

รวม: {{ cart_total }}

ให้เสร็จสิ้นการสั่งซื้อ: {{ cart_url }}

ต้องการความช่วยเหลือ? ติดต่อทีมสนับสนุนของเรา: {{ support_url }}

---
คุณได้รับอีเมลนี้เพราะคุณเพิ่มสินค้าในตะกร้าของคุณที่ {{ shop_name }}.
เพื่อหยุดการรับการแจ้งเตือนตะกร้า โปรดเข้าชม: {{ preferences_url }}
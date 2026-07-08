---
template_type: wishlist_price_drop
category: Wishlist
---

# Email Template: wishlist_price_drop

## Subject
🔥 แจ้งเตือนการลดราคา: {{ product_name }} ตอนนี้ลด {{ discount_percentage }}% แล้ว!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🔥 แจ้งเตือนการลดราคา!
        </mj-text>
        <mj-text font-size="18px" color="#047857" align="center">
          ประหยัด {{ discount_percentage }}% สำหรับสินค้าในรายการต้องการของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข่าวดี {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สินค้าในรายการต้องการของคุณเพิ่งลดราคาลง! อย่าพลาดโอกาสในการประหยัด
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column width="35%">
            <mj-image src="{{ product_image }}" alt="{{ product_name }}" border-radius="8px" />
          </mj-column>
          <mj-column width="65%">
            <mj-text font-weight="bold" font-size="18px" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ product_name }}
            </mj-text>
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              ราคาเดิม: <span style="text-decoration: line-through;">{{ original_price }}</span>
            </mj-text>
            <mj-text font-size="24px" font-weight="bold" color="#059669">
              ราคาปัจจุบัน: {{ new_price }}
            </mj-text>
            <mj-text font-size="16px" font-weight="bold" color="#dc2626">
              ประหยัด {{ savings_amount }} ({{ discount_percentage }}% OFF)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#059669" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ซื้อตอนนี้ & ประหยัด {{ discount_percentage }}%
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              ⏰ <strong>ระยะเวลาจำกัด:</strong> การลดราคานี้จะไม่สิ้นสุดตลอดไป ราคาอาจเพิ่มขึ้นได้ทุกเมื่อ!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ลบออกจากรายการต้องการ: <a href="{{ remove_wishlist_url }}">คลิกที่นี่</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔥 แจ้งเตือนการลดราคา!
ประหยัด {{ discount_percentage }}% สำหรับสินค้าในรายการต้องการของคุณ

ข่าวดี {{ customer_name }}!

สินค้าในรายการต้องการของคุณเพิ่งลดราคาลง! อย่าพลาดโอกาสในการประหยัด

{{ product_name }}
ราคาเดิม: {{ original_price }}
ตอนนี้: {{ new_price }}
ประหยัด {{ savings_amount }} ({{ discount_percentage }}% OFF)

ซื้อตอนนี้ & ประหยัด {{ discount_percentage }}%: {{ product_url }}

⏰ ระยะเวลาจำกัด: การลดราคานี้จะไม่สิ้นสุดตลอดไป ราคาอาจเพิ่มขึ้นได้ทุกเมื่อ!

ลบออกจากรายการต้องการ: {{ remove_wishlist_url }}
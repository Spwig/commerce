---
template_type: back_in_stock_low_stock_warning
category: Stock Notifications
---

# Email Template: back_in_stock_low_stock_warning

## Subject
⚠️ {{ product_name }} กลับมาแล้วแต่ขายเร็ว! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ สินค้ามีจำนวนจำกัด - อย่ารอช้า!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }} กลับมาวางจำหน่ายแล้ว!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณ {{ customer_name }} ครับ/ค่ะ,
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! สินค้าที่คุณรอคอยกลับมาวางจำหน่ายอีกครั้ง แต่รีบหน่อยนะ - เราเหลือเพียง {{ stock_remaining }} หน่วยเท่านั้น!
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
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ product_description }}
            </mj-text>
            <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}">
              {{ product_price }}
            </mj-text>
            {% if variant_name %}
            <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              แบบ: {{ variant_name }}
            </mj-text>
            {% endif %}
            <mj-spacer height="10px" />
            <mj-text font-size="14px" color="#dc2626" font-weight="bold">
              ⚠️ คงเหลือเพียง {{ stock_remaining }} หน่วยเท่านั้น!
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ product_url }}" background-color="#dc2626" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          ซื้อตอนนี้ก่อนของจะหมด
        </mj-button>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" align="center">
              🔥 <strong>สินค้านี้ขายหมด {{ times_sold_out }} ครั้งในช่วงหนึ่งเดือนที่ผ่านมา!</strong><br/>
              อย่าพลาดอีกครั้ง - ตั้งสินค้าทันทีขณะที่ยังมีสต็อก
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          ไม่สนใจอีกต่อไป? <a href="{{ unsubscribe_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ยกเลิกการแจ้งเตือนนี้</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ สินค้ามีจำนวนจำกัด - อย่ารอช้า!

{{ product_name }} กลับมาวางจำหน่ายแล้ว!

Hi {{ customer_name }},

Great news! The item you were waiting for is back in stock. But hurry - we only have {{ stock_remaining }} unit{{ stock_remaining|pluralize }} left!

PRODUCT:
{{ product_name }}
{{ product_description }}
Price: {{ product_price }}
{% if variant_name %}Variant: {{ variant_name }}{% endif %}

⚠️ ONLY {{ stock_remaining }} LEFT IN STOCK!

Buy now before it's gone: {{ product_url }}

🔥 This product sold out {{ times_sold_out }} time{{ times_sold_out|pluralize }} in the past month!
Don't miss out again - order now while supplies last.

Not interested anymore? Unsubscribe: {{ unsubscribe_url }}
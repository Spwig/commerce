---
template_type: pos_low_inventory_alert
category: POS
---

# Email Template: pos_low_inventory_alert

## Subject
📦 การแจ้งเตือนสต็อกต่ำ: มีสินค้า {{ product_count }} ชิ้นที่กำลังหมดสต็อกที่ {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          📦 การแจ้งเตือนสต็อกต่ำ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สต็อกกำลังหมด
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          มีสินค้า {{ product_count }} ชิ้น {{ product_count|pluralize:'is,are' }} กำลังหมดสต็อกที่ {{ location_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการแจ้งเตือน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>สถานที่:</strong> {{ location_name }}<br/>
              <strong>สินค้าที่ได้รับผลกระทบ:</strong> {{ product_count }}<br/>
              <strong>ตรวจพบ:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สินค้าที่มีสต็อกต่ำ:
        </mj-text>

        {% for item in low_stock_items %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ item.product_name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {% if item.variant_name %}<strong>Version:</strong> {{ item.variant_name }}<br/>{% endif %}
              <strong>สต็อกปัจจุบัน:</strong> <span style="color: #dc2626; font-weight: bold;">{{ item.current_stock }}</span><br/>
              <strong>จุดสั่งซื้อใหม่:</strong> {{ item.reorder_point }}<br/>
              <strong>SKU:</strong> {{ item.sku }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อแนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • สร้างใบสั่งซื้อสำหรับสินค้าที่มีสต็อกต่ำ<br/>
          • โอนสต็อกจากสถานที่อื่น<br/>
          • อัปเดตจุดสั่งซื้อใหม่หากจำเป็น<br/>
          • พิจารณาปรับระดับสต็อกมาตรฐาน
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ inventory_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูสต็อก
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ purchase_orders_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          สร้างใบสั่งซื้อ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 การแจ้งเตือนสต็อกต่ำ

สต็อกกำลังหมด

มีสินค้า {{ product_count }} ชิ้น {{ product_count|pluralize:'is,are' }} กำลังหมดสต็อกที่ {{ location_name }}.

รายละเอียดการแจ้งเตือน:
- สถานที่: {{ location_name }}
- สินค้าที่ได้รับผลกระทบ: {{ product_count }}
- ตรวจพบ: {{ detected_at }}

สินค้าที่มีสต็อกต่ำ:
{% for item in low_stock_items %}
{{ item.product_name }}
{% if item.variant_name %}Version: {{ item.variant_name }}{% endif %}
สต็อกปัจจุบัน: {{ item.current_stock }}
จุดสั่งซื้อใหม่: {{ item.reorder_point }}
SKU: {{ item.sku }}

{% endfor %}

ข้อแนะนำ:
• สร้างใบสั่งซื้อสำหรับสินค้าที่มีสต็อกต่ำ
• โอนสต็อกจากสถานที่อื่น
• อัปเดตจุดสั่งซื้อใหม่หากจำเป็น
• พิจารณาปรับระดับสต็อกมาตรฐาน

ดูสต็อก: {{ inventory_url }}
สร้างใบสั่งซื้อ: {{ purchase_orders_url }}
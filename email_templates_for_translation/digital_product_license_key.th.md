---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
ใบอนุญาตซอฟต์แวร์ของคุณ - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ใบอนุญาตของคุณพร้อมใช้งานแล้ว
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text>
          ขอบคุณสำหรับการซื้อ {{ product_name }}! นี่คือใบอนุญาตของคุณสำหรับการเปิดใช้งาน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          ใบอนุญาตของคุณ
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          กดเพื่อคัดลอกหรือจดจำไว้ดีๆ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          รายละเอียดใบอนุญาต:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ผลิตภัณฑ์: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • รุ่น: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ประเภทใบอนุญาต: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • จำนวนการเปิดใช้งานสูงสุด: {{ max_activations }} เครื่อง
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ความถูกต้อง: ใบอนุญาตตลอดชีวิต
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ใช้ได้ถึง: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          วิธีการเปิดใช้งาน:
        </mj-text>
        <mj-text font-size="14px">
          1. ดาวน์โหลดและติดตั้งซอฟต์แวร์
        </mj-text>
        <mj-text font-size="14px">
          2. เปิดแอปพลิเคชัน
        </mj-text>
        <mj-text font-size="14px">
          3. ใส่ใบอนุญาตของคุณเมื่อถูกขอ
        </mj-text>
        <mj-text font-size="14px">
          4. กด "เปิดใช้งาน" เพื่อสรุปขั้นตอน
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          ดาวน์โหลดซอฟต์แวร์
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ ข้อควรระวัง:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • รักษาอีเมลนี้ไว้ดีๆ - คุณจะต้องใช้ใบอนุญาตสำหรับการติดตั้งใหม่
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • อย่าแบ่งปันใบอนุญาตของคุณกับผู้อื่น
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • คุณสามารถปิดการใช้งานอุปกรณ์จากแดชบอร์ดบัญชีของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ต้องการความช่วยเหลือในการเปิดใช้งาน? ติดต่อ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ใบอนุญาตของคุณพร้อมใช้งานแล้ว

สวัสดี {{ customer_name }},

ขอบคุณสำหรับการซื้อ {{ product_name }}! นี่คือใบอนุญาตของคุณสำหรับการเปิดใช้งาน

ใบอนุญาตของคุณ:
{{ license_key }}

รายละเอียดใบอนุญาต:
• ผลิตภัณฑ์: {{ product_name }}
• รุ่น: {{ product_version }}
• ประเภทใบอนุญาต: {{ license_type }}
• จำนวนการเปิดใช้งานสูงสุด: {{ max_activations }} เครื่อง
{% if is_lifetime %}• ความถูกต้อง: ใบอนุญาตตลอดชีวิต{% else %}• ใช้ได้ถึง: {{ expiration_date }}{% endif %}

วิธีการเปิดใช้งาน:
1. ดาวน์โหลดและติดตั้งซอฟต์แวร์
2. เปิดแอปพลิเคชัน
3. ใส่ใบอนุญาตของคุณเมื่อถูกขอ
4. กด "เปิดใช้งาน" เพื่อสรุปขั้นตอน

{% if download_url %}ดาวน์โหลดซอฟต์แวร์: {{ download_url }}

{% endif %}ข้อควรระวัง:
• รักษาอีเมลนี้ไว้ดีๆ - คุณจะต้องใช้ใบอนุญาตสำหรับการติดตั้งใหม่
• อย่าแบ่งปันใบอนุญาตของคุณกับผู้อื่น
• คุณสามารถปิดการใช้งานอุปกรณ์จากแดชบอร์ดบัญชีของคุณ

ต้องการความช่วยเหลือในการเปิดใช้งาน? ติดต่อ {{ support_email }}
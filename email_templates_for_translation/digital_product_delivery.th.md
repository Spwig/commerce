---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
สินค้าดิจิทัลของคุณพร้อมใช้งานแล้ว - คำสั่งซื้อ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          สินค้าดิจิทัลของคุณพร้อมใช้งานแล้ว!
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
          ขอบคุณสำหรับการซื้อสินค้า! สินค้าดิจิทัลของคุณพร้อมสำหรับการดาวน์โหลดแล้ว。
        </mj-text>
        <mj-text font-weight="bold">
          คำสั่งซื้อ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          รุ่น: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ขนาดไฟล์: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          ดาวน์โหลดทันที
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>ข้อมูลสำคัญ:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • คุณสามารถดาวน์โหลดสินค้านี้ได้ {{ download_limit }} ครั้ง
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • ลิงก์ดาวน์โหลดจะหมดอายุใน {{ expiration_days }} วัน
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • โปรดเก็บอีเมลนี้ไว้เพื่อใช้อ้างอิงในอนาคต
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          ต้องการความช่วยเหลือ? ติดต่อทีมสนับสนุนของเราที่ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
สินค้าดิจิทัลของคุณพร้อมใช้งานแล้ว!

สวัสดี {{ customer_name }},

ขอบคุณสำหรับการซื้อสินค้า! สินค้าดิจิทัลของคุณพร้อมสำหรับการดาวน์โหลดแล้ว。

คำสั่งซื้อ #{{ order_number }}

สินค้า: {{ product_name }}
รุ่น: {{ product_version }}
ขนาดไฟล์: {{ file_size }}

ดาวน์โหลดสินค้าของคุณได้ที่:
{{ download_url }}

ข้อมูลสำคัญ:
{% if download_limit %}• คุณสามารถดาวน์โหลดสินค้านี้ได้ {{ download_limit }} ครั้ง
{% endif %}{% if expiration_days %}• ลิงก์ดาวน์โหลดจะหมดอายุใน {{ expiration_days }} วัน
{% endif %}• โปรดเก็บอีเมลนี้ไว้เพื่อใช้อ้างอิงในอนาคต

ต้องการความช่วยเหลือ? ติดต่อทีมสนับสนุนของเราที่ {{ support_email }}
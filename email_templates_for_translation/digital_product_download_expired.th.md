---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
ลิงก์ดาวน์โหลดหมดอายุ - คำสั่งซื้อ #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ลิงก์ดาวน์โหลดหมดอายุ
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
          ลิงก์ดาวน์โหลดสำหรับ <strong>{{ product_name }}</strong> จากคำสั่งซื้อ #{{ order_number }} ของคุณได้หมดอายุแล้ว。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          ลิงก์ดาวน์โหลดจะหมดอายุหลังจาก {{ expiration_days }} วันนับจากวันที่ซื้อเพื่อความปลอดภัย。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          ต้องการลิงก์ดาวน์โหลดใหม่?
        </mj-text>
        <mj-text>
          คุณสามารถขอรับลิงก์ดาวน์โหลดใหม่ได้โดยการเข้าสู่บัญชีของคุณ หรือติดต่อทีมสนับสนุนของเรา。
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          ไปยังบัญชีของฉัน
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          มีคำถาม? ติดต่อ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ลิงก์ดาวน์โหลดหมดอายุ

สวัสดี {{ customer_name }},

ลิงก์ดาวน์โหลดสำหรับ {{ product_name }} จากคำสั่งซื้อ #{{ order_number }} ของคุณได้หมดอายุแล้ว。

ลิงก์ดาวน์โหลดจะหมดอายุหลังจาก {{ expiration_days }} วันนับจากวันที่ซื้อเพื่อความปลอดภัย。

ต้องการลิงก์ดาวน์โหลดใหม่?
คุณสามารถขอรับลิงก์ดาวน์โหลดใหม่ได้โดยการเข้าสู่บัญชีของคุณ หรือติดต่อทีมสนับสนุนของเรา。

ไปยังบัญชีของฉัน: {{ account_url }}

มีคำถาม? ติดต่อ {{ support_email }}
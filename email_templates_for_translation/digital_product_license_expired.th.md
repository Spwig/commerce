---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
ใบอนุญาตใกล้หมดอายุ - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          ใบอนุญาตใกล้หมดอายุ
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
          ใบอนุญาตของคุณสำหรับ <strong>{{ product_name }}</strong> จะหมดอายุเร็ว ๆ นี้
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>License Key:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Expires:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>Days Remaining:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          ต่ออายุใบอนุญาตของคุณ
        </mj-text>
        <mj-text>
          ต่ออายุใบอนุญาตของคุณวันนี้เพื่อใช้งาน {{ product_name }} ต่อ
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          ต่ออายุทันที
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          มีคำถามเกี่ยวกับการต่ออายุ? ติดต่อ {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ใบอนุญาตใกล้หมดอายุ

สวัสดี {{ customer_name }},

ใบอนุญาตของคุณสำหรับ {{ product_name }} จะหมดอายุเร็ว ๆ นี้

รายละเอียดใบอนุญาต:
• License Key: {{ license_key }}
• Expires: {{ expiration_date }}
• Days Remaining: {{ days_remaining }}

ต่ออายุใบอนุญาตของคุณ:
ต่ออายุใบอนุญาตของคุณวันนี้เพื่อใช้งาน {{ product_name }} ต่อ

ต่ออายุทันที: {{ renewal_url }}

มีคำถามเกี่ยวกับการต่ออายุ? ติดต่อ {{ support_email }}
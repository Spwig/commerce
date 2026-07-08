---
template_type: license_maintenance_renewal
category: License
---

# Email Template: license_maintenance_renewal

## Subject
การต่ออายุการบำรุงรักษา - หมายเลขคำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          การต่ออายุการบำรุงรักษา!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          หมายเลขคำสั่งซื้อ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          สวัสดี {{ customer_name }},
        </mj-text>
        <mj-text>
          การสมัครสมาชิกการบำรุงรักษา Spwig ของคุณได้รับการต่ออายุอย่างสำเร็จ คุณจะยังคงได้รับการอัปเดตแพลตฟอร์ม, การแก้ไขความปลอดภัย และคุณสมบัติใหม่ๆ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สรุปการต่ออายุ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          คีย์ใบอนุญาต: {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          วันหมดอายุการบำรุงรักษา: {{ renewal_expires_at }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          หมายเลขคำสั่งซื้อ: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Included -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          สิ่งที่รวมอยู่ในแพ็กเกจ
        </mj-text>
        <mj-text font-size="14px">
          การบำรุงรักษาที่เปิดใช้งานของคุณให้คุณเข้าถึง:
        </mj-text>
        <mj-text font-size="14px" padding-top="5px">
          - การอัปเดตคุณสมบัติแพลตฟอร์มและปรับปรุง
        </mj-text>
        <mj-text font-size="14px">
          - การแก้ไขความปลอดภัยและข้อบกพร่อง
        </mj-text>
        <mj-text font-size="14px">
          - การปล่อยส่วนประกอบใหม่ผ่านเซิร์ฟเวอร์อัปเกรด
        </mj-text>
        <mj-text font-size="14px">
          - การสนับสนุนทางเทคนิค
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          ไม่มีการดำเนินการใดที่จำเป็นจากคุณ การอัปเดตจะยังคงสามารถเข้าถึงได้ผ่านระบบอัปเดตส่วนประกอบในแดชบอร์ดผู้ดูแลของคุณ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
การต่ออายุการบำรุงรักษา!

หมายเลขคำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

การสมัครสมาชิกการบำรุงรักษา Spwig ของคุณได้รับการต่ออายุอย่างสำเร็จ คุณจะยังคงได้รับการอัปเดตแพลตฟอร์ม, การแก้ไขความปลอดภัย และคุณสมบัติใหม่ๆ

สรุปการต่ออายุ:
- คีย์ใบอนุญาต: {{ license_key }}
- วันหมดอายุการบำรุงรักษา: {{ renewal_expires_at }}
- หมายเลขคำสั่งซื้อ: {{ order_number }}

สิ่งที่รวมอยู่ในแพ็กเกจ:
- การอัปเดตคุณสมบัติแพลตฟอร์มและปรับปรุง
- การแก้ไขความปลอดภัยและข้อบกพร่อง
- การปล่อยส่วนประกอบใหม่ผ่านเซิร์ฟเวอร์อัปเกรด
- การสนับสนุนทางเทคนิค

ไม่มีการดำเนินการใดที่จำเป็นจากคุณ การอัปเดตจะยังคงสามารถเข้าถึงได้ผ่านระบบอัปเดตส่วนประกอบในแดชบอร์ดผู้ดูแลของคุณ

ต้องการความช่วยเหลือ? ติดต่อ {{ support_email }}
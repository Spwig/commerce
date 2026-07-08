---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ การกู้คืนสำรองข้อมูลสำเร็จ - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ การกู้คืนสำรองข้อมูลสำเร็จ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การดำเนินการกู้คืนสำรองข้อมูลของคุณสำเร็จแล้ว ข้อมูลร้านค้าของคุณได้รับการกู้คืนแล้ว
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการกู้คืน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ไฟล์สำรอง:</strong> {{ backup_filename }}<br/>
              <strong>วันที่สำรอง:</strong> {{ backup_date }}<br/>
              <strong>เริ่มต้น:</strong> {{ restore_started_at }}<br/>
              <strong>เสร็จสิ้น:</strong> {{ restore_completed_at }}<br/>
              <strong>ระยะเวลา:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ ขั้นตอนสำคัญถัดไป:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. ตรวจสอบว่าร้านค้าของคุณทำงานได้ตามปกติ<br/>
              2. ตรวจสอบข้อมูลสำคัญ (สินค้า, คำสั่งซื้อ, ลูกค้า)<br/>
              3. ลบแคชหากจำเป็น<br/>
              4. ทดสอบกระบวนการทำงานสำคัญ (การชำระเงิน, การเข้าถึงแดชบอร์ดผู้ดูแลระบบ)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ไปยังแดชบอร์ดผู้ดูแลระบบ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP RESTORE COMPLETED

Hi {{ admin_name }},

Your backup restore operation has completed successfully. Your store data has been restored.

RESTORE DETAILS:
- Backup File: {{ backup_filename }}
- Backup Date: {{ backup_date }}
- Started: {{ restore_started_at }}
- Completed: {{ restore_completed_at }}
- Duration: {{ restore_duration }}

⚠️ IMPORTANT NEXT STEPS:
1. Verify your store is functioning correctly
2. Check key data (products, orders, customers)
3. Clear cache if needed
4. Test critical workflows (checkout, admin access)

Go to admin dashboard: {{ admin_dashboard_url }}
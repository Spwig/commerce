---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 สำคัญ: การกู้คืนสำรองข้อมูลล้มเหลว - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 สำคัญ: การกู้คืนสำรองข้อมูลล้มเหลว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          คุณ {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การดำเนินการกู้คืนสำรองข้อมูลสำคัญได้ล้มเหลว ร้านค้าของคุณอาจอยู่ในสถานะที่ไม่สอดคล้องกันและต้องการความสนใจทันที
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              รายละเอียดการกู้คืน:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>ไฟล์สำรอง:</strong> {{ backup_filename }}<br/>
              <strong>เริ่มต้น:</strong> {{ restore_started_at }}<br/>
              <strong>ล้มเหลว:</strong> {{ restore_failed_at }}<br/>
              <strong>ระยะเวลา:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          รายละเอียดข้อผิดพลาด:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 การดำเนินการทันทีจำเป็น:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>ห้าม</strong> ทำการเปลี่ยนแปลงใดๆ ที่ร้านค้า<br/>
              2. ตรวจสอบการเชื่อมต่อและความสมบูรณ์ของฐานข้อมูล<br/>
              3. ตรวจสอบบันทึกข้อผิดพลาดเพื่อดูรายละเอียดการเรียกข้อมูล<br/>
              4. ติดต่อฝ่ายสนับสนุนทางเทคนิคทันที<br/>
              5. พิจารณาการย้อนกลับไปยังสถานะที่ดีที่สุดที่ทราบก่อนหน้านี้
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูบันทึกการกู้คืน
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          ติดต่อฝ่ายสนับสนุนฉุกเฉิน
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 สำคัญ: การกู้คืนสำรองข้อมูลล้มเหลว

คุณ {{ admin_name }},

การดำเนินการกู้คืนสำรองข้อมูลสำคัญได้ล้มเหลว ร้านค้าของคุณอาจอยู่ในสถานะที่ไม่สอดคล้องกันและต้องการความสนใจทันที

รายละเอียดการกู้คืน:
- ไฟล์สำรอง: {{ backup_filename }}
- เริ่มต้น: {{ restore_started_at }}
- ล้มเหลว: {{ restore_failed_at }}
- ระยะเวลา: {{ restore_duration }}

รายละเอียดข้อผิดพลาด:
{{ error_message }}

🚨 การดำเนินการทันทีจำเป็น:
1. ห้ามทำการเปลี่ยนแปลงใดๆ ที่ร้านค้า
2. ตรวจสอบการเชื่อมต่อและความสมบูรณ์ของฐานข้อมูล
3. ตรวจสอบบันทึกข้อผิดพลาดเพื่อดูรายละเอียดการเรียกข้อมูล
4. ติดต่อฝ่ายสนับสนุนทางเทคนิคทันที
5. พิจารณาการย้อนกลับไปยังสถานะที่ดีที่สุดที่ทราบก่อนหน้านี้

ดูบันทึกการกู้คืน: {{ admin_backup_url }}
ติดต่อฝ่ายสนับสนุนฉุกเฉิน: {{ support_url }}
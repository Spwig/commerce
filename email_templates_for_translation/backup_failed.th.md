---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 ฉุกเฉิน: การสำรองข้อมูลล้มเหลว - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ การสำรองข้อมูลล้มเหลว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          สวัสดี {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การสำรองข้อมูลสำคัญสำหรับร้านค้า {{ shop_name }} ของคุณได้ล้มเหลว จำเป็นต้องดำเนินการทันทีเพื่อความปลอดภัยของข้อมูล
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              รายละเอียดการสำรองข้อมูล:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>ประเภทการสำรองข้อมูล:</strong> {{ backup_type }}<br/>
              <strong>เริ่มต้น:</strong> {{ backup_started_at }}<br/>
              <strong>ล้มเหลว:</strong> {{ backup_failed_at }}<br/>
              <strong>ระยะเวลา:</strong> {{ backup_duration }}
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

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          คำแนะนำในการแก้ไข:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. ตรวจสอบพื้นที่จัดเก็บข้อมูลที่ใช้ได้ในเซิร์ฟเวอร์ของคุณ<br/>
          2. ตรวจสอบการเชื่อมต่อฐานข้อมูล<br/>
          3. ตรวจสอบบันทึกข้อผิดพลาดเพื่อดูรายละเอียดการเรียกขั้นตอน<br/>
          4. ลองสำรองข้อมูลอีกครั้งด้วยตนเอง หรือรอการสำรองข้อมูลครั้งต่อไป<br/>
          5. หากปัญหายังคงอยู่ โปรดติดต่อฝ่ายสนับสนุน
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูบันทึกการสำรองข้อมูล
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          ลองสำรองข้อมูลอีกครั้ง
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>การสำรองข้อมูลครั้งสุดท้ายที่สำเร็จ:</strong> {{ last_successful_backup }}<br/>
          <strong>การสำรองข้อมูลครั้งถัดไป:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 ฉุกเฉิน: การสำรองข้อมูลล้มเหลว

สวัสดี {{ admin_name }},

การสำรองข้อมูลสำคัญสำหรับร้านค้า {{ shop_name }} ของคุณได้ล้มเหลว จำเป็นต้องดำเนินการทันทีเพื่อความปลอดภัยของข้อมูล

รายละเอียดการสำรองข้อมูล:
- ประเภทการสำรองข้อมูล: {{ backup_type }}
- เริ่มต้น: {{ backup_started_at }}
- ล้มเหลว: {{ backup_failed_at }}
- ระยะเวลา: {{ backup_duration }}

รายละเอียดข้อผิดพลาด:
{{ error_message }}

คำแนะนำในการแก้ไข:
1. ตรวจสอบพื้นที่จัดเก็บข้อมูลที่ใช้ได้ในเซิร์ฟเวอร์ของคุณ
2. ตรวจสอบการเชื่อมต่อฐานข้อมูล
3. ตรวจสอบบันทึกข้อผิดพลาดเพื่อดูรายละเอียดการเรียกขั้นตอน
4. ลองสำรองข้อมูลอีกครั้งด้วยตนเอง หรือรอการสำรองข้อมูลครั้งต่อไป
5. หากปัญหายังคงอยู่ โปรดติดต่อฝ่ายสนับสนุน

ดูบันทึกการสำรองข้อมูล: {{ admin_backup_url }}
ลองสำรองข้อมูลอีกครั้ง: {{ retry_backup_url }}

การสำรองข้อมูลครั้งสุดท้ายที่สำเร็จ: {{ last_successful_backup }}
การสำรองข้อมูลครังถัดไป: {{ next_scheduled_backup }}

---
นี่คือการแจ้งเตือนระบบสำคัญสำหรับผู้ดูแลระบบ {{ shop_name }}

ข้อควรระวัง: รักษาทุกส่วนของ Django template syntax ({{ }}, {% %}), ทุก MJML tags (<mj-*>), ทุก HTML attributes และทุกอีโมจิไว้เหมือนเดิม


---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
ปัญหาผู้ให้บริการชำระเงิน - SDK ของ {{ provider_name }} ไม่สามารถโหลดได้

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          ปัญหาผู้ให้บริการชำระเงิน
        </mj-text>
        <mj-text>
          SDK สำหรับการชำระเงินของ {{ provider_name }} ไม่สามารถโหลดได้ขณะที่ลูกค้ากำลังดำเนินการชำระเงิน อาจบ่งบอกถึงปัญหาการให้บริการของผู้ให้บริการ
        </mj-text>
        <mj-text>
          <strong>ผู้ให้บริการ:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>ประเภทข้อผิดพลาด:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>เวลา:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>จำนวนความล้มเหลว (ชั่วโมงที่แล้ว):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          การแจ้งเตือนนี้ถูกจำกัดการส่งเพียงหนึ่งครั้งต่อผู้ให้บริการต่อชั่วโมง หากปัญหายังคงเกิดขึ้น กรุณาตรวจสอบแดชบอร์ดของผู้ให้บริการหรือติดต่อฝ่ายสนับสนุนของพวกเขา
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          ดูการตั้งค่าการชำระเงิน
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ปัญหาผู้ให้บริการชำระเงิน

SDK สำหรับการชำระเงินของ {{ provider_name }} ไม่สามารถโหลดได้ขณะที่ลูกค้ากำลังดำเนินการชำระเงิน อาจบ่งบอกถึงปัญหาการให้บริการของผู้ให้บริการ

ผู้ให้บริการ: {{ provider_name }}
ประเภทข้อผิดพลาด: {{ error_type }}
เวลา: {{ timestamp }}
จำนวนความล้มเหลว (ชั่วโมงที่แล้ว): {{ failure_count }}

การแจ้งเตือนนี้ถูกจำกัดการส่งเพียงหนึ่งครั้งต่อผู้ให้บริการต่อชั่วโมง หากปัญหายังคงเกิดขึ้น กรุณาตรวจสอบแดชบอร์ดของผู้ให้บริการหรือติดต่อฝ่ายสนับสนุนของพวกเขา

ดูการตั้งค่าการชำระเงิน: {{ admin_url }}
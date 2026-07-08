---
template_type: subscription_dunning_final_notice
category: Subscriptions
---

# Email Template: subscription_dunning_final_notice

## Subject
⚠️ การแจ้งเตือนสุดท้าย: การสมัครสมาชิกของคุณจะถูกยกเลิกใน {{ days_until_cancellation }} วัน

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          ⚠️ การแจ้งเตือนสุดท้าย
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การยกเลิกการสมัครสมาชิกใกล้เข้ามาแล้ว
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          คุณคือ {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          นี่คือการแจ้งเตือนสุดท้ายของคุณ เรายังไม่สามารถดำเนินการชำระเงินสำหรับการสมัครสมาชิก {{ plan_name }} ของคุณได้ หากเราไม่ได้รับการชำระเงินภายใน {{ days_until_cancellation }} วัน การสมัครสมาชิกของคุณจะถูกยกเลิก
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ การชำระเงินล้มเหลว - ต้องดำเนินการ
            </mj-text>
            <mj-text color="#991b1b">
              <strong>การสมัครสมาชิก:</strong> {{ plan_name }}<br/>
              <strong>จำนวนเงินที่ต้องชำระ:</strong> {{ amount_due }}<br/>
              <strong>จำนวนครั้งที่ชำระล้มเหลว:</strong> {{ retry_count }}<br/>
              <strong>ครั้งสุดท้ายที่พยายามชำระ:</strong> {{ last_retry_date }}<br/>
              <strong>วันที่ยกเลิก:</strong> <span style="font-weight: bold; font-size: 16px;">{{ cancellation_date }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อผิดพลาดในการชำระเงิน:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ payment_error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สิ่งที่จะเกิดขึ้น:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          หากไม่ได้รับการชำระเงินภายใน {{ cancellation_date }}:<br/>
          • การสมัครสมาชิกของคุณจะถูกยกเลิก<br/>
          • คุณจะสูญเสียสิทธิ์ในการเข้าถึงประโยชน์ทั้งหมดของสมาชิก<br/>
          • ข้อมูลของคุณอาจถูกลบ (ดูนโยบายการรักษาข้อมูล)<br/>
          • คุณจะต้องสมัครสมาชิกอีกครั้งเพื่อเริ่มต้นการเข้าถึงใหม่
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          อัปเดตวิธีการชำระเงินทันที
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_payment_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          อัปเดตวิธีการชำระเงิน
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ปัญหาที่พบบ่อยและวิธีแก้ไข:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • <strong>บัตรหมดอายุ:</strong> อัปเดตด้วยบัตรเครดิตที่ใช้งานได้<br/>
          • <strong>ยอดเงินไม่เพียงพอ:</strong> ตรวจสอบให้แน่ใจว่ายอดเงินเพียงพอ<br/>
          • <strong>บัตรถูกปฏิเสธ:</strong> ติดต่อธนาคารของคุณหรือใช้บัตรอื่น<br/>
          • <strong>ที่อยู่ไม่ตรงกัน:</strong> ตรวจสอบให้แน่ใจว่าที่อยู่ในการออกใบแจ้งหนี้ตรงกับบัตร
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" font-weight="bold">
              ต้องการความช่วยเหลือหรือไม่?
            </mj-text>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              หากคุณกำลังประสบปัญหาในการชำระเงินหรือต้องการความช่วยเหลือ กรุณาติดต่อทีมสนับสนุนของเราทันที
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ติดต่อทีมสนับสนุน
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          หากคุณต้องการยกเลิกการสมัครสมาชิกของคุณ คุณสามารถทำได้ในการตั้งค่าบัญชีของคุณ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ การแจ้งเตือนสุดท้าย

การยกเลิกการสมัครสมาชิกใกล้เข้ามาแล้ว

คุณคือ {{ customer_name }},

นี่คือการแจ้งเตือนสุดท้ายของคุณ เรายังไม่สามารถดำเนินการชำระเงินสำหรับการสมัครสมาชิก {{ plan_name }} ของคุณได้ หากเราไม่ได้รับการชำระเงินภายใน {{ days_until_cancellation }} วัน การสมัครสมาชิกของคุณจะถูกยกเลิก

⚠️ การชำระเงินล้มเหลว - ต้องดำเนินการ:
- การสมัครสมาชิก: {{ plan_name }}
- จำนวนเงินที่ต้องชำระ: {{ amount_due }}
- จำนวนครั้งที่ชำระล้มเหลว: {{ retry_count }}
- ครั้งสุดท้ายที่พยายามชำระ: {{ last_retry_date }}
- วันที่ยกเลิก: {{ cancellation_date }}

ข้อผิดพลาดในการชำระเงิน:
{{ payment_error_message }}

สิ่งที่จะเกิดขึ้น:
หากไม่ได้รับการชำระเงินภายใน {{ cancellation_date }}:
• การสมัครสมาชิกของคุณจะถูกยกเลิก
• คุณจะสูญเสียสิทธิ์ในการเข้าถึงประโยชน์ทั้งหมดของสมาชิก
• ข้อมูลของคุณอาจถูกลบ (ดูนโยบายการรักษาข้อมูล)
• คุณจะต้องสมัครสมาชิกอีกครั้งเพื่อเริ่มต้นการเข้าถึงใหม่

อัปเดตวิธีการชำระเงินทันที

ปัญหาที่พบบ่อยและวิธีแก้ไข:
• บัตรหมดอายุ: อัปเดตด้วยบัตรเครดิตที่ใช้งานได้
• ยอดเงินไม่เพียงพอ: ตรวจสอบให้แน่ใจว่ายอดเงินเพียงพอ
• บัตรถูกปฏิเสธ: ติดต่อธนาคารของคุณหรือใช้บัตรอื่น
• ที่อยู่ไม่ตรงกัน: ตรวจสอบให้แน่ใจว่าที่อยู่ในการออกใบแจ้งหนี้ตรงกับบัตร

ต้องการความช่วยเหลือหรือไม่?
หากคุณกำลังประสบปัญหาในการชำระเงินหรือต้องการความช่วยเหลือ กรุณาติดต่อทีมสนับสนุนของเราทันที

อัปเดตวิธีการชำระเงิน: {{ update_payment_url }}
ติดต่อทีมสนับสนุน: {{ support_url }}

หากคุณต้องการยกเลิกการสมัครสมาชิกของคุณ คุณสามารถทำได้ในการตั้งค่าบัญชีของคุณ

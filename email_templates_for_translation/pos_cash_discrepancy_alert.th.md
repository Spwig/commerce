---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ แจ้งเตือนเงินสดไม่ตรงกัน: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ แจ้งเตือนเงินสดไม่ตรงกัน
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          แจ้งเตือนความแตกต่างของเงินสด
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          พบความไม่สอดคล้องของเงินสดจำนวน {{ discrepancy_amount }} ขณะปิดกะที่ {{ terminal_name }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดความไม่สอดคล้อง:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>เครื่องขาย:</strong> {{ terminal_name }}<br/>
              <strong>พนักงานแคชเชียร์:</strong> {{ cashier_name }}<br/>
              <strong>วันที่กะ:</strong> {{ shift_date }}<br/>
              <strong>ระยะเวลากะ:</strong> {{ shift_duration }}<br/>
              <strong>ตรวจพบ:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การนับเงินสด:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>เงินสดที่คาดหวัง:</strong> {{ expected_cash }}<br/>
              <strong>เงินสดที่นับได้:</strong> {{ counted_cash }}<br/>
              <strong>ความไม่สอดคล้อง:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>เงินสดเริ่มต้น:</strong> {{ opening_cash }}<br/>
              <strong>ยอดขายเงินสด:</strong> {{ cash_sales }}<br/>
              <strong>เงินคืนเงินสด:</strong> {{ cash_refunds }}<br/>
              <strong>เงินสดที่จ่ายออก:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          หมายเหตุของแคชเชียร์:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขั้นตอนแนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. ตรวจสอบประวัติการทำธุรกรรมเพื่อหาข้อผิดพลาด<br/>
          2. ตรวจสอบการชำระเงินสดที่ยังไม่ได้บันทึก<br/>
          3. ยืนยันว่าการนับเงินสดถูกต้อง<br/>
          4. บันทึกความไม่สอดคล้องในหมายเหตุของกะ<br/>
          5. ติดต่อพนักงานแคชเชียร์หากจำเป็น
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูรายงานกะ
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ตรวจสอบการทำธุรกรรม
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ตรวจพบความไม่สอดคล้องของเงินสด

แจ้งเตือนความแตกต่างของเงินสด

พบความไม่สอดคล้องของเงินสดจำนวน {{ discrepancy_amount }} ขณะปิดกะที่ {{ terminal_name }}

รายละเอียดความไม่สอดคล้อง:
- เครื่องขาย: {{ terminal_name }}
- พนักงานแคชเชียร์: {{ cashier_name }}
- วันที่กะ: {{ shift_date }}
- ระยะเวลากะ: {{ shift_duration }}
- ตรวจพบ: {{ detected_at }}

การนับเงินสด:
- เงินสดที่คาดหวัง: {{ expected_cash }}
- เงินสดที่นับได้: {{ counted_cash }}
- ความไม่สอดคล้อง: {{ discrepancy_amount }}

BREAKDOWN:
- เงินสดเริ่มต้น: {{ opening_cash }}
- ยอดขายเงินสด: {{ cash_sales }}
- เงินคืนเงินสด: {{ cash_refunds }}
- เงินสดที่จ่ายออก: {{ cash_paid_out }}

{% if cashier_note %}
CASHIER'S NOTE:
"{{ cashier_note }}"
{% endif %}

RECOMMENDED ACTIONS:
1. ตรวจสอบประวัติการทำธุรกรรมเพื่อหาข้อผิดพลาด
2. ตรวจสอบการชำระเงินสดที่ยังไม่ได้บันทึก
3. ยืนยันว่าการนับเงินสดถูกต้อง
4. บันทึกความไม่สอดคล้องในหมายเหตุของกะ
5. ติดต่อพนักงานแคชเชียร์หากจำเป็น

ดูรายงานกะ: {{ shift_report_url }}
ตรวจสอบการทำธุรกรรม: {{ transaction_history_url }}
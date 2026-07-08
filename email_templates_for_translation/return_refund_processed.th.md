---
template_type: return_refund_processed
category: Returns
---

# Email Template: return_refund_processed

## Subject
การคืนเงินสำเร็จ - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          การคืนเงินสำเร็จ
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          คำสั่งซื้อ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          การคืนสินค้าสำหรับคำสั่งซื้อ <strong>#{{ order_number }}</strong> ของคุณได้รับการตรวจสอบแล้ว และเงินคืนของคุณได้รับการดำเนินการแล้ว。
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
              รายละเอียดการคืนเงิน
            </mj-text>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>จำนวนเงินคืน:</strong> {{ refund_currency }} {{ refund_amount }}
            </mj-text>
            {% if restocking_fee %}
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ค่าธรรมเนียมการคืนสินค้า:</strong> {{ restocking_fee_currency }} {{ restocking_fee }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>หมายเหตุ:</strong> การคืนเงินอาจใช้เวลา 5-10 วันทำการเพื่อปรากฏในบัญชีของคุณ ขึ้นอยู่กับผู้ให้บริการชำระเงินของคุณ。
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          หากคุณมีคำถามใด ๆ เกี่ยวกับการคืนเงินของคุณ กรุณาติดต่อทีมสนับสนุนของเรา。
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การคืนเงินสำเร็จ - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

การคืนสินค้าสำหรับคำสั่งซื้อ #{{ order_number }} ของคุณได้รับการตรวจสอบแล้ว และเงินคืนของคุณได้รับการดำเนินการแล้ว。

รายละเอียดการคืนเงิน:
- จำนวนเงินคืน: {{ refund_currency }} {{ refund_amount }}
{% if restocking_fee %}- ค่าธรรมเนียมการคืนสินค้า: {{ restocking_fee_currency }} {{ restocking_fee }}{% endif %}

หมายเหตุ: การคืนเงินอาจใช้เวลา 5-10 วันทำการเพื่อปรากฏในบัญชีของคุณ ขึ้นอยู่กับผู้ให้บริการชำระเงินของคุณ。

หากคุณมีคำถามใด ๆ เกี่ยวกับการคืนเงินของคุณ กรุณาติดต่อทีมสนับสนุนของเรา。

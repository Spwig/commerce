---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
ขอบคุณสำหรับคำสั่งซื้อ #{{ order_number }}! - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 ขอบคุณสำหรับคำสั่งซื้อของคุณ!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          เราดีใจที่คุณได้ทำการซื้อสินค้า! คำสั่งซื้อของคุณได้รับการยืนยันแล้ว และเรากำลังเตรียมสินค้าเพื่อจัดส่ง
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              สรุปคำสั่งซื้อ
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>หมายเลขคำสั่งซื้อ:</strong> {{ order_number }}<br/>
              <strong>วันที่สั่งซื้อ:</strong> {{ order_date }}<br/>
              <strong>ยอดรวม:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ติดตามคำสั่งซื้อของคุณ
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สิ่งที่จะเกิดขึ้นต่อไปคืออะไร?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. เราจะเตรียมคำสั่งซื้อของคุณ (โดยทั่วไปภายใน 1-2 วันทำการ)
          <br/>
          2. คุณจะได้รับการยืนยันการจัดส่งพร้อมข้อมูลติดตามการจัดส่ง
          <br/>
          3. คำสั่งซื้อของคุณจะถูกส่งไปยัง: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>คุณทราบหรือไม่?</strong><br/>
              คุณสามารถติดตามคำสั่งซื้อของคุณได้ทุกเมื่อในแดชบอร์ดบัญชีของคุณ
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          มีคำถาม? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">ติดต่อทีมสนับสนุนของเรา</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 ขอบคุณสำหรับคำสั่งซื้อของคุณ!

สวัสดี {{ customer_name }},

เราดีใจที่คุณได้ทำการซื้อสินค้า! คำสั่งซื้อของคุณได้รับการยืนยันแล้ว และเรากำลังเตรียมสินค้าเพื่อจัดส่ง

สรุปคำสั่งซื้อ:
- หมายเลขคำสั่งซื้อ: {{ order_number }}
- วันที่สั่งซื้อ: {{ order_date }}
- ยอดรวม: {{ order_total }}

ติดตามคำสั่งซื้อของคุณ: {{ order_tracking_url }}

สิ่งที่จะเกิดขึ้นต่อไปคืออะไร?
1. เราจะเตรียมคำสั่งซื้อของคุณ (โดยทั่วไปภายใน 1-2 วันทำการ)
2. คุณจะได้รับการยืนยันการจัดส่งพร้อมข้อมูลติดตามการจัดส่ง
3. คำสั่งซื้อของคุณจะถูกส่งไปยัง: {{ shipping_address }}

💡 คุณทราบหรือไม่?
คุณสามารถติดตามคำสั่งซื้อของคุณได้ทุกเมื่อในแดชบอร์ดบัญชีของคุณ

มีคำถาม? ติดต่อทีมสนับสนุนของเรา: {{ support_url }}

---
คำสั่งซื้อ #{{ order_number }} ที่ {{ shop_name }}
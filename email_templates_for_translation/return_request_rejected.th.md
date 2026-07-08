---
template_type: return_request_rejected
category: Returns
---

# Email Template: return_request_rejected

## Subject
การแจ้งความคืบหน้าการขอคืนสินค้า - คำสั่งซื้อ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#92400e' }}">
          การแจ้งความคืบหน้าการขอคืนสินค้า
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#92400e' }}">
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
          เราได้พิจารณาคำขอคืนสินค้าของคุณสำหรับคำสั่งซื้อ <strong>#{{ order_number }}</strong> และในขณะนี้เราไม่สามารถอนุมัติคำขอของคุณได้
        </mj-text>

        {% if rejection_reason %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>เหตุผล:</strong> {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          หากคุณมีคำถามเกี่ยวกับการตัดสินใจนี้หรือคิดว่าอาจมีข้อผิดพลาดเกิดขึ้น กรุณาติดต่อทีมสนับสนุนของเรา
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การแจ้งความคืบหน้าการขอคืนสินค้า - คำสั่งซื้อ #{{ order_number }}

สวัสดี {{ customer_name }},

เราได้พิจารณาคำขอคืนสินค้าของคุณสำหรับคำสั่งซื้อ #{{ order_number }} และในขณะนี้เราไม่สามารถอนุมัติคำขอของคุณได้

{% if rejection_reason %}เหตุผล: {{ rejection_reason }}{% endif %}

หากคุณมีคำถามเกี่ยวกับการตัดสินใจนี้หรือคิดว่าอาจมีข้อผิดพลาดเกิดขึ้น กรุณาติดต่อทีมสนับสนุนของเรา
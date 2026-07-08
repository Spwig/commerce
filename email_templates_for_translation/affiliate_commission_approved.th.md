---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
ค่าคอมมิชชั่นได้รับการอนุมัติแล้ว: {{ commission_amount }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f8f9fa">
    <!-- Header -->
    <mj-section background-color="#ffffff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="#212529" align="center">
          ✓ ค่าคอมมิชชั่นได้รับการอนุมัติแล้ว!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          ได้รับการอนุมัติสำหรับการจ่ายเงิน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          สวัสดี {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          ค่าคอมมิชชั่น {{ commission_amount }} จากออเดอร์ #{{ order_number }} ของคุณได้รับการอนุมัติแล้ว และจะถูกรวมในรอบการจ่ายเงินครั้งต่อไปของคุณ
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          การจ่ายเงินจะถูกดำเนินการตามตารางการชำระเงินของคุณ คุณจะได้รับอีเมลอีกครั้งเมื่อการจ่ายเงินถูกดำเนินการ
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          ดูค่าคอมมิชชั่น
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อฝ่ายสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
ค่าคอมมิชชั่นได้รับการอนุมัติแล้ว: {{ commission_amount }}

สวัสดี {{ affiliate_name }},

ค่าคอมมิชชั่น {{ commission_amount }} จากออเดอร์ #{{ order_number }} ของคุณได้รับการอนุมัติแล้ว และจะถูกรวมในรอบการจ่ายเงินครั้งต่อไปของคุณ

การจ่ายเงินจะถูกดำเนินการตามตารางการชำระเงินของคุณ คุณจะได้รับอีเมลอีกครั้งเมื่อการจ่ายเงินถูกดำเนินการ

ดูค่าคอมมิชชั่นของคุณ: {{ portal_url }}

{{ shop_name }}
มีคำถาม? ติดต่อ {{ support_email }}
---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
การชำระเงินถูกยกเลิก - {{ payout_amount }}

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
          การชำระเงินถูกยกเลิก
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
          การชำระเงินของคุณจำนวน {{ payout_amount }} (ID การชำระเงิน: {{ payout_id }}) ถูกยกเลิกแล้ว。
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          หากคุณมีข้อสงสัยเกี่ยวกับการที่การชำระเงินนี้ถูกยกเลิก โปรดติดต่อทีมสนับสนุนของเรา。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          ดูแดชบอร์ดผู้พันธมิตร
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          มีคำถาม? <a href="mailto:{{ support_email }}" style="color: #007bff;">ติดต่อทีมสนับสนุน</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
การชำระเงินถูกยกเลิก - {{ payout_amount }}

สวัสดี {{ affiliate_name }},

การชำระเงินของคุณจำนวน {{ payout_amount }} (ID การชำระเงิน: {{ payout_id }}) ถูกยกเลิกแล้ว。

หากคุณมีข้อสงสัยเกี่ยวกับการที่การชำระเงินนี้ถูกยกเลิก โปรดติดต่อทีมสนับสนุนของเรา。

ดูแดชบอร์ดของคุณ: {{ portal_url }}

{{ shop_name }}
คำถาม? ติดต่อ {{ support_email }}
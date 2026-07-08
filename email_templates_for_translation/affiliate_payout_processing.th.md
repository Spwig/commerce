---
template_type: affiliate_payout_processing
category: Affiliate Program
---

# Email Template: affiliate_payout_processing

## Subject
การจ่ายเงิน {{ payout_amount }} ของคุณกำลังดำเนินการ

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
          💸 การดำเนินการการจ่ายเงิน
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#17a2b8" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          การดำเนินการการจ่ายเงินของคุณ
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          ID การจ่ายเงิน: {{ payout_id }}
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
          ข่าวดี! การจ่ายเงิน {{ payout_amount }} ของคุณกำลังดำเนินการอยู่แล้ว
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          เงินจะเข้าบัญชีของคุณภายใน 3-5 วันทำการ เนื่องจากวันทำการ คุณจะได้รับอีเมลฉบับอื่นเมื่อการจ่ายเงินเสร็จสิ้น
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>ID การจ่ายเงิน:</strong> {{ payout_id }}<br/>
          <strong>จำนวนเงิน:</strong> {{ payout_amount }}<br/>
          <strong>วิธีการชำระเงิน:</strong> {{ payout_method }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          ดูประวัติการจ่ายเงิน
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
การจ่ายเงิน {{ payout_amount }} ของคุณกำลังดำเนินการ

Hi {{ affiliate_name }},

Good news! Your payout of {{ payout_amount }} is now being processed.

Payout Details:
- Payout ID: {{ payout_id }}
- Amount: {{ payout_amount }}
- Payment Method: {{ payout_method }}

The funds should arrive in your account within 3-5 business days. You'll receive another email when the payout is complete.

View payout history: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}
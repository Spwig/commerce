---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ การโอนเงินเสร็จสิ้น: {{ payout_amount }}

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
          🎉 Payout Completed!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ Successfully Paid
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          Payout ID: {{ payout_id }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          Hi {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Your payout of {{ payout_amount }} has been successfully completed!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          The funds have been sent to your payment method. Depending on your bank or payment processor, it may take 1-2 business days to appear in your account.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          Thank you for promoting {{ shop_name }}. Keep up the great work!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          View Payout Details
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: #007bff;">
            Contact Support
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ Payout completed: {{ payout_amount }}

Hi {{ affiliate_name }},

Your payout of {{ payout_amount }} has been successfully completed!

Payout Details:
- Payout ID: {{ payout_id }}
- Amount: {{ payout_amount }}
- Payment Method: {{ payout_method }}

The funds have been sent to your payment method. Depending on your bank or payment processor, it may take 1-2 business days to appear in your account.

Thank you for promoting {{ shop_name }}. Keep up the great work!

View payout details: {{ portal_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}
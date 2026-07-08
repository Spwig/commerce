---
template_type: affiliate_payout_cancelled
category: Affiliate Program
---

# Email Template: affiliate_payout_cancelled

## Subject
إلغاء دفع - {{ payout_amount }}

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
          إلغاء الدفع
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          مرحباً {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          تم إلغاء دفعتك البالغة قيمتها {{ payout_amount }} (رقم الدفع: {{ payout_id }}).
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          إذا كانت لديك أسئلة حول سبب إلغاء هذه الدفعة، يرجى التواصل مع فريق الدعم لدينا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          عرض لوحة القيادة الخاصة بك
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          هل لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
إلغاء الدفع - {{ payout_amount }}

مرحباً {{ affiliate_name }},

تم إلغاء دفعتك البالغة قيمتها {{ payout_amount }} (رقم الدفع: {{ payout_id }}).

إذا كانت لديك أسئلة حول سبب إلغاء هذه الدفعة، يرجى التواصل مع فريق الدعم لدينا.

عرض لوحة القيادة الخاصة بك: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ اتصل بـ {{ support_email }}
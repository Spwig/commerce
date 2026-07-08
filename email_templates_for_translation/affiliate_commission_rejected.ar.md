---
template_type: affiliate_commission_rejected
category: Affiliate Program
---

# Email Template: affiliate_commission_rejected

## Subject
تحديث حالة العمولة - طلب #{{ order_number }}

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
          تحديث حالة العمولة
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
         您好 {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          نود إعلامك بأن العمولة الخاصة بطلب #{{ order_number }} ({{ commission_amount }}) لم تُوافق عليها.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يحدث هذا عادةً عندما يتم إلغاء الطلب أو إرجاعه قبل انتهاء فترة العمولة.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          إذا كانت لديك أسئلة حول هذه العمولة، يرجى التواصل مع فريق الدعم لدينا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#6c757d" color="#ffffff" href="{{ portal_url }}">
          اعرض لوحة القيادة الخاصة بك
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          هل لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">تواصل مع الدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تحديث حالة العمولة - طلب #{{ order_number }}

مرحبًا {{ affiliate_name }},

نود إعلامك بأن العمولة الخاصة بطلب #{{ order_number }} ({{ commission_amount }}) لم تُوافق عليها.

يحدث هذا عادةً عندما يتم إلغاء الطلب أو إرجاعه قبل انتهاء فترة العمولة.

إذا كانت لديك أسئلة حول هذه العمولة، يرجى التواصل مع فريق الدعم لدينا.

عرض لوحة القيادة الخاصة بك: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ تواصل مع {{ support_email }}
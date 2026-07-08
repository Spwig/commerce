---
template_type: affiliate_payout_failed
category: Affiliate Program
---

# Email Template: affiliate_payout_failed

## Subject
الإجراء المطلوب: فشل الدفع

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
        <mj-text font-size="32px" font-weight="bold" color="#dc3545" align="center">
          ⚠️ فشل الدفع
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Display -->
    <mj-section background-color="#fff3cd" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#856404" align="center" padding-top="10px">
          معرف الدفع: {{ payout_id }}
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
          واجهنا مشكلة في معالجة دفعتك المقدرة على {{ payout_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          هذا يحدث عادةً بسبب معلومات الدفع غير الصحيحة أو مشكلة مع مزود الدفع الخاص بك.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يرجى تحديث معلومات الدفع في لوحة تحكم المُحَوِّل الخاص بك والاتصال بفريق الدعم لدينا لحل هذه المشكلة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#dc3545" color="#ffffff" href="{{ portal_url }}">
          تحديث معلومات الدفع
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          هل تحتاج إلى مساعدة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
الإجراء المطلوب: فشل الدفع

مرحباً {{ affiliate_name }},

واجهنا مشكلة في معالجة دفعتك المقدرة على {{ payout_amount }} (معرف الدفع: {{ payout_id }}).

هذا يحدث عادةً بسبب معلومات الدفع غير الصحيحة أو مشكلة مع مزود الدفع الخاص بك.

يرجى تحديث معلومات الدفع في لوحة تحكم المُحَوِّل الخاص بك والاتصال بفريق الدعم لدينا لحل هذه المشكلة.

تحديث معلومات الدفع: {{ portal_url }}

{{ shop_name }}
هل تحتاج إلى مساعدة؟ اتصل بـ {{ support_email }}
---
template_type: affiliate_payout_completed
category: Affiliate Program
---

# Email Template: affiliate_payout_completed

## Subject
✓ تم إتمام الدفع: {{ payout_amount }}

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
          🎉 تم إتمام الدفع!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payout Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          ✓ تم الدفع بنجاح
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ payout_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
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
          تم إتمام دفتك من {{ payout_amount }} بنجاح!
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          تم إرسال الأموال إلى وسيلة الدفع الخاصة بك. حسب بنكك أو معالج الدفع الخاص بك، قد يستغرق الأمر من 1 إلى 2 أيام عمل لظهوره في حسابك.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          شكرًا لترويج {{ shop_name }}. استمر في العمل الرائع!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          عرض تفاصيل الدفع
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          هل لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">اتصل بفريق الدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ تم إتمام الدفع: {{ payout_amount }}

مرحباً {{ affiliate_name }},

تم إتمام دفتك من {{ payout_amount }} بنجاح!

تفاصيل الدفع:
- معرف الدفع: {{ payout_id }}
- المبلغ: {{ payout_amount }}
- وسيلة الدفع: {{ payout_method }}

تم إرسال الأموال إلى وسيلة الدفع الخاصة بك. حسب بنكك أو معالج الدفع الخاص بك، قد يستغرق الأمر من 1 إلى 2 أيام عمل لظهوره في حسابك.

شكرًا لترويج {{ shop_name }}. استمر في العمل الرائع!

عرض تفاصيل الدفع: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ اتصل بـ {{ support_email }}
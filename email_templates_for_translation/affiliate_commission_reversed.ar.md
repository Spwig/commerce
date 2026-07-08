---
template_type: affiliate_commission_reversed
category: Affiliate Program
---

# Email Template: affiliate_commission_reversed

## Subject
الرسوم المستردة - طلب #{{ order_number }}

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
          الرسوم المستردة
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
          تم استرداد رسوم طلب #{{ order_number }} ({{ commission_amount }}) بسبب استرجاع العميل.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          عند طلب العملاء عمليات استرجاع، يتم استرداد أي رسوم مرتبطة تلقائياً لضمان دقة الحسابات.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          هذا جزء طبيعي من عملية الشراكة. استمر في الترويج لـ {{ shop_name }} للحصول على رسوم جديدة!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          عرض لوحة تحكم الشراكة
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="#f8f9fa" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="#6c757d" align="center">
          {{ shop_name }}<br/>
          لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: #007bff;">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
الرسوم المستردة - طلب #{{ order_number }}

مرحباً {{ affiliate_name }},

تم استرداد رسوم طلب #{{ order_number }} ({{ commission_amount }}) بسبب استرجاع العميل.

عند طلب العملاء عمليات استرجاع، يتم استرداد أي رسوم مرتبطة تلقائياً لضمان دقة الحسابات.

هذا جزء طبيعي من عملية الشراكة. استمر في الترويج لـ {{ shop_name }} للحصول على رسوم جديدة!

عرض لوحة تحكمك: {{ portal_url }}

{{ shop_name }}
لديك أسئلة؟ اتصل بـ {{ support_email }}
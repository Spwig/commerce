---
template_type: affiliate_commission_earned
category: Affiliate Program
---

# Email Template: affiliate_commission_earned

## Subject
لقد كسبت عمولة قدرها {{ commission_amount }}!

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
          💰 تم كسب العمولة!
        </mj-text>
        <mj-text font-size="18px" color="#6c757d" align="center">
          خبر سار من {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Display -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-bottom="10px">
          💵 عمولتك
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="14px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="10px">
          من طلب #{{ order_number }}
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
          تهانينا! لقد كسبت عمولة قدرها {{ commission_amount }} من طلب #{{ order_number }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          استمر في الترويج لـ {{ shop_name }} لكسب عمولات إضافية. كلما زادت مبيعاتك، زاد ما تربحه!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Commission Details -->
    <mj-section background-color="#f8f9fa" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          <strong>رقم الطلب:</strong> #{{ order_number }}<br/>
          <strong>مبلغ العمولة:</strong> {{ commission_amount }}<br/>
          <strong>نسبة العمولة:</strong> {{ commission_rate }}%
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          عرض لوحة القيادة الخاصة بك
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
لقد كسبت عمولة قدرها {{ commission_amount }}!

مرحباً {{ affiliate_name }},

تهانينا! لقد كسبت عمولة قدرها {{ commission_amount }} من طلب #{{ order_number }}.

تفاصيل العمولة:
- رقم الطلب: #{{ order_number }}
- مبلغ العمولة: {{ commission_amount }}
- نسبة العمولة: {{ commission_rate }}%

استمر في الترويج لـ {{ shop_name }} لكسب عمولات إضافية.

عرض لوحة القيادة الخاصة بك: {{ portal_url }}

{{ shop_name }}
لديك أسئلة؟ اتصل بـ {{ support_email }}
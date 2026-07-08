---
template_type: affiliate_account_activated
category: Affiliate Program
---

# Email Template: affiliate_account_activated

## Subject
مرحبا بك مرة أخرى! تم إعادة تنشيط الحساب

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
          🎉 تم إعادة تنشيط الحساب!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="#28a745" padding="40px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#ffffff" align="center">
          مرحبا بك مرة أخرى!
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          تم إعادة تنشيط حسابك التابع
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="#ffffff" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="#212529">
          السلام عليكم {{ affiliate_name }},
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          أخبار سارة! تم إعادة تنشيط حسابك التابع لـ {{ shop_name }}.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يمكنك استئناف ترويج منتجاتنا وربح عمولات فوراً.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          الوصول إلى لوحة التحكم الخاصة بك
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
مرحبا بك مرة أخرى! تم إعادة تنشيط الحساب

السلام عليكم {{ affiliate_name }},

أخبار سارة! تم إعادة تنشيط حسابك التابع لـ {{ shop_name }}.

يمكنك استئناف ترويج منتجاتنا وربح عمولات فوراً.

الوصول إلى لوحة التحكم الخاصة بك: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ اتصل بـ {{ support_email }}
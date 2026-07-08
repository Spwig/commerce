---
template_type: affiliate_commission_approved
category: Affiliate Program
---

# Email Template: affiliate_commission_approved

## Subject
تمت الموافقة على العمولة: {{ commission_amount }}

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
          ✓ تمت الموافقة على العمولة!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Approval Display -->
    <mj-section background-color="#007bff" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#ffffff" align="center" line-height="1">
          {{ commission_amount }}
        </mj-text>
        <mj-text font-size="16px" color="#ffffff" align="center" padding-top="10px">
          تم الموافقة على الدفع
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
          تم الموافقة على عمولتك البالغة {{ commission_amount }} من طلب #{{ order_number }} وستتم إضافتها إلى دفتك التالية.
        </mj-text>
        <mj-text font-size="16px" color="#212529">
          يتم معالجة الدفعات وفقًا لجدول الدفع الخاص بك. ستتلقى بريدًا إلكترونيًا آخر عندما تتم معالجة الدفعة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="#ffffff" padding="30px 20px">
      <mj-column>
        <mj-button background-color="#007bff" color="#ffffff" href="{{ portal_url }}">
          عرض العمولات
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
العمولة تم الموافقة عليها: {{ commission_amount }}

السلام عليكم {{ affiliate_name }},

تم الموافقة على عمولتك البالغة {{ commission_amount }} من طلب #{{ order_number }} وستتم إضافتها إلى دفتك التالية.

تتم معالجة الدفعات وفقًا لجدول الدفع الخاص بك. ستتلقى بريدًا إلكترونيًا آخر عندما تتم معالجة الدفعة.

عرض عمولتك: {{ portal_url }}

{{ shop_name }}
هل لديك أسئلة؟ تواصل مع {{ support_email }}
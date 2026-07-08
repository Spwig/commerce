---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
الغاء التحويل - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          الغاء التحويل
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً بك،
        </mj-text>
        <mj-text>
          تم إلغاء طلب الغاء الاشتراك الخاص بك لـ <strong>{{ store_name }}</strong>. سيستمر اشتراكك في <strong>{{ plan_name }}</strong> بشكل طبيعي — لا يتطلب الأمر أي إجراء من جانبك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل الاشتراك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الخطة: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          تاريخ الفاتورة القادم: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          يستمر متجرك في العمل بشكل طبيعي. سيتم استئناف الفواتير في التاريخ المذكور أعلاه.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
الغاء التحويل - {{ store_name }}

اهلاً بك،

تم إلغاء طلب الغاء الاشتراك الخاص بك لـ {{ store_name }}. سيستمر اشتراكك في {{ plan_name }} بشكل طبيعي — لا يتطلب الأمر أي إجراء من جانبك.

تفاصيل الاشتراك:
- الخطة: {{ plan_name }}
- تاريخ الفاتورة القادم: {{ next_billing_date }}

يستمر متجرك في العمل بشكل طبيعي. سيتم استئناف الفواتير في التاريخ المذكور أعلاه.

{% if admin_url %}الذهاب إلى متجرك: {{ admin_url }}

{% endif %}تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
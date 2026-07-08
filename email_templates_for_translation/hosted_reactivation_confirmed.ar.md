---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
مرحباً مرة أخرى! {{ store_name }} نشطة مرة أخرى

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          مرحباً مرة أخرى!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} نشطة مرة أخرى
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً بك,
        </mj-text>
        <mj-text>
          أخبار سارة! تم إعادة تنشيط متجرك <strong>{{ store_name }}</strong>. الآن الاشتراك الخاص بك في <strong>{{ plan_name }}</strong> نشط، ومتجرك يعود إلى العمل.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل إعادة التنشيط
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الخطة: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الدفع المعالج: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          تاريخ الفاتورة القادم: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          يعود متجرك إلى العمل الآن. قد يستغرق الأمر بضع دقائق لاستعادة كل شيء بالكامل. بمجرد أن يكون متجرك نشطًا، يمكنك الوصول إليه من خلال {{ store_url }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
مرحباً مرة أخرى! {{ store_name }} نشطة مرة أخرى

أهلاً بك,

أخبار سارة! تم إعادة تنشيط متجرك {{ store_name }}. الآن الاشتراك الخاص بك في {{ plan_name }} نشط، ومتجرك يعود إلى العمل.

تفاصيل إعادة التنشيط:
- الخطة: {{ plan_name }}
- الدفع المعالج: {{ currency }}{{ amount }}
- تاريخ الفاتورة القادم: {{ next_billing_date }}

يعود متجرك إلى العمل الآن. قد يستغرق الأمر بضع دقائق لاستعادة كل شيء بالكامل. بمجرد أن يكون متجرك نشطًا، يمكنك الوصول إليه من خلال {{ store_url }}.

الانتقال إلى متجرك: {{ admin_url }}

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
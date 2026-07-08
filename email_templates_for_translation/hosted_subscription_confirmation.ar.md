---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
تم تأكيد الاشتراك - {{ store_name }}

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
          تم تأكيد الاشتراك!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          مرحبًا بك في Spwig
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          شكرًا لاشتراكك! تم تأكيد خطة <strong>{{ plan_name }}</strong> الخاصة بك لـ <strong>{{ store_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل الخطة
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الخطة: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          فترة الفاتورة: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          المبلغ: {{ currency }}{{ amount }}{% if intro_period %} (سعر مقدم){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          سعرك المقدم سيسري لمدة {{ intro_period }}. بعدها، ستتجدد خطةك بسعر {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          يتم إعداد متجرك الآن، وستتلقى بريدًا إلكترونيًا آخر عندما يصبح جاهزًا.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          تاريخ الفاتورة القادم: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تم تأكيد الاشتراك!

أهلاً {{ name|default:'there' }},

شكرًا لاشتراكك! تم تأكيد خطة {{ plan_name }} الخاصة بك لـ {{ store_name }}.

تفاصيل الخطة:
- الخطة: {{ plan_name }}
- فترة الفاتورة: {{ billing_interval }}
- المبلغ: {{ currency }}{{ amount }}{% if intro_period %} (سعر مقدم){% endif %}
{% if intro_period %}
هذا هو سعرك المقدم لمدة {{ intro_period }}. بعدها، ستتجدد خطةك بسعر {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
يتم إعداد متجرك الآن، وستتلقى بريدًا إلكترونيًا آخر عندما يصبح جاهزًا.

تاريخ الفاتورة القادم: {{ next_billing_date }}

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
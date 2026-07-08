---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
الحساب معلق - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          الحساب معلق
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
          أهلاً {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          تم تعليق متجرك <strong>{{ store_name }}</strong> بسبب عدم سداد الفاتورة.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ما يعنيه هذا
        </mj-text>
        <mj-text font-size="14px">
          أصبح متجرك الآن في وضع القراءة فقط -- يمكن للعملاء التصفح ولكن الطلبات معطلة. بياناتك آمنة وستظل محفوظة لمدة 30 يومًا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          لاستعادة الوصول الكامل، يرجى تحديث وسيلة الدفع الخاصة بك وسداد المبلغ المستحق.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="استعادة متجرك" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
الحساب معلق - {{ store_name }}

أهلاً {{ name|default:'there' }},

تم تعليق متجرك {{ store_name }} بسبب عدم سداد الفاتورة.

ما يعنيه هذا:
أصبح متجرك الآن في وضع القراءة فقط -- يمكن للعملاء التصفح ولكن الطلبات معطلة. بياناتك آمنة وستظل محفوظة لمدة 30 يومًا.

للاستعادة الوصول الكامل، يرجى تحديث وسيلة الدفع الخاصة بك وسداد المبلغ المستحق.

استعادة متجرك: https://spwig.com/account

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
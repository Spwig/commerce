---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
تحذير من الإيقاف - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          تحذير من الإيقاف
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          الإجراء المطلوب لـ {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          مرحبًا {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          تم تأجيل دفعك لـ <strong>{{ plan_name }}</strong>. إذا لم يتم حل المشكلة بحلول <strong>{{ grace_end_date }}</strong>, سيتم وضع متجرك في وضع القراءة فقط.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ما يعنيه الإيقاف
        </mj-text>
        <mj-text font-size="14px">
          إذا تم إيقاف متجرك، فسيظل متاحًا للزوار، لكنك لن تستطيع إجراء أي تغييرات. سيتم تعليق الطلبات الجديدة حتى يتم دفع المبلغ المستحق.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          يرجى تحديث وسيلة الدفع الخاصة بك لتجنب أي اضطراب في متجرك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="تحديث وسيلة الدفع" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تحذير من الإيقاف - {{ store_name }}

مرحبًا {{ name|default:'there' }},

تم تأجيل دفعك لـ {{ plan_name }}. إذا لم يتم حل المشكلة بحلول {{ grace_end_date }}, سيتم وضع متجرك في وضع القراءة فقط.

ما يعنيه الإيقاف:
إذا تم إيقاف متجرك، فسيظل متاحًا للزوار، لكنك لن تستطيع إجراء أي تغييرات. سيتم تعليق الطلبات الجديدة حتى يتم دفع المبلغ المستحق.

يرجى تحديث وسيلة الدفع الخاصة بك لتجنب أي اضطراب في متجرك.

تحديث وسيلة الدفع: https://spwig.com/account

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
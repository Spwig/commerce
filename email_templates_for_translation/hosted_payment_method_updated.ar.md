---
template_type: hosted_payment_method_updated
category: License
---

# Email Template: hosted_payment_method_updated

## Subject
تم تحديث وسيلة الدفع - {{ store_name }}

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
          تم تحديث وسيلة الدفع
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
          تم تحديث وسيلة الدفع الخاصة بخطة <strong>{{ plan_name }}</strong> الخاصة بك على <strong>{{ store_name }}</strong> بنجاح.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Security Notice -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          لم تكن قد قمت بهذا التغيير؟
        </mj-text>
        <mj-text font-size="14px">
          إذا لم تقم بتحديث وسيلة الدفع الخاصة بك، يرجى التواصل فورًا مع فريق الدعم لدينا حتى نتمكن من تأمين حسابك.
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
تم تحديث وسيلة الدفع - {{ store_name }}

أهلاً بك،

تم تحديث وسيلة الدفع الخاصة بخطة {{ plan_name }} الخاصة بك على {{ store_name }} بنجاح.

لم تكن قد قمت بهذا التغيير؟
إذا لم تقم بتحديث وسيلة الدفع الخاصة بك، يرجى التواصل فورًا مع فريق الدعم لدينا حتى نتمكن من تأمين حسابك.

الذهاب إلى متجرك: {{ admin_url }}

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
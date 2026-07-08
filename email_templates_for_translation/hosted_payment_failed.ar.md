---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
فشل الدفع - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          مشكلة في الدفع
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          إجراء مطلوب لـ {{ store_name }}
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
          لم نتمكن من معالجة دفعتك لـ <strong>{{ plan_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل الدفع
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          المبلغ: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الخطة: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. لتجنب أي انقطاع في الخدمة، يرجى تحديث وسيلة الدفع الخاصة بك.
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
مشكلة في الدفع - {{ store_name }}

أهلاً {{ name|default:'there' }},

لم نتمكن من معالجة دفعتك لـ {{ plan_name }}.

تفاصيل الدفع:
- المبلغ: {{ currency }}{{ amount }}
- الخطة: {{ plan_name }}

{{ retry_info }}. لتجنب أي انقطاع في الخدمة، يرجى تحديث وسيلة الدفع الخاصة بك.

تحديث وسيلة الدفع: https://spwig.com/account

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
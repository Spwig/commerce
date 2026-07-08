---
template_type: hosted_provision_failed
category: License
---

# Email Template: hosted_provision_failed

## Subject
الإجراء المطلوب - مشكلة إعداد المتجر لـ {{ store_name }}

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
    <mj-section background-color="{{ theme.color.error|default:'#dc2626' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          مشكلة إعداد المتجر
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
          واجهنا مشكلة أثناء إعداد متجرك <strong>{{ store_name }}</strong>. تم إبلاغ فريقنا وهم يحققون في الأمر.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Error Details -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="#991b1b" padding-bottom="10px">
          ما حدث
        </mj-text>
        <mj-text font-size="14px" color="#7f1d1d">
          {{ provision_error }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ماذا يحدث بعد ذلك؟
        </mj-text>
        <mj-text font-size="14px">
          تم إبلاغ فريق الدعم تلقائيًا بهذا المشكل. لا تحتاج إلى اتخاذ أي إجراء - سنصل إليك بمجرد حل المشكلة.
        </mj-text>
        <mj-text font-size="14px" padding-top="10px">
          إذا كانت لديك أي أسئلة في الوقت الحالي، لا تتردد في التواصل معنا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
مشكلة إعداد المتجر - {{ store_name }}

أهلاً {{ name|default:'there' }},

واجهنا مشكلة أثناء إعداد متجرك {{ store_name }}. تم إبلاغ فريقنا وهم يحققون في الأمر.

ما حدث:
{{ provision_error }}

ماذا يحدث بعد ذلك؟
تم إبلاغ فريق الدعم تلقائيًا بهذا المشكل. لا تحتاج إلى اتخاذ أي إجراء - سنصل إليك بمجرد حل المشكلة.

إذا كانت لديك أي أسئلة في الوقت الحالي، لا تتردد في التواصل معنا.

تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
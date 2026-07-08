---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
هام: حذف البيانات في 7 أيام - {{ store_name }}

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
          تحذير حذف البيانات
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
          سيتم حذف متجرك <strong>{{ store_name }}</strong> وكل البيانات المرتبطة به بشكل دائم في <strong>{{ termination_date }}</strong>. لا يمكن التراجع عن هذا الإجراء.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ما يمكنك فعله
        </mj-text>
        <mj-text font-size="14px">
          إذا أردت الاحتفاظ ببياناتك، يرجى تصديرها قبل هذا التاريخ أو إعادة تنشيط اشتراكك لمنع الحذف.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="إعادة تنشيط الاشتراك" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
تحذير حذف البيانات - {{ store_name }}

أهلاً {{ name|default:'there' }},

سيتم حذف متجرك {{ store_name }} وكل البيانات المرتبطة به بشكل دائم في {{ termination_date }}. لا يمكن التراجع عن هذا الإجراء.

ما يمكنك فعله:
إذا أردت الاحتفاظ ببياناتك، يرجى تصديرها قبل هذا التاريخ أو إعادة تنشيط اشتراكك لمنع الحذف.

إعادة تنشيط الاشتراك: https://spwig.com/account

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
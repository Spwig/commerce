---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
تم تأكيد الإلغاء - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          تم تأكيد الإلغاء
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
          تم إلغاء اشتراكك في <strong>{{ plan_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ماذا يحدث بعد ذلك
        </mj-text>
        <mj-text font-size="14px">
          ستظل لديك إمكانية الوصول الكامل حتى <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          بعدها، سيتم الحفاظ على بيانات متجرك لمدة 30 يومًا حتى <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          إذا كنت ترغب في تصدير بياناتك قبل انتهاء الوصول، يمكنك فعل ذلك من لوحة التحكم الخاصة بك. هل تغيرت رأيك؟ يمكنك إعادة تنشيط اشتراكك في أي وقت.
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
تم تأكيد الإلغاء - {{ store_name }}

أهلاً {{ name|default:'there' }},

تم إلغاء اشتراكك في {{ plan_name }}.

ماذا يحدث بعد ذلك:
- ستظل لديك إمكانية الوصول الكامل حتى {{ access_until_date }}.
- بعدها، سيتم الحفاظ على بيانات متجرك لمدة 30 يومًا حتى {{ termination_date }}.

إذا كنت ترغب في تصدير بياناتك قبل انتهاء الوصول، يمكنك فعل ذلك من لوحة التحكم الخاصة بك. هل تغيرت رأيك؟ يمكنك إعادة تنشيط اشتراكك في أي وقت.

إعادة تنشيط الاشتراك: https://spwig.com/account

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
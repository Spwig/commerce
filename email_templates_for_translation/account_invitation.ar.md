---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
أنشئ حسابك في {{ site_name }}

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
          لقد دُعيت!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          أنشئ حسابك في {{ site_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ customer_name }},
        </mj-text>
        <mj-text>
          لاحظنا أنك كنت تتسوق معنا كضيف. أنشئ حسابًا كاملًا لتفعيل مزايا مثل متابعة الطلبات، والتسجيل السريع، والعروض الحصرية.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          سجل التسوق الخاص بك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          إجمالي الطلبات: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          إجمالي المبلغ: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          لماذا إنشاء حساب؟
        </mj-text>
        <mj-text font-size="14px">
          - تابع طلباتك واطلع على سجل الطلبات
        </mj-text>
        <mj-text font-size="14px">
          - تسجيل أسرع مع تفاصيل محفوظة
        </mj-text>
        <mj-text font-size="14px">
          - أدار عناوينك وتفضيلاتك
        </mj-text>
        <mj-text font-size="14px">
          - احصل على عروض وخصومات حصرية
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="أنشئ حسابك" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          سيسمح هذا الرابط لك بإعداد كلمة مرور لحسابك. سيتم الحفاظ على سجل الطلبات الحالي.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
لقد دُعيت لإنشاء حسابك!

أهلاً {{ customer_name }},

لقد لاحظنا أنك كنت تتسوق معنا كضيف. أنشئ حسابًا كاملًا لتفعيل مزايا مثل متابعة الطلبات، والتسجيل السريع، والعروض الحصرية.

سجل التسوق الخاص بك:
- إجمالي الطلبات: {{ total_orders }}
- إجمالي المبلغ: {{ total_spent }}

لماذا إنشاء حساب؟
- تابع طلباتك واطلع على سجل الطلبات
- تسجيل أسرع مع تفاصيل محفوظة
- أدار عناوينك وتفضيلاتك
- احصل على عروض وخصومات حصرية

أنشئ حسابك: {{ activation_url }}

سيسمح هذا الرابط لك بإعداد كلمة مرور لحسابك. سيتم الحفاظ على سجل الطلبات الحالي.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
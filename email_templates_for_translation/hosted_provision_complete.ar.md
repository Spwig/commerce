---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
متجرك جاهز - {{ store_name }}

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
          متجرك جاهز!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} جاهز لك
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
          أخبار سارة! متجرك على منصة Spwig <strong>{{ store_name }}</strong> تم إنشاؤه وتم تفعيله الآن. يمكنك البدء في إعداد منتجاتك، وعلامتك التجارية، وطرق الدفع فورًا.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          تفاصيل متجرك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          رابط المتجر: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          لوحة التحكم: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          المنطقة: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          بدء سريع
        </mj-text>
        <mj-text font-size="14px">
          1. سجّل الدخول إلى لوحة التحكم الخاصة بك باستخدام البريد الإلكتروني وكلمة المرور التي حددتها أثناء الشراء
        </mj-text>
        <mj-text font-size="14px">
          2. أضف شعار متجرك وعلامتك التجارية تحت قسم التصميم > إعدادات القالب
        </mj-text>
        <mj-text font-size="14px">
          3. أضف منتجاتك الأولى تحت قسم المخزون > المنتجات
        </mj-text>
        <mj-text font-size="14px">
          4. أعد تكوين مزود الدفع تحت قسم الإعدادات > مزودي الدفع
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
متجرك جاهز!

{{ store_name }} جاهز لك.

أهلاً {{ name|default:'there' }},

أخبار سارة! متجرك على منصة Spwig {{ store_name }} تم إنشاؤه وتم تفعيله الآن. يمكنك البدء في إعداد منتجاتك، وعلامتك التجارية، وطرق الدفع فورًا.

تفاصيل متجرك:
- رابط المتجر: {{ store_url }}
- لوحة التحكم: {{ admin_url }}
- المنطقة: {{ region }}

بدء سريع:
1. سجّل الدخول إلى لوحة التحكم الخاصة بك باستخدام البريد الإلكتروني وكلمة المرور التي حددتها أثناء الشراء
2. أضف شعار متجرك وعلامتك التجارية تحت قسم التصميم > إعدادات القالب
3. أضف منتجاتك الأولى تحت قسم المخزون > المنتجات
4. أعد تكوين مزود الدفع تحت قسم الإعدادات > مزودي الدفع

انتقل إلى لوحة التحكم: {{ admin_url }}

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
رخصة Spwig - طلب #{{ order_number }}

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
          شكرًا لشركتك!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          مرحبًا {{ customer_name }},
        </mj-text>
        <mj-text>
          اكتملت شراءك لـ <strong>{{ product_name }}</strong>. ستجد أدناه مفتاح الترخيص ورمز التكوين لبدء استخدامك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ملخص الطلب
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          المنتج: {{ product_name }}{% if includes_pos %} (يحتوي على POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          المبلغ: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          رقم الطلب: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          مفتاح الترخيص الخاص بك
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          احفظ هذا المفتاح - ستحتاجه لإعادة التثبيت
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          رمز التكوين الخاص بك
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          استخدم هذا الرمز أثناء التثبيت لتفعيل متجرك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          البدء
        </mj-text>
        <mj-text font-size="14px">
          1. اتبع دليل التكوين الخاص بنا لتثبيت Spwig على خادمك
        </mj-text>
        <mj-text font-size="14px">
          2. أدخل رمز التكوين الخاص بك عند طلب ذلك أثناء التثبيت
        </mj-text>
        <mj-text font-size="14px">
          3. سيتم تفعيل متجرك تلقائيًا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="View Setup Guide" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          أنشئ حسابك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          اضبط كلمة مرور لإدارة تراخيصك، الوصول إلى التنزيلات، والحصول على التحديثات.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Create Your Account" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          ملاحظة مهمة:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          احفظ هذا البريد الإلكتروني - يحتوي على مفتاح الترخيص ورمز التكوين للاستفادة المستقبلية. لا تشارك هذه المفاتيح مع الآخرين.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
شكرًا لشركتك!

طلب #{{ order_number }}

مرحبًا {{ customer_name }},

اكتملت شراءك لـ {{ product_name }}. ستجد أدناه مفتاح الترخيص ورمز التكوين لبدء استخدامك.

ملخص الطلب:
- المنتج: {{ product_name }}{% if includes_pos %} (يحتوي على POS){% endif %}
- المبلغ: {{ price }}
- رقم الطلب: {{ order_number }}

مفتاح الترخيص الخاص بك:
{{ license_key }}
احفظ هذا المفتاح - ستحتاجه لإعادة التثبيت.

رمز التكوين الخاص بك:
{{ setup_token }}
استخدم هذا الرمز أثناء التثبيت لتفعيل متجرك.

البدء:
1. اتبع دليل التكوين الخاص بنا لتثبيت Spwig على خادمك
2. أدخل رمز التكوين الخاص بك عند طلب ذلك أثناء التثبيت
3. سيتم تفعيل متجرك تلقائيًا

عرض دليل التكوين: {{ setup_url }}
{% if activation_url %}
إنشاء حسابك:
أدخل كلمة مرور لإدارة تراخيصك، الوصول إلى التنزيلات، والحصول على التحديثات.
{{ activation_url }}
{% endif %}
ملاحظة مهمة:
احفظ هذا البريد الإلكتروني - يحتوي على مفتاح الترخيص ورمز التكوين للاستفادة المستقبلية. لا تشارك هذه المفاتيح مع الآخرين.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
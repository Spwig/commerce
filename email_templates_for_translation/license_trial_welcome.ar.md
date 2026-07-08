---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
مرحباً بكم في Spwig - تجربة مجانية مدتها {{ trial_days }} يومًا

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          مرحباً بكم في Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          تجربة مجانية مدتها {{ trial_days }} يومًا جاهزة
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
          شكرًا لتجربة {{ product_name }}! تم تفعيل تجربتك وتمتلك {{ trial_days }} يومًا لاستكشاف كل ما يوفره Spwig{% if includes_pos %}, بما في ذلك نظام نقاط البيع الخاص بنا{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          رمز إعدادك
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          استخدم هذا الرمز أثناء التثبيت لتفعيل متجر التجربة الخاص بك
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
          1. اتبع دليل الإعداد لتثبيت Spwig على خادمك
        </mj-text>
        <mj-text font-size="14px">
          2. أدخل رمز الإعداد الخاص بك عند طلب ذلك أثناء التثبيت
        </mj-text>
        <mj-text font-size="14px">
          3. ابدأ في بناء متجرك عبر الإنترنت!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="عرض دليل الإعداد" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          ما الذي يشمله تجربتك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الوصول الكامل إلى جميع الميزات الأساسية لمدة {{ trial_days }} يومًا
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          قوائم المنتجات، الطلبات، وإدارة العملاء
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          تخصيص القوالب وبناء الصفحات
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          تكامل مزودي الدفع والشحن
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          نظام نقاط البيع (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          سيتم انتهاء تجربتك بعد {{ trial_days }} يومًا. عندما تكون جاهزًا، قم بالترقية إلى رخصة كاملة للحفاظ على متجرك يعمل دون فقدان البيانات.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
مرحباً بكم في Spwig!
تجربة مجانية مدتها {{ trial_days }} يومًا جاهزة.

أهلاً {{ customer_name }},

شكرًا لتجربة {{ product_name }}! تم تفعيل تجربتك وتمتلك {{ trial_days }} يومًا لاستكشاف كل ما يوفره Spwig{% if includes_pos %}, بما في ذلك نظام نقاط البيع الخاص بنا{% endif %}.

رمز إعدادك:
{{ setup_token }}
استخدم هذا الرمز أثناء التثبيت لتفعيل متجر التجربة الخاص بك.

البدء:
1. اتبع دليل الإعداد لتثبيت Spwig على خادمك
2. أدخل رمز الإعداد الخاص بك عند طلب ذلك أثناء التثبيت
3. ابدأ في بناء متجرك عبر الإنترنت!

عرض دليل الإعداد: {{ setup_url }}

ما الذي يشمله تجربتك:
- الوصول الكامل إلى جميع الميزات الأساسية لمدة {{ trial_days }} يومًا
- قوائم المنتجات، الطلبات، وإدارة العملاء
- تخصيص القوالب وبناء الصفحات
- تكامل مزودي الدفع والشحن
{% if includes_pos %}- نظام نقاط البيع (POS){% endif %}

سيتم انتهاء تجربتك بعد {{ trial_days }} يومًا. عندما تكون جاهزًا، قم بالترقية إلى رخصة كاملة للحفاظ على متجرك يعمل دون فقدان البيانات.

هل تحتاج إلى مساعدة؟ تواصل مع {{ support_email }}
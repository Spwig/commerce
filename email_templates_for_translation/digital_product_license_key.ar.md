---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
مفتاح الترخيص الخاص بك - طلب #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          مفتاح الترخيص الخاص بك جاهز
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          أهلاً {{ customer_name }},
        </mj-text>
        <mj-text>
          شكرًا لشراء {{ product_name }}! إليك مفتاح الترخيص الخاص بك لتفعيله.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          مفتاح الترخيص الخاص بك
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          اضغط لنسخ أو اكتبها بعناية
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          تفاصيل الترخيص:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • المنتج: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • الإصدار: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • نوع الترخيص: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • عدد التفعيلات القصوى: {{ max_activations }} جهاز(ات)
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • الصلاحية: ترخيص مدى الحياة
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • الصلاحية حتى: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          كيفية التفعيل:
        </mj-text>
        <mj-text font-size="14px">
          1. قم بتنزيل وتثبيت البرنامج
        </mj-text>
        <mj-text font-size="14px">
          2. افتح التطبيق
        </mj-text>
        <mj-text font-size="14px">
          3. أدخل مفتاح الترخيص عند طلب ذلك
        </mj-text>
        <mj-text font-size="14px">
          4. اضغط على "تفعيل" لإكمال العملية
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          تنزيل البرنامج
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ ملاحظة مهمة:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • احتفظ بهذا البريد الإلكتروني - ستحتاج إلى مفتاح الترخيص ل إعادة التثبيت
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • لا تشارك مفتاح الترخيص مع الآخرين
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • يمكنك إلغاء تفعيل الأجهزة من لوحة تحكم حسابك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          هل تحتاج إلى مساعدة في التفعيل؟ تواصل مع {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
مفتاح الترخيص الخاص بك جاهز

أهلاً {{ customer_name }},

شكرًا لشراء {{ product_name }}! إليك مفتاح الترخيص الخاص بك لتفعيله.

مفتاح الترخيص الخاص بك:
{{ license_key }}

تفاصيل الترخيص:
• المنتج: {{ product_name }}
• الإصدار: {{ product_version }}
• نوع الترخيص: {{ license_type }}
• عدد التفعيلات القصوى: {{ max_activations }} جهاز(ات)
{% if is_lifetime %}• الصلاحية: ترخيص مدى الحياة{% else %}• الصلاحية حتى: {{ expiration_date }}{% endif %}

كيفية التفعيل:
1. قم بتنزيل وتثبيت البرنامج
2. افتح التطبيق
3. أدخل مفتاح الترخيص عند طلب ذلك
4. اضغط على "تفعيل" لإكمال العملية

{% if download_url %}تنزيل البرنامج: {{ download_url }}

{% endif %}ملاحظة مهمة:
• احتفظ بهذا البريد الإلكتروني - ستحتاج إلى مفتاح الترخيص ل إعادة التثبيت
• لا تشارك مفتاح الترخيص مع الآخرين
• يمكنك إلغاء تفعيل الأجهزة من لوحة تحكم حسابك

هل تحتاج إلى مساعدة في التفعيل؟ تواصل مع {{ support_email }}
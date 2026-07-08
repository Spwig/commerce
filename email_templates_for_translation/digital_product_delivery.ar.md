---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
المنتج الرقمي جاهز - طلب #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          المنتج الرقمي جاهز!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          مرحباً {{ customer_name }},
        </mj-text>
        <mj-text>
          شكرًا لشرائك! المنتج الرقمي الخاص بك جاهز الآن للتنزيل.
        </mj-text>
        <mj-text font-weight="bold">
          طلب #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          الإصدار: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          حجم الملف: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          قم بالتنزيل الآن
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>معلومات مهمة:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • يمكنك تنزيل هذا المنتج {{ download_limit }} مرة
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • رابط التنزيل ينتهي في {{ expiration_days }} يوم
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • احتفظ بهذا البريد الإلكتروني للمراجعات المستقبلية
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          تحتاج إلى مساعدة؟ تواصل مع فريق الدعم لدينا في {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
المنتج الرقمي جاهز!

مرحباً {{ customer_name }},

شكرًا لشرائك! المنتج الرقمي الخاص بك جاهز الآن للتنزيل.

طلب #{{ order_number }}

المنتج: {{ product_name }}
الإصدار: {{ product_version }}
حجم الملف: {{ file_size }}

قم بتنزيل منتجك هنا:
{{ download_url }}

معلومات مهمة:
{% if download_limit %}• يمكنك تنزيل هذا المنتج {{ download_limit }} مرة
{% endif %}{% if expiration_days %}• رابط التنزيل ينتهي في {{ expiration_days }} يوم
{% endif %}• احتفظ بهذا البريد الإلكتروني للمراجعات المستقبلية

تحتاج إلى مساعدة؟ تواصل مع فريق الدعم لدينا في {{ support_email }}
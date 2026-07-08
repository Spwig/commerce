---
template_type: digital_product_download_expired
category: Digital Products
---

# Email Template: digital_product_download_expired

## Subject
انتهت صلاحية رابط التنزيل - الطلب #{{ order_number }}

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
    <mj-section background-color="{{ theme.color.error|default:'#ef4444' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          انتهت صلاحية رابط التنزيل
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
          انتهت صلاحية رابط تنزيل <strong>{{ product_name }}</strong> من الطلب #{{ order_number }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Expired Information -->
    <mj-section background-color="#fef2f2" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#991b1b">
          تنتهي روابط التنزيل بعد {{ expiration_days }} يومًا من الشراء لأسباب أمنية.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Request New Link -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          هل تحتاج إلى رابط تنزيل جديد؟
        </mj-text>
        <mj-text>
          يمكنك طلب رابط تنزيل جديد من خلال تسجيل الدخول إلى حسابك أو التواصل مع فريق الدعم لدينا.
        </mj-text>
        <mj-button href="{{ account_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          الانتقال إلى حسابي
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          لديك أسئلة؟ تواصل مع {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
انتهت صلاحية رابط التنزيل

مرحباً {{ customer_name }},

انتهت صلاحية رابط تنزيل {{ product_name }} من الطلب #{{ order_number }}.

تنتهي روابط التنزيل بعد {{ expiration_days }} يومًا من الشراء لأسباب أمنية.

هل تحتاج إلى رابط تنزيل جديد؟
يمكنك طلب رابط تنزيل جديد من خلال تسجيل الدخول إلى حسابك أو التواصل مع فريق الدعم لدينا.

الانتقال إلى حسابي: {{ account_url }}

لديك أسئلة؟ تواصل مع {{ support_email }}
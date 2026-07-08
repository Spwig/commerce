---
template_type: digital_product_license_expired
category: Digital Products
---

# Email Template: digital_product_license_expired

## Subject
مفتاح الترخيص قريباً من الانتهاء - {{ product_name }}

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
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          مفتاح الترخيص قريباً من الانتهاء
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
          سيتم انتهاء ترخيصك لـ <strong>{{ product_name }}</strong> قريباً.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section background-color="#fffbeb" padding="20px" border="2px solid {{ theme.color.warning|default:'#f59e0b' }}" border-radius="8px">
      <mj-column>
        <mj-text font-size="14px" color="#92400e">
          <strong>مفتاح الترخيص:</strong> {{ license_key }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>ينتهي في:</strong> {{ expiration_date }}
        </mj-text>
        <mj-text font-size="14px" color="#92400e">
          <strong>العدد المتبقي من الأيام:</strong> {{ days_remaining }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Renewal -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          أعد تجديد ترخيصك
        </mj-text>
        <mj-text>
          استمر في الاستمتاع بـ {{ product_name }} من خلال تجديد ترخيصك اليوم.
        </mj-text>
        <mj-button href="{{ renewal_url }}" background-color="{{ theme.color.warning|default:'#f59e0b' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          أعد التجديد الآن
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          هل لديك أسئلة حول التجديد؟ تواصل مع {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
مفتاح الترخيص قريباً من الانتهاء

مرحباً {{ customer_name }},

سيتم انتهاء ترخيصك لـ {{ product_name }} قريباً.

تفاصيل الترخيص:
• مفتاح الترخيص: {{ license_key }}
• ينتهي في: {{ expiration_date }}
• عدد الأيام المتبقي: {{ days_remaining }}

أعد تجديد ترخيصك:
استمر في الاستمتاع بـ {{ product_name }} من خلال تجديد ترخيصك اليوم.

أعد التجديد الآن: {{ renewal_url }}

هل لديك أسئلة حول التجديد؟ تواصل مع {{ support_email }}
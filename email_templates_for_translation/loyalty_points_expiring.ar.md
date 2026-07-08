---
template_type: loyalty_points_expiring
category: Loyalty Program
---

# Email Template: loyalty_points_expiring

## Subject
تذكير: {{ expiring_points }} نقطة ستنقضي قريبًا

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.error|default:'#ef4444' }}" align="center">
          ⏰ نقاط ستنقضي قريبًا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Points Display -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center">
          {{ expiring_points }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center">
          نقطة ستنقضي في {{ days_until_expiration }} أيام
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center">
          تاريخ الانتهاء: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          أهلاً {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          لا تدع نقاطك تضيع! لديك {{ expiring_points }} نقطة ستنتهي قريبًا.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          استبدلها الآن للحصول على مكافآت حصرية قبل أن تنتهي.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Suggested Rewards -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          المكافآت التي يمكنك الحصول عليها:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}">
          تصفح دليل المكافآت واحصل على نقاطك قبل انتهاء صلاحيتها.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ rewards_url }}">
          استبدل النقاط الآن
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تذكير: {{ expiring_points }} نقطة ستنقضي قريبًا

أهلاً {{ customer_name }},

لا تدع نقاطك تضيع! لديك {{ expiring_points }} نقطة ستنتهي في {{ days_until_expiration }} أيام.

تاريخ الانتهاء: {{ expiration_date }}

استبدلها الآن للحصول على مكافآت حصرية قبل أن تنتهي.

استبدل النقاط: {{ rewards_url }}

{{ shop_name }}
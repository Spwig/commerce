---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
تذكير: منحة {{ reward_amount }} الخاصة بك ستنتهي قريبًا

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
          ⏰ منحة تنتهي قريبًا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Warning Banner -->
    <mj-section background-color="{{ theme.color.warning_light|default:'#fef3c7' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="48px" font-weight="bold" color="#856404" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="18px" color="#856404" align="center" padding-top="10px">
          تنتهي خلال {{ days_until_expiration }} أيام
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
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
          لا تدع منحتك الخاصة بدعوة {{ reward_amount }} تضيع! ستنتهي خلال {{ days_until_expiration }} أيام.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          استخدمها الآن في شراءك القادم قبل فوات الأوان!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>نوع المنحة:</strong> {{ reward_type_display }}<br/>
          <strong>المبلغ:</strong> {{ reward_amount }}<br/>
          <strong>تنتهي:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          اشترِ الآن
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
تذكير: منحة {{ reward_amount }} الخاصة بك ستنتهي قريبًا

أهلاً {{ customer_name }},

لا تدع منحتك الخاصة بدعوة {{ reward_amount }} تضيع! ستنتهي خلال {{ days_until_expiration }} أيام.

تفاصيل المنحة:
- النوع: {{ reward_type_display }}
- المبلغ: {{ reward_amount }}
- تنتهي: {{ expiration_date }}

استخدمها الآن في شراءك القادم قبل فوات الأوان!

اشترِ الآن: {{ shop_url }}

{{ shop_name }}
لديك أسئلة؟ اتصل بـ {{ support_email }}
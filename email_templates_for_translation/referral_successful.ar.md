---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 صديقك {{ referee_name }} قد зарегистрился حديثًا!

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
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 نجاح الإحالة!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          انضم {{ referee_name }}!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          أصبحت إحالتك الآن عضوًا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          أخبار سارة! {{ referee_name }} قد зарегистрился حديثًا باستخدام رابط إحالتك.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          بمجرد أن يقوم بعملية شراء أولية، فسوف تتلقى أنت وصديقك مكافآت! سنرسل لك بريدًا إلكترونيًا آخر عندما يحدث ذلك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          ماذا يحدث بعد ذلك؟
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }} يقوم بعملية شراء أولية<br/>
          2. أنت وصديقك تتلقى المكافآت تلقائيًا<br/>
          3. يمكنك استخدام مكافآتك في أي عملية شراء مستقبلية
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          استمر في المشاركة للحصول على المزيد!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
          border="2px dashed {{ theme.color.primary|default:'#2563eb' }}"
          border-radius="8px"
          padding="15px"
          font-size="14px"
          color="{{ theme.color.primary|default:'#2563eb' }}"
          align="center"
          font-family="monospace"
        >
          {{ referral_link }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          عرض إحالاتي
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
🎉 صديقك {{ referee_name }} قد зарегистрился حديثًا!

مرحبًا {{ customer_name }},

أخبار سارة! {{ referee_name }} قد зарегистрился حديثًا باستخدام رابط إحالتك.

بمجرد أن يقوم بعملية شراء أولية، فسوف تتلقى أنت وصديقك مكافآت! سنرسل لك بريدًا إلكترونيًا آخر عندما يحدث ذلك.

ماذا يحدث بعد ذلك؟
1. {{ referee_name }} يقوم بعملية شراء أولية
2. أنت وصديقك تتلقى المكافآت تلقائيًا
3. يمكنك استخدام مكافآتك في أي عملية شراء مستقبلية

استمر في المشاركة للحصول على المزيد:
{{ referral_link }}

عرض إحالاتك: {{ referral_dashboard_url }}

{{ shop_name }}
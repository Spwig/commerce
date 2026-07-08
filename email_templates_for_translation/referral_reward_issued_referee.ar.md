---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
مرحباً! إليك مكافأتك البالغة {{ reward_amount }}

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
          🎁 هدية الترحيب!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          شكرًا لانضمامك إلينا
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 مكافأة الترحيب الخاصة بك
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          ينتهي في: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا بكم في {{ shop_name }}! قام {{ referrer_name }} بإحالتك، ونود أن نشكرك بجائزة ترحيب بقيمة {{ reward_amount }}.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          تم إضافة مكافأتك إلى حسابك وهي جاهزة للاستخدام في شراءك القادم!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          كيفية استخدام مكافأتك
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. تصفح منتجاتنا وأضف العناصر إلى سلة التسوق<br/>
          2. انتقل إلى الخروج<br/>
          3. سيتم تطبيق مكافأتك تلقائيًا<br/>
          4. استمتع بمدخراتك!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          ابدأ التسوق
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          يمكنك أيضًا كسب مكافآت!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          شارك رابط الإحالة الخاص بك مع الأصدقاء واحصل على مكافآت عندما يقومون بإجراء أول عملية شراء.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          احصل على رابط الإحالة الخاص بي
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
مرحباً! إليك مكافأتك البالغة {{ reward_amount }}

مرحبًا {{ customer_name }},

مرحبًا بكم في {{ shop_name }}! قام {{ referrer_name }} بإحالتك، ونود أن نشكرك بجائزة ترحيب بقيمة {{ reward_amount }}.

المكافأة: {{ reward_amount }}
النوع: {{ reward_type_display }}
{% if expires_at %}تنتهي في: {{ expires_at }}{% endif %}

كيفية استخدام مكافأتك:
1. تصفح منتجاتنا وأضف العناصر إلى سلة التسوق
2. انتقل إلى الخروج
3. سيتم تطبيق مكافأتك تلقائيًا
4. استمتع بمدخراتك!

ابدأ التسوق: {{ shop_url }}

يمكنك أيضًا كسب مكافآت!
شارك رابط الإحالة الخاص بك مع الأصدقاء واحصل على مكافآت عندما يقومون بإجراء أول عملية شراء.
احصل على رابط الإحالة الخاص بك: {{ my_referral_link_url }}

{{ shop_name }}
لديك أسئلة؟ اتصل بـ {{ support_email }}
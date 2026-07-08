---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
أرسل {{ referrer_name }} لك هدية!

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
          🎁 لقد تم دعوك!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} يريد مشاركة {{ shop_name }} معك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          احصل على هديتك الترحيبية
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          عند أول شراء لك
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Personal Message -->
    {% if personal_message %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" font-style="italic" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.primary|default:'#2563eb' }}">
          "{{ personal_message }}"
          <br/><br/>
          - {{ referrer_name }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          مرحبًا،
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} يعتقد أنك ستحب التسوق في {{ shop_name }}. لترحيبك، نقدم لك خصمًا قدره {{ reward_amount }} على أول شراء لك!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          فقط اضغط على الزر أدناه للبدء، وسيتم تطبيق المكافأة تلقائيًا على أول طلبك.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          كيف تعمل المكافأة
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. اضغط على الزر لزيارة {{ shop_name }}<br/>
          2. تصفح واجمِ العناصر إلى سلة التسوق الخاصة بك<br/>
          3. أكمل عملية الشراء<br/>
          4. سيتم تطبيق مكافأتك البالغة {{ reward_amount }} تلقائيًا!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          احصل على هديتي {{ reward_amount }}
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          تم إرسال هذه الدعوة من قبل {{ referrer_name }}<br/>
          لديك أسئلة؟ <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">اتصل بالدعم</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} sent you a gift!

Hi there,

{{ referrer_name }} thinks you'll love shopping at {{ shop_name }}. To welcome you, we're offering {{ reward_amount }} off your first purchase!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

How It Works:
1. Visit {{ shop_name }}
2. Browse and add items to your cart
3. Complete your purchase
4. Your {{ reward_amount }} reward is automatically applied!

Claim your gift: {{ referral_link }}

{{ shop_name }}
This invitation was sent by {{ referrer_name }}
Questions? Contact {{ support_email }}
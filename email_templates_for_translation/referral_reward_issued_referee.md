---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
Welcome! Here's your {{ reward_amount }} reward

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
          🎁 Welcome Gift!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Thanks for joining us
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 Your Welcome Reward
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          Expires: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Welcome to {{ shop_name }}! {{ referrer_name }} referred you, and we wanted to say thanks with a {{ reward_amount }} welcome reward.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Your reward has been added to your account and is ready to use on your next purchase!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          How to Use Your Reward
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. Browse our products and add items to your cart<br/>
          2. Proceed to checkout<br/>
          3. Your reward will be automatically applied<br/>
          4. Enjoy your savings!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Start Shopping
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          You Can Earn Rewards Too!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Share your own referral link with friends and earn rewards when they make their first purchase.
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          Get My Referral Link
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          Questions? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Contact Support</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Welcome! Here's your {{ reward_amount }} reward

Hi {{ customer_name }},

Welcome to {{ shop_name }}! {{ referrer_name }} referred you, and we wanted to say thanks with a {{ reward_amount }} welcome reward.

Your Reward: {{ reward_amount }}
Type: {{ reward_type_display }}
{% if expires_at %}Expires: {{ expires_at }}{% endif %}

How to Use Your Reward:
1. Browse our products and add items to your cart
2. Proceed to checkout
3. Your reward will be automatically applied
4. Enjoy your savings!

Start shopping: {{ shop_url }}

You Can Earn Rewards Too!
Share your own referral link with friends and earn rewards when they make their first purchase.
Get your referral link: {{ my_referral_link_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
Welcome to {{ shop_name }} Rewards!

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
          🎉 Welcome to Rewards!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Start earning points with every purchase
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Hi {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Welcome to the {{ shop_name }} Rewards program! You've been automatically enrolled and can start earning points right away.
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 Welcome Bonus: {{ bonus_points }} points!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Your Tier:</strong> {{ current_tier }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          {{ tier_benefits }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          How to Earn Points
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Make purchases - Earn points on every order<br/>
          • Write reviews - Share your feedback<br/>
          • Refer friends - Spread the word<br/>
          • Birthday rewards - Special points on your birthday
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          View My Rewards
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
Welcome to {{ shop_name }} Rewards!

Hi {{ customer_name }},

Welcome to the {{ shop_name }} Rewards program! You've been automatically enrolled and can start earning points right away.

{% if bonus_points %}Welcome Bonus: {{ bonus_points }} points!{% endif %}

Your Tier: {{ current_tier }}
{{ tier_benefits }}

How to Earn Points:
- Make purchases - Earn points on every order
- Write reviews - Share your feedback
- Refer friends - Spread the word
- Birthday rewards - Special points on your birthday

View your rewards: {{ account_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

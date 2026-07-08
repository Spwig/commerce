---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
Reminder: Your {{ reward_amount }} reward expires soon

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
          ⏰ Reward Expiring Soon
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
          expires in {{ days_until_expiration }} days
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          Expiration date: {{ expiration_date }}
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
          Don't let your {{ reward_amount }} referral reward go to waste! It will expire in {{ days_until_expiration }} days.
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          Use it now on your next purchase before it's too late!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>Reward Type:</strong> {{ reward_type_display }}<br/>
          <strong>Amount:</strong> {{ reward_amount }}<br/>
          <strong>Expires:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          Shop Now
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
Reminder: Your {{ reward_amount }} reward expires soon

Hi {{ customer_name }},

Don't let your {{ reward_amount }} referral reward go to waste! It will expire in {{ days_until_expiration }} days.

Reward Details:
- Type: {{ reward_type_display }}
- Amount: {{ reward_amount }}
- Expires: {{ expiration_date }}

Use it now on your next purchase before it's too late!

Shop now: {{ shop_url }}

{{ shop_name }}
Questions? Contact {{ support_email }}

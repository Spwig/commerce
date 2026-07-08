---
template_type: referral_reward_issued_referrer
category: Referral Program
---

# Email Template: referral_reward_issued_referrer

## Subject
आपने {{ reward_amount }} पुरस्कार अर्जित किया!

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
          🎉 आपने एक पुरस्कार अर्जित किया!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referee_name }} के द्वारा आपके संदर्भ लिंक के उपयोग से आपका पहला खरीदारी किया गया।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 आपका पुरस्कार
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          {{ reward_type_display }}
        </mj-text>
        {% if expires_at %}
        <mj-text font-size="13px" color="rgba(255, 255, 255, 0.9)" align="center" padding-top="5px">
          अवधि समाप्त: {{ expires_at }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          बधाई हो! {{ referee_name }} ने आपके संदर्भ लिंक के उपयोग से अपनी पहली खरीदारी की है, और आपने {{ reward_amount }} पुरस्कार अर्जित किया है!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          अपने संदर्भ लिंक को बांटते रहें और अधिक पुरस्कार अर्जित करें। आप द्वारा अधिक दोस्तों के संदर्भ करने से आप अधिक अर्जित कर सकते हैं!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Referral Stats -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="20px">
          आपके संदर्भ सांख्यिकी
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-group>
        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" line-height="1">
            {{ total_referrals }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            सफल संदर्भ
          </mj-text>
        </mj-column>

        <mj-column width="50%" background-color="{{ theme.color.background|default:'#ffffff' }}" border-radius="8px" padding="20px 10px">
          <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.success|default:'#10b981' }}" align="center" line-height="1">
            {{ total_rewards_earned }}
          </mj-text>
          <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="8px" text-transform="uppercase">
            कुल पुरस्कार
          </mj-text>
        </mj-column>
      </mj-group>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          मेरे संदर्भ देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          बांटते रहें, अधिक अर्जित करें!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background|default:'#ffffff' }}"
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
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          अपने दोस्तों के साथ इस लिंक को बांटें और अधिक पुरस्कार अर्जित करें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
आपने {{ reward_amount }} पुरस्कार अर्जित किया!

हेलो {{ customer_name }},

बधाई हो! {{ referee_name }} ने आपके संदर्भ लिंक के उपयोग से अपनी पहली खरीदारी की है, और आपने {{ reward_amount }} पुरस्कार अर्जित किया है!

आपका पुरस्कार: {{ reward_amount }}
प्रकार: {{ reward_type_display }}
{% if expires_at %}अवधि समाप्त: {{ expires_at }}{% endif %}

आपके संदर्भ सांख्यिकी:
- सफल संदर्भ: {{ total_referrals }}
- कुल पुरस्कार अर्जित: {{ total_rewards_earned }}

अपने संदर्भ लिंक को बांटते रहें और अधिक पुरस्कार अर्जित करें:
{{ referral_link }}

आपके संदर्भ देखें: {{ referral_dashboard_url }}

{{ shop_name }}
सवाल हैं? समर्थन से संपर्क करें {{ support_email }}
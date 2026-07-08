---
template_type: referral_reward_expiring
category: Referral Program
---

# Email Template: referral_reward_expiring

## Subject
स्मरण: आपका {{ reward_amount }} पुरस्कार जल्दी ही खत्म हो जाएगा

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
          ⏰ पुरस्कार जल्दी ही खत्म हो जाएगा
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
          {{ days_until_expiration }} दिन में खत्म हो जाएगा
        </mj-text>
        <mj-text font-size="14px" color="#856404" align="center" padding-top="5px">
          अंतिम तिथि: {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          अपना {{ reward_amount }} संदर्भ पुरस्कार बर्बाद न करें! यह {{ days_until_expiration }} दिन में खत्म हो जाएगा।
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          इसे अपनी अगली खरीदारी पर अब उपयोग करें, जब तक वक्त नहीं हो जाता।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>पुरस्कार प्रकार:</strong> {{ reward_type_display }}<br/>
          <strong>राशि:</strong> {{ reward_amount }}<br/>
          <strong>अंतिम तिथि:</strong> {{ expiration_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.error|default:'#ef4444' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          अब खरीदें
        </mj-button>
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
स्मरण: आपका {{ reward_amount }} पुरस्कार जल्दी ही खत्म हो जाएगा

हेलो {{ customer_name }},

अपना {{ reward_amount }} संदर्भ पुरस्कार बर्बाद न करें! यह {{ days_until_expiration }} दिन में खत्म हो जाएगा।

पुरस्कार विवरण:
- प्रकार: {{ reward_type_display }}
- राशि: {{ reward_amount }}
- अंतिम तिथि: {{ expiration_date }}

इसे अब अपनी अगली खरीदारी पर उपयोग करें, जब तक वक्त नहीं हो जाता।

अब खरीदें: {{ shop_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
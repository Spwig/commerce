---
template_type: referral_reward_issued_referee
category: Referral Program
---

# Email Template: referral_reward_issued_referee

## Subject
स्वागत है! यहाँ आपका {{ reward_amount }} रिवार्ड है

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
          🎁 स्वागत उपहार!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          हमारे साथ शामिल होने के लिए धन्यवाद
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Display -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          🎉 आपका स्वागत रिवार्ड
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
          {{ shop_name }} में स्वागत है! {{ referrer_name }} आपको संदर्भित करता है, और हम आपके लिए एक {{ reward_amount }} स्वागत रिवार्ड के साथ धन्यवाद कहना चाहते हैं।
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          आपका रिवार्ड आपके खाते में जोड़ दिया गया है और अगली खरीद पर उपयोग के लिए तैयार है!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How to Use -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          अपने रिवार्ड का उपयोग कैसे करें
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. हमारे उत्पादों की जांच करें और छोड़े गए आइटम कार्ट में जोड़ें<br/>
          2. चेकआउट प्रक्रिया के लिए आगे बढ़ें<br/>
          3. आपका रिवार्ड स्वचालित रूप से लागू किया जाएगा<br/>
          4. अपनी बचत का आनंद लीजिए!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ shop_url }}">
          खरीदारी शुरू करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Share and Earn -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          आप भी रिवार्ड कमा सकते हैं!
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          अपने दोस्तों के साथ अपना संदर्भ लिंक साझा करें और जब वे अपनी पहली खरीद करते हैं तो आप रिवार्ड कमा सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ my_referral_link_url }}">
          मेरा संदर्भ लिंक प्राप्त करें
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
स्वागत है! यहाँ आपका {{ reward_amount }} रिवार्ड है

हेलो {{ customer_name }},

{{ shop_name }} में स्वागत है! {{ referrer_name }} आपको संदर्भित करता है, और हम आपके लिए एक {{ reward_amount }} स्वागत रिवार्ड के साथ धन्यवाद कहना चाहते हैं।

आपका रिवार्ड: {{ reward_amount }}
प्रकार: {{ reward_type_display }}
{% if expires_at %}अवधि समाप्त: {{ expires_at }}{% endif %}

अपने रिवार्ड का उपयोग कैसे करें:
1. हमारे उत्पादों की जांच करें और छोड़े गए आइटम कार्ट में जोड़ें
2. चेकआउट प्रक्रिया के लिए आगे बढ़ें
3. आपका रिवार्ड स्वचालित रूप से लागू किया जाएगा
4. अपनी बचत का आनंद लीजिए!

खरीदारी शुरू करें: {{ shop_url }}

आप भी रिवार्ड कमा सकते हैं!
अपने दोस्तों के साथ अपना संदर्भ लिंक साझा करें और जब वे अपनी पहली खरीद करते हैं तो आप रिवार्ड कमा सकते हैं।
मेरा संदर्भ लिंक प्राप्त करें: {{ my_referral_link_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
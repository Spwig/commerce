---
template_type: referral_invitation
category: Referral Program
---

# Email Template: referral_invitation

## Subject
{{ referrer_name }} ने आपके लिए एक उपहार भेजा!

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
          🎁 आपके लिए एक आमंत्रण!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ referrer_name }} आपके लिए {{ shop_name }} शेयर करना चाहता है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reward Offer -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-bottom="10px">
          अपना स्वागत उपहार प्राप्त करें
        </mj-text>
        <mj-text font-size="48px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center" line-height="1">
          {{ reward_amount }}
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          अपनी पहली खरीद पर
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
          हैलो,
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ referrer_name }} सोचता है कि आपको {{ shop_name }} पर खरीदारी करना बहुत पसंद आएगा। आपका स्वागत करते हुए, हम आपकी पहली खरीद पर {{ reward_amount }} की छूट दे रहे हैं!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          नीचे दिए गए बटन पर क्लिक करके शुरू करें और आपका उपहार आपके पहले ऑर्डर पर स्वचालित रूप से लागू हो जाएगा।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- How it Works -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          कैसे काम करता है
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. बटन पर क्लिक करके {{ shop_name }} जाएं<br/>
          2. आइटम्स को अपने कार्ट में जोड़ें<br/>
          3. अपनी खरीदारी पूरी करें<br/>
          4. आपका {{ reward_amount }} उपहार स्वचालित रूप से लागू हो जाएगा!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_link }}">
          मेरा {{ reward_amount }} उपहार दावा करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}<br/>
          यह आमंत्रण {{ referrer_name }} द्वारा भेजा गया था<br/>
          सवाल हैं? <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">समर्थन से संपर्क करें</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ referrer_name }} ने आपके लिए एक उपहार भेजा!

हैलो,

{{ referrer_name }} सोचता है कि आपको {{ shop_name }} पर खरीदारी करना बहुत पसंद आएगा। आपका स्वागत करते हुए, हम आपकी पहली खरीद पर {{ reward_amount }} की छूट दे रहे हैं!

{% if personal_message %}"{{ personal_message }}"
- {{ referrer_name }}
{% endif %}

कैसे काम करता है:
1. {{ shop_name }} जाएं
2. आइटम्स को अपने कार्ट में जोड़ें
3. अपनी खरीदारी पूरी करें
4. आपका {{ reward_amount }} उपहार स्वचालित रूप से लागू हो जाएगा!

आपका उपहार दावा करें: {{ referral_link }}

{{ shop_name }}
यह आमंत्रण {{ referrer_name }} द्वारा भेजा गया था
सवाल हैं? {{ support_email }} से संपर्क करें
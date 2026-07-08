---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 {{ referee_name }} के लिए अतिरिक्त बॉनस अंक!

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 आपके द्वारा अंक अर्जित करने के लिए एक बॉनस!
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          शेयर करने के लिए धन्यवाद, {{ customer_name }}!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          अच्छी खबर! {{ referee_name }} आपके द्वारा अपने रेफरल के माध्यम से हमारे लॉयल्टी प्रोग्राम में शामिल हो गए हैं, और आपने बॉनस अंक अर्जित कर लिए हैं!
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              आपको मिला
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} अंक
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ referee_name }} के लिए रेफरल करने के लिए
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अपडेट किया गया बैलेंस:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>अंक बैलेंस:</strong> {{ total_points }} अंक<br/>
          <strong>रेफरल बॉनस:</strong> +{{ bonus_points }} अंक<br/>
          <strong>मित्र रेफरल:</strong> {{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              शेयर करते रहें, अर्जित करते रहें!
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              हर एक मित्र के शामिल होने के लिए {{ points_per_referral }} अंक अर्जित करें। कोई सीमा नहीं है!
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              अपना रेफरल लिंक शेयर करें
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          खरीदारी शुरू करें
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 रेफरल बॉनस अर्जित किया गया!

शेयर करने के लिए धन्यवाद, {{ customer_name }}!

अच्छी खबर! {{ referee_name }} आपके द्वारा अपने रेफरल के माध्यम से हमारे लॉयल्टी प्रोग्राम में शामिल हो गए हैं, और आपने बॉनस अंक अर्जित कर लिए हैं!

आपको मिला:
+{{ bonus_points }} अंक
{{ referee_name }} के लिए रेफरल करने के लिए

अपडेट किया गया बैलेंस:
- अंक बैलेंस: {{ total_points }} अंक
- रेफरल बॉनस: +{{ bonus_points }} अंक
- मित्र रेफरल: {{ total_referrals }}

शेयर करते रहें, अर्जित करते रहें!
हर एक मित्र के शामिल होने के लिए {{ points_per_referral }} अंक अर्जित करें। कोई सीमा नहीं है!

अपना रेफरल लिंक शेयर करें: {{ referral_url }}
खरीदारी शुरू करें: {{ shop_url }}
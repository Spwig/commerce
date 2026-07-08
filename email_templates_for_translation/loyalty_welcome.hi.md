---
template_type: loyalty_welcome
category: Loyalty Program
---

# Email Template: loyalty_welcome

## Subject
{{ shop_name }} पुरस्कार में आपका स्वागत है! 🎉

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
          🎉 {{ shop_name }} पुरस्कार में आपका स्वागत है!
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          प्रत्येक खरीदारी के साथ अंक अर्जित करें
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
          {{ shop_name }} पुरस्कार कार्यक्रम में आपका स्वागत है! आपको ऑटोमैटिक रूप से रजिस्टर कर दिया गया है और आप तुरंत अंक अर्जित कर सकते हैं।
        </mj-text>

        <!-- Bonus Points (if any) -->
        {% if bonus_points %}
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          <strong>🎁 स्वागत बोनस: {{ bonus_points }} अंक!</strong>
        </mj-text>
        {% endif %}

        <!-- Current Tier -->
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding="20px 0" />
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>आपका स्तर:</strong> {{ current_tier }}
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
          अंक कैसे अर्जित करें
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • खरीदारी करें - प्रत्येक ऑर्डर पर अंक अर्जित करें<br/>
          • समीक्षा लिखें - अपनी प्रतिक्रिया साझा करें<br/>
          • दोस्तों को संदेश दें - शब्द फैलाएं<br/>
          • जन्मदिन पुरस्कार - अपने जन्मदिन के दिन विशेष अंक
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ account_url }}">
          मेरे पुरस्कार देखें
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
{{ shop_name }} पुरस्कार में आपका स्वागत है!

हेलो {{ customer_name }},

{{ shop_name }} पुरस्कार कार्यक्रम में आपका स्वागत है! आपको ऑटोमैटिक रूप से रजिस्टर कर दिया गया है और आप तुरंत अंक अर्जित कर सकते हैं।

{% if bonus_points %}स्वागत बोनस: {{ bonus_points }} अंक!{% endif %}

आपका स्तर: {{ current_tier }}
{{ tier_benefits }}

अंक कैसे अर्जित करें:
- खरीदारी करें - प्रत्येक ऑर्डर पर अंक अर्जित करें
- समीक्षा लिखें - अपनी प्रतिक्रिया साझा करें
- दोस्तों को संदेश दें - शब्द फैलाएं
- जन्मदिन पुरस्कार - अपने जन्मदिन के दिन विशेष अंक

अपने पुरस्कार देखें: {{ account_url }}

{{ shop_name }}
सवाल हैं? {{ support_email }} से संपर्क करें
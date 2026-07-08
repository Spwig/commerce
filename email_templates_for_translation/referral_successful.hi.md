---
template_type: referral_successful
category: Referral Program
---

# Email Template: referral_successful

## Subject
🎉 आपका दोस्त {{ referee_name }} अब रजिस्टर हो गए!

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
          🎉 रेफरल सफलता!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Success Banner -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          {{ referee_name }} शामिल हो गए!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          आपका रेफरल अब एक सदस्य है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हैलो {{ customer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          अच्छी खबर! {{ referee_name }} आपके रेफरल लिंक के उपयोग से अब रजिस्टर हो गए।
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          जब वे अपनी पहली खरीद करते हैं, तो आप दोनों पुरस्कार प्राप्त करेंगे! जब ऐसा होता है, तो हम आपको एक अन्य ईमेल भेजेंगे।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="10px">
          अगला क्या होगा?
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          1. {{ referee_name }} अपनी पहली खरीद करते हैं<br/>
          2. आप दोनों अपने पुरस्कार को स्वचालित रूप से प्राप्त करते हैं<br/>
          3. आप अपने पुरस्कार को किसी भी भविष्य की खरीद पर उपयोग कर सकते हैं
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Keep Sharing -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center" padding-bottom="15px">
          अधिक कमाने के लिए अधिक साझा करें!
        </mj-text>
        <mj-text
          background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}"
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
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ referral_dashboard_url }}">
          मेरे रेफरल देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          {{ shop_name }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 आपका दोस्त {{ referee_name }} अब रजिस्टर हो गए!

हैलो {{ customer_name }},

अच्छी खबर! {{ referee_name }} आपके रेफरल लिंक के उपयोग से अब रजिस्टर हो गए।

जब वे अपनी पहली खरीद करते हैं, तो आप दोनों पुरस्कार प्राप्त करेंगे! जब ऐसा होता है, तो हम आपको एक अन्य ईमेल भेजेंगे।

अगला क्या होगा?
1. {{ referee_name }} अपनी पहली खरीद करते हैं
2. आप दोनों अपने पुरस्कार को स्वचालित रूप से प्राप्त करते हैं
3. आप अपने पुरस्कार को किसी भी भविष्य की खरीद पर उपयोग कर सकते हैं

अधिक कमाने के लिए अधिक साझा करें:
{{ referral_link }}

अपने रेफरल देखें: {{ referral_dashboard_url }}

{{ shop_name }}
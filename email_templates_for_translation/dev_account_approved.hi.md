---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
स्पविग डेवलपर प्रोग्राम में आपका स्वागत है, {{ developer_name }}!

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          स्पविग में आपका स्वागत है!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          आपके डेवलपर आवेदन को अनुमोदित कर दिया गया है
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          हेलो {{ developer_name }},
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          बधाई हो! आपके डेवलपर आवेदन को अनुमोदित कर दिया गया है। अब आपके पास स्पविग डेवलपर पोर्टल के पूर्ण पहुँच है।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          आपका मुफ्त डेवलपर लाइसेंस इंतजार कर रहा है
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          एक अनुमोदित डेवलपर के रूप में, आपको एक <strong>मुफ्त स्पविग शॉप + पॉज़ इंस्टॉलेशन</strong> मिलता है जिसमें अपडेट लगातार होते रहते हैं। अपना लाइसेंस दावा करें, अपने सर्वर पर स्पविग को इंस्टॉल करें, और तुरंत कम्पोनेंट्स बनाना शुरू करें।
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          मुफ्त लाइसेंस दावा करें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          शुरू करें:
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> अपना मुफ्त डेवलपर लाइसेंस दावा करें
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> अपने सर्वर पर स्पविग को इंस्टॉल करें
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> हमारे SDKs के उपयोग से अपना पहला कम्पोनेंट बनाएं
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> अपने डैशबोर्ड से इसे सबमिट करें
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          डैशबोर्ड पर जाएं
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>स्पविग डेवलपर पोर्टल</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          प्रश्न हैं? डेवलपर समर्थन से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
हेलो {{ developer_name }},

बधाई हो! आपके डेवलपर आवेदन को अनुमोदित कर दिया गया है। अब आपके पास स्पविग डेवलपर पोर्टल के पूर्ण पहुँच है।

आपका मुफ्त डेवलपर लाइसेंस इंतजार कर रहा है
एक अनुमोदित डेवलपर के रूप में, आपको एक मुफ्त स्पविग शॉप + पॉज़ इंस्टॉलेशन मिलता है जिसमें अपडेट लगातार होते रहते हैं। अपना लाइसेंस दावा करें, अपने सर्वर पर स्पविग को इंस्टॉल करें, और तुरंत कम्पोनेंट्स बनाना शुरू करें।

मुफ्त लाइसेंस दावा करें: {{ license_url }}

शुरू करें:
1. मुफ्त डेवलपर लाइसेंस दावा करें: {{ license_url }}
2. अपने सर्वर पर स्पविग को इंस्टॉल करें
3. हमारे SDKs के उपयोग से अपना पहला कम्पोनेंट बनाएं
4. अपने डैशबोर्ड से इसे सबमिट करें

डैशबोर्ड पर जाएं: {{ dashboard_url }}

---
स्पविग डेवलपर पोर्टल
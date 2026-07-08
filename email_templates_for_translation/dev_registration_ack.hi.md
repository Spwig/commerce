---
template_type: dev_registration_ack
category: Developer Portal
---

# Email Template: dev_registration_ack

## Subject
हमने आपके डेवलपर आवेदन को प्राप्त कर लिया, {{ developer_name }}

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
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          आवेदन प्राप्त!
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          हम आपके डेवलपर आवेदन की जांच कर रहे हैं
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
          आपके द्वारा Spwig डेवलपर प्रोग्राम में आवेदन के लिए धन्यवाद। हमने आपके आवेदन को प्राप्त कर लिया है और हमारी टीम इसकी जल्दी जांच करेगी।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What's Next Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          अगला क्या होगा?
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> हमारी टीम आपके आवेदन की जांच करती है (आमतौर पर 2-3 व्यावसायिक दिन)
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> आप हमारे फैसले के साथ एक ईमेल प्राप्त करेंगे
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>3.</strong> एक बार अनुमोदित, आपको डेवलपर डैशबोर्ड के पूर्ण पहुँच मिल जाएगा
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ portal_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          डेवलपर पोर्टल देखें
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig डेवलपर पोर्टल</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          सवाल हैं? डेवलपर समर्थन से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
हेलो {{ developer_name }},

Spwig डेवलपर प्रोग्राम में आवेदन के लिए धन्यवाद। हमने आपके आवेदन को प्राप्त कर लिया है और हमारी टीम इसकी जल्दी जांच करेगी।

अगला क्या होगा?
1. हमारी टीम आपके आवेदन की जांच करती है (आमतौर पर 2-3 व्यावसायिक दिन)
2. आप हमारे फैसले के साथ एक ईमेल प्राप्त करेंगे
3. एक बार अनुमोदित, आपको डेवलपर डैशबोर्ड के पूर्ण पहुँच मिल जाएगा

डेवलपर पोर्टल देखें: {{ portal_url }}

---
Spwig डेवलपर पोर्टल
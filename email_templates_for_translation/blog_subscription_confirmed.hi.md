---
template_type: blog_subscription_confirmed
category: Blog
---

# Email Template: blog_subscription_confirmed

## Subject
अपने सदस्यता की पुष्टि करें {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अपने सदस्यता की पुष्टि करें
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          हैलो {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ blog_name }} के लिए आपकी सदस्यता के लिए धन्यवाद! अपनी सदस्यता को पूरा करने और अपडेट्स प्राप्त करना शुरू करने के लिए, कृपया अपना ईमेल पता पुष्टि करें।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          सदस्यता की पुष्टि करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              बटन क्लिक नहीं कर सकते? अपने ब्राउज़र में इस लिंक की कॉपी और पेस्ट करें:
              <br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>क्यों पुष्टि करें?</strong><br/>
          ईमेल पुष्टि हमें आपको अपडेट्स प्राप्त करने की इच्छा बताती है और स्पैम को रोकती है। आपकी गोपनीयता और ईमेल डिब्बा हमारे लिए महत्वपूर्ण है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          सदस्यता नहीं ली? आप इस ईमेल को आसानी से अनदेखा कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
अपने सदस्यता की पुष्टि करें

हैलो {{ subscriber_name }},

{{ blog_name }} के लिए आपकी सदस्यता के लिए धन्यवाद! अपनी सदस्यता को पूरा करने और अपडेट्स प्राप्त करना शुरू करने के लिए, कृपया अपना ईमेल पता पुष्टि करें।

सदस्यता की पुष्टि करें: {{ confirmation_url }}

क्यों पुष्टि करें?
ईमेल पुष्टि हमें आपको अपडेट्स प्राप्त करने की इच्छा बताती है और स्पैम को रोकती है। आपकी गोपनीयता और ईमेल डिब्बा हमारे लिए महत्वपूर्ण है।

सदस्यता नहीं ली? आप इस ईमेल को आसानी से अनदेखा कर सकते हैं।

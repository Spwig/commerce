---
template_type: newsletter_signup_confirm
category: Newsletter
---

# Email Template: newsletter_signup_confirm

## Subject
कृपया {{ store_name }} की अपनी सदस्यता की पुष्टि करें

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          अपनी सदस्यता की पुष्टि करें
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ store_name }} से सुनने के लिए साइन अप करने के लिए धन्यवाद! हमारे अपडेट और ऑफर प्राप्त करना शुरू करने के लिए कृपया अपनी ईमेल पता की पुष्टि करें।
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ confirmation_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="18px" font-weight="bold" border-radius="6px" padding="18px 50px">
          सदस्यता की पुष्टि करें
        </mj-button>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              बटन पर क्लिक नहीं कर पा रहे? इस लिंक को कॉपी करें और अपने ब्राउज़र में पेस्ट करें:<br/>
              <span style="color: {{ theme.color.primary|default:'#2563eb' }}; font-family: 'Courier New', monospace;">{{ confirmation_url }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>पुष्टि क्यों करें?</strong><br/>
          अपनी ईमेल की पुष्टि करने से हमें यह सुनिश्चित करने में मदद मिलती है कि आप वास्तव में हमारे अपडेट चाहते हैं, और यह आपके इनबॉक्स को स्पैम-मुक्त रखता है।
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          साइन अप नहीं किया? आप इस ईमेल को सुरक्षित रूप से अनदेखा कर सकते हैं।
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
{{ store_name }} की अपनी सदस्यता की पुष्टि करें

{{ store_name }} से सुनने के लिए साइन अप करने के लिए धन्यवाद! हमारे अपडेट और ऑफर प्राप्त करना शुरू करने के लिए कृपया अपनी ईमेल पता की पुष्टि करें:

{{ confirmation_url }}

अपनी ईमेल की पुष्टि करने से हमें यह सुनिश्चित करने में मदद मिलती है कि आप वास्तव में हमारे अपडेट चाहते हैं, और यह आपके इनबॉक्स को स्पैम-मुक्त रखता है।

साइन अप नहीं किया? आप इस ईमेल को सुरक्षित रूप से अनदेखा कर सकते हैं।
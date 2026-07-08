---
template_type: dev_account_suspended
category: Developer Portal
---

# Email Template: dev_account_suspended

## Subject
आपका Spwig डेवलपर अकाउंट रोक दिया गया है

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Warning Accent -->
    <mj-section background-color="{{ theme.color.warning|default:'#f59e0b' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          अकाउंट रोक दिया गया है
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          आपके डेवलपर अकाउंट के बारे में महत्वपूर्ण अपडेट
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
          आपका Spwig डेवलपर अकाउंट रोक दिया गया है। इस अवधि के दौरान आपके द्वारा प्रकाशित कम्पोनेंट्स उपलब्ध रहेंगे लेकिन आप नए कम्पोनेंट्स या अपडेट्स को भेज नहीं सकते।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reason Section (if provided) -->
    {% if suspension_reason %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          कारण:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.warning|default:'#f59e0b' }}">
          {{ suspension_reason }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          यदि आपको लगता है कि यह गलत तौर पर किया गया है, तो कृपया हमें <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; text-decoration: none;">{{ support_email }}</a> पर संपर्क करें।
        </mj-text>
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
          प्रश्न हैं? डेवलपर समर्थन से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
हेलो {{ developer_name }},

आपका Spwig डेवलपर अकाउंट रोक दिया गया है। इस अवधि के दौरान आपके द्वारा प्रकाशित कम्पोनेंट्स उपलब्ध रहेंगे लेकिन आप नए कम्पोनेंट्स या अपडेट्स को भेज नहीं सकते।

{% if suspension_reason %}कारण: {{ suspension_reason }}{% endif %}

यदि आपको लगता है कि यह गलत तौर पर किया गया है, तो कृपया हमें {{ support_email }} पर संपर्क करें।

---
Spwig डेवलपर पोर्टल
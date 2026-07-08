---
template_type: dev_account_rejected
category: Developer Portal
---

# Email Template: dev_account_rejected

## Subject
आपके Spwig डेवलपर आवेदन के अपडेट

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
          आवेदन अपडेट
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          आपके Spwig डेवलपर आवेदन के अपडेट
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
          Spwig डेवलपर प्रोग्राम में आपके द्वारा दिखाए गए रुचि के लिए धन्यवाद। ध्यानपूर्वक समीक्षा के बाद, हम इस समय आपके आवेदन को अनुमोदित करने में असमर्थ हैं।
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reason Section (if provided) -->
    {% if rejection_reason %}
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          कारण:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="15px" background-color="{{ theme.color.background|default:'#ffffff' }}" border-left="3px solid {{ theme.color.error|default:'#ef4444' }}">
          {{ rejection_reason }}
        </mj-text>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Support Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          यदि आपके पास प्रश्न हैं या आपको लगता है कि यह गलत तैयार किया गया है, तो कृपया हमें <a href="mailto:{{ support_email }}" style="color: {{ theme.color.primary|default:'#2563eb' }}; text-decoration: none;">{{ support_email }}</a> पर संपर्क करें।
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
          प्रश्न? डेवलपर समर्थन से संपर्क करें
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
हेलो {{ developer_name }},

Spwig डेवलपर प्रोग्राम में आपके द्वारा दिखाए गए रुचि के लिए धन्यवाद। ध्यानपूर्वक समीक्षा के बाद, हम इस समय आपके आवेदन को अनुमोदित करने में असमर्थ हैं।

{% if rejection_reason %}कारण: {{ rejection_reason }}{% endif %}

यदि आपके पास प्रश्न हैं या आपको लगता है कि यह गलत तैयार किया गया है, तो कृपया हमें {{ support_email }} पर संपर्क करें।

---
Spwig डेवलपर पोर्टल